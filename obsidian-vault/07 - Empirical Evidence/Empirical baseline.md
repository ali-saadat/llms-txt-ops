---
title: Empirical baseline
tags:
  - empirical
  - moc
  - honest-framing
aliases:
  - baseline
  - three studies
created: 2026-05-23
updated: 2026-05-23
---

# Empirical baseline

> [!quote] The plugin's core stance
> The empirical record on llms.txt's direct impact on AI citations is **null** per three independent studies + Google's John Mueller confirming Google doesn't use it.

## Three independent studies

| Study | Sample | Finding |
|---|---|---|
| [[SE Ranking study]] | 300,000 domains | No correlation between llms.txt presence and AI visibility |
| [[OtterlyAI study]] | 90 days of AI crawler logs | LLM crawlers ignore llms.txt; fetch what they want |
| [[Search Engine Land study]] | 10-site controlled test | No measurable citation lift |

## What John Mueller said

> [!quote] Google's John Mueller (multiple 2025 statements)
> Google does not use llms.txt as any kind of ranking or indexing signal.

OpenAI, Anthropic, and other major AI vendors have not publicly committed to using it either.

## What this means for the plugin

- [[advise]] never promises AI-citation lift
- [[stakeholder-comms]] never drafts "this will boost AI traffic" framing
- Honest redirect: schema.org, external citations, content quality, author E-E-A-T

## When llms.txt IS useful (the legitimate cases)

1. **[[dev-docs|Developer documentation]]** — coding agents (Cursor, Claude Code, Cline) read it
2. **Replacing a [[01 Bloated enumeration|bloated existing file]]** — strictly better than the broken status quo
3. **Internal RAG/chatbot grounding** — the curated file doubles as your own AI's source-of-truth

If a site's situation doesn't match one of these three, the plugin recommends SKIP — and explains why with these three studies.

## Source

- `../knowledge/02-empirical-evidence.md`
- `../knowledge/03-seo-perspective.md`
- `../knowledge/04-decision-framework.md`

## Related

- [[Map of Content#Empirical baseline]]
- [[advise]] — cites these studies in every decision
- [[15 Over-promising to stakeholders]] — the anti-pattern that the empirical baseline addresses
