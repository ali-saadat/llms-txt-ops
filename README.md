# llms-txt-advisor

**A Claude plugin that helps your website decide whether to ship an `llms.txt` file — and if yes, builds it, deploys it, and drafts the team email.** Now callable from anywhere via A2A v1.0.

[![Status](https://img.shields.io/badge/validation-100%25-brightgreen)]() [![Tests](https://img.shields.io/badge/tests-42%20passing-brightgreen)]() [![Gold parity](https://img.shields.io/badge/gold--parity-10%2F10-brightgreen)]() [![A2A](https://img.shields.io/badge/A2A-v1.0%20Tier%201%2B2%2B3-blue)]() [![Docker](https://img.shields.io/badge/docker-ready-blue)]() [![License](https://img.shields.io/badge/license-MIT-blue)]() [![Version](https://img.shields.io/badge/version-1.4.0-green)]() [![Anti-patterns](https://img.shields.io/badge/anti--patterns-17-orange)]()

---

## One-click deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy) [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template) [![Deploy to Fly.io](https://img.shields.io/badge/fly.io-deploy-purple)](https://fly.io/launch)

Or run locally:

```bash
docker compose up                                # mock mode, no API key
# or
docker run -p 8000:8000 llms-txt-advisor:1.4.0   # same
```

Then call it from anywhere: see [`INTEGRATIONS.md`](INTEGRATIONS.md) for n8n, LangGraph, CrewAI, Python, curl, and raw HTTP examples.

---

## Pick your guide

- 🧑‍💼 **Non-technical?** Read [`USER_GUIDE.md`](USER_GUIDE.md) — plain-English step-by-step, no jargon, includes "should I bother with this at all?" guidance.
- 👨‍💻 **Developer / SEO engineer?** Keep reading this README.
- 🔌 **Want to call this from n8n / LangGraph / CrewAI / your stack?** See [`INTEGRATIONS.md`](INTEGRATIONS.md).
- 🚀 **Deploying it permanently?** See [`deploy/README.md`](deploy/README.md) — one-click for Render, Fly.io, Railway, or self-hosted Docker.
- 🤖 **Building agents that call this one?** See [`A2A.md`](A2A.md) — Agent-to-Agent protocol guide.
- 🧭 **Just want a map of the repo?** See [`INDEX.md`](INDEX.md).

---

## What this is (one paragraph)

A [Claude Code](https://claude.com/claude-code) plugin (8 skills, 18 sectors, 13 languages) that:
1. Tells your team **honestly** whether shipping an `llms.txt` file will help them — most of the time it won't.
2. When it does help (dev docs, internal grounding, replacing broken files), generates the file, audits it for 15 documented anti-patterns, and produces deployment + stakeholder artifacts.
3. Comes with A2A v1.0 support so other AI agents can call into this advisor.

Grounded in three independent empirical studies. Refuses to over-promise. Plain text in, well-formed file + Nginx config + team email out.

## TL;DR — Install and use

```bash
# Install
/plugin marketplace add https://github.com/ali-saadat/llms-txt-ops
/plugin install llms-txt-advisor

# First time? Get oriented in 60 seconds
/llms-txt-advisor:setup-recommender

# Configure for your specific site (15–20 minutes)
/llms-txt-advisor:cold-start-interview

# Then use any skill
/llms-txt-advisor:advise              # "Should I ship an llms.txt?"
/llms-txt-advisor:audit               # Review my existing file
/llms-txt-advisor:generate            # Create a new file
/llms-txt-advisor:customize           # Update a section
/llms-txt-advisor:deploy              # Server config + CI validation
/llms-txt-advisor:stakeholder-comms   # Draft email or Jira ticket
```

---

## For non-technical users — read this section

### What does this plugin actually do for me?

**If you're an SEO lead, product manager, or business owner**, here's the bottom line:

| Your situation | What this plugin tells you |
|---|---|
| "My CEO read an article about llms.txt — should we add it?" | Probably no. Here's how to explain why with evidence. |
| "We already have an llms.txt — is it any good?" | Audits it against 15 documented failure modes; flags Critical/High issues. |
| "We're building developer docs" | Yes ship it. Here's the template, the file, the deploy. |
| "We have a 12MB bloated llms.txt that auto-generated itself" | Replace it. Here's a curated 28KB version that preserves coverage. |
| "We need to explain this decision to leadership" | Drafts the email in your language, with the right framing. |

### The honest baseline

Three independent studies all show: shipping an `llms.txt` file does **not** measurably increase AI citations or AI-driven traffic. Period.

- SE Ranking study: 300,000 domains, no correlation between llms.txt presence and AI visibility
- OtterlyAI study: 90 days of server logs, AI crawlers ignore llms.txt
- Search Engine Land study: 10 sites tested, no measurable lift

This plugin is built on that evidence. It will not promise something the data doesn't support.

### Where llms.txt *does* help

- **Developer documentation**: coding agents (Cursor, Claude Code, Cline, Aider) read it and give better answers to your devs
- **Internal RAG/chatbot grounding**: your own AI features benefit from the curated content map
- **Replacing a broken file**: if you already have a bloated/wrong llms.txt, replacing it is strictly better than the status quo

If your situation isn't on that list, the plugin will tell you so and redirect you to the things that actually work (schema.org, original research, author bylines, etc.).

### Step by step for non-technical users

Full walkthrough with screenshots-style narration: see [`USER_GUIDE.md`](USER_GUIDE.md).

---

## Use it from anywhere — not just Claude Code

This plugin has two faces:

1. **Inside Claude Code** — install via `/plugin install llms-txt-advisor` and use the slash commands.
2. **Outside Claude Code** — run the included A2A v1.0 server and call it from any language, framework, or no-code tool.

| Where you want to use it | What to do | Pointer |
|---|---|---|
| Inside Claude Code | `/plugin install llms-txt-advisor` | [TL;DR section below](#tldr--install-and-use) |
| Local Docker | `docker compose up` | [`docker-compose.yml`](docker-compose.yml) |
| Render / Fly / Railway (one-click hosted) | Click a deploy button above | [`deploy/README.md`](deploy/README.md) |
| n8n / Zapier / Make.com / any no-code | Import [`integrations/n8n/workflow-llms-txt-audit.json`](integrations/n8n/workflow-llms-txt-audit.json) | [`integrations/n8n/README.md`](integrations/n8n/README.md) |
| LangGraph | Tool wrapper pattern | [`integrations/langgraph/example.py`](integrations/langgraph/example.py) |
| CrewAI | `BaseTool` subclass pattern | [`integrations/crewai/example.py`](integrations/crewai/example.py) |
| Python (raw or wrapped) | Two patterns | [`integrations/python/example.py`](integrations/python/example.py) |
| curl / Node / Go / anything HTTP | Standard JSON-RPC 2.0 | [`integrations/raw-http/curl-examples.sh`](integrations/raw-http/curl-examples.sh) |
| Another A2A v1.0 agent | Standard A2A — point at our Agent Card | [`A2A.md`](A2A.md) |

**Full integration master guide**: [`INTEGRATIONS.md`](INTEGRATIONS.md).

---

## For technical users — install, develop, deploy

### Install (Claude Code plugin)

```bash
# Discover via marketplace
/plugin marketplace add https://github.com/ali-saadat/llms-txt-ops

# Install the main plugin (or one of the agent bundles)
/plugin install llms-txt-advisor

# Or:
/plugin install llms-txt-bootstrap   # For new sites (4 skills)
/plugin install llms-txt-migration   # For sites with existing files (5 skills)
```

### Skill list

| Skill | What it does |
|---|---|
| `setup-recommender` | Orientation — figures out which skill you want |
| `cold-start-interview` | Configures the practice profile (15–20 min full, 2 min quick) |
| `advise` | Decision questions + disambiguation router |
| `audit` | Review existing llms.txt against 15 anti-patterns |
| `generate` | Create new file from curated templates |
| `customize` | Surgical section updates |
| `deploy` | Server config (Nginx/Apache/Caddy/Vercel/Netlify/Cloudflare) + CI validation |
| `stakeholder-comms` | Drafts emails / Jira tickets in 13 languages |

### Repo layout

```
llms-txt-ops/
├── README.md                  # This file (you are here)
├── USER_GUIDE.md              # Non-technical step-by-step
├── INDEX.md                   # Full doc navigation
├── CHANGELOG.md               # Release history
├── CONTRIBUTING.md            # How to add sectors / languages / skills
├── A2A.md                     # Agent-to-Agent protocol guide
├── CONNECTORS.md              # MCP connector category reference
├── CLAUDE.md                  # Practice profile template
├── MEMORY.md                  # Project memory (for future Claude sessions)
├── LICENSE                    # MIT
├── VALIDATION_REPORT.md       # 100% validation results
├── pytest.ini                 # Pytest config (asyncio mode)
├── .claude-plugin/            # Plugin manifest + marketplace
├── .well-known/               # A2A Agent Card (Tier 1)
├── .mcp.json                  # MCP connector slots (13 categories)
├── .githooks/                 # Pre-commit hook
├── skills/                    # 8 user-invokable skills (source of truth)
├── knowledge/                 # Empirical evidence, sectors, languages, deep refs
├── agent-bundles/             # 2 themed plugin bundles (sync'd from skills/)
├── managed-agent-cookbooks/   # 1 cookbook (staleness-watcher, 3-tier security)
├── case-study/                # Worked example (anonymized marketplace)
├── stakeholder/               # Email templates + framing language
├── templates/                 # Starter llms.txt files + validate.sh
├── reference/                 # AI-bot user-agents and other lookup tables
├── evals/                     # 8 evals.json (61 prompts) + workflow docs
├── scripts/                   # check.py, sync.py, deploy + a2a-server + a2a-client
└── tests/                     # 42 pytest tests covering A2A Tier 2 + 3
```

### Quick validation (1 command each)

```bash
# Structural validation — must pass before any commit
python3 scripts/check.py
# → 42 PASS, 0 WARN, 0 FAIL

# Skill copy drift between skills/ and agent-bundles/*/skills/
python3 scripts/sync.py --check
# → PASS: no drift detected

# A2A test suite (Tier 2 server + Tier 3 client + loopback)
python3 -m pytest tests/ -v
# → 42 passed in ~1 second

# Cookbook deploy validation (dry-run, no API call)
bash scripts/deploy-managed-agent.sh staleness-watcher
# → PASS: Cookbook staleness-watcher validation complete
```

Pre-commit hook at `.githooks/pre-commit` runs check.py + sync.py automatically — enable with:

```bash
git config core.hooksPath .githooks
```

### A2A (Agent-to-Agent) support

All three A2A v1.0 tiers are fully implemented:

| Tier | Status | Where |
|---|---|---|
| Tier 1 — Discovery (Agent Card) | ✅ Live | `.well-known/agent-card.json` |
| Tier 2 — Server endpoint (JSON-RPC + SSE) | ✅ Implemented | `scripts/a2a-server.py` |
| Tier 3 — Client (call other A2A agents) | ✅ Implemented | `scripts/a2a-client.py` |

Quickstart (Python directly):

```bash
# Run the server in mock mode (no API key needed)
python3 scripts/a2a-server.py --port 8000

# From another terminal, talk to it
python3 scripts/a2a-client.py http://localhost:8000 discover
python3 scripts/a2a-client.py http://localhost:8000 send --skill advise --text "..."
python3 scripts/a2a-client.py http://localhost:8000 stream --skill audit --text "..."
```

Or via Docker:

```bash
docker compose up                                # all defaults
docker run -p 8000:8000 llms-txt-advisor:1.4.0   # one-liner
```

Full guide (protocol details, auth, security, testing matrix): **[`A2A.md`](A2A.md)**.
Hosted-deploy guide (Render, Fly, Railway, self-hosted Docker): **[`deploy/README.md`](deploy/README.md)**.
Integration patterns from non-Claude environments: **[`INTEGRATIONS.md`](INTEGRATIONS.md)**.

### Managed-agent cookbook deployment

```bash
# Dry-run (no API call)
bash scripts/deploy-managed-agent.sh staleness-watcher

# Live deploy (requires ANTHROPIC_API_KEY + per-MCP env-vars)
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_MCP_URL=https://...
export BING_WEBMASTER_MCP_URL=https://...
export PROFOUND_MCP_URL=https://...
bash scripts/deploy-managed-agent.sh staleness-watcher --live
```

The cookbook implements a **3-tier security split** following the [`anthropics/financial-services`](https://github.com/anthropics/financial-services) pattern:

- **Tier 1 — crawler** (touches untrusted HTML): no MCP, no Write, only Read/Grep/Bash
- **Tier 2 — analyzer** (trusted MCP only): GitHub, Bing AI Performance, Profound; no Write
- **Tier 3 — report-writer**: only Write capability, constrained to `./out/<domain>/`

### Status — 100% across every validation layer

| Layer | Result |
|---|---|
| Structural validation (`check.py`) | **42 PASS, 0 WARN, 0 FAIL** |
| Skill sync drift detection (`sync.py`) | **PASS — no drift** |
| Cookbook deploy dry-run | **PASS — staleness-watcher validates** |
| A2A test suite (pytest) | **42 passed** |
| Skill trigger evals | **94/94 PASS** (61 production + 23 niche + 10 cross-axis) |
| JSON / YAML files parse | **all 16 JSON + 4 YAML files clean** |

### Versioning

- **Patch** (`x.y.PATCH`): description tweaks, eval additions, doc fixes
- **Minor** (`x.MINOR.0`): new skills, sectors, languages, connectors, A2A tier upgrades
- **Major** (`MAJOR.0.0`): breaking changes to skill IDs, removed skills/sectors/languages

Patch-bump after any changes:

```bash
python3 scripts/sync.py --version-bump
```

Manually edit `.claude-plugin/plugin.json` + `.well-known/agent-card.json` for minor/major bumps.

### Adding to the plugin

| Want to add... | See |
|---|---|
| A new sector | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a sector" |
| A new language | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a language" |
| A new skill | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a skill" |
| A new MCP connector | [`CONNECTORS.md`](CONNECTORS.md) |
| A new agent bundle | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a bundle" |

### Architecture credits

| Pattern | Source repo |
|---|---|
| Two-`CLAUDE.md` template + cold-start interview + bounce-on-placeholder | `anthropics/claude-for-legal` |
| `~~category` placeholders + `CONNECTORS.md` + Standalone-vs-Supercharged | `anthropics/knowledge-work-plugins` |
| Agent + vertical split + `sync.py` + 3-tier cookbook + source-of-truth prompt | `anthropics/financial-services` |
| `legal-builder-hub` meta-skill recommender | `claude-for-legal/legal-builder-hub` |
| Skills eval workflow | `anthropics/skills` (skill-creator) |

### License

MIT — see [`LICENSE`](LICENSE).

### Where to start, by role

| Role | Read first |
|---|---|
| Non-technical user (manager, SEO lead, business owner) | [`USER_GUIDE.md`](USER_GUIDE.md) |
| Developer installing the plugin | This README → "TL;DR" |
| Developer extending the plugin | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Building an agent that calls this one | [`A2A.md`](A2A.md) |
| Verifying it works | [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) |
| Quarterly health-check on a deployed file | [`managed-agent-cookbooks/staleness-watcher/`](managed-agent-cookbooks/staleness-watcher/) |
| Understanding the empirical basis | [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md) |
| Just looking for "what file does what?" | [`INDEX.md`](INDEX.md) |
