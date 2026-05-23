# 07 — Failure Modes and Anti-Patterns

*Status: Compiled May 15, 2026. The common mistakes that turn llms.txt into a liability or waste of effort.*

## Anti-pattern 1: The bloated-enumeration file (the 12.5 MB trap)

The single most common failure mode at scale.

### What it looks like

A site lists every page, every vendor, every product, every city × category combination — anything that has a URL gets enumerated. The result is a file in the tens-of-megabytes range with 40,000+ links.

### Why it happens

Auto-generation against sitemap.xml without filtering. The team treats llms.txt like a second sitemap.

### Why it's harmful

1. **Exceeds every LLM context window.** A 12.5 MB file cannot be ingested even by frontier models with 1M+ token windows. Most of it gets truncated.
2. **Signal dilutes.** High-priority pages get buried among thousands of low-priority ones. The LLM can't tell what's important.
3. **Duplicates what sitemap.xml already serves.** No information gain.
4. **Crawl budget waste.** AI bots that do fetch it are pulling MBs of low-value content.
5. **Stale risk amplified.** A 40k-link file is impossible to keep updated.

### Fix

Use the **URL pattern technique** (see `05-implementation.md`). List the top 10–12 highest-traffic entries explicitly; declare the URL pattern for the long tail; let sitemap.xml carry the actual enumeration.

The ExampleMart case study (`../case-study/example-marketplace-case.md`) is the canonical example of recovering from this: 12.5 MB → 27.8 KB while preserving full 81-province coverage.

## Anti-pattern 2: Confusing llms.txt with robots.txt

Common when teams approach llms.txt as a control-surface file.

### What it looks like

