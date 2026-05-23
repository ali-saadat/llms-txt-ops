---
title: "16 PII leakage in enumeration"
tags:
  - anti-pattern
  - severity/critical
aliases:
  - "Anti-pattern #16"
  - "#16 PII leakage in enumeration"
created: 2026-05-23
updated: 2026-05-23
severity: critical
applies_to: [marketplace]
---

# Anti-pattern #16 — PII leakage in enumeration

> [!danger] CRITICAL severity
> Phone numbers, emails, addresses inline next to vendor URLs

## Where this most often hits

Sectors with elevated risk: [[marketplace]]

## How [[audit]] detects it

See `../knowledge/07-failure-modes.md` — anti-pattern #16 for the full detection signal, why it's harmful, and the fix.

## Related

- [[audit]] — the skill that detects this
- [[generate]] — must produce output that avoids this
- [[Map of Content#Anti-patterns (17)]]
