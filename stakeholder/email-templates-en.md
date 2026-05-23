# English Business Email Templates

*Reusable email patterns for llms.txt-related stakeholder communication. Anchored in the ExampleMart case but generalizable.*

## Template 1: Initial recommendation to ship/revise llms.txt

**Subject**: `[Project] llms.txt — Revised Proposal Attached`

```
Hi [Recipient],

First — genuine thanks for bringing me into this. The fact that [Site] 
already ships an llms.txt at all puts you ahead of roughly 90% of sites 
worldwide, and the instinct to question whether "longer is better" is 
exactly the right one. Most teams never get that far.

I dug into the current file and rebuilt it based on where the standard 
has moved in 2026. Quick summary below, full file attached.

The current long file — honest pros and cons

[Bullet table of pros and cons]

The instinct was right; the execution pattern just predates what the 
standard has become.

Why the revised file works better

[Comparison table: file size, link count, embedded directives, coverage, 
tools surfaced, agentic-commerce hook]

What this unlocks for [Site]

- Brand-level questions get answered accurately from the entity-facts block
- Long-tail queries resolve cleanly via URL patterns
- Legal/process questions route to authoritative guides — highest 
  citation-potential pages
- Forward-compatible with llms-full.txt and MCP — positioning ahead of 
  agentic commerce

The revised file is attached and ready to deploy. Replacing the current 
one is a one-afternoon change with meaningful upside.

Happy to jump on a call to walk through it or iterate on anything the 
[Site] team wants to emphasize differently. Thanks again for the trust 
in asking — this was a fun one.

Best Regards,
[Name]
```

## Template 2: Comprehensive response after receiving multiple sets of feedback

**Subject**: `Re: [Project] llms.txt — vN Revision Addressing All Feedback`

```
Hi [Recipient 1], hi [Recipient 2],

Thank you both — genuinely. [Recipient 1], your [N] structural questions 
sharpened the whole conversation. [Recipient 2], the depth of your 
[domain] review is exactly the kind of input that moves the file from 
"compliant with the spec" to "actually useful for the business." Every 
single one of your [N] points is reflected in vN, and in a couple of 
places the implementation goes a step further than the suggestion. 
Details below.

Two files attached:
1. project-llms-vN.txt — the deploy-ready file ([size], [link count] 
   curated URLs, [section count] sections, UTF-8 without BOM, fully 
   validated)
2. project-llms-deployment-spec.md — the Jira-ready deployment spec with 
   structural rationale, CI validation script, server config headers, 
   and a per-section breakdown of how the file gets generated and maintained

---

## Addressing [Recipient 2]'s [N] [domain] points

Going through each in order. Everything is in vN.

[For each point: name it, mark status, explain how vN addresses it, 
optionally note where implementation goes beyond the suggestion]

---

## Answering [Recipient 1]'s [N] structural questions

### Q1 — [Question 1]

[Concise answer with table or bullets]

### Q2 — [Question 2]

[Concise answer]

---

## What vN unlocks beyond the immediate request

- **One file, two audiences.** The same file serves external AI agents 
  AND doubles as the source-of-truth grounding map for our own future 
  RAG / chatbot / support-assistant work. No duplication of effort.
- **Forward-compatibility.** The IETF AIPREF working group (chartered 
  Jan 2025) is where the actual standardization is happening. If/when 
  it ratifies and major LLMs commit, we are already correct. Cheap 
  insurance.
- **Planned llms-full.txt companion.** Mintlify's pattern — concatenate 
  full markdown of ~30 highest-citation-potential articles for direct 
  context-window ingestion. Tracked as a planned next phase.

---

## Honest expectations setting

One thing I want to be transparent about so we're aligned on what 
success means.

The empirical record on llms.txt's direct impact on AI citations is 
sobering. Three independent studies — SE Ranking (n=300,000 domains, 
Nov 2025), OtterlyAI (90-day server logs, Feb 2026), and Search Engine 
Land (10-site test, Jan 2026) — all found no measurable AI-citation 
lift from publishing the file. John Mueller has explicitly said Google 
does not consume it.

So why ship anyway? Three reasons that survive scrutiny:

1. The status quo (the current bloated file) is the worst option. 
   Replacing it with vN is a clear, immediate improvement regardless 
   of provider adoption — we move from "broken" to "correct."
2. Internal grounding bonus. The instructions block is excellent 
   grounding material for our own AI work — value accrues even if no 
   external AI ever reads the file.
3. Forward-compatibility costs us nothing. If AIPREF ratifies and 
   providers commit, we're already correct.

The levers that actually move AI citations today are content quality, 
external citations (Wikipedia, Reddit, YouTube), schema.org, and clean 
semantic HTML — exactly the areas where the SEO team is already 
investing. The llms.txt work supports that broader strategy; it doesn't 
replace it.

I'd rather we ship vN with the right expectations than over-promise and 
disappoint anyone six months from now.

---

## Next steps

- **Jira ticket** — the deployment spec is structured to copy-paste 
  straight into the ticket. Includes acceptance criteria, validation 
  script, server config, deploy/rollback playbook.
- **CI validation** — wire the validation script into the build pipeline 
  so future refreshes can't ship broken.
- **Server headers** — Nginx config block in the spec.
- **robots.txt consistency check** — every URL in vN must be Allow: for 
  the AI user-agents we care about.
- **Quarterly refresh** — documented cadence; next review [date].
- **Monitoring** — log per-user-agent fetches to /llms.txt once deployed.

Happy to jump on a 30-minute call to walk through vN section by section.

Thanks again to you both for the time and the rigor on this.

Best Regards,
[Name]
```

