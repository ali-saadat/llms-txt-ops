# User Guide — Non-Technical Walkthrough

*For SEO leads, product managers, business owners, and anyone whose job touches a website but doesn't involve writing code.*

This guide walks you through the llms-txt-advisor plugin in plain English. No command line needed beyond two lines of setup. By the end of this guide, you'll know whether your site should even bother with an llms.txt file, and if yes, you'll have one ready to ship.

---

## Part 1 — Should you even read this guide?

**Short answer**: maybe. Read this 60-second checklist first.

| Question | If yes, continue |
|---|---|
| Someone on your team is asking about "llms.txt" | ✅ |
| Your CEO read an article about it and wants action | ✅ |
| You already have a `/llms.txt` file on your website and you're not sure if it's any good | ✅ |
| You run a developer documentation site (SDK, API docs) | ✅ — strongest case for shipping |
| You're building your own AI chatbot/search and want to give it the best content map | ✅ |
| You want to "rank higher on ChatGPT" | ⚠️ Read this guide so you can explain to your team why llms.txt is NOT how that works |
| None of the above | Skip — there are higher-leverage things to do |

---

## Part 2 — What is llms.txt in plain English?

Imagine your website has a robots.txt file (rules for search engines) and a sitemap.xml file (a map for search engines). `llms.txt` is supposed to be a similar map, but for **AI systems** (like ChatGPT, Claude, Gemini) — telling them which pages on your site are most important and how to interpret them.

Spec proposed by Jeremy Howard / Answer.AI in September 2024. It's a plain text file at `yoursite.com/llms.txt`.

### Does it actually work? (the honest answer)

**Three independent studies** tested this question:

1. **SE Ranking** (2025) — checked 300,000 websites
2. **OtterlyAI** (2025) — analyzed 90 days of AI crawler logs
3. **Search Engine Land** (2025) — controlled test across 10 sites

**All three found**: shipping llms.txt has no measurable effect on:
- AI citation rates (how often AI chatbots quote your site)
- AI-driven traffic to your site
- Visibility in AI answers

Google's John Mueller publicly confirmed Google does not use llms.txt for any ranking purpose. OpenAI, Anthropic, and other major AI vendors have not committed to using it either.

**So why bother?** Read on.

---

## Part 3 — When llms.txt IS worth shipping

Three specific situations make it worthwhile:

### Situation 1: Developer documentation

If your site is documentation for an SDK, API, library, or developer tool — coding agents (Cursor, Claude Code, GitHub Copilot, Cline, Aider) read llms.txt to give your developers better answers.

**Concrete benefit**: a dev asks Cursor "how do I authenticate with your API?" — with a good llms.txt, Cursor finds the right page faster.

### Situation 2: Replacing a bloated/broken existing file

If your site already has an `llms.txt` file but it's auto-generated, 10+ MB, full of dead links, or otherwise broken — replacing it is strictly better than leaving the bad version up.

The plugin handles this via its "audit" → "generate" → "deploy" workflow.

### Situation 3: Internal AI grounding

If your company is building its own AI chatbot/search/RAG system — a curated llms.txt doubles as grounding material for that internal system. One file, two audiences (external AI vendors + your own system).

### Anything else? Default = skip.

If your site doesn't fit one of those three situations, the plugin will tell you so and point you at things that **actually do** move the needle:

| Goal | Higher-leverage investment |
|---|---|
| Be cited by AI | Schema.org JSON-LD + author E-E-A-T + Wikipedia citations |
| AI-driven traffic | Reddit/YouTube content + original research + earned links |
| Brand authority in AI answers | Consistent entity disambiguation + canonical content + structured author bylines |

---

## Part 4 — Installing the plugin (one-time, 5 minutes)

You only need to do this once.

### Prerequisites

