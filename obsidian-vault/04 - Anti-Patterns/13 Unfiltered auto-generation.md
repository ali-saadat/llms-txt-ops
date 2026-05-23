---
title: "13 Unfiltered auto-generation"
tags:
  - anti-pattern
  - severity/critical
aliases:
  - "Anti-pattern #13"
  - "#13 Unfiltered auto-generation"
created: 2026-05-23
updated: 2026-05-23
severity: critical
applies_to: [marketplace,ecommerce]
---

# Anti-pattern #13 — Unfiltered auto-generation

> [!danger] CRITICAL severity
> sitemap.xml piped directly to llms.txt without curation

## Where this most often hits

Sectors with elevated risk: [[marketplace]], [[ecommerce]]

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #13 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
