# Validation Notes — Corrections Applied During Research Synthesis

*Captured during the research consolidation phase that built this knowledge base. Documents which source claims were verified, which were corrected, and how.*

## Why this file exists

This knowledge base integrates findings from multiple research outputs — original deep research, two third-party AI-generated reports, and the real ExampleMart case. Source claims were independently verified before integration. This file documents the corrections applied so the skill is honest about its provenance.

## Corrections applied

### Model and pricing

| Original claim | Correction | Source verified against |
|---|---|---|
| Claude Haiku 4.5 pricing unstated | Actual pricing: **$1 / $5 per 1M tokens** (input/output), 200K context | [Anthropic — Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5) |
| Qwen3 Embedding has 262,144-token context | **Conflation**. Qwen3.6 base LM has 262K context; Qwen3 Embedding family has 8K max length | [Qwen3-Embedding GitHub](https://github.com/QwenLM/Qwen3-Embedding) |
| GPT-5.5 pricing $5/$30 | Verified accurate | [OpenAI GPT-5.5 announcement](https://openai.com/index/introducing-gpt-5-5/) |
| GPT-5.4 mini $0.75/$4.5 and nano $0.20/$1.25 | Verified accurate | OpenAI API docs |
| Gemini 3.1 Pro $2/$12, 2.5 Flash $0.30/$2.50, 3.1 Flash-Lite $0.25/$1.50 | Verified accurate (3.1 Pro jumps to $4/$18 above 200K context) | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| DeepSeek V4-Flash $0.14/$0.28, V4-Pro $0.435/$0.87 promo through May 31, 2026 | Verified accurate | [DeepSeek V4 preview release](https://api-docs.deepseek.com/news/news260424) |
| Mistral Small 4 $0.15/$0.6, Medium 3.5 $1.5/$7.5, Large 3 $0.5/$1.5 | Verified accurate | Mistral pricing page |
| Llama 4 Scout 10M context | Verified accurate | [Meta Llama 4 blog](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) |

### Case study figures

| Original claim | Correction | Source verified against |
|---|---|---|
| Klarna AI assistant success — no caveat | **Klarna later reversed and rehired humans** for customer service. The headline metrics (2.3M conversations, 700 agents equivalent, etc.) are real but not durable. | [CX Dive — Klarna reinvests in human talent](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/) |
| NYC MyCity chatbot sourced to AP | Original reporting was [The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law), not AP | The Markup primary URL |
| Air Canada C$812.02 damages | Verified accurate (C$650.88 fare + C$36.14 pre-judgment interest + C$125 tribunal fees) | [McCarthy Tétrault analysis](https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot) |
| Vagaro 44% AI resolution rate, 3h → 23min, CSAT 87% → 92% | Verified accurate | [Zendesk Vagaro case study](https://www.zendesk.com/customer/vagaro/) |
| NOBULL 49% YoY ticket reduction | Verified accurate | [Zendesk NOBULL case study](https://www.zendesk.com/customer/nobull/) |
| DPD chatbot disabled after swearing incident | Verified accurate (Ashley Beauchamp prompt sequence) | [TIME](https://time.com/6564726/ai-chatbot-dpd-curses-criticizes-company/) |

### llms.txt-specific

| Original claim | Correction | Source verified against |
|---|---|---|
| `/.well-known/llms.txt` framed as RFC 8615 convention | **Mintlify-only convention**, NOT in the official llmstxt.org spec | [llmstxt.org official spec](https://llmstxt.org/) — does not mention .well-known |
| Mueller's noindex statement implied 2026 | Statement is from **July 2025** | [SEJ — Mueller on noindex header for llms.txt](https://www.searchenginejournal.com/google-says-it-could-make-sense-to-use-noindex-header-with-llms-txt/551744/) |
| IndexNow as Bing's "primary" recommendation | **Interpretive** — Microsoft promotes IndexNow but does not use the exact word "primary" | Microsoft IndexNow page |
| Google Merchant Center IPTC requirement framed as new May 2026 | In force **since the 2024 product data spec update** — current but not new | Google Merchant Center policy page |
| FAQPage rich result deprecation overstated | The **rich result** is gone (May 7, 2026); the **FAQPage Schema.org markup itself is not deprecated** | [Search Engine Land — FAQ rich results deprecation](https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957) |
| DiscussionForumPosting + JSON-LD recommended | Google specifically recommends **Microdata or RDFa** for this schema type to avoid duplicating large text blocks | Google Search Central DiscussionForumPosting docs |
| SE Ranking 300k study findings | Verified accurate (10.13% adoption, removing variable improved XGBoost accuracy) | [SE Ranking study](https://seranking.com/blog/llms-txt/) |
| OtterlyAI 0.1% / 84 of 62,100 figure | Verified accurate | [OtterlyAI experiment](https://otterly.ai/blog/the-llms-txt-experiment/) |
| Search Engine Land 10-site study findings | Verified accurate (8 no change, 1 declined 19.7%, 2 gained with confounders) | [Search Engine Land](https://searchengineland.com/does-llms-txt-matter-467740) |
| Mueller Bluesky quote, January 2026 | Verified accurate | Search Engine Roundtable |

### Other technical claims

| Original claim | Correction | Source verified against |
|---|---|---|
| "Lost in the Middle" paper findings | Verified — Liu et al., arXiv 2307.03172, TACL 2024. Performance highest at start/end of context, degrades in middle. | [arXiv 2307.03172](https://arxiv.org/abs/2307.03172) |
| "The Leaderboard Illusion" paper | Verified — arXiv 2504.20879, NeurIPS 2025 poster. Argues Chatbot Arena distorted by private testing, data-access asymmetries. | [arXiv 2504.20879](https://arxiv.org/abs/2504.20879) |
| vLLM features (PagedAttention, continuous batching, etc.) | Verified | [vLLM docs](https://docs.vllm.ai/en/latest/) |
| Mintlify llms-full.txt 5-6× more visits than llms.txt | Verified per Mintlify's own log analysis | [Mintlify blog](https://www.mintlify.com/blog/how-often-do-llms-visit-llms-txt) |

## Source quality hierarchy

When sources disagreed or coexisted, the knowledge base prioritized:

1. **Primary statements** (Mueller's actual Bluesky post, the SE Ranking study URL, official policy pages)
2. **Reputable secondary coverage** (Search Engine Land, Search Engine Journal, Search Engine Roundtable when they're quoting/paraphrasing primary sources)
3. **Vendor-self-reported data** — included where useful but flagged as such (Mintlify's "27% accuracy improvement" is unreplicated)
4. **Anecdotal claims** — included only as illustration, never as proof of pattern

## What was NOT verified independently

The following claims appear in the knowledge base based on the source materials but should be re-verified before high-stakes use:

- **Wellows 2,400-citation study** — claim of "author E-E-A-T 2.3× citation lift" is cited but methodology unreviewed
- **Walker Sands "schema → 30% AI-overview visibility lift"** — vendor-reported, not independently replicated
- **Peec AI 30M-source analysis** — Wikipedia 47.9% citation share claim is from Peec AI's own analysis
- **Conductor State of AEO/GEO 2026 Report** — methodology not externally audited
- **Yoast launching first SEO plugin generator June 2025** — relies on Yoast's own press release

When citing these in advisory output, hedge appropriately: "per [vendor]'s analysis..." rather than "studies show..."

## Methodology notes

The validation was performed via:

1. **Parallel web research** — multiple research agents in parallel, each focused on a specific claim cluster
2. **Primary source seeking** — chasing back to the original URL / arXiv / press release rather than accepting secondary reporting
3. **Quote verification** — verbatim text matched against primary source where possible
4. **Date verification** — every "as of X" claim cross-checked against publication date

The fact-checking was scoped to claims that materially affect recommendations. Minor stylistic claims and adjective choices were not exhaustively verified.

## Recommended re-verification cadence

This knowledge base should be re-verified when:
- A major AI provider publicly commits to (or rejects) consuming llms.txt at crawl time
- The IETF AIPREF working group ratifies a draft
- A new independent empirical study is published (especially anything contradicting the three primary studies)
- Significant adoption shifts (e.g., a top-50 AI-cited domain adds or removes)
- Model landscape changes substantially (new pricing tiers, new flagship models, deprecations)

Suggested cadence: quarterly. Track via the watch-list in `../README.md`.

## Cross-references

- For full sources bibliography → `sources.md`
- For methodology of how this knowledge base was built → `../README.md`
