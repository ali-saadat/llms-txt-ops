# 02 — Empirical Evidence: What Studies Actually Show

*Status: Compiled May 15, 2026. All claims sourced; see `../reference/sources.md`.*

## TL;DR

Three independent empirical studies as of May 2026 — covering 300k+ domains, 90-day server-log analyses, and controlled multi-site tests — all converge on the same conclusion: **publishing llms.txt does not produce measurable AI-citation lift.** Google has explicitly stated it does not consume the file. The format's own creator has clarified it was never meant for big LLM crawlers.

If a stakeholder claims llms.txt will drive AI traffic, the evidence base does not support them.

## The three primary studies

### Study 1: SE Ranking 300k-domain analysis

- **Author**: Yulia Deda, SE Ranking
- **Published**: November 7, 2025
- **URL**: [seranking.com/blog/llms-txt/](https://seranking.com/blog/llms-txt/)
- **Sample**: ~300,000 domains
- **Methodology**: Spearman correlation + XGBoost + SHAP analysis to test whether llms.txt correlates with AI citations

**Key findings**:
- Adoption: 10.13% overall
- **Lower among high-traffic sites (8.27%) than mid-traffic (10.54%)** — the opposite of what you'd expect if it worked
- **Removing the llms.txt feature improved the XGBoost model's accuracy** — the variable was noise

**Verbatim verdict**: *"llms.txt doesn't seem to directly impact AI citation frequency. At least not yet."*

**Why it matters**: This is the largest-N study. If llms.txt had even a small effect, it would show up at this sample size. It does not.

### Study 2: OtterlyAI 90-day server log analysis

- **Author**: Thomas Peham, OtterlyAI
- **Published**: February 5, 2026
- **URL**: [otterly.ai/blog/the-llms-txt-experiment/](https://otterly.ai/blog/the-llms-txt-experiment/)
- **Methodology**: Tracked server logs across multiple sites for 90 days, segmented by user-agent

**Key findings**:
- Out of **62,100 AI bot requests, only 84 (0.1%) touched `/llms.txt`**
- The file performed **3× worse than an average content page** on the same domain in terms of fetch frequency
- Most fetches were ChatGPT's browsing tool fetching specific URLs handed to it by users, not systematic crawling

**Why it matters**: This is the only study with direct server-log evidence. It quantifies the gap between "AI bots are out there" and "AI bots are reading llms.txt" — they are out there, they are not reading it.

### Study 3: Search Engine Land 10-site controlled test

- **Author**: Ana Fernández, Search Engine Land
- **Published**: January 20, 2026
- **URL**: [searchengineland.com/does-llms-txt-matter-467740](https://searchengineland.com/does-llms-txt-matter-467740)
- **Sample**: 10 sites across finance, B2B SaaS, ecommerce, insurance, pet care
- **Methodology**: Tracked 90 days pre-implementation, 90 days post-implementation

**Key findings**:
- **8 of 10 sites saw no measurable change**
- **1 site declined 19.7%**
- **2 sites gained (12.5% neobank, 25% B2B SaaS)** — but both with confounding factors (Bloomberg coverage, downloadable templates, new FAQ pages)

**Verbatim verdict**: *"Sites that launched new functional content saw gains. Sites that documented existing content saw no gains."*

**Why it matters**: This is the most controlled study. It directly tests "did adding llms.txt produce a lift?" The answer is no in 9/10 cases, and the one outlier (-19.7%) is concerning enough to flag.

## Adoption-erosion signals

| Signal | Source | Date |
|---|---|---|
| Walmart published llms.txt, then **removed it within ~60 days** | [ALLMO report](https://www.allmo.ai/articles/llms-txt) | Nov 2025 → Jan 2026 |
| Only **1 of top 50 AI-cited domains** (Target.com) has llms.txt | ALLMO report | Jan 2026 |
| High-traffic adoption (8.27%) is **lower** than mid-traffic (10.54%) | SE Ranking study | Nov 2025 |

These are not signals of momentum.

## On-record statements

### Google

**John Mueller, Bluesky, Jan 20, 2026** (in response to whether Google hosting llms.txt files counted as endorsement):
> *"I'm tempted to say something snarky since this has come up so often, but to be direct, no."*

**John Mueller, earlier (cited Search Engine Journal)**:
> *"None of the AI services have said they're using LLMs.TXT, and you can tell when you look at your server logs that they don't even check for it. To me, it's comparable to the keywords meta tag."*
> Source: [Search Engine Journal](https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/)

**Gary Illyes, Search Central Live, July 2025**: Confirmed Google does not support llms.txt and has no plans to. ([Search Engine Roundtable](https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html))

**John Mueller on noindex for llms.txt**, July 2025: A `X-Robots-Tag: noindex` header on `/llms.txt` "could make sense" to prevent it from showing up oddly in search results. ([SEJ](https://www.searchenginejournal.com/google-says-it-could-make-sense-to-use-noindex-header-with-llms-txt/551744/))

### Other providers (silence is itself a signal)

- **Anthropic** — publishes their own llms.txt; no public commitment that Claude consumes third-party files at crawl time
- **OpenAI** — no official statement on systematic consumption
- **Meta, Mistral** — silent
- **Microsoft Bing** — published [AI Performance report](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) (Feb 9, 2026) for citation telemetry, but no llms.txt-specific feature

### Format creator clarification

**Jeremy Howard (Answer.AI), Hacker News, [item 47058870](https://news.ycombinator.com/item?id=47058870)**:
> *"llms.txt files have nothing to do with crawlers or big LLM companies. They are for individual client agents to use."*

This is the most honest framing — and it's narrower than how llms.txt is usually marketed by vendors.

## SEO industry positions

### Skeptics (the mainstream)

| Voice | Position | Source |
|---|---|---|
| **Cyrus Shepard (Moz / Zyppy)** | Scored llms.txt **2/10 — lowest of 23 AI ranking factors** | [signal.zyppy.com/p/ai-citation-ranking-factors](https://signal.zyppy.com/p/ai-citation-ranking-factors) |
| **Mark Williams-Cook (Candour)** | *"llms.txt isn't a thing. No major LLMs have documented support... Spend your time elsewhere."* (808 LinkedIn reactions) | LinkedIn |
| **Lily Ray (Amsive)** | *"llms.txt and .md files are a distraction... for now it's a bit overhyped."* | Public statement |
| **Mike King (iPullRank)** | Tells clients to skip it — *"not standard or widely referenced by major systems."* | iPullRank AI Search Manual |
| **Eli Schwartz** | *"AEO is a reputation problem, not a technical one."* | Public talks |
| **Kai Spriestersbach** | *"The llms.txt is dead. More precisely: a dud."* | [Medium](https://medium.com/@kaispriestersbach/the-llms-txt-is-dead-more-precisely-a-dud-ab7bee4f469c) |
| **Duane Forrester (ex-Bing)** | Five abuse vectors — cloaking, keyword stuffing, content poisoning, redirect chains, trust laundering | [Substack](https://duaneforresterdecodes.substack.com/p/llmstxt-the-webs-next-great-idea) |

### Defenders (the minority)

| Voice | Position | Note |
|---|---|---|
| **Carolyn Shelby (Yoast)** | *"llms.txt isn't robots.txt: It's a treasure map for AI"* | Yoast was the first SEO plugin to ship a generator (June 2025). Shelby is at Yoast — vendor-adjacent. |
| **Semrush** | Added "missing llms.txt" warning to Site Audit | Most pro-llms.txt major tool vendor |
| **Mintlify** | Auto-generates for every docs site | The format's commercial champion |

### Pattern

**Vendors that don't sell content/brand services lean pro-llms.txt** (it gives them a shippable feature). **Vendors and agencies selling content/brand strategy lean anti.** Read positions accordingly.

## SEO tool vendor positions

| Vendor | Position | Site Audit support |
|---|---|---|
| Ahrefs | Skeptical | No check |
| Semrush | Pro | Yes (missing-file warning) |
| SE Ranking | Published the damaging study | No check |
| Moz / Zyppy | Cyrus Shepard scored it 2/10 | No check |
| Sistrix / Conductor / BrightEdge / SearchPilot | Invested in citation-tracking instead | No check |
| Yoast | Pro. Plugin ships generator | n/a |
| Google Search Console / Bing Webmaster Tools | No support | n/a |

## Counter-position: why ship llms.txt anyway?

The empirical evidence rules out citation lift as a benefit. But three real benefits remain:

1. **Replacing a broken/bloated file is unambiguously good.** If the site already has an llms.txt that's exhaustive (vendor-enumeration anti-pattern) or otherwise malformed, replacing it with a curated v3-style file is a clear improvement regardless of provider adoption. *Status quo is the worst option.*
2. **Internal grounding asset.** The same file works as the source-of-truth grounding map for the site's own future RAG / chatbot work. One file, two audiences. Value accrues even if no external AI ever reads it.
3. **Forward-compatibility insurance.** If AIPREF ratifies and providers commit, sites with curated llms.txt files are already correct. Cost is low — half a day of curation.

None of these are growth levers. All three are defensive or operational.

## What does actually move AI citations (the high-leverage list)

Ranked by impact, drawn from [Princeton's GEO paper (Aggarwal et al.)](https://arxiv.org/abs/2311.09735), [Peec AI's 30M-source analysis](https://almcorp.com/blog/top-domains-cited-by-ai-search/), [Wellows' 2,400-citation study](https://wellows.com/blog/social-media-ai-citations-report-2026/), and the [Conductor State of AEO/GEO 2026 report](https://www.conductor.com/academy/state-of-aeo-geo-report/):

1. **External citations from authoritative sources** — Wikipedia drives 47.9% of top ChatGPT citations; Wikipedia + Reddit drive >25% of US ChatGPT citations
2. **Authoritative Reddit threads** — Perplexity cites Reddit ~46.7% of the time
3. **YouTube content with transcripts** — 23.3% of Google AI Overview citations
4. **Original research / first-party data** — iPullRank's "Information Gain"
5. **Schema.org structured data** — sites with schema see up to 30% higher AI-overview visibility
6. **Author E-E-A-T with verified entity bylines** — 2.3× citation lift
7. **Statistics Addition (+41%) / Quotation Addition (+28%) / Cite Sources** — strongest Princeton findings
8. **Digital PR / brand mentions** — "reputation layer"
9. **Clean semantic HTML + Core Web Vitals + sitemap hygiene** — table stakes
10. **llms.txt** — bottom of the list or off it entirely

When advising stakeholders who want AI visibility, redirect engineering hours to items 1–9.

## Open questions / things to watch

- **IETF AIPREF working group** — when (or if) it ratifies, the standardization story changes
- **Any single major provider commitment** — if OpenAI, Anthropic, or Google publicly commits to crawl-time consumption, the empirical baseline shifts
- **AI search dashboards** — Bing AI Performance, Profound, Peec AI, OtterlyAI — these tools are getting better; their data will refine the empirical picture
- **Cloudflare's Markdown for Agents** — content-negotiation pattern may displace the `.md` mirror approach the spec recommends
