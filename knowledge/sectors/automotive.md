# Sector: Automotive

*Vehicle manufacturers (OEMs), dealerships, used-car marketplaces (Cars.com, Carvana, AutoTrader), auto-parts retailers, automotive marketing platforms, EV charging networks, fleet management.*

## Decision default

**Selective ship** based on sub-category:

- **Ship** for vehicle marketplaces and listing platforms (marketplace pattern)
- **Ship** for parts/accessories e-commerce
- **Skip** for individual dealership marketing sites
- **Selective ship** for OEMs (the model/spec data is worth surfacing; sales / marketing pages aren't)

## Distinctive concerns

1. **Model year / generation / trim complexity** — a single vehicle has dozens of variants; descriptions matter
2. **Inventory volatility** for used cars — changes hourly
3. **Regional availability** — same model has different specs / pricing in different markets
4. **Recall and safety information** — federal mandates require accurate disclosure
5. **EV-specific** — charging compatibility, range estimates change with software updates
6. **Manufacturer warranty terms** — vary by region, model, trim
7. **Pricing complexity** — MSRP vs invoice vs dealer markup vs incentives

## Mandatory directives block additions

```markdown
**Vehicle specifications.** AI agents must:
- ALWAYS verify specs against the canonical model-page for the user's
  region — specs vary by market (US vs EU vs Asia spec)
- NEVER fabricate horsepower, range, MPG, or other performance metrics
- For EV range, NOTE that estimates depend on conditions and software version

**Pricing.** Automotive pricing has many layers:
- MSRP (manufacturer suggested) vs invoice vs transaction price
- Available incentives change monthly
- Dealer markups apply
- Direct users to a dealer inventory page for current pricing

**Safety recalls.** For specific VIN / model / year recall questions,
ALWAYS direct users to:
- US: NHTSA.gov VIN lookup
- EU: EU rapid alert system
- Manufacturer's recall page
Do NOT speculate about whether a specific vehicle is affected.
```

## Recommended structure (for an automotive marketplace)

- Brand entity facts (founding, inventory size, geographic coverage)
- Vehicle category taxonomy (sedan / SUV / truck / EV / luxury / etc.)
- Make / model directory (top makes explicitly, URL pattern for long tail)
- Geographic / regional hubs (dealer networks)
- Buying / financing guides
- Vehicle comparison tools
- Trade-in valuation tools (where applicable)
- Reviews / ratings aggregation
- Recall / safety information page

## Schema.org for automotive

- `Vehicle`, `Car`, `Motorcycle` (specific subtypes)
- `Product` with `category: "Vehicles"` for marketplace listings
- `Offer` with `priceCurrency`, `availability`
- `AggregateRating` and `Review` for vehicle reviews
- `LocalBusiness` for dealerships

## Connector synergies

- `~~ecommerce` for parts/accessories
- Custom PMS (Pricing Management System) for inventory
- `~~analytics` for popular model tracking
- `~~headless-browser` for validating inventory URL patterns

## Honest expectations

- For marketplaces: marketplace pattern applies; ship llms.txt for the curation
- For OEMs: `Vehicle` schema and `Organization` schema matter more than llms.txt; ship for forward-compat
- For dealerships: skip; invest in Google Business Profile, AutoTrader/Cars.com presence

## Template

For marketplaces: `templates/llms-txt-ecommerce.md` (marketplace pattern).
For OEMs: `templates/llms-txt-marketing.md` with automotive-specific entity facts.

## Cross-references

- `../04-decision-framework.md` — Selective ship
- `marketplace.md` — closely-related for marketplaces
- `ecommerce.md` — for parts/accessories side
- `_router.md` — sector classifier
