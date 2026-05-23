---
name: advise
description: >
  Main advisory router for general llms.txt questions AND the disambiguation
  fallback for vague inputs. Use when the user asks general questions —
  "should I add llms.txt", "is llms.txt worth it", "what does llms.txt do",
  "explain llms.txt to my team", "what's the SOTA on llms.txt", "I need help
  with my llms.txt". **Also use as the disambiguation fallback** for bare verb
  inputs without specific targets — "update my llms.txt" (without naming a
  section), "fix it" (no referent), "change it", "modify the file",
  "update everything", "change everything", "fix the whole thing" — this
  skill asks clarifying questions before routing to a destructive skill
  (customize, generate, deploy). Routes to specialized sub-skills (audit,
  generate, customize, deploy, stakeholder-comms) when the user's intent
  becomes clearer. Always bounces to cold-start-interview if the practice
  profile isn't configured. **Global ambiguity policy**: single-word inputs
  ("help") route here for clarification, never directly to destructive
  skills.
argument-hint: "[--provisional to skip profile check and use defaults]"
---

# Advise — llms.txt Advisory Router

## Step 1 — Profile check

Read `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`.

| Condition | Action |
|---|---|
| File missing OR has `[PLACEHOLDER]` markers | Bounce (see below) |
| User passed `--provisional` | Skip profile, use defaults from `CLAUDE.md` template at plugin root |
| File configured | Continue to Step 2 |

### Bounce script

> "I notice you haven't configured your llms.txt advisor profile yet — that's how I tailor recommendations to your specific site context.
>
> Two choices:
> - Run `/llms-txt-advisor:cold-start-interview` (2-20 minutes depending on path) to configure your profile. Then I'll give you tailored output.
> - Say "**provisional**" and I'll continue using generic defaults. Every output will be tagged `[PROVISIONAL — configure your profile for tailored output]`.
>
> Which?"

Wait.

## Step 2 — Detect intent

Listen to what the user is asking and route:

| User intent | Route to |
|---|---|
| "Should I add llms.txt to my site?" | Continue here — apply decision framework |
| "Review my existing llms.txt" / "audit my file" | `/llms-txt-advisor:audit` |
| "Generate / write / create an llms.txt" | `/llms-txt-advisor:generate` |
| "Update / tweak / customize specific section" | `/llms-txt-advisor:customize` |
| "How do I deploy it" / "server config" / "validation script" | `/llms-txt-advisor:deploy` |
| "Help me write the email to my SEO team" / "talk to stakeholders" | `/llms-txt-advisor:stakeholder-comms` |
| "What's the SOTA" / "tell me about llms.txt" / general education | Continue here — explain |

If routing, announce: *"That sounds like `/llms-txt-advisor:[X]` — invoking that. You can cancel if I picked wrong."* Then invoke.

If continuing here, proceed to Step 3.

## Step 3 — Apply decision framework (for "should I ship" questions)

1. Load `knowledge/04-decision-framework.md`.
2. Cross-reference against the user's profile (site type, goal).
3. Apply the decision matrix.
4. Be explicit about the empirical baseline — load `knowledge/02-empirical-evidence.md` if the user needs the three-studies citation.

### Decision flow

```
Site type from profile?
├── Developer documentation → STRONG SHIP
│   → recommend templates/llms-txt-dev-docs.md + /generate
├── Marketing / blog → DEFAULT SKIP
│   → explain why, redirect to schema + external citations + Reddit/YouTube
├── E-commerce → DEFAULT SKIP UNLESS replacing-bloated-file
│   → if existing is bloated: SHIP per ExampleMart pattern
├── News / publisher → DEFAULT SKIP
│   → invest in author E-E-A-T, Wikipedia citations
├── Mixed (docs + marketing) → SHIP ON DOCS SUBDOMAIN ONLY
└── Marketplace → SHIP (ExampleMart pattern is the playbook)

Goal from profile?
├── replacing-broken-file → SHIP (status quo is worst option)
├── internal-grounding → SHIP (one file, two audiences)
├── forward-compatibility → SHIP minimal if cost is ≤4 hours
├── AI-visibility → DON'T SHIP, redirect to GEO toolkit
└── leadership-mandate → SHIP with explicit honest framing
```

## Step 4 — Produce the recommendation

Structure the answer as:

1. **Verdict** — ship / skip / it depends, with one-sentence reason
2. **Empirical reality** — brief: three studies, Google said no, real use cases are narrow
3. **For YOUR site specifically** — apply the user's profile context
4. **Next steps** — concrete: which skill to invoke next, which template to use, what the engineering cost looks like

## Step 5 — Offer follow-up

After the recommendation:

> "Want me to:
> 1. Generate a starting file based on what we just discussed → `/llms-txt-advisor:generate`
> 2. Draft the stakeholder communication explaining the decision → `/llms-txt-advisor:stakeholder-comms`
> 3. Walk through deployment specifics → `/llms-txt-advisor:deploy`
> 4. Just leave you with this advice and you'll come back later"

## Guardrails

- **Never recommend llms.txt as a citation lever.** The empirical evidence does not support it. If the user pushes back, cite Mueller and the three studies.
- **Never produce marketing-style descriptions.** If the user wants "punchy copy" for the file, redirect — descriptions should be literal "what's on the page" language per the implementation guide.
- **Don't promise traffic.** Ever. Don't promise AI mentions. Don't promise citation lift. The evidence base doesn't support any of those promises.
- **Do promise specific operational improvements**: replacing a broken file, building an internal grounding asset, having CI validation in place.

## Cross-references

- `knowledge/04-decision-framework.md` — the core decision matrix
- `knowledge/02-empirical-evidence.md` — the studies and quotes
- `knowledge/03-seo-perspective.md` — for SEO-stance questions
- `knowledge/01-foundations.md` — for "what is it" questions
- `case-study/example-marketplace-case.md` — the canonical worked example
- `stakeholder/expectations.md` — framing language for pushback scenarios
