# 06 — Deployment and Operations

*Status: Compiled May 15, 2026. Production-grade deployment guidance for llms.txt — server config, CI validation, robots.txt consistency, monitoring.*

## Server configuration

### Nginx

The canonical pattern. Serves the file at `/llms.txt` with correct headers.

```nginx
location = /llms.txt {
    alias /var/www/example.com/llms.txt;

    # Encoding — addresses the most common operational mistake
    default_type "text/markdown; charset=utf-8";

    # Don't index in search — Mueller-confirmed appropriate (July 2025)
    add_header X-Robots-Tag "noindex" always;

    # 1-hour cache — purge on deploy
    add_header Cache-Control "public, max-age=3600" always;

    # Allow cross-origin if AI tools fetch from a different origin
    add_header Access-Control-Allow-Origin "*" always;
}
```

### Apache

```apache
<Files "llms.txt">
    ForceType "text/markdown; charset=utf-8"
    Header set X-Robots-Tag "noindex"
    Header set Cache-Control "public, max-age=3600"
    Header set Access-Control-Allow-Origin "*"
</Files>
```

### Caddy

```caddy
example.com {
    @llms_txt path /llms.txt
    handle @llms_txt {
        header Content-Type "text/markdown; charset=utf-8"
        header X-Robots-Tag "noindex"
        header Cache-Control "public, max-age=3600"
        file_server
    }
}
```

### Cloudflare Workers / Vercel / Netlify

For edge-deployed sites, set headers in the framework config:

**Next.js `next.config.js`**:
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/llms.txt',
        headers: [
          { key: 'Content-Type', value: 'text/markdown; charset=utf-8' },
          { key: 'X-Robots-Tag', value: 'noindex' },
          { key: 'Cache-Control', value: 'public, max-age=3600' },
        ],
      },
    ];
  },
};
```

**Vercel `vercel.json`**:
```json
{
  "headers": [
    {
      "source": "/llms.txt",
      "headers": [
        { "key": "Content-Type", "value": "text/markdown; charset=utf-8" },
        { "key": "X-Robots-Tag", "value": "noindex" },
        { "key": "Cache-Control", "value": "public, max-age=3600" }
      ]
    }
  ]
}
```

## The encoding mistake (and how to prevent it)

The most common operational mistake is serving the file with the wrong charset, leading to corrupted display of non-ASCII characters (Turkish ş ğ ı, Spanish ñ á é, Chinese, etc.).

### The three things to verify

1. **File is UTF-8 without BOM**. Verify:
   ```bash
   file -bi llms.txt
   # Expected: text/plain; charset=utf-8 (no "with-bom")

   head -c 3 llms.txt | xxd | head -1
   # If BOM present, first 3 bytes are: ef bb bf — should NOT be present
   ```

2. **Server sets `charset=utf-8` explicitly**. Verify:
   ```bash
   curl -I https://yoursite.com/llms.txt | grep -i content-type
   # Expected: Content-Type: text/markdown; charset=utf-8
   ```

3. **No intermediate transformation in CDN / proxy**. Some corporate proxies apply ASCII normalization. Test:
   ```bash
   # Compare local file hash to served file hash
   shasum -a 256 llms.txt
   curl -s https://yoursite.com/llms.txt | shasum -a 256
   # Hashes must match exactly
   ```

If hashes don't match, something in the transport pipeline is mutating the file. Investigate CDN, proxies, and any middleware.

## CI validation pipeline

Every deploy should run automated checks. Below is a complete validation script (also in `../templates/validate.sh`).

```bash
#!/usr/bin/env bash
# CI validation for llms.txt
set -euo pipefail

FILE="${1:-llms.txt}"
EXPECTED_HASH="${2:-}"  # Optional pinned hash

echo "Validating $FILE..."

# 1. File exists and is readable
[ -r "$FILE" ] || { echo "FAIL: cannot read $FILE"; exit 1; }

# 2. UTF-8 encoding (file utility, BSD or GNU)
ENC=$(file -bi "$FILE" | grep -oE 'charset=[a-zA-Z0-9-]+' || echo "")
if [[ "$ENC" != "charset=utf-8" && "$ENC" != "charset=us-ascii" ]]; then
    echo "FAIL: encoding is $ENC, expected utf-8"
    exit 1
fi

# 3. No BOM
BOM=$(head -c 3 "$FILE" | xxd -p)
if [[ "$BOM" == "efbbbf" ]]; then
    echo "FAIL: BOM detected at file start"
    exit 1
