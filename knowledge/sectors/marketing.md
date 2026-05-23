# Sector: Marketing / Brand Site

*Corporate marketing sites, brand homepages, product positioning pages, B2C brand awareness sites.*

## Decision default

**Skip.**

This is the sector where the empirical evidence most clearly says don't ship. Marketing sites don't have developer audiences (the only validated llms.txt consumer), and AI-citation studies consistently show null lift.

## Distinctive concerns

1. **Marketing language is the trap** — descriptions get filled with "revolutionize", "cutting-edge", "industry-leading" which tells LLMs nothing useful
2. **Product positioning vs facts** — promotional language conflicts with the "concrete description" llms.txt convention
3. **Lead-generation flow** — most marketing sites have a "Contact Sales" / demo-request flow that's the conversion point
4. **Press / media kit** — usually exists on most marketing sites; valuable for AI citation
5. **Awards / customer logos** — proof points that are useful for AI authority

## What to invest in instead

| Investment | Why |
|---|---|
| `Organization` schema | Anchor for AI knowledge graph |
| Authoritative press citations | Wikipedia, news articles, industry analyst quotes |
| FAQPage schema (note: rich result deprecated 2026, schema still useful) | AI agents extract from this |
| Author/leadership `Person` schema | E-E-A-T signal |
| Original research / data publications | Princeton paper "Information Gain" lever |
| Clear pricing page with `Offer` schema | Direct answer to common questions |

## If shipping anyway

Keep it minimal — 5-10 KB max. Strip ruthlessly:

- Brand entity facts
- Main product hubs (3-8 max)
- Pricing page link
- Customer-story directory
- Press / media kit
- Contact

Don't ship:
- Every blog post
- Every campaign landing page
- Every webinar / event page

## Honest expectations conversation

For marketing-only sites, the cold-start interview should explicitly push back if the stated goal is "AI visibility":

> "Marketing sites have no documented AI-citation lift from llms.txt. The studies (SE Ranking n=300k, OtterlyAI, Search Engine Land) all show null impact. For your site specifically, I'd recommend skipping llms.txt and investing the same engineering time in: (1) `Organization` schema on the homepage, (2) Wikipedia citation strategy, (3) original research / data publications, (4) authoritative press mentions, (5) FAQPage schema even though rich results are gone."

## Connector synergies

- `~~cms` — typically WordPress / Webflow / custom
- `~~analytics` — basic
- `~~ai-visibility` — track baseline citations to see if anything moves

## Template

Use `templates/llms-txt-marketing.md` if shipping anyway. The template has explicit guidance that most marketing sites should skip.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `../03-seo-perspective.md` — GEO toolkit alternatives
- `_router.md` — sector classifier
