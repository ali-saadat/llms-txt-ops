---
title: "02 robots.txt confusion"
tags:
  - anti-pattern
  - severity/high
aliases:
  - "Anti-pattern #2"
  - "#2 robots.txt confusion"
created: 2026-05-23
updated: 2026-05-23
severity: high
applies_to: [all]
---

# Anti-pattern #2 — robots.txt confusion

> [!warning] HIGH severity
> User-agent directives inside llms.txt — wrong file

## Where this most often hits

Sectors with elevated risk: _all sectors_

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #2 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
