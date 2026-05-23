---
title: "10 Encoding errors"
tags:
  - anti-pattern
  - severity/critical
aliases:
  - "Anti-pattern #10"
  - "#10 Encoding errors"
created: 2026-05-23
updated: 2026-05-23
severity: critical
applies_to: [all]
---

# Anti-pattern #10 — Encoding errors

> [!danger] CRITICAL severity
> Non-UTF-8 or BOM present; served without charset

## Where this most often hits

Sectors with elevated risk: _all sectors_

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #10 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
