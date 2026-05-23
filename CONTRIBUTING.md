# Contributing to llms-txt-advisor

Guide for extending and improving the plugin.

## Quick reference

```bash
python3 scripts/check.py                   # Validate plugin structure (run before any commit)
python3 scripts/sync.py --check            # Detect drift between source skills and bundles
python3 scripts/sync.py --sync             # Propagate source changes to bundles
python3 scripts/sync.py --version-bump     # Patch-bump plugin.json version
python3 scripts/check.py --self-install    # Install pre-commit hook
bash scripts/deploy-managed-agent.sh staleness-watcher  # Cookbook dry-run
```

## Before you commit

Make sure the pre-commit hook is installed:

```bash
python3 scripts/check.py --self-install
```

This runs both `check.py` and `sync.py --check` on every commit. If either fails, the commit is blocked.

If you bypass the hook (`git commit --no-verify`), run validation manually first.

## Repo conventions

| Convention | Why |
|---|---|
| `SKILL.md` files live ONLY inside `skills/<name>/` | Anthropic skill convention — root SKILL.md is reserved and would be confusing |
| Frontmatter `description` ≤ 1536 chars | Skill listing truncates beyond this |
| SKILL.md body ≤ 500 lines (target: ≤ 300) | Anthropic guidance — move detail to `references/` |
| Cross-references use relative paths | Survive plugin install/symlink |
| Markdown link checker via `check.py` | Catches broken refs at commit time |
| Source-of-truth in `skills/` | Bundles in `agent-bundles/` are vendored copies, never edit there |
| Plugin.json version pinned to `1.0.0` until next release | Use `sync.py --version-bump` for patch bumps |

## How to extend

### Add a new sector

15 minutes.

1. Create `knowledge/sectors/<sector-name>.md` modeled on an existing one (e.g., `knowledge/sectors/healthcare.md` is a good template for regulated industries; `knowledge/sectors/marketplace.md` for multi-vendor sites).

