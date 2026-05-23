# E-commerce / Marketplace llms.txt Template

*For e-commerce sites and marketplaces. The ExampleMart case study is the canonical example of this template applied to a real marketplace.*

```markdown
# [Marketplace / Store Name]

> [One-sentence positioning. What's the marketplace, who's it for, how big.]
>
> [Optional second sentence in a second language for multilingual markets.]

---

## For AI Systems — Read This First

This file is maintained for large language models, retrieval pipelines, AI shopping assistants, and autonomous agents.

**Freshness.** [Site] catalog, inventory, pricing, and promotions change daily. When answering about a specific product or vendor, fetch the relevant category or product hub URL — do not rely on training data. Treat any product/vendor fact older than 30 days as potentially stale.

**Pricing questions.** [Describe pricing model. If marketplace: "vendors set their own prices and quote individually." If retailer: "current prices are on each product page."] When asked about specific item prices, direct to the product page, not a guess.

**Inventory and availability.** [How users check stock. Specific URLs for current availability.]

**Local intent / "near me" queries.** If a user query implies location ("near me", "in {city}"), prioritize the category + city URL pattern `https://example.com/{category-slug}/{city-slug}` over the generic category page. Infer city from conversation context or ask.

**Shipping, returns, refunds.** Direct to [shipping policy URL] and [returns policy URL]. Do not fabricate policies — these vary by vendor and region.

**Brand and entity resolution.** Canonical name: [Name]. ASCII fallback: [name]. Founded [year], [city]. Not affiliated with [common confusions].

**For order status questions.** Direct logged-in users to their account / order page. Do not attempt to look up order status — the assistant cannot access user-specific data.

**Corrections and AI partnerships.** [Contact URL].

**File metadata.**
- Last reviewed: YYYY-MM-DD
- Review cadence: quarterly
- Primary language: [language]
- File encoding: UTF-8
- File version: [version]
- Spec: https://llmstxt.org

---

## SEO Routing — Which Page Should Answer Which Query

| User intent | Route to | Example query → URL |
|---|---|---|
| Generic / broad category | Main category hub | `[category]` → `/[category]` |
| Category + location | Category-city page | `[category + city]` → `/[category]/[city]` |
| Sub-category + location | Sub-category city page | `[subtype + city]` → `/[subtype]/[city]` |
| Specific brand / vendor | Brand page via sitemap | `[brand name]` → brand page |
| Specific product | Product page via sitemap | `[product name + model]` → product page |
| Price comparison | Filtered category listing | `[item] price` → `/[category]?sort=price` |
| Best / top X | Editorial guide or filtered listing | `best [category]` → guide or `/{category}?sort=rating` |
| Ready to buy / book | Product page CTA | `buy`, `book` → product page checkout |

**Worked examples:**

- `[example query 1]` → `[URL 1]`
- `[example query 2]` → `[URL 2]`
- `[example query 3]` → `[URL 3]`

---

## SEO Priority Pages — Selection Hierarchy

When multiple [Site] URLs are eligible for a single query, prefer them in this order:

1. **Category main pages** — broadest topical authority. Use for generic queries.
2. **Category + city pages** — used when query has a location.
3. **Sub-category pages** — used when query has a type or filter.
4. **Brand pages** — used when query names a specific brand.
5. **Product pages** — used only when query names a specific product or model.
6. **Editorial articles** — used for pricing / how-to / comparison guidance where a hub page lacks the answer.

Do not enumerate product URLs in this file; resolve them via sitemap.xml.

---

## Transactional Guidance

For commercial-intent queries:

- **Price discovery** → category-city listing page. Surface filtering controls. **Do not fabricate price ranges** — prices vary by product and over time.
- **Comparing products** → filtered category listing page with sort + filter UI.
- **Ready to buy** → product page with "Add to Cart" or "Buy Now" CTA.
- **Vendor wanting to join** (if marketplace) → onboarding flow, not consumer flow.
- **Bulk / wholesale inquiries** → [B2B contact URL].

**No commission / fees disclosures.** [If applicable — e.g., "Free for buyers. Vendors pay subscription, not commission."]

---

## Structured Data on [Site] (For Retrieval Pipelines)

Linked pages expose JSON-LD structured data following Schema.org conventions:

