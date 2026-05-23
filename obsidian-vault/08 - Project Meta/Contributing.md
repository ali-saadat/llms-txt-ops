---
title: Contributing
tags:
  - meta
  - contributing
created: 2026-05-23
updated: 2026-05-23
---

# Contributing

> [!important] By submitting a PR you agree to the dual-license model
> Your contribution can be made available under both PolyForm Noncommercial (public repo) AND any commercial license the maintainer grants. See [[License model]].

## Pre-commit hook

```bash
git config core.hooksPath .githooks
```

Auto-runs `check.py + sync.py --check` on every commit.

## Validation chain

```bash
python3 scripts/check.py            # 42 PASS, 0 WARN, 0 FAIL
python3 scripts/sync.py --check     # no drift between skills/ and agent-bundles/*/skills/
python3 -m pytest tests/ -q         # 42 cases
bash scripts/deploy-managed-agent.sh staleness-watcher  # cookbook dry-run
```

## How to add a sector / language / skill

See `../CONTRIBUTING.md` § "Adding a sector" / "Adding a language" / "Adding a skill".

## Source

- `../CONTRIBUTING.md`
- `../.githooks/pre-commit`

## Related

- [[License model]]
- [[Versioning policy]]
- [[Version history]]
