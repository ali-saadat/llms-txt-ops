---
title: Language router
tags:
  - language
  - architecture
aliases:
  - languages router
  - end-user language policy
created: 2026-05-23
updated: 2026-05-23
---

# Language router

> [!important] End-user-driven policy
> The plugin asks the user what language they want. It does NOT auto-detect aggressively.

## Three axes, three defaults

| Axis | Default | Override |
|---|---|---|
| **llms.txt file content** | English | User explicit request, profile preference |
| **Stakeholder communication** | Match user's typing language | User explicit request |
| **Conversation tone** (Claude's responses) | Match user's typing language | User explicit request |
| **Templates & references** (plugin internals) | English | n/a — internal docs stay English |

## Why English is the default for file content

- LLM crawlers process English best
- English is the universal default for technical web standards (robots.txt, sitemap.xml, JSON-LD)
- Multilingual sites typically include a bilingual summary blockquote rather than translating the whole file

## Source

- `../knowledge/languages/_router.md`

## Related

- [[Map of Content#Languages (13)]]
- [[cold-start-interview]] — asks 4 language questions during setup
- [[stakeholder-comms]]