## Template 3: Encoding/quality issue response (when the source is actually clean)

**Subject**: `Re: [Project] llms.txt — [Issue] Verification`

```
Hi [Recipient],

Thank you for the careful review and the specific examples — that's 
exactly the kind of feedback that lets us run a real verification.

We took your concern seriously and ran [N] independent checks on the 
source file:

[Table of checks with status:]
- File encoding: UTF-8 confirmed via file -bi
- BOM check: no BOM present
- Character inventory: [counts of relevant characters] all correctly 
  encoded
- Pattern search for the corrupted strings you reported: zero occurrences 
  in source
- Device 1: [tool] displays correctly
- Device 2: [tool] displays correctly
- SHA-256 hash: [hash] for downstream byte-level verification

Our conclusion: the source file is clean. What you observed is likely a 
display-layer or transit-layer issue — most plausible candidates being 
[font fallback / email gateway normalization / copy-paste intermediate 
processing].

To ensure this concern doesn't resurface, we're adding three defensive 
measures:

1. CI checks UTF-8 validity + BOM absence + character inventory before 
   every deploy. Build fails otherwise.
2. Post-deploy SHA-256 verification against the source hash. Catches 
   CDN / proxy transformations.
3. Future transfers via shared drive or Git PR rather than email. 
   Removes the intermediate-tool risk.

If you'd like to verify together, I'm happy to do a short screen share 
where we open the file side-by-side in [recommended viewer / VS Code] 
on your device. Just let me know a time that works.

Thanks again for catching this — even when it turns out the source is 
clean, having a robust diagnostic protocol in place is its own win.

Best Regards,
[Name]
```

## Template 4: Saying "no, we shouldn't ship llms.txt"

**Subject**: `Re: llms.txt for [Site] — recommend skipping, here's why`

```
Hi [Recipient],

Thanks for raising this. I want to give you an honest assessment rather 
than just agree because llms.txt is trending.

For [Site] specifically, I recommend NOT shipping llms.txt. Here's the 
reasoning:

**Site type**: [Site] is a [marketing site / blog / news publisher / 
small ecommerce]. The audience that consumes llms.txt directly — 
developers using coding agents like Cursor and Claude Code — isn't our 
audience.

**Empirical evidence**: Three independent studies (SE Ranking n=300k, 
OtterlyAI 90-day logs, Search Engine Land 10-site test) all found no 
measurable AI-citation lift from publishing llms.txt. John Mueller has 
explicitly stated Google does not consume it.

**Higher-leverage alternatives**: For our AI visibility goals, the 
empirically supported levers are:

1. Schema.org / JSON-LD on key pages — directly consumed by AI crawlers
2. Earning external citations (Wikipedia ~48% of top ChatGPT citations, 
   Reddit ~47% of Perplexity citations, YouTube ~23% of Google AI 
   Overviews)
3. Original research / first-party data
4. Author bios with verified entity bylines (2.3× citation lift)
5. Clean SSR/SSG for indexable content
6. IndexNow for Bing/Copilot freshness

I'd rather invest the engineering hours in items 1-6 than in a file 
that the empirical evidence doesn't support.

If shipping llms.txt is desired for forward-compatibility reasons — 
i.e., "what if it matters in the future?" — I can ship a minimal 
auto-generated version in a couple hours. But I want to be clear that's 
defensive cost, not an AI-visibility investment.

Happy to talk through this if it's useful.

Best Regards,
[Name]
```

## Template 5: Concise update to leadership

**Subject**: `llms.txt for [Site] — status update`

```
Hi [Recipient],

Quick status on the llms.txt work:

- Current file (12.5 MB, 43k links) replaced with curated v3 (27.8 KB, 
  153 links). Same coverage via URL patterns; 600× smaller.
- SEO team review integrated — six structural improvements (query 
  routing, priority hierarchy, transactional guidance, schema disclosure, 
  local intent, encoding).
- Deployment spec ready for the engineering team to open the Jira ticket.
- CI validation script in place — encoding + BOM + size + link liveness 
  checks pre-deploy.

Honest expectations: this doesn't drive measurable AI citations. The 
three real wins are (1) fixing the broken current file, (2) the file 
doubles as internal grounding for our future RAG/chatbot work, (3) 
forward-compatibility with the IETF AIPREF standardization path.

No action needed from you — flagging for visibility.

Best Regards,
[Name]
```

## Template 6: Vendor outreach (if a vendor reaches out about "AI search optimization")

**Subject**: `Re: AI search optimization for [Site] — interested in empirical basis`

```
Hi [Vendor],

Appreciate the outreach. Before we engage on AI-search optimization, I 
want to understand the empirical basis for your approach.

The independent studies I'm aware of all found no measurable AI-citation 
lift from llms.txt or related "AI optimization" tactics:

- SE Ranking, n=300,000 domains, Nov 2025 — null impact
- OtterlyAI, 90-day server logs across multiple sites, Feb 2026 — 0.1% 
  of AI bot traffic touched llms.txt
- Search Engine Land, 10-site controlled test, Jan 2026 — 8 of 10 sites 
  saw no change, 1 declined

What's the evidence base your optimization is built on? If you have 
controlled studies with statistical methodology, I'd be very interested.

If your evidence is anecdotal or vendor-reported, that's worth knowing 
too — I'd want to factor it differently.

Best Regards,
[Name]
```

## Cross-references

- For Turkish-language versions → `email-templates-tr.md`
- For framing language → `expectations.md`
- For real example of stakeholder communication arc → `../case-study/example-marketplace-case.md`
