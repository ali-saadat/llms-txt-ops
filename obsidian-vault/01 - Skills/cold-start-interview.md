---
title: cold-start-interview
tags:
  - skill
  - configuration
aliases:
  - cold-start
  - interview
created: 2026-05-23
updated: 2026-05-23
---

# cold-start-interview

> [!important] The only skill that writes the practice profile
> Other skills [[Map of Content|bounce here]] if `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` has placeholder markers.

## When this fires

Triggers: "configure my profile", "set up my profile", "interview me", "start fresh", "redo from scratch", "reset my profile", "forget everything and start over", `--quick` for the 2-minute path.

## Two modes

- **Full** (15-20 min): walks every section of the profile template
- **`--quick`** (2 min): only the must-haves (site name, type, primary language, goal)

## What it writes

`~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` — the practice profile that every other skill reads. Template lives at `../CLAUDE.md`.

## Language policy captured

End-user-driven (see [[Language router]]):

- File content default: English
- Stakeholder comms: user's typing language
- Conversation tone: user's typing language

## Source

- `../skills/cold-start-interview/SKILL.md`
- `../skills/cold-start-interview/references/sector-question-banks.md`
- `../skills/cold-start-interview/references/honest-expectations-script.md`

## Related

- [[setup-recommender]] — orientation that routes here
- [[advise]] — recommended skill to invoke after setup
- [[Map of Content#Skills (8)]]
