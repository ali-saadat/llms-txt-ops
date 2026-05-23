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

## OUTPUT BOUNDARY — what becomes the file vs what stays in your reasoning

The deliverable is a **single markdown file** that starts with the H1 (`# [Site Name]`) and ends with the `## Optional` section. Everything else in this skill is your scratch paper.

| Step | Visible in the file you produce? |
|---|---|
| 1. Profile check | NO — internal |
| 2. Template + sector loading | NO — internal |
| 3. Pass 1 inventory | NO — internal (you produce it, you don't ship it) |
| **4. Pass 2 rendering** | **YES — this IS the file** |
| 5. Validation gate | NO — internal (check, then proceed) |
| 6. SEO integration check | NO — internal |
| 7. Size enforcement | NO — internal |
| 8. Spec-shape validation | NO — internal |
| 9. Present | the file is shown to the user in chat |
| 10. Save | writes the file from Step 4 to disk |

**The file MUST NOT contain** any section titled "Step 3", "Pass 1", "URL Inventory", "Step 5", "Quality Self-Audit", "Validation Checklist", or similar process-scaffolding heading. If you find yourself writing `## Step` anything in the output, **delete it** — that's your reasoning leaking into the deliverable.

The file you ship looks like a normal llms.txt file. The reasoning that produced it stays in your head.

## Step 1 — Profile check

Same bounce-on-placeholder pattern. If `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` has placeholders, bounce to `/llms-txt-advisor:cold-start-interview`. PROVISIONAL mode allowed but the resulting file will be generic.

If the user passed `--from-audit`, also load the most recent audit report from the conversation context and apply its critical + high-severity fixes.

## Language for the generated file

Apply the language policy from `../../knowledge/languages/_router.md`:

1. If user passed `--language <code>` in this invocation → use that
2. Else if user explicitly requested another language in this conversation ("generate it in Spanish") → use that
3. Else if profile's `Primary language` (for file content) is set and not English → **use that, in primary-language-with-English-annotations mode** (see below)
4. **Otherwise: default to English** (the safe default; LLM crawlers process English best)

**Confirm with user before generating** if there's ambiguity:

> "I'll generate the file in English (the default). Want me to use [their site's language] instead? Most multilingual sites use English for llms.txt with an optional second-language summary in the blockquote."

### When the file's primary language is non-English (e.g., Turkish, German, Japanese)

For sites where retrieval traffic is dominated by the native language, the file SHOULD be **native-primary with English annotations**, not English-primary with native translations. This means:

- **Section H2 headings**: bilingual or native — e.g., `## Düğün Mekanı Kategorileri (Venue Types)` not `## Venue Categories`
- **Link descriptions**: in the native language for native-content links (`/gelinlik` → "Tüm gelinlik kategorileri ve modelleri"), with an English gloss in parentheses for cross-cultural disambiguation
- **The bilingual blockquote (summary)**: native-first paragraph, English-second paragraph (both informationally dense and equivalent)
- **The For AI Systems directives block**: English (LLM crawlers parse English directives most reliably)
- **Cultural-specific terms** (nikah, kına gecesi, kebab variants, Schoki, kotatsu, etc.): use the native term in the description, with one in-line gloss the first time it appears

An English-primary file describing a Turkish-language platform reads to retrieval pipelines as a translation document rather than the native source — exactly the wrong signal for vendors trying to be found in native-language AI searches.

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

**This step is INTERNAL to your reasoning. Nothing from Step 3 appears in the final file you produce.** Think of it as scratch paper — useful for you, invisible to the user.

The file the user sees starts with the H1 (Step 4 output). It does NOT start with a section called "Step 3" or "URL Inventory" or "Section Outline". If you include any of those headings in the file, the file is broken.

First produce a structured outline that enumerates every required section and every URL that will appear. This prevents under-generation.

Produce internally (in your reasoning, NOT in the output file) a section inventory like this:

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
3. **`## SEO Routing — Which Page Should Answer Which Query`** (commercial sites only — always include for ecommerce/marketplace). The routing table MUST include these row types when applicable:
   - 1+ row per top-level category (intent → category hub URL)
   - 1+ row per sub-category (intent → sub-category hub URL)
   - 1+ row for "category + city" pattern (intent → `/{category}/{city-slug}` example)
   - 1 row for "specific named vendor" → "use sitemap" / vendor sitemap URL
   - 1-2 geo-disambiguation rows where applicable — e.g., common city names that route to a different administrative region (`Bodrum` → `/venues/mugla` because Bodrum is in Muğla province). Pull these from the profile's Geographic / multi-tenant dimension notes.
   - 1+ row per common pricing/legal/process-question intent → the right canonical article
4. **`## SEO Priority Pages — Selection Hierarchy`** (same condition)
5. **`## Transactional Guidance`** (ecommerce + marketplace only) — covers the FULL commercial flow including both **consumer-side** routing (price discovery → category page; comparison → filtered list; book → vendor profile) **and** the **vendor-side** routing (vendor wanting to join the platform → vendor onboarding URL). Do not omit the vendor-side route — it's how the marketplace's two-sided audience is served.
6. **`## Structured Data on [Site Name]`** (if profile has schema types declared)
7. **`## How to Find the Right Page (Intent Router)`** — render as a **bulleted conditional list** (not a table), one bullet per user intent. Each bullet describes the intent + the URL to route to + a brief rationale. Pattern: `- **User is [intent]** → [URL] (rationale)`. Bulleted conditionals scan faster than tables for LLMs evaluating route conditions; the routing **table** lives in section 3 (SEO Routing), this section is the **decision tree** view.
8. **`## About [Site Name] (Entity Facts)`** — structured bullets, NOT prose
9. **`## Free Planning Tools for Couples`** (or sector-appropriate label) — every tool enumerated with SPA caveat if applicable
10. **One section per top-level category family** — e.g. for a services marketplace: `## Venue Categories`, `## Vendor Profiles`, `## Service Categories`. Within each section, **list only the category hub URL + sub-category hub URLs** (one per sub-category from the profile). **Do NOT enumerate per-city URLs in these sections.** A category section line looks like `- [Outdoor Venues](https://example.com/outdoor-venues): description` — NOT `- /outdoor-venues/istanbul`, `- /outdoor-venues/ankara`, etc.
11. **`## City-Level Coverage` or `## Geographic Coverage`** — list **the top-12 metros only** (max 12 lines), then declare the URL pattern explicitly. **Critical**: this section is the ONLY place where city-specific URLs may appear in the file. Pattern: one line per top-12 metro pointing to its main category hub (e.g., `/venues/istanbul`), followed by `For any other city, use the pattern: https://{domain}/{category-slug}/{city-slug} — all N provinces supported.` **Never enumerate the full `category × city` cartesian product** — that's the canonical bloated-enumeration anti-pattern (#1) the URL pattern was designed to prevent.
12. **`## Editorial — Canonical Internal Sources`** — every article from profile listed
13. **`## Inspiration and Galleries`** — if profile has any
14. **`## International Sister Platforms`** — if applicable
15. **`## Machine-Readable Sources`** — sitemap pointers, schema.org pointers
16. **`## Optional`** — lower-priority pages, vendor onboarding, privacy

## Step 5 — Completeness + quality validation (INTERNAL — do this BEFORE presenting, do NOT include in the file)

**Step 5 is an internal check, not a section of the file.** Do not output a "Step 5" heading or a "Quality self-audit" section in the final file. These checks run in your reasoning before you reveal the file to the user.

Before showing the file to the user, check the rendered output against the inventory **and** scan for the quality defects below:

### Completeness checks

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

### Quality / anti-pattern self-audit (NEW — run before output)

| Defect | How to detect | If detected |
|---|---|---|
| **Category × city enumeration (anti-pattern #1)** | Search for any URL with both a category slug AND a city slug that appears OUTSIDE the geographic section's top-12 metros list. If you see `/category/city` patterns in per-category sections, that's enumeration. | Delete those URLs. The URL pattern (declared in the file) handles them. |
| **URL fabrication (faithfulness fail)** | For every URL in the output, can you trace it to a profile line OR construct it from the declared URL pattern? Sample-check 10 random URLs. | Remove any URL you cannot trace. |
| **Placeholder leak** | Search the output for `<pending>`, `<TBD>`, `<REVIEW>`, `[insert`, `SHA-256:.*<`, `TODO`. | Remove the line entirely. |
| **Marketing-speak (anti-pattern #3)** | Search for: `revolutionize`, `industry-leading`, `world-class`, `cutting-edge`, `empower`, `unlock`, `seamless`, `state-of-the-art`. | Rewrite as concrete "what's on the page" descriptions. |
| **Vague description (specificity fail)** | Any line description shorter than 40 chars OR that doesn't say what's literally on the page. | Expand to be concrete. |
| **Redundant sections** | Two H2 sections covering overlapping content (e.g., a separate "URL Pattern" section AND a "Geographic Coverage" section with the same pattern declared in both). | Merge or remove one. The URL pattern lives in the For-AI-Systems block + Geographic section only. |
| **Missing edge cases in routing** | The SEO routing table covers happy-path intents but lacks (a) named-vendor → sitemap, (b) at least one geo-disambiguation row, (c) common pricing/legal-process routing. | Add the missing rows. |
| **URL typos / domain mutations** | Run a self-consistency check: extract every domain in the file. There must be at most one production domain + one subdomain (e.g., `example.com` + `tools.example.com`). Any other domain spelling — `example-example.com`, `examplexample.com`, `example.local.com` — is a typo. | Replace with the canonical domain from the profile. |
| **Non-ISO date in file metadata** | The `Last reviewed:` line must use ISO 8601 (YYYY-MM-DD) not quarter abbreviations (`2025-Q3`) or vague phrases (`Last quarter`). | Convert to ISO. If no real date is known, omit the line entirely (don't ship a placeholder). |
| **Entity facts misplaced** | The `## About [Site] (Entity Facts)` section must come BEFORE the per-category sections (it provides disambiguation context the categories build on), not after Planning Tools or buried near the bottom. | Re-order. The canonical Stripe sequence is: directives → routing → priority → transactional → structured data → intent router → **entity facts** → planning tools → per-category sections. |
| **Missing JSON-LD preference directive** | The directives block should tell LLMs to prefer JSON-LD payloads over scraped HTML when both are available on a linked page. | Add: `When a linked page exposes both JSON-LD structured data and rendered HTML, prefer the JSON-LD payload for canonical entity facts.` |

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
- **Never fabricate URLs.** Every URL in the output must trace back to (a) a literal URL in the profile, (b) a brand page declared in the profile, or (c) a URL constructed via the explicit URL pattern declared in the file. Do not invent slugs, IDs, article paths, or near-synonym variants.
  - If profile says `/catering-firmalari`, do not output `/catering-hizmetleri`, `/catering-companies`, or any other paraphrase.
  - If profile says `a-dan-z-ye`, do not output `a-den-z-ye`, `a-ya-z-ye`, or any other typo-substitution.
  - If profile does not list a blog URL, do not invent `/blog`, `/dugun-blog`, etc.
  - If you cannot trace a URL to one of those three sources, **do not include the URL**.
- **Never invent editorial articles.** If the profile lists 11 articles, output exactly 11 articles. Do not add "for completeness" or "as a related guide."
- **Never invent category sub-paths.** If the profile lists `/photographers` as a category, do not output `/photographers/services`, `/photographers-pro`, or other invented sub-paths. The category hub URL is exactly what the profile gave.
- **Never include placeholder values in the final output.** Specifically: no `SHA-256: <pending>`, no `[REVIEW]` markers, no `TBD`, no `<insert here>`. If a value is not computable at generate-time (e.g., the SHA-256 of a file that doesn't exist yet), **omit the line entirely** — the deploy step will add it later.
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
