#!/usr/bin/env python3
"""
a2a-server.py — Production-grade A2A v1.0 server endpoint for llms-txt-advisor.

Implements the Tier 2 of A2A support per A2A.md:
  - Serves the static Agent Card at /.well-known/agent-card.json
  - Accepts JSON-RPC 2.0 over HTTP at /a2a
  - Methods: message/send, message/stream, tasks/get, tasks/cancel, tasks/list
  - SQLite-backed task persistence (survives restarts)
  - Bearer-token authentication (configurable via A2A_API_KEYS env-var)
  - Per-key in-memory token-bucket rate limiting
  - SSE streaming for long-running tasks
  - Audit logging (one JSON line per request)
  - Two modes:
      mock (default, no API key needed): skill-aware canned responses for testing
      live (requires ANTHROPIC_API_KEY): real Claude calls with SKILL.md as system prompt

Usage (mock mode — no API key):
  python3 scripts/a2a-server.py

Usage (live mode):
  export ANTHROPIC_API_KEY=sk-ant-...
  export A2A_MODE=live
  export A2A_API_KEYS="caller1=secret1,caller2=secret2"     # optional bearer auth
  python3 scripts/a2a-server.py --port 8000

Environment variables:
  A2A_MODE           mock|live           default: mock
  A2A_DB_PATH        path to SQLite DB   default: ./a2a-tasks.db (in $PWD)
  A2A_API_KEYS       caller=key pairs    default: unset (auth disabled)
  A2A_RATE_LIMIT     reqs per minute     default: 30
  A2A_AUDIT_LOG      path to JSONL file  default: ./a2a-audit.log
  ANTHROPIC_API_KEY  required if live    default: unset
  A2A_MODEL          Claude model        default: claude-sonnet-4-5-20250929

References:
  - A2A v1.0 spec: https://a2a-protocol.org/latest/specification/
  - JSON-RPC 2.0: https://www.jsonrpc.org/specification
  - SSE: https://html.spec.whatwg.org/multipage/server-sent-events.html
"""

import argparse
import asyncio
import contextlib
import json
import logging
import os
import sqlite3
import sys
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, AsyncIterator, Optional

# --- Constants and paths -------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
AGENT_CARD_PATH = ROOT / ".well-known" / "agent-card.json"
SKILLS_DIR = ROOT / "skills"

DEFAULT_DB_PATH = Path(os.environ.get("A2A_DB_PATH", "./a2a-tasks.db")).resolve()
DEFAULT_AUDIT_LOG = Path(os.environ.get("A2A_AUDIT_LOG", "./a2a-audit.log")).resolve()
DEFAULT_RATE_LIMIT = int(os.environ.get("A2A_RATE_LIMIT", "30"))
DEFAULT_MODEL = os.environ.get("A2A_MODEL", "claude-sonnet-4-6")

# Per-skill max_tokens budgets — generate is by far the most output-heavy
# (full llms.txt file). Override globally via A2A_MAX_TOKENS env-var; this
# table sets defaults that match what each skill actually produces.
SKILL_MAX_TOKENS: dict[str, int] = {
    "generate":             16000,
    "cold-start-interview":  8000,
    "audit":                 8000,
    "customize":             6000,
    "stakeholder-comms":     4000,
    "deploy":                4000,
    "advise":                4000,
    "setup-recommender":     2000,
}
DEFAULT_MAX_TOKENS = int(os.environ.get("A2A_MAX_TOKENS", "8000"))
DEFAULT_MODE = os.environ.get("A2A_MODE", "mock").lower()

# JSON-RPC 2.0 error codes (per spec)
ERR_PARSE = -32700
ERR_INVALID_REQUEST = -32600
ERR_METHOD_NOT_FOUND = -32601
ERR_INVALID_PARAMS = -32602
ERR_INTERNAL = -32603
ERR_UNAUTHORIZED = -32001  # Server-defined
ERR_RATE_LIMITED = -32002
ERR_TASK_NOT_FOUND = -32003
ERR_TERMINAL_STATE = -32004

# A2A task states (per v1.0 spec)
STATE_SUBMITTED = "submitted"
STATE_WORKING = "working"
STATE_INPUT_REQUIRED = "input-required"
STATE_COMPLETED = "completed"
STATE_FAILED = "failed"
STATE_CANCELED = "canceled"

