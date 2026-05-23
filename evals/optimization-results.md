# Description Optimization Analysis

*Manual analysis of each skill's `description:` frontmatter against its evals. Identifies likely false-positive triggers, false-negative misses, and refinement suggestions. Run periodically; re-run when adding new eval prompts.*

## Optimization methodology

For each skill, we check:

1. **Coverage of positive triggers** — does the description contain phrases that would make Claude route to this skill for each positive case?
2. **Disambiguation from related skills** — does the description make it clear when NOT to use this skill?
3. **Trigger-phrase density** — are the most common user phrasings included?
4. **Length** — under 1536 chars (frontmatter truncation point)?

Then refine the description based on findings.

## Per-skill analysis

### cold-start-interview

**Current description excerpt**: *"...Use on first use of the plugin, when CLAUDE.md is missing or still contains [PLACEHOLDER] markers, or when the user says 'set up the plugin', 'configure llms-txt advisor', 'onboard me', 'let's get started', 'I don't have an llms.txt yet', 'help me create my first llms.txt', 'we want to start fresh', 'we don't have llms.txt', or 'where do I begin'..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| cs-001 "I just installed... how do I set it up?" | cold-start | ✓ ("set up the plugin") |
| cs-002 "I don't have an llms.txt yet... where do I start?" | cold-start | ✓ ("I don't have an llms.txt yet" + "where do I begin") |
| cs-003 "onboard me" | cold-start | ✓ (exact phrase) |
| cs-004 "Let's configure this plugin..." | cold-start | ✓ ("configure llms-txt advisor") |
| cs-005 (negative — audit) | audit | should NOT fire cold-start; description doesn't claim review/audit |
| cs-006 (negative — generate) | generate | should NOT fire cold-start; description focuses on setup |
| cs-007 "We want to start fresh..." | cold-start | ✓ ("we want to start fresh") |
| cs-008 (negative — advise) | advise | should NOT fire cold-start; description doesn't claim research/general |

**Result**: PASS. No refinement needed.

### advise

**Current description excerpt**: *"Main router skill for llms.txt advisory questions. Use when the user asks general questions about llms.txt — 'should I add llms.txt', 'is llms.txt worth it', 'what does llms.txt do', 'explain llms.txt to my team', 'what's the SOTA on llms.txt'..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| ad-001 "Should we add llms.txt..." | advise | ✓ (close to "should I add llms.txt") |
| ad-002 "Is llms.txt actually worth it..." | advise | ✓ (exact paraphrase) |
| ad-003 "What does llms.txt do?" | advise | ✓ (exact phrase) |
| ad-004 "What's the SOTA on llms.txt in 2026?" | advise | ✓ (exact phrase) |
| ad-005 (negative — generate) | generate | should route to generate; advise description says routing |
| ad-006 (negative — cold-start) | cold-start | should route to cold-start; advise description says routing |
| ad-007 "I'm not sure if we even need this..." | advise | ✓ (uncertainty → advise) |

**Result**: PASS. No refinement needed.

### audit

**Current description excerpt**: *"Review an existing llms.txt file... Use when the user says 'review my llms.txt', 'audit our file', 'what's wrong with my llms.txt', 'check this llms.txt', 'is our llms.txt any good'..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| au-001 "Review my llms.txt..." | audit | ✓ (exact phrase) |
| au-002 "Audit our file" | audit | ✓ (exact phrase) |
| au-003 "Is our llms.txt any good?" | audit | ✓ (exact phrase) |
| au-004 "What's wrong with my llms.txt?" | audit | ✓ (exact phrase) |
| au-005 "Check this llms.txt file" | audit | ✓ (exact phrase) |
| au-006 (negative — generate) | generate | should route to generate; "from scratch" is not in audit desc |
| au-007 (negative — customize) | customize | should route to customize; "update the SEO routing section" is targeted |
| au-008 "[pastes 12MB file] thoughts?" | audit | ✓ — large file with "thoughts" implies review |

**Result**: PASS. No refinement needed.

### generate

**Current description**: *"Generate a new llms.txt file from scratch... Use when the user says 'create our llms.txt', 'generate llms.txt', 'draft a file for us', 'build the llms.txt', or after /audit recommends regeneration..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| gn-001 "Generate the llms.txt file" | generate | ✓ |
| gn-002 "Create our llms.txt now" | generate | ✓ |
| gn-003 "Draft an llms.txt for us..." | generate | ✓ |
| gn-004 "Build the llms.txt with audit fixes applied" | generate | ✓ ("--from-audit pathway") |
| gn-005 (negative — audit) | audit | should route to audit |
| gn-006 (negative — cold-start) | cold-start | should route to cold-start |
| gn-007 "Make me an llms.txt" | generate | **possibly weak** — "make" is not in the description |