2. The sector file must include:
   - **Decision default** (Ship / Skip / Selective)
   - **Distinctive concerns** (regulatory, technical, audience)
   - **Mandatory directives block additions** (text to splice into the For-AI-Systems block)
   - **Recommended structure** (sections to include)
   - **Connector synergies** (which `~~categories` matter most)
   - **Honest expectations** (what llms.txt will and won't do for this sector)
   - **Schema.org for [sector]** (which JSON-LD types apply)
   - **Template pointer** (which file in `templates/` to use as base)
   - **Cross-references** at the bottom

3. Update `knowledge/sectors/_router.md`:
   - Add to the classification table
   - Add to the decision defaults table
   - If layered (e.g., proptech marketplace = real-estate × marketplace), add to the composition matrix

4. Run `python3 scripts/check.py` to validate. No drift detected = success.

5. Add eval prompts for routing:
   ```
   evals/<some-relevant-skill>/evals.json:
   - "I run a [sector] site — should I ship llms.txt?" → expected: advise
   - "Generate llms.txt for our [sector] site" → expected: generate
   ```

### Add a new language

15 minutes.

1. Create `knowledge/languages/<code>.md` (ISO 639-1 lowercase, e.g., `pl`, `vi`, `hi`).

2. Copy structure from an existing language file (`knowledge/languages/de.md` is a good template for European languages with formal/informal distinction; `knowledge/languages/ja.md` for honorific-heavy languages).

3. Required sections:
   - Formality calibration table (context → form of address)
   - Honorifics (with examples)
   - Formal vs informal form (with verb conjugation table)
   - Common business email phrases table (purpose → phrase)
   - Closing patterns table (formality → closing)
   - Honest-expectations opening (translated)
   - Three-reasons framing (translated)
   - Date and number formats
   - Cultural notes (5-10 bullets)
   - [Optional] Language-specific llms.txt concerns (regulatory, technical, scripts)

4. Update `knowledge/languages/_router.md`:
   - Add to the "Available language files" table

5. Run `python3 scripts/check.py` to validate.

6. (Optional) Add a cross-axis eval scenario that exercises the new language with a sector.

### Add a new skill

1-2 hours plus evals.

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: >
     One paragraph describing what triggers this skill (specific trigger phrases),
     what it does, what it produces, and when NOT to use it (negative triggers
     or redirect to other skills). Aim for 800-1200 chars. The first 200 chars
     are the most important — they appear in skill listings.
   argument-hint: "[--flag-1] [--flag-2 <value>]"
   ---

   # Skill Name

   ## What this skill does
   ...

   ## Step 1 — Profile check
   Read `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`.
   Bounce to /llms-txt-advisor:cold-start-interview if [PLACEHOLDER] markers present.

   ## Step 2 — ...
   ```

2. If the skill grows beyond ~300 lines, create `skills/<skill-name>/references/` and move deep-dive content there.

3. Add `evals/<skill-name>/evals.json`:
   ```json
   {
     "skill": "skill-name",
     "purpose": "Trigger evaluation for...",
     "prompts": [
       {
         "id": "<short-prefix>-001",
         "type": "positive",
         "input": "user phrasing that should trigger this skill",
         "expected_skill": "skill-name",
         "rationale": "why"
       },
       {
         "id": "<short-prefix>-002",
         "type": "negative",
         "input": "user phrasing that should NOT trigger (should fire different skill)",
         "expected_skill": "<other-skill-name>",
         "rationale": "why"
       }
     ]
   }
   ```

4. Update `.well-known/agent-card.json` to declare the new skill as an `AgentSkill`:
   ```json
   {
     "id": "skill-name",
     "name": "Skill Name",
     "description": "...",
     "inputModes": ["text/plain"],
     "outputModes": ["text/markdown"],
     "examples": ["..."],
     "tags": ["..."]
   }
   ```

5. Update `README.md` skill catalog table.

6. If the skill should be bundled in `llms-txt-bootstrap` or `llms-txt-migration`:
   ```bash
   mkdir agent-bundles/<bundle>/skills/<skill-name>
   python3 scripts/sync.py --sync
   ```

7. Run the eval-driven improvement workflow (see `evals/IMPROVEMENT_WORKFLOW.md`).

### Add a new connector category

5 minutes.

1. Edit `CONNECTORS.md`:
   - Add row to the category table with `~~category-name`, included servers (if pre-configured), and other options
   - Include Western, Asian, and Russian vendor examples where applicable
   - Add row to the degradation matrix
   - Add row to the per-sector recommendations matrix

2. Edit `.mcp.json`:
   - Add the connector to `mcpServers` with empty URL: `"<name>": { "type": "http", "url": "" }`
   - Add to `recommendedCategories`

3. Reference the new placeholder in relevant skill SKILL.md files where useful.

4. Run `python3 scripts/check.py`.

### Add a new agent bundle

```bash
# Scaffold
python3 scripts/sync.py --add-agent-bundle <bundle-name>

# Add skill marker subdirectories for each skill to bundle
mkdir agent-bundles/<bundle-name>/skills/<skill-1>
mkdir agent-bundles/<bundle-name>/skills/<skill-2>
# ... etc

# Populate from source
python3 scripts/sync.py --sync

# Verify
python3 scripts/sync.py --check
```

Bundles are **vendored copies** of source skills. NEVER edit `agent-bundles/*/skills/*/SKILL.md` directly — edit the source in `skills/<name>/SKILL.md` and re-sync.

### Add a new managed-agent cookbook

```bash
mkdir managed-agent-cookbooks/<cookbook-name>
mkdir managed-agent-cookbooks/<cookbook-name>/subagents
```

Required files (model on `managed-agent-cookbooks/staleness-watcher/`):

- `agent.yaml` — orchestrator manifest with `name`, `model`, `system.file` reference, `tools`, `mcp_servers`, `callable_agents`, `skills`
- `README.md` — explain what the cookbook does, the security model, deployment steps
- `subagents/*.yaml` — for each sub-agent: name, description, system prompt, tools (constrained), output_schema with regex-bounded fields

Apply the three-tier security split for any cookbook that touches untrusted external content:
- Tier 1 (reader): Read+Grep+Bash only, NO MCP, NO Write, schema-validated JSON output
- Tier 2 (analyzer): trusted MCP read, NO Write, no arbitrary URL fetching
- Tier 3 (writer): ONLY tier with Write, NO raw external content, output paths regex-constrained

Test with:
```bash
bash scripts/deploy-managed-agent.sh <cookbook-name>
```

## The eval-driven improvement workflow

See `evals/IMPROVEMENT_WORKFLOW.md` for the proven 4-round pattern (87.3% → 100% on this plugin):

1. **Round 1**: baseline measurement
2. **Round 2**: fix easy wins (description gaps, boundary ambiguity)
3. **Round 3**: move disambiguation INTO descriptions (not just bodies)
4. **Round 4**: niche/edge case stress test

Common patterns that improve trigger accuracy:

1. **Explicit trigger phrases** — list user phrasings verbatim in descriptions
2. **Negative triggers** — explicit redirects ("Use OTHER_SKILL instead if...")
3. **Qualified vs vanilla phrasing** — one skill owns vanilla, the other owns qualified
4. **Ambiguity policy** — single-word inputs go to advise, never to destructive skills
5. **Multilingual intent matching** — semantic, not literal, trigger matching

Anti-patterns to avoid:

1. Piling every paraphrase into description (1536 char limit)
2. Multiple skills claiming the same ambiguous phrase
3. Disambiguation in skill body but not description
4. Lenient eval grading (false confidence)

## A2A protocol contributions

A2A Tier 2 (server) and Tier 3 (client) are already implemented — see `scripts/a2a-server.py` and `scripts/a2a-client.py`, with the full guide in [`A2A.md`](A2A.md). To extend them:

1. To add capabilities to `scripts/a2a-server.py`:
   - Add a new JSON-RPC method handler in `build_app()` (follow the pattern of `_do_tasks_list`)
   - Add a corresponding test in `tests/test_a2a_server.py`
   - Document the method in `A2A.md`

2. Update `.well-known/agent-card.json`:
   - Replace `url` placeholder with actual endpoint
   - Update `_implementationStatus` to reflect Tier 2 deployed
   - Add real `securitySchemes`

3. Update `A2A.md` deployment section.

4. Add A2A integration tests.

See `A2A.md` for the full Tier 2 / Tier 3 specifications.

## Submitting changes

1. Run validations:
   ```bash
   python3 scripts/check.py
   python3 scripts/sync.py --check
   bash scripts/deploy-managed-agent.sh staleness-watcher  # if cookbook changed
   ```

2. If you added/changed a skill, run the eval-driven optimization at least 2 rounds.

3. Update relevant documentation:
   - `README.md` if skill catalog changed
   - `CHANGELOG.md` with the change
   - `.well-known/agent-card.json` if skills changed
   - `evals/<skill>/evals.json` if descriptions changed

4. Bump the version:
   - Patch (`x.y.PATCH`): `python3 scripts/sync.py --version-bump`
   - Minor (`x.MINOR.0`): manually edit `.claude-plugin/plugin.json`
   - Major (`MAJOR.0.0`): only for breaking changes

5. The pre-commit hook will validate. If it fails, fix and re-commit.

## Style conventions

- **Tone**: honest, evidence-based, refuses to over-promise. Match the existing voice.
- **Empirical citations**: when making claims about AI behavior, cite the three primary studies (SE Ranking n=300k, OtterlyAI 90-day, Search Engine Land 10-site). Don't invent numbers.
- **Cross-cultural communication**: respect the language-specific conventions documented in `knowledge/languages/`. Don't translate honorifics into role titles or vice-versa.
- **No emojis in skill descriptions** — they consume the 1536-char budget.
- **Markdown**: prefer tables for structured info, code blocks for examples, headers for navigation. Avoid HTML.
- **File names**: lowercase-with-hyphens for skills/sectors/languages; SCREAMING_SNAKE.md only for top-level conventional files (README, LICENSE, CHANGELOG, CONTRIBUTING).

## Questions

- Architecture / patterns: see the architecture-inspiration table in `README.md` for the upstream Anthropic repos this plugin learns from
- Specific skill behavior: read the SKILL.md and its `references/` subdirectory
- Empirical claims: see `reference/sources.md` for the bibliography
- A2A: see `A2A.md`
- Cookbook: see `managed-agent-cookbooks/staleness-watcher/README.md`
- Evals: see `evals/IMPROVEMENT_WORKFLOW.md`
