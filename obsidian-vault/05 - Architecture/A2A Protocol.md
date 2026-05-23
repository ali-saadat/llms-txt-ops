---
title: A2A Protocol
tags:
  - architecture
  - a2a
  - moc
aliases:
  - A2A
  - agent-to-agent
created: 2026-05-23
updated: 2026-05-23
---

# A2A Protocol

> [!abstract] Agent-to-Agent v1.0
> Linux Foundation protocol (March 2026 v1.0 spec). Lets agents discover, communicate, and collaborate across vendors. Complements [[MCP|MCP (Model Context Protocol)]] which is agent-to-tool.

## Three tiers, all implemented

| Tier | What | Status | Note |
|---|---|---|---|
| Discovery | [[A2A Tier 1 - Agent Card]] | ✅ Live | `.well-known/agent-card.json` |
| Server endpoint | [[A2A Tier 2 - Server]] | ✅ Implemented | `scripts/a2a-server.py` |
| Client (outbound) | [[A2A Tier 3 - Client]] | ✅ Implemented | `scripts/a2a-client.py` |

## MCP vs A2A

| Protocol | Direction | Use case |
|---|---|---|
| **MCP** | Agent → Tool | Let agent call GitHub API |
| **A2A** | Agent → Agent | Let one company's agent call another's |
| **Both** | Composed | A2A agent uses MCP tools, exposed via A2A |

This project supports BOTH: MCP via `.mcp.json` + [[CONNECTORS]] for vendor-agnostic tool calls; A2A across all three tiers for inbound + outbound.

## Why v1.0.0 path differs

A2A v0.x used `/.well-known/agent.json`. v1.0 (March 2026) changed to `/.well-known/agent-card.json` (hyphenated). Old clients 404. The Agent Card here uses the v1.0 path.

## Source

- `../A2A.md` — full guide
- `../.well-known/agent-card.json` — Tier 1 artifact

## Related

- [[A2A Tier 1 - Agent Card]]
- [[A2A Tier 2 - Server]]
- [[A2A Tier 3 - Client]]
- [[Architecture]]
- [[Integrations]] — how non-A2A clients (n8n, raw HTTP) connect
