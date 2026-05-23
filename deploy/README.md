# Deploy configs

One-click deploy templates for the llms-txt-advisor A2A server. Each platform's config sits in this directory; the README in the repo root has clickable deploy buttons.

| Platform | Config file | One-click button |
|---|---|---|
| Render | [`render.yaml`](render.yaml) | https://render.com/deploy?repo=<fork-url> |
| Fly.io | [`fly.toml`](fly.toml) | `fly launch --copy-config --no-deploy && fly deploy` |
| Railway | [`railway.json`](railway.json) | https://railway.app/new/template?template=<fork-url> |
| Docker | [`../Dockerfile`](../Dockerfile) | `docker build -t llms-txt-advisor . && docker run -p 8000:8000 llms-txt-advisor` |
| Docker Compose | [`../docker-compose.yml`](../docker-compose.yml) | `docker compose up` |
| Vercel | not supported | Vercel is serverless; the A2A server is stateful (SQLite) and uses SSE. Use Render/Fly/Railway for stateful workloads. |
| Cloudflare Workers | not supported | Same reason — stateful + SSE. (Could be adapted to Cloudflare Containers if/when needed.) |
| AWS App Runner / Cloud Run | works with `Dockerfile` directly | Point at the repo, App Runner / Cloud Run auto-builds the Dockerfile |

## Required secrets after deploy

Every platform deploys in **mock mode by default** (no API key needed — produces canned but skill-aware responses).

To enable **live mode** (real Claude calls):

| Variable | Value | Notes |
|---|---|---|
| `A2A_MODE` | `live` | Switches from mock to real Claude calls |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Required for live mode |
| `A2A_API_KEYS` | `caller1=$(openssl rand -hex 32),caller2=...` | Bearer-token allowlist. **Always set in production** — otherwise the endpoint is open to anyone. |

## TLS

All three managed platforms (Render, Fly, Railway) provision TLS automatically on the platform-assigned hostname. For your own domain:

- **Render**: dashboard → Settings → Custom Domains
- **Fly.io**: `fly certs add a2a.yourcompany.com`
- **Railway**: dashboard → Settings → Networking → Generate Domain → Add Custom Domain

For self-hosted Docker deploy, the included [`Caddyfile`](Caddyfile) terminates TLS via Let's Encrypt — uncomment the `caddy` service in `docker-compose.yml`.

## What gets deployed

The `Dockerfile` (root) builds a minimal Python 3.13 image containing:

- `scripts/a2a-server.py` — the FastAPI server
- `scripts/a2a-client.py` — for in-container debugging
- `.well-known/agent-card.json` — Tier 1 discovery
- `skills/` — for live mode (system prompts)
- Pinned dependencies from `requirements.txt`

Other repo contents (knowledge corpus, evals, agent bundles, etc.) are excluded via `.dockerignore` to keep the image small.

## Costs (May 2026)

| Platform | Free tier | Smallest paid |
|---|---|---|
| Render | 750 hrs/mo + sleeps after 15 min idle | $7/mo always-on |
| Fly.io | 3 shared-cpu-1x machines + 3GB storage free | ~$2/mo per machine when not using free tier |
| Railway | $5/mo trial credit | Usage-based; ~$5–10/mo for low-traffic |
| Docker Compose | Free (your hardware) | n/a |

For most use cases — the A2A server idles when not in use and only runs the Claude API call when called — the cheapest option is **Fly.io's always-on shared CPU at ~$2/mo** + the per-call Claude API cost.
