# AI Crawler User-Agent Reference

*Current AI bot user-agent inventory as of May 2026. Use for robots.txt configuration and consistency with llms.txt URL allowlist.*

## Bot inventory

### OpenAI

| User-agent | Purpose | Typical use |
|---|---|---|
| `GPTBot` | Training data collection | Block to opt out of OpenAI training |
| `OAI-SearchBot` | Search / attribution crawler | Allow to drive ChatGPT Search referrals |
| `ChatGPT-User` | User-triggered browsing (when ChatGPT users hand it a URL) | Allow — user-initiated, not systematic |

### Anthropic

| User-agent | Purpose | Typical use |
|---|---|---|
| `ClaudeBot` | Training data collection | Block to opt out of Anthropic training |
| `Claude-User` | User-triggered browsing | Allow — user-initiated |
| `Claude-SearchBot` | Anthropic search / attribution | Allow to drive Claude Search referrals |

### Google

| User-agent | Purpose | Typical use |
|---|---|---|
| `Googlebot` | Standard Google Search crawler | Allow (you want this for Search) |
| `Google-Extended` | **Separate** Gemini training and grounding | Block to opt out of Gemini training (does NOT block Google Search) |
| `Google-Agent` | New AI-agent traffic UA (added 2026) | Decide per your AI-agent policy |

### Perplexity

| User-agent | Purpose | Typical use |
|---|---|---|
| `PerplexityBot` | Perplexity indexing | Allow to be indexed in Perplexity |
| `Perplexity-User` | User-triggered Perplexity browsing | Allow — user-initiated |

### Meta

| User-agent | Purpose | Typical use |
|---|---|---|
| `Meta-ExternalAgent` | Meta AI crawling | Block to opt out of Meta AI |
| `Meta-ExternalFetcher` | Meta on-demand fetches | Decide per policy |
| `FacebookExternalHit` | Open Graph / link preview rendering | Allow for social-share previews |

### Microsoft / Bing

| User-agent | Purpose | Typical use |
|---|---|---|
| `Bingbot` | Standard Bing Search crawler | Allow for Bing Search |
| `BingPreview` | Bing preview fetcher | Allow |

Bing has not announced a separate AI-training crawler as of May 2026. AI features (Copilot, Bing AI summaries) use Bingbot results.

### Other notable

| User-agent | Purpose | Typical use |
|---|---|---|
| `CCBot` | Common Crawl (training corpus for many LLMs) | Block if you want broad opt-out from public training sets |
| `AI2Bot` | Allen Institute for AI | Decide per policy |
| `Applebot-Extended` | Apple Intelligence training | Block to opt out of Apple training (does NOT block Apple Search) |
| `Bytespider` | TikTok / ByteDance crawler | Decide per policy |
| `cohere-ai` | Cohere training | Block to opt out of Cohere |
| `omgilibot` / `omgili` | Webz.io aggregation | Decide per policy |

## Decision pattern: per-purpose, not per-vendor

The natural temptation is to think "do we want to be in ChatGPT?" or "do we want to be in Claude?" That framing leads to inconsistent decisions.

Better framing: **decide per purpose**.

| Purpose | Recommended access | Why |
|---|---|---|
| Search / attribution (drives referral traffic) | **Allow** all search bots | Free traffic. Same logic as allowing Googlebot. |
| User-triggered browsing | **Allow** | User-initiated, no systematic data extraction |
| Training data collection | **Decide per opt-out policy** | This is where the real choice lives |
| Generic / unattributed | **Block** typically | Low value, unclear policy |

## Sample robots.txt patterns

### Pattern A: Allow search, block training (most common)

```
# Allow search / attribution agents
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Perplexity-User
Allow: /

# Block training crawlers
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: CCBot
Disallow: /

# Default
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### Pattern B: Allow everything (broadest exposure)

```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Choose this only if you're comfortable with any LLM training on your content.

### Pattern C: Block AI entirely (rare; usually only for paywalled / sensitive content)

```
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: Claude-SearchBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Meta-ExternalAgent
User-agent: Applebot-Extended
User-agent: CCBot
Disallow: /

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Note: this does NOT block normal Google Search (Googlebot) or Bing Search (Bingbot).

## Consistency with llms.txt

Every URL listed in your llms.txt MUST be accessible to the AI user-agents you've allowed. Inconsistency creates a "treasure map that leads to locked doors."

Verification check:

```bash
# Pick 5 sample URLs from llms.txt
URLS=$(grep -oE 'https?://[^)`'"'"'"<>{}[:space:]]+' llms.txt | head -5)

# Check robots.txt accessibility for each
for url in $URLS; do
    PATH=$(echo "$url" | sed 's|^https\?://[^/]*||')
    echo "URL: $url"
    echo "Path: $PATH"
    # Manual check: is $PATH blocked for any AI bot you want to allow?
done
```

## Future: IETF AIPREF

The [IETF AIPREF working group](https://datatracker.ietf.org/wg/aipref/about/) is developing a more granular preference vocabulary that distinguishes purposes (train / search / RAG / summarize) and may eventually subsume the current per-user-agent approach.

When AIPREF ratifies and providers commit, expect to declare:
- `train`: allow / disallow
- `search`: allow / disallow
- `rag`: allow / disallow
- `summarize`: allow / disallow

Per purpose, not per vendor. This is the direction.

## How to detect new AI bots

Server log monitoring catches new bots. Look for:
- Unusual user-agent strings matching `*Bot`, `*-AI`, `*-User`, `*GPT*`, `*Claude*`, etc.
- Datacenter IP ranges (cloud providers) with elevated request rates
- High concurrency from a small number of source ASNs

When a new bot appears in logs:
1. Check its documentation if published
2. Decide per purpose (training? search? user-triggered?)
3. Update robots.txt
4. Update this reference

## Cross-references

- For robots.txt consistency check with llms.txt → `../knowledge/06-deployment.md`
- For decision framework on access → `../knowledge/03-seo-perspective.md`
- For training opt-out signal patterns → `../knowledge/03-seo-perspective.md` (Google-Extended discussion)
