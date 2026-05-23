# Sector-Specific Question Banks

*Detailed follow-up questions to ask during cold-start interview Part 4 (Information Architecture) based on the site type. Load when the user answers Part 0's site-type question.*

## Developer documentation

```
1. What's your product? (SDK, API, platform, framework)
2. What languages does your SDK support? (Python / JS / Go / Ruby / Java / etc.)
3. What's your API style? (REST / GraphQL / gRPC / Both)
4. Do you have an OpenAPI or GraphQL schema published? Where?
5. How many API endpoints? (rough count — affects whether to enumerate or pattern)
6. Do you have a webhook event catalog?
7. Are there multiple API versions live? Which version is documented?
8. What's your authentication model? (API key, OAuth, bearer token)
9. Do you have a sandbox / test environment?
10. Where do code samples live? (in-docs, GitHub, separate repo)
```

## E-commerce

```
1. What do you sell? (products / services / digital / subscription)
2. Approximately how many SKUs?
3. How is your category hierarchy structured? (top 2 levels — that's all that goes in llms.txt)
4. Do you have brand/manufacturer pages?
5. Do you ship internationally? Which markets?
6. What's your shipping/returns policy structure?
7. Do you have a size guide / fit guide?
8. Editorial / lookbook content?
9. Customer reviews — first-party only, or third-party (e.g., Yotpo, Trustpilot)?
10. AI-generated product images — using these? (Triggers Google Merchant Center IPTC requirement)
```

## Marketplace

```
1. What's the marketplace category? (services, products, real estate, gigs, hospitality, automotive, healthcare, events, etc.)
2. Approximately how many vendors/sellers?
3. Geographic dimension? (cities, regions, countries, all-N-provinces of a country)
4. URL pattern for the geographic dimension? (e.g., /{category}/{city-slug})
5. How many top-level service categories? (these go in llms.txt; vendors don't)
6. What's the inquiry-to-vendor flow? (quote request, contact form, instant booking)
7. Do you have planning tools or calculators? (budget planner, comparison tool, etc.)
8. Vendor onboarding flow URL?
9. Editorial articles? (guides, "how to choose a [vendor type]")
10. International sister brands?
```

## News / publisher

```
1. What's your editorial scope? (news, opinion, investigative, niche-specific)
2. How many authors / contributors?
3. Do you have author profile pages?
4. Editorial standards page URL?
5. Corrections policy URL?
6. Sections / beats / verticals — what's the top-level taxonomy?
7. Subscription / paywall model?
8. AI-assisted content — do you use it, and how do you disclose?
9. Press releases / public-relations content?
10. Archive — do you have evergreen content vs date-bound content?
```

## Education

```
1. What kind of institution? (K-12 / university / MOOC / training / LMS / language)
2. Multiple campuses or programs?
3. Accreditation? (which body)
4. Academic calendar — how often does enrollment open?
5. Faculty / instructor directory?
6. Tuition / pricing model?
7. Multiple languages of instruction?
8. Open educational resources (OERs)?
9. LMS — is it public-accessible or auth-gated?
10. Student vs prospective vs faculty audiences — distinct sections?
```

## Healthcare

```
1. What's the organization type? (hospital / clinic / pharma / payer / digital health / telehealth)
2. Patient-facing vs practitioner-facing content?
3. Regulatory jurisdiction? (US FDA / EU EMA / UK MHRA / etc.)
4. Clinical specialties / departments?
5. Prescribing information (PI) hubs — if pharma?
6. Continuing medical education (CME)?
7. Patient portals — auth-gated only?
8. Multi-language patient education needed?
9. HIPAA / GDPR posture?
10. Emergency / urgent care language — how do you direct users in crisis?
```

## Fintech / banking / insurance

```
1. What's the product? (banking / payments / lending / insurance / wealth / crypto / B2B fintech)
2. Consumer-facing vs developer-facing (API documentation)?
3. Regulatory jurisdiction? (US FINRA/SEC / EU MiFID II / UK FCA / APAC MAS/JFSA)
4. Pricing model? (fee, subscription, rate-based)
5. Compliance disclosures hub?
6. Risk disclaimers required?
7. KYC / AML flow?
8. For crypto: token listing page, regulatory status by jurisdiction
9. Developer APIs — webhook events, idempotency keys?
10. Sandbox / test environment?
```

## Government / civic

```
1. What level? (federal / state / municipal / international body)
2. Which services are documented? (apply for X, file Y, request Z)
3. Multi-language requirements? (statutory)
4. Accessibility compliance (Section 508 / WCAG / EU accessibility)?
5. Authority dating — how do you mark current vs superseded?
6. Restricted vs public records?
7. Open data portal? API for that?
8. Elections-related content?
9. Emergency hotlines — how are they surfaced?
10. Plain-language mandate?
```

## B2B SaaS

```
1. Product category? (CRM / ERP / project management / analytics / etc.)
2. Customer-facing marketing site + docs subdomain split?
3. Integration ecosystem — how many integrations? Partner portal?
4. Security / compliance certifications? (SOC 2, ISO 27001, HIPAA, GDPR)
5. Customer story / case study count?
6. Comparison content ("X vs Y") — do you publish these?
7. Pricing model? (per-seat, usage, tiered, enterprise-only)
8. API documentation? Where?
9. Changelog / roadmap?
10. Developer community / community forum?
```

## Gaming

```
1. Studio / publisher / platform / esports / community?
2. Are you documenting a game, an engine, a modding API, or a service?
3. Modding ecosystem? Workshop?
4. Multiple games / titles?
5. Regional release variations?
6. Age rating considerations? (ESRB / PEGI / CERO)
7. SDK documentation if you're a platform?
8. Patch notes / release cadence?
9. Community forums?
10. Microtransaction / in-game economy disclosures?
```

## Non-profit

```
1. What's your mission focus?
2. Country / region of operations?
3. Tax status? (US 501c3 / UK charity / etc.)
4. Annual revenue range?
5. Programs vs operations split?
6. Annual reports archive?
7. Financial transparency disclosures? (US Form 990)
8. Volunteer engagement flow?
9. Donation flow? (third-party processor)
10. Beneficiary privacy considerations?
```

## Media / entertainment

```
1. Type? (studio / network / streaming / podcast / music / talent agency / film)
2. Content library size?
3. Geographic distribution rights?
4. Talent / cast directory?
5. Press / media kit?
6. Awards / accolades hub?
7. For live events: scheduling and broadcast info?
8. For music: artist roster, label affiliations?
9. Royalty / licensing inquiries?
10. Investor relations (if public)?
```

## Generic / mixed

When site doesn't fit cleanly:

```
1. What's the primary purpose of the site? (in one sentence)
2. Who's the primary audience?
3. What's the conversion / engagement goal?
4. What are the top 5-10 pages by traffic?
5. Is there a documentation / help / FAQ section?
6. Is there commercial / transactional content?
7. Is there editorial content (articles, blog)?
8. How is content organized — categorical, hierarchical, temporal, flat?
9. Are there geographic / multi-tenant dimensions?
10. Are there multiple distinct audiences with different needs?
```

After these answers, classify into the closest existing sector and load that file.

## Cross-references

- `../SKILL.md` Part 4 (Information Architecture)
- `../../../knowledge/sectors/_router.md` — sector classifier
- `../../../knowledge/sectors/<sector>.md` — per-sector details
