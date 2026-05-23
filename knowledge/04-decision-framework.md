# 04 — Decision Framework: Should You Ship llms.txt?

*Status: Compiled May 15, 2026. The empirical evidence does not support llms.txt as a growth lever. This framework determines when shipping is nonetheless worthwhile.*

## The honest default

**Default position: don't ship llms.txt unless one of the following applies.**

This is the inverse of how llms.txt is usually pitched. The evidence does not support it as an AI-visibility tactic, and the engineering hours are better spent on schema.org, external citations, content quality, and clean HTML. Ship llms.txt only when at least one of the "ship-worthy" cases applies.

## Ship-worthy cases

### Case 1: Developer documentation consumed by coding agents

**Ship it.** This is the one case with documented value.

- Audience: developers using Cursor, Claude Code, Cline, Aider, GitHub Copilot Workspace
- Mechanism: user pastes your llms.txt URL as a docs source; the IDE crawls it
- Effort: ~30 min if on Mintlify/Fern/GitBook (auto-generated); ~half-day if hand-rolled
- Risk: zero
- Benefit: real but bounded — developer adoption of your tool

Examples that are doing this well: Anthropic, Cursor, Perplexity, Stripe, Cloudflare, Vercel.

### Case 2: Replacing a broken / bloated existing file

**Ship the replacement.** The status quo is the worst option.

If the site already has an llms.txt that is:
- Enumerating thousands of vendor/product URLs (the 12.5 MB anti-pattern)
- Contains encoding errors
- Is auto-generated without curation
- Hasn't been updated in months

…then a curated replacement is unambiguously better than the existing file. The ExampleMart case study (`../case-study/example-marketplace-case.md`) is the canonical example: 12.5 MB → 27.8 KB curated, with full URL-pattern coverage preserving the 81-province addressability without enumeration.

### Case 3: Internal grounding asset

**Ship it if you're building your own AI features.** The same file works as the source-of-truth grounding map for your own future RAG / chatbot / support-assistant work. Value accrues even if no external AI ever reads it.

The instructions block, query routing, and curated link set are exactly what you'd hand a RAG system as a starting point. One file, two audiences.

### Case 4: Forward-compatibility insurance

