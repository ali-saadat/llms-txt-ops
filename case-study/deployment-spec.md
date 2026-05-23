# Example Marketplace llms.txt — Deployment Spec (v3)

*Jira-ready answers to the two open questions, plus deployment checklist. Adapted from the case-study project for general re-use.*

## Answers to the two structural questions

### 1. Based on what criteria is the new llms.txt structured?

| Criterion | Decision | Source / Reference |
|---|---|---|
| File spec | [llmstxt.org](https://llmstxt.org/) — H1, blockquote summary, optional body, H2 sections with `[Title](url): description` link lists, special `## Optional` section | Jeremy Howard / Answer.AI, Sept 2024 |
| Size budget | ≤ 50 KB (well within every LLM context window). Long-tail vendor URLs live in sitemap.xml, not in llms.txt | SE Ranking 300k-domain study; OtterlyAI server-log analysis showing llms.txt fetched ≪ 1% of AI bot traffic |
| Pattern | "Stripe-style" — embedded `For AI Systems — Read This First` instructions block, then curated link sections | Used by Stripe, Anthropic, Vercel, Cloudflare |
| What to include | Brand entity facts, main category hubs, top-12 regional hubs, planning tools, canonical editorial articles, sitemaps, sister brands | "Curated semantic map of source-of-truth pages" — llmstxt.org spec |
| What to exclude | All long-tail vendor pages (use URL pattern + sitemap), faceted/parameterized URLs, login pages, ephemeral promotions | Reduces ~12 MB → ~28 KB while preserving full coverage via URL pattern |
| SEO routing | Explicit query → URL mappings; SEO priority hierarchy (category > category-city > sub-category > vendor); transactional guidance — provided by SEO Lead | SEO review notes |
| Schema disclosure | Section listing the Schema.org types used on linked pages (LocalBusiness, Review, Article, Product, etc.) | SEO Lead's review |
| Local intent | Explicit "near me" / city-inference directive | SEO Lead's review |
| Encoding | UTF-8 without BOM; verified via `file -bi example-llms-v3.txt` should return `text/plain; charset=utf-8` | Resolves character-encoding concern from SEO review |
| Update cadence | Quarterly review documented in file metadata; regenerate on major IA changes | Standard practice; documented in `File metadata` block |

### 2. Based on what reference will the developer generate this file?

**Hybrid: hand-curated instructions + script-validated URL list.**

The file is NOT auto-generated end-to-end. The high-signal sections — the instructions block, the SEO routing rules, the transactional guidance, the schema-disclosure section, the priority hierarchy — are hand-curated because they encode editorial intent that no crawler can infer. Auto-generation would defeat the entire purpose of curation.

What the developer needs:

| Section | Source | Generation approach |
|---|---|---|
| H1 + summary | This spec | Static |
| `For AI Systems` directives | This spec + SEO review | Static; reviewed quarterly |
| `SEO Routing` query→URL table | SEO Lead's mappings | Static; updated by SEO team when IA changes |
| `SEO Priority Pages` hierarchy | SEO Lead's review | Static |
| `Transactional Guidance` | SEO Lead's review | Static |
| `Structured Data on [Site]` | Front-end team confirmation of which JSON-LD types ship on which page templates | Static; updated when schema changes |
| `About [Site] (Entity Facts)` | This spec | Static; reviewed quarterly |
| `Free Planning Tools` | Live URLs at the tools subdomain | Validated by build script (check 200 OK) |
| Category and service hubs | `https://example.com/sitemap.xml` filtered to category-hub URLs (one per category, no city subdivision) | Auto-generated list, hand-curated descriptions |
| Top-12 regional hubs | Sorted by traffic from Google Analytics (top 12 regions by sessions, last 90 days) | Auto-selected, hand-described |
| `Editorial Articles` | Curated by SEO/Content team (highest citation-potential articles) | Hand-curated; rotated based on content team's Q&A roadmap |
| `Machine-Readable Sources` | `https://example.com/sitemap.xml` index | Auto-fetched, listed |
| `Optional` section | This spec | Static |

**Validation step in CI/CD:**

```bash
# 1. Encoding check
file -bi example-llms-v3.txt | grep -q "charset=utf-8" || exit 1

# 2. Link-check every URL returns 200 OK (or 301 → 200)
grep -oE 'https://[^)]+' example-llms-v3.txt | \
  xargs -P 8 -I {} curl -s -o /dev/null -w "%{http_code} {}\n" {} | \
  grep -v "^2\|^301" && exit 1

# 3. Size check (alert if > 50 KB)
[ $(wc -c < example-llms-v3.txt) -lt 51200 ] || echo "Warning: size exceeds 50 KB"

# 4. Spec-shape check via llms_txt2ctx
pip install llms-txt && python -c "from llms_txt import parse_markdown; parse_markdown(open('example-llms-v3.txt').read())"
```

---

## Deployment checklist

### Server configuration (Nginx)

```nginx
location = /llms.txt {
    alias /var/www/example.com/llms.txt;
    default_type "text/markdown; charset=utf-8";
    add_header X-Robots-Tag "noindex" always;
    add_header Cache-Control "public, max-age=3600" always;
    add_header Access-Control-Allow-Origin "*" always;
}
```

Notes:
- `Content-Type: text/markdown; charset=utf-8` — addresses encoding concern at the wire level
- `X-Robots-Tag: noindex` — confirmed by John Mueller (Search Engine Journal, July 2025) as appropriate; prevents the file from cluttering SERPs
- `Cache-Control: max-age=3600` — 1-hour CDN cache; purge on deploy
- **Do NOT `Disallow: /llms.txt` in robots.txt** — noindex only works on crawlable URLs

### robots.txt consistency check

Every URL listed in `llms.txt` must be `Allow:` (or at minimum not `Disallow:`) for the AI user-agents we care about:
- `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`
- `ClaudeBot`, `Claude-User`, `Claude-SearchBot`
- `PerplexityBot`, `Perplexity-User`
- `Google-Extended` (separate from Googlebot — controls Gemini training/grounding)
- `Meta-ExternalAgent`, `CCBot`, `AI2Bot`

Decide access per-purpose, not per-vendor: typically allow search/attribution agents (they drive referrals) while blocking training crawlers if needed.

### Future companion file: `/llms-full.txt`

Out of scope for this ticket but worth tracking:
- Concatenate full markdown of the ~30 highest-citation-potential editorial articles
- Auto-generate as part of the same build pipeline
- Expected size: 1–5 MB
- Same headers as `/llms.txt`
- Mintlify's own log analysis shows `llms-full.txt` gets 5–6× more AI bot fetches than `llms.txt`

### Monitoring

Add to existing log pipeline:

```
GET /llms.txt → log: timestamp, user-agent, IP, response-time
GET /llms-full.txt → same
```

Dashboard slice: per-user-agent fetches over time. Realistic expectation: traffic dominated by ChatGPT browsing tool, not systematic crawlers. Set up alerting only for sudden drops (could indicate file is broken).

---

## Honest expectations setting

Per the consolidated research (May 2026):

- **No major AI provider has publicly committed to consuming llms.txt at crawl time.** Google explicitly said no (Mueller, Jan 2026). Anthropic, OpenAI, Meta, and Mistral are silent.
- **Three independent studies** (SE Ranking n=300k, OtterlyAI 90-day logs, Search Engine Land 10-site test) found **no measurable AI-citation impact** from publishing llms.txt.
- **The one defensible use case** is developer documentation consumed by coding agents (Cursor, Claude Code, Cline). For most other sites, the closest analog is users pointing their IDE at the docs — a tiny audience.

**So why ship it?** Three reasons:

1. **It's already there in a broken form.** Replacing the bloated file with a curated one is unambiguously better. The status quo is the worst option.
2. **Forward-compatibility.** If/when AIPREF ratifies and major LLMs commit (the IETF AIPREF working group is the actual standardization path), we are already correct.
3. **Internal usefulness.** The instructions block is excellent grounding material for any future RAG / chatbot work — same source-of-truth file for both external AI agents and internal pipelines.

**What we should NOT expect.** Measurable lift in ChatGPT/Gemini citations or AI-search referrals. The empirical record is clear. The levers that actually move AI visibility are content quality, external citations (Wikipedia, Reddit, YouTube), schema.org, and clean semantic HTML. Broader SEO investments are where the real upside sits.

---

## Summary of changes v2 → v3

Six SEO additions integrated from the SEO Lead's review:

1. **Local intent / "near me" directive** added to the `For AI Systems` block
2. **New section: SEO Routing — Which Page Should Answer Which Query** — explicit query→URL mapping table
3. **New section: SEO Priority Pages — Selection Hierarchy** — broad → category-city → sub-category → vendor
4. **New section: Transactional Guidance** — routes commercial-intent queries to listing pages, not blog content
5. **New section: Structured Data on [Site]** — discloses Schema.org types per page template
6. **Encoding verified** — file is UTF-8 without BOM; server config sets `charset=utf-8` explicitly

File size: ~28 KB (vs v2 ~22 KB, vs original ~12 MB).

Two operational adds:

- **File metadata block** updated: version 3.0, last reviewed [date]
- **Deployment headers documented** in this spec (Nginx + robots.txt consistency)
