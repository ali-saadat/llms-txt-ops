---
name: cold-start-interview
description: >
  Run the full configuration interview that writes the user's practice profile
  to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`. Use when the user
  is ready to invest 15-20 minutes (or 2 minutes via --quick) actually
  configuring the plugin for their specific site — not just exploring.
  Trigger phrases: "configure llms-txt advisor", "configure the plugin for
  our [site type]", "onboard me", "let's get started", "I don't have an
  llms.txt yet but I want to create one", "help me create my first llms.txt",
  "we want to start fresh", "we don't have llms.txt", "let's walk through
  setup", "configure my profile", "set up my profile", "help me set up the
  plugin for the first time", "set up the plugin for the first time",
  "set up for the first time", "start over", "start fresh", "redo from
  scratch", "reset my profile", "forget everything and start over". Also fires automatically when the practice
  profile is missing or contains [PLACEHOLDER] markers (every other skill
  bounces here when found). **Use setup-recommender instead if the user is
  just exploring, asks "where do I start", says "I'm new to this plugin",
  or wants the 60-second starter-pack overview before committing to
  configuration.** This is the only skill that writes the practice profile.
  **Ambiguity policy**: single-word inputs ("help", "hi") or bare verbs
  without targets do NOT auto-route here. The user must signal commitment
  to configuration (15-20 minute investment) before this skill activates.
  **Multilingual matching**: trigger phrases match by intent across
  languages — Japanese "プロフィールを設定してください", Turkish "profilimi
  yapılandır", Spanish "configura mi perfil", German "konfiguriere mein
  Profil" etc. all match "configure my profile" intent. Match semantic
  meaning, not literal English tokens.
argument-hint: "[--redo] [--quick] [--full] [--section <name>] [--check-integrations] [--language <code>]"
---

# Cold-Start Interview — llms.txt Advisor

## What this skill does

Walks the user through a structured conversation that gathers exactly enough context to make every other skill in this plugin produce tailored, honest output. Writes the user's answers to a practice profile at `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`. Every downstream skill reads from that path.

**This is the only skill that should run on a fresh install.** Skills like `advise`, `audit`, `generate`, `customize`, and `deploy` all check for `[PLACEHOLDER]` markers in the practice profile and bounce to here if found.

## Step 1 — State check (do this first, every time)

Read `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`. Then branch:

| Condition | Action |
|---|---|
| File does not exist | Fresh install. Create parent dirs. Proceed to Step 2. |
| File exists, has `[PLACEHOLDER]` markers | Incomplete. Proceed to Step 2 (or jump to `--section` if flag passed). |
| File exists, has `<!-- SETUP PAUSED AT: -->` HTML comment | Resume. Announce: *"Picking up where we left off — you were partway through [section]."* |
| File exists, fully configured, no `--redo` flag | Already configured. Ask: *"Your profile is configured. (a) review it, (b) re-run cold start (--redo), (c) update a specific section (--section <name>), or (d) proceed with `/advise`?"* |
| User explicitly passed `--redo` | Confirm backup + proceed. |
| `--check-integrations` | Skip interview; re-probe MCP/data sources only (see `references/subcommand-flows.md`). |

## Step 2 — Install scope check (briefly)

Verify user-scope install, not project-scope. If project-scoped, warn briefly that some external file reads may not work.

## Step 3 — Fork-first preamble

Open with this:

> "Welcome. I'm going to walk you through setting up the llms.txt advisor for your site. There are two paths:
>
> - **Quick (2 minutes)** — minimum questions, sensible defaults for the rest. Refine later.
> - **Full (15-20 minutes)** — proper interview covering goals, stack, IA, schema, SEO context, deployment, stakeholders.
>
> Which works for you?"

Wait. If "quick" → run quick path per `references/subcommand-flows.md`. If "full" → full path. Unsure → default to full.

## Step 4 — The interview

### Pacing rules (apply throughout)

- **Max 2-3 questions per turn.** Never 5 at once.
- **No "please provide" / "configure your settings"**. Use conversational framing.
- **Wait for response before next batch.** Use "I'll wait" or "Take your time."
- **Pause-and-resume** if user defers: write `[PENDING]` marker, add `<!-- SETUP PAUSED AT: section -->`, save.
- **Seed docs over typed answers.** For anything written down (existing llms.txt, robots.txt, sitemap, schema), ask for URL/paste first.
- **Language match**: respond in the user's typing language for the interview itself. Pull translations from `../../knowledge/languages/<code>.md`. **The user's preference always wins** — ask explicitly which language they want for: (a) the interview itself, (b) the generated llms.txt file content (English is the default for the file unless they request otherwise), (c) stakeholder communication drafts. See `../../knowledge/languages/_router.md` for the language policy.

### Part 0 — Site identity (always)

```
Tell me about the site:
1. What's it called? (Site name or brand)
2. What's the primary domain?
3. In one sentence — what does it do?
```

Wait, then:

```
A few follow-ups:
1. What kind of site? (developer documentation / marketing or blog / e-commerce /
   marketplace / news or publisher / education / healthcare / fintech /
   government / B2B SaaS / gaming / non-profit / media-entertainment / mixed)
