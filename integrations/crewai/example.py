"""
CrewAI integration: use the llms-txt-advisor as a Tool that any Agent can call.

Requires:
    pip install crewai httpx

Usage:
    export OPENAI_API_KEY=...                 # CrewAI's default LLM
    export A2A_URL=https://a2a.example.com
    export A2A_BEARER=your-token
    python3 example.py
"""

import asyncio
import os
import uuid

import httpx

try:
    from crewai import Agent, Task, Crew
    from crewai.tools import BaseTool
except ImportError:
    print("This example requires crewai. Install with: pip install crewai")
    raise


A2A_URL = os.environ.get("A2A_URL", "http://localhost:8000")
A2A_BEARER = os.environ.get("A2A_BEARER")


def _a2a_send_sync(skill: str, text: str) -> str:
    """Synchronous wrapper because CrewAI tools are sync-first."""
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
    r = httpx.post(f"{A2A_URL}/a2a", json=body, headers=headers, timeout=60)
    r.raise_for_status()
    env = r.json()
    if "error" in env:
        return f"[A2A error] {env['error']['message']}"
    return env["result"]["artifacts"][0]["parts"][0]["text"]


class LLMSTxtAdviseTool(BaseTool):
    name: str = "llms_txt_advise"
    description: str = (
        "Ask the llms-txt advisory agent about whether a site should ship llms.txt, "
        "decision frameworks, empirical evidence, or general SEO guidance about it."
    )

    def _run(self, question: str) -> str:
        return _a2a_send_sync("advise", question)


class LLMSTxtAuditTool(BaseTool):
    name: str = "llms_txt_audit"
    description: str = (
        "Audit an existing llms.txt file (URL or content) against 15 documented "
        "anti-patterns. Returns severity-tagged findings."
    )

    def _run(self, file_url_or_content: str) -> str:
        return _a2a_send_sync("audit", file_url_or_content)


def main():
    seo_strategist = Agent(
        role="SEO Strategist",
        goal="Decide whether the site should ship llms.txt and produce a recommendation",
        backstory=(
            "You're a pragmatic SEO lead who only recommends interventions with "
            "evidence-backed ROI. You consult the llms-txt advisor before making calls."
        ),
        tools=[LLMSTxtAdviseTool(), LLMSTxtAuditTool()],
        verbose=True,
    )

    task = Task(
        description=(
            "Our marketing team wants to add llms.txt to https://example-marketplace.com "
            "to 'rank better in ChatGPT'. Decide what to recommend. Use the llms-txt advisor "
            "to ground your answer in evidence."
        ),
        expected_output="A 3-paragraph recommendation with concrete next steps.",
        agent=seo_strategist,
    )

    crew = Crew(agents=[seo_strategist], tasks=[task], verbose=True)
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL RECOMMENDATION")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
