# Eval-Driven Improvement Workflow

*How to iteratively improve the llms-txt-advisor plugin using evals + the skill-creator pattern.*

## Why this workflow

Trigger descriptions are the most fragile part of any Claude plugin. As real-world usage surfaces unexpected phrasings, descriptions need iterative refinement. This document captures the workflow used to take this plugin from **87.3% (round 1) → 95.5% (round 2) → 100% (round 3) → 100% on niche cases (round 4)**.

## The four-round pattern (proven on this plugin)

### Round 1 — Baseline measurement

1. Create `evals/<skill>/evals.json` for each skill with 5-10 prompts
2. Categorize each prompt: `positive` (should fire skill), `negative` (should fire different skill), `edge` (boundary case)
3. Run an LLM grader against the prompts (see "How to run evals" below)
4. Document pass rate as the baseline

**Output of Round 1 for this plugin**: 48/55 = 87.3%

### Round 2 — Fix the easy wins

For each FAIL in Round 1:

1. Identify whether it's a **description gap** (skill description doesn't claim the phrase) or **boundary ambiguity** (two skills both claim the phrase)
2. For description gaps: add the missing trigger phrase to the appropriate skill's `description:` field
3. For boundary ambiguities: add explicit "use X instead if..." redirect language to both skills

**Common Round 2 fixes** applied to this plugin:
- Added "make me an llms.txt" trigger to `generate`
- Strengthened cold-start vs setup-recommender boundary with explicit redirect language
- Added "first time" / "for the first time" triggers to cold-start

**Output of Round 2**: 6/7 previously-failing now PASS → ~95.5%

### Round 3 — Move disambiguation into descriptions

For boundary ambiguities that survived Round 2, the fix is usually that disambiguation lives in the skill body but not in the description Claude reads at trigger time.

For each surviving FAIL:

1. Move disambiguation from skill body to description
2. Make one skill the **explicit default** for vanilla phrasing
3. Make the other skill **only fire on qualified variants**

**Round 3 fix applied to this plugin**:
- `deploy`: now only fires on "deployment Jira", "CI ticket", "ops ticket" (qualified)
- `stakeholder-comms`: now explicit default for "write the Jira ticket description" (vanilla)
- Both skills' descriptions explicitly redirect ambiguous cases

**Output of Round 3**: 12/12 = 100%

### Round 4 — Niche / edge case stress testing

Once core eval passes 100%, probe boundaries with:

- Multilingual inputs (Japanese, Turkish, Arabic, etc.)
- Adversarial inputs (prompt injection probes)
- Ambiguous boundaries (single-word inputs, bare verbs without targets)
- Off-topic requests (skill should refuse)
- Cross-axis combinations (sector × language × connector)

**Round 4 fixes applied to this plugin**:
- Added "ambiguity policy" sections to descriptions (bare verbs → advise, not destructive skills)
- Added explicit "update everything" / "fix the whole thing" examples to advise's disambiguation list
- Added multilingual-intent matching note to cold-start

**Output of Round 4**: 11/11 = 100% on niche cases

## How to run evals

### Option A: Manual LLM grading (used in this plugin's development)

Spawn a sub-agent acting as the grader:

```
For each prompt:
1. Read the skill descriptions
2. Predict which skill Claude would route the prompt to
3. Compare to expected
4. Mark PASS or FAIL with reasoning
```

This is what's documented in `optimization-results.md`. It's lightweight, doesn't require API credentials, and surfaces failures with explanations.

### Option B: Automated via anthropic-skills:skill-creator

Once the skill-creator skill is available in your Claude Code instance:

```
/anthropic-skills:skill-creator
> "Run evals on the llms-txt-advisor plugin using the evals/ directory"
```

The skill-creator runs each prompt in parallel sub-agents (with-skill vs baseline), uses an LLM grader, and produces a benchmark report.

For description optimization specifically:

```bash
python -m scripts.run_loop \
    --eval-set evals/<skill>/evals.json \
    --skill-path skills/<skill> \
    --max-iterations 5
```

This iteratively refines descriptions until the pass rate stops improving.

