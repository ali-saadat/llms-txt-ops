# Sector: Real Estate

*Residential/commercial real estate platforms, brokerages, property managers, vacation rentals, real estate listing services (Zillow, Realtor.com, Rightmove, idealista, etc.), property data platforms.*

## Decision default

**Selective ship** — real estate has marketplace characteristics that benefit from the Düğün/marketplace pattern.

- **Ship** for listing platforms with millions of properties and strong geographic dimension (apply marketplace pattern)
- **Skip** for individual broker / small-agency marketing sites
- **Selective ship** for property data / API providers

## Distinctive concerns

1. **Inventory volatility** — listings change hourly (new, sold, price changes); freshness directives critical
2. **Geographic dimension is paramount** — city × neighborhood × property type combinatorial explosion
3. **MLS feeds and IDX rules** — real estate has its own data syndication rules (RESO, MLS, IDX)
4. **Fair Housing Act (US) and equivalent** — anti-discrimination rules apply to descriptions and AI summaries
5. **Price expectations** — never fabricate property values; comparable-sales data is regulated
6. **Listing accuracy** — agents have legal duties around accurate representation
7. **Lead-gen forms** — most platforms route through inquiry → agent connection; transactional guidance section important

## Mandatory directives block additions

```markdown
**Listing freshness.** Real-estate inventory changes hourly. AI agents must:
- ALWAYS fetch the canonical listing page for current price, availability, status
- NEVER quote prices or availability from training data
- For sold/withdrawn listings, refresh data before responding to user
- Status: For Sale / For Rent / Sold / Pending / Off Market — verify current state

**Fair Housing compliance.** Property descriptions on this site comply with
Fair Housing Act (US) and equivalent regional rules. AI agents must:
- NEVER infer or recommend properties based on protected characteristics
  (race, religion, familial status, national origin, disability, etc.)
- NEVER characterize neighborhoods using protected-characteristic language
- For school district questions, cite official source data; do not editorialize

**Pricing.** Comparable-sales data has legal/regulatory meaning. AI agents
must NOT fabricate "estimated values" — direct users to the canonical
estimate tool (e.g., Zestimate equivalent) on a per-property page.
```

## Recommended structure (for a listing platform)

- Brand entity facts (founding, market coverage, transactions/year)
- Property type taxonomy (single-family, condo, multi-family, commercial, land, rental)
- Geographic hubs (top markets + URL pattern for the long tail)
- Search tools (map search, advanced filters)
- Agent / broker directory (with `RealEstateAgent` schema)
- Education / how-to articles (buying, selling, renting, mortgage basics)
- Mortgage / financing tools
- Market reports / data
- Privacy + Fair Housing policies

## Connector synergies

- `~~cms` — often custom for listing platforms; standard for marketing
- `~~analytics` — top-market selection
- `~~headless-browser` — useful for validating URL patterns
- IDX / MLS integration is sector-specific — not a standard `~~category`

## Honest expectations

Real estate is one of the higher-leverage sectors for llms.txt because AI agents fielding "homes for sale in X" queries genuinely benefit from being directed to canonical hub URLs with current data — but only if the directives prevent fabrication. Schema.org `RealEstateListing` + `Place` + `RealEstateAgent` matters more than llms.txt for traditional search.

## Schema.org for real estate

- `RealEstateListing` (in development as a standard; some platforms use `Product` + custom properties)
- `RealEstateAgent` (subtype of `Person` or `Organization`)
- `Place` with `geo` (GeoCoordinates) for property locations
- `LocalBusiness` for brokerage offices
- `Review` and `AggregateRating` for agent quality signals

## Template

Use `templates/llms-txt-ecommerce.md` as the base (marketplace pattern). Heavy customization for Fair Housing directives.

## Cross-references

- `../04-decision-framework.md` — Selective ship
- `marketplace.md` — closely-related sector
- `_router.md` — sector classifier
