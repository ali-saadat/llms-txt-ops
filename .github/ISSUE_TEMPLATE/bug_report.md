---
name: Bug report
about: Something is broken or behaving unexpectedly
title: '[bug] '
labels: bug
---

## What happened

Describe the unexpected behavior.

## What you expected

What did you expect to happen instead?

## To reproduce

Steps to reproduce the behavior:

1. Run `...`
2. See error / unexpected output

## Environment

- Plugin version: (run `cat .claude-plugin/plugin.json | grep version`)
- Claude Code version: (run `claude --version`)
- OS: (macOS / Linux / Windows + version)
- Python version: (`python3 --version`)
- Mode: mock / live

## Validation output

If applicable, paste the output of:

```
python3 scripts/check.py
python3 scripts/sync.py --check
python3 -m pytest tests/ -v
```

## Additional context

Anything else relevant.
