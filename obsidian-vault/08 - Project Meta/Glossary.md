---
title: Glossary
tags:
  - meta
  - glossary
  - reference
aliases:
  - terms
  - definitions
created: 2026-05-23
updated: 2026-05-23
---

# Glossary

> [!info] Terms used throughout the vault
> Alphabetical. Internal concepts link to their dedicated note.

## A

**A2A** — Agent-to-Agent protocol v1.0 (Linux Foundation, March 2026). See [[A2A Protocol]].

**Anti-pattern** — A documented failure mode. The [[audit]] skill checks against 17 of them. See [[Map of Content#Anti-patterns (17)]].

**Anthropic API** — The Messages API used in live mode. Requires `ANTHROPIC_API_KEY`.

## B

**Bearer auth** — HTTP `Authorization: Bearer <token>` scheme used by [[A2A Tier 2 - Server]]. Configure via `A2A_API_KEYS=caller1=key1,caller2=key2` env-var.

**Best-of-N** — Generate N candidates, pick the best via a verifier. See [[Best-of-N Sampling]].

## C

**Cold-start interview** — The setup conversation that writes a practice profile. See [[cold-start-interview]].

**Composition router** — Logic that combines product-domain × delivery-channel sectors. See [[sector router]].

## D

**Decision framework** — The matrix [[advise]] uses to recommend SHIP / SKIP. Lives in `../knowledge/04-decision-framework.md`.

**Defects** — Specific quality issues identified by [[LLM Judge]] in Stage 2. Fed to [[Self-Refine]] in Stage 3.

## E

**Empirical baseline** — The honest stance: null AI-citation impact per three studies. See [[Empirical baseline]].

## G

**GEO** — Generative Engine Optimization. The broader discipline of which llms.txt is one (small) part.

**Gold standard** — A hand-iterated reference file used as the comparison target in [[LLM Judge|gold-parity testing]].

## J

**Judge variance** — The ±0.2-0.3 score swing between identical evaluations by the same [[LLM Judge]]. Why stable 10/10 is unrealistic.

**JSON-RPC 2.0** — The wire protocol used by [[A2A Tier 2 - Server]].

## L

**llms.txt** — The plain-text content map for AI systems proposed by Jeremy Howard / Answer.AI (Sept 2024). [llmstxt.org](https://llmstxt.org).

**LLM judge** — Using an LLM to score another LLM's output. See [[LLM Judge]].

## M

**MCP** — Model Context Protocol. Agent-to-tool (different from agent-to-agent [[A2A Protocol|A2A]]).

**Mock mode** — A2A server mode that returns canned skill-aware responses without calling Claude. See [[A2A Tier 2 - Server]].

## P

**Per-skill max_tokens** — The token-budget table in `scripts/a2a-server.py`. `generate=16K`, `audit=8K`, `advise=4K`, etc.

**PolyForm Noncommercial 1.0.0** — The current [[License model|license]]. Free for personal/research/education/charity; commercial requires paid license.

**Practice profile** — The user's site-specific configuration written by [[cold-start-interview]] to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`.

**PROVISIONAL mode** — Skills' fallback when the profile is unconfigured. Generic defaults; outputs tagged `[PROVISIONAL]`.

## R

**Refine pipeline** — The multi-stage quality refinement. See [[Quality Refinement Pipeline]].

## S

**Self-Refine** — Madaan et al. 2023 critique-revise pattern. +20% absolute improvement. See [[Self-Refine]].

**SOTA** — State-of-the-art. As of May 2026, see [[Quality Refinement Pipeline#References]].

**SPA caveat** — Note in llms.txt that a JavaScript-rendered subdomain returns an empty shell to HTML crawlers.

**Stripe pattern** — The canonical modern best-practice structure for llms.txt: For-AI-Systems → SEO Routing → Priority Pages → Transactional → Structured Data → Intent Router → Entity Facts → per-category → Optional.

**SSE** — Server-Sent Events, used by [[A2A Tier 2 - Server]]'s `message/stream` method.

## T

**Tier 1 / Tier 2 / Tier 3** — A2A capability layers. See [[A2A Tier 1 - Agent Card]], [[A2A Tier 2 - Server]], [[A2A Tier 3 - Client]].

## U

**URL pattern technique** — Declare `https://{site}/{category-slug}/{city-slug}` once; let LLMs construct long-tail URLs from the pattern. Avoids [[01 Bloated enumeration]].

## V

**Validate.sh** — The CI-grade llms.txt linter. Magic-byte format check, phone-number leakage detection, UTF-8/BOM check, single-H1, size, URL liveness, SHA-256.

## Related

- [[Map of Content]]
- [[Architecture]]
