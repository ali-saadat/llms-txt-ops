# Stakeholder Expectations Framing

*The most important soft skill for llms.txt projects. Sets honest baselines so the project lands without disappointing leadership 6 months later.*

## The framing problem

llms.txt is in an awkward middle position:
- **Less impactful than vendor marketing claims** (no AI-citation lift per empirical evidence)
- **More valuable than pure skeptics admit** (real for dev docs, real for internal grounding, real as forward-compat)

Both stakeholder camps need to be re-framed. This file gives you the language.

## Camp 1: The over-believer

**Belief**: "If we add llms.txt, ChatGPT/Gemini/Claude will cite us more."

**Reality check needed**: This is empirically wrong as of May 2026.

**Framing language**:

> "I want to be honest about what shipping llms.txt will and won't do, because I'd rather we ship with the right expectations than feel disappointed in six months.
>
> Three independent studies — SE Ranking (n=300,000 domains, Nov 2025), OtterlyAI (90-day server logs, Feb 2026), and Search Engine Land (10-site controlled test, Jan 2026) — all found no measurable AI-citation lift from publishing llms.txt. John Mueller (Google) has explicitly stated Google does not consume it. The format's own creator, Jeremy Howard, has clarified that llms.txt is meant for client-side coding agents (Cursor, Claude Code), not for the big LLM crawlers.
>
> What actually moves AI citations today is: content quality, external citations from authoritative sources (Wikipedia drives 47.9% of top ChatGPT citations), Reddit threads (Perplexity ~46.7% Reddit-cited), YouTube with transcripts (23.3% of Google AI Overviews), schema.org structured data (up to 30% AI-overview visibility lift), and author E-E-A-T (2.3× citation lift). Those are where the engineering hours should go.
>
> For our site specifically, there are three real reasons to ship llms.txt anyway: [pick applicable ones below]."

The three real reasons (use the applicable ones):
1. **Replacing a broken existing file** — "Our current llms.txt is [12.5 MB / outdated / malformed]. Replacing it with a curated version is unambiguously better regardless of provider adoption."
2. **Internal grounding asset** — "The same file works as our source-of-truth grounding map for our own future RAG/chatbot work. We get value from it even if no external AI ever reads it."
3. **Forward-compatibility insurance** — "If the IETF AIPREF working group ratifies and providers commit, we're already correct. The cost is a half-day."

## Camp 2: The dismissive skeptic

**Belief**: "llms.txt is hype. Don't waste engineering time on it."

**Partial agreement, partial pushback**:

> "I agree it's not a citation lever — the studies are clear on that. I wouldn't ship llms.txt for AI traffic.
>
> But there are three real reasons to ship a curated version anyway:
>
> 1. If our current file is bloated or broken, replacing it is unambiguously better than leaving it. The status quo is the worst option.
> 2. The same file works as internal grounding for our own RAG/chatbot work, so we get value from it even if no external AI ever reads it.
> 3. If AIPREF ratifies the standardization path, we're already correct.
>
> The cost is a half-day to a day. The risk is zero. I'd ship it for reasons (1) and (2), not for AI visibility."

## Camp 3: The "what's the ROI?" pragmatist

**Belief**: "Show me the business case or this doesn't ship."

**Framing language**:

> "There isn't a measurable ROI on AI citations — I want to be upfront about that. The three studies that have tried to measure it found none.
>
> The business case is defensive, not offensive:
>
> 1. **Risk mitigation**: our current file is [describe state]. The bloat creates [waste / signal dilution / crawl-budget cost]. Fixing this is engineering hygiene.
> 2. **Internal asset**: the curated file becomes the source-of-truth grounding map for our own AI features. We're going to need that artifact anyway if we ship AI features in the next 12 months.
> 3. **Forward-compat insurance**: the IETF is standardizing this space (AIPREF working group). If providers commit, we're already correct. If they don't, we lost a half-day.
>
> Net: half-day investment, removes a known operational liability, gives us a reusable internal asset. The expected return on AI citations is zero — and that's what we should plan for."

## Camp 4: The SEO team

**Belief varies**: some SEO teams see llms.txt as part of GEO/AEO strategy; others dismiss it.

**Framing language** (works for both):

> "llms.txt isn't a ranking factor — Google has explicitly stated they don't consume it, and the empirical record shows no AI-citation lift. So this isn't an SEO investment in the traditional sense.
>
> But the file is high-leverage for SEO collaboration in a different way: it's where the SEO team's understanding of query → page routing, priority hierarchy, and commercial intent gets encoded for AI consumption. Even if no external AI ever fetches the file, the routing logic you'd encode is exactly the same routing logic that should inform our schema.org strategy, our internal-search ranking, and our future RAG/chatbot grounding.
>
> So I'd love your input on six specific things: [list the six SEO areas from the ExampleMart case]. The same input pays off in three places."

