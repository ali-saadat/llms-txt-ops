"""Tier 2 A2A server tests — covers all JSON-RPC methods, auth, rate limits,
SSE streaming, error codes, and SQLite persistence.

Runs entirely in mock mode (no Anthropic API key required).
"""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from conftest import rpc


# ============================================================
# Discovery endpoints
# ============================================================


class TestDiscovery:
    def test_root_returns_summary(self, client: TestClient):
        r = client.get("/")
        assert r.status_code == 200
        body = r.json()
        assert body["agent"] == "llms-txt-advisor"
        assert body["mode"] == "mock"
        assert body["a2aEndpoint"] == "/a2a"
        assert "advise" in body["skills"]
        assert len(body["skills"]) == 8
        assert body["authRequired"] is False

    def test_health(self, client: TestClient):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_agent_card_served(self, client: TestClient):
        r = client.get("/.well-known/agent-card.json")
        assert r.status_code == 200
        card = r.json()
        assert card["protocolVersion"].startswith("1.")
        assert len(card["skills"]) == 8


# ============================================================
# message/send happy path
# ============================================================


class TestMessageSend:
    def test_send_succeeds_in_mock_mode(self, client: TestClient):
        r = client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"role": "user", "parts": [{"kind": "text", "text": "hello"}]},
                    "metadata": {"skill": "advise"},
                },
            ),
        )
        assert r.status_code == 200
        env = r.json()
        assert env["jsonrpc"] == "2.0"
        assert env["id"] == "1"
        assert "error" not in env
        task = env["result"]
        assert task["status"]["state"] == "completed"
        assert len(task["artifacts"]) == 1
        text = task["artifacts"][0]["parts"][0]["text"]
        assert "MOCK MODE" in text
        assert "advise" in text.lower()

    def test_send_each_skill_works(self, client: TestClient):
        skills = [
            "advise",
            "audit",
            "cold-start-interview",
            "customize",
            "deploy",
            "generate",
            "setup-recommender",
            "stakeholder-comms",
        ]
        for skill in skills:
            r = client.post(
                "/a2a",
                json=rpc(
                    "message/send",
                    {
                        "message": {"role": "user", "parts": [{"kind": "text", "text": "hi"}]},
                        "metadata": {"skill": skill},
                    },
                ),
            )
            assert r.status_code == 200
            env = r.json()
            assert env["result"]["status"]["state"] == "completed", f"failed for {skill}"


# ============================================================
# message/send error paths
# ============================================================


class TestMessageSendErrors:
    def test_unknown_skill(self, client: TestClient):
        r = client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"parts": [{"kind": "text", "text": "x"}]},
                    "metadata": {"skill": "no-such-skill"},
                },
            ),
        )
        env = r.json()
        assert env["error"]["code"] == -32602
        assert "Unknown skill" in env["error"]["message"]

    def test_missing_skill_metadata(self, client: TestClient):
        r = client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {"message": {"parts": [{"kind": "text", "text": "x"}]}},
            ),
        )
        env = r.json()
        assert env["error"]["code"] == -32602
        assert "metadata.skill" in env["error"]["message"]

    def test_missing_jsonrpc_version(self, client: TestClient):
        r = client.post(
            "/a2a",
            json={"id": "1", "method": "message/send", "params": {}},
        )
        env = r.json()
        assert env["error"]["code"] == -32600

    def test_missing_method(self, client: TestClient):
        r = client.post("/a2a", json={"jsonrpc": "2.0", "id": "1"})
        env = r.json()
        assert env["error"]["code"] == -32600

    def test_unknown_method(self, client: TestClient):
        r = client.post("/a2a", json=rpc("not/a/real/method"))
        env = r.json()
        assert env["error"]["code"] == -32601

    def test_invalid_json_body(self, client: TestClient):
        r = client.post(
            "/a2a",
            content=b"this is not json",
            headers={"Content-Type": "application/json"},
        )
        env = r.json()
        assert env["error"]["code"] == -32700

    def test_non_object_body(self, client: TestClient):
        r = client.post("/a2a", json=["array", "not", "object"])
        env = r.json()
        assert env["error"]["code"] == -32600


