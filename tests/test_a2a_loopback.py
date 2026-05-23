"""End-to-end loopback tests: Tier 3 client → Tier 2 server, in-process.

Uses httpx.ASGITransport to mount the FastAPI app as a transport target so the
real A2AClient code path exercises the real server code path without any
network or open sockets.
"""

from __future__ import annotations

import httpx
import pytest


@pytest.mark.asyncio
class TestLoopback:
    async def test_full_round_trip_send(self, app_factory, a2a_client_module):
        app = app_factory()
        transport = httpx.ASGITransport(app=app)

        async with a2a_client_module.A2AClient("http://server") as client:
            client._client = httpx.AsyncClient(
                transport=transport, base_url="http://server"
            )
            card = await client.discover()
            assert card["name"] == "llms-txt-advisor"
            assert len(card["skills"]) == 8

            task = await client.send("advise", "should I ship llms.txt?")
            assert task["status"]["state"] == "completed"
            text = task["artifacts"][0]["parts"][0]["text"]
            assert "MOCK MODE" in text
            assert "advise" in text.lower()

            # tasks/get works for the same task
            fetched = await client.get_task(task["id"])
            assert fetched["id"] == task["id"]

            # tasks/list includes our task
            listed = await client.list_tasks()
            ids = {t["id"] for t in listed["tasks"]}
            assert task["id"] in ids

            await client._client.aclose()

    async def test_loopback_with_auth(self, app_factory, a2a_client_module):
        app = app_factory(api_keys={"loopback-token": "loopback-caller"})
        transport = httpx.ASGITransport(app=app)

        # Without token: 401
        async with a2a_client_module.A2AClient("http://server") as client:
            client._client = httpx.AsyncClient(
                transport=transport, base_url="http://server"
            )
            with pytest.raises(a2a_client_module.A2AHttpError) as ei:
                await client.list_tasks()
            assert ei.value.status == 401
            await client._client.aclose()

        # With correct token: works
        async with a2a_client_module.A2AClient(
            "http://server", bearer_token="loopback-token"
        ) as client:
            client._client = httpx.AsyncClient(
                transport=transport, base_url="http://server"
            )
            result = await client.list_tasks()
            assert "tasks" in result
            await client._client.aclose()

    async def test_loopback_stream(self, app_factory, a2a_client_module):
        app = app_factory()
        transport = httpx.ASGITransport(app=app)

        async with a2a_client_module.A2AClient("http://server") as client:
            client._client = httpx.AsyncClient(
                transport=transport, base_url="http://server"
            )
            states_seen = []
            delta_texts = []
            async for event in client.stream("audit", "review my file"):
                if "result" not in event:
                    continue
                result = event["result"]
                if "state" in result:
                    states_seen.append(result["state"])
                if "delta" in result and result["delta"].get("kind") == "text":
                    delta_texts.append(result["delta"]["text"])

            assert "submitted" in states_seen
            assert "completed" in states_seen
            assert delta_texts  # at least one delta event
            joined = "".join(delta_texts)
            assert "MOCK MODE" in joined
            await client._client.aclose()

    async def test_loopback_invalid_skill_propagates(
        self, app_factory, a2a_client_module
    ):
        app = app_factory()
        transport = httpx.ASGITransport(app=app)

        async with a2a_client_module.A2AClient("http://server") as client:
            client._client = httpx.AsyncClient(
                transport=transport, base_url="http://server"
            )
            with pytest.raises(a2a_client_module.A2ARpcError) as ei:
                await client.send("no-such-skill", "x")
            assert ei.value.code == -32602
            await client._client.aclose()
