# A2A (Agent-to-Agent) Protocol Support

*Implementation status, deployment guide, and security notes for A2A v1.0 support in the llms-txt-advisor plugin.*

## TL;DR

| Tier | What it is | Status | Where it lives |
|---|---|---|---|
| **Tier 1: Discovery** | Static Agent Card at `/.well-known/agent-card.json` | ✅ **Live** | `.well-known/agent-card.json` |
| **Tier 2: Server endpoint** | Live JSON-RPC over HTTP endpoint that other A2A agents can call | ✅ **Implemented** | `scripts/a2a-server.py` |
| **Tier 3: Client-side** | Our agents can call OUT to external A2A agents | ✅ **Implemented** | `scripts/a2a-client.py` |

Full test coverage: 42 pytest tests across server, client, and end-to-end loopback. Run `python3 -m pytest tests/` to verify.

## What is A2A?

A2A (Agent-to-Agent / Agent2Agent) is an open protocol for **horizontal communication between AI agents** — different agents from different vendors discovering, communicating, and collaborating with each other. It complements MCP (Model Context Protocol), which is for **vertical communication between an agent and its tools**.

| Protocol | Direction | Use case |
|---|---|---|
| **MCP** | Agent → Tool | "Let my agent call the GitHub API" |
| **A2A** | Agent → Agent | "Let one company's agent call another company's agent" |
| **Both** | Composed | A2A agent internally uses MCP tools, exposes A2A to other agents |

This plugin has full support for both: MCP via `.mcp.json` + `~~category` placeholders (for tool calls), and A2A across all three tiers.

## Current state of A2A (May 2026)