- Putting `Disallow:` directives in llms.txt (it has no such concept)
- Believing llms.txt blocks AI crawlers from training (it doesn't)
- Adding `User-agent: GPTBot` headers to llms.txt thinking it's robots.txt syntax

### Why it happens

Both files live at the site root. Names sound similar. Both relate to bots.

### The actual distinction

- **robots.txt**: opt-OUT / access control. Tells crawlers *whether* they can fetch.
- **llms.txt**: opt-IN curation. Tells AI agents *what's worth reading* if they do fetch.

### Fix

For blocking AI training: use robots.txt with the appropriate user-agents (`GPTBot`, `ClaudeBot`, `Google-Extended`, `Meta-ExternalAgent`). See `../reference/ai-bots.md`.

For opting OUT of AI grounding entirely: not yet a standard. The [IETF AIPREF working group](https://datatracker.ietf.org/wg/aipref/about/) is working on this.

## Anti-pattern 3: Marketing-speak descriptions

The descriptions after the colon are what LLMs use to decide whether to fetch the link. Marketing copy tells LLMs nothing useful.

### What it looks like

```markdown
- [Project Planning](https://example.com/planning): Revolutionize your workflow with our cutting-edge platform!
- [Photography](https://example.com/photography): Capture your perfect moments with the best in the business!
- [Venues](https://example.com/venues): Find your dream venue from our curated selection!
```

### Why it's harmful

- LLMs don't know what's actually on the page
- Generic language doesn't help retrieval-decision logic
- Looks promotional, reduces trust

### Fix

Write concrete, literal descriptions:

```markdown
- [Planning Tools](https://example.com/planning): Budget calculator with category benchmarks, date-driven to-do list, seating chart tool
- [Vendor Directory](https://example.com/vendors): 4,200+ vendors searchable by city + category + pricing tier, with portfolios and contract templates
- [Service Hubs](https://example.com/services): Top-level service-category directory — links to outdoor / hotel / historical / hall sub-types, each by city
```

## Anti-pattern 4: Listing everything

Defeats the purpose of curation. Forces LLMs to choose for you, which they do badly.

### What it looks like

- Every blog post listed
- Every product variant listed
- Every faceted URL (color × size × material combinations) listed
- Every paginated archive page listed

### Why it's harmful

Curation IS the value. A list of everything is just sitemap.xml in markdown.

### Fix

Apply ruthless inclusion criteria:
- For marketing sites: 5–10 most important pages
- For docs sites: top concepts + API surface + most-asked-about pages
- For e-commerce: category hubs only, never products
- For news/publisher: editorial standards + author hubs + canonical guides

Use the `## Optional` section for borderline inclusions you don't want to drop entirely.

## Anti-pattern 5: Treating llms.txt as a legal document

Some teams add DMCA notices, copyright assertions, training restrictions, or EULA language inside llms.txt.

### What it looks like

```markdown
# Our Company

> Welcome. By accessing this file you agree to our Terms of Service available at /terms. Reproduction of this content for AI training is strictly prohibited. All rights reserved. Patent-pending content. Do not redistribute. ...
```

### Why it's harmful

- LLMs are reading this to find content, not to read legalese
- Legal restrictions belong in robots.txt + AIPREF when ratified + terms of service pages
- Bloats the file without benefit

### Fix

Keep llms.txt purely descriptive. Put legal restrictions on dedicated pages and reference them from llms.txt as content (`/privacy`, `/terms`).

## Anti-pattern 6: Cloaking-style description mismatch

This is the most dangerous anti-pattern from a search-engine policy standpoint.

### What it looks like

- llms.txt description says one thing; actual page content is different
- Description promises detailed content; page is a thin teaser
- Description mentions data that doesn't exist on the page

### Why it's harmful

- John Mueller's January 2026 statements comparing llms.txt to meta keywords specifically referenced the gameability concern
- If Google ever enforces parity (and they have signaled they might), description-vs-content mismatch reads as cloaking
- Cloaking penalties exist in Google's spam policies

### Fix

Treasure-map honesty: every description must accurately describe what's actually on the linked page. Test by sampling 5 random links from your llms.txt and visiting them.

## Anti-pattern 7: Broken or non-canonical URLs

### What it looks like

- 404 links (page was moved or deleted)
- 301 redirect chains (link doesn't go directly to the final URL)
- Parameterized URLs (`?utm_source=...`) when there's a clean canonical
- Alternate-language URLs when there's a self-canonical
- HTTP URLs when site is HTTPS

### Why it's harmful

- 404s waste the AI's fetch budget and signal staleness
- Redirect chains add latency
- Non-canonical URLs split signals
- HTTP links can fail under HSTS

### Fix

Add link-checking to CI (`templates/validate.sh` does this). Run before every deploy. Reject anything that's not a direct 2xx.

## Anti-pattern 8: Forgetting to regenerate

A llms.txt published in 2024 and never touched is stale by 2026.

### What it looks like

- Last-reviewed date missing or 1+ year old
- Links to deprecated pages still present
- Mentions of features that no longer exist
- City list outdated (you added markets that aren't listed)

### Why it's harmful

LLMs surfacing your outdated content is worse than them not surfacing it at all. Customer support gets calls about features that were removed.

### Fix

- Add a `File metadata` block with last-reviewed date and review cadence
- Set a calendar reminder for quarterly review
- Tie llms.txt regeneration to the same CI pipeline as sitemap.xml regeneration
- Diff llms.txt in PRs so reviewers see the changes

## Anti-pattern 9: Stale CDN cache after deploy

Per [Open Shadow's 2026 guide](https://www.openshadow.io/guides/llms-txt): "stale CDN copies are the most common operational bug."

### What it looks like

- llms.txt deployed to origin
- CDN still serving old version
- Symptom: changes you made aren't reflected when fetching the public URL

### Fix

Add CDN purge to the deploy pipeline. See `06-deployment.md` for Cloudflare / Fastly examples.

## Anti-pattern 10: Encoding errors

### What it looks like

- Non-ASCII characters display as garbled (`Dü ün` instead of `ExampleMart`)
- Mojibake patterns (`Ã¼` instead of `ü`)
- Display differs between viewers / browsers / AI tools

### Two failure points

1. **The file itself is corrupted** — e.g., saved in Windows-1252 instead of UTF-8
2. **The server doesn't declare charset** — file is UTF-8 but `Content-Type` lacks `charset=utf-8`, so consumers guess wrong

### Fix

Both points have to be correct:

1. Save file as UTF-8 without BOM. Verify: `file -bi llms.txt` returns `charset=utf-8`.
2. Server sends `Content-Type: text/markdown; charset=utf-8`. Verify: `curl -I https://yoursite.com/llms.txt | grep -i content-type`.

CI script catches the first; manual cURL post-deploy catches the second.

## Anti-pattern 11: Indexing the llms.txt itself

### What it looks like

Search results include `https://yoursite.com/llms.txt` as a SERP entry.

### Why it's harmful

- Confuses search users
- Mueller (July 2025) said it should make sense to noindex it

### Fix

Add `X-Robots-Tag: noindex` header. **Do NOT also `Disallow:` it in robots.txt** — noindex only works on crawlable URLs.

## Anti-pattern 12: Not running CI validation before deploy

If you ship llms.txt without automated checks, you will eventually ship a broken one — bad encoding, dead links, size blowup, or removed-page references.

### Fix

Wire `templates/validate.sh` into the deploy pipeline. Block deploys that fail validation.

## Anti-pattern 13: Auto-generating from sitemap.xml unfiltered

The fastest path to the bloated-enumeration trap (#1).

### What it looks like

A script that reads sitemap.xml and emits a markdown list of every URL.

### Fix

Auto-generation is fine, but filter:
- Only include category hubs (not category × city × vendor permutations)
- Only include top-N pages by traffic
- Apply curation rules (no faceted URLs, no login pages, no per-user pages)

Hybrid is best: auto-fetch the URL set, hand-write descriptions, manual curation for the high-signal sections (instructions, routing, hierarchy).

## Anti-pattern 14: Vendor-coupling without exit plan

If you adopted llms.txt because your docs platform (Mintlify, Fern) auto-generates one, that's fine — but verify you can export the file if you switch platforms.

### Fix

Periodically download the file and check it into your repo as a backup. If you migrate platforms, you have a baseline to recreate from.

## Anti-pattern 15: Over-promising to stakeholders

The single most common project failure mode. Pitching llms.txt as "this will boost our AI traffic" sets up disappointment 3-6 months later when nothing happens.

### Fix

See `../stakeholder/expectations.md`. The honest framing:

> "I want to ship llms.txt for three reasons: replacing our bloated current file is unambiguously better; it doubles as internal grounding for our own AI work; and it's forward-compatibility insurance. It will NOT measurably increase ChatGPT or Gemini citations — the empirical evidence on that is clear. Investing in schema.org, external citations, and content quality is where we'll move the AI-visibility needle."

## Anti-pattern 16: PII / contact-detail leakage in vendor enumeration

A specific failure mode of the bloated-enumeration anti-pattern (#1) that deserves its own callout: many auto-generated marketplace files inline vendor phone numbers, email addresses, street addresses, and other PII directly into the descriptions next to each enumerated URL.

### What it looks like

```
- [Some Venue, Istanbul](https://example.com/venues/istanbul/some-venue): Phone: +90 2129630057. Modern interior, parking available
- [Another Venue, Beylikdüzü](https://example.com/venues/istanbul/another-venue): Phone: +90 2129630757. Garden, live music
```

### Why it's harmful

1. **GDPR / KVKK exposure**: phone numbers and addresses of small-business contacts are personal data; bulk-shipping them in a public crawlable file is a defensible compliance breach
2. **Stale data multiplied**: when the vendor changes phone numbers, every LLM that cached the file still cites the old one — and there is no way to recall
3. **Scraper bait**: the file becomes a one-stop-shop for spam-call enumeration
4. **Wrong layer**: contact details belong on the canonical vendor page (where they're maintained), not in a list

### Detection

```bash
# Phone-number leakage detection — adjust the country pattern as needed
grep -cE '\+?[0-9]{1,3}[-. ]?\(?[0-9]{3,4}\)?[-. ]?[0-9]{3,4}[-. ]?[0-9]{3,4}' llms.txt
# > 10 hits → likely PII enumeration
```

### Fix

1. Remove all individual vendor descriptions; reduce to category-city hubs + URL pattern (per #1's fix)
2. Add a directive: "Specific vendor contact information lives on the vendor's canonical page. Fetch the page rather than relying on cached data, which may be stale."
3. If your sitemap auto-generation harvested PII, also audit your sitemap.xml — same risk

## Anti-pattern 17: Non-markdown file format

The llms.txt spec requires plain markdown. Files served as RTF, HTML, PDF, or DOCX violate the spec and fail downstream tooling.

### What it looks like

- `llms.txt` actually contains RTF control codes (`\rtf1`, `\fonttbl`, `\cf2`)
- `llms.txt` contains HTML (`<html>`, `<body>`, `<a href="...">`)
- `llms.txt` is a PDF served with `Content-Type: text/plain` to "pass" naive checks
- `llms.txt` is generated by a CMS that wraps markdown in HTML

### Why it's harmful

1. **Spec violation**: clients that follow the spec strictly reject the file
2. **Parser failures**: every llms.txt parser written assumes markdown — wrapping in HTML/RTF means none of them work
3. **Encoding drift**: RTF specifically uses its own escape system (`\'e7` for `ç`, etc.) that bypasses UTF-8

### Detection

```bash
# Magic-byte check
head -c 5 llms.txt | hexdump -C
# RTF: starts with "{\\rtf"
# HTML: starts with "<!DO" or "<htm"
# PDF: starts with "%PDF"
# Real markdown: should be ASCII (often "# " for the H1)

file llms.txt
# Should report "ASCII text" or "UTF-8 Unicode text", not "Rich Text Format" / "HTML document" / "PDF document"
```

### Fix

1. Confirm the source-of-truth is plain markdown in your repo / CMS
2. Disable any "render before serving" middleware on the `/llms.txt` route
3. Serve with `Content-Type: text/markdown; charset=utf-8` (not `application/rtf`, not `text/html`)
4. Add `validate.sh` to CI — it catches non-markdown files via the magic-byte check

## Anti-pattern recovery summary

| Anti-pattern | Recovery approach |
|---|---|
| Bloated enumeration | URL pattern technique; reduce to top-N + sitemap pointer |
| Confusion with robots.txt | Separate concerns; robots.txt for access, llms.txt for curation |
| Marketing descriptions | Rewrite all descriptions as literal "what's on the page" |
| Listing everything | Apply ruthless curation criteria; use `## Optional` for borderline |
| Legal document mode | Move legalese to `/terms`; reference from llms.txt as content |
| Cloaking mismatch | Audit links; align descriptions with actual page content |
| Broken URLs | Run CI link-check; fix all 4xx/5xx |
| Forgetting to regenerate | Add metadata block + quarterly calendar reminder |
| Stale CDN | Add purge to deploy pipeline |
| Encoding errors | UTF-8 no BOM + server `charset=utf-8` |
| Indexing | Add `X-Robots-Tag: noindex` |
| No CI validation | Wire `validate.sh` into pipeline |
| Unfiltered auto-gen | Add curation filters |
| Vendor lock | Periodic backup to repo |
| Over-promising | Reframe to internal grounding + forward-compat |
| PII leakage in enumeration | Strip contact details; route to canonical vendor page |
| Non-markdown file format | Source-of-truth must be plain markdown; serve `text/markdown` |

## Cross-references

- For the case study showing recovery from anti-pattern #1 → `../case-study/example-marketplace-case.md`
- For implementation done right → `05-implementation.md`
- For deployment ops → `06-deployment.md`
- For stakeholder framing to avoid over-promising → `../stakeholder/expectations.md`
