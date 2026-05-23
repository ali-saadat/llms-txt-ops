# Index — Navigating the llms-txt-advisor Repo

This is the docs map. Skim it to find what you need fast.

For installation and first-use, start with [`README.md`](README.md).
For contributing, see [`CONTRIBUTING.md`](CONTRIBUTING.md).
For release history, see [`CHANGELOG.md`](CHANGELOG.md).

---

## By role

### "I'm not technical — where do I start?"

1. [`USER_GUIDE.md`](USER_GUIDE.md) — plain-English 10-part walkthrough, no jargon
2. Install via Claude Code: `/plugin marketplace add <repo-url>` → `/plugin install llms-txt-advisor`
3. Run `/llms-txt-advisor:setup-recommender` for 60-second orientation

### "I'm a developer — what do I do?"

1. [`README.md`](README.md) — install, dev quickstart, status
2. Install via `/plugin marketplace add <repo-url>`
3. Run `/llms-txt-advisor:setup-recommender` for orientation
4. Or run `/llms-txt-advisor:cold-start-interview` for full configuration

### "I want to understand the empirical evidence"

1. [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md) — three studies, Mueller quote, baseline
2. [`knowledge/04-decision-framework.md`](knowledge/04-decision-framework.md) — ship/skip decision matrix
3. [`knowledge/03-seo-perspective.md`](knowledge/03-seo-perspective.md) — GEO/AEO context

### "I'm extending the plugin — adding a sector, language, skill, or connector"

1. [`CONTRIBUTING.md`](CONTRIBUTING.md) — full development guide
2. [`evals/IMPROVEMENT_WORKFLOW.md`](evals/IMPROVEMENT_WORKFLOW.md) — eval-driven trigger optimization

### "I want to verify the plugin works"

1. [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) — comprehensive validation results
2. Run `python3 scripts/check.py` — 9-check structural validation
3. Run `python3 scripts/sync.py --check` — drift detection across agent bundles
4. Review [`evals/optimization-results.md`](evals/optimization-results.md) — eval results across 4 rounds

### "I'm deploying production agents (Managed Agents API)"

1. [`managed-agent-cookbooks/staleness-watcher/`](managed-agent-cookbooks/staleness-watcher/) — 3-tier security split cookbook
2. [`scripts/deploy-managed-agent.sh`](scripts/deploy-managed-agent.sh) — dry-run + live deploy script
3. [`A2A.md`](A2A.md) — Agent-to-Agent protocol integration

### "I need to communicate with stakeholders"

1. Run `/llms-txt-advisor:stakeholder-comms` — drafts emails in 13 languages
2. [`stakeholder/expectations.md`](stakeholder/expectations.md) — framing language
3. [`knowledge/languages/_router.md`](knowledge/languages/_router.md) — language policy

---

## By purpose

### Entry-point documentation

| File | What it covers |
|---|---|
| [`README.md`](README.md) | Master entry — non-technical + technical sections, install, status, directory tree, one-click deploy buttons |
| [`USER_GUIDE.md`](USER_GUIDE.md) | Plain-English 10-part walkthrough for non-technical users (no jargon) |
| [`INTEGRATIONS.md`](INTEGRATIONS.md) | Master guide for calling the plugin from anywhere — n8n, LangGraph, CrewAI, Python, raw HTTP |
| [`A2A.md`](A2A.md) | Agent-to-Agent v1.0 protocol: all 3 tiers, deployment, security checklist |
| [`INDEX.md`](INDEX.md) | This file — navigation map |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes (v1.0.0, v1.1.0 A2A Tier 2+3, v1.2.0 deploy + integrations) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to add sectors, languages, skills, connectors, bundles, cookbooks |
| [`MEMORY.md`](MEMORY.md) | Project memory — paths, validation commands, constraints for future Claude sessions |
| [`LICENSE`](LICENSE) | MIT |
| [`Dockerfile`](Dockerfile) + [`docker-compose.yml`](docker-compose.yml) + [`.env.example`](.env.example) | Container deploy (one-line: `docker compose up`) |
| [`requirements.txt`](requirements.txt) | Pinned pip deps for non-Docker installs |
| [`.gitignore`](.gitignore) + [`.dockerignore`](.dockerignore) | Exclusions |

