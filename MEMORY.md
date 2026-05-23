# MEMORY.md — llms-txt-ops

*Project memory for future Claude sessions. Curated per the Auto Dream protocol. Keep under 200 lines.*

## What this repo is

A Claude Code plugin (`llms-txt-advisor`) for advising websites on whether/how to ship an `llms.txt` file. Honest framing: three independent empirical studies show **null AI-citation impact**. Defensible use cases are narrow: developer docs, internal RAG grounding, replacing bloated existing files.

Distributed as: standalone plugin, two agent bundles (bootstrap + migration), managed-agent cookbook (staleness-watcher with 3-tier security split), and an A2A v1.0 server (callable from anywhere — Docker/Render/Fly/Railway one-click ready).

**Public on GitHub**: https://github.com/ali-saadat/llms-txt-ops — dual-license model (v2.0.0+): PolyForm Noncommercial 1.0.0 for non-commercial use, paid commercial license required for any for-profit use (see `COMMERCIAL.md`). Code at commit `5eb4ae4` or earlier remains MIT in frozen form. CI green.

## Critical user constraints (preserve verbatim)

1. **Never name the private test client or its industry in committed files.** Real-world test fixtures live under `.e2e-private/` (gitignored). All examples in the public repo use anonymized "ExampleMart" / generic marketplace language. Specific industry verticals from private fixtures are also kept out of committed examples (no "wedding", no "dugun", etc.).
2. **Language policy is end-user-driven.** llms.txt file content default = English. Stakeholder communication + conversation tone = match user's typing language. Native-primary mode for non-English-primary sites (Turkish headings + descriptions, English directives block).
3. **No AI attribution in commits.** Inherits from global rule.

## Current state (v1.4.0 + SOTA refinement, 2026-05-23)

