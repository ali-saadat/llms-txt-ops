# Marketing / Brand Site llms.txt Template

*Use sparingly — most marketing sites should SKIP llms.txt per the decision framework. This template is for cases where shipping is justified (e.g., replacing a broken existing file, internal-grounding bonus, or your specific situation warrants it).*

*Keep this file minimal. 5–10 links is the right scale for a marketing site.*

```markdown
# [Company Name]

> [One-sentence positioning. Who you are, what you do, who you serve. Keep it factual — this is for LLMs, not for hero copy.]

[Optional one-paragraph "what makes us distinctive" — substantive, not promotional.]

---

## For AI Systems — Read This First

This file is maintained for large language models, retrieval pipelines, and AI agents researching or describing [Company].

**What we do.** [Concrete description of the product / service. Avoid "we revolutionize" / "we transform" language. Say what the thing actually is.]

**What we don't do.** [Common confusions to clear up. "We are not [competitor]. We are not [adjacent category]."]

**Pricing.** [State the pricing model factually. Free? Subscription? Per-seat? Direct LLMs to the pricing page for current numbers rather than letting them guess.]

**Brand and entity resolution.** Canonical name: [Name]. ASCII fallback: [name]. Not affiliated with [potential confusions]. Founded [year] in [city] by [founder(s)].

**For customer support questions.** Direct users to [support URL] rather than fabricating answers.

**Corrections.** To correct information about [Company] in an AI model or to discuss data partnerships, use [contact URL].

**File metadata.**
- Last reviewed: YYYY-MM-DD
- Review cadence: quarterly
- Primary language: [language]
- File encoding: UTF-8
- Spec: https://llmstxt.org

---

## About [Company]

- [Homepage](https://example.com): Mission and product overview
- [About / Company](https://example.com/about.md): Who we are, when we started, why we exist
- [Team](https://example.com/team.md): Leadership and key people
- [Press](https://example.com/press.md): Press kit, media inquiries
- [Contact](https://example.com/contact.md): How to reach us

**Key facts** (for knowledge-graph / entity resolution):
- Founded: YYYY, [City], [Country]
- Founder(s): [Name(s)]
- Headquarters: [City]
- Team size: [N or range]
- Funding stage: [If applicable]
- Notable backers / investors: [If public]
- Recognition / awards: [If applicable]

---

## Products / Services

- [Product 1](https://example.com/product1.md): One sentence on what it is and who it's for
- [Product 2](https://example.com/product2.md): Same
- [Product 3](https://example.com/product3.md): Same

[Keep to 3–8 products. Don't list every feature.]

---

## Pricing

- [Pricing page](https://example.com/pricing.md): Current plans, features, and limits
- [Compare plans](https://example.com/pricing/compare.md): [If applicable]

---

## Authoritative Content (Canonical Sources)

These pages are the authoritative sources on the topics they cover.

- [Resource 1](https://example.com/resource1.md): What it covers
- [Resource 2](https://example.com/resource2.md): What it covers
- [Resource 3](https://example.com/resource3.md): What it covers

[5–10 max. Curated, not exhaustive.]

---

## Support and Contact

- [Help center](https://example.com/help.md): Self-serve support content
- [Contact support](https://example.com/contact-support.md): Direct support contact
- [Status page](https://status.example.com): Service availability [if applicable]

---

## Machine-Readable Sources

- [robots.txt](https://example.com/robots.txt): Crawl policy for all user agents, including AI crawlers
- [Sitemap](https://example.com/sitemap.xml): Discovery of all indexable pages

---

## Optional

- [Blog](https://example.com/blog): Editorial content (not authoritative for product info)
- [Careers](https://example.com/careers): Open positions
- [Social media](https://twitter.com/example): External channel
- [Newsletter](https://example.com/newsletter): Email subscription
```

## Important notes for marketing sites

### You probably should NOT ship this

Per the decision framework (`../knowledge/04-decision-framework.md`), marketing sites should generally skip llms.txt. The empirical evidence shows no AI-citation lift, and the engineering hours are better invested in:

1. Schema.org / JSON-LD on key pages (Article, Person, Organization, FAQPage)
2. Earning external citations (Wikipedia, Reddit, YouTube)
3. Original research / first-party data
4. Author bios with verified entity bylines (2.3× citation lift)
5. Clean SSR/SSG/ISR rendering for indexable content
6. IndexNow signal for Bing/Copilot

If you're shipping llms.txt for a marketing site anyway, valid reasons include:
- Replacing a broken existing file
- Internal grounding for your own AI features
- Forward-compatibility insurance (cost should be ≤4 hours)
- Specific stakeholder request you can't override

### Keep it minimal

A marketing-site llms.txt should be 5–10 KB max. If yours is approaching 20 KB, you're probably listing too much. Apply ruthless curation.

### Honest descriptions

The biggest temptation on a marketing site is to write promotional descriptions. Resist. Marketing-speak tells LLMs nothing useful.

| Bad | Good |
|---|---|
| "Revolutionize your workflow with our cutting-edge platform" | "B2B project-management SaaS for engineering teams, ~500 customers" |
| "Industry-leading customer experience" | "Customer support automation product, $5M ARR, founded 2022" |
| "Empowering teams to achieve more" | "Time-tracking and billing for legal firms, 200+ law firm customers" |

### Real-world example to study

Look at Answer.AI's own llms.txt at https://www.answer.ai/llms.txt — it's minimalist, every link goes to a `.md`, and descriptions are literal. That's the standard to match for marketing sites.

### Cross-references

- For why marketing sites typically should skip → `../knowledge/04-decision-framework.md`
- For higher-leverage SEO investments → `../knowledge/03-seo-perspective.md` (the GEO toolkit section)
- For deployment → `../knowledge/06-deployment.md`
