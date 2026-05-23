---
title: MCP
tags:
  - architecture
  - external
created: 2026-05-23
updated: 2026-05-23
---

# MCP (Model Context Protocol)

> [!info] Agent-to-tool protocol
> Different from [[A2A Protocol|A2A]] which is agent-to-agent. MCP lets an AI agent call external tools (GitHub API, DB queries, etc.).

This project supports MCP via:
- `.mcp.json` with 13 connector category slots
- `../CONNECTORS.md` with the `~~category` dictionary

See `../CONNECTORS.md` for connector catalog.

## Related

- [[A2A Protocol]] — the other half of the agent stack
- [[Architecture]]

