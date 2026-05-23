# Sector: News / Publisher

*Editorial sites, news organizations, magazine publishers, opinion sites, investigative journalism.*

## Decision default

**Skip llms.txt for the news content itself.** The empirical record applies most starkly here: AI citations come from external citation (Wikipedia, Reddit, social), author E-E-A-T, and clean structured data — not from llms.txt.

**Exception**: ship llms.txt for editorial standards, policies, and authority documentation if you want AI agents grounded in your editorial process when summarizing your content.

## Distinctive concerns

1. **Author trust is paramount** — AI Overviews and AI search heavily weight `Person`, `ProfilePage`, and `Article` schema. This is where to invest.
2. **AI scraping and licensing** — many publishers are negotiating individual licensing deals with AI providers. `robots.txt` AI-bot policies matter more than llms.txt.
3. **Date-of-record / publication date** — fresh content needs `datePublished` and `dateModified` schema; news rankings reward recency.
4. **Corrections policy** — distinct from privacy policy; AI agents should cite the corrections policy when handling user reports of errors.
5. **Provenance for AI-assisted content** — Google's "Who, How, Why" framework matters; visible bylines + AI-assistance disclosure.

## What to invest in instead of llms.txt

| Investment | Why |
|---|---|
| `Person` schema on author pages | 2.3× citation lift per Wellows study |
| `ProfilePage` schema (Google supports as of 2024) | Strengthens E-E-A-T signal |
| `Article` / `NewsArticle` schema with all fields | What AI Overviews actually consume |
| Wikipedia citations | Drives 47.9% of top ChatGPT citations |
| Original research / first-party data | Princeton paper Information Gain finding |
| Earning third-party citations | What Princeton showed actually moves citations |

## If you ship llms.txt anyway

For a news publisher, the defensible llms.txt should focus on:

1. **Editorial standards page** — your policies, sourcing methodology
2. **Corrections policy** — how errors are flagged and fixed
3. **Author directory** — link to all author profile pages
4. **Topic glossaries / explainers** — canonical reference content
5. **Series / vertical hubs** — major investigation series, beat hubs

Do NOT enumerate individual articles. They live in the sitemap. The articles index updates too fast for llms.txt cadence.

## Connector synergies

- `~~cms` — high value; CMS holds the editorial standards page, author directory
- `~~analytics` — track which evergreen / canonical content gets AI traffic
- `~~search-console` — Bing Webmaster Tools for AI Performance citations

## AI bot access decisions

News publishers face a particularly sharp choice on `robots.txt`:

| Strategy | Pros | Cons |
|---|---|---|
| Block all AI training bots | Protects content from being used for training without compensation | Loses AI search referrals if you also block search bots |
| Allow search/attribution bots, block training | Best of both — get cited, don't get scraped for training | Requires per-purpose-not-per-vendor configuration |
| Block all AI bots entirely | Maximum protection | Maximum invisibility in AI search |

Most publishers are converging on "allow search/attribution, block training, negotiate licensing for training" — but the policy is rapidly evolving.

## FAQPage rich result deprecation

[Google deprecated FAQ rich results May 7, 2026](https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957). The FAQPage **schema** is not deprecated — it's still useful for AI extraction even without rich-result display. Don't build SEO strategy around FAQPage markup alone; do still include it for AI parsing.

## Canonical examples

No widely-cited news publisher has a public llms.txt as of May 2026. The major test cases would be: NYT, Bloomberg, WSJ, Reuters, AP. All currently focus on schema.org + licensing deals rather than llms.txt.

## Template

Use `templates/llms-txt-marketing.md` as the base, but **strip** sections that don't apply to journalism (no transactional guidance, no e-commerce structure). Add editorial-standards + corrections-policy + author-directory sections.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `../03-seo-perspective.md` — GEO toolkit (high-leverage items)
- `_router.md` — sector classifier