**Ship a minimal version if cost is near zero.** The [IETF AIPREF working group](https://datatracker.ietf.org/wg/aipref/about/) (chartered Jan 2025) is where the real standardization is happening. If/when it ratifies and providers commit, sites with curated llms.txt files are already correct.

This is the weakest case standalone — only ship for this reason if a Mintlify/Fern auto-generator already handles it. Don't spend more than an hour on it for this alone.

## Skip cases (the empirical default)

### Marketing site / blog / general content

**Skip.** No evidence of AI-citation lift. Spend the engineering hours on:
- Schema.org / JSON-LD on key pages (Article, Person, Organization, FAQPage)
- Earning external citations (Wikipedia, Reddit, YouTube)
- Original research / first-party data
- Clean SSR/SSG/ISR rendering for indexable content

### E-commerce / catalog sites

**Skip the llms.txt itself.** But invest in:
- Product schema (Product, Offer, AggregateRating, Review)
- Authoritative third-party reviews (AI search engines pull from those)
- Image provenance (IPTC `DigitalSourceType: trainedAlgorithmicMedia` for AI-generated product images per Google Merchant Center policy — in force since 2024)
- IndexNow for catalog freshness signaling to Bing

### News / publisher

**Skip.** Avoid generic AI summaries. Invest in:
- Visible bylines with ProfilePage schema
- Editorial standards page
- IndexNow for freshness
- AI-attribution disclosures where readers would reasonably wonder how content was created

### Pure consumer brand site

**Skip.** Same as marketing.

## Mixed / hybrid sites

### Docs + marketing

**Ship llms.txt on the docs subdomain only.** Skip marketing pages.

Pattern:
- `https://docs.example.com/llms.txt` — curated developer-docs file
- No file at `https://example.com/llms.txt`

### SaaS product site (marketing + product docs + blog)

**Ship llms.txt scoped to product docs only.** Don't list marketing pages or blog posts unless they're canonical "how to use the product" articles.

### Marketplace (vendors + consumers + content)

**Ship llms.txt** — but the ExampleMart case is the playbook. Do NOT enumerate vendor URLs (let sitemap.xml carry them). DO include:
- Category hubs (your main entry points)
- Top-N city pages by traffic
- URL patterns for the long tail
- Free planning tools
- Editorial articles
- Sitemap pointers

## Decision matrix

| Site type | llms.txt | Why | Higher-leverage SEO investment |
|---|---|---|---|
| **Developer documentation** | **Ship** | Real audience (coding agents) | Clean Markdown + per-page mirrors + schema on key concept pages |
| **Marketing site / blog** | **Skip** | No evidence of impact | Schema.org, FAQ content, Reddit/YouTube presence, original research |
| **E-commerce** | **Skip** | No evidence; vendor-page enumeration risks bloat | Product schema, Review schema, IPTC provenance, third-party reviews |
| **News / publisher** | **Skip** | Generic AI summaries underperform | Bylines, ProfilePage schema, editorial standards, IndexNow |
| **Mixed (docs + marketing)** | **Ship on docs subdomain** | Docs audience is real; marketing isn't | Schema + clean SSR/SSG for marketing |
| **Marketplace** | **Ship (ExampleMart pattern)** | Curated hubs + URL patterns + tools work | Category-page schema, vendor LocalBusiness markup, Bing AI Performance monitoring |
| **Existing file is bloated/broken** | **Replace** | Status quo is worst option | Combine replacement with monitoring setup |
| **You're building your own RAG/chatbot** | **Ship** (internal grounding bonus) | One file, two audiences | Track which sections your own AI uses |
| **Already auto-generated by your platform** | **Keep** | No reason to remove | Don't expect impact |

## Cost / benefit summary

| Path | Engineering cost | Benefit |
|---|---|---|
| Auto-gen (Mintlify, Fern, etc.) | 0 hours | Compliant file; coding-agent value if applicable |
| Hand-rolled minimal | 4 hours | Compliant; signals editorial intent |
| Hand-rolled production (Stripe pattern with SEO routing) | 1-2 days | Compliant + useful for SEO routing + internal grounding |
| Replacing bloated existing | 1 day | Removes anti-pattern; meaningful upgrade |
| **NOT shipping** | 0 hours | Frees those hours for higher-leverage work |

## Refusal language for stakeholders pushing llms.txt for SEO

When a stakeholder believes llms.txt will drive AI citations:

> "Three independent studies — SE Ranking (n=300,000), OtterlyAI (90-day server logs), and Search Engine Land (10-site test) — all found no measurable AI-citation lift from publishing llms.txt. John Mueller has explicitly stated Google does not consume it. The format's own creator has clarified it's meant for client-side coding agents, not big LLM crawlers.
>
> I want us to ship llms.txt in the right cases, but I want to be honest about what success means. For AI visibility, the levers that empirically work are content quality, external citations (Wikipedia, Reddit, YouTube), schema.org, and clean semantic HTML. Those are where the engineering hours should go.
>
> For our site specifically, here's where llms.txt does still make sense: [insert applicable ship-worthy case]."

## Refusal language for stakeholders dismissing llms.txt entirely

When a stakeholder thinks llms.txt is pointless and won't approve any work:

> "I agree it's not a citation lever — the studies are clear. But there are three real reasons to ship a curated version anyway: (1) if our current file is bloated or broken, replacing it is unambiguously better than leaving it; (2) the same file works as internal grounding for our own RAG/chatbot work, so we get value from it even if no external AI ever reads it; (3) if AIPREF ratifies the standardization path, we're already correct.
>
> The cost is a half-day to a day. The risk is zero. I'd ship it for (1) and (2), not for AI visibility."

## Cross-references

- For empirical evidence to cite → `02-empirical-evidence.md`
- For SEO routing patterns → `03-seo-perspective.md`
- For implementation → `05-implementation.md`
- For deployment → `06-deployment.md`
- For real case showing this decision flow → `../case-study/example-marketplace-case.md`
- For stakeholder framing language → `../stakeholder/expectations.md`