2. What language(s) is the site itself in? (the content visitors see)
3. What language do you want the generated llms.txt file to be in?
   (default: English. Most LLM crawlers process English best. Override only
    if you specifically want non-English — e.g., your site is monolingual
    non-English and you want the file to match.)
4. What language do you want stakeholder communication drafts in?
   (default: matches your typing language)
```

Wait.

**On answer**: load the matching sector file from `../../knowledge/sectors/<sector>.md` for sector-specific follow-ups (see `references/sector-question-banks.md` for the question banks).

For marketplace / e-commerce with multi-region: also ask about the geographic dimension.

### Part 1 — Goals and honest expectations (always — most important section)

```
Now the honest part — why are you considering llms.txt?
1. Are you trying to:
   (a) Replace a broken / bloated existing file
   (b) Build internal grounding for your own RAG / chatbot / AI features
   (c) Forward-compatibility insurance against future standards
   (d) AI visibility — get cited more in ChatGPT, Gemini, Claude
   (e) Leadership asked for it
   (f) Other (describe)
2. Are you already running your own AI features (chatbot, RAG, support)?
```

Wait.

**Critical branch on (d) or (e)**: invoke the full honest-expectations conversation per `references/honest-expectations-script.md`. The user must explicitly choose between SKIP path (recommendation memo) and SHIP-with-realistic-expectations path.

For (a), (b), or (c): continue straight through.

Then:

```
Have you set realistic expectations with leadership / stakeholders on this?
The studies show no measurable AI-citation lift. The wins are
replacing-broken, internal-grounding, and forward-compat. Aligned?
1. Yes, aligned.
2. No, still need to have that conversation.
3. We're framing it as AI visibility internally — I know that's a problem.
```

### Part 2 — Existing state probe

```
1. Current llms.txt at site root? Yes (paste URL) / No / Don't know
2. Where is your sitemap.xml?
3. Is there a robots.txt? Where?
```

**If they have an existing llms.txt**: fetch and analyze (size, link count, instructions block present, SEO routing present, bloat assessment). Report findings.

```
Two more:
1. Hosted docs platform that auto-generates? (Mintlify / Fern / GitBook /
   ReadMe / Redocly / No)
