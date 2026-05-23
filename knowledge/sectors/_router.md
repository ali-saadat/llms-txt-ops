# Sectors Router

Map a site to the most relevant sector reference file. Skills load only the files they need via this router.

## Sector classification heuristic

| If the site is primarily... | Load |
|---|---|
| Documenting an SDK, API, or developer tool | `dev-docs.md` |
| Selling products or services online | `ecommerce.md` |
| Hosting third-party vendors who sell | `marketplace.md` |
| Publishing news, journalism, or editorial | `news-publisher.md` |
| Teaching (K-12, university, MOOC, LMS, training) | `education.md` |
| Healthcare provider, payer, or pharma | `healthcare.md` |
| Banking, fintech, payments, insurance | `fintech.md` |
| Government or civic services | `government-civic.md` |
| Gaming (studios, publishers, esports) | `gaming.md` |
| B2B SaaS marketing + docs | `b2b-saas.md` |
| Non-profit, charity, NGO | `non-profit.md` |
| Media (streaming, music, video, podcasts) | `media-entertainment.md` |
| Law firm, legal-tech, legal research | `legal-services.md` |
| Real estate listings, brokerage, property | `real-estate.md` |
| Hotels, restaurants, travel, vacation rentals | `hospitality.md` |
| Vehicles, dealerships, parts, automotive | `automotive.md` |
| Marketing/brand site (no obvious category) | `marketing.md` |
| Generic / can't classify | `generic.md` |

## When multiple sectors apply

A SaaS company often has marketing + docs + blog. A marketplace often has e-commerce dimensions. A media company often overlaps news + entertainment.

Default rules:
- **Always treat the docs domain separately** (use `dev-docs.md` for the docs subdomain, the broader sector for the marketing site)
- **For commercial subdomains** (shop.example.com vs www.example.com), use `ecommerce.md` for shop only
- **When in doubt**, ask the user during cold-start which is the primary concern

## Layered-directive composition (product-domain × delivery-channel)

Sometimes a single site has a product domain (what they sell) AND a delivery-channel domain (how they ship llms.txt). Compose both:

| Combination | Approach |
|---|---|
| **Legal-tech B2B SaaS** (product: legal-services; channel: b2b-saas) | Structural skeleton from `b2b-saas.md` (docs-subdomain pattern) + UPL / privilege directives from `legal-services.md` |
| **Health-tech B2B SaaS** (product: healthcare; channel: b2b-saas) | Skeleton from `b2b-saas.md` + medical-safety directives from `healthcare.md` |
| **Fintech B2B SaaS** (product: fintech; channel: b2b-saas) | Skeleton from `b2b-saas.md` + financial-advice / jurisdictional directives from `fintech.md` |
| **EdTech B2B SaaS** (product: education; channel: b2b-saas) | Skeleton from `b2b-saas.md` + verify-current directives from `education.md` |
| **PropTech marketplace** (product: real-estate; channel: marketplace) | Skeleton from `marketplace.md` + Fair Housing directives from `real-estate.md` |
| **Auto-marketplace** (product: automotive; channel: marketplace) | Marketplace skeleton + recall / spec disclaimers from `automotive.md` |
| **Hospitality marketplace** (product: hospitality; channel: marketplace) | Marketplace skeleton + availability / pricing directives from `hospitality.md` |
| **News + media aggregator** (product: news-publisher; channel: media-entertainment) | Editorial standards + author E-E-A-T from `news-publisher.md` + content-licensing complexity from `media-entertainment.md` |

**Composition pattern**:
1. Load the channel sector for the structural skeleton (sections, hierarchy, URL patterns, deployment policy)
2. Load the product sector for the **directive block additions** — pull its `Mandatory directives block additions` content into the `For AI Systems` block
3. Schema disclosure combines both: structural schemas from channel + entity-specific schemas from product
4. Stakeholder communication treats both contexts (channel stakeholders + product domain experts)

When the cold-start interview detects a layered site (e.g., user says "B2B SaaS in the legal-tech space" or "marketplace for healthcare providers"), explicitly capture both sectors in the profile and apply the composition pattern at generate-time.

## Sector × decision-framework interaction

The decision framework in `../04-decision-framework.md` defaults vary by sector:

| Sector | Default for shipping llms.txt |
|---|---|
| dev-docs | **Ship** — real audience |
| ecommerce | **Skip** — invest in Product schema + third-party reviews |
| marketplace | **Ship** (ExampleMart pattern) — but only if avoiding bloat |
| news-publisher | **Skip** — invest in author E-E-A-T + Wikipedia citations |
| education | **Skip** — invest in canonical content + author bios |
| healthcare | **Skip** for marketing pages; **Ship** for clinical reference docs aimed at practitioners |
| fintech | **Skip** for marketing; consider for developer-facing API docs |
| government-civic | **Skip** generally; consider for open-data portals |
| gaming | **Skip** for marketing; consider for game-mod/API docs |
| b2b-saas | **Ship on docs subdomain only** |
| non-profit | **Skip** — invest in schema.org and earned citations |
| media-entertainment | **Skip** |

Defenders within "skip" sectors usually have:
- A bloated existing llms.txt that needs replacing
- An internal RAG/chatbot project that benefits from the curated map
- A forward-compatibility insurance rationale

Apply the standard honest-expectations conversation regardless of sector.
