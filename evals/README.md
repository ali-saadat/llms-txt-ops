# Skill Evals

*Trigger-detection evaluations for each skill. Used to validate that descriptions correctly route user inputs to the right skills.*

## Structure

Each skill has its own subdirectory with an `evals.json` containing 5-10 test prompts categorized as:

- **positive** — the input should fire this skill
- **negative** — the input should fire a different skill
- **edge** — boundary case, may go either way but expected resolution is documented

## How to run evals

### Manual approach (lightweight)

For each prompt in `evals.json`:

1. In a clean Claude Code session with the plugin installed, type the input
2. Observe which skill (if any) Claude invokes
3. Compare to `expected_skill`
4. Mark PASS / FAIL

Useful for spot-checks. Not parallelizable.

### Automated approach (anthropic-skills:skill-creator)

The `anthropic-skills:skill-creator` skill includes evaluation infrastructure that:

1. Runs each prompt in parallel subagents (with-skill vs baseline)
2. Grades the output via an LLM grader
3. Aggregates results into a benchmark report

To use:

```
/anthropic-skills:skill-creator
> "Run evals on the llms-txt-advisor plugin skills using the evals/ directory"
```

The skill-creator will:
- Discover the evals/<skill>/evals.json files
- Run with-skill vs without-skill comparisons
- Produce a grading report
- Suggest description improvements

### Description optimization loop

From the `skill-creator` skill:

```bash
python -m scripts.run_loop \
    --eval-set evals/<skill>/evals.json \
    --skill-path skills/<skill> \
    --max-iterations 5
```

This iteratively tunes the `description:` field in `SKILL.md` frontmatter to maximize trigger accuracy.

## What good evals look like

- **Positive cases** — paraphrases of the trigger phrases in the description
- **Negative cases** — phrases that LOOK relevant but should route to a different skill
- **Edge cases** — boundary situations (e.g., user has both existing file AND wants new setup)
- **Diverse phrasing** — formal, casual, technical, non-English
- **Real-world wording** — what users actually say, not what specs say

## Eval-driven description improvement

After running evals, common issues and fixes:

| Issue | Cause | Fix in description |
|---|---|---|
| Positive case doesn't trigger | Description too narrow | Add the paraphrase as a trigger phrase |
| Negative case wrongly triggers | Description too broad | Add explicit "do NOT use for" clause |
| Edge case ambiguous | Decision rule unclear | Document the edge case explicitly |
| Multiple skills compete | Overlapping descriptions | Disambiguate by use case |

## Skill descriptions — quality checklist

A good description (per Anthropic guidance, frontmatter ≤1536 chars):

- [ ] Opens with concrete first sentence ("Use this skill when...")
- [ ] Lists 5-10 specific trigger phrases users actually say
- [ ] Includes the skill's distinctive scope (what it does vs what it doesn't)
- [ ] Has explicit "do NOT use this skill for X" clause
- [ ] Mentions what the skill outputs / produces
- [ ] Empirical-evidence anchor if applicable (e.g., "grounded in three independent studies")

## Current eval coverage

| Skill | Eval prompts | Positive | Negative | Edge |
|---|---|---|---|---|
| cold-start-interview | 8 | 4 | 3 | 1 |
| advise | 7 | 4 | 2 | 1 |
| audit | 8 | 5 | 2 | 1 |
| generate | 7 | 4 | 2 | 1 |
| customize | 7 | 4 | 2 | 1 |
| deploy | 8 | 5 | 2 | 1 |
| stakeholder-comms | 8 | 5 | 2 | 1 |
| setup-recommender | 8 | 5 | 2 | 1 |

Total: 61 trigger evals.

## Adding new evals

When you observe a real-world prompt that misroutes:

1. Add the prompt to `evals/<skill>/evals.json`
2. Mark whether it's positive / negative / edge for the expected skill
3. If it's a recurring miscategorization, update the skill description
4. Re-run evals to confirm fix

## Cross-references

- Each skill's `SKILL.md` — the description being evaluated
- `../scripts/check.py` — validates evals.json schema
- `anthropic-skills:skill-creator` — the eval runner (from the Anthropic skills repo)
- Reference: [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
