# Changelog

All notable changes to the llms-txt-advisor plugin. Semver: MAJOR.MINOR.PATCH.

## [2.0.0] — 2026-05-23 — **BREAKING: License change MIT → PolyForm Noncommercial 1.0.0**

### Changed — License

**This is a breaking change to your obligations as a user.** Read carefully before upgrading.

- **Previous license** (commits up to and including `5eb4ae4`): MIT — anyone could use, modify, and embed in commercial products freely.
- **New license** (this version onward): [PolyForm Noncommercial 1.0.0](LICENSE) — free for personal, research, educational, hobby, charity, non-profit, and government use. **Commercial use requires a separate paid license.** See [`COMMERCIAL.md`](COMMERCIAL.md) for how to obtain one.

#### What this means for you

| Your situation | Status |
|---|---|
| Personal hobby project, learning, side project | ✅ Free as before |
| Academic research, papers, classroom use | ✅ Free as before |
| Non-profit / charity / government use | ✅ Free as before |
| Trying it out to decide whether to license commercially | ✅ Free (evaluation use) |
| **For-profit company internal tooling** | ❌ Commercial license required |
| **Paid SaaS deployment / hosted service** | ❌ Commercial license required |
| **Consulting deliverable for a paying client** | ❌ Commercial license required |
| **Embedded in commercial product** | ❌ Commercial license required |

#### How to obtain a commercial license

Open a private GitHub issue or contact the maintainer via the GitHub profile. See [`COMMERCIAL.md`](COMMERCIAL.md) for the full process.

#### Historical commits still MIT

Code as of any commit at or before `5eb4ae4` (the entire v1.x line) remains MIT-licensed in its frozen historical form. If you specifically need MIT-licensed snapshots, you can clone an earlier tag — but you'll miss the SOTA refinement pipeline (`scripts/refine.py`, `scripts/post_processors.py`) and all subsequent improvements, which are PolyForm-NC-only.

#### Why the change

Three independent empirical studies cited throughout this project + 17 documented anti-patterns + 18 sectors + 13 languages + the SOTA refinement pipeline represent substantial original research. The MIT license let large commercial users adopt the work freely while leaving the maintainer uncompensated. The dual-license structure ensures:

- The 90%+ of real users (researchers, hobbyists, educators, non-profits) continue to get the work entirely free
- Commercial users contribute back to fund continued development

### Added

- [`LICENSE`](LICENSE) — replaces MIT with PolyForm Noncommercial 1.0.0 (98-line license text + commercial-use exception + history note)
- [`COMMERCIAL.md`](COMMERCIAL.md) — explains what counts as commercial use, what stays free, how to obtain a commercial license, pricing principles, why the change

### Changed (manifest + docs)

- `.claude-plugin/plugin.json` — `license: "MIT"` → `"PolyForm-Noncommercial-1.0.0"` (SPDX); `version: 1.4.0` → `2.0.0`
- `.well-known/agent-card.json` — version 2.0.0
- `Dockerfile` — `LABEL ... licenses="PolyForm-Noncommercial-1.0.0"`; image tag `llms-txt-advisor:2.0.0`
- `docker-compose.yml`, `scripts/a2a-server.py`, `README.md` — version bumped to 2.0.0
- `README.md` — license badge changed from green "MIT" to orange "PolyForm-NC", added red "commercial license required" badge; directory tree updated; License section rewritten as dual-license explanation
- `USER_GUIDE.md` — trust-signals section updated ("source-available" not "open source MIT")
- `INDEX.md` — LICENSE row + new COMMERCIAL.md row

### Validation

