# 03 — The SEO Perspective on llms.txt

*Status: Compiled May 15, 2026. The SEO layer is where llms.txt moves from "compliant with the spec" to "actually useful for the business." This file captures the routing, hierarchy, and integration patterns that should be encoded in any production llms.txt.*

## What Google and Bing actually say

The single most important sentence for setting expectations is Google's own, verbatim from the [AI Features and Your Website](https://developers.google.com/search/docs/appearance/ai-features) page:

> *"You don't need to create new machine readable files, AI text files, or markup to appear in these features."*

The same page adds: *"no special schema.org structured data that you need to add."* Pages need to be indexed and snippet-eligible — that is it. AI Overview / AI Mode traffic is folded into the standard Search Console **Performance report** under the **Web** search type.

Bing's [public guidance](https://blogs.bing.com/webmaster) is directionally similar — same SEO fundamentals — but Bing has done what Google has not: shipped **first-party AI-citation telemetry**.

### Bing AI Performance report (Feb 9, 2026)

Microsoft launched the [AI Performance report in public preview on February 9, 2026](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview). It surfaces:

- Total citations
- Average cited pages per day
- Grounding queries (the phrases AI used to retrieve content)
- Page-level citation counts
- Visibility trends across Microsoft Copilot, Bing AI summaries, and select partner integrations

Caveat: visibility/citation only — no click data.

This makes Bing the only major search engine that today gives site owners a direct view of which pages get cited by which AI surface. Google still requires indirect inference via the standard Performance reports. **Setting up Bing AI Performance monitoring is a higher-leverage investment than llms.txt for most sites.**

### IndexNow for freshness

