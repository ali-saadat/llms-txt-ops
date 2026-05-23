---
title: Versioning policy
tags:
  - meta
  - versioning
aliases:
  - semver policy
created: 2026-05-23
updated: 2026-05-23
---

# Versioning policy

> [!info] Semver: MAJOR.MINOR.PATCH

| Bump | Triggers |
|---|---|
| **Patch** (`x.y.PATCH`) | Description tweaks, eval additions, doc fixes — no skill-shape changes |
| **Minor** (`x.MINOR.0`) | New skills, sectors, languages, connectors; [[A2A Protocol|A2A]] tier upgrades; additive guardrails; eval/judge additions |
| **Major** (`MAJOR.0.0`) | Breaking changes to skill IDs, removed skills, manifest schema changes, **[[License model|license changes]]** |

## Mechanics

```bash
# Patch-bump only
python3 scripts/sync.py --version-bump

# Minor/Major — manually edit both:
#   .claude-plugin/plugin.json
#   .well-known/agent-card.json
```

## Source

- `../CHANGELOG.md`
- `../scripts/sync.py --version-bump`

## Related

- [[Version history]]
- [[License model]]
- [[Contributing]]