## Camp 5: Leadership / executive

**Belief**: usually some combination of "are we behind on AI?" mixed with "what's the cost?"

**Framing language**:

> "Quick honest summary on llms.txt:
>
> - **What it is**: a proposed markdown file at our site root that gives AI agents a curated map of our content. Started by Answer.AI in Sept 2024.
> - **What it does**: not much, in terms of measurable AI traffic. Three independent studies show no impact on AI citations. Google has said they don't use it.
> - **Why ship anyway**: [pick applicable reasons]
> - **Cost**: half-day to a day of engineering, plus a quarterly review thereafter.
> - **Risk**: zero, if we do it right.
>
> Recommend we ship a curated version, frame it internally as ['fixing the bloated current file' / 'building our internal grounding asset' / 'forward-compat insurance'], and don't communicate it as an AI-visibility play. That last part matters — over-promising on AI traffic is a real trap."

## Camp 6: The vendor pushing llms.txt as a service

**Belief**: "Our tool will optimize your llms.txt for AI search."

**Framing**: skeptical without being rude.

> "Appreciate the offer. Before we engage, I want to understand the empirical basis for the claim that an optimized llms.txt drives measurable AI search visibility. The independent studies I'm aware of — SE Ranking n=300k, OtterlyAI 90-day logs, Search Engine Land 10-site test — all found no measurable lift. John Mueller has stated Google doesn't consume it.
>
> What's the evidence base your optimization is built on? If you have case studies with controlled variables and statistical methodology, I'd be very interested to see them."

If they push back with anecdotes / vendor case studies / "well, Mintlify saw X" — politely note that Mintlify is the format's commercial champion with skin in the game, and their internal studies haven't been independently replicated.

## Universal honest-framing principles

1. **Separate technical expectations from political expectations.** Technical: no AI-citation lift. Political: shipping signals forward-thinking. Both are real; don't conflate.

2. **Use "three reasons that survive scrutiny" framing.** It's specific, defensible, and doesn't over-promise.

3. **Name the empirical sources.** SE Ranking n=300k, OtterlyAI 90-day, Search Engine Land 10-site. Specificity earns credibility.

4. **Quote Mueller verbatim where applicable.** *"I'm tempted to say something snarky since this has come up so often, but to be direct, no."* — January 2026, Bluesky.

5. **Acknowledge the legitimate uncertainty.** The space is evolving. AIPREF could ratify; a provider could commit. Be honest about what we don't know.

6. **Always offer the higher-leverage alternative.** Schema.org, external citations, content quality, clean HTML. Items 1-9 on the GEO toolkit list.

7. **Don't promise traffic.** Ever. The evidence doesn't support it.

8. **Do promise specific operational improvements.** "We'll go from a 12.5 MB file to a 27.8 KB curated one." "We'll have a CI pipeline that catches encoding errors." "We'll have a source-of-truth grounding map for our future RAG work." These are concrete and defensible.

## Stock phrases worth keeping

| Phrase | When to use |
|---|---|
| *"I want to be honest about what success means here"* | Opening for any expectations-setting conversation |
| *"Three independent studies all found null impact"* | Anchor for the empirical case |
| *"The status quo is the worst option"* | Justifying replacement of a bloated existing file |
| *"One file, two audiences"* | Explaining internal-grounding bonus |
| *"Forward-compatibility insurance"* | Justifying low-cost speculative work |
| *"The cost is a half-day. The risk is zero."* | Closing for any small project pitch |
| *"That's where the engineering hours should go"* | Redirecting to higher-leverage SEO investments |
| *"Disclaimers don't transfer liability"* | When discussing chatbot/LLM-feature risk (Air Canada) |
| *"Plan for the reversal"* | When discussing AI feature deployment (Klarna lesson) |

## What NOT to say

| Phrase | Why it's wrong |
|---|---|
| "This will increase our AI citations" | Empirically unsupported. Avoid. |
| "All the major LLMs will read this" | False as of May 2026. |
| "This is the new robots.txt" | Misleading — it's NOT robots.txt, and not on the same standardization path. |
| "We'll see traffic lift in 3-6 months" | No evidence basis. |
| "We need this to compete in AI search" | The competition is content, citations, schema — not llms.txt. |
| "It's risk-free to over-claim" | It is not. Over-promising is a real career risk. |

## Cross-references

- For empirical sources → `../knowledge/02-empirical-evidence.md`
- For decision framework → `../knowledge/04-decision-framework.md`
- For real stakeholder communication example → `../case-study/example-marketplace-case.md` and `email-templates-en.md`, `email-templates-tr.md`
