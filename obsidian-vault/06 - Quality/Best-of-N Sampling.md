---
title: Best-of-N Sampling
tags:
  - quality
  - sota
  - sampling
aliases:
  - BoN
  - Best-of-N
created: 2026-05-23
updated: 2026-05-23
---

# Best-of-N Sampling

> [!info] Stage 1 of [[Quality Refinement Pipeline]]
> Generate N candidates with different prompt variants (temperature substitutes), use [[LLM Judge]] to pick the best.

## How it works here

```
Generate 3 candidates in parallel via [[A2A Tier 2 - Server]]:
  - "conservative" interpretation
  - "balanced" interpretation
  - "expressive" interpretation
→ Judge each via [[LLM Judge]]
→ Return highest-scoring as refinement seed for [[Self-Refine]]
```

## Why prompt variants instead of temperature?

The A2A server doesn't expose `temperature` on its API (per-skill `max_tokens` is the only tunable). We approximate diversity via prompt-level rephrasing — coarser than true temperature but works for refinement.

## Research lineage

- [Scalable Best-of-N Selection via Self-Certainty (arXiv:2502.18581, 2025)](https://arxiv.org/abs/2502.18581) — proves BoN scales without reward models
- ELHSR (OpenReview 2025) — hidden-state reward models, +12.7% on MATH with 0.005% params
- [Wang et al. 2022 — Self-Consistency](https://arxiv.org/abs/2203.11171) — original BoN-style work

## Related

- [[Quality Refinement Pipeline]] — orchestrator
- [[LLM Judge]] — the verifier
- [[Self-Refine]] — the next stage
