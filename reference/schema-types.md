# Schema.org Types per Page Type

*Reference for the "Structured Data on [Site]" disclosure section in llms.txt. Map page templates to the JSON-LD types they should ship and the LLM-relevant fields to populate.*

## Why this matters

llms.txt should include a section disclosing which Schema.org types are present on linked pages. Tells retrieval pipelines what to expect and instructs them to prefer JSON-LD over scraped HTML.

Schema.org is what AI Overviews, Copilot, Gemini, and most AI search surfaces actually consume (Google Merchant Center IPTC requirement since 2024 is a recent example of provenance standardization).

## Page type → recommended schema map

### Homepage / brand page

- **Organization** (or `LocalBusiness` if physical)
  - `name`, `legalName`, `url`, `logo`
  - `foundingDate`, `founder` (use `Person`)
  - `address` (use `PostalAddress`)
  - `sameAs` array linking social profiles for entity reconciliation
  - `numberOfEmployees`
  - `description`
- **WebSite** with **SearchAction**
  - Enables Sitelinks Search Box, useful for AI agents discovering search endpoints

### Editorial article / blog post

- **Article** (or `NewsArticle`, `BlogPosting`)
  - `headline`, `description`, `image` (multiple aspect ratios)
  - `datePublished`, `dateModified`
  - `author` (use `Person` with full sub-graph including `jobTitle`, `affiliation`)
  - `publisher` (use `Organization`)
  - `mainEntityOfPage`
- **BreadcrumbList**
- Optional: `speakable` for voice / audio AI surfaces

### Author / profile page

- **ProfilePage** (Google supports as of 2024)
  - `mainEntity` references a `Person`
  - **Person** sub-graph: `name`, `image`, `jobTitle`, `worksFor`, `sameAs` (LinkedIn, ORCID, Twitter), `description`, `knowsAbout`
  - `dateCreated` of the profile
- E-E-A-T-critical: this is the page that anchors authorship signals for AI citation lift (2.3× per Wellows study)

### Product page (e-commerce)

- **Product**
  - `name`, `description`, `image`, `brand` (use `Brand`)
  - `sku`, `gtin`, `mpn`
  - `offers` (use `Offer` with `price`, `priceCurrency`, `priceValidUntil`, `availability`, `itemCondition`)
  - `aggregateRating` (use `AggregateRating`)
  - `review` array (use `Review` with `author`, `reviewRating`, `datePublished`)
- **BreadcrumbList**
- For AI-generated product images: IPTC `DigitalSourceType: trainedAlgorithmicMedia` per Google Merchant Center policy (in force since 2024)

### Vendor / business page (marketplace)

- **LocalBusiness** (subtype based on category: `Restaurant`, `Photographer`, `EventVenue`, etc.)
  - `name`, `address`, `geo` (use `GeoCoordinates`), `telephone`, `openingHours`
  - `priceRange` (e.g., "$$")
  - `aggregateRating`, `review`
  - `image` array
  - `sameAs` for social verification
- **Service** for vendor service offerings
- **BreadcrumbList**

### Category / collection hub

- **CollectionPage**
  - `name`, `description`
  - `mainEntity` referencing the items in the collection
- **BreadcrumbList**
- **ItemList** with each item as a `ListItem`
  - For category-city hubs, each item is the vendor / product in that city

### FAQ page

- **FAQPage**
  - `mainEntity` array of `Question` (each with `acceptedAnswer` as `Answer`)
- Note: FAQ rich results in Google search were deprecated May 7, 2026 — but the `FAQPage` schema itself is still useful for AI extraction
- For pages with one main Q&A, prefer `QAPage` (community Q&A surface)

### Community / forum thread

- **DiscussionForumPosting** for forums
- **QAPage** for true single-question Q&A pages
- For DiscussionForumPosting, Google specifically recommends Microdata or RDFa over JSON-LD to avoid duplicating large text blocks

### Tool / web app

- **WebApplication** (or `SoftwareApplication`)
  - `name`, `description`, `applicationCategory`
  - `offers` if paid
  - `screenshot`
  - `featureList`

### Recipe (food sites)

- **Recipe**
  - `name`, `description`, `image`, `author`, `datePublished`
  - `prepTime`, `cookTime`, `totalTime`, `recipeYield`
  - `recipeIngredient` array
  - `recipeInstructions` (use `HowToStep`)
  - `nutrition` (use `NutritionInformation`)
  - `aggregateRating`

### Event

- **Event** (or `BusinessEvent`, `MusicEvent`, etc.)
  - `name`, `description`, `image`
  - `startDate`, `endDate`
  - `location` (use `Place` with `address`)
  - `organizer`, `performer`
  - `offers` for ticketing
  - `eventStatus` (especially post-COVID: scheduled / cancelled / rescheduled / online)
  - `eventAttendanceMode` (online / offline / mixed)

### How-to guide

- **HowTo**
  - `name`, `description`
  - `step` array of `HowToStep`
  - `tool`, `supply`
  - `totalTime`, `estimatedCost`

## The "prefer JSON-LD over scraped HTML" instruction

In the llms.txt structured-data disclosure section, include this directive verbatim:

> "For canonical entity facts, prefer the JSON-LD payload over scraped HTML when both are available."

This tells retrieval pipelines that JSON-LD is the authoritative source — clearer, structured, and less ambiguous than parsing rendered HTML.

## Validation

- [Google Rich Results Test](https://search.google.com/test/rich-results) — checks if Google understands the structured data
- [Schema.org Validator](https://validator.schema.org/) — checks against the schema.org definitions
- [Bing Markup Validator](https://www.bing.com/webmasters/tools/markup-validator) — checks Bing-specific signals

For sites at scale, automate validation in CI:

```bash
# Sample: curl page + extract JSON-LD + validate against schema
curl -s https://example.com/page | \
    grep -A 100 'application/ld+json' | \
    # ... process and validate
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Schema includes data not visible on the page | Schema must reflect visible page content (Google policy) |
| Using `FAQPage` when the page is a Q&A page | Use `QAPage` for true single-question community Q&A |
| Using JSON-LD for `DiscussionForumPosting` | Microdata or RDFa is preferred to avoid text duplication |
| Author schema with no `sameAs` | E-E-A-T weak — add LinkedIn, ORCID, social profiles |
| `Organization` without `sameAs` | Entity reconciliation fails — add Wikipedia, Wikidata, LinkedIn, etc. |
| AI-generated product image without IPTC tag | Google Merchant Center policy violation |
| Multiple schema types competing on same page | Pick the most specific type; nest others as sub-graphs |

## Cross-references

- For where this gets disclosed in llms.txt → `../knowledge/03-seo-perspective.md` and `../knowledge/05-implementation.md`
- For higher-leverage SEO investments (schema is in the top 5) → `../knowledge/02-empirical-evidence.md`