| Aspect | Value |
|---|---|
| Plugin version | 1.4.0 (+ SOTA refinement at commit `5eb4ae4`) |
| GitHub | `ali-saadat/llms-txt-ops` — 9 commits, all CI green (latest run: success) |
| Tracked files | 174 |
| Root .md docs | 12 (README, USER_GUIDE, A2A, CHANGELOG, CLAUDE, CONNECTORS, CONTRIBUTING, INDEX, INTEGRATIONS, MEMORY, SECURITY, VALIDATION_REPORT) |
| Scripts | 7 (check.py, sync.py, deploy-managed-agent.sh, a2a-server.py, a2a-client.py, refine.py, post_processors.py) |
| Skills | 8 user-invocable + 12 progressive-disclosure references |
| Anti-patterns | 17 documented (added #16 PII leakage, #17 non-markdown in v1.3.0) |
| Sectors | 18 + composition router |
| Languages | 13 + end-user-driven policy router |
| Agent bundles | 2 (bootstrap, migration) — sync'd via sync.py |
| Cookbooks | 1 (staleness-watcher, 3-tier security split) |
| A2A | Tier 1 live + Tier 2 implemented + Tier 3 implemented |
| Tests | 42 pytest passing |
| Trigger evals | 94 prompts (61 production + 23 niche + 10 cross-axis), 100% pass |
| Gold-parity score (post-SOTA-refinement) | **9.40 peak** (gold avg: 9.55; within judge noise) |

## Validation chain (run before any commit; pre-commit hook auto-runs check.py + sync.py)

```bash
python3 scripts/check.py            # 42 PASS, 0 WARN, 0 FAIL
python3 scripts/sync.py --check     # no drift between skills/ and agent-bundles/*/skills/
python3 -m pytest tests/ -q         # 42 pytest cases
bash scripts/deploy-managed-agent.sh staleness-watcher  # cookbook dry-run
```

## Docker e2e (verified working end-to-end)

```bash
# 1. Create .env (gitignored). IMPORTANT: shell-exported empty vars override .env;
#    if shell has ANTHROPIC_API_KEY="" exported, run `unset ANTHROPIC_API_KEY` first.
cat > .env <<EOF
A2A_MODE=live
ANTHROPIC_API_KEY=sk-ant-...
A2A_API_KEYS=local-test=\$(openssl rand -hex 32)
EOF

# 2. Build + run
docker compose up -d

# 3. Tier 3 client → Tier 2 server → real Claude
A2A_BEARER=$(grep '^A2A_API_KEYS=' .env | cut -d= -f3) \
python3 scripts/a2a-client.py http://localhost:8000 send --skill advise --text "..."
```

## SOTA refinement pipeline (closes last 5-10% to gold)

`scripts/refine.py` orchestrates: **Best-of-N candidate generation → judge selection → Self-Refine critique-revise loop → deterministic post-processing → final judge**.

```bash
python3 scripts/refine.py \
    --base-url http://localhost:8000 --bearer "$A2A_BEARER" \
    --skill generate --text-file profile.md --output refined.md \
    --n-candidates 3 --max-iterations 2 --target-score 9.5 \
    --iso-date 2026-05-23 --allowed-domain example.com
```

Cost: ~9-11 API calls (~$1.50-2.00) per refined generation. Empirical: lifts 8.62 baseline → 9.40 peak (within judge noise of gold's 9.55).

References for the techniques used: Self-Refine (Madaan 2023, arXiv:2303.17651), Best-of-N + Self-Certainty (arXiv:2502.18581), Constitutional AI (Anthropic 2026), deterministic post-processing (standard agent pattern). Full catalog at `knowledge/09-quality-refinement.md`.

## Key paths

| Purpose | Path |
|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Marketplace plugins | `.claude-plugin/marketplace.json` |
| MCP connector config | `.mcp.json` |
| A2A Agent Card (Tier 1) | `.well-known/agent-card.json` |
| A2A Tier 2 server | `scripts/a2a-server.py` (per-skill max_tokens: generate=16K, audit=8K, advise=4K, etc.) |
| A2A Tier 3 client | `scripts/a2a-client.py` |
| **SOTA refinement orchestrator** | `scripts/refine.py` |
| Deterministic post-processors | `scripts/post_processors.py` |
| Profile template | `CLAUDE.md` → user copies to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` |
| Skills source of truth | `skills/` (propagated to `agent-bundles/*/skills/` via `sync.py`) |
| Knowledge corpus | `knowledge/01..09-*.md` + `knowledge/sectors/` + `knowledge/languages/` |
| Empirical evidence | `knowledge/02-empirical-evidence.md` (SE Ranking n=300k, OtterlyAI 90d, Search Engine Land) |
| Anti-patterns | `knowledge/07-failure-modes.md` (17 documented) |
| Quality refinement techniques | `knowledge/09-quality-refinement.md` (SOTA citations + usage) |
| Eval suite | `evals/*/evals.json` (8 files) + `evals/IMPROVEMENT_WORKFLOW.md` |
| Pytest tests | `tests/test_a2a_{server,client,loopback}.py` |
| Platform deploy configs | `render.yaml`, `fly.toml`, `railway.json` (must be at REPO ROOT, not in deploy/) |
| GitHub Actions CI | `.github/workflows/validate.yml` (Node 24 opt-in) |
| Private gold-parity judge | `.e2e-private/quality_judge.py` (gitignored) |
| Private LLM judge (10-dim) | `.e2e-private/llm_judge.py` (gitignored) |

## Architecture patterns adopted

| Pattern | Source repo |
|---|---|
| Two-CLAUDE.md template + cold-start + bounce-on-placeholder | `anthropics/claude-for-legal` |
| `~~category` placeholders + CONNECTORS.md + Standalone-vs-Supercharged | `anthropics/knowledge-work-plugins` |
| Agent + vertical split + sync.py + 3-tier cookbook | `anthropics/financial-services` |
| Meta-skill recommender | `claude-for-legal/legal-builder-hub` |
| Skill-creator eval workflow | `anthropics/skills` |

## Skill triggering policies (encoded in skill descriptions)

- **Global ambiguity**: single-word inputs → `advise` for clarification, never to destructive skills
- **Bare verbs without targets** ("update everything", "fix it") → `advise`
- **"Jira ticket" disambiguation**: vanilla → `stakeholder-comms`; qualified ("deployment Jira", "CI ticket") → `deploy`
- **Profile gating**: every destructive skill bounces to `cold-start-interview` if profile is unconfigured
- **Provisional mode**: user says "provisional" → continue with generic defaults, tag outputs `[PROVISIONAL]`

## Private test fixtures (gitignored)

Under `.e2e-private/`:
- `input/<client>-bloated.rtf` — ~16 MB bloated RTF source (real-world test material)
- `input/gold-standard-v3.txt` — ~27 KB curated v3 (gold reference)
- `profile/CLAUDE.md` — configured TestMarketplace profile (anonymized)
- `harness.py` — runner with `audit | compare | wire` subcommands
- `llm_judge.py` — structural 10-dimension gold-parity scorer
- `quality_judge.py` — content-quality 8-dimension scorer (1-10 scale, not pass/fail)
- `live-output/` — iterative test outputs (refined-aligned.md is the gold-parity champion)

## Honest expectations baseline (the plugin's core stance)

Empirical record on llms.txt's direct impact on AI citations is **null** per three independent studies + Google's John Mueller confirming Google doesn't use it. The plugin **never** promises AI-citation lift. Redirects such requests to higher-leverage investments: schema.org, external citations, content quality, author E-E-A-T.

## Versioning policy

- **Patch**: description tweaks, eval additions, doc fixes — no skill-shape changes
- **Minor**: new skills, sectors, languages, connectors; A2A tier upgrades; additive guardrails; eval/judge additions
- **Major**: breaking changes to skill IDs, removed skills, manifest schema changes

`python3 scripts/sync.py --version-bump` to patch-bump. Manually edit `plugin.json` + `agent-card.json` for minor/major bumps.

## Recent version history (one-line each)

- **1.4.0** + SOTA refinement (commit `5eb4ae4`) — refine.py + post_processors.py + knowledge/09; 9.40 peak gold-parity
- **1.4.0** — Generate skill 2-pass pattern, gold-parity verified
- **1.3.0** — E2E gold-standard test; added anti-patterns #16 (PII), #17 (non-markdown); marketplace mandatory-directives section
- **1.2.0** — Docker + one-click deploy (Render/Fly/Railway) + n8n/LangGraph/CrewAI integration kits
- **1.1.0** — A2A Tier 2 server (production) + Tier 3 client + 42 pytest cases
- **1.0.0** — Initial release: 8 skills, 18 sectors, 13 languages, A2A Tier 1, agent bundles, cookbook

## Gitignore state (verified 2026-05-23)

The `.gitignore` excludes (in addition to standard Python/IDE noise):
- `.env` (with `!.env.example` allowed) — secrets
- `.e2e-private/` — private test fixtures
- `llms-txt-advisor.local.md` (with `!llms-txt-advisor.local.md.example`) — user-specific profile overrides
- `a2a-tasks.db*`, `a2a-audit.log` — A2A server runtime artifacts (when running locally outside Docker)

## Last reviewed

2026-05-23 — repo state verified after SOTA refinement ship (commit `5eb4ae4`); 174 tracked files; 9 commits; CI green; memory consolidation requested again, drift-corrected and timestamp refreshed
