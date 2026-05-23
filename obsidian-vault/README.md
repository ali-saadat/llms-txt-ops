---
title: llms-txt-ops Obsidian Vault
tags:
  - moc
  - dashboard
aliases:
  - Vault Home
created: 2026-05-23
updated: 2026-05-23
---

# llms-txt-ops — Obsidian Vault

> [!info] What this vault is
> A wikilink-navigated knowledge base for the [llms-txt-ops](https://github.com/ali-saadat/llms-txt-ops) project. Notes here cross-reference the source markdown under `../knowledge/`, `../skills/`, etc. — no duplicate content; pure navigation + synthesis.

> [!tip] Start here
> Open [[Map of Content]] for the top-level navigation. Or pick a thread:
> - **"What does this project do?"** → [[Architecture]]
> - **"What are the 8 skills?"** → [[Map of Content#Skills (8)]]
> - **"How does it score against gold?"** → [[Quality Refinement Pipeline]]
> - **"What's the licensing story?"** → [[License model]]

---

## Project at a glance

- **Repo**: [github.com/ali-saadat/llms-txt-ops](https://github.com/ali-saadat/llms-txt-ops) (public)
- **Current version**: `2.0.0`
- **License**: [[License model|PolyForm Noncommercial 1.0.0]] (commercial use requires paid license)
- **Source-of-truth notes**: live in `../knowledge/01..09-*.md` (this vault links to them)

## Quick stats

| Aspect | Count | Note |
|---|---|---|
| User-invocable skills | 8 | the [[Map of Content#Skills (8)|Skills section]] |
| Documented anti-patterns | 17 | the [[Map of Content#Anti-patterns (17)|Anti-patterns section]] |
| Sectors | 18 | the [[Map of Content#Sectors (18)|Sectors section]] |
| Languages | 13 | the [[Map of Content#Languages (13)|Languages section]] |
| A2A tiers implemented | 3 | [[A2A Protocol]] |
| Pytest cases | 42 | passing in ~1s |
| Trigger evals | 94 prompts | 100% pass |
| Gold-parity score | 9.4 / 10 | [[Quality Refinement Pipeline]] |

## Frequently-visited

- [[Map of Content]]
- [[Architecture]]
- [[A2A Protocol]]
- [[Quality Refinement Pipeline]]
- [[Empirical baseline]]
- [[License model]]
- [[Glossary]]

## Source files (outside the vault)

These live in the parent repo and are referenced via wikilinks from inside the vault:

- `../README.md` — repo entry point
- `../USER_GUIDE.md` — non-technical walkthrough
- `../INTEGRATIONS.md` — how-to-call-this-from-X
- `../A2A.md` — protocol guide
- `../CHANGELOG.md` — version log
- `../knowledge/01..09-*.md` — knowledge corpus
- `../skills/*/SKILL.md` — skill prompts

%% Vault built with the `obsidian:obsidian-markdown` skill. Convention: every cross-vault wikilink uses shortest-form names. External URLs use standard markdown links. Frontmatter properties are: title, tags, aliases, created, updated. %%