1. **Claude Code installed** — get it at [claude.com/claude-code](https://claude.com/claude-code) (free)
2. **A copy of this repo on your machine** — typically at `~/Downloads/llms-txt-ops/`

### Two commands to install

Open Claude Code in any folder and type these two slash-commands one at a time:

```
/plugin marketplace add ~/Downloads/llms-txt-ops
```

```
/plugin install llms-txt-advisor
```

The plugin is now available. You'll see new commands all starting with `/llms-txt-advisor:`.

### Wait — what's a "slash command"?

In Claude Code, typing `/` shows a menu of commands. Type a few letters to filter. They're the way you invoke skills from this plugin.

---

## Part 5 — Your first 5 minutes with the plugin

There are only two commands you need to know to get started:

### Step 1 — Get oriented (60 seconds)

```
/llms-txt-advisor:setup-recommender
```

This is a quick orientation skill. It will:
1. Ask you 2 questions about your situation
2. Tell you which other skill is right for you
3. Set your expectations honestly

**That's it.** This skill writes nothing, breaks nothing. Just orientation.

### Step 2 — Configure for your site (15–20 minutes, or 2-minute quick mode)

When you're ready to actually use the plugin for your site:

```
/llms-txt-advisor:cold-start-interview
```

This is the **only** skill that writes a "practice profile" — a small configuration file that captures your site's specifics so every other skill can produce tailored output instead of generic advice.

It asks about:
- Your site's name and primary language
- What kind of site (docs, marketing, e-commerce, news, etc.)
- Whether you already have an llms.txt and where
- Your hosting setup (Nginx, Vercel, etc.)
- Who the stakeholders are
- Honest goals (so it doesn't over-promise to your leadership)

You can answer "I don't know" or "skip" to most questions — it'll use reasonable defaults.

If you don't have 15 minutes, run the quick version:

```
/llms-txt-advisor:cold-start-interview --quick
```

That covers just the essentials in about 2 minutes.

---

## Part 6 — Common scenarios with full walkthroughs

### Scenario A: "We don't have an llms.txt — should we add one?"

```
/llms-txt-advisor:advise
```

Then describe your situation. The advisor will:
1. Apply the decision framework against your profile
2. Tell you ship / skip / it depends
3. Cite the three empirical studies if needed
4. Suggest the next concrete step

### Scenario B: "We have an llms.txt — is it any good?"

```
/llms-txt-advisor:audit
```

Paste the URL (e.g., `https://example.com/llms.txt`) or the file contents. The audit will:
1. Check spec compliance (encoding, format, size)
2. Score against 15 documented failure modes
3. Tag findings as Critical / High / Medium / Low
4. Recommend specific fixes

### Scenario C: "Generate me a new llms.txt"

```
/llms-txt-advisor:generate
```

Walks through file generation using the curated templates that match your site type. Output: a ready-to-deploy `llms.txt` file plus a deployment specification.

### Scenario D: "Tweak the products section in my existing file"

```
/llms-txt-advisor:customize
```

Surgical updates to a named section. You point at what you want changed — it doesn't rewrite the whole file.

### Scenario E: "How do I actually put the file on my server?"

```
/llms-txt-advisor:deploy
```

Produces concrete deployment steps for your hosting setup: Nginx config snippets, Apache rules, Caddy directives, Vercel/Netlify/Cloudflare instructions. Includes a CI validation script.

### Scenario F: "I need to explain this to my SEO team / manager"

```
/llms-txt-advisor:stakeholder-comms
```

Drafts a polite, professional email or Jira ticket in your language (13 supported). Honest framing — never promises things the evidence doesn't support. Includes table formatting, color-coded prioritization, and the right level of detail for your audience.

---

## Part 7 — What if I get stuck?

### "I typed a command and Claude asked me a question I don't understand"

Just answer "I don't know" or "skip" — the plugin handles unknowns gracefully with reasonable defaults.

### "I want to start over"

```
/llms-txt-advisor:cold-start-interview
```

Run this again — it overwrites the previous profile. Or say "reset my profile" / "forget everything and start over."

### "I want generic output without configuring my profile"

When you run any skill, say "provisional" — the plugin will use conservative defaults and label its output as `[PROVISIONAL]` so you know it's not tailored.

### "My team speaks a different language"

The plugin supports 13 languages: English, Turkish, Spanish, German, French, Japanese, Mandarin Chinese, Arabic, Portuguese, Italian, Dutch, Korean, Russian. Just type in your language — the plugin matches.

For the llms.txt file content itself, English is the default (since AI crawlers parse English best). You can override that during the cold-start interview.

### "I need to roll this out to multiple sites / a multi-region operation"

The plugin handles this via "sector composition" — see the cold-start interview's questions about geographic dimension, multi-tenant patterns, and URL templates. The canonical worked example is in [`case-study/example-marketplace-case.md`](case-study/example-marketplace-case.md) (12 MB → 28 KB recovery).

### "I want to monitor the file's freshness over time"

The plugin includes a managed-agent cookbook called `staleness-watcher` that runs weekly and emails you if the file goes stale, hits broken links, or drifts from your sitemap. Setup requires a developer — point them at `managed-agent-cookbooks/staleness-watcher/` and `scripts/deploy-managed-agent.sh`.

---

## Part 8 — Glossary

| Term | Plain meaning |
|---|---|
| **llms.txt** | A plain-text file at `yoursite.com/llms.txt` that's meant to be a content map for AI systems |
| **Spec** | The official rules for what llms.txt should look like (proposed by Answer.AI, September 2024) |
| **Schema.org / JSON-LD** | A different, well-established standard for structured data on web pages. Much more impactful than llms.txt for AI visibility. |
| **GEO / AEO** | Generative Engine Optimization / Answer Engine Optimization — the SEO discipline around AI search. llms.txt is a small part of it. |
| **MCP** | Model Context Protocol — how AI agents call external tools. Not related to llms.txt directly. |
| **A2A** | Agent-to-Agent protocol — how AI agents talk to each other. This plugin supports it; most users never need to know. |
| **Practice profile** | The small config file the cold-start interview writes for you. Captures your site's specifics so output is tailored. |
| **PROVISIONAL** | A tag the plugin adds to output when you haven't configured your profile yet — means "this is generic; configure for better output." |
| **Anti-pattern** | A common llms.txt mistake. The plugin checks for 15 of them. |
| **Cold-start interview** | The 15–20 minute (or 2-minute quick) configuration conversation |
| **Skill** | A specialized feature of the plugin you invoke with a slash-command |
| **Bundle** | A pre-packaged set of skills for a specific journey (bootstrap = new sites; migration = existing files) |

---

## Part 9 — Trust signals

How can you trust this plugin's advice?

1. **It cites real studies, by name.** SE Ranking, OtterlyAI, Search Engine Land — all checkable.
2. **It refuses to over-promise.** If you ask "will this get me more AI citations?", the plugin says no, the evidence doesn't support that.
3. **It has 100% validation.** 42 structural checks pass, 94 trigger evals pass, 42 automated tests pass. See [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).
4. **The code is source-available.** PolyForm Noncommercial 1.0.0 — free for personal/research/educational/non-profit use; commercial users need a paid license (see [`COMMERCIAL.md`](COMMERCIAL.md)). Read any file. Audit any claim.
5. **It's grounded in patterns from Anthropic's reference repos** (claude-for-legal, knowledge-work-plugins, financial-services) — not invented from scratch.

If the plugin ever tells you something that feels off, you can challenge it: "show me the source for that claim" — every empirical statement is traceable to `knowledge/02-empirical-evidence.md` and its citations.

---

## Part 10 — What to do next

| Your situation right now | Next action |
|---|---|
| Curious, no specific question | Run `/llms-txt-advisor:setup-recommender` for 60-second orientation |
| Have a specific decision to make | Run `/llms-txt-advisor:advise` and describe your situation |
| Existing llms.txt to check | Run `/llms-txt-advisor:audit` with the URL |
| Need to write the email to leadership | Run `/llms-txt-advisor:stakeholder-comms` |
| Just want to read more about why | See [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md) and [`knowledge/04-decision-framework.md`](knowledge/04-decision-framework.md) |

If you got value from this guide and want to extend the plugin (add a sector, language, or skill), hand this repo to a developer with [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Need help?

- For commands not working: try `/llms-txt-advisor:advise` and explain your issue in plain words — it routes to the right skill
- For technical issues: see the developer-facing [`README.md`](README.md) and [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)
- For the empirical basis: [`knowledge/02-empirical-evidence.md`](knowledge/02-empirical-evidence.md)

**Honest closing note**: the most likely outcome of running this plugin is that it tells you "don't ship llms.txt, here are the things that actually work instead." That's the feature, not a bug.
