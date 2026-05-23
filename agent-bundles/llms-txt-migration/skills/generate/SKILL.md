---
name: generate
description: >
  Generate a new llms.txt file from scratch based on the user's practice profile.
  Use when the user says "create our llms.txt", "generate llms.txt", "make me an
  llms.txt", "draft a file for us", "build the llms.txt", "produce the llms.txt",
  or after `/audit` recommends regeneration ("--from-audit"). Produces a complete
  file ready for deployment, plus optional deployment spec and stakeholder
  communication drafts based on profile preferences. **Default file language is
  English** unless user explicitly requests another language via `--language <code>`
  or has set a non-English preference in their profile.
argument-hint: "[--from-audit to start from an audit report's findings] [--quick for minimal file] [--full for complete Stripe-pattern file] [--language <code> to override default English]"
---

# Generate — Create an llms.txt File

## Step 1 — Profile check

Same bounce-on-placeholder pattern. If `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` has placeholders, bounce to `/llms-txt-advisor:cold-start-interview`. PROVISIONAL mode allowed but the resulting file will be generic.

If the user passed `--from-audit`, also load the most recent audit report from the conversation context and apply its critical + high-severity fixes.

## Language for the generated file

Apply the language policy from `../../knowledge/languages/_router.md`:

1. If user passed `--language <code>` in this invocation → use that
2. Else if user explicitly requested another language in this conversation ("generate it in Spanish") → use that
3. Else if profile's `Primary language` (for file content) is set and not English → use that
4. **Otherwise: default to English** (the safe default; LLM crawlers process English best)

**Confirm with user before generating** if there's ambiguity:

> "I'll generate the file in English (the default). Want me to use [their site's language] instead? Most multilingual sites use English for llms.txt with an optional second-language summary in the blockquote."

Only auto-select non-English if profile is explicit OR the user requested it in this turn.

## Step 2 — Select template + sector references

Read the user's profile `Site type` field. Map to template + load the sector-specific guidance:

| Site type | Template file | Sector guidance to load |
|---|---|---|
| Developer documentation | `templates/llms-txt-dev-docs.md` | `knowledge/sectors/dev-docs.md` |
| Marketing site / blog | `templates/llms-txt-marketing.md` | `knowledge/sectors/marketing.md` (with strong push to skip per decision framework) |
| E-commerce | `templates/llms-txt-ecommerce.md` | `knowledge/sectors/ecommerce.md` |
| Marketplace | `templates/llms-txt-ecommerce.md` (ExampleMart pattern) | `knowledge/sectors/marketplace.md` |
| News / publisher | `templates/llms-txt-marketing.md` adapted | `knowledge/sectors/news-publisher.md` |
| Mixed | `templates/llms-txt-generic.md` | `knowledge/sectors/generic.md` |
| Any other sector | `templates/llms-txt-generic.md` | matching sector file from `knowledge/sectors/` |

**Critical**: load the sector file's `Mandatory directives block additions` section (if present) — those directives MUST be in the output. The marketplace sector has 9 mandatory directives; do not omit any.

If marketing/blog and user has no compelling reason from Part 1 of cold-start, re-confirm with one question before proceeding:

> "Your profile says this is a marketing/blog site, and the decision framework default for that is 'skip llms.txt'. Are you sure you want to proceed? The empirical evidence shows no AI-citation lift for this site type."

Wait. If they confirm, proceed.

## Step 3 — Pass 1: Build the section outline + URL inventory

**Do not start writing the file yet.** First produce a structured outline that enumerates every required section and every URL that will appear. This prevents under-generation.

Produce internally (need not show to user) a section inventory like this:

```yaml
sections:
  - H1_block:
      title: "[Site name]"
      bilingual_summary_blockquote: required if profile.primary_languages includes non-English
      english_summary_blockquote: required always
  - for_ai_systems:
      directives:
        - Freshness          # required for any sector with changing data
        - Pricing/commission # required for marketplaces (per sector guidance)
        - Local intent       # required if profile.geography is multi-region
        - Brand resolution   # required always (entity disambiguation)
        - URL pattern        # required if profile.long_tail > 100 items
        - File metadata      # required always
        # + sector-specific mandatory directives loaded in Step 2
  - seo_routing_table:
      target_rows: 15-25 query-to-URL pairs covering every category + every sub-category in profile
  - seo_priority_pages:
      hierarchy_depth: 5 levels minimum
  - transactional_guidance:
      required: site_type in {ecommerce, marketplace}
  - structured_data_section:
      required: profile.schema_org_types is non-empty
      table_rows: 1 per page template type from profile
  - intent_router:
      target_intents: 5-10 named user intents with route URL
  - entity_facts:
      structured_bullets: required
      facts_to_include:
        - Founded (year + location)
        - Founder name (if known)
        - Headquarters
        - Team size (if known)
        - Business model
        - Monthly users / scale metric
        - Market share (if known)
        - Vendor / inventory count
        - Geographic coverage
        - Recognition / certifications
        - International sister brands (if any)
  - category_sections:
      # ONE section per top-level category FAMILY from profile.information_architecture.top_level_categories
      # Within each, list ALL sub-categories from the profile (do not abbreviate)
  - planning_tools:
      required: profile.information_architecture.planning_tools is non-empty
      enumerate: every tool from profile with its URL + 1-line description + SPA caveat if JS-rendered
  - editorial_articles:
      enumerate: every canonical article from profile.information_architecture.editorial_articles
  - inspiration_galleries:
      required: profile.has_real_stories_or_galleries
  - machine_readable_sources:
      sitemaps_list: required
      schema_org_pointers: required
  - optional_section:
      contents: lower-priority pages, vendor-onboarding link, sister-brand pointers
```

