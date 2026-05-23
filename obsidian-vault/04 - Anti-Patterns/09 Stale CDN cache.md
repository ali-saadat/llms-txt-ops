---
title: "09 Stale CDN cache"
tags:
  - anti-pattern
  - severity/high
aliases:
  - "Anti-pattern #9"
  - "#9 Stale CDN cache"
created: 2026-05-23
updated: 2026-05-23
severity: high
applies_to: [all]
---

# Anti-pattern #9 — Stale CDN cache

> [!warning] HIGH severity
> Local SHA-256 ≠ served URL SHA-256

## Where this most often hits

Sectors with elevated risk: _all sectors_

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #9 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
