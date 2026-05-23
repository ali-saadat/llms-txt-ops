---
title: "11 Indexing the file itself"
tags:
  - anti-pattern
  - severity/high
aliases:
  - "Anti-pattern #11"
  - "#11 Indexing the file itself"
created: 2026-05-23
updated: 2026-05-23
severity: high
applies_to: [all]
---

# Anti-pattern #11 — Indexing the file itself

> [!warning] HIGH severity
> No X-Robots-Tag: noindex header on served file

## Where this most often hits

Sectors with elevated risk: _all sectors_

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #11 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
