# Agent Bundle: llms-txt-bootstrap

**Use case**: A team starting from scratch with no existing llms.txt — they want orientation, configuration, file generation, and deployment guidance in one self-contained package.

This bundle vendors copies of these skills from the canonical `skills/` directory:

- `setup-recommender` — 2-minute orientation (which sector / language / connectors to use)
- `cold-start-interview` — full configuration walkthrough
- `generate` — create the llms.txt file from the practice profile
- `deploy` — production deployment guidance + CI validation

## Workflow

```
1. /llms-txt-bootstrap:setup-recommender     (60-second orientation)
2. /llms-txt-bootstrap:cold-start-interview  (2-20 min configuration)
3. /llms-txt-bootstrap:generate              (produce the file)
4. /llms-txt-bootstrap:deploy                (server config + CI)
```

## Keeping in sync

The skills in this bundle are **vendored copies**. To update:

1. Edit the source in `../../skills/<skill-name>/SKILL.md`
2. Run `python3 ../../scripts/sync.py --sync`
3. Verify with `python3 ../../scripts/sync.py --check` (should show "no drift")

CI hook in `.githooks/pre-commit` runs the drift check automatically.

## Pattern source

Adapted from `anthropics/financial-services` agent-plugins pattern — agents bundle their dependencies for self-contained installation.
