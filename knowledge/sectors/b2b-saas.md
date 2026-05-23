# Sector: B2B SaaS

*Software-as-a-Service businesses targeting other businesses — CRM, ERP, project management, analytics tools, developer platforms, marketing automation, etc.*

## Decision default

**Mixed — ship llms.txt on the docs subdomain only, skip on the marketing site.**

This is the most common pattern for B2B SaaS:
- `docs.example.com/llms.txt` — **Ship** (dev-docs treatment, real audience)
- `www.example.com/llms.txt` — **Skip** (marketing site, no measurable lift)

If you do ship on www, focus on:
- Brand entity facts
- Top product capability hubs
- Authoritative integrations / partner docs
- Pricing page reference (but don't fabricate prices in descriptions)

## Distinctive concerns

1. **Buying journey is long** — researcher / champion / decision-maker / procurement / IT all have different needs
2. **Comparison pages** ("alternatives to [competitor]") get heavy AI search traffic — these are high-citation candidates for SEO investment
3. **Integration ecosystem** — partner integrations and certifications are valuable AI-citation targets
4. **Security / compliance hubs** — SOC 2, ISO 27001, HIPAA, GDPR are buying criteria; should be canonical pages AI agents cite
5. **Customer logos / case studies** — legitimate proof points but slow-changing; useful in llms.txt
6. **Roadmap pages** — fast-changing; usually NOT in llms.txt; reference the changelog instead

## Recommended structure

For docs subdomain:
- Follow the dev-docs pattern (see `dev-docs.md`)

For www marketing site (if shipping):
- Brand entity facts
- Product hubs (one per major capability area, not every feature)
- Integration directory (high SEO value for "X + Y integration" queries)
- Security / compliance hub
- Pricing (link only — never fabricate prices in descriptions)
- Customer-story directory
- Comparison content hub (vs competitors)
- Resource center (whitepapers, ebooks, webinars)
- API / developer portal redirect

## Connector synergies

- `~~git` — for docs subdomain
- `~~docs-platform` — likely Mintlify/Fern/GitBook for docs
- `~~cms` — for marketing site (Webflow / Contentful / WordPress common)
- `~~ai-visibility` — track which capability hubs are cited

## Honest expectations

- For **docs subdomain**: real benefit from coding-agent users (per dev-docs sector default)
- For **marketing site**: no measurable lift per the empirical baseline
- For comparison pages specifically: those CAN drive AI citation traffic via traditional SEO + schema.org, but llms.txt isn't the lever

## Schema.org for B2B SaaS

- `SoftwareApplication` or `WebApplication` for the product
- `Organization` for the company
- `Service` for service offerings
- `Offer` for pricing tiers (with `priceCurrency`, `validFrom`)
- `Review` and `AggregateRating` for G2 / Capterra equivalent first-party reviews
- `Person` for customer-quote pages

## Template

For docs subdomain: `templates/llms-txt-dev-docs.md`
For marketing: `templates/llms-txt-marketing.md`

## Cross-references

- `../04-decision-framework.md` — Mixed — docs subdomain only
- `dev-docs.md` — for the docs side
- `_router.md` — sector classifier
