# 01 — Foundations: What llms.txt Is and Where It Stands

*Status: Compiled May 15, 2026. Sources in `../reference/sources.md`.*

## TL;DR

`llms.txt` is a **community-proposed**, **non-standardized** markdown file format intended to give LLMs and AI agents a curated, structured map of a website's most important content. Proposed by Jeremy Howard (Answer.AI / fast.ai) on September 3, 2024. It is **not** an IETF, W3C, or IANA standard, and no major AI provider has publicly committed to consuming it at crawl time.

## Origin

- **Proposer**: Jeremy Howard, [Answer.AI](https://www.answer.ai/) / [fast.ai](https://www.fast.ai/)
- **Date**: [September 3, 2024 blog post](https://www.answer.ai/posts/2024-09-03-llmstxt.html)
- **Spec**: [llmstxt.org](https://llmstxt.org/)
- **Reference repo**: [AnswerDotAI/llms-txt](https://github.com/AnswerDotAI/llms-txt)
- **Reference parser**: `llms_txt2ctx` CLI in the same repo

The original framing was: "a proposal to provide information to help LLMs use websites." Howard's later HN clarification narrowed the scope further: *"llms.txt files have nothing to do with crawlers or big LLM companies. They are for individual client agents to use."*

## The format

### Required elements

Only **one element is strictly required**: a single H1 heading with the site/project name.

### Recommended structure

```markdown
# Site / Project Name

> One-sentence summary giving key context to the LLM.

Optional framing paragraphs. No headings allowed in the body before the first H2.

## Section Name
- [Page title](https://site.com/page.md): Short description for the LLM
- [Another page](https://site.com/other.md): Another description

## Another Section
- [Page](https://site.com/p.md): Description

## Optional
- [Skippable page](https://site.com/extra.md): Lower-priority, droppable under context pressure
```

### Parser-special rules

- **`## Optional`** is the one section name with semantic meaning. Parsers MAY drop it under context-window pressure. Use it for secondary/skippable material.
- Link list items follow the exact form: `- [Title](url): description`. The description after the colon is what LLMs use to decide whether to fetch the link.
- The H1 is the only required element. Everything else is optional but conventional.

### Canonical location

- **`/llms.txt`** at the site root — per the official spec
- **`/.well-known/llms.txt`** — a Mintlify-introduced mirror convention, **NOT in the official spec** (don't conflate)

## llms.txt vs llms-full.txt

Only `llms.txt` is in the formal spec. `llms-full.txt` is a community convention popularized by Mintlify.

| File | Purpose | Size |
|---|---|---|
| `llms.txt` | Curated *index* of links + descriptions | Small (typically <50 KB) |
| `llms-full.txt` | Concatenated full markdown of every linked page | Large (often MB / millions of tokens) |

Per [Mintlify's log analysis](https://www.mintlify.com/blog/how-often-do-llms-visit-llms-txt), `llms-full.txt` gets **5–6× more visits** than `llms.txt`, mostly from ChatGPT's browsing tool when handed a URL by a user.

## Standardization status

**Not standardized.** None of:
- IETF RFC
- W3C Recommendation
- IANA registration
- ISO standard

It remains a community proposal under Answer.AI's stewardship.

### Where the actual standardization is happening

The [IETF AIPREF working group](https://datatracker.ietf.org/wg/aipref/about/) (chartered January 2025) is where AI-related web standards are being built — but it is **extending robots.txt**, not adopting llms.txt. Two active drafts:

- [draft-ietf-aipref-vocab](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/) — vocabulary for AI-usage preferences (train / search / RAG / summarize)
- [draft-ietf-aipref-attach](https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/) — attaching preferences via robots.txt extensions, HTTP headers, and `.well-known/ai-preferences`

When AIPREF ratifies, it will likely subsume access-control signaling that llms.txt is sometimes mistakenly thought to provide. llms.txt's *curation* role (which pages matter) is orthogonal and could survive — but the standardization momentum is not behind it.

### Historical comparison

| Standard | Origin | Path to legitimacy |
|---|---|---|
| robots.txt | De facto from 1994 | [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309) ratified 2022 — 28 years to formal status. Succeeded because Google, Yahoo, Microsoft all publicly committed to honoring it. |
| sitemap.xml | Google + Yahoo + Microsoft joint proposal 2006 | Never formally standardized (sitemaps.org joint protocol). Adoption driven by search engine commitment. |
| llms.txt | Sept 2024 community proposal | No major provider commitment as of May 2026. No path to formal standardization. |
| meta keywords | Early 1990s | Used widely, then dropped by Google due to abuse. Cited by Mueller as the analog to llms.txt. |

## Adoption landscape (May 2026)

### Verified named adopters

- **Major AI labs (publish but don't necessarily consume third-party files)**: [Anthropic](https://docs.anthropic.com/llms.txt), [Cursor](https://cursor.com/llms.txt), [Perplexity](https://docs.perplexity.ai/llms-full.txt)
- **Developer infrastructure**: Vercel, Cloudflare, Stripe, Supabase, Hugging Face, ElevenLabs, Zapier, Resend, Fireworks AI, Writer, Aptos, Chakra UI, Mastercard developer platform, Coinbase, Pinecone, Windsurf
- **Inflection point**: [Mintlify auto-generated llms.txt for every docs site it hosts starting November 2024](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt) — overnight added thousands of dev-doc sites

### Directories tracking adoption

- [directory.llmstxt.cloud](https://directory.llmstxt.cloud/)
- [llmstxt.site](https://llmstxt.site/)
- [llmstxthub.com](https://github.com/thedaviddias/llms-txt-hub)

### Overall scale

- [SE Ranking's 300k-domain crawl](https://seranking.com/blog/llms-txt/) (Nov 2025): ~10% adoption overall, **lower among high-traffic sites (8.27%)** than mid-traffic (10.54%) — opposite of what you'd expect if it worked
- [ALLMO's January 2026 report](https://www.allmo.ai/articles/llms-txt) found only **1 of the top 50 most-cited AI-search domains** (Target.com) had an llms.txt
- **Walmart published one in November 2025 and removed it by January 2026** — early signal of disenchantment

## Who actually consumes llms.txt

This is the most load-bearing question and the answer is sobering.

| Consumer | Status as of May 2026 |
|---|---|
| **Google / Gemini** | **Explicit no.** John Mueller (Bluesky, Jan 2026): *"I'm tempted to say something snarky since this has come up so often, but to be direct, no."* Gary Illyes confirmed at Search Central Live (July 2025). |
| **Anthropic / Claude** | Publishes [docs.anthropic.com/llms.txt](https://platform.claude.com/docs/llms.txt) but has not publicly committed Claude to fetching third-party files at crawl time. |
| **OpenAI / ChatGPT** | No official statement. Browsing tool fetches URLs handed to it (including llms.txt), but no systematic crawler behavior. |
| **Perplexity** | Publishes one. Server-log analyses show PerplexityBot largely absent from llms.txt requests. |
| **Cursor / Claude Code / Cline / Aider** | **Real consumption.** Users paste an llms.txt URL as a docs source; the IDE crawls it. User-initiated, not automatic. |
| **Meta / Mistral** | Silent. |

**Key insight**: No equivalent of the 1994 robots.txt commitment exists for llms.txt. That commitment is why robots.txt and sitemap.xml succeeded; its absence is why meta keywords failed. Mueller has drawn that exact parallel.

## Format ecosystem

### Real-world examples to reference

| Site | llms.txt URL | Why it's a useful reference |
|---|---|---|
| Answer.AI (canonical) | https://www.answer.ai/llms.txt | Minimalist, every link goes to a `.md`, descriptions literal |
| Anthropic | https://docs.anthropic.com/llms.txt | Large-scale (1,400+ links), organized by API surface |
| Stripe | https://docs.stripe.com/llms.txt | Has an instructions section — prompt engineering shipped as static file |
| Cloudflare | https://developers.cloudflare.com/llms.txt | Vertical-by-vertical, 20+ products |

### Format variants observed in the wild

- **Pure curation** (Answer.AI style): bare minimum, link list only
- **Stripe pattern** (instructions-first): embedded `## For AI Systems — Read This First` block with directives, then curated links. **This is the modern best practice** and what we recommend.
- **Auto-generated** (Mintlify, Fern): every docs page automatically listed. Less curated but zero effort to maintain.
- **Bloated/exhaustive** (the anti-pattern): every URL on the site enumerated. The 12.5 MB ExampleMart pre-revision case is an example. **Do not do this.**

## Spec gaps worth knowing

The official spec is intentionally minimal. It does NOT specify:

- **Internationalization (i18n)**: No guidance on multi-language sites. Emerging convention: per-locale files at `/en/llms.txt`, `/de/llms.txt` mirroring hreflang clusters.
- **HTTP headers**: No `Content-Type` recommendation. Conventional choices: `text/markdown; charset=utf-8` or `text/plain; charset=utf-8`.
- **Caching**: No recommendation. Practical default: `Cache-Control: public, max-age=3600` with explicit purge on deploy.
- **Indexing**: No guidance on whether the file itself should be indexed. [John Mueller (SEJ, July 2025)](https://www.searchenginejournal.com/google-says-it-could-make-sense-to-use-noindex-header-with-llms-txt/551744/) said `X-Robots-Tag: noindex` "could make sense" — recommended default.
- **`.md` mirrors**: The spec encourages serving `.md` versions of HTML pages but doesn't specify how. Modern alternative: HTTP content negotiation per [Cloudflare's Markdown for Agents (Feb 2026)](https://blog.cloudflare.com/markdown-for-agents/).
- **Sitemap relationship**: Not specified. Practical reading: llms.txt is a *curated subset* of sitemap.xml's universe, not a replacement.

## Cross-references

- For decision framework (should I ship?) → `04-decision-framework.md`
- For the empirical record (what studies say) → `02-empirical-evidence.md`
- For implementation details → `05-implementation.md`
- For deployment ops → `06-deployment.md`
- For the SEO routing layer that turns llms.txt from "compliant" to "useful" → `03-seo-perspective.md`
