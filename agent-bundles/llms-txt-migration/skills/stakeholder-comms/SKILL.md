---
name: stakeholder-comms
description: >
  Draft stakeholder communication and written artifacts for llms.txt
  projects — emails to managers, SEO leads, dev teams, leadership;
  Jira ticket descriptions; status memos; recommendation memos. Sets
  realistic expectations grounded in empirical evidence, handles
  cross-cultural professional communication in any language requested
  by the user (matches user's typing language by default, overridable
  via --language). **This skill is the default for ALL writing/drafting
  tasks**, including the default for vanilla "write the Jira ticket
  description" or "draft the Jira ticket" requests. Trigger phrases:
  "draft an email", "draft the email", "write the email", "help me
  explain this to my manager / SEO team / CEO", "respond to my SEO
  expert", "write the Jira ticket description", "write the Jira ticket",
  "draft the Jira ticket", "stakeholder memo", "recommendation memo",
  "status update", "follow-up email". For specifically technical Jira
  tickets where the user explicitly says "deployment Jira", "technical
  Jira", "ops Jira", or "CI ticket", use `deploy --ticket` instead.
argument-hint: "[--language <code>] [--audience manager|seo|engineering|leadership|vendor|sceptic] [--type initial|follow-up|encoding-issue|disagreement|status-update|stakeholder-jira-ticket]"
---

**Note on Jira tickets**: this skill produces the **stakeholder-facing** Jira ticket — business context, owners, communication updates, expected outcomes for non-technical readers. For a **deployment** Jira ticket (technical scope: server config, CI changes, robots.txt diff), use `/llms-txt-advisor:deploy` instead.

# Stakeholder Communication — Draft Emails and Memos

## Step 1 — Profile check

Bounce-on-placeholder pattern. The skill especially needs:

- `Stakeholder communication preferences` section of the profile (language, stakeholder names, business convention)
- `Goals` from Part 1 of cold-start (so framing matches the agreed expectation baseline)

## Language for the draft

Apply the language policy from `../../knowledge/languages/_router.md`:

1. If user passed `--language <code>` in this invocation → use that
2. Else if user explicitly requested ("draft this in [language]") → use that
3. Else match the **user's typing language** in the current conversation
4. Else if profile's `Communication language(s) for stakeholder docs` is set → use that
5. Else default to English

**Confirm with user if ambiguous**:

> "I'll draft this in [detected language] to match how you're writing. Want a different language for the email itself?"

Load the appropriate language file from `../../knowledge/languages/<code>.md` for tone, honorifics, closings, and cultural notes.

## Step 2 — Identify audience and type

If not specified via flags, ask:

```
Who's the email going to, and what's the situation?

Audience:
1. Manager / sponsor
2. SEO lead or SEO expert
3. Engineering team (the engineering team / etc.)
4. Leadership / executive
5. Vendor reaching out about "AI optimization"
6. Skeptic on the team

Type:
1. Initial recommendation
2. Follow-up after feedback / multiple feedback sets
3. Encoding-issue / quality dispute response
4. Disagreement / pushback handling
5. Status update
```

Wait.

## Step 3 — Load framing language

Load `stakeholder/expectations.md` for the camp-specific framing.

For each camp the user might address:
- **Over-believer** — gentle reality check + "three reasons that survive scrutiny"
- **Skeptic** — partial agreement + three reasons to ship anyway
- **Pragmatist** — defensive business case (risk mitigation, internal asset, forward-compat insurance)
- **SEO team** — collaboration framing (you encode the routing logic, not "this is SEO work")
- **Leadership** — concise honest summary + cost + risk + recommendation
- **Vendor** — polite empirical-basis-request

## Step 4 — Load language-specific template

For English: `stakeholder/email-templates-en.md`
For Turkish: `stakeholder/email-templates-tr.md`

For Turkish business email, observe conventions:
- `the SEO Lead` / `the Sponsor` honorifics for women / men
- Formal `siz` form throughout (`teşekkür ederim`, `incelemeniz`, `paylaştığınız`)
- `Saygılarımla,` closing
- Optional `İyi çalışmalar dilerim` ek nezaket ifadesi
- Technical terms in English (UTF-8, SHA-256, Jira)

