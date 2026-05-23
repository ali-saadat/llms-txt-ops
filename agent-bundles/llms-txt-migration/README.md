# Agent Bundle: llms-txt-migration

**Use case**: A team with an existing llms.txt (often bloated / outdated) that needs auditing, fixing, re-generating, and re-deploying. Optimized for the "12 MB → 28 KB recovery" pattern.

This bundle vendors copies of these skills from the canonical `skills/` directory:

- `audit` — review the existing file, identify anti-patterns
- `customize` — targeted section updates
- `generate` — produce v2/v3 of the file (or `--from-audit` for audit-driven regeneration)
- `deploy` — re-deployment with CI validation
- `stakeholder-comms` — draft the "we're replacing the file because..." email

## Workflow

```
1. /llms-txt-migration:audit                 (assess current state, severity-tagged findings)
2. /llms-txt-migration:customize             (if minor — fix sections in place)
   OR
   /llms-txt-migration:generate --from-audit (if major — full regeneration)
3. /llms-txt-migration:deploy                (re-deploy with monitoring)
4. /llms-txt-migration:stakeholder-comms     (communicate the migration)
```

## Keeping in sync

Same as bootstrap bundle — vendored copies, sync via `scripts/sync.py --sync`.

## Pattern source

Adapted from `anthropics/financial-services` agent-plugins pattern.
