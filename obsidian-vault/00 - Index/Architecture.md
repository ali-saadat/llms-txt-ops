---
title: Architecture
tags:
  - architecture
  - moc
aliases:
  - System Map
created: 2026-05-23
updated: 2026-05-23
---

# Architecture

> [!abstract] One-paragraph summary
> A Claude Code plugin (8 skills) + an A2A v1.0 server callable from anywhere (Docker / Render / Fly / Railway / n8n / LangGraph / CrewAI). Skills are defined by `SKILL.md` files with frontmatter triggers; the live A2A server feeds the SKILL.md as system prompt and the user message as user prompt to `claude-sonnet-4-6`. A quality-refinement pipeline (Best-of-N + [[Self-Refine]] + [[Post-Processors|deterministic post-processors]]) closes the last 5-10% to gold-standard quality.

---

## High-level diagram

```mermaid
graph TB
    subgraph User["User entry points"]
        A[Claude Code]
        B[n8n / Zapier]
        C[LangGraph / CrewAI]
        D[curl / any HTTP]
    end
    subgraph Plugin["llms-txt-ops"]
        E[Tier 1 Agent Card]
        F[Tier 2 A2A Server<br/>FastAPI + SQLite]
        G[Tier 3 Client<br/>A2AClient]
        H[Skills SKILL.md prompts<br/>8 skills]
        I[Knowledge corpus<br/>9 files + sectors + languages]
        J[Refinement Pipeline<br/>refine.py + post_processors.py]
    end
    K[Anthropic API<br/>claude-sonnet-4-6]
    A -->|/llms-txt-advisor:skill| H
    B -->|HTTP POST /a2a| F
    C -->|HTTP POST /a2a| F
    D -->|JSON-RPC| F
    G -->|JSON-RPC| F
    F -->|live mode| K
    F -->|reads| H
    H -->|loads on demand| I
    J -->|orchestrates| F
    J -->|critique-revise| K
    F -.serves.- E

    class E,F,G,H,I,J internal-link
```

---

## Component map

| Layer | Component | Note |
|---|---|---|
| Discovery | [[A2A Tier 1 - Agent Card]] | `.well-known/agent-card.json` |
| Server | [[A2A Tier 2 - Server]] | `scripts/a2a-server.py` (FastAPI + JSON-RPC + SQLite + SSE) |
| Client | [[A2A Tier 3 - Client]] | `scripts/a2a-client.py` (async + CLI) |
| Refinement | [[Quality Refinement Pipeline]] | `scripts/refine.py` (Best-of-N + Self-Refine + post-process) |
| Post-processing | [[Post-Processors]] | `scripts/post_processors.py` (deterministic) |
| Skills | 8 skills | `skills/*/SKILL.md` |
| Knowledge corpus | 9 numbered files + sectors + languages | `knowledge/` |
| Cookbook | [[Cookbook - Staleness Watcher]] | `managed-agent-cookbooks/staleness-watcher/` |
| Integrations | n8n + LangGraph + CrewAI + Python + curl | [[Integrations]] |
| Deploys | Docker · Render · Fly · Railway · self-hosted | [[Deploy targets]] |

---

## Skill invocation flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude Code
    participant S as SKILL.md
    participant K as Knowledge corpus
    participant Cl as Claude (Anthropic API)

    U->>C: /llms-txt-advisor:generate
    C->>S: load skills/generate/SKILL.md
    S->>K: load sectors/marketplace.md (on-demand)
    S->>K: load knowledge/05-implementation.md
    C->>Cl: system=SKILL.md+context, user=profile
    Cl-->>C: generated llms.txt
    C-->>U: present file + offer save/deploy
```

For the full path with refinement, see [[Quality Refinement Pipeline]].

---

## Architecture patterns adopted

| Pattern | Source repo |
|---|---|
| Two-CLAUDE.md template + cold-start + bounce-on-placeholder | `anthropics/claude-for-legal` |
| `~~category` placeholders + Standalone-vs-Supercharged | `anthropics/knowledge-work-plugins` |
| Agent + vertical split + sync.py + 3-tier cookbook | `anthropics/financial-services` |
| Meta-skill recommender | `claude-for-legal/legal-builder-hub` |
| Skill-creator eval workflow | `anthropics/skills` |

See [[Versioning policy]] for how patterns evolve here.

---

## Related notes

- [[Map of Content]] — top-level index
- [[A2A Protocol]] — protocol-level details
- [[Quality Refinement Pipeline]] — SOTA refinement
- [[Empirical baseline]] — the honest stance baked into every skill
