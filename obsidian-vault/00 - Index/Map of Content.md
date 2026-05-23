---
title: Map of Content
tags:
  - moc
aliases:
  - MOC
created: 2026-05-23
updated: 2026-05-23
---

# Map of Content

> [!tip] How to use this map
> Every note in this vault is reachable from here. Click any wikilink to jump.

---

## Skills (8)

User-invocable via `/llms-txt-advisor:<skill>` in Claude Code.

| Skill | Trigger | Output |
|---|---|---|
| [[setup-recommender]] | "I just installed this" | Orientation (60s) |
| [[cold-start-interview]] | "Set up my profile" | Practice profile written |
| [[advise]] | "Should I ship?" | Decision verdict |
| [[audit]] | "Review my file" | Severity-tagged findings |
| [[generate]] | "Create new file" | Production llms.txt |
| [[customize]] | "Update section X" | Surgical edit |
| [[deploy]] | "Server config" | Nginx/CI/validate.sh |
| [[stakeholder-comms]] | "Draft email" | Email or Jira ticket |

`#skill`

---

## Anti-patterns (17)

The plugin's [[audit]] skill checks against these.

- [[01 Bloated enumeration]] — 12 MB / 40k+ URLs
- [[02 robots.txt confusion]] — User-agent inside llms.txt
- [[03 Marketing-speak descriptions]] — Revolutionize / cutting-edge
- [[04 Listing everything]] — No curation
- [[05 Legal document mode]] — DMCA boilerplate
- [[06 Cloaking-style mismatch]] — Description ≠ page
- [[07 Broken URLs]] — 4xx/5xx links
- [[08 Forgetting to regenerate]] — Stale metadata
- [[09 Stale CDN cache]] — Local SHA ≠ served SHA
- [[10 Encoding errors]] — non-UTF-8 / BOM
- [[11 Indexing the file itself]] — No noindex header
- [[12 No CI validation]] — Manual ship workflow
- [[13 Unfiltered auto-generation]] — Sitemap → llms.txt verbatim
- [[14 Vendor lock]] — Platform-generated, no backup
- [[15 Over-promising to stakeholders]] — "AI traffic" promises
- [[16 PII leakage in enumeration]] — Inline phone numbers
- [[17 Non-markdown file format]] — RTF/HTML/PDF

`#anti-pattern`

---

## Sectors (18)

> [!note] Composition router
> A single site can be product-domain × delivery-channel (e.g., legal-tech B2B SaaS = [[legal-services]] product × [[b2b-saas]] channel). The [[sector router]] handles composition.

### Strongest ship rationale

- [[dev-docs]] — coding agents read it; real users
- [[marketplace]] — replaces bloated existing files
- [[b2b-saas]] — docs subdomain only

### Default skip (with override conditions)

- [[ecommerce]] · [[marketing]] · [[news-publisher]] · [[education]] · [[healthcare]] · [[fintech]] · [[government-civic]] · [[gaming]] · [[non-profit]] · [[media-entertainment]]

### Specialty verticals

- [[legal-services]] · [[real-estate]] · [[hospitality]] · [[automotive]]

### Fallback

- [[generic]]

`#sector`

---

## Languages (13)

End-user-driven: llms.txt content = English by default; conversation tone + stakeholder comm = match user's typing language.

- [[English]] · [[Turkish]] · [[Spanish]] · [[German]] · [[French]] · [[Japanese]] · [[Mandarin Chinese]] · [[Arabic]] · [[Portuguese]] · [[Italian]] · [[Dutch]] · [[Korean]] · [[Russian]]

`#language`

---

## Architecture

- [[Architecture]] — system map
- [[A2A Protocol]]
  - [[A2A Tier 1 - Agent Card]]
  - [[A2A Tier 2 - Server]]
  - [[A2A Tier 3 - Client]]
- [[Cookbook - Staleness Watcher]] — managed-agent (3-tier security)
- [[Deploy targets]] — Docker · Render · Fly · Railway
- [[Integrations]] — n8n · LangGraph · CrewAI · Python · curl

`#architecture`

---

## Quality refinement (SOTA, May 2026)

- [[Quality Refinement Pipeline]] — orchestrator
- [[Best-of-N Sampling]] — Stage 1
- [[LLM Judge]] — Stage 2 + 5
- [[Self-Refine]] — Stage 3 (Madaan 2023, +20%)
- [[Post-Processors]] — Stage 4 (deterministic)

`#quality`

---

## Empirical baseline

- [[Empirical baseline]] — the honest stance
- [[SE Ranking study]] — n=300k
- [[OtterlyAI study]] — 90-day server logs
- [[Search Engine Land study]] — 10-site controlled test

`#empirical`

---

## Project meta

- [[Version history]]
- [[License model]] — dual-license
- [[Versioning policy]]
- [[Contributing]]
- [[Glossary]]

`#meta`
