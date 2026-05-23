# Security policy

## Supported versions

The latest minor release on `main` receives security fixes. Older versions do not.

## Reporting a vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead:

- Email the project owner directly via the GitHub-listed contact, or
- Use [GitHub's private vulnerability reporting](https://github.com/ali-saadat/llms-txt-ops/security/advisories/new)

Include:

1. Description of the vulnerability
2. Steps to reproduce
3. Affected version(s)
4. Suggested remediation (if known)

You can expect an acknowledgement within 7 days. Fixes typically ship within 30 days.

## Notes on the A2A server (`scripts/a2a-server.py`)

The Tier 2 server is built with security in mind:

- **Bearer-token authentication** via `A2A_API_KEYS` env-var (mandatory for production)
- **Per-caller rate limiting** (default 30 req/min, configurable)
- **Caller isolation** in `tasks/get` and `tasks/list`
- **Audit logging** to JSONL for every request and task completion
- **SQLite persistence** with per-caller ownership

If you operate the server publicly:

- Always set `A2A_API_KEYS` (the server logs a warning if unset)
- Terminate TLS at a reverse proxy (Caddyfile provided in `deploy/`)
- Set a reasonable per-caller `A2A_RATE_LIMIT`
- Ship `a2a-audit.log` to a centralized SIEM
- Rotate `ANTHROPIC_API_KEY` regularly

See [`A2A.md`](A2A.md) for the full security checklist.

## Notes on test data

The repository's `.e2e-private/` directory is gitignored. It is intended for private fixture files that should never be committed. Verify before pushing:

```bash
git status .e2e-private/   # should show nothing
```
