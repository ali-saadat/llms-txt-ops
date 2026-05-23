---
title: setup-recommender
tags:
  - skill
  - orientation
aliases:
  - setup
  - recommender
created: 2026-05-23
updated: 2026-05-23
---

# setup-recommender

> [!info] 60-second orientation skill
> The lightest-weight skill. Asks 2 questions, points you at the right next skill, writes nothing. Safe to invoke when you don't know what to do.

## When this fires

Triggers: "I just installed this plugin", "first time using this", "where do I start", "give me the 60-second version".

## What it does

1. Asks: are you brand new to llms.txt, or do you already have a file?
2. Routes to either [[cold-start-interview]] (if configuring) or [[advise]] (if curious)
3. Never bounces to destructive skills

## Source

- `../skills/setup-recommender/SKILL.md`
- `../skills/setup-recommender/references/role-based-workflows.md`

## Related skills

- [[cold-start-interview]] — the next step if you commit to setup
- [[advise]] — the next step if you want decision help only
- [[Map of Content#Skills (8)]]