### Plugin manifest and configuration

| File | What it covers |
|---|---|
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Plugin manifest — name, version, license, author |
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | 3 installable plugins (main + 2 bundles) for `/plugin marketplace add` |
| [`.mcp.json`](.mcp.json) | 13 connector category slots — fill in MCP server URLs to enable |
| [`.well-known/agent-card.json`](.well-known/agent-card.json) | A2A v1.0 Agent Card declaring all 8 skills as AgentSkill objects |
| [`CLAUDE.md`](CLAUDE.md) | Practice profile template (placeholders) — copied to `~/.claude/plugins/config/llms-txt-advisor/` on first use |
| [`CONNECTORS.md`](CONNECTORS.md) | `~~category` dictionary — 13 connector categories with Western, Asian, Russian vendor examples |
| [`A2A.md`](A2A.md) | Agent-to-Agent protocol integration status + roadmap |

### Knowledge corpus (`knowledge/`)

| File | What it covers |
|---|---|
| [`knowledge/01-foundations.md`](knowledge/01-foundations.md) | What llms.txt is, where it came from |
| [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md) | Three studies (SE Ranking, OtterlyAI, Search Engine Land) + Mueller quote |
| [`knowledge/03-seo-perspective.md`](knowledge/03-seo-perspective.md) | GEO/AEO context, how SEO teams should frame it |
| [`knowledge/04-decision-framework.md`](knowledge/04-decision-framework.md) | Ship/skip decision matrix |
| [`knowledge/05-implementation.md`](knowledge/05-implementation.md) | Spec compliance, format requirements |
| [`knowledge/06-deployment.md`](knowledge/06-deployment.md) | Server config, validation, CI |
| [`knowledge/07-failure-modes.md`](knowledge/07-failure-modes.md) | 15 anti-patterns and failure modes to avoid |
| [`knowledge/08-adjacent-features.md`](knowledge/08-adjacent-features.md) | Bing AI Performance, log analysis, adjacent features |
| [`knowledge/sectors/`](knowledge/sectors/) | 18 sectors + `_router.md` (composition matrix for product-domain × delivery-channel) |
| [`knowledge/languages/`](knowledge/languages/) | 13 languages + `_router.md` (end-user-driven policy) |

### Skills (`skills/`)

User-invokable via `/llms-txt-advisor:<skill-name>`:

| Skill | When to use |
|---|---|
| [`skills/setup-recommender/`](skills/setup-recommender/) | Orientation skill (60s–2min) — "I just installed", "first time using" |
| [`skills/cold-start-interview/`](skills/cold-start-interview/) | Full configuration (2 or 15-20min) — "configure my profile", "set up my profile" |
| [`skills/advise/`](skills/advise/) | Main router + disambiguation fallback — "should I add llms.txt", "what does llms.txt do" |
| [`skills/audit/`](skills/audit/) | Review existing file — "audit my llms.txt", "review my file" |
| [`skills/generate/`](skills/generate/) | Create new file — "generate llms.txt", "write llms.txt from scratch" |
| [`skills/customize/`](skills/customize/) | Targeted section updates — "update the products section" (requires named target) |
| [`skills/deploy/`](skills/deploy/) | Server config + validation — "deploy to Nginx", "set up CI validation" |
| [`skills/stakeholder-comms/`](skills/stakeholder-comms/) | Draft emails/Jira — "write an email to my SEO lead" |

Each skill has a `references/` subdirectory with progressive-disclosure deep-dive content (loaded only when relevant).

### Agents and managed-agent cookbooks

