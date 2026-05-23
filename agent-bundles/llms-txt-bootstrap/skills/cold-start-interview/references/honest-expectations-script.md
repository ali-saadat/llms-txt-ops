# Honest Expectations Conversation Script

*Full conversational script for Part 1 of the cold-start interview when the user's stated goal is "AI visibility" or "leadership mandate". Load this when those answers come up. Use the language file from `knowledge/languages/` for non-English versions.*

## English version

```
Important conversation before we continue.

The empirical record on llms.txt and AI citations is sobering. Three
independent studies all found no measurable AI-citation lift:

1. SE Ranking (Yulia Deda, November 7, 2025) — analyzed 300,000 domains
   using XGBoost + SHAP. Adoption was 10.13% overall but LOWER among
   high-traffic sites (8.27%) than mid-traffic (10.54%). When researchers
   removed the llms.txt feature from their model, prediction accuracy
   actually IMPROVED — the variable was noise.

2. OtterlyAI (Thomas Peham, February 5, 2026) — tracked 90 days of server
   logs. Out of 62,100 AI bot requests, only 84 touched /llms.txt — 0.1%.
   The file performed 3× WORSE than an average content page.

3. Search Engine Land (Ana Fernández, January 20, 2026) — controlled
   test on 10 sites. 8 of 10 saw no measurable change after publishing
   llms.txt. 1 declined 19.7%. 2 gained (12.5% and 25%) but with
   confounding factors — they got Bloomberg coverage, launched new
   functional content, fixed crawl errors. NOT the llms.txt file.

John Mueller (Google) has explicitly said Google does not consume the
file. On Bluesky in January 2026, asked whether Google hosting llms.txt
on its own properties was an endorsement: "I'm tempted to say something
snarky since this has come up so often, but to be direct, no."

The format's own creator, Jeremy Howard at Answer.AI, clarified on
Hacker News: "llms.txt files have nothing to do with crawlers or big
LLM companies. They are for individual client agents to use."

The bottom line: if your goal is to drive AI citations or get more
ChatGPT / Gemini / Claude referrals, llms.txt is empirically not the
lever. What does work, ranked by evidence:

1. External citations from authoritative sources — Wikipedia drives
   47.9% of top ChatGPT citations
2. Authoritative Reddit threads — Perplexity cites Reddit ~46.7% of the time
3. YouTube content with transcripts — 23.3% of Google AI Overviews
4. Original research / first-party data
5. Schema.org structured data
6. Author E-E-A-T with verified entity bylines (2.3× citation lift)
7. Statistics Addition (+41%), Quotation Addition (+28%), Cite Sources
   (Princeton paper findings)
8. Clean semantic HTML + Core Web Vitals + sitemap hygiene

So I want to give you two paths to choose between:

OPTION 1 — Don't ship llms.txt.

I can write up a clear recommendation memo for your team / leadership
explaining the decision. The memo will cite these three studies, name
the higher-leverage GEO toolkit alternatives, and lay out a clear
investment plan for items 1-8 above. This is the empirically-supported
choice for your situation.

OPTION 2 — Ship llms.txt anyway, with realistic expectations.

There are three defensible reasons that survive scrutiny:
  (a) Replacing a broken existing file — the status quo is the worst
      option, and a curated replacement is unambiguously better
      regardless of provider adoption.
  (b) Internal grounding asset — the same file works as the source-of-
      truth map for your own future RAG / chatbot / support assistant
      work. You get value from it even if no external AI ever reads it.
  (c) Forward-compatibility insurance — if the IETF AIPREF working group
      ratifies and providers commit (no guarantee, but watch-list item),
      you'll already be correct.

If you choose Option 2, I'll continue the interview and we'll set
expectations honestly throughout. Your llms.txt will get shipped, but
your team will not believe it'll drive AI traffic.

Which do you want — Option 1 or Option 2?
```

## Stakeholder-defense follow-ups

After the user chooses, prepare them for likely pushback:

### If they chose Option 1 (skip)

User concern: "But what if I'm wrong and llms.txt becomes important later?"

Response:
> "Fair question. The hedge is to revisit annually — when AIPREF ratifies or any major provider commits publicly, we re-evaluate in a 30-minute conversation. Meanwhile we invest in the items that have evidence today. If you want, I can set a calendar reminder for [date + 6 months]."

User concern: "My leadership specifically asked for llms.txt."

Response:
> "Two paths. (1) I can draft the memo explaining why we're investing differently — it cites the studies and shows the better path. Most leadership accepts evidence-based reasoning. (2) If leadership requires shipping, we ship with the defensible reasons explicitly stated upfront so no one is misled about expected outcomes."

### If they chose Option 2 (ship)

User concern: "How do we present this internally — what's the win?"

Response:
> "The internal narrative is: we replaced a [broken/missing/auto-generated] file with a curated one, the file now doubles as the grounding map for our own AI features, and we're forward-compatible against standards work in progress. Three concrete wins. No claim of AI traffic."

User concern: "What if it actually does drive citations?"

Response:
> "If it does, that's surprise upside. We won't pre-promise it because the empirical baseline says it won't. If we see citations in Bing AI Performance / Profound, we'll note it as a positive surprise, not as the expected outcome we promised."

## Cross-references

- `../SKILL.md` Step 4 Part 1
- `../../../knowledge/02-empirical-evidence.md` — primary source for all citations above
- `../../../stakeholder/expectations.md` — framing language for follow-up conversations
- `../../../knowledge/languages/<lang>.md` — for translated versions
