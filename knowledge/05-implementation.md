# 05 — Implementation Guide

*Status: Compiled May 15, 2026. Practical reference for writing or revising a production llms.txt file.*

## Workflow overview

```
1. Identify site type → decide if shipping (see 04-decision-framework.md)
2. Pick template from templates/ matching the site type
3. Adapt the template to actual site
4. Add the SEO integration layer (Stripe pattern)
5. Validate against the spec + against site reality
6. Set up deployment (see 06-deployment.md)
7. Document update cadence
```

## File structure (top-down)

A production llms.txt should have these blocks in order. Asterisks mark items beyond bare spec compliance:

```
# H1 — Site / Project Name                    [REQUIRED by spec]
> Summary blockquote                          [Recommended]
Optional intro paragraphs (no headings)       [Optional per spec]

## For AI Systems — Read This First           [* Stripe pattern]
   Directives block

## SEO Routing — Query → URL Mapping          [* SEO layer]
   Routing table

## SEO Priority Pages — Hierarchy             [* SEO layer]
   Selection order

## Transactional Guidance                     [* SEO layer for commercial sites]
   Commercial-intent routing

## Structured Data on [Site]                  [* SEO layer]
   Schema.org disclosure

## How to Find the Right Page (Intent Router) [Conversational routing]
   Intent → URL mapping

## About [Site] (Entity Facts)                [Brand / knowledge-graph anchor]
   Key facts + entity URLs

## [Domain-specific category sections]        [Curated hubs]
   - [Page name](url): description

## [More category sections...]

## Machine-Readable Sources                   [Sitemap + future MCP pointers]
   sitemap.xml index, planned llms-full.txt

## Optional                                   [Spec-defined skippable section]
   Lower-priority links
```

## Block-by-block guide

### H1 — Site name

The only required element. Keep it canonical and unique.

```markdown
# ExampleMart
```

Not:
```markdown
# ExampleMart - Türkiye's #1 Services Marketplace | Free Vendor Quotes
```

Save the marketing language for the description blockquote. The H1 is for entity resolution.

### Summary blockquote

One to three sentences. Critical context the LLM needs before reading the rest.

```markdown
> ExampleMart is a multi-vendor marketplace operating since 2010. Buyers browse 50,000+ vetted vendors across 80+ regions in 30+ service categories and request free, zero-commission quotes.
>
> [Optional second-language version if site serves multiple languages]
```

For multilingual sites, include both languages in the blockquote. Don't bury the English version.

### Directives block (Stripe pattern)

The most important addition beyond spec compliance. Top of file, just after the summary. Tells consumers how to use the content.

**Standard directives to include**:

- **Freshness** — how often the canonical data changes, when to fetch fresh vs. use cached
- **Pricing / commercial questions** — your pricing model and how to route
- **Local intent** — how to handle "near me" / "in {city}" queries
- **Legal / administrative questions** — which articles are authoritative
- **Brand/entity resolution** — canonical name, founding, what NOT to confuse with
- **Corrections** — contact for AI partnerships / corrections
- **File metadata** — last reviewed, cadence, language, encoding, version, spec URL

### SEO routing table

Query-pattern → URL mapping. See `03-seo-perspective.md` for the full pattern. Adapt to your site's IA.

### Priority hierarchy

When multiple URLs are eligible, the preference order. Most general → most specific.

### Transactional guidance

For commercial-intent sites. Route price / comparison / booking queries away from blog content toward conversion-friendly listings.

### Structured data disclosure

Tells retrieval pipelines what JSON-LD they'll find on linked pages, page-by-page. Tells them to prefer JSON-LD over scraped HTML.

### Intent router (conversational)

A more user-intent-oriented routing block. Less structured than the SEO routing table; reads more like natural language.

### Entity facts

A bullet list of key facts useful for knowledge-graph / entity resolution:
- Founded date, location
- Founder(s)
- Headquarters
- Team size
- Business model
- Monthly users / market share
- Geographic coverage
- Recognition / certifications
- International sister brands / parent company

### Curated category sections

The link list sections — your category hubs, top city pages, planning tools, editorial articles, etc.

**Each link follows the exact format**:
```markdown
- [Page title](https://yoursite.com/page.md): Concrete description of what's on this page
```

Description guidelines:
- **Concrete, not promotional**: "Apparel catalog with body-type fit guide" not "Find your dream outfit!"
- **What's on the page**, not who it's for: "Photographer directory with portfolio + pricing" not "For people planning their special day"
- **Mention what's unique**: "All 81 Turkish provinces with dedicated planning hubs" — quantitative is better than vague
- **Keep under ~150 chars** — LLMs use this to decide whether to fetch