| Path | What it does |
|---|---|
| [`agents/`](agents/) | In-session agent bundle for interactive use |
| [`managed-agent-cookbooks/staleness-watcher/`](managed-agent-cookbooks/staleness-watcher/) | Headless 3-tier security split: crawler (untrusted HTML, no MCP) → analyzer (trusted MCP) → report-writer (only Write capability) |
| [`scripts/deploy-managed-agent.sh`](scripts/deploy-managed-agent.sh) | Cookbook deploy with `--dry-run` (default) + `--live` modes |
| [`scripts/a2a-server.py`](scripts/a2a-server.py) | A2A Tier 2 production server — FastAPI JSON-RPC + SSE + SQLite + auth + rate limiting |
| [`scripts/a2a-client.py`](scripts/a2a-client.py) | A2A Tier 3 client — `A2AClient` class + CLI (`discover`, `send`, `stream`, `get`, `cancel`, `list`) |

### Agent bundles (for `/plugin marketplace add` installations)

| Bundle | Bundled skills | Target audience |
|---|---|---|
| [`agent-bundles/llms-txt-bootstrap/`](agent-bundles/llms-txt-bootstrap/) | setup-recommender + cold-start-interview + generate + deploy | New sites without existing llms.txt |
| [`agent-bundles/llms-txt-migration/`](agent-bundles/llms-txt-migration/) | audit + customize + generate + deploy + stakeholder-comms | Sites with existing (often bloated) llms.txt |

### Case study and templates

| Path | What it covers |
|---|---|
| [`case-study/example-marketplace-case.md`](case-study/example-marketplace-case.md) | Canonical worked example: 12.5MB → 28KB marketplace recovery (anonymized) |
| [`case-study/deployment-spec.md`](case-study/deployment-spec.md) | Worked deployment specification |
| [`case-study/lessons-extracted.md`](case-study/lessons-extracted.md) | What we learned from the real case |
| [`templates/`](templates/) | Starting templates: dev-docs, marketplace, generic; `validate.sh` linter |

### Stakeholder communication

| File | What it covers |
|---|---|
| [`stakeholder/expectations.md`](stakeholder/expectations.md) | Framing language for pushback scenarios |
| [`stakeholder/email-templates/`](stakeholder/email-templates/) | Email templates by audience |

### Validation and tooling (`scripts/`)

| Script | What it does |
|---|---|
| [`scripts/check.py`](scripts/check.py) | 9-check structural validator — plugin.json, .mcp.json, CLAUDE.md, SKILL.md frontmatter, agents, cookbooks, cross-references, evals, size constraints |
| [`scripts/sync.py`](scripts/sync.py) | Skill-copy drift detection between `skills/` and `agent-bundles/*/skills/` |
| [`scripts/deploy-managed-agent.sh`](scripts/deploy-managed-agent.sh) | Managed Agents cookbook deploy (`--dry-run` default, `--live` for production) |
| [`scripts/a2a-server.py`](scripts/a2a-server.py) | A2A Tier 2 server — FastAPI JSON-RPC + SSE, SQLite, Bearer auth, rate limit, mock/live modes |
| [`scripts/a2a-client.py`](scripts/a2a-client.py) | A2A Tier 3 client — class + CLI for calling out to external A2A agents |
| [`.githooks/pre-commit`](.githooks/pre-commit) | Auto-validates on every commit |
| [`templates/validate.sh`](templates/validate.sh) | llms.txt file linter (encoding, BOM, size, URL liveness, SHA-256) |
| [`pytest.ini`](pytest.ini) | Pytest config — asyncio_mode = auto |

### A2A protocol (v1.0)

| File | What it covers |
|---|---|
| [`A2A.md`](A2A.md) | Full A2A guide — all three tiers, deployment, security checklist, testing matrix |
| [`.well-known/agent-card.json`](.well-known/agent-card.json) | Tier 1 — Agent Card declaring all 8 skills as `AgentSkill` objects |
| [`scripts/a2a-server.py`](scripts/a2a-server.py) | Tier 2 — JSON-RPC + SSE server (mock/live modes) |
| [`scripts/a2a-client.py`](scripts/a2a-client.py) | Tier 3 — outbound client (programmatic + CLI) |

### Deploy + integrations

