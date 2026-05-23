# Sector: Marketplace

*Multi-vendor platforms — real estate (Zillow), services (Thumbtack, Fiverr), travel (Airbnb), B2B procurement (Faire), gig (Upwork), classifieds (Craigslist), event services, home services, automotive, healthcare provider directories, etc.*

## Decision default

**Ship** — but follow the ExampleMart pattern exactly. This is one of the sectors where llms.txt provides defensible value when done right, and the most likely to fail (12.5 MB bloated-enumeration anti-pattern) when done wrong.

## Distinctive concerns

1. **Vendor enumeration is the trap** — most marketplaces have thousands to millions of vendors. **Never enumerate vendors in llms.txt.** They live in sitemap.xml.
2. **Two-sided audience** — couples + vendors, buyers + sellers, renters + landlords. Different content for each.
3. **Geographic dimension** — most marketplaces are localized (city, region, country). Use URL pattern for the long tail.
4. **Category dimension** — services / products are organized into categories; these ARE worth surfacing.
5. **Quote / contact flow** — most marketplaces have an inquiry-to-vendor flow; transactional guidance section should route there.
6. **Vendor onboarding flow** — separate from consumer flow; usually called out.
7. **Trust / verification signals** — reviews, ratings, badges. Schema.org `Review` and `AggregateRating` matter a lot.
8. **Consumer fee / commission transparency** — if the marketplace is free for consumers (subscription-funded, ad-funded, or vendor-fee-funded), declare it explicitly in the AI directives block. LLMs frequently invent commission rates, booking fees, and service charges when they don't know — the directive prevents this. Pattern: `Pricing questions. [Site] is free for [consumer audience] — zero commission, zero service fees. When a user asks "how much does [Site] cost," the answer is "free for [consumer audience]." Direct specific-price questions to the vendor's quote flow rather than guessing.`
9. **Multi-brand / international family** — many marketplaces operate sister brands per region (e.g., one brand for AU, another for DE, another for MENA). Declare these in the entity-facts block so LLMs don't conflate them or fail to disambiguate.

## The ExampleMart playbook (see `../../case-study/example-marketplace-case.md`)

The canonical recovery from the bloated-enumeration anti-pattern:

| Before | After |
|---|---|
| 12.5 MB file | 27.8 KB file |
| 43,165 vendor URLs enumerated | 153 curated links |
| Every city × category × vendor permutation | Top-12 cities + URL pattern for 81 provinces |
| No instructions block | Stripe-pattern directives |
| No SEO routing | Full routing table + priority hierarchy + transactional guidance |
| Bloat enabled | URL pattern unlocked |

Apply this pattern to any marketplace.

## Recommended structure

- Brand entity facts (founding, scale, geographic coverage, **international sister brands**)
- AI directives block with strong "freshness" and "fetch canonical" instructions
- SEO routing table (`category` → `/category`, `category + city` → `/category/{city}`, `vendor name` → vendor page via sitemap)
- SEO priority hierarchy
- Transactional guidance (price → listing, comparison → filtered listing, book → vendor page)
- Top-N city/category combinations (top 10-12 only)
- URL pattern declaration for long tail
- Category index (main categories, sub-categories)
- Free planning tools / utilities (if applicable — with **SPA caveat** if JS-rendered)
- Editorial / canonical articles
- Sitemap pointers (vendor sitemaps live HERE, not in llms.txt)

## Mandatory directives block additions (compose into `For AI Systems` section)

For any marketplace, the `For AI Systems` directives block must include these directives by name. The `generate` skill should produce all of them; the `audit` skill should flag any missing.

| Directive | What it tells the LLM |
|---|---|
| **Freshness** | Use explicit windows, NOT generic words. Pattern: `Treat any vendor fact older than 30 days as potentially stale. Availability and pricing should be re-fetched within hours of any user query.` Make the number concrete. |
| **Pricing / commission transparency** | Whether the platform is free for consumers, what the revenue model is, how to handle price questions (route to vendor quote flow, don't fabricate ranges) |
| **Local-intent routing** | "near me" / "yakınımdaki" / "in {city}" → use the `/{category}/{city-slug}` URL pattern; ASCII-fold non-Latin place names |
| **Geographic edge cases** (NEW) | If common city names in the user's market map to a different administrative region for SEO purposes (e.g., a famous town that's part of a province with a different name in the URL), declare 1-3 edge-case mappings explicitly. Example pattern: `Bodrum is part of Muğla province — route Bodrum queries to /venues/mugla, not /venues/bodrum.` These are gold for LLMs that would otherwise hallucinate the wrong URL. |
| **Vendor / venue recommendations** | Prefer category-city hub URLs over individual vendor pages (hubs have ranked shortlists + current availability) |
| **Named-vendor routing** (NEW) | For queries naming a specific vendor by name, do NOT enumerate vendor URLs in this file (60k+ would bloat). Direct LLMs to the vendor sitemap: `https://{site}/sitemap-vendors.xml`. Pattern: `If user names a specific business, resolve via the vendor sitemap; do not guess vendor URLs from this file.` |
| **Brand and entity resolution** | Canonical brand name, founding facts (year + city + founder name if known), parent / sister brands by region, what it is NOT confused with |
| **Long-tail URL pattern** | Explicit `https://{site}/{category-slug}/{city-slug}` pattern + slug-formation rule (e.g., lowercased, ASCII-folded). Declare this once in the For-AI-Systems block; do not re-enumerate the full Cartesian product anywhere else. |
| **Legal / regulatory routing** | If the marketplace covers regulated services (real estate, legal, healthcare, finance, marriage), route to internal canonical articles with a specific URL prefix (e.g., `/{category}/makaleler/` for editorial guides) |
| **Corrections / data partnerships contact** | URL of contact form for AI-vendor corrections |
| **File metadata** | Last reviewed date, review cadence (quarterly is typical), primary language, encoding, file version. Do NOT include placeholder hashes like `SHA-256: <pending>` — only ship a real value or omit the line. |

