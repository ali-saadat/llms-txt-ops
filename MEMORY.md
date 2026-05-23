# MEMORY.md — llms-txt-advisor plugin

*Project-specific facts for future Claude sessions. Curated per the Auto Dream protocol. Keep under 200 lines.*

## What this repo is

A Claude Code plugin (`llms-txt-advisor`) for advising websites on whether/how to ship an `llms.txt` file. Honest framing: empirical evidence (three independent studies) shows **null AI-citation impact**. Defensible use cases are narrow: developer docs, internal RAG grounding, replacing bloated existing files.

Distributed as: standalone plugin, two agent bundles (bootstrap + migration), managed-agent cookbook (staleness-watcher with 3-tier security split), and an A2A v1.0 server (callable from anywhere).

## Critical user constraints (preserve verbatim)

1. **Never name the private test client or its industry in committed files.** Real-world test fixtures live under `.e2e-private/` (gitignored). All examples in the public repo use anonymized "ExampleMart" / generic marketplace language. Specific industry verticals from private fixtures are also kept out of committed examples.
2. **Language policy is end-user-driven.** llms.txt file content default = English (user-overrideable). Stakeholder communication + conversation tone = match user's typing language.
3. **No AI attribution in commits.** Inherits from global rule.

## Current state (v1.4.0, 2026-05-23)

