---
title: LLM Judge
tags:
  - quality
  - testing
aliases:
  - quality_judge.py
  - llm_judge.py
created: 2026-05-23
updated: 2026-05-23
---

# LLM Judge

> [!info] Used by [[Quality Refinement Pipeline]] in Stages 2 + 5
> Uses `claude-sonnet-4-6` to score generated output across 8 quality dimensions vs a gold-standard reference (or abstract quality if no gold).

## 8 quality dimensions (1-10 each)

| # | Dimension | What it measures |
|---|---|---|
| 1 | DESCRIPTION_SPECIFICITY | Concrete vs vague/marketing |
| 2 | DIRECTIVE_USEFULNESS | Would LLM benefit from each directive? |
| 3 | SEO_ROUTING_COHERENCE | Query→URL mappings make sense |
| 4 | ENTITY_FACTS_ACCURACY | Founder, founded, scale, structured bullets |
| 5 | PROSE_QUALITY | Reads well end-to-end |
| 6 | FAITHFULNESS_TO_PROFILE | No fabricated URLs, slugs match |
| 7 | STRIPE_PATTERN_FIDELITY | Sections in canonical order |
| 8 | ANTI_PATTERN_ABSENCE | No bloat, no marketing, no leaked scaffolding |

## Variance reality

> [!warning] Judge is stochastic
> Same input, different judge run → ±0.2-0.3 score swing. **Gold standard itself never scores stable 10** — it oscillates 9.25–9.88 across runs (mean 9.55, std 0.20).
>
> A stable 10/10 every run is **not achievable** with this evaluation pattern.

## Two scripts

Both in `.e2e-private/` (gitignored — private test infrastructure):

- `llm_judge.py` — pass/fail structural judge (10 binary checks)
- `quality_judge.py` — 1-10 quality judge (8 dimensions) ← used by refine pipeline

## Usage

```bash
python3 .e2e-private/quality_judge.py \
    --live  refined.md \
    --gold  gold-standard.md
```

Output: per-dimension scores + delta winner + defect list + overall average + verdict line.

## Source

- `../scripts/refine.py` — embeds the judge for refinement
- `.e2e-private/quality_judge.py` — standalone (private)
- `.e2e-private/llm_judge.py` — standalone alternative (private)

## Related

- [[Quality Refinement Pipeline]]
- [[Best-of-N Sampling]] — Stage 2 selection mechanism
- [[Self-Refine]] — Stage 3 critique source
