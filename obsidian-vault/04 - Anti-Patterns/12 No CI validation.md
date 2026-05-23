---
title: "12 No CI validation"
tags:
  - anti-pattern
  - severity/medium
aliases:
  - "Anti-pattern #12"
  - "#12 No CI validation"
created: 2026-05-23
updated: 2026-05-23
severity: medium
applies_to: [all]
---

# Anti-pattern #12 — No CI validation

> [!note] MEDIUM severity
> Manual deploy without validate.sh in the pipeline

## Where this most often hits

Sectors with elevated risk: _all sectors_

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #12 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
