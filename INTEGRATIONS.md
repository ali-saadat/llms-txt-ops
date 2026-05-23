# Integrations — How to call this from anywhere

The llms-txt-advisor exposes the same set of skills through **two interfaces**:

1. **Claude Code plugin** — `/llms-txt-advisor:<skill>` — best for interactive use inside Claude Code
2. **A2A v1.0 HTTP API** — `POST /a2a` over JSON-RPC — works from any language, framework, or no-code tool

This document covers the second one — how to call this agent from outside Claude Code.

---

## Choose your starting point

| You are... | Go to |
|---|---|
| **Trying it locally for 60 seconds** | [Quickstart — local Docker](#quickstart--local-docker) |
| **Deploying it permanently to the internet** | [Hosted deployments](#hosted-deployments) |
| **Building a no-code workflow (n8n, Zapier, Make)** | [n8n](#n8n--no-code-workflows) — also works for any other HTTP-capable no-code tool |
| **Building an agent with LangGraph** | [LangGraph](#langgraph) |
| **Building an agent with CrewAI** | [CrewAI](#crewai) |
| **Calling from Python directly** | [Python](#python) |
| **Calling from Node.js / TypeScript / Go / curl / anything HTTP** | [Raw HTTP](#raw-http) |
| **Embedding in another A2A v1.0 agent** | [A2A-to-A2A](#a2a-to-a2a-cross-agent-calls) |

---

## Quickstart — local Docker

One command from a clean machine:

```bash
git clone <repo-url>
cd llms-txt-ops
docker compose up
```

The server is now at `http://localhost:8000`. Try it:

```bash
curl http://localhost:8000/.well-known/agent-card.json
bash integrations/raw-http/curl-examples.sh
```

Default mode is **mock** — canned responses, no API key needed. Good for testing the integration.

For real Claude calls, edit `.env` (copy from `.env.example`):

```bash
cp .env.example .env
# Edit: A2A_MODE=live, ANTHROPIC_API_KEY=sk-ant-..., A2A_API_KEYS="caller1=$(openssl rand -hex 32)"
docker compose up
```

---

## Hosted deployments

All one-click. Pick the platform you prefer:

| Platform | Setup | Cost (May 2026) | Best for |
|---|---|---|---|
| **Render** | Push repo → Render auto-detects [`deploy/render.yaml`](deploy/render.yaml) | Free tier (sleeps) or $7/mo | Easiest dashboard |
| **Fly.io** | `fly launch --copy-config && fly deploy` using [`deploy/fly.toml`](deploy/fly.toml) | ~$2/mo always-on | Cheapest always-on |
| **Railway** | Connect repo → uses [`deploy/railway.json`](deploy/railway.json) | $5/mo trial → usage-based | Fastest cold start |
| **Self-hosted Docker** | `docker compose --profile production up -d` + [`deploy/Caddyfile`](deploy/Caddyfile) | Hardware only | Full control |
| **AWS App Runner / GCP Cloud Run** | Point at the `Dockerfile` | Per-request | Existing cloud accounts |

Full deploy guide: [`deploy/README.md`](deploy/README.md).

**Cost note**: in live mode, the per-request Anthropic API cost dwarfs the hosting cost. A small Fly.io VM running this server costs less per month than ~100 typical advisory calls to Claude.

### After deploy: lock it down

In any production deploy, **always** set `A2A_API_KEYS`. Otherwise the endpoint is open and any internet user can burn your Claude API quota.

```bash
# Generate a per-caller key
openssl rand -hex 32
# → e.g., 8f7a2b1e9d3c4f5e6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f

# Set on the platform
fly secrets set A2A_API_KEYS="zapier-prod=8f7a2b1e9d3c..."
```

Then every caller must send `Authorization: Bearer 8f7a2b1e9d3c...` — see each integration's docs below.

---

## n8n — no-code workflows

Best for: cron-based audits, webhook responders, Slack/email automation, CMS-triggered regeneration.

**Quick path**: import [`integrations/n8n/workflow-llms-txt-audit.json`](integrations/n8n/workflow-llms-txt-audit.json) into n8n, change the `baseUrl` in the **Config** node, hit **Execute Workflow**.

Full guide: [`integrations/n8n/README.md`](integrations/n8n/README.md) — covers webhooks, scheduled runs, Slack integration, auth, error handling.

The same pattern works for **Zapier**, **Make.com**, **Pipedream**, **Workato**, **IFTTT** — anywhere with an HTTP Request node. Wire up:

- URL: `https://your-a2a-host/a2a`
- Method: POST
- Headers: `Content-Type: application/json`, `Authorization: Bearer <token>`
- Body: the JSON-RPC envelope shown in [`integrations/raw-http/curl-examples.sh`](integrations/raw-http/curl-examples.sh)

---

## LangGraph

[`integrations/langgraph/example.py`](integrations/langgraph/example.py) — wraps the A2A call as LangChain tools (`llms_txt_advise`, `llms_txt_audit`, `llms_txt_generate`) that any LangGraph node can bind.

```bash
pip install langgraph langchain-core httpx
A2A_URL=https://a2a.example.com python3 integrations/langgraph/example.py
```

---

## CrewAI

[`integrations/crewai/example.py`](integrations/crewai/example.py) — wraps the A2A call as `BaseTool` subclasses (`LLMSTxtAdviseTool`, `LLMSTxtAuditTool`) that any CrewAI agent can use.

```bash
pip install crewai httpx
A2A_URL=https://a2a.example.com python3 integrations/crewai/example.py
```

---

## Python

Two patterns in [`integrations/python/example.py`](integrations/python/example.py):

1. **Use the wrapper** (`scripts/a2a-client.py`) — full client with retries, validation, SSE streaming
2. **Use raw `httpx`** — when you don't want to ship the wrapper

Both async. The wrapper is recommended for production.

```python
import asyncio, importlib.util
spec = importlib.util.spec_from_file_location("a2a_client", "scripts/a2a-client.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

async def main():
    async with mod.A2AClient("https://a2a.example.com",
                             bearer_token="...") as client:
        task = await client.send(skill="advise", text="Should I ship llms.txt?")
        print(task["artifacts"][0]["parts"][0]["text"])

asyncio.run(main())
```

---

## Raw HTTP

The A2A server speaks standard JSON-RPC 2.0 over HTTP. Call it from anything:

- **curl**: see [`integrations/raw-http/curl-examples.sh`](integrations/raw-http/curl-examples.sh)
- **Node.js**: `fetch(url, { method: 'POST', body: JSON.stringify({ jsonrpc: '2.0', ... }) })`
- **Go**: `http.Post(url, "application/json", bytes.NewReader(envelope))`
- **PHP, Ruby, Java, .NET, Rust** — any HTTP client works

The JSON-RPC envelope shape is identical across languages:

```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "your message"}]
    },
    "metadata": {"skill": "advise"}
  }
}
```

Response shape:

```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "result": {
    "id": "task-uuid",
    "status": {"state": "completed"},
    "artifacts": [
      {
        "parts": [{"kind": "text", "text": "the response"}]
      }
    ]
  }
}
```

Or with an error:

```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "error": {"code": -32602, "message": "Unknown skill: foo"}
}
```

---

## A2A-to-A2A (cross-agent calls)

If you have another A2A v1.0 agent (Microsoft Copilot Studio, AWS Bedrock AgentCore, Salesforce Agentforce, ServiceNow, etc.), it can call this advisor directly:

1. Your agent's A2A client fetches our Agent Card at `https://our-host/.well-known/agent-card.json`
2. Discovers our 8 skills
3. Sends `message/send` with the skill ID it wants
4. Receives the artifact

No special code on either side — both ends speak the same v1.0 protocol.

Full spec compliance details: [`A2A.md`](A2A.md).

---

## Skill IDs (for `metadata.skill`)

| ID | What it does |
|---|---|
| `advise` | Decision questions, general guidance |
| `audit` | Review existing llms.txt against 15 anti-patterns |
| `generate` | Create new file from curated templates |
| `customize` | Surgical section updates |
| `deploy` | Server config + CI validation |
| `stakeholder-comms` | Draft emails / Jira tickets |
| `setup-recommender` | Orientation — what skill should I use |
| `cold-start-interview` | Multi-turn profile configuration (less ideal for one-shot A2A calls) |

---

## Mode comparison

| Mode | Set via | What it returns | When to use |
|---|---|---|---|
| **mock** (default) | `A2A_MODE=mock` | Skill-aware canned responses based on SKILL.md frontmatter | Local dev, integration testing, sanity checks |
| **live** | `A2A_MODE=live` + `ANTHROPIC_API_KEY` | Real Claude responses with the skill's full SKILL.md as system prompt | Production |

Both modes return the same shape, so you can develop against mock and flip to live in production without code changes.

---

## Skill-trigger logic stays the same

The descriptions in [`skills/*/SKILL.md`](skills/) (which determine how Claude Code's skill router picks a skill) are also what Claude sees as the system prompt in live A2A mode. So:

- A vague question to `advise` → same disambiguation behavior as inside Claude Code
- An audit request to `audit` → same 15-anti-pattern checklist
- A profile-bounce condition → same `[PROVISIONAL]` tag in the response

100% behavior parity between Claude Code plugin invocation and A2A invocation.

---

## What's NOT yet supported

Honest list of gaps:

| Missing | Workaround | Likely added in |
|---|---|---|
| Native n8n custom node (instead of generic HTTP node) | Use the HTTP Request node — works fine | When demand justifies the npm package |
| Zapier / Make.com pre-built triggers | Same — generic HTTP works | Same |
| Multi-turn `cold-start-interview` via single A2A call | Use the Claude Code plugin for this skill | n8n etc. aren't great for multi-turn anyway |
| Hosted public SaaS (turn-key, no self-deploy) | Self-deploy via Render/Fly/Railway | Would require commercial model |
| OAuth2 / DPoP / mTLS auth | Bearer tokens cover most cases | If/when an enterprise integrator asks |
| Streaming over n8n / Zapier (SSE) | Use `message/send` not `message/stream` | n8n doesn't natively handle SSE |

---

## Next steps by role

| You want to... | Do this |
|---|---|
| See it work in 60 seconds | `docker compose up`, then `bash integrations/raw-http/curl-examples.sh` |
| Build a quick automation | Open [`integrations/n8n/README.md`](integrations/n8n/README.md) |
| Build a multi-agent system | Open [`integrations/langgraph/example.py`](integrations/langgraph/example.py) or [`integrations/crewai/example.py`](integrations/crewai/example.py) |
| Deploy permanently | Open [`deploy/README.md`](deploy/README.md) |
| Understand the protocol | Open [`A2A.md`](A2A.md) |
| Validate the deploy | Run `python3 -m pytest tests/` — 42 tests, ~1s |