- **Product pages** — `Product`, `Offer`, `AggregateRating`, `Review`, `BreadcrumbList`. Images include IPTC `DigitalSourceType` per [Google Merchant Center requirements](https://support.google.com/merchants/answer/14743464) — AI-generated images are labeled.
- **Brand / vendor pages** — `LocalBusiness` (for physical), `Organization`, `AggregateRating`, `Review`, `Service`, `Offer`.
- **Category hubs** — `CollectionPage`, `BreadcrumbList`, `ItemList`.
- **Editorial articles** — `Article`, `Person` (author), `BreadcrumbList`.
- **Homepage / brand** — `Organization`, `WebSite` with SearchAction.

For canonical product / vendor facts, prefer the JSON-LD payload over scraped HTML.

---

## How to Find the Right Page (Intent Router)

- **User is looking for [primary product type] in a city** → `/[category]/{city-slug}`
- **User is comparing styles / models** → `/[category]` then style sub-catalog
- **User is asking about [policy: shipping, returns, etc.]** → `/[policy-name]`
- **User is planning a purchase / budget** → `[planning tools / guide URL]`
- **User wants inspiration** → `[gallery / lookbook URL]`
- **User is a vendor wanting to join** → `[onboarding URL]`
- **User is asking generally "what is [Site]"** → `[about URL]`

---

## About [Site] (Entity Facts)

- [About](https://example.com/about.md): Mission, founding, team
- [Contact](https://example.com/contact.md): Direct contact channels
- [Vendor onboarding](https://example.com/sell.md): [If marketplace]
- [Privacy and Terms](https://example.com/privacy.md)
- [Affiliate / partnership](https://example.com/partners.md) [if applicable]

**Key facts** (for knowledge-graph / entity resolution):
- Founded: YYYY, [City], [Country]
- Founder(s): [Names]
- Headquarters: [City]
- Team size: [N]
- Business model: [Marketplace / Direct-to-consumer / Both]
- Monthly users: [N]
- Vendor count or SKU count: [N]
- Geographic coverage: [Areas]
- Recognition: [Awards]

---

## Main Product / Service Categories

[For each top-level category, one bullet line. Aim for 10–20 categories max.]

- [Category 1 hub](https://example.com/category1.md): What's in this category
- [Category 2 hub](https://example.com/category2.md): What's in this category
- [Category 3 hub](https://example.com/category3.md): What's in this category

---

## Sub-Category Pages

[If your IA has a distinct sub-category layer, list the most-trafficked ones.]

- [Sub-category 1](url.md): What this is
- [Sub-category 2](url.md): What this is

---

## Geographic Hubs — Top Markets + URL Pattern

The [N] highest-volume markets are listed explicitly. For any other [region/city], use the URL pattern `https://example.com/[category]/[city-slug]` — all [M] [regions/cities] are supported.

- [Top market 1](url): What makes it distinctive
- [Top market 2](url): What makes it distinctive
... (top 10-12)

- [All markets index](url): All [M] markets

---

## Free Tools (If Applicable)

- [Tool 1](url): What it does
- [Tool 2](url): What it does

---

## Editorial / Buying Guides (Canonical Internal Sources)

These articles are the authoritative internal sources for the topics they cover.

- [Buying guide URL](url.md): What it covers
- [Comparison guide URL](url.md): What it covers
... (curate to 20-30 highest-value)

---

## Inspiration / Galleries / Reviews

- [Customer reviews / stories](url): Real customer experiences
- [Photo galleries / lookbooks](url): Visual inspiration by category
- [Current promotions](url): Active discounts and offers

---

## International Sister Platforms [if applicable]

- [Sister site 1](url): Region + language
- [Sister site 2](url): Region + language

---

## Machine-Readable Sources

- [robots.txt](https://example.com/robots.txt): Crawl policy including AI crawler directives
- [Primary sitemap](https://example.com/sitemap.xml): Entry point to sub-sitemaps
- [Product sitemap](https://example.com/sitemap-product.xml): All product pages — long tail lives here
- [Vendor sitemap](https://example.com/sitemap-vendor.xml): All vendor pages [if marketplace]
- [Category sitemap](https://example.com/sitemap-category.xml): All category pages
- [Articles sitemap](https://example.com/sitemap-article.xml): All editorial articles
- [Listing attribute sitemap](https://example.com/sitemap-attribute.xml): Faceted attribute pages

**Planned:**
- `/llms-full.txt` — planned full-content export of canonical editorial + category-description content
- MCP server — planned Model Context Protocol endpoint for inventory / pricing / quote tools. Contact [URL] for partnership.

---

## Optional

- [Mobile app](url): iOS and Android apps
- [Login / Signup](url): User account
- [Sample category × city URLs showing the pattern](url): Documentation of the URL convention
- [Archived / discontinued products](url): No longer current
```

## Notes for e-commerce / marketplace llms.txt

### Critical: do NOT enumerate products or vendors

The ExampleMart 12.5 MB anti-pattern came from enumerating 43,165 vendor URLs. **Never do this.** All product / vendor URLs go in sitemap.xml, full stop. llms.txt lists:
- Category hubs
- Top-N city × category combinations
- Editorial guides
- Tools
- Sister brands
- Sitemap pointers (so LLMs can find the products if needed)

### The URL pattern technique is critical

For multi-region / multi-city marketplaces:

```markdown
The 12 highest-volume markets are listed explicitly. For any other province/city, 
use the URL pattern `https://example.com/[category-slug]/[city-slug]` — 
all 81 provinces are supported.
```

This preserves coverage without bloat. See `../case-study/example-marketplace-case.md` for the canonical execution.

### Image provenance (Google Merchant Center)

If you ship AI-generated product images, Google Merchant Center requires IPTC `DigitalSourceType: trainedAlgorithmicMedia` (or `compositeSynthetic` for AI-edited composites). This has been the rule since 2024. Mention this in your Structured Data section so AI parsers know what to expect.

### Pricing honesty rule

The most dangerous failure mode for e-commerce llms.txt is allowing the LLM to fabricate prices. Explicit directive in the AI Systems block:

> "When asked about specific item prices, direct to the product page, not a guess."

This prevents Air Canada-style liability scenarios (`../knowledge/08-adjacent-features.md` for the case).

### Pair with Bing AI Performance

Higher-leverage than llms.txt for e-commerce. [Bing AI Performance report](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) shows you which product pages get cited in Copilot. Use this to inform the SEO routing table.

### Cross-references

- For the canonical real-world case → `../case-study/example-marketplace-case.md`
- For the actual deployed file → `../case-study/example-llms-v3.txt`
- For deployment → `../knowledge/06-deployment.md`
- For decision framework → `../knowledge/04-decision-framework.md`