## When to re-run evals

| Trigger | Action |
|---|---|
| New skill added to the plugin | Add evals/<new-skill>/evals.json + re-run full eval |
| User reports a miscategorization in production | Add the misrouting case to the relevant evals.json + re-run |
| Description edited | Re-run evals for that skill + adjacent skills it competes with |
| Quarterly review | Re-run full eval + niche-case stress test |
| New language or sector added | Add cross-axis cases to evals + verify no regressions |

## Common patterns that emerge

After four rounds of refinement on this plugin, here are the patterns that consistently improve trigger accuracy:

### Pattern 1: Explicit trigger phrases

Include the exact user phrasings as trigger lists in descriptions:

```
description: >
  Use when the user says "do X", "perform Y", "request Z".
```

### Pattern 2: Negative triggers (explicit redirects)

For skill pairs that compete on similar phrasings:

```
description: >
  ...
  Use OTHER_SKILL instead if the user [specific condition].
```

### Pattern 3: Qualified vs vanilla phrasing

For skills competing on a noun:

```
deploy description: "fires on 'deployment ticket', 'CI ticket' (qualified)"
stakeholder-comms description: "default for vanilla 'write the ticket' phrasings"
```

### Pattern 4: Ambiguity policy section

Add to descriptions explicitly:

```
**Ambiguity policy**: bare verbs without targets do NOT route here — they
go to `advise` for disambiguation. Single-word inputs ("help") also route
to `advise`, not to destructive skills.
```

### Pattern 5: Multilingual intent matching

```
**Multilingual matching**: trigger phrases match by intent across languages —
Japanese "プロフィールを設定", Spanish "configura mi perfil", etc. all match
"configure my profile" intent. Match semantic meaning, not literal English
tokens.
```

## Anti-patterns to avoid

### Don't pile every paraphrase into the description

Descriptions are capped at 1,536 chars in the skill listing. Be ruthless about which trigger phrases survive — keep only the ones that pull weight.

### Don't make every skill claim ambiguous phrases

If skill A and skill B both claim "update", routing is broken. Pick one as the default; make the other fire only on qualified variants.

### Don't put disambiguation only in the skill body

The body is loaded after triggering. Descriptions are read at trigger time. Disambiguation must live in the description to actually route.

### Don't grade the eval leniently

If the LLM grader is generous, you'll deploy false confidence. The grading agent in our workflow is instructed: *"Be honest and rigorous. Don't grade leniently. Predict what Claude would actually do, not what would be ideal."*

## Specific anti-patterns we encountered and fixed

1. **"Jira ticket" double-claim** — both deploy and stakeholder-comms claimed it. Fix: stakeholder-comms owns vanilla; deploy owns "deployment/CI/ops" qualified variants only.
2. **"Set up the plugin" double-claim** — cold-start and setup-recommender both claimed it. Fix: cold-start owns "set up + profile" / "set up + first time" (commitment); setup-recommender owns "I just installed" (orientation).
3. **Bare "update my llms.txt"** — customize was too greedy. Fix: customize requires a named target; bare verbs go to advise.
4. **Single-word "help"** — could route anywhere. Fix: global ambiguity policy in advise + explicit "do NOT route here" in destructive skills.

## Measuring improvement

Track these metrics over time:

| Metric | Target | Current |
|---|---|---|
| Trigger eval pass rate (canonical 55 prompts) | ≥ 95% | 100% |
| Niche-case eval pass rate (23 stress prompts) | ≥ 95% | 100% |
| Cross-axis matrix coverage (10 scenarios) | ≥ 9/10 fully PASS | 10/10 (after composition guidance added) |
| Mean confidence per pass | HIGH | HIGH |
| Number of "ambiguous" boundary cases | < 5 | 0 |

Re-measure quarterly. When the eval prompts no longer reflect real usage, refresh them.

## Cross-references

- `README.md` — eval methodology overview
- `optimization-results.md` — per-skill analysis from Rounds 1-3
- Individual `<skill>/evals.json` files — the eval prompts themselves
- `../VALIDATION_REPORT.md` — full validation including all eval rounds