fi

# 4. Has exactly one H1
H1_COUNT=$(grep -c "^# " "$FILE" || true)
if [[ "$H1_COUNT" != "1" ]]; then
    echo "FAIL: expected 1 H1, found $H1_COUNT"
    exit 1
fi

# 5. Size budget (50 KB warning, 200 KB hard fail)
SIZE=$(wc -c < "$FILE")
if [[ "$SIZE" -gt 204800 ]]; then
    echo "FAIL: file size ${SIZE} bytes exceeds 200 KB hard limit"
    exit 1
fi
if [[ "$SIZE" -gt 51200 ]]; then
    echo "WARN: file size ${SIZE} bytes exceeds 50 KB target"
fi

# 6. All URLs return 2xx or 301→2xx (parallel curl with timeout)
echo "Checking URLs..."
BAD_URLS=$(grep -oE 'https://[^)]+' "$FILE" | sort -u | \
    xargs -P 8 -I {} sh -c 'CODE=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 "{}" || echo "000"); [ "${CODE:0:1}" != "2" ] && echo "{} [$CODE]"' || true)

if [[ -n "$BAD_URLS" ]]; then
    echo "FAIL: bad URLs found:"
    echo "$BAD_URLS"
    exit 1
fi

# 7. Optional: verify SHA-256 against pinned hash
if [[ -n "$EXPECTED_HASH" ]]; then
    ACTUAL_HASH=$(shasum -a 256 "$FILE" | awk '{print $1}')
    if [[ "$ACTUAL_HASH" != "$EXPECTED_HASH" ]]; then
        echo "FAIL: SHA-256 mismatch"
        echo "  Expected: $EXPECTED_HASH"
        echo "  Actual:   $ACTUAL_HASH"
        exit 1
    fi
fi

# 8. Optional: spec-shape parse via llms_txt2ctx if installed
if command -v llms_txt2ctx >/dev/null 2>&1; then
    llms_txt2ctx --check "$FILE" >/dev/null 2>&1 || {
        echo "WARN: llms_txt2ctx parse failed"
    }
fi