TERMINAL_STATES = {STATE_COMPLETED, STATE_FAILED, STATE_CANCELED}


# --- Pre-flight ----------------------------------------------------------

if not AGENT_CARD_PATH.exists():
    print(f"ERROR: agent-card.json not found at {AGENT_CARD_PATH}", file=sys.stderr)
    print("Run from plugin root after Tier 1 is in place.", file=sys.stderr)
    sys.exit(1)

with open(AGENT_CARD_PATH) as f:
    AGENT_CARD: dict[str, Any] = json.load(f)

SKILL_IDS: set[str] = {s["id"] for s in AGENT_CARD["skills"]}
SKILL_BY_ID: dict[str, dict[str, Any]] = {s["id"]: s for s in AGENT_CARD["skills"]}


# --- Logging -------------------------------------------------------------

logger = logging.getLogger("a2a")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


# --- Auth: parse A2A_API_KEYS ------------------------------------------

def _parse_api_keys() -> dict[str, str]:
    """Parse `A2A_API_KEYS=name1=key1,name2=key2` into a {key: name} mapping.

    If unset or empty, auth is disabled (anyone can call). In production, ALWAYS set
    this env-var and use real per-caller credentials.
    """
    raw = os.environ.get("A2A_API_KEYS", "").strip()
    if not raw:
        return {}
    out: dict[str, str] = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair or "=" not in pair:
            continue
        name, key = pair.split("=", 1)
        out[key.strip()] = name.strip()
    return out


# --- Rate limiter --------------------------------------------------------

class TokenBucket:
    """Per-key sliding-window rate limiter (in-memory).

    Production: replace with Redis-backed limiter (e.g., redis-py + sliding-window-log).
    """

    def __init__(self, requests_per_minute: int = DEFAULT_RATE_LIMIT) -> None:
        self.rpm = requests_per_minute
        self.window: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        cutoff = now - 60.0
        q = self.window[key]
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= self.rpm:
            return False
        q.append(now)
        return True


# --- SQLite task store ---------------------------------------------------

class TaskStore:
    """SQLite-backed task store implementing the A2A task lifecycle.

    Schema:
      tasks(id TEXT PK, skill TEXT, state TEXT, history JSON, artifacts JSON,
            metadata JSON, caller TEXT, created REAL, updated REAL)
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_schema()

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def _init_schema(self) -> None:
        with self._conn() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    skill TEXT NOT NULL,
                    state TEXT NOT NULL,
                    history TEXT NOT NULL DEFAULT '[]',
                    artifacts TEXT NOT NULL DEFAULT '[]',
                    metadata TEXT NOT NULL DEFAULT '{}',
                    caller TEXT,
                    created REAL NOT NULL,
                    updated REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_tasks_caller ON tasks(caller);
                CREATE INDEX IF NOT EXISTS idx_tasks_state ON tasks(state);
            """)

    def create(self, skill: str, message: dict[str, Any], caller: Optional[str] = None) -> str:
        task_id = str(uuid.uuid4())
        now = time.time()
        with self._conn() as c:
            c.execute(
                "INSERT INTO tasks(id, skill, state, history, artifacts, metadata, caller, created, updated) "
                "VALUES(?, ?, ?, ?, '[]', '{}', ?, ?, ?)",
                (
                    task_id,
                    skill,
                    STATE_SUBMITTED,
                    json.dumps([message]),
                    caller,
                    now,
                    now,
                ),
            )
        return task_id

    def get(self, task_id: str, caller: Optional[str] = None) -> Optional[dict[str, Any]]:
        with self._conn() as c:
            row = c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row is None:
                return None
            if caller is not None and row["caller"] not in (None, caller):
                # Caller isolation: a key can only see its own tasks.
                return None
            return self._row_to_task(row)

    def update_state(self, task_id: str, state: str) -> None:
        with self._conn() as c:
            c.execute(
                "UPDATE tasks SET state = ?, updated = ? WHERE id = ?",
                (state, time.time(), task_id),
            )

    def append_artifact(self, task_id: str, artifact: dict[str, Any]) -> None:
        with self._conn() as c:
            row = c.execute("SELECT artifacts FROM tasks WHERE id = ?", (task_id,)).fetchone()
            arts = json.loads(row["artifacts"]) if row else []
            arts.append(artifact)
            c.execute(
                "UPDATE tasks SET artifacts = ?, updated = ? WHERE id = ?",
                (json.dumps(arts), time.time(), task_id),
            )

    def append_history(self, task_id: str, message: dict[str, Any]) -> None:
        with self._conn() as c:
            row = c.execute("SELECT history FROM tasks WHERE id = ?", (task_id,)).fetchone()
            hist = json.loads(row["history"]) if row else []
            hist.append(message)
            c.execute(
                "UPDATE tasks SET history = ?, updated = ? WHERE id = ?",
                (json.dumps(hist), time.time(), task_id),
            )

    def list_for_caller(self, caller: Optional[str], limit: int = 50) -> list[dict[str, Any]]:
        with self._conn() as c:
            if caller is None:
                rows = c.execute(
                    "SELECT * FROM tasks ORDER BY created DESC LIMIT ?", (limit,)
                ).fetchall()
            else:
                rows = c.execute(
                    "SELECT * FROM tasks WHERE caller IS NULL OR caller = ? "
                    "ORDER BY created DESC LIMIT ?",
                    (caller, limit),
                ).fetchall()
            return [self._row_to_task(r) for r in rows]

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "status": {"state": row["state"]},
            "history": json.loads(row["history"]),
            "artifacts": json.loads(row["artifacts"]),
            "metadata": json.loads(row["metadata"]),
            "created": row["created"],
            "updated": row["updated"],
        }