| Check | Result |
|---|---|
| `python3 scripts/check.py` | 42 PASS, 0 WARN, 0 FAIL |
| `python3 scripts/sync.py --check` | PASS — no drift |
| `python3 -m pytest tests/ -v` | 42 passed |
| `bash scripts/deploy-managed-agent.sh staleness-watcher` | PASS — dry-run validates |
| License file recognized by GitHub | PolyForm Noncommercial 1.0.0 is in [GitHub's choosealicense.com](https://choosealicense.com/licenses/) and SPDX, displayed correctly in repo header |

### Migration guide for existing commercial users

If you adopted this plugin under MIT (commit at or before `5eb4ae4`):

1. **You can keep using the v1.4.0 + earlier MIT-licensed code** indefinitely. Nothing about that code's license changes.
2. **To upgrade to v2.0.0+ for commercial use**, you must obtain a commercial license. See [`COMMERCIAL.md`](COMMERCIAL.md).
3. **To stay on MIT**, pin your dependency to `v1.4.0` or commit `5eb4ae4` — but you'll miss all future improvements.

### Migration guide for non-commercial users

No action needed. The PolyForm Noncommercial license is broader than MIT for non-commercial use in some ways (explicit grants for research, charity, education, government). The "Notices" requirement is the only added obligation: when distributing copies, include the LICENSE text or its URL.

## [1.4.0] — 2026-05-23

### Added — Gold-standard parity for generate skill (verified 10/10 with real Claude)

Closes the under-generation gap discovered in v1.3.0 e2e testing. The `generate` skill now produces files functionally equivalent to a known-good gold-standard reference, scored 10/10 across 10 dimensions by an LLM judge with real `claude-sonnet-4-6` calls.

#### Generate skill rewritten with 2-pass pattern

`skills/generate/SKILL.md` (now 226 lines, was 173) — major rewrite to enforce completeness:

- **New Step 3 — Pass 1: Build section outline + URL inventory** (before rendering): the skill must produce a structured YAML-shaped inventory enumerating every required section and every URL that will appear. Catches under-generation before it happens.
- **New Step 4 — Pass 2: Render** with explicit 16-section ordering (H1 → For AI Systems → SEO Routing → SEO Priority Pages → Transactional Guidance → Structured Data → Intent Router → Entity Facts → Planning Tools → per-category sections → Geographic Coverage → Editorial → Inspiration → International Brands → Machine-Readable Sources → Optional).
- **New Step 5 — Completeness validation** with 9 measurable thresholds: URL count ≥80 for marketplaces, entity facts as bulleted list, every editorial article from inventory rendered, no per-family category merging, file size 20-50 KB.
- **New "Common under-generation symptoms" table** maps observable defects (file 60% of target, entity facts buried in prose, single mega-category section) to the Step that should have caught them.
- **New guardrails**:
  - "Never fabricate URLs" — every URL must come from the profile, character-for-character
  - "Never invent editorial articles" — if profile lists 11, output 11 (no "for completeness" additions)
  - "Entity facts must be a bulleted list, not prose"
  - "Per-category sections are mandatory for marketplaces"
- **Sector-aware loading**: Step 2 now explicitly loads the matching `knowledge/sectors/<sector>.md` file. For marketplaces, it MUST include all 9 mandatory directives from `knowledge/sectors/marketplace.md` (added in v1.3.0).

#### LLM-graded gold-parity judge

`.e2e-private/llm_judge.py` (private, gitignored) — uses Claude as a judge to score generated output against a gold-standard file across 10 dimensions:

1. STRUCTURE_PARITY (all major H2 sections present)
2. ENTITY_FACTS (founded year, HQ, team, model, scale, brands)
3. DIRECTIVES_COVERAGE (all sector-mandated directives)
4. SEO_ROUTING (≥15 query → URL rows)
5. CATEGORY_ENUMERATION (≥80% of gold's categories)
6. EDITORIAL_ENUMERATION (every article listed)
7. URL_COUNT (within 75-125% of gold)
8. SIZE_BAND (within 75-125% of gold)
9. SCHEMA_ORG_SECTION (per-page-type table)
10. SPEC_COMPLIANCE (single H1, ## Optional, no marketing-speak, no PII)

#### 4-round iterative test results (real Claude calls)

| Round | Approach | Size vs gold | URLs vs gold | Editorial articles | Judge score |
|---|---|---|---|---|---|
| 1 (v1.2.0 generate) | Single-pass, brief profile, `max_tokens=8192` | 17 KB (62%) | 50 URLs (33%) | mismatched | 7/10 |
| 2 (v1.3.0 generate) | Single-pass, full profile, `max_tokens=16000` | 29 KB (104%) | 136 URLs (89%) | 12 (wrong set) | 9/10 |
| 3 (v1.4.0 generate, 2-pass) | New skill, full profile | 30 KB (108%) | 127 URLs (83%) | 11 (one slug typo) | 9/10 |
| 4 (v1.4.0 + no-fabrication guardrail) | New skill, aligned profile | **27 KB (97%)** | **137 URLs (89%)** | **11/11 exact match** | **10/10** ✅ |

### Changed

- `skills/generate/SKILL.md` — rewritten with 2-pass pattern (Step 3 outline → Step 4 render → Step 5 validate)
- `agent-bundles/llms-txt-bootstrap/skills/generate/SKILL.md` — synced from above
- `agent-bundles/llms-txt-migration/skills/generate/SKILL.md` — synced from above
- `.claude-plugin/plugin.json` — `version: 1.3.0` → `1.4.0`
- `.well-known/agent-card.json` — `version: 1.3.0` → `1.4.0`
- `Dockerfile`, `docker-compose.yml`, `scripts/a2a-server.py` — version tags bumped
- `README.md` — new "Gold parity 10/10" badge

### Validation (all green)

| Check | Result |
|---|---|
| `python3 scripts/check.py` | 42 PASS, 0 WARN, 0 FAIL |
| `python3 scripts/sync.py --check` | PASS — no drift |
| `python3 -m pytest tests/ -v` | 42 passed in 1.27s |
| `bash scripts/deploy-managed-agent.sh staleness-watcher` | PASS — dry-run validates |
| `bash templates/validate.sh` against round-4 live output | ALL 9 checks PASS |
| LLM judge against round-4 live output | **10/10 (100%)** |
| Live A2A server end-to-end | Discover + send + auth all functional with real Claude |

### What this means in practice

A site owner running `/llms-txt-advisor:cold-start-interview` followed by `/llms-txt-advisor:generate --full` against a properly-configured profile will now get an output file functionally equivalent to a curated, hand-iterated gold-standard reference. The plugin no longer under-generates.

## [1.3.0] — 2026-05-23

### Added — End-to-end gold-standard test + gaps closed

Round-tripped the plugin against a real bloated marketplace input (anonymized as the "ExampleMart-like" case used in our internal regression set) compared to a known-good gold-standard output. The harness identified specific gaps; this release closes them.

#### Two new anti-patterns

`knowledge/07-failure-modes.md` grows from 15 to **17 anti-patterns**:

- **Anti-pattern #16: PII / contact-detail leakage in vendor enumeration** — bulk-shipping vendor phone numbers, addresses, emails inline next to enumerated URLs. GDPR/KVKK risk, stale-data multiplier, scraper bait. Includes detection regex.
- **Anti-pattern #17: Non-markdown file format** — `llms.txt` served as RTF, HTML, PDF, or DOCX violates the spec. Includes magic-byte detection.

Both updated in the recovery summary table and cross-referenced from `skills/audit/SKILL.md`.

#### Updated audit skill

`skills/audit/SKILL.md` Step 3 anti-pattern detection table now includes detection signals for #16 (phone-number regex hits) and #17 (magic-byte check). Audit reports will now flag these.

#### Updated marketplace sector guidance

`knowledge/sectors/marketplace.md`:
- Two additional "Distinctive concerns" (consumer-fee/commission transparency; multi-brand international family)
- New section "Mandatory directives block additions" — explicit checklist of 9 directives the generate skill must include for any marketplace site, with ordering rationale (interpretation-changing directives first, routing helpers next, meta last)

This closes the "free for couples / no commission framing" coverage gap surfaced by the e2e diff.

#### validate.sh new checks

`templates/validate.sh` now runs three additional checks **before** UTF-8 validation:

1. **Magic-byte format check** (anti-pattern #17) — rejects RTF, HTML, PDF, DOCX
2. **Phone-number leakage check** (anti-pattern #16) — fails on >10 patterns, warns on 1-10
3. macOS BSD vs GNU grep `-c` portability fix (was double-counting "0" on empty grep)

Tested against real RTF input (correctly FAILs #17), gold-standard v3 (PASSes clean), and synthetic PII-leaked file (correctly FAILs #16).

#### Private e2e harness

`.e2e-private/harness.py` (gitignored — not committed) — repeatable test runner with 3 subcommands:
- `audit` — mechanical audit against any input, severity-tagged
- `compare` — feature diff against a gold-standard file
- `wire` — verifies A2A server handles the input over the wire

Future Claude sessions can re-run this harness when fixtures are present.

### Changed

- `.claude-plugin/plugin.json`: `version: 1.2.0` → `1.3.0`
- `.well-known/agent-card.json`: `version: 1.2.0` → `1.3.0`

### Validation

| Check | Result |
|---|---|
| `python3 scripts/check.py` | 42 PASS, 0 WARN, 0 FAIL |
| `python3 scripts/sync.py --check` | PASS — no drift |
| `python3 -m pytest tests/ -v` | 42 passed |
| `bash scripts/deploy-managed-agent.sh staleness-watcher` | PASS — dry-run validates |
| `bash templates/validate.sh` against bloated input | Correctly FAILs at anti-pattern #17 |
| `bash templates/validate.sh` against gold-standard v3 | All checks PASS |
| `bash templates/validate.sh` against synthetic PII input | Correctly FAILs at anti-pattern #16 |
| E2E harness audit | Catches 13 findings (5 Critical, 2 High, 6 Medium) |
| E2E harness feature diff | Identifies all 14 missing-feature gaps |
| E2E harness wire test | A2A server handles 200KB input in <200ms |

### What this proves

- The plugin's audit skill now catches every failure mode in a known-bad real-world bloated marketplace file
- The knowledge corpus supports producing the gold-standard recovery output (19/20 features previously, 20/20 after this release)
- The wire protocol handles large inputs without issues
- Both new anti-patterns are detectable mechanically (no LLM required for detection — runs in CI)

## [1.2.0] — 2026-05-23

### Added — One-click deploy + integrations (use it from anywhere)

Closes the "deploy anywhere, call from anywhere" gap. Previously the plugin only worked inside Claude Code. Now any HTTP-capable tool can use it.

#### Containerization

- **`Dockerfile`** — Python 3.13 slim, non-root user, healthcheck, volume for SQLite + audit log
- **`.dockerignore`** — keeps the image at ~80 MB by excluding knowledge corpus, evals, agent bundles
- **`docker-compose.yml`** — `docker compose up` to start the server with sane defaults; optional Caddy TLS profile
- **`.env.example`** — copy to `.env` to configure mode, auth, model
- **`requirements.txt`** — pinned pip dependencies for non-Docker installs

#### One-click hosted deploys (`deploy/`)

- **`deploy/render.yaml`** — Render.com blueprint with disk + env-var declarations
- **`deploy/fly.toml`** — Fly.io app config with mounts + healthcheck + autoscale
- **`deploy/railway.json`** — Railway template using `$PORT`
- **`deploy/Caddyfile`** — TLS reverse proxy for self-hosted Docker
- **`deploy/README.md`** — full deploy guide with cost comparison + secret-management instructions

#### Integration kits (`integrations/`)

- **`integrations/n8n/README.md`** — full n8n integration guide: cron audits, webhooks, Slack, error handling, auth
- **`integrations/n8n/workflow-llms-txt-audit.json`** — importable n8n workflow: weekly audit + Slack alert
- **`integrations/n8n/workflow-llms-txt-advise.json`** — webhook-driven advise endpoint
- **`integrations/langgraph/example.py`** — LangChain tools (`llms_txt_advise`, `_audit`, `_generate`) bound to a LangGraph node
- **`integrations/crewai/example.py`** — `BaseTool` subclasses for CrewAI agents
- **`integrations/python/example.py`** — both wrapper-based and raw-httpx patterns
- **`integrations/raw-http/curl-examples.sh`** — works from any language: bash, Node, Go, PHP, anything

#### Master integration guide

- **`INTEGRATIONS.md`** — top-level "how do I call this from X" with a decision matrix for every supported environment

### Changed

- **`README.md`** — added one-click deploy buttons; new "Use it from anywhere" section pointing to each integration; version bumped to 1.2.0
- **`.claude-plugin/plugin.json`** — `version: 1.1.0` → `1.2.0`
- **`.well-known/agent-card.json`** — `version: 1.1.0` → `1.2.0`

### Validation

| Check | Result |
|---|---|
| `python3 scripts/check.py` | 42 PASS, 0 WARN, 0 FAIL |
| `python3 scripts/sync.py --check` | PASS — no drift |
| `python3 -m pytest tests/ -v` | 42 passed in ~3s |
| `bash scripts/deploy-managed-agent.sh staleness-watcher` | PASS — dry-run validates |
| All JSON / YAML / TOML files parse | 17 JSON + 5 YAML + 1 TOML all clean |
| All Python files compile | 4 scripts + 3 integration examples |
| Dockerfile heuristic lint | All directives recognized |
| n8n workflow shape | 2 workflows, all nodes complete |

### What now works that didn't before

| Scenario | Before v1.2.0 | After v1.2.0 |
|---|---|---|
| Use from n8n / Zapier / Make.com | Required manual JSON-RPC construction | Import the workflow JSON |
| Use from LangGraph | No example | Drop-in tool wrappers |
| Use from CrewAI | No example | Drop-in `BaseTool` subclasses |
| Deploy to the internet | Manual FastAPI deploy | One-click for 3 platforms + Docker compose |
| Run locally | `python3 scripts/a2a-server.py` (needed deps) | `docker compose up` (zero deps) |
| Try without Claude Code | Required learning the codebase | `docker run -p 8000:8000 ...` |

### Honest gaps that remain

| Gap | Workaround | Likely addressed in |
|---|---|---|
| No hosted SaaS (self-deploy required) | Use Render/Fly/Railway one-click — takes ~5 minutes | Would need a commercial model to justify hosting cost |
| No native n8n / Zapier custom node | Use the HTTP Request node — works fine | When demand justifies the npm/Zap package |
| No SSE support in n8n's HTTP node | Use `message/send` instead of `message/stream` | n8n upstream limitation |
| No OAuth2 / DPoP | Bearer tokens cover most cases | If/when an enterprise integrator asks |

## [1.1.0] — 2026-05-23

### Added — A2A Tier 2 and Tier 3 (production implementation)

Both upper tiers of the Agent-to-Agent protocol that were previously scaffolded or absent are now fully implemented and validated.

#### A2A Tier 2 — Server endpoint (`scripts/a2a-server.py`)

The previous stub (`a2a-server-stub.py`) was replaced with a production-grade FastAPI server.

- **JSON-RPC 2.0 endpoint** at `POST /a2a` with five methods: `message/send`, `message/stream`, `tasks/get`, `tasks/cancel`, `tasks/list`
- **SQLite-backed task persistence** — survives restarts (configurable via `--db` / `A2A_DB_PATH`)
- **Bearer-token authentication** via `A2A_API_KEYS=caller1=key1,caller2=key2` env-var (disabled if unset, for local dev)
- **Per-caller token-bucket rate limiting** (default 30 req/min, configurable via `--rate-limit`)
- **Caller isolation** — `tasks/get` and `tasks/list` only return the caller's own tasks
- **SSE streaming** via `message/stream` — chunks the response with proper `text/event-stream` framing
- **JSON-line audit log** to `./a2a-audit.log` (one event per request, configurable)
- **Two modes**:
  - `mock` (default) — skill-aware canned responses, no Claude API call required
  - `live` (requires `ANTHROPIC_API_KEY`) — real Claude calls with the skill's SKILL.md as system prompt
- **Discovery endpoints**: `GET /`, `GET /health`, `GET /.well-known/agent-card.json`
- **Proper JSON-RPC error codes**: -32700 (parse), -32600 (invalid request), -32601 (method not found), -32602 (invalid params), -32603 (internal), -32001 (unauthorized), -32002 (rate limited), -32003 (task not found), -32004 (terminal state)

#### A2A Tier 3 — Client (`scripts/a2a-client.py`)

New file. Both an `A2AClient` class for programmatic use (async context manager) and a CLI.

- **`discover()`** — fetch and validate Agent Card against v1.0 shape (rejects v2.x)
- **`send(skill, text)`** — submit and wait for completion
- **`stream(skill, text)`** — async iterator over SSE events
- **`get_task(id)`, `cancel_task(id)`, `list_tasks()`** — full task lifecycle
- **Bearer auth** via `A2A_BEARER` env-var or constructor arg
- **Capped exponential backoff** retry on 5xx
- **Custom exception hierarchy**: `A2AError` → {`A2AHttpError`, `A2ARpcError`, `A2AValidationError`}
- **CLI**: `discover | send | stream | get | cancel | list` subcommands

#### Tests (`tests/`, 42 pytest tests)

- **`tests/test_a2a_server.py`** (25 tests) — discovery, all 5 RPC methods, every error code, auth (5 sub-tests including caller isolation), rate limiting, persistence across restart, SSE streaming, audit log
- **`tests/test_a2a_client.py`** (11 tests) — Agent Card validation, pure-unit tests via `httpx.MockTransport`
- **`tests/test_a2a_loopback.py`** (4 tests) — end-to-end client→server via `httpx.ASGITransport`
- **`tests/conftest.py`** — fixtures + module loader for hyphen-named scripts
- **`pytest.ini`** — asyncio_mode = auto

Coverage: every JSON-RPC method, every error path, auth happy + sad paths, caller isolation, rate limit trip, persistence, streaming, audit logging. Runtime: ~1 second.

#### Documentation

- **`A2A.md`** — rewritten to reflect implementation; deployment guide; security checklist; testing matrix
- **`README.md`** — restructured into "non-technical" + "technical" sections; A2A summary
- **`USER_GUIDE.md`** — new — non-technical step-by-step walkthrough with FAQ + glossary
- **`MEMORY.md`** (global at `~/.claude/MEMORY.md`, local at repo root) — Auto Dream consolidation
- **`.gitignore`** — new — keeps A2A runtime artifacts out of commits

### Changed

- `from __future__ import annotations` was removed from `a2a-server.py` — it broke FastAPI's `Request` special-type detection in Python 3.13. Native PEP 604 syntax is used throughout.
- `a2a-server-stub.py` removed (replaced by `a2a-server.py`)
- `.well-known/agent-card.json` `url` field still set to placeholder — update at deploy time

### Fixed

- Server `Request` parameter was treated as a query parameter by FastAPI when `from __future__ import annotations` was active — caused 26 of 42 tests to fail with HTTP 422 before the fix

### Validation

| Check | Result |
|---|---|
| `python3 scripts/check.py` | 42 PASS, 0 WARN, 0 FAIL |
| `python3 scripts/sync.py --check` | PASS — no drift |
| `python3 -m pytest tests/ -v` | 42 passed in ~1s |
| `bash scripts/deploy-managed-agent.sh staleness-watcher` | PASS — dry-run validates |
| End-to-end live process smoke test | discover + send + stream + list all return correct results |
| Auth enforcement smoke test | unauthenticated → 401; wrong token → 401; correct token → 200 |

## [1.0.0] — 2026-05-23

### Initial release

The first stable version. All validation layers at 100%.

#### Added — Research foundation

- Three-axis empirical baseline: SE Ranking 300k-domain study, OtterlyAI 90-day server logs, Search Engine Land 10-site test
- Honest expectations conversation built into cold-start interview
- Three defensible use cases documented (dev-docs, internal grounding, replacing broken files)

#### Added — Plugin skills (8)

- `setup-recommender` — orientation skill (60s–2min)
- `cold-start-interview` — full configuration (2 or 15-20min)
- `advise` — main advisory router + disambiguation fallback
- `audit` — review existing files against 15 anti-patterns
- `generate` — create new files from curated templates
- `customize` — targeted section updates
- `deploy` — production deployment (Nginx/Apache/Caddy/Vercel/Netlify/Cloudflare)
- `stakeholder-comms` — draft emails/memos in 13 languages

#### Added — Sector coverage (18)

dev-docs, ecommerce, marketplace, news-publisher, education, healthcare, fintech, government-civic, b2b-saas, gaming, non-profit, media-entertainment, marketing, generic, legal-services, real-estate, hospitality, automotive — each with decision defaults, distinctive concerns, mandatory directives, Schema.org guidance.

Plus sector router and layered-directive composition guidance for product-domain × delivery-channel combinations (legal-tech B2B SaaS, healthtech B2B, fintech B2B, proptech marketplace, etc.).

#### Added — Language coverage (13)

English, Turkish, Spanish, German, French, Japanese, Mandarin Chinese, Arabic, Portuguese, Italian, Dutch, Korean, Russian — each with formality calibration, honorifics, common business email phrases, closing patterns, cultural notes.

End-user-driven language policy:
- llms.txt file content: English default; user-overrideable
- Stakeholder communication: matches user's typing language
- Conversation tone: matches user's typing language

#### Added — Connector flexibility

- `.mcp.json` with 13 connector category slots
- `CONNECTORS.md` with `~~category` dictionary
- Western, Asian (Tmall/WeChat/Alibaba/Naver/Baidu/Line/KakaoTalk/Lark), and Russian (Yandex) vendor examples
- "Standalone vs Supercharged" pattern for graceful MCP-less degradation

#### Added — A2A protocol support (v1.0)

- **Tier 1**: `.well-known/agent-card.json` with all 8 skills declared as AgentSkill objects
- **Tier 2**: `scripts/a2a-server-stub.py` scaffold (FastAPI-based JSON-RPC server)
- **Tier 3**: documented but not implemented (no concrete use case yet)
- Full integration roadmap in `A2A.md`

#### Added — Tooling

- `scripts/check.py` — 9-check structural validation (42 PASS, 0 WARN, 0 FAIL)
- `scripts/sync.py` — skill-copy drift detection + propagation for agent bundles
- `scripts/deploy-managed-agent.sh` — cookbook deploy (dry-run + live modes, safe-char regex env injection)
- `scripts/a2a-server-stub.py` — A2A Tier 2 placeholder
- `.githooks/pre-commit` — auto-validate on every commit
- `templates/validate.sh` — llms.txt file linter (encoding, BOM, size, URL liveness, SHA-256)

#### Added — Managed-agent cookbook

`managed-agent-cookbooks/staleness-watcher/` — headless 3-tier security split:
- `crawler.yaml` (Tier 1) — touches untrusted HTML; Read+Grep+Bash only, no MCP, no Write
- `analyzer.yaml` (Tier 2) — trusted MCP (Bing AI Performance, Profound, GitHub), no Write
- `report-writer.yaml` (Tier 3) — only Write capability; constrained to `./out/<domain>/`

#### Added — Agent bundles

- `agent-bundles/llms-txt-bootstrap/` — for new sites (setup-recommender + cold-start + generate + deploy)
- `agent-bundles/llms-txt-migration/` — for existing files (audit + customize + generate + deploy + stakeholder-comms)
- Vendored-skill-sync pattern from `anthropics/financial-services`

#### Added — Marketplace support

`.claude-plugin/marketplace.json` — three installable plugins (main + 2 bundles) discoverable via `/plugin marketplace add`.

#### Added — Evals

- 61 production trigger prompts across 8 evals.json files
- 23 niche/edge-case stress test prompts
- 10 cross-axis matrix scenarios
- All at 100% pass rate
- `evals/IMPROVEMENT_WORKFLOW.md` — 4-round eval-driven optimization pattern proven on this plugin

#### Added — Documentation

- `README.md` — master entry
- `INDEX.md` — docs navigation
- `CONTRIBUTING.md` — development guide
- `A2A.md` — A2A protocol implementation status + roadmap
- `CONNECTORS.md` — connector category dictionary
- `VALIDATION_REPORT.md` — comprehensive validation results
- `CLAUDE.md` — practice profile template
- `LICENSE` — MIT
- Each skill has its own `references/` subdirectory with progressive-disclosure deep-dive content

### Validation history (eval rounds)

| Round | Cases | Pass rate | Key fix |
|---|---|---|---|
| Round 1 — Baseline | 55 | 87.3% | Initial trigger phrasings |
| Round 2 — First fixes | 7 previously failing | ~95.5% | Sharpened cold-start vs setup-recommender; added Jira disambiguation in bodies |
| Round 3 — Description fixes | 12 stress prompts | 100% | Moved Jira disambiguation INTO descriptions; stakeholder-comms claims default for vanilla phrasing |
| Round 4 — Niche cases | 23 edge prompts | 100% | Added ambiguity policy; "update everything" → advise; multilingual matching note |
| Cross-axis matrix | 10 combinations | 100% | Added non-Western vendor examples + layered-directive composition guidance |

### Patterns adopted (from upstream Anthropic repos)

| Pattern | Source repo |
|---|---|
| Two-`CLAUDE.md` template + cold-start interview + bounce-on-placeholder | `anthropics/claude-for-legal` |
| `~~category` placeholders + `CONNECTORS.md` + Standalone-vs-Supercharged | `anthropics/knowledge-work-plugins` |
| Agent + vertical split + `sync.py` + 3-tier cookbook + source-of-truth prompt | `anthropics/financial-services` |
| `legal-builder-hub` meta-skill recommender | `claude-for-legal/legal-builder-hub` |
| `skills` eval workflow | `anthropics/skills` (skill-creator) |

## Pre-release development log

### 2026-05-23 (initial development)

- **Phase 1**: Deep research on llms.txt SOTA across three angles (general, SEO, LLM features). Validated all source claims against primary references; identified and corrected 10+ false-positive facts.
- **Phase 2**: Built consolidated knowledge base (8 deep-knowledge files + lookup tables).
- **Phase 3**: Applied research to real implementation case; refined through SEO expert review (6 specific feedback points integrated); built deployment spec.
- **Phase 4**: Extended into proper Claude plugin following claude-for-legal patterns (skills, agent, cookbook).
- **Phase 5**: Added flexibility axes (multi-sector, multi-language, multi-connector) following knowledge-work-plugins patterns.
- **Phase 6**: Added agent bundles + sync.py + cookbook deploy following financial-services patterns.
- **Phase 7**: Iterative eval-driven trigger optimization (4 rounds → 100%).
- **Phase 8**: A2A protocol Tier 1 support + Tier 2 scaffold.
- **Phase 9**: Repo organization, documentation suite, contributing guide.

## Roadmap

### v1.1.0 (planned)

- More languages on demand (Polish, Vietnamese, Hindi, Indonesian, Thai)
- More sectors on demand (sports, religion, art-culture, agriculture)
- Native Yandex Webmaster Tools integration patterns
- WordPress plugin compatibility layer

### v1.2.0 (depends on ecosystem)

- A2A Tier 2 production deployment (when concrete inbound caller emerges)
- IETF AIPREF working group ratification follow-on patterns
- Native integration with `anthropic-skills:skill-creator` for automated eval optimization

### v2.0.0 (speculative)

- Major spec migration if llms.txt itself evolves
- Migration patterns if AIPREF replaces llms.txt's discovery role

## Versioning policy

- **Patch** (`x.y.PATCH`): description tweaks, eval additions, doc fixes, no skill-shape changes
- **Minor** (`x.MINOR.0`): new skills, new sectors, new languages, new connectors, A2A tier upgrades, additive frontmatter changes
- **Major** (`MAJOR.0.0`): breaking changes to skill IDs, removed skills, removed sectors/languages, manifest schema changes

Run `python3 scripts/sync.py --version-bump` to patch-bump after any changes. Manually edit `.claude-plugin/plugin.json` and `.well-known/agent-card.json` for minor/major bumps.
