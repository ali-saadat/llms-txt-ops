---
title: A2A Tier 1 - Agent Card
tags:
  - architecture
  - a2a
  - tier-1
aliases:
  - Agent Card
  - Tier 1
created: 2026-05-23
updated: 2026-05-23
---

# A2A Tier 1 — Agent Card (Discovery)

> [!info] What it is
> A static JSON file at `.well-known/agent-card.json` that declares the agent's identity, capabilities, and skills.

## What's in it

- `name`, `displayName`, `description`, `version`, `protocolVersion`
- `provider` (organization + URL)
- `capabilities` (streaming, pushNotifications, stateTransitionHistory)
- `defaultInputModes` / `defaultOutputModes`
- `securitySchemes` (currently `noAuth` since Tier 2 has separate Bearer auth)
- `skills[]` — 8 AgentSkill objects, one per [[Map of Content#Skills (8)|plugin skill]]

## Validation

```bash
python3 -c "import json; json.load(open('.well-known/agent-card.json'))"
# Or via Tier 3 client:
python3 scripts/a2a-client.py http://localhost:8000 discover
```

## Source

- `../.well-known/agent-card.json`
- `../A2A.md` § Tier 1

## Related

- [[A2A Protocol]]
- [[A2A Tier 2 - Server]] — what serves the Agent Card at runtime
- [[Map of Content#Skills (8)]] — what the card declares