# --- Audit logger --------------------------------------------------------

class AuditLog:
    """One JSON line per request. Append-only. Tail with `tail -f`."""

    def __init__(self, path: Path) -> None:
        self.path = path
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def log(self, event: dict[str, Any]) -> None:
        event = {"ts": time.time(), **event}
        try:
            with open(self.path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            logger.warning("audit log failed: %s", e)


# --- Skill invocation (mock + live) -------------------------------------

def _extract_text(message: dict[str, Any]) -> str:
    """Extract plain text from an A2A message (multi-part)."""
    parts = message.get("parts", [])
    if not parts and "text" in message:
        return str(message["text"])
    return "\n".join(p.get("text", "") for p in parts if p.get("kind", "text") == "text")


def _read_skill_md(skill_id: str) -> str:
    """Read a SKILL.md from disk. Returns "" if not found (mock fallback)."""
    p = SKILLS_DIR / skill_id / "SKILL.md"
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def invoke_mock(skill_id: str, text: str) -> str:
    """Mock invocation: returns a skill-aware canned response.

    This is what the server returns when A2A_MODE != live OR no API key is set.
    It reads the SKILL.md frontmatter description so the response is at least
    grounded in what the skill is actually for.
    """
    skill_meta = SKILL_BY_ID.get(skill_id, {})
    name = skill_meta.get("name", skill_id)
    desc = skill_meta.get("description", "")
    return (
        f"[MOCK MODE — no Claude call made]\n\n"
        f"Skill: **{name}** ({skill_id})\n\n"
        f"Request: {text!r}\n\n"
        f"This server is running in mock mode. In live mode (A2A_MODE=live + "
        f"ANTHROPIC_API_KEY set), the request would have been routed to a Claude "
        f"invocation with the skill's SKILL.md as the system prompt.\n\n"
        f"Skill description: {desc[:300]}{'...' if len(desc) > 300 else ''}"
    )


async def invoke_live(skill_id: str, text: str, model: str = DEFAULT_MODEL) -> str:
    """Live invocation: call the Anthropic Messages API with the skill's SKILL.md.

    Requires ANTHROPIC_API_KEY. Uses the `anthropic` Python SDK.
    """
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "Live mode requires the anthropic SDK: pip install anthropic"
        ) from e

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Live mode requires ANTHROPIC_API_KEY env-var")

    system = _read_skill_md(skill_id) or f"You are the {skill_id} skill."
    # Pick max_tokens: per-skill table > env-var > default
    max_tokens = SKILL_MAX_TOKENS.get(skill_id, DEFAULT_MAX_TOKENS)
    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": text}],
    )
    parts = []
    for block in msg.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts) if parts else "[no text response]"