# ============================================================
# tasks/get + tasks/cancel + tasks/list
# ============================================================


class TestTaskLifecycle:
    def _send(self, client, skill="advise", text="hello"):
        r = client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"role": "user", "parts": [{"kind": "text", "text": text}]},
                    "metadata": {"skill": skill},
                },
            ),
        )
        return r.json()["result"]

    def test_tasks_get_after_send(self, client):
        task = self._send(client)
        r = client.post("/a2a", json=rpc("tasks/get", {"id": task["id"]}, rpc_id="2"))
        env = r.json()
        assert env["id"] == "2"
        assert env["result"]["id"] == task["id"]
        assert env["result"]["status"]["state"] == "completed"

    def test_tasks_get_not_found(self, client):
        r = client.post("/a2a", json=rpc("tasks/get", {"id": "no-such-task"}))
        env = r.json()
        assert env["error"]["code"] == -32003

    def test_tasks_get_requires_id(self, client):
        r = client.post("/a2a", json=rpc("tasks/get", {}))
        assert r.json()["error"]["code"] == -32602

    def test_tasks_cancel_terminal_state_rejected(self, client):
        # mock-mode tasks complete immediately, so cancel should reject
        task = self._send(client)
        r = client.post("/a2a", json=rpc("tasks/cancel", {"id": task["id"]}))
        env = r.json()
        assert env["error"]["code"] == -32004
        assert "terminal state" in env["error"]["message"]

    def test_tasks_cancel_not_found(self, client):
        r = client.post("/a2a", json=rpc("tasks/cancel", {"id": "no-such-task"}))
        env = r.json()
        assert env["error"]["code"] == -32003

    def test_tasks_list_returns_recent(self, client):
        # Submit 3 tasks
        ids = [self._send(client, text=f"t{i}")["id"] for i in range(3)]
        r = client.post("/a2a", json=rpc("tasks/list", {"limit": 50}))
        env = r.json()
        listed_ids = {t["id"] for t in env["result"]["tasks"]}
        assert set(ids) <= listed_ids
        assert env["result"]["count"] >= 3


# ============================================================
# Auth
# ============================================================


class TestAuth:
    def test_no_auth_required_when_keys_empty(self, app_factory):
        app = app_factory(api_keys={})
        client = TestClient(app)
        r = client.post("/a2a", json=rpc("tasks/list", {}))
        assert r.json()["result"]["count"] >= 0

    def test_auth_required_when_keys_set(self, app_factory):
        app = app_factory(api_keys={"secret-token": "caller-1"})
        client = TestClient(app)
        r = client.post("/a2a", json=rpc("tasks/list", {}))
        assert r.status_code == 401

    def test_auth_accepts_valid_bearer(self, app_factory):
        app = app_factory(api_keys={"secret-token": "caller-1"})
        client = TestClient(app)
        r = client.post(
            "/a2a",
            json=rpc("tasks/list", {}),
            headers={"Authorization": "Bearer secret-token"},
        )
        assert r.status_code == 200
        assert "result" in r.json()

    def test_auth_rejects_invalid_bearer(self, app_factory):
        app = app_factory(api_keys={"secret-token": "caller-1"})
        client = TestClient(app)
        r = client.post(
            "/a2a",
            json=rpc("tasks/list", {}),
            headers={"Authorization": "Bearer wrong-token"},
        )
        assert r.status_code == 401

    def test_caller_isolation_in_task_get(self, app_factory):
        app = app_factory(
            api_keys={"key-a": "caller-a", "key-b": "caller-b"}
        )
        client = TestClient(app)

        # caller-a creates a task
        r = client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"parts": [{"kind": "text", "text": "x"}]},
                    "metadata": {"skill": "advise"},
                },
            ),
            headers={"Authorization": "Bearer key-a"},
        )
        task_id = r.json()["result"]["id"]

        # caller-b tries to fetch — should see task-not-found
        r2 = client.post(
            "/a2a",
            json=rpc("tasks/get", {"id": task_id}),
            headers={"Authorization": "Bearer key-b"},
        )
        assert r2.json()["error"]["code"] == -32003

        # caller-a can still fetch
        r3 = client.post(
            "/a2a",
            json=rpc("tasks/get", {"id": task_id}),
            headers={"Authorization": "Bearer key-a"},
        )
        assert r3.json()["result"]["id"] == task_id