echo "PASS: $FILE validated ($SIZE bytes)"
```

### Post-deploy verification

After deployment, verify the live URL is byte-identical to the file you approved:

```bash
LOCAL_HASH=$(shasum -a 256 llms.txt | awk '{print $1}')
LIVE_HASH=$(curl -s https://yoursite.com/llms.txt | shasum -a 256 | awk '{print $1}')

if [[ "$LOCAL_HASH" != "$LIVE_HASH" ]]; then
    echo "FAIL: deployed file differs from source"
    exit 1
fi
```

This catches CDN transformations, proxy mutations, and accidental deploys of the wrong file.

## robots.txt consistency

Every URL listed in llms.txt must be accessible to the AI user-agents you want consuming it. Inconsistency creates a "treasure map that leads to locked doors."

### Verification rule

For each AI user-agent in your robots.txt, every URL in llms.txt must be `Allow:` (or at least not `Disallow:`).

### Decide access per-purpose, not per-vendor

Use the user-agent inventory in `../reference/ai-bots.md`. Common decision pattern:

| Purpose | User agents | Recommended access |
|---|---|---|
| Search / attribution (drives referrals) | `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot` | **Allow** |
| User-triggered browsing | `ChatGPT-User`, `Claude-User`, `Perplexity-User` | **Allow** |
| Training data collection | `GPTBot`, `ClaudeBot`, `Google-Extended`, `Meta-ExternalAgent` | **Block** if you don't want training; **Allow** if comfortable |
| Generic / unknown | `CCBot`, `AI2Bot` | **Block** typically |

Sample robots.txt for an llms.txt-bearing site that allows search but blocks training:

```
# Allow search and attribution agents
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Allow user-triggered browsing
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
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

# Default allow
User-agent: *
Allow: /

# Sitemap and llms.txt pointers
Sitemap: https://example.com/sitemap.xml
```

Note: the `Sitemap:` directive is standard. There is no equivalent `LLMs:` directive — the file is just expected to live at `/llms.txt`.

## Monitoring

### Server logs

Log every request to `/llms.txt` and `/llms-full.txt` with user-agent and timestamp.

```nginx
log_format llms_access '$remote_addr - [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_user_agent"';

location = /llms.txt {
    access_log /var/log/nginx/llms_access.log llms_access;
    # ... rest of config
}
```

### What to look for

| Pattern | Meaning | Action |
|---|---|---|
| Fetches dominated by `ChatGPT-User` | Users handing URLs to ChatGPT | Expected — file is being consumed at user-request time |
| Fetches dominated by training crawlers | Training data collection | Verify robots.txt access policy matches intent |
| Sudden drop to zero fetches | File or server broken | Run CI validation immediately |
| Massive spike from one IP | Scraper / abuse | Rate limit |
| Datacenter IPs (Google Cloud, OVH) hitting the file | Generic infrastructure scraping | Usually not real AI consumption |

### Realistic expectations

Per OtterlyAI's 90-day study: across multiple sites, 62,100 AI bot requests total → only 84 (0.1%) touched `/llms.txt`. Do NOT expect heavy consumption. Set monitoring alerts only for *unexpected drops* (could indicate file is broken), not for low traffic.

### Bing AI Performance setup

Higher-leverage than monitoring llms.txt itself. Set up [Bing AI Performance report](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview):

1. Verify site ownership in Bing Webmaster Tools
2. Wait 7+ days for data collection
3. Review citation counts, grounding queries, page-level breakdown
4. Use grounding queries to inform the SEO routing table in your llms.txt

This is the only first-party AI-citation telemetry currently available.

## Update cadence

| Trigger | Action |
|---|---|
| Major IA change (new category, removed category) | Update llms.txt within 1 week |
| New high-value editorial article | Add to Rehber Yazılar section within 1 week |
| Quarterly schedule | Full review: links still resolve, descriptions accurate, top-12 cities still right by GA traffic |
| AI provider commits to consuming llms.txt | Reassess scope and add provider-specific directives if relevant |

Set a calendar reminder for the quarterly review. Use the `file metadata` block in the file itself to track last-reviewed date.

## CDN considerations

### Cache invalidation on deploy

Every deploy must purge the CDN cache for `/llms.txt`. Stale-CDN-after-deploy is the single most common operational bug (per [Open Shadow's 2026 guide](https://www.openshadow.io/guides/llms-txt)).

For Cloudflare:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"files":["https://example.com/llms.txt","https://example.com/llms-full.txt"]}'
```

For Fastly: similar pattern via `purge` API.

For Vercel / Netlify: cache is tied to deploys; purges automatically.

### TTL choice

- `max-age=3600` (1 hour) — sensible default
- `max-age=86400` (24 hours) — if file rarely changes
- `max-age=0, must-revalidate` — only if you want every fetch to re-check (rare; expensive)

Don't set TTL longer than your typical update interval.

## Future: `/llms-full.txt`

For sites where llms.txt is succeeding, consider adding `/llms-full.txt` — concatenated full markdown of the highest-value pages.

**Scope**: 20–30 articles, ~30 hub descriptions. Auto-generated from canonical markdown sources. Same headers as llms.txt.

**Trigger to add**: when your llms.txt server logs show meaningful traffic (e.g., regular `ChatGPT-User` fetches with documented downstream conversions).

**Size**: typically 1–5 MB. Compress aggressively (gzip in transport).

Mintlify's data shows `llms-full.txt` gets 5–6× more AI bot fetches than `llms.txt` once published, so the value is real once you've earned the audience.

## Operational checklist for first deployment

- [ ] File generated and reviewed against `05-implementation.md` checklist
- [ ] Local CI validation passes (`templates/validate.sh`)
- [ ] SHA-256 hash recorded and pinned in deployment ticket
- [ ] Server config block added (Nginx / Apache / Caddy / Vercel / etc.)
- [ ] robots.txt updated for AI user-agent consistency
- [ ] CDN cache purge step added to deploy pipeline
- [ ] Post-deploy hash verification automated
- [ ] Server logs enabled for `/llms.txt` and `/llms-full.txt`
- [ ] Bing AI Performance monitoring set up (parallel investment, higher leverage)
- [ ] Calendar reminder set for quarterly review
- [ ] Internal documentation updated to reflect that llms.txt exists and what it covers

## Cross-references

- For validation script as standalone → `../templates/validate.sh`
- For Nginx config as standalone → `../templates/nginx-config.conf`
- For implementation guide → `05-implementation.md`
- For real deployment spec → `../case-study/deployment-spec.md`
- For AI bot inventory → `../reference/ai-bots.md`