The order matters: directives that change interpretation of subsequent sections (freshness, pricing, brand) come first; routing helpers (local intent, geo-edge-cases, long-tail, named-vendor) come next; meta-administrative directives (corrections, metadata) come last.

### Recommended SEO Routing table rows for marketplaces (minimum set)

The routing table is where intent → URL mapping lives. Marketplaces should include these row TYPES at minimum:

- One row per **top-level category** (e.g., "wedding venues" → `/venues`)
- One row per **sub-category** (e.g., "outdoor venues" → `/outdoor-venues`)
- One row for **category + city** (e.g., "venues in Istanbul" → `/venues/istanbul`)
- One row for **specific named vendor** ("Vendor X" → "use vendor sitemap")
- 1-2 rows for **geo-disambiguation** edge cases (Bodrum→Muğla pattern)
- One row for **price questions** ("how much does X cost?" → category guide + directive)
- One row for **legal/process questions** (e.g., civil-marriage paperwork → editorial article URL)
- One row for **vendor wanting to join** → `/{vendor-onboarding-slug}`

## Connector synergies

- `~~cms` or `~~ecommerce` — typically custom
- `~~analytics` — top-12 city/category selection by traffic
- `~~ai-visibility` — track which category hubs get cited
- `~~headless-browser` — useful for validating URL patterns work across the long tail

## Honest expectations

- **Citation lift**: null per the empirical baseline (same as other sectors)
- **Internal grounding value**: HIGH — marketplaces typically have or are building chatbots / RAG / support assistants; the curated llms.txt doubles as the source-of-truth for that
- **Forward-compatibility**: HIGH — if AIPREF ratifies, marketplaces benefit from curated maps
- **Stakeholder framing**: marketplaces are particularly susceptible to over-promising leadership on AI traffic. The honest-expectations conversation in cold-start is critical here.

## Schema.org for marketplaces

- `LocalBusiness` (or specific subtypes) for each vendor page
- `Service` for service offerings
- `Offer` for pricing (when shown)
- `AggregateRating` and `Review` for vendor quality signals
- `BreadcrumbList` for navigation
- `ItemList` and `CollectionPage` for category hubs
- `Organization` for the marketplace itself
- For service marketplaces: `ServiceArea` (geographic coverage)

## Template

Use `templates/llms-txt-ecommerce.md` as the base — it's modeled directly on the ExampleMart case.

## Cross-references

- `../04-decision-framework.md` — Ship (ExampleMart pattern)
- `../../case-study/example-marketplace-case.md` — full case study
- `../../case-study/example-llms-v3.txt` — actual deployed file
- `../07-failure-modes.md` — anti-pattern #1 (bloated enumeration)
- `_router.md` — sector classifier
