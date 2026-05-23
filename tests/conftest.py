"""Shared pytest fixtures for the A2A test suite."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from typing import Iterator

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT))


def _load_module(name: str, path: Path):
    """Import a Python file that has a hyphen in its name (so the normal
    import system won't find it). Returns the module object.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, f"Cannot load {path}"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# These are hyphen-named CLI scripts — load them as modules for testing.
@pytest.fixture(scope="session")
def a2a_server_module():
    return _load_module("a2a_server", SCRIPTS / "a2a-server.py")


@pytest.fixture(scope="session")
def a2a_client_module():
    return _load_module("a2a_client", SCRIPTS / "a2a-client.py")


@pytest.fixture
def tmp_db(tmp_path: Path) -> Path:
    return tmp_path / "tasks.db"


@pytest.fixture
def tmp_audit(tmp_path: Path) -> Path:
    return tmp_path / "audit.log"


@pytest.fixture
def app_factory(a2a_server_module, tmp_db, tmp_audit):
    """Returns a callable to build a FastAPI app for testing.

    Usage:
        app = app_factory(mode="mock", api_keys=None)
        client = TestClient(app)
    """

    def _make(mode="mock", api_keys=None, rate_limit=1000):
        # Default to high rate limit so tests don't trip the limiter.
        return a2a_server_module.build_app(
            mode=mode,
            db_path=tmp_db,
            audit_path=tmp_audit,
            rate_limit=rate_limit,
            api_keys=api_keys or {},
        )

    return _make


@pytest.fixture
def app(app_factory):
    """Default mock-mode app, no auth, high rate limit."""
    return app_factory()


@pytest.fixture
def client(app):
    """FastAPI TestClient bound to the default app."""
    from fastapi.testclient import TestClient

    return TestClient(app)


def rpc(method: str, params: dict | None = None, rpc_id: str = "1") -> dict:
    """Build a JSON-RPC 2.0 request envelope."""
    return {"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params or {}}
