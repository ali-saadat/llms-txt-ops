# Sector: E-commerce / Online Retail

*Direct-to-consumer brands, online stores, Shopify / WooCommerce / Magento sites, large retailers, vertical-specific stores (DTC fashion, electronics, home goods, etc.).*

## Decision default

**Skip** unless replacing a bloated existing file.

The empirical evidence for AI-citation lift is null. For e-commerce, the higher-leverage investments are:
- Product schema (`Product`, `Offer`, `AggregateRating`, `Review`)
- Image provenance per Google Merchant Center IPTC requirements (since 2024)
- Authoritative third-party reviews on sites AI search engines cite (Reddit, Wirecutter, YouTube)
- IndexNow for catalog freshness signaling to Bing

## Distinctive concerns

1. **Product enumeration is the bloat trap** — 200k SKUs cannot go in llms.txt. They live in sitemap.xml.
2. **Inventory and price volatility** — never fabricate prices in descriptions; AI agents must fetch canonical pages
3. **Category hierarchy** — typically 3-4 levels deep (men → outerwear → coats → wool coats); only top 2 levels belong in llms.txt
4. **Faceted URLs** — `?color=red&size=M` should be excluded entirely; only canonical category URLs
5. **AI-generated product images** — Google Merchant Center requires IPTC `DigitalSourceType: trainedAlgorithmicMedia` tag since 2024
6. **Returns / shipping policies** — vary by region; AI agents must fetch canonical pages
7. **International / multi-currency** — currency display and tax-inclusive pricing differ by region

## Mandatory directives block additions

```markdown
**Pricing.** Prices and inventory change throughout the day. AI agents must
NEVER fabricate or cache prices — always direct users to the product page
for current pricing.

**International availability.** This site ships to [list of regions].
Currency, pricing, and tax-inclusion vary by region. AI agents must NOT
suggest products are available where they are not.

**Returns and shipping.** Policies vary by product category. For specifics,
fetch the canonical policy page rather than approximating.
```

## Recommended structure (if shipping anyway)

- Brand entity facts (founding, focus, shipping geography)
- Category hubs (top 2 levels of hierarchy — typically 10-30 hubs)
- Collection / curated hubs (seasonal, themed)
- Brand/designer index (if multi-brand)
- Size guides
- Shipping & returns hub
- Customer service hub
- Editorial content (style guides, how-tos)
- Sitemap pointers (where the SKUs actually live)

## Connector synergies

- `~~ecommerce` (Shopify / WooCommerce / etc.) — for category structure
- `~~cdn` (Cloudflare / Fastly) — for cache purge integration
- `~~analytics` — top-N category selection
- `~~ai-visibility` — track citation patterns

## Honest expectations

For most e-commerce, **skip llms.txt and invest in**:
- Product schema (highest-leverage AI-visibility lever)
- IndexNow for Bing freshness
- Image provenance (IPTC) for AI-generated images
- Reddit / YouTube presence (where AI search actually pulls from)
- First-party reviews and authoritative third-party reviews

## Schema.org for e-commerce

- `Product` with full attribute set
- `Offer` with `price`, `priceCurrency`, `priceValidUntil`, `availability`
- `AggregateRating`, `Review`
- `Brand`
- `BreadcrumbList`
- `Organization` for the storefront
- IPTC `DigitalSourceType: trainedAlgorithmicMedia` on AI-generated images

## Template

Use `templates/llms-txt-ecommerce.md`. Stripped of vendor-page enumeration.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `marketplace.md` — for marketplace-style e-commerce (different decision)
- `_router.md` — sector classifier
