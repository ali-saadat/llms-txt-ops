# Sources Bibliography

*All primary sources for empirical claims in this knowledge base. Use when citing back to original studies, statements, and specifications.*

## Spec and origin

- [llmstxt.org — official specification](https://llmstxt.org/)
- [Jeremy Howard / Answer.AI proposal, Sept 3 2024](https://www.answer.ai/posts/2024-09-03-llmstxt.html)
- [AnswerDotAI/llms-txt — reference implementation + llms_txt2ctx parser](https://github.com/AnswerDotAI/llms-txt)
- [Answer.AI's own llms.txt — canonical minimalist example](https://www.answer.ai/llms.txt)

## Standardization track

- [IETF AIPREF working group](https://datatracker.ietf.org/wg/aipref/about/) — chartered Jan 2025
- [draft-ietf-aipref-vocab](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/) — AI usage preferences vocabulary
- [draft-ietf-aipref-attach](https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/) — attaching preferences via robots.txt extensions, HTTP headers, .well-known/ai-preferences
- [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309) — robots.txt (formalized 2022, de facto since 1994)
- [sitemaps.org](https://www.sitemaps.org/) — sitemap.xml joint protocol (Google + Yahoo + Microsoft, 2006)

## Empirical studies (the three primary)

- **SE Ranking 300k-domain study, Yulia Deda, Nov 7 2025**: [seranking.com/blog/llms-txt/](https://seranking.com/blog/llms-txt/)
  - Verdict: *"llms.txt doesn't seem to directly impact AI citation frequency. At least not yet."*
  - Methodology: Spearman correlation + XGBoost + SHAP, n=300,000 domains
  - Key finding: removing llms.txt feature improved model accuracy (it was noise)
- **OtterlyAI llms.txt experiment, Thomas Peham, Feb 5 2026**: [otterly.ai/blog/the-llms-txt-experiment/](https://otterly.ai/blog/the-llms-txt-experiment/)
  - Verdict: 0.1% of AI bot traffic touched llms.txt; file performed 3× worse than average content page
- **Search Engine Land 10-site test, Ana Fernández, Jan 20 2026**: [searchengineland.com/does-llms-txt-matter-467740](https://searchengineland.com/does-llms-txt-matter-467740)
  - Verdict: 8 of 10 sites saw no change, 1 declined 19.7%, 2 gained (with confounders)

## Google statements

- [Mueller via Search Engine Journal — "comparable to the keywords meta tag"](https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/)
- [Search Engine Roundtable — "Google does not endorse llms.txt"](https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html) (Jan 2026, Mueller Bluesky post)
- [Mueller on noindex header for llms.txt, July 2025](https://www.searchenginejournal.com/google-says-it-could-make-sense-to-use-noindex-header-with-llms-txt/551744/)
- [Google AI Features and Your Website documentation](https://developers.google.com/search/docs/appearance/ai-features) — *"You don't need to create new machine readable files, AI text files, or markup..."*
- [Google scaled content abuse / spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google site reputation abuse policy](https://developers.google.com/search/blog/2024/11/site-reputation-abuse)
- [Google creating helpful content — "Who, How, Why"](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google dynamic rendering workaround](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering)

## Bing / Microsoft statements

- [Bing AI Performance report launch, Feb 9 2026](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)
- [Bing IndexNow](https://www.bing.com/indexnow)

## SEO industry positions

- [Ahrefs — What is llms.txt](https://ahrefs.com/blog/what-is-llms-txt/) — skeptical
- [Cyrus Shepard — AI Citation Ranking Factors (Moz/Zyppy)](https://signal.zyppy.com/p/ai-citation-ranking-factors) — scored llms.txt 2/10, lowest of 23 factors
- [Carolyn Shelby — llms.txt isn't robots.txt (Search Engine Land)](https://searchengineland.com/llms-txt-isnt-robots-txt-its-a-treasure-map-for-ai-456586) — defender position
- [Carolyn Shelby — No, llms.txt is not the new meta keywords](https://searchengineland.com/no-llms-txt-is-not-the-new-meta-keywords-458199)
- [Roger Montti — LLMs.txt: boost or waste of time? (SEJ)](https://www.searchenginejournal.com/llms-txt-for-ai-seo/556576/) — skeptical
- [iPullRank AI Search Manual (Mike King)](https://ipullrank.com/ai-search-manual) — tells clients to skip
- [Conductor State of AEO/GEO 2026 Report](https://www.conductor.com/academy/state-of-aeo-geo-report/)
- [Kai Spriestersbach — The llms.txt is dead (Medium, Feb 2026)](https://medium.com/@kaispriestersbach/the-llms-txt-is-dead-more-precisely-a-dud-ab7bee4f469c)
- [Duane Forrester — llms.txt: web's next great idea or spam magnet (Substack)](https://duaneforresterdecodes.substack.com/p/llmstxt-the-webs-next-great-idea)

## Implementation references

- [Mintlify — Best llms.txt platforms 2026](https://www.mintlify.com/library/best-llms-txt-platforms)
- [Mintlify — How often do LLMs visit llms.txt](https://www.mintlify.com/blog/how-often-do-llms-visit-llms-txt) — 5-6× more visits to llms-full.txt vs llms.txt
- [Mintlify — Best llms.txt platforms](https://www.mintlify.com/library/best-llms-txt-platforms)
- [Mintlify — Free generator](https://www.mintlify.com/library/free-llms-txt)
- [Firecrawl — How to create an llms.txt](https://www.firecrawl.dev/blog/How-to-Create-an-llms-txt-File-for-Any-Website)
- [Firecrawl hosted generator](https://llmstxt.firecrawl.dev/)
- [Cloudflare Markdown for Agents, Feb 2026](https://blog.cloudflare.com/markdown-for-agents/) — content negotiation pattern
- [Open Shadow 2026 guide](https://www.openshadow.io/guides/llms-txt)

## GEO / AEO empirical references

- [Princeton GEO paper, Aggarwal et al., 2023](https://arxiv.org/abs/2311.09735) — Statistics +41%, Quotation +28%, Cite Sources
- [KDD '24 GEO paper](https://dl.acm.org/doi/10.1145/3637528.3671900)
- [Peec AI — Top domains cited by AI search](https://almcorp.com/blog/top-domains-cited-by-ai-search/) — Wikipedia 47.9% of top ChatGPT citations
- [Wellows 2,400-citation study](https://wellows.com/blog/social-media-ai-citations-report-2026/) — author E-E-A-T 2.3× citation lift
- [Princeton paper showing Lost in the Middle, Liu et al.](https://arxiv.org/abs/2307.03172)
- [The Leaderboard Illusion, NeurIPS 2025](https://arxiv.org/abs/2504.20879)

## LLM features / case studies (for adjacent topic)

- [Moffatt v. Air Canada — McCarthy Tétrault analysis](https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot) — C$812.02 damages
- [Air Canada chatbot — CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)
- [NYC MyCity chatbot — The Markup original](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law)
- [NYC MyCity follow-up — The Markup](https://themarkup.org/news/2024/04/02/malfunctioning-nyc-ai-chatbot-still-active-despite-widespread-evidence-its-encouraging-illegal-behavior)
- [DPD chatbot incident — TIME](https://time.com/6564726/ai-chatbot-dpd-curses-criticizes-company/)
- [DPD chatbot — Silicon UK](https://www.silicon.co.uk/e-innovation/artificial-intelligence/dpd-disable-ai-chatbot-546650)
- [Klarna AI assistant — original press release](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/)
- [Klarna reversal — CX Dive](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/) — rehired humans
- [Vagaro / Zendesk AI case study](https://www.zendesk.com/customer/vagaro/) — 44% resolution rate, 3h→23min
- [NOBULL / Zendesk AI case study](https://www.zendesk.com/customer/nobull/) — 49% YoY ticket reduction

## Adoption directories

- [directory.llmstxt.cloud](https://directory.llmstxt.cloud/)
- [llmstxt.site](https://llmstxt.site/)
- [llmstxthub.com / thedaviddias/llms-txt-hub](https://github.com/thedaviddias/llms-txt-hub)
- [ALLMO report Jan 2026 — only Target.com in top 50 AI-cited has llms.txt](https://www.allmo.ai/articles/llms-txt)

## Real-world llms.txt examples (canonical references)

- [Answer.AI llms.txt](https://www.answer.ai/llms.txt) — minimalist canonical reference
- [Anthropic docs llms.txt](https://docs.anthropic.com/llms.txt) — large-scale, 1,400+ links
- [Cursor llms.txt](https://cursor.com/llms.txt)
- [Perplexity docs llms.txt](https://docs.perplexity.ai/llms-full.txt)
- [Stripe docs llms.txt](https://docs.stripe.com/llms.txt) — has instructions section
- [Cloudflare developers llms.txt](https://developers.cloudflare.com/llms.txt)

## Generators and tooling

- [Firecrawl llmstxt generator](https://llmstxt.firecrawl.dev/) / [GitHub](https://github.com/firecrawl/llmstxt-generator)
- [Mintlify free generator](https://www.mintlify.com/library/free-llms-txt)
- [docusaurus-plugin-llms](https://github.com/rachfop/docusaurus-plugin-llms)
- [next-plugin-llms (TurboDocx)](https://github.com/TurboDocx/next-plugin-llms)
- [Yoast llms.txt generator (June 2025, first SEO plugin)](https://yoast.com/press/yoast-launches-the-first-llms-txt-generator-in-an-seo-plugin-ushering-in-a-new-era-of-ai-ready-content/)
- [WordPress Website LLMs.txt plugin](https://wordpress.org/plugins/website-llms-txt/)
- [WordPress LLMs-Full.txt Generator plugin](https://wordpress.org/plugins/llms-full-txt-generator/)
- [llmstxtvalidator.dev](https://llmstxtvalidator.dev/) — validator (loose)

## AI citation tracking tools

- [Profound](https://www.tryprofound.com)
- [Peec AI](https://peec.ai/)
- [Goodie](https://higoodie.com)
- [OtterlyAI](https://otterly.ai)
- [AIPRM](https://www.aiprm.com/)

## Citation rule

When citing in advisory output, prefer:

1. Primary sources (Mueller's actual Bluesky post, the study URLs, official policy pages)
2. Specific quote with attribution + date when available
3. Quantitative findings (e.g., "10.13% adoption per SE Ranking n=300k") over qualitative claims

Avoid:

- Vendor-self-reported studies as primary evidence (Mintlify's "27% accuracy improvement" claim is unreplicated)
- Second-hand quotes when primary source exists
- Anecdotal claims as proof of pattern