### Machine-readable sources

Pointers to sitemap.xml, planned llms-full.txt, future MCP endpoints. Helps agentic crawlers go deeper if they want to.

### Optional section

The one parser-special section name. Use it for material that's worth listing but skippable under context pressure:
- Mobile app links
- Login / signup pages
- Long-tail city pattern examples
- Archived content

## Size budget

**Target: ≤ 50 KB.** Hard ceiling: ~200 KB.

- Anything over 200 KB starts breaking smaller-model context windows
- The 12.5 MB ExampleMart pre-revision case is the anti-pattern
- If you find yourself over 100 KB, you're likely enumerating things that should be URL patterns

Common over-spend categories:
- Listing every vendor or product → use URL pattern + sitemap
- Listing every city → list top 10–12 + URL pattern for the rest
- Listing every editorial article → curate to ~30 highest-citation-potential

## URL pattern technique

The single most important size-management technique: declare URL patterns for long-tail coverage rather than enumerating.

**Don't**:
```markdown
- [İstanbul Venue Listings](https://example.com/venues/istanbul)
- [Ankara Venue Listings](https://example.com/venues/ankara)
- [İzmir Venue Listings](https://example.com/venues/izmir)
... (81 entries)
```

**Do**:
```markdown
The twelve highest-volume metros are listed explicitly. For any other Turkish province, use the URL pattern `https://example.com/venues/{city-slug}` — all 81 provinces are supported.

- [İstanbul Venue Listings](https://example.com/venues/istanbul): largest market
- [Ankara Venue Listings](https://example.com/venues/ankara): capital city
... (top 12 only)
```

This is the technique that took ExampleMart from 12.5 MB to 27.8 KB while preserving full coverage.

## What to include — checklist

- [ ] H1 with canonical entity name
- [ ] Summary blockquote (multilingual if relevant)
- [ ] AI directives block with at minimum: freshness, pricing/commercial guidance, local intent, brand/entity, corrections, file metadata
- [ ] SEO routing table (query → URL)
- [ ] SEO priority hierarchy
- [ ] Transactional guidance (if commercial site)
- [ ] Structured-data disclosure
- [ ] Intent router
- [ ] Entity facts block
- [ ] Main category hub links
- [ ] Top-N city or sub-category links (with URL pattern for long tail)
- [ ] Curated editorial articles (highest-citation-potential)
- [ ] Machine-readable sources pointers (sitemap.xml, planned llms-full.txt)
- [ ] Optional section for skippable secondary material

## What to exclude — checklist

- [ ] Vendor / product pages (use sitemap.xml — they belong there)
- [ ] Faceted / filtered URLs (`?color=red&size=M`)
- [ ] Login / signup / account pages
- [ ] Per-user pages (profiles, dashboards, sessions)
- [ ] Internal search result pages
- [ ] Paginated archive pages beyond page 1
- [ ] Ephemeral campaigns / time-limited promotions
- [ ] Marketing-speak descriptions ("revolutionize your...")
- [ ] DMCA / legal boilerplate (separate page, not in llms.txt)

## Description writing rules

Good descriptions follow specific patterns:

| Bad | Good |
|---|---|
| "Learn about our streaming API" | "Streaming API quickstart — SSE setup, retry, cancellation" |
| "Find your perfect event venue" | "Venue directory with 60,000+ listings searchable by city and venue type" |
| "Comprehensive privacy resources" | "Privacy policy and terms of service" |
| "Revolutionize your photography choices" | "Photographer directory with portfolio + per-tier pricing + contract templates" |
| "Everything you need to know about marriage" | "Civil-marriage application process step-by-step, with required documents and timelines (Türkiye)" |

Descriptions are the part LLMs actually parse to decide whether to fetch the link. They're not throwaway.

## Treasure-map honesty

A critical rule: **don't describe content that doesn't exist on the linked page.**

If your description says "step-by-step legal process with required documents" and the actual page is a thin marketing teaser, you've created a cloaking-style mismatch. If Google ever enforces parity (Mueller's January 2026 statement suggested they might), this gets you penalized.

Test: pick 5 random links from your llms.txt. Visit the page. Does the description match what's actually on the page? Adjust until yes.

## Cross-references

- For spec basics → `01-foundations.md`
- For SEO routing patterns in detail → `03-seo-perspective.md`
- For deployment / server config → `06-deployment.md`
- For anti-patterns to avoid → `07-failure-modes.md`
- For templates → `../templates/`
- For real implementation → `../case-study/example-marketplace-case.md`
