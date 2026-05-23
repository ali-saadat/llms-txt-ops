---
title: Deploy targets
tags:
  - architecture
  - deployment
aliases:
  - Deployments
  - Hosting
created: 2026-05-23
updated: 2026-05-23
---

# Deploy targets

> [!tip] One-click deploy ready
> Platform configs are at the repo root (Render/Fly/Railway each look there by default). Caddy + self-host configs in `../deploy/`.

## Supported platforms

| Platform | Config | Cost (May 2026) |
|---|---|---|
| Local Docker | `../docker-compose.yml` | Free (your hardware) |
| Render | `../render.yaml` | Free tier sleeps; $7/mo always-on |
| Fly.io | `../fly.toml` | ~$2/mo shared-CPU always-on |
| Railway | `../railway.json` | $5/mo trial → usage-based |
| AWS App Runner / GCP Cloud Run | uses `../Dockerfile` directly | Per-request |
| Self-hosted Docker + Caddy TLS | `../deploy/Caddyfile` | Hardware only |

## Not supported

| Platform | Why |
|---|---|
| Vercel | Serverless; [[A2A Tier 2 - Server]] is stateful (SQLite) + uses SSE |
| Cloudflare Workers | Same — stateful + SSE incompatible |

## Required secrets after deploy

| Variable | When | Notes |
|---|---|---|
| `A2A_MODE` | switch from mock | set to `live` for real Claude calls |
| `ANTHROPIC_API_KEY` | live mode | required |
| `A2A_API_KEYS` | production | ALWAYS set — otherwise public endpoint = denial-of-wallet bait |
| `A2A_MAX_TOKENS` | optional | global default; per-skill table also applies |

## Source

- `../deploy/README.md` — deploy guide
- Platform configs at repo root

## Related

- [[A2A Tier 2 - Server]] — what gets deployed
- [[Integrations]] — how to call after deploy
