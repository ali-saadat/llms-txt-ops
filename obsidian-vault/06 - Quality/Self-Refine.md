---
title: Self-Refine
tags:
  - quality
  - sota
  - critique-revise
aliases:
  - critique-revise loop
created: 2026-05-23
updated: 2026-05-23
---

# Self-Refine

> [!important] Stage 3 of [[Quality Refinement Pipeline]]
> Iterative critique → revise loop. Madaan et al. 2023. **+20% absolute improvement** across 7 tasks.

## How it works here

For each iteration (up to 2):

1. [[LLM Judge]] scores the current best candidate, returns specific defects
2. Send candidate + defect list to Claude with "revise to fix these, keep everything else" prompt
3. Re-judge the revision
4. If score improved → new best; if not → stop (diminishing returns)

## Why it works

> [!quote] From Madaan 2023
> "Self-Refine enables LLMs to generate feedback on their work, use it to improve the output, and repeat this process."

The same LLM that generated the draft can usefully critique it — but ONLY if the critique is specific (not "improve quality") and the revise prompt preserves what's correct.

## Empirical observation in this project

| Iteration | Effect |
|---|---|
| 1 | +0.30 typical improvement |
| 2 | +0.10 or no improvement; sometimes regression |
| 3+ | Net negative (diminishing returns + judge variance) |

Why iteration 2 sometimes regresses: judge feedback after the first revision becomes noisier — defects it lists are smaller and the revision prompt churns content that was fine.

## Research lineage

- [Self-Refine: Iterative Refinement with Self-Feedback (Madaan et al. 2023, arXiv:2303.17651)](https://arxiv.org/pdf/2303.17651)
- [Anthropic Constitutional AI](https://www.anthropic.com/news/claudes-constitution) — the same critique-revise pattern at training time
- [Critique-GRPO (arXiv:2506.03106)](https://arxiv.org/pdf/2506.03106) — RL variant

## Related

- [[Quality Refinement Pipeline]]
- [[Best-of-N Sampling]] — Stage 1 (feeds Self-Refine)
- [[Post-Processors]] — Stage 4 (catches what Self-Refine misses)
