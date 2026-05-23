---
title: deploy
tags:
  - skill
  - operations
aliases:
  - deployer
created: 2026-05-23
updated: 2026-05-23
---

# deploy

> [!info] Server config + CI validation
> Handles Nginx, Apache, Caddy, Vercel, Netlify, Cloudflare. Wires `templates/validate.sh` into your CI. **Only fires on qualified Jira phrasing** — see disambiguation note.

## When this fires

Triggers: "deploy to Nginx", "set up CI validation", "production deployment", "deployment Jira ticket", "CI ticket", "ops ticket".

> [!warning] Jira disambiguation
> Vanilla "write the Jira ticket" → [[stakeholder-comms]] (default).
> Qualified "deployment Jira" / "CI ticket" / "ops Jira" → deploy.

## What it produces

- Nginx/Apache/Caddy config snippets
- `validate.sh` integration into CI (GitHub Actions / GitLab CI / etc.)
- CDN purge strategy
- SHA-256 pinning instructions
- Headers: `Content-Type: text/markdown; charset=utf-8`, `X-Robots-Tag: noindex`, `Cache-Control: max-age=3600`

## Source

- `../skills/deploy/SKILL.md`
- `../skills/deploy/references/platform-configs.md`
- `../skills/deploy/references/ci-platforms.md`

## Related

- [[generate]] — produces the file deploy ships
- [[stakeholder-comms]] — Jira for the business side
- [[Cookbook - Staleness Watcher]] — post-deploy health check
- [[Map of Content#Skills (8)]]