# --- FastAPI app builder ------------------------------------------------

def build_app(
    mode: str = DEFAULT_MODE,
    db_path: Path = DEFAULT_DB_PATH,
    audit_path: Path = DEFAULT_AUDIT_LOG,
    rate_limit: int = DEFAULT_RATE_LIMIT,
    api_keys: Optional[dict[str, str]] = None,
):
    """Build the FastAPI app. Importable for tests via TestClient."""
    from fastapi import FastAPI, HTTPException, Request, Header, Depends
    from fastapi.responses import JSONResponse, StreamingResponse

    if api_keys is None:
        api_keys = _parse_api_keys()

    store = TaskStore(db_path)
    limiter = TokenBucket(rate_limit)
    audit = AuditLog(audit_path)

    app = FastAPI(
        title="llms-txt-advisor A2A server",
        description=f"A2A v1.0 server (mode={mode}). Implements message/send, message/stream, tasks/get, tasks/cancel, tasks/list.",
        version="2.0.0",
    )

    # Expose state for tests / introspection
    app.state.mode = mode
    app.state.store = store
    app.state.limiter = limiter
    app.state.audit = audit
    app.state.api_keys = api_keys

    # --- Auth dependency ---

    async def auth(authorization: Optional[str] = Header(None)) -> Optional[str]:
        """Return caller name if authenticated, None if auth is disabled.

        Raises HTTPException(401) if a bearer is presented but invalid, or if
        auth is enabled and no bearer is provided.
        """
        if not api_keys:
            # Auth disabled (no A2A_API_KEYS set)
            return None
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Missing Bearer token")
        token = authorization.split(" ", 1)[1].strip()
        if token not in api_keys:
            raise HTTPException(status_code=401, detail="Invalid Bearer token")
        return api_keys[token]

    # --- Discovery endpoints ---

    @app.get("/.well-known/agent-card.json")
    async def serve_agent_card():
        return JSONResponse(AGENT_CARD)

    @app.get("/")
    async def root():
        return {
            "agent": AGENT_CARD["name"],
            "version": AGENT_CARD["version"],
            "protocolVersion": AGENT_CARD["protocolVersion"],
            "mode": mode,
            "agentCardUrl": "/.well-known/agent-card.json",
            "a2aEndpoint": "/a2a",
            "skills": sorted(SKILL_IDS),
            "authRequired": bool(api_keys),
        }

    @app.get("/health")
    async def health():
        return {"status": "ok", "mode": mode}

    # --- Main JSON-RPC endpoint ---

    @app.post("/a2a")
    async def handle_a2a(request: Request, caller: Optional[str] = Depends(auth)):
        # Parse body
        try:
            body = await request.json()
        except Exception as e:
            return _rpc_error(None, ERR_PARSE, f"Parse error: {e}")

        if not isinstance(body, dict):
            return _rpc_error(None, ERR_INVALID_REQUEST, "Request must be a JSON object")

        rpc_id = body.get("id")
        method = body.get("method")
        params = body.get("params") or {}

        if body.get("jsonrpc") != "2.0":
            return _rpc_error(rpc_id, ERR_INVALID_REQUEST, "jsonrpc must be '2.0'")
        if not method:
            return _rpc_error(rpc_id, ERR_INVALID_REQUEST, "method is required")

        # Rate limit per caller (or per IP if anon)
        rate_key = caller or request.client.host if request.client else "anon"
        if not limiter.allow(rate_key):
            audit.log({"event": "rate_limited", "caller": rate_key, "method": method})
            return _rpc_error(rpc_id, ERR_RATE_LIMITED, f"Rate limit exceeded ({rate_limit}/min)")

        audit.log({"event": "request", "caller": caller, "method": method, "rpc_id": rpc_id})

        # Dispatch
        try:
            if method == "message/send":
                return await _do_message_send(rpc_id, params, caller)
            if method == "message/stream":
                return await _do_message_stream(rpc_id, params, caller)
            if method == "tasks/get":
                return _do_tasks_get(rpc_id, params, caller)
            if method == "tasks/cancel":
                return _do_tasks_cancel(rpc_id, params, caller)
            if method == "tasks/list":
                return _do_tasks_list(rpc_id, params, caller)
            return _rpc_error(rpc_id, ERR_METHOD_NOT_FOUND, f"Method not found: {method}")
        except Exception as e:
            logger.exception("Internal error on %s", method)
            audit.log({"event": "error", "method": method, "error": str(e)})
            return _rpc_error(rpc_id, ERR_INTERNAL, f"Internal error: {e}")

    # --- Method implementations ---

    async def _do_message_send(rpc_id, params, caller):
        message = params.get("message", {})
        metadata = params.get("metadata", {})
        skill_id = metadata.get("skill")
        if not skill_id:
            return _rpc_error(rpc_id, ERR_INVALID_PARAMS, "metadata.skill is required")
        if skill_id not in SKILL_IDS:
            return _rpc_error(
                rpc_id,
                ERR_INVALID_PARAMS,
                f"Unknown skill: {skill_id}. Available: {sorted(SKILL_IDS)}",
            )

        task_id = store.create(skill_id, message, caller)
        store.update_state(task_id, STATE_WORKING)

        text = _extract_text(message)
        try:
            if mode == "live":
                result_text = await invoke_live(skill_id, text)
            else:
                result_text = invoke_mock(skill_id, text)
        except Exception as e:
            store.update_state(task_id, STATE_FAILED)
            store.append_artifact(
                task_id,
                {"type": "error", "parts": [{"kind": "text", "text": str(e)}]},
            )
            return _rpc_error(rpc_id, ERR_INTERNAL, f"Invocation failed: {e}")

        artifact = {
            "artifactId": str(uuid.uuid4()),
            "name": f"response-{skill_id}",
            "parts": [{"kind": "text", "text": result_text}],
        }
        store.append_artifact(task_id, artifact)
        store.update_state(task_id, STATE_COMPLETED)

        task = store.get(task_id, caller)
        audit.log({"event": "task_completed", "task_id": task_id, "skill": skill_id})
        return _rpc_result(rpc_id, task)

    async def _do_message_stream(rpc_id, params, caller):
        message = params.get("message", {})
        metadata = params.get("metadata", {})
        skill_id = metadata.get("skill")
        if not skill_id:
            return _rpc_error(rpc_id, ERR_INVALID_PARAMS, "metadata.skill is required")
        if skill_id not in SKILL_IDS:
            return _rpc_error(rpc_id, ERR_INVALID_PARAMS, f"Unknown skill: {skill_id}")

        task_id = store.create(skill_id, message, caller)

        async def event_stream() -> AsyncIterator[str]:
            yield _sse({"jsonrpc": "2.0", "id": rpc_id, "result": {"taskId": task_id, "state": STATE_SUBMITTED}})
            store.update_state(task_id, STATE_WORKING)
            yield _sse({"jsonrpc": "2.0", "id": rpc_id, "result": {"taskId": task_id, "state": STATE_WORKING}})

            text = _extract_text(message)
            try:
                if mode == "live":
                    result_text = await invoke_live(skill_id, text)
                else:
                    result_text = invoke_mock(skill_id, text)
            except Exception as e:
                store.update_state(task_id, STATE_FAILED)
                yield _sse(
                    {
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {"code": ERR_INTERNAL, "message": str(e)},
                    }
                )
                return

            # Chunk the output for streaming feel
            chunk_size = 200
            for i in range(0, len(result_text), chunk_size):
                chunk = result_text[i : i + chunk_size]
                yield _sse(
                    {
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": {
                            "taskId": task_id,
                            "state": STATE_WORKING,
                            "delta": {"kind": "text", "text": chunk},
                        },
                    }
                )
                await asyncio.sleep(0.01)

            artifact = {
                "artifactId": str(uuid.uuid4()),
                "name": f"response-{skill_id}",
                "parts": [{"kind": "text", "text": result_text}],
            }
            store.append_artifact(task_id, artifact)
            store.update_state(task_id, STATE_COMPLETED)

            yield _sse(
                {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": {
                        "taskId": task_id,
                        "state": STATE_COMPLETED,
                        "artifact": artifact,
                    },
                }
            )

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    def _do_tasks_get(rpc_id, params, caller):
        task_id = params.get("id")
        if not task_id:
            return _rpc_error(rpc_id, ERR_INVALID_PARAMS, "id is required")
        task = store.get(task_id, caller)
        if task is None:
            return _rpc_error(rpc_id, ERR_TASK_NOT_FOUND, f"Task not found: {task_id}")
        return _rpc_result(rpc_id, task)

    def _do_tasks_cancel(rpc_id, params, caller):
        task_id = params.get("id")
        if not task_id:
            return _rpc_error(rpc_id, ERR_INVALID_PARAMS, "id is required")
        task = store.get(task_id, caller)
        if task is None:
            return _rpc_error(rpc_id, ERR_TASK_NOT_FOUND, f"Task not found: {task_id}")
        state = task["status"]["state"]
        if state in TERMINAL_STATES:
            return _rpc_error(rpc_id, ERR_TERMINAL_STATE, f"Task in terminal state: {state}")
        store.update_state(task_id, STATE_CANCELED)
        audit.log({"event": "task_canceled", "task_id": task_id})
        return _rpc_result(rpc_id, store.get(task_id, caller))

    def _do_tasks_list(rpc_id, params, caller):
        limit = int(params.get("limit", 50))
        tasks = store.list_for_caller(caller, limit=limit)
        return _rpc_result(rpc_id, {"tasks": tasks, "count": len(tasks)})

    # --- Response helpers ---

    def _rpc_result(rpc_id, result):
        return JSONResponse({"jsonrpc": "2.0", "id": rpc_id, "result": result})

    def _rpc_error(rpc_id, code, message, data=None):
        err = {"code": code, "message": message}
        if data is not None:
            err["data"] = data
        return JSONResponse(
            {"jsonrpc": "2.0", "id": rpc_id, "error": err},
            status_code=200,  # JSON-RPC errors are 200 OK at HTTP layer
        )

    def _sse(payload: dict[str, Any]) -> str:
        return f"data: {json.dumps(payload)}\n\n"

    return app


