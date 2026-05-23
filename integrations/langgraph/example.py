"""
LangGraph integration: use the llms-txt-advisor as a tool in a LangGraph agent.

The pattern: wrap the A2A `send` call as a LangChain tool, then bind it to any
LangGraph node that needs llms.txt advisory.

Requires:
    pip install langgraph langchain-core httpx

Usage:
    export A2A_URL=https://a2a.example.com
    export A2A_BEARER=your-token   # if your server requires auth
    python3 example.py
"""

import asyncio
import os
import uuid
from typing import Annotated

import httpx
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


A2A_URL = os.environ.get("A2A_URL", "http://localhost:8000")
A2A_BEARER = os.environ.get("A2A_BEARER")


# ---------------------------------------------------------------
# A2A tool — one tool per skill, or a single dynamic one
# ---------------------------------------------------------------


async def _a2a_send(skill: str, text: str) -> str:
    """Submit to the A2A server and return the artifact text."""
    headers = {"Content-Type": "application/json"}
    if A2A_BEARER:
        headers["Authorization"] = f"Bearer {A2A_BEARER}"
    body = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {"role": "user", "parts": [{"kind": "text", "text": text}]},
            "metadata": {"skill": skill},
        },
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{A2A_URL}/a2a", json=body, headers=headers)
        r.raise_for_status()
        env = r.json()
        if "error" in env:
            return f"[A2A error] {env['error']['message']}"
        artifacts = env["result"].get("artifacts", [])
        if not artifacts:
            return "(no response)"
        return artifacts[0]["parts"][0]["text"]


@tool
async def llms_txt_advise(question: str) -> str:
    """Ask the llms-txt advisory agent about whether to ship llms.txt,
    decision frameworks, empirical evidence, or general guidance."""
    return await _a2a_send("advise", question)


@tool
async def llms_txt_audit(file_url_or_content: str) -> str:
    """Audit an existing llms.txt file against the 15 documented anti-patterns.
    Pass either the URL of the file or its raw content."""
    return await _a2a_send("audit", file_url_or_content)


@tool
async def llms_txt_generate(site_profile_description: str) -> str:
    """Generate an llms.txt file body for a site. Pass a description of the
    site (sector, hosting, IA)."""
    return await _a2a_send("generate", site_profile_description)


# ---------------------------------------------------------------
# Example LangGraph node that uses one of these tools
# ---------------------------------------------------------------


class State(TypedDict):
    messages: Annotated[list, add_messages]


async def advisor_node(state: State) -> State:
    """Single node that calls the advise tool with the last user message."""
    last_msg = state["messages"][-1].content
    response = await llms_txt_advise.ainvoke({"question": last_msg})
    return {"messages": [("assistant", response)]}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("advisor", advisor_node)
    graph.set_entry_point("advisor")
    graph.add_edge("advisor", END)
    return graph.compile()


async def main():
    g = build_graph()
    out = await g.ainvoke(
        {"messages": [("user", "Our CEO wants us to add llms.txt. Should we?")]}
    )
    print(out["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
