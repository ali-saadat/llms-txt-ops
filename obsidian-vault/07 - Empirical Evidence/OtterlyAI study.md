---
title: OtterlyAI study
tags:
  - empirical
  - study
created: 2026-05-23
updated: 2026-05-23
study_year: 2025
sample_size: 90_days
---

# OtterlyAI study

> [!info] 90 days of AI crawler server logs
> Direct measurement of crawler behavior, not inferred from search results.

## Finding

AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) fetch whatever they want based on their own signals. The presence or absence of `llms.txt` did not change their crawl pattern.

## Why this matters

This is the only study that looks at the actual mechanism: do crawlers behave differently when llms.txt is present? Answer: no.

## Source

- `../knowledge/02-empirical-evidence.md` § OtterlyAI

## Related

- [[Empirical baseline]]
- [[SE Ranking study]]
- [[Search Engine Land study]]
- [[Map of Content#Empirical baseline]]
