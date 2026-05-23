#!/usr/bin/env python3
"""
a2a-client.py — A2A v1.0 client for calling out to external A2A agents.

Implements Tier 3 of A2A support per A2A.md: outbound calls from our agents to
other A2A v1.0-compliant agents. The client handles:

  - Agent Card discovery (GET /.well-known/agent-card.json)
  - Agent Card validation against the v1.0 shape
  - Sync send-and-wait via message/send
  - SSE streaming via message/stream
  - Task lifecycle (tasks/get, tasks/cancel)
  - Bearer-token auth (per A2A_BEARER env-var or constructor arg)
  - Retry-on-5xx with capped exponential backoff

Programmatic use:
    from scripts.a2a_client import A2AClient
    async with A2AClient("http://localhost:8000") as client:
        card = await client.discover()
        task = await client.send(skill_id="advise", text="should I ship llms.txt?")
        print(task["artifacts"][0]["parts"][0]["text"])

CLI:
    python3 scripts/a2a-client.py http://localhost:8000 discover
    python3 scripts/a2a-client.py http://localhost:8000 send --skill advise --text "..."
    python3 scripts/a2a-client.py http://localhost:8000 stream --skill audit --text "..."
    python3 scripts/a2a-client.py http://localhost:8000 list

References:
  - A2A v1.0 spec: https://a2a-protocol.org/latest/specification/
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import uuid
from typing import Any, AsyncIterator, Optional

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. pip install httpx", file=sys.stderr)
    sys.exit(1)


# --- Exceptions ----------------------------------------------------------


class A2AError(Exception):
    """Base for client-side A2A errors."""


class A2AHttpError(A2AError):
    """HTTP-layer error (network, 4xx, 5xx)."""

    def __init__(self, status: int, body: str) -> None:
        super().__init__(f"HTTP {status}: {body[:200]}")
        self.status = status
        self.body = body


class A2ARpcError(A2AError):
    """JSON-RPC layer error (parse, method-not-found, server-defined)."""

    def __init__(self, code: int, message: str, data: Any = None) -> None:
        super().__init__(f"RPC error {code}: {message}")
        self.code = code
        self.rpc_message = message
        self.data = data


class A2AValidationError(A2AError):
    """Agent Card failed validation."""


# --- Validation ----------------------------------------------------------


def validate_agent_card(card: dict[str, Any]) -> None:
    """Sanity-check a fetched Agent Card. Not a full schema validator —
    just enough to catch the obvious "this isn't an A2A card" cases.
    """
    required_fields = ["name", "protocolVersion", "skills"]
    missing = [f for f in required_fields if f not in card]
    if missing:
        raise A2AValidationError(f"Agent Card missing required fields: {missing}")

    if not isinstance(card["skills"], list):
        raise A2AValidationError("Agent Card 'skills' must be a list")

    for i, skill in enumerate(card["skills"]):
        if "id" not in skill:
            raise A2AValidationError(f"Skill #{i} missing required 'id'")

    if not str(card["protocolVersion"]).startswith("1."):
        raise A2AValidationError(
            f"Unsupported protocolVersion: {card['protocolVersion']} (this client supports 1.x)"
        )


# --- The client ----------------------------------------------------------


class A2AClient:
    """Async A2A v1.0 client.

    Use as an async context manager so the underlying httpx.AsyncClient is
    cleaned up properly:

        async with A2AClient(base_url) as client:
            await client.discover()
            task = await client.send("advise", "hello")
    """

    def __init__(
        self,
        base_url: str,
        bearer_token: Optional[str] = None,
        timeout: float = 30.0,
        retries: int = 3,
        rpc_path: str = "/a2a",
        card_path: str = "/.well-known/agent-card.json",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.bearer = bearer_token or os.environ.get("A2A_BEARER")
        self.timeout = timeout
        self.retries = retries
        self.rpc_path = rpc_path
        self.card_path = card_path
        self._client: Optional[httpx.AsyncClient] = None
        self._agent_card: Optional[dict[str, Any]] = None

    async def __aenter__(self) -> A2AClient:
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.bearer:
            h["Authorization"] = f"Bearer {self.bearer}"
        return h

    async def _http(self, method: str, path: str, **kwargs) -> httpx.Response:
        assert self._client is not None, "Use as async context manager"
        url = self.base_url + path
        last_exc: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            try:
                r = await self._client.request(method, url, **kwargs)
                if r.status_code >= 500 and attempt < self.retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                return r
            except httpx.HTTPError as e:
                last_exc = e
                if attempt >= self.retries:
                    break
                await asyncio.sleep(min(2**attempt, 8))
        raise A2AHttpError(0, str(last_exc) if last_exc else "request failed")

    # --- Public API ---

    async def discover(self) -> dict[str, Any]:
        """Fetch and validate the Agent Card.

        Returns the parsed card. Raises A2AValidationError if it doesn't look
        like a v1.x A2A Agent Card.
        """
        r = await self._http("GET", self.card_path, headers={"Accept": "application/json"})
        if r.status_code != 200:
            raise A2AHttpError(r.status_code, r.text)
        try:
            card = r.json()
        except json.JSONDecodeError as e:
            raise A2AValidationError(f"Agent Card is not valid JSON: {e}")
        validate_agent_card(card)
        self._agent_card = card
        return card

    async def list_skills(self) -> list[dict[str, Any]]:
        """Return the skill list from the Agent Card (discovers if needed)."""
        if self._agent_card is None:
            await self.discover()
        return self._agent_card["skills"]  # type: ignore[index]

    async def send(
        self,
        skill: str,
        text: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """message/send — submit a task and wait for the completed result.

        Returns the completed Task dict (with artifacts populated). Raises
        A2ARpcError if the server returned a JSON-RPC error.
        """
        params = {
            "message": {"role": "user", "parts": [{"kind": "text", "text": text}]},
            "metadata": {"skill": skill, **(metadata or {})},
        }
        return await self._rpc("message/send", params)

    async def stream(
        self,
        skill: str,
        text: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """message/stream — submit a task and yield SSE events as they arrive.

        Each yielded dict is a JSON-RPC envelope ({"result": {...}} or
        {"error": {...}}). Stops when the server closes the connection.
        """
        assert self._client is not None, "Use as async context manager"
        rpc_id = str(uuid.uuid4())
        body = {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "method": "message/stream",
            "params": {
                "message": {"role": "user", "parts": [{"kind": "text", "text": text}]},
                "metadata": {"skill": skill, **(metadata or {})},
            },
        }
        url = self.base_url + self.rpc_path
        headers = {**self._headers(), "Accept": "text/event-stream"}
        async with self._client.stream(
            "POST", url, json=body, headers=headers, timeout=self.timeout
        ) as r:
            if r.status_code != 200:
                body_text = await r.aread()
                raise A2AHttpError(r.status_code, body_text.decode("utf-8", "replace"))
            buf = ""
            async for chunk in r.aiter_text():
                buf += chunk
                while "\n\n" in buf:
                    event, buf = buf.split("\n\n", 1)
                    for line in event.split("\n"):
                        if line.startswith("data: "):
                            payload = line[6:].strip()
                            if not payload:
                                continue
                            try:
                                yield json.loads(payload)
                            except json.JSONDecodeError:
                                continue

    async def get_task(self, task_id: str) -> dict[str, Any]:
        return await self._rpc("tasks/get", {"id": task_id})

    async def cancel_task(self, task_id: str) -> dict[str, Any]:
        return await self._rpc("tasks/cancel", {"id": task_id})

    async def list_tasks(self, limit: int = 50) -> dict[str, Any]:
        return await self._rpc("tasks/list", {"limit": limit})

    # --- Internal ---

    async def _rpc(self, method: str, params: dict[str, Any]) -> Any:
        rpc_id = str(uuid.uuid4())
        body = {"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params}
        r = await self._http("POST", self.rpc_path, json=body, headers=self._headers())
        if r.status_code != 200:
            raise A2AHttpError(r.status_code, r.text)
        try:
            envelope = r.json()
        except json.JSONDecodeError as e:
            raise A2AHttpError(r.status_code, f"Server returned non-JSON: {e}")
        if "error" in envelope:
            err = envelope["error"]
            raise A2ARpcError(
                err.get("code", -1),
                err.get("message", "unknown error"),
                err.get("data"),
            )
        return envelope.get("result")


# --- CLI -----------------------------------------------------------------


def _print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2))


async def _cmd_discover(base_url: str, bearer: Optional[str]) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        card = await client.discover()
        _print_json(
            {
                "name": card.get("name"),
                "version": card.get("version"),
                "protocolVersion": card.get("protocolVersion"),
                "skillCount": len(card.get("skills", [])),
                "skills": [s["id"] for s in card.get("skills", [])],
                "capabilities": card.get("capabilities", {}),
            }
        )
    return 0


async def _cmd_send(
    base_url: str, bearer: Optional[str], skill: str, text: str, raw: bool
) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        task = await client.send(skill, text)
        if raw:
            _print_json(task)
        else:
            print(f"Task ID: {task['id']}")
            print(f"State:   {task['status']['state']}")
            print("=" * 60)
            for art in task.get("artifacts", []):
                for part in art.get("parts", []):
                    if part.get("kind", "text") == "text":
                        print(part.get("text", ""))
    return 0


async def _cmd_stream(
    base_url: str, bearer: Optional[str], skill: str, text: str
) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        last_state = None
        printed = 0
        async for event in client.stream(skill, text):
            result = event.get("result", {})
            err = event.get("error")
            if err:
                print(f"\n[error] {err}", file=sys.stderr)
                return 1
            state = result.get("state")
            if state and state != last_state:
                print(f"\n[{state}]", end="", flush=True)
                last_state = state
            delta = result.get("delta", {})
            if delta.get("kind") == "text":
                print(delta.get("text", ""), end="", flush=True)
                printed += 1
        if printed == 0:
            print("(no streamed text)")
        else:
            print()
    return 0


async def _cmd_get(base_url: str, bearer: Optional[str], task_id: str) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        _print_json(await client.get_task(task_id))
    return 0


async def _cmd_cancel(base_url: str, bearer: Optional[str], task_id: str) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        _print_json(await client.cancel_task(task_id))
    return 0


async def _cmd_list(base_url: str, bearer: Optional[str], limit: int) -> int:
    async with A2AClient(base_url, bearer_token=bearer) as client:
        _print_json(await client.list_tasks(limit=limit))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="A2A v1.0 client (Tier 3).")
    parser.add_argument("base_url", help="Base URL of the A2A agent, e.g. http://localhost:8000")
    parser.add_argument(
        "--bearer",
        default=os.environ.get("A2A_BEARER"),
        help="Bearer token (or set A2A_BEARER env-var)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("discover", help="Fetch and validate the Agent Card")

    p_send = sub.add_parser("send", help="Send a message and wait for completion")
    p_send.add_argument("--skill", required=True, help="Skill id to invoke")
    p_send.add_argument("--text", required=True, help="Message text")
    p_send.add_argument("--raw", action="store_true", help="Print full task JSON")

    p_stream = sub.add_parser("stream", help="Send a message and stream the response")
    p_stream.add_argument("--skill", required=True, help="Skill id to invoke")
    p_stream.add_argument("--text", required=True, help="Message text")

    p_get = sub.add_parser("get", help="Get a task by ID")
    p_get.add_argument("task_id")

    p_cancel = sub.add_parser("cancel", help="Cancel a task")
    p_cancel.add_argument("task_id")

    p_list = sub.add_parser("list", help="List recent tasks")
    p_list.add_argument("--limit", type=int, default=20)

    args = parser.parse_args(argv)

    try:
        if args.cmd == "discover":
            return asyncio.run(_cmd_discover(args.base_url, args.bearer))
        if args.cmd == "send":
            return asyncio.run(
                _cmd_send(args.base_url, args.bearer, args.skill, args.text, args.raw)
            )
        if args.cmd == "stream":
            return asyncio.run(
                _cmd_stream(args.base_url, args.bearer, args.skill, args.text)
            )
        if args.cmd == "get":
            return asyncio.run(_cmd_get(args.base_url, args.bearer, args.task_id))
        if args.cmd == "cancel":
            return asyncio.run(_cmd_cancel(args.base_url, args.bearer, args.task_id))
        if args.cmd == "list":
            return asyncio.run(_cmd_list(args.base_url, args.bearer, args.limit))
        parser.print_help()
        return 2
    except A2AError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
