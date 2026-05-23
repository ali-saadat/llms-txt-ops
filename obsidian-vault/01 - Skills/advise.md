---
title: advise
tags:
  - skill
  - decision
  - router
aliases:
  - advisor
created: 2026-05-23
updated: 2026-05-23
---

# advise

> [!tip] Decision router + global ambiguity fallback
> Single-word inputs ("help", "fix", "update") route here for clarification, never to destructive skills.

## When this fires

- Decision questions: "should I ship llms.txt?", "what's the SOTA?", "is it worth it?"
- Bare verbs without targets: "update everything", "fix it"
- General education requests
- Single-word fallbacks

## What it does

1. Loads `../knowledge/04-decision-framework.md`
2. Cross-references the user's profile (site type, goal)
3. Applies the decision matrix
4. Cites [[Empirical baseline|the three studies]] explicitly
5. Routes to a specific destructive skill if the user's intent becomes clear

## Decision flow

```
Site type → SHIP / SKIP / CONDITIONAL
Goal      → SHIP / SKIP / SKIP-with-redirect-to-GEO
```

Sectors where SHIP is the default: [[dev-docs]], [[marketplace]], [[b2b-saas]] (docs subdomain only).

Sectors where SKIP is the default: most marketing, news, healthcare, fintech — see [[Map of Content#Sectors (18)]].

## Source

- `../skills/advise/SKILL.md`
- `../skills/advise/references/decision-tree-examples.md`

## Related

- [[Empirical baseline]] — what advice is grounded in
- [[Versioning policy]]
- [[Map of Content#Skills (8)]]
