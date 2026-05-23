---
title: A2A Tier 3 - Client
tags:
  - architecture
  - a2a
  - tier-3
  - client
aliases:
  - A2A Client
  - Tier 3
created: 2026-05-23
updated: 2026-05-23
---

# A2A Tier 3 — Client

> [!info] Async A2A v1.0 client (class + CLI)
> `A2AClient` class for programmatic use, CLI for human use. Both call out to ANY A2A v1.0-compliant server (not just ours).

## What it does

- **`discover(url)`** — fetch + validate Agent Card; rejects v2.x or malformed
- **`send(skill, text)`** — sync send-and-wait
- **`stream(skill, text)`** — async iterator over SSE events
- **`get_task(id)` / `cancel_task(id)` / `list_tasks()`**
- Bearer auth via `A2A_BEARER` env-var or constructor arg
- Capped exponential backoff on 5xx

## Exception hierarchy

- `A2AError`
  - `A2AHttpError` (HTTP layer)
  - `A2ARpcError` (JSON-RPC error response)
  - `A2AValidationError` (Agent Card shape failure)

## CLI usage

```bash
python3 scripts/a2a-client.py http://localhost:8000 discover
python3 scripts/a2a-client.py http://localhost:8000 send --skill advise --text "..."
python3 scripts/a2a-client.py http://localhost:8000 stream --skill audit --text "..."
python3 scripts/a2a-client.py http://localhost:8000 list --limit 20
python3 scripts/a2a-client.py http://localhost:8000 get <task-id>
python3 scripts/a2a-client.py http://localhost:8000 cancel <task-id>

# With auth:
A2A_BEARER=token python3 scripts/a2a-client.py http://localhost:8000 discover
```

## Source

- `../scripts/a2a-client.py`
- `../A2A.md` § Tier 3
- `../integrations/python/example.py` — programmatic usage

## Related

- [[A2A Tier 2 - Server]] — what this client talks to
- [[Integrations]] — n8n, LangGraph, CrewAI alternatives
- [[Quality Refinement Pipeline]] — uses this to send + judge