**Refinement needed**: add "make" as a trigger word for generate.

### customize

**Current description**: *"Update a specific section of the user's practice profile or an existing llms.txt file. Use when the user wants to refine without re-running the full cold-start interview — 'update the SEO routing', 'add more cities to the city list', 'fix the directives block', 'tweak the transactional guidance'..."*

**Eval check**: PASS. All positive cases have direct trigger phrases. Negatives correctly excluded.

### deploy

**Current description**: *"Produce deployment guidance for the user's llms.txt — Nginx / Apache / Caddy / Vercel / Netlify / Cloudflare server config, CI validation pipeline wiring, robots.txt consistency checks, CDN purge strategy, monitoring setup, and a Jira-ready ticket description. Use when the user says 'how do I deploy', 'server config', 'ship it to production', 'CI for llms.txt', 'robots.txt setup'..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| dp-001 "How do I deploy..." | deploy | ✓ |
| dp-002 "Give me the Nginx config..." | deploy | ✓ |
| dp-003 "Set up CI validation..." | deploy | ✓ |
| dp-004 "Open a Jira ticket..." | deploy | ✓ (Jira-ready in description) |
| dp-005 "We're on Cloudflare Workers..." | deploy | ✓ (Cloudflare listed) |
| dp-006 (negative — generate) | generate | correct routing |
| dp-007 (negative — stakeholder-comms) | stakeholder-comms | correct routing |
| dp-008 "What headers should we set..." | deploy | ✓ (server config implies headers) |

**Result**: PASS.

### stakeholder-comms

**Current description**: *"Draft stakeholder communication for llms.txt projects — emails to managers, SEO leads, dev teams, leadership. ...Use when the user says 'draft an email', 'help me explain this to my manager / SEO team / CEO', 'respond to my SEO expert', 'write the Jira ticket description'..."*

**Eval check**: PASS. Specific role-based triggers covered.

### setup-recommender

**Current description**: *"Meta-skill that recommends a starter-pack setup for new users of the llms-txt-advisor plugin. Asks 3-4 lightweight questions about role, site type, primary language, and existing tooling... Use when users say 'where do I start', 'I'm new to this plugin', 'what should I install first', 'recommend a setup for me', 'starter pack', 'help me get going'..."*

**Eval check**:

| Prompt | Expected | Current desc likely fires? |
|---|---|---|
| sr-001 "I'm new to this plugin..." | setup-recommender | ✓ (exact phrase) |
| sr-002 "Recommend a setup..." | setup-recommender | ✓ (exact phrase) |
| sr-003 "Give me a starter pack" | setup-recommender | ✓ (starter pack in description) |
| sr-004 "What should I install first?" | setup-recommender | ✓ (exact phrase) |
| sr-005 "Help me get going..." | setup-recommender | ✓ (exact phrase) |
| sr-006 (negative — cold-start) | cold-start | "set up the plugin and configure my profile" — both skills could fire; need disambiguation |
| sr-007 (negative — audit) | audit | "review my existing file" — clearly audit |
| sr-008 "60-second version" | setup-recommender | ✓ (--quick flag) |

**Refinement noted**: sr-006 has potential ambiguity. The current description's "lower-commitment than cold-start-interview" clause helps. Could add stronger disambiguation: "Use setup-recommender for orientation BEFORE the user commits to configuration; use cold-start-interview when the user is ready to configure."

## Refinements applied

### generate description

Adding "make" as a trigger word. Before:
```
Use when the user says "create our llms.txt", "generate llms.txt", "draft a file for us", "build the llms.txt"...
```

After:
```
Use when the user says "create our llms.txt", "generate llms.txt", "make me an llms.txt", "draft a file for us", "build the llms.txt"...
```

### setup-recommender description

Strengthening disambiguation from cold-start-interview. Adding to the existing description:

```
Use this skill for ORIENTATION before the user commits to configuration. Use
cold-start-interview when the user is ready to actually configure (e.g., they
already know what they want and just need to walk through the questions).
```

## Verification

After refinements:

1. Re-run check.py to ensure descriptions still validate
2. Re-run mental walkthrough of eval prompts
3. Track in this file any future miscategorization observed in production use

## Future improvements (for skill-creator integration)

When running through anthropic-skills:skill-creator:

1. Set up parallel subagent comparison (with-skill vs baseline)
2. Use 20 trigger eval queries per skill (current 7-8 is a starter set)
3. Apply the `scripts.run_loop` iterative optimizer
4. Aggregate via `scripts.aggregate_benchmark`

Document any production miscategorizations in evals.json and re-optimize.

## Cross-references

- Each skill's `SKILL.md` frontmatter
- `README.md` — this evals overview
- `../scripts/check.py` — validates evals.json schema