- **Launched**: April 2025 by Google Cloud with ~50 partners
- **Donated to Linux Foundation**: June 2025
- **Spec v1.0 released**: March 12, 2026
- **Adoption**: 150+ supporting organizations; production deployments at Microsoft (Azure AI Foundry, Copilot Studio), AWS (Bedrock AgentCore), Salesforce (Agentforce), SAP (Joule), ServiceNow, Workday, PayPal
- **Native framework support**: LangGraph, CrewAI, LlamaIndex Agents, Semantic Kernel, AutoGen, Google ADK
- **No native support yet from**: Anthropic Claude Agent SDK, OpenAI Agents SDK (both focus on MCP)
- **Public agent registry**: [a2aregistry.org](https://a2aregistry.org/) — ~15 verifiable public agents as of May 2026

## Tier 1: Agent Card Discovery

### What we ship

A static A2A v1.0-compliant Agent Card at `.well-known/agent-card.json`. Declares all 8 plugin skills as `AgentSkill` objects with `id`, `name`, `description`, `inputModes`, `outputModes`, `examples`, and `tags`.

### Why the hyphenated path

A2A v0.x used `/.well-known/agent.json`. The v1.0 spec (March 2026) changed to `/.well-known/agent-card.json` (hyphenated). Old blog posts and v0.x clients will 404. **We use the v1.0 path.**

### Validation

```bash
python3 -c "import json; json.load(open('.well-known/agent-card.json'))"
# (No output = valid JSON)

# Full client-side validation:
python3 scripts/a2a-client.py http://localhost:8000 discover
```

## Tier 2: Server Endpoint

### What it is

`scripts/a2a-server.py` is a production-grade FastAPI app that implements:

- **`GET /.well-known/agent-card.json`** — discovery
- **`POST /a2a`** — JSON-RPC 2.0 endpoint with these methods:
  - `message/send` — submit a task, wait for the completed result
  - `message/stream` — submit a task, get SSE stream of state + delta events
  - `tasks/get` — fetch task state + artifacts by ID
  - `tasks/cancel` — cancel a non-terminal task
  - `tasks/list` — list recent tasks (filtered to your caller)
- **`GET /health`** — readiness probe
- **`GET /`** — agent summary (skills, mode, auth status)

### Features

| Feature | Implementation |
|---|---|
| Task persistence | SQLite (default `./a2a-tasks.db`, configurable) — survives restarts |
| Auth | Bearer-token via `A2A_API_KEYS=caller1=key1,caller2=key2` env-var; disabled if unset |
| Rate limiting | Per-caller sliding window (default 30 req/min, `--rate-limit` flag) |
| Caller isolation | Each caller only sees their own tasks (server-enforced in `tasks/get`, `tasks/list`) |
| Audit logging | One JSON line per request to `./a2a-audit.log` |
| Mock mode | Skill-aware canned responses (default — no API key needed) |
| Live mode | Real Claude API calls with the skill's SKILL.md as system prompt |
| Streaming | SSE chunks via `message/stream` |

### Running the server

```bash
# Mock mode (no Claude calls — for testing)
python3 scripts/a2a-server.py --port 8000

# Live mode (real Claude calls)
export ANTHROPIC_API_KEY=sk-ant-...
export A2A_MODE=live
python3 scripts/a2a-server.py --port 8000

# Production (live + auth + custom rate limit)
export ANTHROPIC_API_KEY=sk-ant-...
export A2A_MODE=live
export A2A_API_KEYS="salesforce-agentforce=$(openssl rand -hex 32),servicenow=$(openssl rand -hex 32)"
python3 scripts/a2a-server.py --host 0.0.0.0 --port 8000 --rate-limit 60
```

All flags + env-vars:

| Env-var | Flag | Default | Purpose |
|---|---|---|---|
| `A2A_MODE` | `--mode` | `mock` | `mock` or `live` |
| `A2A_DB_PATH` | `--db` | `./a2a-tasks.db` | SQLite task store |
| `A2A_AUDIT_LOG` | `--audit` | `./a2a-audit.log` | Audit JSONL path |
| `A2A_RATE_LIMIT` | `--rate-limit` | `30` | Per-caller req/min |
| `A2A_API_KEYS` | — | unset | Bearer-token map (`name1=key1,name2=key2`) |
| `ANTHROPIC_API_KEY` | — | unset | Required for live mode |
| `A2A_MODEL` | — | `claude-sonnet-4-5-20250929` | Model used in live mode |

### Print resolved config (no server start)

```bash
python3 scripts/a2a-server.py --print-config
```

### Deployment

Same patterns as any FastAPI service:

```bash
# Local dev
python3 scripts/a2a-server.py --port 8000

# Production with multiple workers
pip install gunicorn
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 \
    --pythonpath scripts \
    "a2a-server:build_app()"
```

Behind a reverse proxy (recommended), terminate TLS at the proxy, set:
- `X-Forwarded-Proto`, `X-Forwarded-For`, `X-Forwarded-Host` headers
- A long enough timeout to accommodate Claude calls (60s+)
- Disable response buffering for `/a2a` so SSE streaming works (`X-Accel-Buffering: no` is already set by the server)

## Tier 3: Client

### What it is

`scripts/a2a-client.py` provides:

1. An **`A2AClient`** class for programmatic use (async)
2. A **CLI** for human use (`python3 scripts/a2a-client.py <url> <cmd> ...`)

### Programmatic usage

```python
from scripts.a2a_client import A2AClient   # see import note below

async with A2AClient("https://other-agent.example.com",
                     bearer_token="my-token") as client:
    card = await client.discover()
    print(f"Connected to {card['name']} with {len(card['skills'])} skills")

    task = await client.send(skill="audit", text="please review my llms.txt")
    text = task["artifacts"][0]["parts"][0]["text"]

    # Or stream:
    async for event in client.stream(skill="audit", text="..."):
        if "delta" in event.get("result", {}):
            print(event["result"]["delta"]["text"], end="")
```

> **Import note**: the script is named `a2a-client.py` (hyphen). For programmatic use, either rename it to `a2a_client.py` in your project or use `importlib.util.spec_from_file_location` — see `tests/conftest.py` for the pattern.

### CLI usage

```bash
# Discover what an agent exposes
python3 scripts/a2a-client.py http://localhost:8000 discover

# Send a message and wait
python3 scripts/a2a-client.py http://localhost:8000 send \
    --skill advise --text "should I ship llms.txt for a marketing site?"

# Stream the response token by token
python3 scripts/a2a-client.py http://localhost:8000 stream \
    --skill audit --text "review this file"

# List your recent tasks
python3 scripts/a2a-client.py http://localhost:8000 list --limit 20

# Inspect or cancel a specific task
python3 scripts/a2a-client.py http://localhost:8000 get <task-id>
python3 scripts/a2a-client.py http://localhost:8000 cancel <task-id>

# With auth
A2A_BEARER=my-token python3 scripts/a2a-client.py http://localhost:8000 discover
```

### Client features

- **Agent Card validation** — fetches and shape-checks before any send. Rejects v2.x or malformed cards.
- **JSON-RPC envelope handling** — wraps every request, unwraps results, raises `A2ARpcError` on error responses.
- **Retry on 5xx** — capped exponential backoff (configurable via `retries=` constructor arg).
- **Streaming via SSE** — `client.stream()` is an async iterator over JSON-RPC frames.
- **Bearer token** — explicit arg or `A2A_BEARER` env-var.
- **Async context manager** — proper httpx client cleanup.

## Testing

```bash
# Full A2A test suite (42 tests, runs in ~1 second)
python3 -m pytest tests/ -v

# Just the server tests
python3 -m pytest tests/test_a2a_server.py -v

# Just the client tests (no network)
python3 -m pytest tests/test_a2a_client.py -v

# End-to-end loopback (client → server via httpx.ASGITransport)
python3 -m pytest tests/test_a2a_loopback.py -v
```

Test coverage:

| Area | Tests |
|---|---|
| Discovery (`/`, `/health`, `/.well-known/agent-card.json`) | 3 |
| `message/send` happy paths (all 8 skills) | 2 |
| `message/send` error paths (-32600/-32601/-32602/-32700) | 7 |
| Task lifecycle (`tasks/get`, `tasks/cancel`, `tasks/list`) | 6 |
| Auth (no keys, missing token, wrong token, valid token, caller isolation) | 5 |
| Rate limiting | 1 |
| SQLite persistence across restart | 1 |
| SSE streaming | 1 |
| Audit log | 1 |
| Client-side validation | 5 |
| Client unit tests (httpx.MockTransport) | 6 |
| End-to-end loopback (httpx.ASGITransport) | 4 |
| **Total** | **42** |

## Security checklist

Before exposing Tier 2 publicly:

1. ✅ **Always set `A2A_API_KEYS`**. Auth is opt-in by design (so local dev / tests just work), but unauthenticated public exposure is denial-of-wallet bait.
2. ✅ **TLS only**. Terminate at a reverse proxy with valid certs. The server speaks plain HTTP intentionally.
3. ✅ **Per-caller rate limits**. Default 30/min may be too generous for paid endpoints — tune `--rate-limit`.
4. ✅ **Caller isolation**. `tasks/get` and `tasks/list` are already isolated per caller. Don't disable this.
5. ✅ **Audit log retention**. The `a2a-audit.log` is JSONL, append-only — ship it to your SIEM or centralized logging.
6. ✅ **API key rotation**. `A2A_API_KEYS` is read at startup. Rotate by redeploying with new values; nothing persists keys to disk.
7. ✅ **Quotas**. The in-memory rate limiter is per-process. Behind multiple replicas, add a shared limiter (Redis token bucket) — easy to bolt on at `TokenBucket` in the server.
8. ✅ **Egress for Tier 3**. The client follows redirects, retries on 5xx. If calling untrusted agents, sandbox the network egress.

## Integration with the managed-agent cookbook

`managed-agent-cookbooks/staleness-watcher/agent.yaml` is designed for Anthropic's Managed Agents API. To make it A2A-callable as well:

1. Deploy the agent via the Managed Agents API (see `scripts/deploy-managed-agent.sh`)
2. Run `a2a-server.py` in live mode in front of it
3. The A2A server's `message/send` handler invokes the skill, which can include calls into the managed agent
4. Optionally, embed `A2AClient` inside the staleness-watcher itself so the agent can fan out to external A2A agents (already supported — see Tier 3 client)

## A2A vs MCP — when to use which

| Situation | Choose |
|---|---|
| You're calling a specific tool (DB query, API call) | **MCP** |
| You're calling another agent (has its own reasoning loop) | **A2A** |
| You're being called by an LLM as a tool | **MCP** server |
| You're being called by another agent | **A2A** server |
| Both: agent that wraps tools and is callable | **Both** (A2A externally, MCP internally) |

## Versioning and SDK pinning

- A2A v1.0 (March 2026) is what this plugin targets
- v0.x clients won't work with our `/.well-known/agent-card.json` path
- The client validates `protocolVersion` starts with `1.` and rejects 2.x
- When the spec evolves, pin the SDK version in `requirements.txt`

## Risks

1. **Spec churn** — v1.0 is recent; v0.x → v1.0 removed the `kind` discriminator and relocated extended-card fields
2. **Discovery path gotcha** — `/.well-known/agent.json` (v0.x) vs `/.well-known/agent-card.json` (v1.0)
3. **Delegation trail** — A2A agents may be invoked by other agents acting on behalf of users; audit logs are essential
4. **Cost / DoW** — Live mode proxies LLM calls; without quotas this is a denial-of-wallet target
5. **Few production failure cases yet** — most postmortems live inside enterprises; biggest reported pain is interop mismatches between SDK versions

## Future work (when triggered by demand)

| Feature | Trigger |
|---|---|
| Push notifications (webhook callbacks on completion) | First paying integration that needs them |
| Redis-backed rate limiter | When multi-replica deployment is needed |
| OAuth2 / DPoP auth | When an enterprise integrator requires it |
| State transition history | When a debugger asks for it |
| Multi-tenant database isolation | When SaaS deployment is on the roadmap |

The current implementation is intentionally minimal-but-correct. Each future feature is a small, well-scoped addition on top.

## Sources

- [A2A v1.0 specification](https://a2a-protocol.org/latest/specification/) (March 2026)
- [Agent Discovery docs](https://a2a-protocol.org/latest/topics/agent-discovery/)
- [Linux Foundation A2A project](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [LF A2A one-year update, April 2026](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)
- [a2aproject/A2A on GitHub](https://github.com/a2aproject/A2A)
- [a2a-python SDK](https://github.com/a2aproject/a2a-python)
- [a2aregistry.org](https://a2aregistry.org/) — community agent registry
- [Auth0: MCP vs A2A](https://auth0.com/blog/mcp-vs-a2a/)
- [AWS Bedrock AgentCore A2A contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html)
- JSON-RPC 2.0: https://www.jsonrpc.org/specification