## Step 5 — Personalize

Pull from profile:
- Stakeholder names
- Project specifics (file size before/after, link count, issues fixed)
- Decision context (why we're shipping or skipping)
- Empirical citations to anchor honesty claims

Combine template + profile context. Produce a draft.

## Step 6 — Run through honesty checks

Before presenting, run these checks against the draft:

- [ ] No claim of "AI citation lift" or "AI traffic increase"
- [ ] No promise of any traffic
- [ ] Empirical evidence cited where claims are made (three studies, Mueller statements)
- [ ] Three-reasons-that-survive-scrutiny framing for "why ship" if applicable
- [ ] Higher-leverage alternatives mentioned (schema, citations, content quality)
- [ ] Specific operational improvements quantified (e.g., "12.5 MB → 27.8 KB")
- [ ] Stakeholder's specific concern addressed in the draft

If any check fails, revise.

## Step 7 — Present and offer formats

```
Draft email below. Three formats available:

1. Plain-text (paste into Gmail compose)
2. Markdown (for review/iteration)
3. HTML (rich-formatted with tables, colors, code blocks for direct Gmail paste)

Which?

[Draft body]
```

If HTML requested, produce a self-contained HTML file at `[some path]` and offer to open it in browser for preview.

## Step 8 — Iterate

If the user wants changes:

- Tone adjustments (more formal / less formal)
- Different framing for a specific section
- Add / remove specific data points
- Translate to a different language
- Adjust length

Apply changes and re-present.

## Special handling per type

### `--type encoding-issue`

The ExampleMart case revealed a specific pattern: SEO expert reports encoding corruption you can't reproduce. The response should:

1. Thank them for the specific examples
2. List the verification steps performed (UTF-8 check, BOM check, character inventory, paste-pattern search, two-device test, SHA-256 hash)
3. Present findings in a table
4. Conclude the source is clean
5. Attribute observed corruption to display / transit layer
6. Add defensive measures regardless (CI checks, post-deploy hash, alternative transfer)
7. Offer screen-share to verify together

Use `stakeholder/email-templates-tr.md` Template 3 for Turkish; `stakeholder/email-templates-en.md` Template 3 for English.

### `--type disagreement`

When the user needs to respectfully disagree with a stakeholder:

- Open with appreciation for their concern
- Present the evidence (three studies, Mueller, etc.)
- Acknowledge the legitimate uncertainty
- Offer the alternative path
- Close with collaboration offer

Never make the disagreement personal. Always anchor in empirical evidence.

### `--type initial`

For the first email pitching the work:

- Open with thanks + acknowledgment
- Brief problem statement (what's wrong with current state)
- Proposed solution with comparison table
- What it unlocks (real benefits, not AI traffic)
- Honest expectations
- Concrete next steps

### `--type status-update`

For periodic updates to leadership:

- Bullet status (concrete, no embellishment)
- Honest expectations restated
- No action needed flag (or specific asks if any)

## Guardrails

- **Never draft a message that overpromises AI traffic / citations.** Even if the user asks. Push back politely.
- **Never use phrases from the "what NOT to say" list** in `stakeholder/expectations.md` ("this will increase our AI citations", "all the major LLMs will read this", etc.).
- **Match the stakeholder's communication style** from the profile. Don't be overly formal with casual stakeholders, or vice versa.
- **Turkish business emails get full formal respect.** `Hanım`/`Bey` honorifics, `siz` form, `Saygılarımla` closing. No exceptions.
- **Always offer the user the chance to review and revise.** This is a draft for the user to send, not for the skill to send directly.

## Cross-references

- `stakeholder/expectations.md` — framing language per camp
- `stakeholder/email-templates-en.md` — English email patterns
- `stakeholder/email-templates-tr.md` — Turkish email patterns
- `knowledge/02-empirical-evidence.md` — citations
- `case-study/example-marketplace-case.md` — real example arc with Turkish-language responses