Now compute a URL inventory:

```
URL_inventory:
  category_hubs: [N URLs — one per top-level category]
  sub_category_hubs: [M URLs — one per sub-category]
  geographic_top_metros: [12 URLs — top-12 cities × top-3 categories = 36 max]
  planning_tools: [K URLs — every tool from profile]
  editorial_articles: [E URLs — every canonical article from profile]
  brand_pages: [hakkimizda / iletisim / isortagim / privacy]
  international_brands: [J URLs — one per sister brand]
TOTAL_target: typically 100-200 unique URLs for a marketplace site
```

If the total is < 80 URLs for a marketplace site, **the IA enumeration is too thin** — go back to the profile and re-extract every category, every sub-category, every editorial article.

## Step 4 — Pass 2: Render the file

With the inventory complete, render the file in this canonical order:

1. **H1 + bilingual summary blockquote** (English mandatory; secondary language if profile is multilingual)
2. **`## For AI Systems — Read This First`** — full Stripe-pattern directives block, including ALL sector-mandatory directives loaded in Step 2
3. **`## SEO Routing — Which Page Should Answer Which Query`** (commercial sites only — always include for ecommerce/marketplace)
4. **`## SEO Priority Pages — Selection Hierarchy`** (same condition)
5. **`## Transactional Guidance`** (ecommerce + marketplace only)
6. **`## Structured Data on [Site Name]`** (if profile has schema types declared)
7. **`## How to Find the Right Page (Intent Router)`** — concrete intents → URLs
8. **`## About [Site Name] (Entity Facts)`** — structured bullets, NOT prose
9. **`## Free Planning Tools for Couples`** (or sector-appropriate label) — every tool enumerated with SPA caveat if applicable
10. **One section per top-level category family** — e.g. for a services marketplace: `## Venue Categories`, `## Vendor Profiles`, `## Service Categories` — every sub-category enumerated. Use the user's actual category names from their profile, not the generic placeholders.
11. **`## City-Level Coverage` or `## Geographic Coverage`** — top-12 metros + URL pattern for the long tail
12. **`## Editorial — Canonical Internal Sources`** — every article from profile listed
13. **`## Inspiration and Galleries`** — if profile has any
14. **`## International Sister Platforms`** — if applicable
15. **`## Machine-Readable Sources`** — sitemap pointers, schema.org pointers
16. **`## Optional`** — lower-priority pages, vendor onboarding, privacy

## Step 5 — Completeness validation (do this BEFORE presenting)

Before showing the file to the user, check the rendered output against the inventory:

| Check | Threshold |
|---|---|
| H1 count | exactly 1 |
| `## Optional` section present | yes (spec-required) |
| Total URLs in file | matches inventory ±5 |
| Entity facts block present as bulleted list | yes |
| Per-category sections from inventory | every one rendered |
| Editorial articles from inventory | every one rendered (no "see the editorial directory" abbreviation) |
| Mandatory directives from sector file | all present in the For AI Systems block |
| File size | 20-50 KB (sweet spot); >50 KB triggers Step 7 curation |
| URL count | ≥ 80 for marketplaces, ≥ 30 for dev-docs, ≥ 50 for ecommerce |

If any check fails, **regenerate the failing section** before showing.

## Step 6 — Apply the SEO integration layer (commercial sites)

If site type is e-commerce, marketplace, or mixed-commercial, the following sections are mandatory regardless of whether the user explicitly asked:

- `## SEO Routing — Which Page Should Answer Which Query` — query → URL mappings
- `## SEO Priority Pages — Selection Hierarchy`
- `## Transactional Guidance`
- `## Structured Data on [Site]`

For developer documentation: omit transactional guidance.

For marketing-only: omit SEO routing and transactional.

## Step 7 — Size budget enforcement

After draft, check:

- Total size ≤ 50 KB target
- If > 50 KB: identify highest-bloat section, apply URL-pattern technique, reduce
- If > 200 KB: hard fail, ask user where to cut

