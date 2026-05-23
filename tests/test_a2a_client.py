"""Tier 3 A2A client tests — pure unit tests (no network) using
httpx.MockTransport, plus loopback tests that exercise the real client
against the in-process Tier 2 server via httpx.ASGITransport.
"""

from __future__ import annotations

import json

import httpx
import pytest


# ============================================================
# Validation
# ============================================================


class TestValidation:
    def test_valid_card_passes(self, a2a_client_module):
        a2a_client_module.validate_agent_card(
            {
                "name": "x",
                "protocolVersion": "1.0",
                "skills": [{"id": "test"}],
            }
        )

    def test_missing_fields_rejected(self, a2a_client_module):
        with pytest.raises(a2a_client_module.A2AValidationError):
            a2a_client_module.validate_agent_card({"name": "x"})

    def test_skills_must_be_list(self, a2a_client_module):
        with pytest.raises(a2a_client_module.A2AValidationError):
            a2a_client_module.validate_agent_card(
                {"name": "x", "protocolVersion": "1.0", "skills": "not-a-list"}
            )

    def test_skill_must_have_id(self, a2a_client_module):
        with pytest.raises(a2a_client_module.A2AValidationError):
            a2a_client_module.validate_agent_card(
                {"name": "x", "protocolVersion": "1.0", "skills": [{"no-id": True}]}
            )

    def test_v2_protocol_rejected(self, a2a_client_module):
        with pytest.raises(a2a_client_module.A2AValidationError):
            a2a_client_module.validate_agent_card(
                {"name": "x", "protocolVersion": "2.0", "skills": []}
            )


# ============================================================
# Client with MockTransport — pure unit tests
# ============================================================


@pytest.mark.asyncio
class TestClientWithMock:
    async def test_discover_validates(self, a2a_client_module):
        card = {
            "name": "test-agent",
            "protocolVersion": "1.0",
            "skills": [{"id": "advise"}, {"id": "audit"}],
        }

        def handler(req: httpx.Request) -> httpx.Response:
            assert req.url.path == "/.well-known/agent-card.json"
            return httpx.Response(200, json=card)

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test") as client:
            client._client = httpx.AsyncClient(transport=transport)
            fetched = await client.discover()
            assert fetched["name"] == "test-agent"
            await client._client.aclose()

    async def test_discover_rejects_invalid_card(self, a2a_client_module):
        def handler(req):
            return httpx.Response(200, json={"name": "broken"})

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test") as client:
            client._client = httpx.AsyncClient(transport=transport)
            with pytest.raises(a2a_client_module.A2AValidationError):
                await client.discover()
            await client._client.aclose()

    async def test_send_returns_task(self, a2a_client_module):
        def handler(req: httpx.Request) -> httpx.Response:
            body = json.loads(req.content)
            assert body["method"] == "message/send"
            return httpx.Response(
                200,
                json={
                    "jsonrpc": "2.0",
                    "id": body["id"],
                    "result": {
                        "id": "task-123",
                        "status": {"state": "completed"},
                        "artifacts": [
                            {"parts": [{"kind": "text", "text": "hello"}]}
                        ],
                    },
                },
            )

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test") as client:
            client._client = httpx.AsyncClient(transport=transport)
            task = await client.send("advise", "hi")
            assert task["id"] == "task-123"
            assert task["artifacts"][0]["parts"][0]["text"] == "hello"
            await client._client.aclose()

    async def test_send_propagates_rpc_error(self, a2a_client_module):
        def handler(req):
            body = json.loads(req.content)
            return httpx.Response(
                200,
                json={
                    "jsonrpc": "2.0",
                    "id": body["id"],
                    "error": {"code": -32601, "message": "Method not found"},
                },
            )

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test") as client:
            client._client = httpx.AsyncClient(transport=transport)
            with pytest.raises(a2a_client_module.A2ARpcError) as ei:
                await client.send("advise", "hi")
            assert ei.value.code == -32601
            await client._client.aclose()

    async def test_http_error_raised(self, a2a_client_module):
        def handler(req):
            return httpx.Response(500, text="boom")

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test", retries=0) as client:
            client._client = httpx.AsyncClient(transport=transport)
            with pytest.raises(a2a_client_module.A2AHttpError) as ei:
                await client.send("advise", "hi")
            assert ei.value.status == 500
            await client._client.aclose()

    async def test_bearer_token_sent(self, a2a_client_module):
        seen = {}

        def handler(req):
            seen["auth"] = req.headers.get("authorization")
            body = json.loads(req.content)
            return httpx.Response(
                200,
                json={"jsonrpc": "2.0", "id": body["id"], "result": {"tasks": [], "count": 0}},
            )

        transport = httpx.MockTransport(handler)
        async with a2a_client_module.A2AClient("http://test", bearer_token="my-token") as client:
            client._client = httpx.AsyncClient(transport=transport)
            await client.list_tasks()
            assert seen["auth"] == "Bearer my-token"
            await client._client.aclose()
