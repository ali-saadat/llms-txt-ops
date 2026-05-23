---
title: A2A Tier 2 - Server
tags:
  - architecture
  - a2a
  - tier-2
  - server
aliases:
  - A2A Server
  - Tier 2
created: 2026-05-23
updated: 2026-05-23
---

# A2A Tier 2 — Server endpoint

> [!important] FastAPI + JSON-RPC 2.0 + SSE + SQLite
> Production-grade Tier 2 server. Two modes: `mock` (canned responses, no API key) and `live` (real Claude calls). Per-skill `max_tokens` budgets.

## JSON-RPC methods

- `message/send` — submit task, wait for completion
- `message/stream` — submit + get SSE stream of state + delta events
- `tasks/get` — fetch by ID
- `tasks/cancel` — cancel non-terminal task
- `tasks/list` — recent tasks (filtered to caller via [[Bearer auth]])

## Discovery endpoints

- `GET /.well-known/agent-card.json` (serves [[A2A Tier 1 - Agent Card|Tier 1]])
- `GET /` (root summary)
- `GET /health` (readiness probe)

## Features

| Feature | Note |
|---|---|
| Task persistence | SQLite at `./a2a-tasks.db` |
| Auth | Bearer-token via `A2A_API_KEYS=caller1=key1,caller2=key2` |
| Rate limiting | Per-caller token bucket (default 30 req/min) |
| Caller isolation | tasks/get + tasks/list scoped per caller |
| Audit logging | JSONL to `./a2a-audit.log` |
| Per-skill max_tokens | generate=16K · audit=8K · advise=4K · etc. |

## JSON-RPC error codes

| Code | Meaning |
|---|---|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params (e.g., unknown skill) |
| -32603 | Internal error |
| -32001 | Unauthorized |
| -32002 | Rate limited |
| -32003 | Task not found |
| -32004 | Task in terminal state |

## Run it

```bash
# Mock mode (no API key)
python3 scripts/a2a-server.py --port 8000

# Live mode
export ANTHROPIC_API_KEY=sk-ant-...
A2A_MODE=live python3 scripts/a2a-server.py --port 8000

# Via Docker
docker compose up
```

## Source

- `../scripts/a2a-server.py`
- `../A2A.md` § Tier 2

## Related

- [[A2A Tier 1 - Agent Card]] — what /well-known serves
- [[A2A Tier 3 - Client]] — talks to this server
- [[Deploy targets]] — where to host this
- [[Quality Refinement Pipeline]] — uses this as substrate
