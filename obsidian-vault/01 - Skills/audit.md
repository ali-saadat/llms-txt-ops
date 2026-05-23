---
title: audit
tags:
  - skill
  - review
aliases:
  - audit-skill
created: 2026-05-23
updated: 2026-05-23
---

# audit

> [!info] Reviews an existing llms.txt file against 17 anti-patterns + SEO-layer best practices

## When this fires

Triggers: "review my llms.txt", "audit our file", "what's wrong with my llms.txt", "is our llms.txt any good", or sharing a URL or pasted content.

## What it does (Step 3 in the skill)

### Mechanical checks (run first)

1. File size (under 50 KB target? 200 KB hard limit?)
2. Encoding (UTF-8 without BOM?)
3. Exactly one H1
4. `## Optional` section present (case-sensitive)
5. All URLs return 2xx (link-check)
6. Served `Content-Type: text/markdown; charset=utf-8`
7. Served `X-Robots-Tag: noindex`
8. robots.txt consistency with declared crawler policy

### Anti-pattern checks (17)

See [[Map of Content#Anti-patterns (17)|the full anti-pattern catalog]]. Each finding cites the anti-pattern number for traceability.

### SEO-layer checks (Stripe pattern)

- [ ] `## For AI Systems — Read This First` directives block
- [ ] Local-intent / "near me" directive
- [ ] `## SEO Routing` table
- [ ] `## SEO Priority Pages — Selection Hierarchy`
- [ ] `## Transactional Guidance` (commercial sites)
- [ ] `## Structured Data on [Site]`
- [ ] Intent router
- [ ] Entity facts block
- [ ] File metadata block

## Severity scale

| Marker | Examples |
|---|---|
| 🔴 Critical | Bloated enumeration, broken encoding, all URLs 4xx, description-content mismatch (cloaking) |
| 🟠 High | Marketing-speak throughout, no instructions block, robots.txt inconsistency |
| 🟡 Medium | Missing SEO routing layer, no last-reviewed metadata, 50-200 KB |
| 🟢 Low | Could use more concrete descriptions, URL pattern not declared for long-tail |

## Output

Severity-tagged markdown report citing anti-pattern numbers (`#1`, `#16`, `#17`, etc.) for every finding.

## Source

- `../skills/audit/SKILL.md`
- `../skills/audit/references/anti-patterns-detection.md`
- `../skills/audit/references/seo-layer-checks.md`

## Related

- [[generate]] — invoke `--from-audit` to apply Critical+High fixes
- [[customize]] — for surgical section updates
- [[Map of Content#Anti-patterns (17)]]
