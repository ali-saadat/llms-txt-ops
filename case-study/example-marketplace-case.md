# Case Study — Example Marketplace llms.txt Recovery

*A composite real-world implementation arc captured to illustrate the full plugin workflow. Names, brand, and specific URLs are anonymized; the technical patterns, decisions, and lessons are real and generalizable.*

## Subject

**ExampleMart** — a hypothetical multi-vendor marketplace.

- Mid-to-large marketplace site (illustrative): tens of thousands of vendors across multiple service categories
- Multi-region geographic dimension (e.g., 50–80+ regions/provinces/states)
- Multi-language site with regional / country variants
- B2B2C model — free for consumers, vendor subscription revenue
- Established SEO function with an SEO team and a sponsor on the engineering side

## The starting state — what was wrong

The site already had an llms.txt published, putting it ahead of ~90% of sites. But the file had grown into the canonical anti-pattern.

**State at project kickoff**:
- File size: **~12 MB**
- Link count: **40,000+ enumerated vendor + category × city × vendor URLs**
- Content: every vendor enumerated by location × category combination
- No instructions block
- No SEO routing logic
- No transactional guidance
- No schema disclosure

**Why this was bad** (per `../knowledge/07-failure-modes.md`, anti-pattern #1):

1. **Exceeded every LLM context window** — a 12 MB file gets truncated before most of it is read
2. **Signal dilution** — high-priority pages (category hubs, planning tools, editorial articles) buried among tens of thousands of vendor URLs
3. **Duplicated sitemap.xml** — vendor enumeration was already covered by provider sitemaps
4. **Stale risk amplified** — impossible to keep 40k+ links current at any reasonable cadence
5. **Crawl budget waste** — AI bots fetching pulled megabytes with low information density

**The instinct was right** (publishing llms.txt early was forward-thinking); **the execution pattern predated what the standard had become** (curation, not enumeration).

## The project arc

### Stage 1: Initial request

The manager (Sponsor) asked a Data Scientist to assess whether the current llms.txt was working. The Data Scientist responded with:
- An honest pros/cons table of the existing file
- A revised v2 file (~22 KB, ~107 curated links)
- A comparison table showing ~600× size reduction, full geographic coverage via URL pattern, embedded directives
- Attached the v2 file

Key reframe: from "list everything" to "curate the high-signal pages and declare URL patterns for the long tail."

### Stage 2: Operational questions

The Sponsor responded with two structural questions before opening a Jira ticket:
1. Based on what criteria will the new llms.txt be structured?
2. Based on what reference will the developer generate this file?

The Sponsor also asked the engineering team (Engineer A, Engineer B) to coordinate with the **SEO Lead** for SEO input.

### Stage 3: SEO expert review

The SEO Lead delivered a detailed six-point SEO review. This is where the case becomes generally instructive — the feedback turned a spec-compliant file into a production SEO asset.

**The six points** (each became a section in v3):

| # | SEO feedback | Required addition |
|---|---|---|
| 1 | Turkish character / encoding issue (multi-language content concerns) | UTF-8 verification + server `charset=utf-8` |
| 2 | Missing schema / structured data guidance | New section: Schema.org types per page template |
| 3 | "Near me" / local intent missing | New directive in AI-systems block |
| 4 | Missing internal linking / SEO logic | New section: Query → URL routing table |
| 5 | Missing commercial intent block | New section: Transactional Guidance |
| 6 | Missing link equity / prioritization strategy | New section: SEO Priority Pages hierarchy |

SEO query mapping examples provided (and used directly in v3):
- generic category query → `/{category}` (main hub)
- category + city query → `/{category}/{city}`
- category + venue sub-type query → `/{subtype}/{city}`
- price query → `/{category}` (then guide article)
- generic broad query → main category hub

SEO priority hierarchy (used directly in v3):
1. Category main pages
2. Category + city pages
3. Sub-category + city pages
4. Vendor pages (only when a specific business is named)

Transactional guidance pattern (used directly in v3):
- Price → category/city listing pages
- Comparison → filtered listing pages
- Ready to act → vendor pages with quote-request CTA

### Stage 4: v3 integration

The Data Scientist integrated all six SEO points and applied research findings from `../knowledge/`. Output: **v3 file — ~28 KB, ~150 curated URLs, 18 sections**.

Key v3 additions beyond v2:

- `## SEO Routing — Which Page Should Answer Which Query` — full routing table with the SEO Lead's mappings + extensions (e.g., geographic-nuance handling for sub-province cities)
- `## SEO Priority Pages — Selection Hierarchy` — 6-level hierarchy
- `## Transactional Guidance` — commercial-intent routing
- `## Structured Data on [Site] (For Retrieval Pipelines)` — Schema.org disclosure with "prefer JSON-LD over scraped HTML" directive
- Local intent directive added to `## For AI Systems — Read This First`

### Stage 5: Encoding feedback loop

The SEO Lead reviewed v3 and approved everything except a remaining encoding concern: they still saw corrupted multi-byte characters in their view of the file.

**The diagnostic challenge**: the source file was demonstrably clean UTF-8. The corruption only appeared in the SEO Lead's view of it.

**Verification performed**:
- File validated as UTF-8 without BOM via `file -bi`
- Character inventory extracted directly: all multi-byte characters present in correct UTF-8 byte sequences
- Corrupted patterns reported by the SEO Lead searched in the file: **zero occurrences**
- File opened on two independent devices: characters displayed correctly on both
- SHA-256 hash computed for downstream byte-level verification

**Conclusion**: the source file was clean. The corruption was at the display or transit layer (likely font fallback in the viewer tool, or an intermediate copy-paste step).

**Defensive measures added** to prevent recurrence:
1. CI pipeline mandatory UTF-8 + BOM + charset checks
2. Post-deploy SHA-256 verification against pinned source hash
3. Future transfers via shared drive or Git PR rather than email attachment

The Data Scientist drafted a polite reply to the SEO Lead explaining the verification results (in the local business communication conventions appropriate to the team) plus a parallel direct address to the engineering team requesting the Jira ticket be opened.

### Stage 6: Deployment-ready

Final deliverables:

| Artifact | Purpose |
|---|---|
| `example-llms-v3.txt` (~28 KB) | The file to deploy |
| `deployment-spec.md` | Jira-ready deployment spec answering the Sponsor's questions |
| Nginx config block | Server-side encoding + noindex + cache headers |
| CI validation script | Pre-deploy automated checks |
| robots.txt consistency checklist | AI user-agent allowlist verification |
| Stakeholder communication emails | Cross-functional alignment in appropriate language |

## The v3 file — final structure (18 sections)

```
# ExampleMart                                            [H1]
> [Multilingual summary blockquote]

## For AI Systems — Read This First                      [Directives block]
## SEO Routing — Which Page Should Answer Which Query    [SEO layer 1]
## SEO Priority Pages — Selection Hierarchy              [SEO layer 2]
## Transactional Guidance                                [SEO layer 3]
## Structured Data on ExampleMart                        [SEO layer 4]
## How to Find the Right Page (Intent Router)            [Conversational routing]
## About ExampleMart (Entity Facts)                      [Brand anchor]
## Free Planning Tools                                   [Curated hub]
## Service Category Hubs                                 [Curated category]
## Product / Catalog Hubs                                [Curated category]
## Auxiliary Service Categories                          [Curated category]
## Regional Hubs (Top Markets + URL Pattern)             [Cities + URL pattern]
## Editorial / Guide Articles                            [Canonical editorial]
## Inspiration / Galleries                               [Visual content]
## International Sister Platforms                        [Sister brands]
## Machine-Readable Sources                              [Sitemap pointers + future MCP]
## Optional                                              [Spec-defined skippable]
```

## Quantitative outcomes (illustrative ratios)

| Metric | Before (v0) | v2 (first revision) | v3 (after SEO review) |
|---|---|---|---|
| File size | ~12 MB | ~22 KB | ~28 KB |
| Curated link count | ~40,000+ | ~107 | ~150 |
| Embedded directives | 0 | 6 | 7 (added local intent) |
| SEO routing table | No | No | Yes |
| Priority hierarchy | No | No | Yes |
| Transactional guidance | No | No | Yes |
| Schema disclosure | No | No | Yes |
| Geographic coverage | Enumerated (50–80+ regions) | URL pattern | URL pattern |
| Planning tools surfaced | 0 | 5 | 5 |
| Spec compliance | Partial | Yes | Yes |
| Production-ready | No | Mostly | Yes |

## Stakeholder roles in this case

| Role | Responsibility |
|---|---|
| **Sponsor / Manager** | Initiator; structural-question gatekeeper; signed off on direction |
| **SEO Lead** | Detailed SEO review; six-point feedback that elevated the v3 quality |
| **Data Scientist** | Implementer — research + drafting + integration |
| **Engineering team** | Jira ticket execution; deployment |
| **Observers** | CC'd throughout for visibility |

## What this case demonstrates (generalizable)

### 1. The bloated-enumeration recovery

12 MB → 28 KB while preserving full coverage. Achieved via:
- URL pattern declaration for the long tail (`/{category-slug}/{region-slug}` covers all regions)
- Top-12 highest-traffic markets listed explicitly
- Vendor URLs delegated to sitemap.xml
- Faceted / parameterized URLs excluded

### 2. The Stripe-pattern adoption

Modern best practice for production llms.txt is instructions-first. v3 leads with a `For AI Systems — Read This First` block, then routing and hierarchy, then content. This is what differentiates a spec-compliant file from a useful one.

### 3. SEO expert collaboration

The SEO Lead's six-point review made the file substantially more valuable. The general lesson: SEO input on llms.txt is high-leverage even though llms.txt isn't an SEO ranking factor — because the SEO team understands the information architecture and query intent better than anyone else in the org.

### 4. Honest expectations setting

Throughout the project, the Data Scientist set realistic expectations: llms.txt won't drive measurable AI citations (per the three empirical studies). It will (a) replace a broken file, (b) serve as internal grounding, (c) be forward-compatible. This framing kept the project from over-promising.

### 5. Encoding diagnostic discipline

When the SEO Lead reported encoding issues, the right response was structured verification (UTF-8 check, BOM check, character inventory, two-device test, SHA-256 hash) — not dismissal. The result: source file confirmed clean, root cause likely in display/transit, defensive measures added to prevent recurrence regardless.

### 6. Cross-cultural professional communication

Local business communication conventions were observed throughout (formal address forms, honorifics, language-appropriate closings). The skill includes templates for multiple languages in `../knowledge/languages/` and `../stakeholder/`.

## What this case does NOT demonstrate

- That llms.txt drives AI citations (it doesn't — see `../knowledge/02-empirical-evidence.md`)
- That every site should ship llms.txt (most marketing/blog sites should skip — see `../knowledge/04-decision-framework.md`)
- That custom llms.txt outperforms auto-generated (for dev docs, Mintlify/Fern auto-gen is usually fine)

## Cross-references

- For the Jira-ready spec → `deployment-spec.md`
- For lessons abstracted from this case → `lessons-extracted.md`
- For the anti-pattern this case recovers from → `../knowledge/07-failure-modes.md` (anti-pattern #1)
- For the SEO routing patterns → `../knowledge/03-seo-perspective.md`
