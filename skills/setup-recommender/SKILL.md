---
name: setup-recommender
description: >
  Lower-commitment ORIENTATION skill — runs BEFORE cold-start-interview for
  users who are just exploring the llms-txt-advisor plugin. Asks 3 lightweight
  questions about role, site type, and primary language, then recommends
  which sector / language / connector / skill combination to start with.
  Trigger phrases: "I just installed this plugin", "where do I start",
  "where do I begin", "I'm new to this plugin", "first time using this",
  "what should I install first", "recommend a setup", "starter pack",
  "help me get going", "give me the 60-second version", "I don't know what
  any of this is for". **Use setup-recommender (this skill) when the user
  hasn't yet committed to configuring — they want orientation.** Use
  cold-start-interview when the user explicitly says they're ready to
  configure their practice profile (15-20 minute commitment). The dividing
  line: setup-recommender = "tell me what's available"; cold-start =
  "walk me through configuring for my site". This skill never writes the
  practice profile — that's cold-start's job.
argument-hint: "[--quick for a 60-second recommendation] [--export to write the starter local override file]"
---

# Setup Recommender — Plugin Starter-Pack Hub

*Inspired by [legal-builder-hub](https://github.com/anthropics/claude-for-legal/tree/main/legal-builder-hub) from claude-for-legal — the meta-plugin whose cold-start IS the starter-pack recommender.*

## When to use this vs cold-start-interview

| Use this skill (`/setup-recommender`) when... | Use cold-start-interview when... |
|---|---|
| User just installed the plugin and is exploring | User has decided to actually configure |
| Quick 2-minute orientation needed | Full 15-20 minute deep configuration |
| "Where do I start?" question | "Set up the plugin for my site" |
| User wants menu of options before committing | User is ready to commit answers |
| Output is a recommendation, no profile written | Output is a populated practice profile |

## Step 1 — Quick triage (3 questions)

Ask all three at once (an exception to the "max 2-3 questions per turn" rule because this is meant to be lightweight):

```
Quick orientation — three questions and I'll recommend the right starting point:

1. What kind of site are we working with?
   (developer documentation / marketing or blog / e-commerce / marketplace /
    news or publisher / education / healthcare / fintech / government / B2B SaaS /
    gaming / non-profit / media-entertainment / mixed / I'm not sure)

2. Primary business language for stakeholder communication?
   (English / Turkish / Spanish / German / French / Japanese / Mandarin / Arabic /
    Portuguese / other)

3. What's your role in this project?
   (engineer / SEO specialist / product manager / leadership /
    founder of a small business / consultant advising a client / other)
```

Wait. Three answers come back, often partial. Fill gaps with one follow-up.

## Step 2 — Produce the recommendation

Based on the three answers, produce a structured starter-pack:

### A. Sector reference recommendation

Map site type to a sector file. Cite the file so the user can read it directly:

| Site type answered | Sector file to load |
|---|---|
| developer documentation | `knowledge/sectors/dev-docs.md` |
| marketing or blog | `knowledge/sectors/marketing.md` |
| e-commerce | `knowledge/sectors/ecommerce.md` |
| marketplace | `knowledge/sectors/marketplace.md` |
| news or publisher | `knowledge/sectors/news-publisher.md` |
| education | `knowledge/sectors/education.md` |
| healthcare | `knowledge/sectors/healthcare.md` |
| fintech | `knowledge/sectors/fintech.md` |
| government | `knowledge/sectors/government-civic.md` |
| B2B SaaS | `knowledge/sectors/b2b-saas.md` |
| gaming | `knowledge/sectors/gaming.md` |
| non-profit | `knowledge/sectors/non-profit.md` |
| media-entertainment | `knowledge/sectors/media-entertainment.md` |
| mixed / unsure | `knowledge/sectors/generic.md` + ask follow-up |

State the **decision default** for that sector explicitly:

- "For developer documentation, the decision default is **SHIP**. This is the one sector with documented value."
- "For marketing, the decision default is **SKIP**. Empirical evidence shows null AI-citation lift."
- (etc.)

### B. Language reference recommendation

Map language to a language file:

| Language answered | Language file |
|---|---|
| English | `knowledge/languages/en.md` (+ `stakeholder/email-templates-en.md`) |
| Turkish | `knowledge/languages/tr.md` (+ `stakeholder/email-templates-tr.md`) |
| Spanish | `knowledge/languages/es.md` |
| German | `knowledge/languages/de.md` |
| French | `knowledge/languages/fr.md` |
| Japanese | `knowledge/languages/ja.md` |
| Mandarin Chinese | `knowledge/languages/zh.md` |
| Arabic | `knowledge/languages/ar.md` |
| Portuguese | `knowledge/languages/pt.md` |
| Other | English fallback + note the gap; offer to add a new language file |

### C. Connector recommendations (per-sector)

Based on the site type, pull the connector recommendations from `CONNECTORS.md` "Connector selection guidance per site type" table. Examples:

- **Dev docs**: prioritize `~~git`, `~~docs-platform`, `~~ai-visibility`
- **E-commerce**: prioritize `~~ecommerce`, `~~analytics`, `~~cdn`, `~~ai-visibility`
- **Marketplace**: prioritize `~~ecommerce` (or `~~cms`), `~~headless-browser`, `~~analytics`
- **News**: prioritize `~~cms`, `~~analytics`, `~~search-console`
- (etc.)

For each recommended connector, suggest one specific vendor option from the category table (e.g., "for `~~git`, GitHub is preconfigured if you use that; GitLab/Bitbucket also work via the same skill text").

### D. Skill workflow recommendation (which skills to run, in what order)

Based on the role + site type:

**If user is engineer + dev docs site:**
```
1. /llms-txt-advisor:cold-start-interview --quick  (2 min)
2. /llms-txt-advisor:generate    (produce the file)
3. /llms-txt-advisor:deploy      (Nginx config + CI)
```

**If user is SEO specialist:**
```
1. /llms-txt-advisor:advise      (decision discussion)
2. /llms-txt-advisor:audit       (review existing file if any)
3. /llms-txt-advisor:cold-start-interview --full  (15-20 min for proper SEO integration)
4. /llms-txt-advisor:generate
```

**If user is leadership:**
```
1. /llms-txt-advisor:advise      (decision discussion, expectation setting)
2. /llms-txt-advisor:stakeholder-comms  (draft communication to team)
```

**If user is consultant advising a client:**
```
1. /llms-txt-advisor:cold-start-interview --full  (build the client profile)
2. Create llms-txt-advisor.local.md.example in the client repo
3. /llms-txt-advisor:audit  (if client has existing file)
4. /llms-txt-advisor:generate  (produce v1)
5. /llms-txt-advisor:deploy
```

**If user is small-business owner:**
```
1. /llms-txt-advisor:advise      (most likely the answer is "skip, here's where to invest instead")
2. If still interested: /llms-txt-advisor:cold-start-interview --quick
```

(These are starter recommendations — actual sequencing should respect what the user wants.)

### E. Honest-expectations preview

Surface the empirical baseline upfront based on sector:

- **High-value sector (dev docs)**: "For your site type, ~~category placeholder patterns apply naturally. Real benefit from coding-agent users."
- **Skip-default sector (marketing/blog)**: "Heads up — the empirical evidence (3 independent studies) shows null AI-citation lift for marketing sites. We can still ship for the right reasons (internal grounding, replacing broken file), but I want you to know that upfront."
- **Mixed**: "Your site spans multiple sectors. We'll likely ship on the docs subdomain and skip on www."

## Step 3 — Offer starter export (--export flag)

If user passed `--export` OR explicitly asks for "a starter file" / "skeleton" / "boilerplate":

Create `./llms-txt-advisor.local.md` in the current project (or wherever the user invokes the skill from), pre-filled with the recommended sector, language, and connector choices. The user can edit further from there.

Format:

```markdown
# Per-Project Override — llms.txt Advisor — Starter Pack

*Generated by /llms-txt-advisor:setup-recommender on [date].*
*Recommended starter setup based on your initial answers. Edit freely.*

## Project identity
- Site type: [from answer]
- Primary language: [from answer]
- Role context: [from answer]

## Recommended sector reference
- Load `knowledge/sectors/[sector].md` for decisions and structure
- Decision default for this sector: [SHIP / SKIP / Mixed]

## Recommended language reference
- Load `knowledge/languages/[lang].md` for communication conventions

## Recommended connectors to set up
- ~~category1 → [specific vendor]
- ~~category2 → [specific vendor]
- ...

## Recommended workflow
[Step list from above]

## Notes
[Any specific guidance from this triage]
```

Save the file and tell the user where.

## Step 4 — Final orientation

End with:

```
That's the recommended starter pack. Three options now:

1. Walk through the full cold-start to lock in your profile:
   /llms-txt-advisor:cold-start-interview

2. Skip to the work you want to do:
   /llms-txt-advisor:advise        (decisions and questions)
   /llms-txt-advisor:audit         (review existing file)
   /llms-txt-advisor:generate      (create new file)
   /llms-txt-advisor:deploy        (production deployment)
   /llms-txt-advisor:stakeholder-comms  (draft team communication)

3. Read the recommended sector + language files first, then come back.

Which?
```

Don't auto-proceed. Let the user choose.

## Special cases

### User can't answer "what kind of site"

If the user can't classify their site, offer to look at it. Ask for the URL. Fetch the homepage and a few pages if possible. Make a best-guess classification and present it.

If still unclear, default to `generic.md` and proceed with conservative recommendations.

### Multiple sectors apply

If the user's site spans sectors (e.g., a fintech B2B SaaS with docs + marketing + blog), recommend the most relevant primary sector but mention the others. Recommend running cold-start with `--section ia` later to capture the multi-sector structure.

### User in a regulated industry

If the user identifies as healthcare, fintech, government, or education, add a specific note about the regulatory considerations from those sector files (PHI, financial advice, accessibility, etc.).

### User wants to skip

If the user says "actually I think we should skip llms.txt" after this triage, validate the decision:

> "That's a fine call. For your site type, the empirical evidence supports skipping. The higher-leverage investments would be: [from the sector file's 'invest in instead' list]. Want me to draft the recommendation memo to your stakeholders explaining the decision? → /llms-txt-advisor:stakeholder-comms"

## --quick variant (60-second version)

If user passed `--quick`, ask only ONE question:

> "Just tell me your site type (dev docs / marketing / e-commerce / marketplace / news / other) — I'll recommend a starter setup in under a minute."

Then produce a condensed recommendation (sector file + first 2 skills to run + default language English). Skip the full export step. Skip the role question.

## Guardrails

- **Never make the recommendation feel like the decision is locked in.** This is orientation, not configuration.
- **Always cite the empirical baseline** for sectors that default to SKIP.
- **Don't run cold-start automatically.** The user must explicitly invoke `/llms-txt-advisor:cold-start-interview` next.
- **Don't write to the user's practice profile.** That's cold-start's job. This skill only writes to `./llms-txt-advisor.local.md` (project-level) if `--export` is used.
- **Respect the user's chosen language** for the conversation itself. If they're typing in Turkish, respond in Turkish. The recommendation file paths are language-agnostic.

## Cross-references

- `cold-start-interview/SKILL.md` — the deep configuration this skill points to
- `advise/SKILL.md` — the next skill for general questions
- `../knowledge/sectors/_router.md` — sector classification logic
- `../knowledge/languages/_router.md` — language resolution logic
- `../CONNECTORS.md` — `~~category` dictionary and per-sector connector recommendations
- `../llms-txt-advisor.local.md.example` — the per-project override template this skill produces
- Pattern source: [`anthropics/claude-for-legal/legal-builder-hub`](https://github.com/anthropics/claude-for-legal/tree/main/legal-builder-hub)

