---
title: Cookbook - Staleness Watcher
tags:
  - architecture
  - cookbook
  - managed-agent
aliases:
  - staleness-watcher
created: 2026-05-23
updated: 2026-05-23
---

# Cookbook — Staleness Watcher

> [!important] 3-tier security split
> Pattern adopted from `anthropics/financial-services`. Each tier has the minimum capability surface area for its job.

## The three tiers

```mermaid
graph LR
    A[Tier 1<br/>crawler<br/>Read+Grep+Bash<br/>NO MCP, NO Write] --> B[Tier 2<br/>analyzer<br/>trusted MCP only<br/>NO Write]
    B --> C[Tier 3<br/>report-writer<br/>ONLY Write<br/>scoped to ./out/]
```

| Tier | Subagent | Capabilities | Why |
|---|---|---|---|
| 1 | `crawler.yaml` | Read, Grep, Bash | Touches untrusted HTML; no MCP, no Write |
| 2 | `analyzer.yaml` | GitHub MCP, Bing AI Performance MCP, Profound MCP | Trusted MCP only; cannot write |
| 3 | `report-writer.yaml` | Write only, scoped to `./out/<domain>/` | Only the writer can write |

## What it does

Quarterly (or on-schedule) health-check for a deployed `llms.txt`:

1. **Crawler** fetches the live llms.txt, robots.txt, sitemap.xml
2. **Analyzer** correlates with GitHub change history + Bing AI Performance metrics + Profound citations data
3. **Report-writer** emits a markdown report identifying drift, broken links, citation trend, action items

## Deploy

```bash
# Dry-run (default, no API call)
bash scripts/deploy-managed-agent.sh staleness-watcher

# Live (requires Anthropic Managed Agents API access + MCP env-vars)
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_MCP_URL=https://...
export BING_WEBMASTER_MCP_URL=https://...
export PROFOUND_MCP_URL=https://...
bash scripts/deploy-managed-agent.sh staleness-watcher --live
```

## Source

- `../managed-agent-cookbooks/staleness-watcher/agent.yaml`
- `../managed-agent-cookbooks/staleness-watcher/subagents/`
- `../scripts/deploy-managed-agent.sh`
- `../agents/staleness-watcher.md` (system prompt)

## Related

- [[Architecture]]
- [[A2A Tier 2 - Server]] — alternative deployment substrate
- [[Deploy targets]]