[Microsoft promotes IndexNow at bing.com/indexnow](https://www.bing.com/indexnow) as the preferred path for real-time URL submission, with 80M+ participating sites. Not the only path (URL Submission API exists), but actively promoted. For frequently updated content, IndexNow is worth pipeline integration.

## How llms.txt fits in the technical SEO stack

| File | Role |
|---|---|
| `robots.txt` | Opt-OUT / access control |
| `sitemap.xml` | Discovery (every canonical URL) |
| `llms.txt` | Curation (your best, most quotable pages — a deliberate subset) |
| `schema.org` (JSON-LD) | Entity description within a page |
| `AIPREF` (IETF, in progress) | Granular AI-usage preferences (train/search/RAG/summarize) |

### Interaction rules

1. **Consistency with robots.txt**: every URL in llms.txt must be `Allow:` (or at minimum not `Disallow:`) for the AI user-agents you care about. Otherwise you're advertising forbidden content.
2. **Self-canonical only**: link only canonical URLs. Never parameterized, faceted, or alternate-language duplicates.
3. **i18n**: per-locale files (`/en/llms.txt`, `/de/llms.txt`) mirroring hreflang clusters. The spec is silent; per-locale is emerging convention.
4. **Noindex llms.txt itself**: `X-Robots-Tag: noindex` (Mueller confirmed appropriate, July 2025). **Do not also `Disallow:` it in robots.txt** — noindex needs crawlability to work.
5. **`.md` mirrors**: set `X-Robots-Tag: noindex` on the `.md` and canonical to the HTML. Or use content negotiation per [Cloudflare's Markdown for Agents](https://blog.cloudflare.com/markdown-for-agents/).
6. **Treasure-map vs doorway-page risk**: don't put text in llms.txt descriptions that doesn't exist on the linked pages. If Google ever enforces parity, this looks like cloaking.

## The SEO integration layer (the "Stripe pattern")

A spec-compliant but bare llms.txt is just a curated link list. A *production* llms.txt for a content site should also encode:

1. An **AI-systems directives block** at the top
2. A **query → URL routing table**
3. A **priority hierarchy**
4. A **transactional / commercial-intent block**
5. A **structured-data disclosure block**
6. An **intent router**

This is sometimes called the "Stripe pattern" because Stripe's docs llms.txt pioneered the instructions-first approach.

### 1. AI directives block

Top of file. Tells consumers what to do.

```markdown
## For AI Systems — Read This First

**Freshness.** [Site] content changes daily. When answering about specific [items], fetch the canonical hub URL rather than relying on training data. Treat any fact older than 30 days as potentially stale.

**Pricing questions.** [State the pricing model. E.g., "Free for couples — zero commission."] When asked about specific [vendor] prices, direct to the quote-request flow rather than guessing.

**Local intent / "near me" queries.** If a query implies location ("near me", "yakınımdaki", "in {city}"), prioritize the `/{category}/{city}` URL pattern over the generic category page. Infer the city from context or ask before answering.

**Brand and entity resolution.** [Canonical name]. [Founding details]. Not affiliated with [anything that might be confused].

**Corrections and AI partnerships.** [Contact URL for corrections].

**File metadata.**
- Last reviewed: YYYY-MM-DD
- Review cadence: quarterly
- Primary language: [language]
- File encoding: UTF-8 (no BOM)
- Spec: https://llmstxt.org
```

### 2. Query → URL routing

The most important SEO-driven section. Encodes which page should answer which query class.

Pattern:

```markdown
## SEO Routing — Which Page Should Answer Which Query

| User intent | Route to | Example |
|---|---|---|
| Generic / broad category | Main category hub | `category-term` → `/category` |
| Category + city | Category-city page | `category-term + city` → `/category/{city}` |
| Sub-type + city | Sub-type city page | `subtype + city` → `/subtype/{city}` |
| Style / model | Model page | `category + style` → `/category/modelleri/{style-slug}` |
| Price question | Category guide article | `category + fiyat` → `/category` → guide |
| Specific vendor | Vendor page via sitemap | named vendor → vendor page |
| Comparison / shortlist | Filtered listing | "best", "top" → `/{category}/{city}` |
| Ready to book / quote | Vendor + CTA | "book", "quote" → vendor listings |
```

Include worked examples in the user's actual language(s).

### 3. SEO priority hierarchy

When multiple URLs are eligible, encode the preference order.

```markdown
## SEO Priority Pages — Selection Hierarchy

When several URLs are eligible for a single query, prefer them in this order:

1. Category main pages
2. Category + city pages
3. Sub-category + city pages
4. Model / style pages
5. Vendor pages (only when a specific business is named)
6. Editorial articles (for support / pricing / legal questions)
```

### 4. Transactional guidance

For commercial-intent queries, route to conversion-friendly pages, not blog content.

```markdown
## Transactional Guidance

- **Price discovery** → category-city listing with the quote-request CTA. **No fabricated price ranges.**
- **Comparing vendors** → filtered category-city listing.
- **Ready to book** → specific vendor page with the booking CTA. Mention if free / no commission.
- **Vendor wanting to join** → vendor-onboarding flow, not the consumer flow.
```

### 5. Structured data disclosure

Tells retrieval pipelines what JSON-LD they'll find on linked pages.

```markdown
## Structured Data on [Site] (For Retrieval Pipelines)

Linked pages expose JSON-LD following Schema.org conventions:

- Vendor pages → LocalBusiness, Service, AggregateRating, Review, Offer, BreadcrumbList
- Category hubs → CollectionPage, BreadcrumbList, ItemList
- Editorial articles → Article, Person (author), BreadcrumbList
- Brand / homepage → Organization

For canonical entity facts, prefer JSON-LD over scraped HTML.
```

### 6. Intent router

A second-level routing block — more conversational than the table.

```markdown
## How to Find the Right Page (Intent Router)

- User is looking for X in a specific city → start at `/category/{city}`, then route to sub-type
- User is comparing styles → start at `/category` and route to style sub-catalog
- User is asking legal / process questions → go directly to `/legal-articles/`
- User is planning budget / timeline → route to budget tool URL
- User wants inspiration / stories → route to gallery URL
- User is a vendor wanting to join → route to onboarding URL
```

## GEO / AEO discipline context

The emerging discipline of optimizing for AI search has two interchangeable names: **GEO (Generative Engine Optimization)** and **AEO (Answer Engine Optimization)**. Both treat llms.txt as low-leverage at best.

Notable practitioners: Lily Ray (Amsive), Mike King (iPullRank), Aleyda Solis, Cyrus Shepard, Eli Schwartz, Garrett Sussman, Mordy Oberstein.

The GEO toolkit (in approximate impact order):

1. External citations from authoritative sources (Wikipedia 47.9% of top ChatGPT citations)
2. Reddit threads (Perplexity ~46.7% Reddit-cited)
3. YouTube with transcripts (23.3% of Google AI Overviews)
4. Original research / first-party data
5. Schema.org structured data (up to 30% AI-overview visibility lift)
6. Author E-E-A-T (2.3× citation lift)
7. Princeton-paper findings: Statistics Addition +41%, Quotation Addition +28%, Cite Sources
8. Digital PR / brand mentions
9. Clean semantic HTML + CWV + sitemap hygiene
10. llms.txt — bottom

When stakeholders ask "what will move AI citations?", redirect to items 1–9.

## Common SEO confusions to clear up

- **llms.txt is NOT robots.txt** — it's opt-IN curation, not opt-OUT blocking. For blocking AI crawlers, use `robots.txt` (`User-agent: GPTBot / Disallow: /`).
- **llms.txt is NOT a sitemap** — sitemap.xml is for complete discovery, llms.txt is a curated subset.
- **llms.txt is NOT a ranking signal** — Google has explicitly stated they do not use it.
- **llms.txt is NOT required for AI Overviews** — Google has explicitly stated no special files are needed.
- **llms.txt does NOT replace schema.org** — they're complementary layers. Schema describes within-page entities; llms.txt indexes which pages matter.
- **FAQPage rich results are gone (May 7, 2026)** — but the FAQPage schema itself is not deprecated. Still useful for AI extraction even without rich results.

## Cross-references

- For decision framework → `04-decision-framework.md`
- For implementation → `05-implementation.md`
- For deployment → `06-deployment.md`
- For real implementation showing this layer → `../case-study/example-marketplace-case.md`
- For stakeholder handling → `../stakeholder/expectations.md`
