"""
Minimal example of calling the llms-txt-advisor A2A server from Python.

Two patterns shown:
  1. Using the provided client wrapper (scripts/a2a-client.py) — recommended
  2. Using raw httpx — useful when you don't want to ship the wrapper

Usage:
    pip install httpx
    python3 example.py
"""

import asyncio
import importlib.util
import json
import os
import sys
import uuid
from pathlib import Path

import httpx

A2A_URL = os.environ.get("A2A_URL", "http://localhost:8000")
A2A_BEARER = os.environ.get("A2A_BEARER")


# ---------------------------------------------------------------
# Pattern 1: use the provided wrapper from scripts/a2a-client.py
# ---------------------------------------------------------------

def _load_client():
    """Load the hyphen-named script as a module."""
    here = Path(__file__).resolve().parent
    candidate = here.parent.parent / "scripts" / "a2a-client.py"
    spec = importlib.util.spec_from_file_location("a2a_client", candidate)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def with_wrapper():
    a2a_client = _load_client()
    async with a2a_client.A2AClient(A2A_URL, bearer_token=A2A_BEARER) as client:
        card = await client.discover()
        print(f"Connected to {card['name']} v{card['version']}")
        print(f"Available skills: {[s['id'] for s in card['skills']]}")
        print()

        task = await client.send(
            skill="advise",
            text="Our marketing team wants me to add llms.txt — should we?",
        )
        print("=" * 60)
        for part in task["artifacts"][0]["parts"]:
            print(part.get("text", ""))
        print("=" * 60)


# ---------------------------------------------------------------
# Pattern 2: raw httpx — no wrapper needed
# ---------------------------------------------------------------


async def with_raw_httpx():
    headers = {"Content-Type": "application/json"}
    if A2A_BEARER:
        headers["Authorization"] = f"Bearer {A2A_BEARER}"

    body = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "What does llms.txt actually do?"}],
            },
            "metadata": {"skill": "advise"},
        },
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{A2A_URL}/a2a", json=body, headers=headers, timeout=60)
        r.raise_for_status()
        envelope = r.json()
        if "error" in envelope:
            print(f"RPC error: {envelope['error']}")
            return
        task = envelope["result"]
        print(f"Task {task['id']} — {task['status']['state']}")
        print(task["artifacts"][0]["parts"][0]["text"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "raw":
        asyncio.run(with_raw_httpx())
    else:
        asyncio.run(with_wrapper())