Common bloat sources:
- Top-N metros listed beyond 12 — keep to 12, defer rest to URL pattern
- Vendor enumeration that snuck in — strip, route to sitemap
- Verbose descriptions — tighten to literal "what's on the page"

## Step 8 — Spec-shape validation

Run the validation checks in-mind (or actually run `templates/validate.sh` against a saved draft):

- Exactly one H1
- `## Optional` section present (case-sensitive)
- All URLs look real (matches profile domain)
- No marketing-speak (`revolutionize`, `cutting-edge`, etc.)
- No `User-agent:` directives (would indicate robots.txt confusion)
- No phone-number patterns inline next to vendor URLs (anti-pattern #16)
- File is plain markdown, not RTF/HTML/PDF (anti-pattern #17)

If any check fails, fix before presenting.

## Step 9 — Present the file

Show the file inline in chat with a structured summary:

```
Generated llms.txt for [site domain]:
- Size:                X KB
- Total URLs:          N (matches inventory: ✓)
- Sections:            M
- Mandatory directives: K/K from sector file
- Entity facts:        present as structured bullets
- SEO integration layer: included
- Anti-pattern checks (validate.sh): all pass
- Compared to gold-standard size band (20-50 KB): in range

[File contents]
```

Then ask:

> "Three options:
> 1. **Save to disk** — I'll write to `[path from profile]/llms.txt`. Confirmed?
> 2. **Iterate on a specific section** — tell me what to change.
> 3. **Continue to deployment guidance** → `/llms-txt-advisor:deploy`"

Wait.

## Step 10 — Save and offer deployment

On confirmation:

1. Write the file to the path specified in the profile (or ask if not specified).
2. Compute and display the SHA-256 hash. Tell the user to pin this in the deployment ticket.
3. Offer: *"Want me to also produce the deployment spec and CI validation pipeline integration? → `/llms-txt-advisor:deploy`"*
4. If profile has `Should I draft stakeholder communication: yes`, offer: *"Want me to draft the email to your stakeholders too? → `/llms-txt-advisor:stakeholder-comms`"*

## Special handling: --from-audit

If invoked with `--from-audit`, retrieve the audit findings from prior context. For each critical + high-severity finding, ensure the new file:

- 🔴 Bloated enumeration (#1) → applies URL pattern
- 🔴 Non-markdown format (#17) → produced as plain UTF-8 markdown
- 🔴 PII leakage (#16) → no phone numbers inline; routes contact via vendor page
- 🔴 Encoding broken (#10) → UTF-8 without BOM
- 🟠 Marketing-speak (#3) → all descriptions concrete
- 🟠 No instructions block → adds Stripe-pattern block
- 🟠 robots.txt inconsistency (#2) → flag in output (cannot fix robots.txt from this skill, but warn)

Include a "Changes from audit" summary block in the response.

## Guardrails

- **Never include vendor / product page enumerations.** Even if the user asks. Delegate to sitemap.xml.
- **Never include faceted URLs or login pages.**
- **Never include inline phone numbers next to vendor URLs.** (#16)
- **Marketing descriptions are rejected.** Rewrite as concrete content descriptions.
- **Entity facts must be a bulleted list, not prose.** Each fact is one line: `- Field: value`.
- **Per-category sections are mandatory** for marketplaces — every top-level category in the profile gets its own H2 section.
- **Never fabricate URLs.** Every URL in the output must come from the profile. Do not invent slugs, IDs, or article paths. If the profile says `/category/makaleler/article-slug-1234`, copy it character-for-character — no substitutions like `a-den` for `a-dan`, no made-up article IDs.
- **Never invent editorial articles.** If the profile lists 11 articles, output exactly 11 articles. Do not add "for completeness" or "as a related guide."
- **The file is a draft for human review.** Treat it that way — present, don't commit silently.

## Common under-generation symptoms (and what causes them)

| Symptom | Cause | Fix |
|---|---|---|
| File is 60% of target size | Skipped Step 3 inventory | Re-run Step 3, then Step 4 |
| Entity facts buried in prose | Wrote summary paragraph instead of bullets | Re-render that section as `- Field: value` lines |
| Editorial section says "see the directory" | Skipped per-article enumeration | Re-render with every article from profile |
| Single "Top Categories" section instead of per-family | Merged categories | Split into 1 section per top-level category family |
| URL count under inventory target | Skipped sub-categories | Re-enumerate from profile.information_architecture |

## Cross-references

- `templates/llms-txt-generic.md` and siblings — starting points
- `templates/llms-txt-ecommerce.md` — the marketplace skeleton (ExampleMart pattern)
- `knowledge/05-implementation.md` — the structural guide
- `knowledge/03-seo-perspective.md` — SEO integration layer
- `knowledge/07-failure-modes.md` — anti-patterns to avoid in generated output
- `knowledge/sectors/marketplace.md` — mandatory directives + structure for marketplaces
- `case-study/example-marketplace-case.md` — the canonical worked example for content depth comparison
