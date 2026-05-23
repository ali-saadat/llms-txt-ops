---
title: Integrations
tags:
  - architecture
  - integrations
aliases:
  - Integration kits
created: 2026-05-23
updated: 2026-05-23
---

# Integrations — how to call this from anywhere

> [!info] Two interfaces, multiple consumers
> 1. **Inside Claude Code** — `/llms-txt-advisor:<skill>` slash commands
> 2. **Outside Claude Code** — A2A v1.0 HTTP API from any language or no-code tool

## Pre-built integration kits

| Target | Path | What's there |
|---|---|---|
| n8n | `../integrations/n8n/` | 2 importable workflow JSONs (audit + advise) + README |
| LangGraph | `../integrations/langgraph/example.py` | `@tool` wrappers for the 3 most-called skills |
| CrewAI | `../integrations/crewai/example.py` | `BaseTool` subclasses |
| Python | `../integrations/python/example.py` | Wrapper + raw httpx patterns |
| Raw HTTP (curl/Node/Go/anything) | `../integrations/raw-http/curl-examples.sh` | bash + JSON-RPC envelopes |
| Another A2A v1.0 agent | none needed — uses standard protocol | See [[A2A Protocol]] |

## Common patterns

### Synchronous call

```bash
curl -X POST http://server/a2a \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"jsonrpc":"2.0","id":"1","method":"message/send",
         "params":{"message":{"parts":[{"kind":"text","text":"..."}]},
                   "metadata":{"skill":"advise"}}}'
```

### Streaming via SSE

`method: "message/stream"` + `Accept: text/event-stream` header → series of `data: {jsonrpc...}` events.

## Skill IDs (for `metadata.skill`)

`advise` · `audit` · `generate` · `customize` · `deploy` · `stakeholder-comms` · `setup-recommender` · `cold-start-interview`

See [[Map of Content#Skills (8)]].

## Source

- `../INTEGRATIONS.md` — master guide
- `../integrations/` — code

## Related

- [[A2A Protocol]]
- [[A2A Tier 3 - Client]]
- [[Deploy targets]]
