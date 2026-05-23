---
title: generate
tags:
  - skill
  - creation
aliases:
  - generator
  - generate-skill
created: 2026-05-23
updated: 2026-05-23
---

# generate

> [!important] 2-pass with completeness validation
> v1.4.0+ enforces Pass 1 (outline + URL inventory) → Pass 2 (render) → Step 5 (completeness validation). Closes under-generation gaps that single-pass produces.

## When this fires

Triggers: "create our llms.txt", "generate llms.txt", "make me an llms.txt", "draft a file for us", "build the llms.txt", "produce the llms.txt", `--from-audit` after [[audit]].

## The OUTPUT BOUNDARY rule

> [!warning] Critical: process scaffolding must NOT leak into the file
> Pass 1 inventory and Step 5 validation are INTERNAL to your reasoning. The file the user sees starts with the H1 and ends with `## Optional`. **No `## Step N`, `## Pass N`, `## URL Inventory`, `## Quality Self-Audit`, or `## Validation Checklist` headings appear in the output.**

## Pass structure

### Pass 1 — Section outline + URL inventory (internal)

YAML-shaped inventory enumerating every required section and every URL that will appear. Catches under-generation before it happens.

### Pass 2 — Render in 16-section canonical order

1. H1 + bilingual blockquote
2. `## For AI Systems — Read This First`
3. `## SEO Routing` (commercial sites)
4. `## SEO Priority Pages — Selection Hierarchy`
5. `## Transactional Guidance` (commercial sites)
6. `## Structured Data on [Site]`
7. `## How to Find the Right Page (Intent Router)`
8. `## About [Site] (Entity Facts)` — bullets, not prose
9. `## Free Planning Tools` (with SPA caveat if applicable)
10. Per-category sections (one per top-level category family)
11. `## Geographic Coverage` — top-12 metros + URL pattern
12. `## Editorial — Canonical Internal Sources`
13. `## Inspiration and Galleries`
14. `## International Sister Platforms`
15. `## Machine-Readable Sources`
16. `## Optional`

### Step 5 — Completeness + quality self-audit (internal)

Measurable thresholds: URL count ≥80 for marketplaces, entity facts as bulleted list, every editorial article rendered, file size 20-50 KB.

## No-fabrication guardrails

> [!danger] These prevented multiple rounds of slug-substitution defects
> - **Never fabricate URLs.** Every URL traces to (a) a literal URL in the profile, (b) a brand page declared in the profile, or (c) a URL constructed via the explicit URL pattern declared in the file.
> - **Never invent editorial articles.** If profile lists 11, output exactly 11.
> - **Never include placeholder values** (`<pending>`, `<TBD>`, `[REVIEW]`, `SHA-256: <...>`).
> - **Never enumerate category × city** — that's [[01 Bloated enumeration|anti-pattern #1]].

## Source

- `../skills/generate/SKILL.md` (367 lines)
- `../skills/generate/references/template-assembly.md`

## Related

- [[audit]] — invoke `--from-audit` to generate fixes
- [[customize]] — for section-level changes
- [[deploy]] — next step after generation
- [[Quality Refinement Pipeline]] — push to 9.5+ via refine.py
- [[Map of Content#Skills (8)]]