# --- CLI -----------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the A2A Tier 2 server.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    parser.add_argument(
        "--mode",
        choices=["mock", "live"],
        default=DEFAULT_MODE,
        help="mock (no API call) or live (real Claude). Default from A2A_MODE env.",
    )
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite DB path")
    parser.add_argument("--audit", default=str(DEFAULT_AUDIT_LOG), help="Audit log path")
    parser.add_argument(
        "--rate-limit", type=int, default=DEFAULT_RATE_LIMIT,
        help=f"Requests per minute per caller (default: {DEFAULT_RATE_LIMIT})",
    )
    parser.add_argument(
        "--print-config", action="store_true",
        help="Print the resolved config and exit (no server start).",
    )
    args = parser.parse_args(argv)

    api_keys = _parse_api_keys()
    auth_status = f"{len(api_keys)} keys configured" if api_keys else "DISABLED (anyone can call)"
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))

    config_summary = {
        "mode": args.mode,
        "host": args.host,
        "port": args.port,
        "db_path": args.db,
        "audit_log": args.audit,
        "rate_limit_per_min": args.rate_limit,
        "auth": auth_status,
        "anthropic_api_key_set": has_anthropic,
        "skills_declared": sorted(SKILL_IDS),
        "agent_card": str(AGENT_CARD_PATH),
    }

    print("=" * 68)
    print(f"  llms-txt-advisor A2A server v1.1.0")
    print("=" * 68)
    for k, v in config_summary.items():
        print(f"  {k:24s} {v}")
    print("=" * 68)

    if args.mode == "live" and not has_anthropic:
        print("ERROR: --mode live requires ANTHROPIC_API_KEY to be set", file=sys.stderr)
        return 2

    if not api_keys:
        print("WARNING: A2A_API_KEYS unset — server accepts unauthenticated requests.")
        print("         Set A2A_API_KEYS='caller1=secret1,caller2=secret2' for production.")
    if args.mode == "mock":
        print("INFO: Running in MOCK mode. Set A2A_MODE=live + ANTHROPIC_API_KEY for real calls.")

    if args.print_config:
        return 0

    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn not installed. pip install uvicorn", file=sys.stderr)
        return 1

    app = build_app(
        mode=args.mode,
        db_path=Path(args.db).resolve(),
        audit_path=Path(args.audit).resolve(),
        rate_limit=args.rate_limit,
        api_keys=api_keys,
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