2. Has anyone tried to ship llms.txt before?
```

### Part 3 — Technical stack (full mode only)

```
1. Server? (Nginx / Apache / Caddy / Vercel / Netlify / Cloudflare Workers / Other)
2. CDN in front? (Cloudflare / Fastly / Akamai / AWS CloudFront / None / Don't know)
3. CI/CD? (GitHub Actions / GitLab / CircleCI / Other)
```

Wait, then:

```
And the framework:
1. What runs the site? (Next.js / Docusaurus / VitePress / Astro / Hugo /
   Jekyll / WordPress / Hand-rolled / Other)
2. Where will the llms.txt source-of-truth live in your repo?
```

### Part 4 — Information architecture (full + minimal-for-quick)

**Quick mode**: just ask for top 5-10 most important pages as URLs.

**Full mode**: load `references/sector-question-banks.md` for sector-specific questions, then ask:

```
Walk me through your IA:
1. Top-level categories? (5-15 most important hubs — names + URL slugs)
2. Geographic / multi-tenant dimension URL pattern?
3. Long-tail dimension to NOT enumerate?
```

Wait, then:

```
A few more:
1. Planning / utility tools on a subdomain? URLs?
2. 10-30 editorial articles to surface to LLMs?
3. Any "what NOT to surface" content?
```

### Part 5 — Schema.org structured data (full mode)

```
For the structured-data disclosure section:
1. What Schema.org types do pages ship? (Article / Product / LocalBusiness /
   Organization / Review / BreadcrumbList / Person / FAQPage / Other / Not sure)
2. Validated via Rich Results Test or Schema.org Validator?
```

If "not sure", load `../../reference/schema-types.md` and offer to defer this section as `[PENDING]`.

### Part 6 — SEO context (full mode)

```
A few SEO questions:
1. SEO team / consultant involved? Who?
2. Stakeholder dynamic? (over-believers / skeptics / pragmatists / mixed)
3. robots.txt for AI crawlers right now? (Allow all / block specific bots /
   block all AI / Don't know)
```

```
And specifically:
1. Bing Webmaster Tools AI Performance report set up? (Feb 2026 launch)
2. Analytics platform? (GA4 / Adobe / Plausible / Other)
```

### Part 7 — Deployment policy (always — confirm defaults even in quick)

**Quick mode**: confirm defaults block.

**Full mode**:

```
Deployment specifics:
1. File at https://yourdomain/llms.txt — confirmed?
2. Content-Type text/markdown; charset=utf-8 + X-Robots-Tag noindex — any override?
3. Cache TTL — default 1 hour. Higher / lower?
4. CDN purge strategy — auto or manual?
5. CI validation script — wire in or run manually?
```

### Part 8 — House style and outputs (full mode)

```
Final outputs config:
1. Tone for AI directives? (Formal-factual / brief-direct / conversational)
2. Produce deployment spec? (Jira-ready / informal MD / no)
3. Draft stakeholder emails? (English / Turkish / both / no)
```

### Part 9 — Stakeholder communication (full mode, only if emails)

```
Stakeholder context:
1. Manager / sponsor? (Name + role)
2. SEO lead?
3. Engineering owner?
4. Email language + business convention?
```

## Step 5 — Seed-doc ingestion (full mode, recommended)

```
One last thing — share these to make output match your real situation:
1. Current llms.txt (URL or paste)
2. robots.txt URL
3. sitemap.xml URL
4. 2-3 editorial articles you want surfaced
5. AI / data-usage policy page
```

For each URL, fetch and analyze. Compare observed vs reported, flag deltas in the profile.

## Step 6 — Write the profile

1. Write populated profile to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`. Create parent dirs.
2. If `--redo`, back up to `CLAUDE.md.bak.YYYYMMDD` first.
3. Remove `[PLACEHOLDER]` markers that have real values; leave `[PENDING]` for skipped sections.
4. Set `Last reviewed` to today; `Next quarterly review due` to today + 90 days.

If user chose SKIP path in Part 1: write a brief profile (goal = "decided-not-to-ship", date, reason) + draft a recommendation memo. Offer to draft the leadership email.

## Step 7 — Confirm and route to next skill

```
Profile configured. Saved to ~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md

What I captured:
- Site type: [X]
- Goal: [Y]
- Stack: [Z]
- IA depth: [N categories, M-province dimension]
- Schema: [types]
- Deployment target: [path + headers]

Next steps:
1. Generate file from scratch → `/llms-txt-advisor:generate`
2. Audit existing file → `/llms-txt-advisor:audit`
3. Deployment spec → `/llms-txt-advisor:deploy`
4. Draft stakeholder comms → `/llms-txt-advisor:stakeholder-comms`
5. General advice → `/llms-txt-advisor:advise`
```

Wait for choice. Don't auto-proceed.

## Subcommand handling

See `references/subcommand-flows.md` for detailed handling of `--quick`, `--full`, `--redo`, `--section <name>`, `--check-integrations`, `--language <code>`, and combinations.

## Special cases

### User doesn't know site type

Offer to look at the site. Ask for the domain. Fetch homepage + key pages if possible. Make best-guess classification, present for confirmation.

### User is advising on another org's site

Ask: *"Whose site is this? Your direct work, or you're advising someone else."* Note in profile under Site identity. Affects stakeholder framing.

### User insists on AI-visibility goal despite evidence

Note explicitly: *"Goal: AI-visibility despite empirical evidence. Stakeholder framing risk acknowledged."* Continue interview but flag that downstream outputs should include `[REMINDER — empirical evidence does not support AI-citation lift]` on stakeholder-facing artifacts. Don't refuse to continue.

## What this skill NEVER does

- Run automatically without user invocation
- Ask 5+ questions at once
- Generate the llms.txt itself (that's `/generate`)
- Write anywhere except `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` and (with confirmation) a backup file
- Skip the honest-expectations conversation in Part 1 (even quick mode runs Part 1)

## Cross-references

### In this skill's references/ (loaded on demand)

- `references/sector-question-banks.md` — sector-specific follow-ups for Part 4
- `references/honest-expectations-script.md` — full Part 1 script when goal is AI-visibility
- `references/subcommand-flows.md` — detailed subcommand handling

### Other skills (next-step routes)

- `../advise/SKILL.md` — main advisory router
- `../audit/SKILL.md` — review existing llms.txt
- `../generate/SKILL.md` — create from scratch
- `../customize/SKILL.md` — update specific sections
- `../deploy/SKILL.md` — deployment guidance
- `../stakeholder-comms/SKILL.md` — draft stakeholder emails

### Knowledge corpus (loaded on demand during interview)

- `../../knowledge/04-decision-framework.md` — when to ship vs skip
- `../../knowledge/02-empirical-evidence.md` — citations for honest-expectations
- `../../knowledge/sectors/<sector>.md` — sector-specific concerns
- `../../knowledge/languages/<code>.md` — language-specific conventions
- `../../templates/llms-txt-<type>.md` — preview what generation will produce
- `../../case-study/example-marketplace-case.md` — worked example