# ============================================================
# Rate limiting
# ============================================================


class TestRateLimit:
    def test_rate_limit_trips_after_quota(self, app_factory):
        app = app_factory(rate_limit=3)
        client = TestClient(app)
        # 3 should succeed, 4th should fail
        for i in range(3):
            r = client.post("/a2a", json=rpc("tasks/list", {}, rpc_id=str(i)))
            assert "error" not in r.json(), f"call {i} unexpectedly errored"
        r = client.post("/a2a", json=rpc("tasks/list", {}, rpc_id="4"))
        env = r.json()
        assert env["error"]["code"] == -32002


# ============================================================
# Persistence (SQLite survives a rebuild)
# ============================================================


class TestPersistence:
    def test_tasks_persist_across_app_rebuild(self, app_factory):
        app1 = app_factory()
        client1 = TestClient(app1)
        r = client1.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"parts": [{"kind": "text", "text": "persist me"}]},
                    "metadata": {"skill": "advise"},
                },
            ),
        )
        task_id = r.json()["result"]["id"]

        # New app instance with same DB — should still find the task
        app2 = app_factory()
        client2 = TestClient(app2)
        r2 = client2.post("/a2a", json=rpc("tasks/get", {"id": task_id}))
        assert r2.json()["result"]["id"] == task_id
        assert r2.json()["result"]["status"]["state"] == "completed"


# ============================================================
# Streaming
# ============================================================


class TestStreaming:
    def test_stream_emits_states_and_delta(self, client):
        with client.stream(
            "POST",
            "/a2a",
            json=rpc(
                "message/stream",
                {
                    "message": {"parts": [{"kind": "text", "text": "stream test"}]},
                    "metadata": {"skill": "advise"},
                },
            ),
        ) as r:
            assert r.status_code == 200
            events = []
            buf = ""
            for chunk in r.iter_text():
                buf += chunk
                while "\n\n" in buf:
                    block, buf = buf.split("\n\n", 1)
                    for line in block.split("\n"):
                        if line.startswith("data: "):
                            events.append(json.loads(line[6:]))

        # We expect at least: submitted state, working state, one or more
        # delta events, and a final completed state.
        states = [e["result"]["state"] for e in events if "result" in e and "state" in e["result"]]
        assert "submitted" in states
        assert "working" in states
        assert "completed" in states

        # At least one delta with text content
        deltas = [
            e["result"]["delta"]["text"]
            for e in events
            if "result" in e and "delta" in e["result"]
        ]
        assert any(deltas)


# ============================================================
# Audit logging
# ============================================================


class TestAuditLog:
    def test_audit_log_writes_request_events(self, app_factory, tmp_audit):
        app = app_factory()
        client = TestClient(app)
        client.post(
            "/a2a",
            json=rpc(
                "message/send",
                {
                    "message": {"parts": [{"kind": "text", "text": "x"}]},
                    "metadata": {"skill": "advise"},
                },
            ),
        )
        lines = tmp_audit.read_text().strip().split("\n")
        events = [json.loads(line) for line in lines if line.strip()]
        kinds = [e["event"] for e in events]
        assert "request" in kinds
        assert "task_completed" in kinds