| Path | Purpose |
|---|---|
| [`INTEGRATIONS.md`](INTEGRATIONS.md) | Master "how do I call this from X" guide |
| [`deploy/`](deploy/) | One-click hosted deploy configs (Render, Fly.io, Railway) + Caddy TLS proxy + deploy README |
| [`Dockerfile`](Dockerfile) + [`docker-compose.yml`](docker-compose.yml) | Container deploy — `docker compose up` |
| [`integrations/n8n/`](integrations/n8n/) | n8n workflow templates (audit + advise) + integration README |
| [`integrations/langgraph/`](integrations/langgraph/) | LangChain tools + LangGraph node example |
| [`integrations/crewai/`](integrations/crewai/) | `BaseTool` subclasses for CrewAI agents |
| [`integrations/python/`](integrations/python/) | Wrapper-based + raw-httpx Python patterns |
| [`integrations/raw-http/curl-examples.sh`](integrations/raw-http/curl-examples.sh) | Bare-bones HTTP examples — works from any language |

### Tests (`tests/`)

| File | What it covers |
|---|---|
| [`tests/conftest.py`](tests/conftest.py) | Pytest fixtures + module loader for hyphen-named scripts |
| [`tests/test_a2a_server.py`](tests/test_a2a_server.py) | 25 tests — server endpoints, JSON-RPC methods, auth, rate limit, SSE, persistence, audit |
| [`tests/test_a2a_client.py`](tests/test_a2a_client.py) | 11 tests — Agent Card validation + client unit tests via httpx.MockTransport |
| [`tests/test_a2a_loopback.py`](tests/test_a2a_loopback.py) | 4 tests — full end-to-end client→server via httpx.ASGITransport |

Run all: `python3 -m pytest tests/ -v` → 42 passed in ~1 second.

### Validation results

| File | What it covers |
|---|---|
| [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) | Comprehensive validation results across all layers |
| [`evals/`](evals/) | 8 evals.json files (61 production prompts) + niche/cross-axis tests |
| [`evals/optimization-results.md`](evals/optimization-results.md) | 4-round eval optimization journey |
| [`evals/IMPROVEMENT_WORKFLOW.md`](evals/IMPROVEMENT_WORKFLOW.md) | Reusable eval-driven optimization pattern |

---

## Quick lookup

| If you want to... | Go to |
|---|---|
| Install the plugin | [`README.md`](README.md) → "Install" |
| Understand why we recommend skip for marketing sites | [`knowledge/04-decision-framework.md`](knowledge/04-decision-framework.md) |
| See the three empirical studies | [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md) |
| Add a new sector | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a sector" |
| Add a new language | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Adding a language" |
| Deploy a managed agent | [`scripts/deploy-managed-agent.sh`](scripts/deploy-managed-agent.sh) + [`A2A.md`](A2A.md) |
| Set up MCP connectors | [`.mcp.json`](.mcp.json) + [`CONNECTORS.md`](CONNECTORS.md) |
| Understand A2A integration | [`A2A.md`](A2A.md) |
| Run evals | [`evals/IMPROVEMENT_WORKFLOW.md`](evals/IMPROVEMENT_WORKFLOW.md) |
| Validate the repo | `python3 scripts/check.py` |
| Find a specific anti-pattern | [`knowledge/07-failure-modes.md`](knowledge/07-failure-modes.md) |
| See the canonical worked case | [`case-study/example-marketplace-case.md`](case-study/example-marketplace-case.md) |

---

## How to find what you need

This repo has 137+ files. If you're not sure where to look:

1. **Search by keyword**: `grep -r "your-keyword" knowledge/ skills/`
2. **Find the skill**: skill descriptions in `skills/*/SKILL.md` frontmatter list every trigger phrase
3. **Find the sector**: [`knowledge/sectors/_router.md`](knowledge/sectors/_router.md) maps any site type
4. **Find the language**: [`knowledge/languages/_router.md`](knowledge/languages/_router.md) covers 13 languages + end-user policy
5. **Still stuck?** Run `/llms-txt-advisor:advise` — it routes to the right skill based on what you ask