| Aspect | Value |
|---|---|
| Plugin version | 1.4.0 |
| Files | ~175 total, 11 root docs |
| Skills | 8 user-invocable (+ 12 progressive-disclosure references) |
| Anti-patterns documented | 17 (added #16 PII leakage, #17 non-markdown format in v1.3.0) |
| Sectors | 18 + composition router |
| Languages | 13 + end-user-driven policy router |
| Agent bundles | 2 (bootstrap, migration) — sync'd via sync.py |
| Cookbooks | 1 (staleness-watcher, 3-tier security split) |
| A2A | Tier 1 live + Tier 2 implemented + Tier 3 implemented |
| Tests | 42 pytest passing in ~1s |
| Trigger evals | 94 prompts (61 production + 23 niche + 10 cross-axis), 100% pass |
| Gold-parity score | **10/10** verified by LLM judge using `claude-sonnet-4-6` |

## Validation chain (run before any commit)

```bash
python3 scripts/check.py            # structural: must show 42 PASS, 0 WARN, 0 FAIL
python3 scripts/sync.py --check     # drift between skills/ and agent-bundles/*/skills/
python3 -m pytest tests/ -q         # A2A test suite
bash scripts/deploy-managed-agent.sh staleness-watcher  # cookbook dry-run
```

Pre-commit hook at `.githooks/pre-commit` runs check.py + sync.py automatically (enable via `git config core.hooksPath .githooks`).

## Key paths

| Purpose | Path |
|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Marketplace plugins (3 installable) | `.claude-plugin/marketplace.json` |
| MCP connector config | `.mcp.json` |
| A2A Agent Card (Tier 1) | `.well-known/agent-card.json` |
| A2A Tier 2 server | `scripts/a2a-server.py` |
| A2A Tier 3 client | `scripts/a2a-client.py` |
| Profile template (placeholders) | `CLAUDE.md` → user copies to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` |
| Skills source of truth | `skills/` (propagated to `agent-bundles/*/skills/` via `sync.py`) |
| Knowledge corpus | `knowledge/01..08-*.md` + `knowledge/sectors/` + `knowledge/languages/` |
| Empirical evidence | `knowledge/02-empirical-evidence.md` (SE Ranking n=300k, OtterlyAI 90d, Search Engine Land) |
| Anti-patterns | `knowledge/07-failure-modes.md` (17 documented) |
| Eval suite | `evals/*/evals.json` (8 files) + `evals/IMPROVEMENT_WORKFLOW.md` |
| Tests | `tests/test_a2a_{server,client,loopback}.py` |
| LLM-judge regression test | `.e2e-private/llm_judge.py` (private, gitignored) |

## Architecture patterns adopted

| Pattern | Source repo |
|---|---|
| Two-CLAUDE.md template + cold-start + bounce-on-placeholder | `anthropics/claude-for-legal` |
| `~~category` placeholders + CONNECTORS.md + Standalone-vs-Supercharged | `anthropics/knowledge-work-plugins` |
| Agent + vertical split + sync.py + 3-tier cookbook | `anthropics/financial-services` |
| Meta-skill recommender | `claude-for-legal/legal-builder-hub` |
| Skill-creator eval workflow | `anthropics/skills` |

## Skill triggering policies (encoded in skill descriptions)

- **Global ambiguity**: single-word inputs route to `advise` for clarification, never to destructive skills
- **Bare verbs without targets** ("update everything", "fix it"): route to `advise`
- **"Jira ticket" disambiguation**: vanilla → `stakeholder-comms`; qualified ("deployment Jira", "CI ticket") → `deploy`
- **Profile gating**: every destructive skill bounces to `cold-start-interview` if profile is unconfigured
- **Provisional mode**: user says "provisional" → continue with generic defaults, tag outputs `[PROVISIONAL]`

## Generate skill — 2-pass pattern (v1.4.0)

`skills/generate/SKILL.md` enforces completeness via:

1. **Pass 1 (Step 3)** — build structured section outline + URL inventory BEFORE writing
2. **Pass 2 (Step 4)** — render in 16-section canonical order
3. **Validation gate (Step 5)** — measurable thresholds (URL count ≥80 for marketplaces, entity facts as bulleted list, every editorial article rendered, 20-50 KB file size)
4. **No-fabrication guardrails** — copy URLs character-for-character from profile; if profile lists N editorial articles, output exactly N (no "for completeness" additions)

## A2A — three-tier implementation

- **Tier 1 (Agent Card)**: `.well-known/agent-card.json` — declares 8 skills, validates against v1.0 spec
- **Tier 2 (Server)**: `scripts/a2a-server.py` — FastAPI JSON-RPC, SQLite tasks, Bearer auth, rate limit, SSE, audit log; `mock` mode (default) + `live` mode (needs `ANTHROPIC_API_KEY`)
- **Tier 3 (Client)**: `scripts/a2a-client.py` — `A2AClient` class + CLI (discover / send / stream / get / cancel / list)

JSON-RPC methods: `message/send`, `message/stream`, `tasks/get`, `tasks/cancel`, `tasks/list`. Default model: `claude-sonnet-4-6`.

## Private test fixtures (gitignored)

Under `.e2e-private/`:
- `input/<client>-bloated.rtf` — ~16 MB bloated RTF source (anti-patterns #1, #16, #17)
- `input/gold-standard-v3.txt` — ~27 KB curated v3 (gold reference for parity testing)
- `profile/CLAUDE.md` — configured TestMarketplace profile (anonymized)
- `harness.py` — runner with `audit | compare | wire` subcommands
- `llm_judge.py` — LLM-graded gold-parity scorer (10 dimensions)
- `live-output/` — generate-live-v1..v4.md (iterative test outputs)

To re-run gold-parity test (requires `ANTHROPIC_API_KEY`):
```bash
python3 .e2e-private/llm_judge.py \
    --live .e2e-private/live-output/<latest>.md \
    --gold .e2e-private/input/gold-standard-v3.txt
```

Target: 10/10 from `claude-sonnet-4-6` judge.

## Honest expectations baseline (the plugin's core stance)

Empirical record on llms.txt's direct impact on AI citations is **null** per three independent studies + Google's John Mueller confirming Google doesn't use it. The plugin **never** promises AI-citation lift. Redirects such requests to higher-leverage investments: schema.org, external citations, content quality, author E-E-A-T.

## Versioning policy

- **Patch** (`x.y.PATCH`): description tweaks, eval additions, doc fixes — no skill-shape changes
- **Minor** (`x.MINOR.0`): new skills, sectors, languages, connectors; A2A tier upgrades; additive guardrails; eval/judge additions
- **Major** (`MAJOR.0.0`): breaking changes to skill IDs, removed skills, manifest schema changes

Run `python3 scripts/sync.py --version-bump` to patch-bump. Manually edit `.claude-plugin/plugin.json` and `.well-known/agent-card.json` for minor/major bumps.

## Recent version history (one-line each)

- **1.4.0** — Generate skill 2-pass pattern; 10/10 LLM-judged gold parity with real Claude
- **1.3.0** — E2E gold-standard test exposed gaps; added anti-patterns #16 (PII), #17 (non-markdown); marketplace mandatory-directives section
- **1.2.0** — Docker + one-click deploy (Render/Fly/Railway) + n8n/LangGraph/CrewAI integration kits
- **1.1.0** — A2A Tier 2 server (production) + Tier 3 client + 42 pytest cases; FastAPI annotation-import bug fixed
- **1.0.0** — Initial release: 8 skills, 18 sectors, 13 languages, A2A Tier 1, agent bundles, cookbook

## Last reviewed

2026-05-23 — v1.4.0 ship; user typed "memory" to trigger Auto Dream consolidation
