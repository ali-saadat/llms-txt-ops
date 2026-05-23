# Anti-Pattern Detection Logic

*Detailed detection logic for each of the 15 anti-patterns from `../../../knowledge/07-failure-modes.md`. Load when running an audit and a specific anti-pattern needs detailed checking.*

## #1 — Bloated enumeration

**Detection**:
- File size > 50 KB AND link count > 1000 → 🔴 Critical
- File size > 200 KB regardless → 🔴 Critical
- Single category with > 500 enumerated items → 🟠 High

**Diagnostic queries**:
```bash
# Size check
wc -c llms.txt

# Link count
grep -oE 'https?://[^)`<>{}[:space:]]+' llms.txt | wc -l

# Per-category distribution
awk '/^## / {section=$0; count=0} /^- \[/ {count++} END {print section, count}' llms.txt
```

**Fix path**: Apply URL pattern technique. List top 10-12 entries, declare pattern for the long tail. See ExampleMart case (12.5 MB → 27.8 KB).

## #2 — robots.txt confusion

**Detection**:
- File contains `User-agent:` lines → 🔴 Critical (this is robots.txt syntax, not llms.txt)
- File contains `Disallow:` or `Allow:` directives → 🔴 Critical

**Diagnostic**:
```bash
grep -E "^(User-agent|Disallow|Allow):" llms.txt
# Should return zero matches
```

**Fix**: Remove all robots.txt-style directives. Move access control to `robots.txt`. llms.txt is opt-IN curation only.

## #3 — Marketing-speak descriptions

**Detection** (keyword presence in link descriptions):
- "revolutionize", "revolutionary"
- "cutting-edge", "bleeding-edge"
- "industry-leading", "world-class", "best-in-class"
- "empowering", "transform", "unlock potential"
- "seamless", "effortless"
- "[CTA-style verbs] your business"

```bash
grep -ciE "revolutionize|cutting-edge|industry-leading|empowering|world-class|best-in-class|seamless|effortless" llms.txt
```

**Severity**: 🟠 High if >5 instances; 🟡 Medium if 2-5; ignore for 1.

**Fix**: Rewrite as concrete "what's on the page" descriptions. See `../../../knowledge/05-implementation.md` description-writing rules.

## #4 — Listing everything

**Detection**:
- Link count > 200 without clear URL-pattern structure → 🟠 High
- Multiple sections with > 50 links each → 🟠 High
- No `## Optional` section despite link count > 50 → 🟡 Medium

**Fix**: Apply ruthless curation criteria. Use `## Optional` for borderline inclusions.

## #5 — Legal document mode

**Detection** (legalese in file content):
- "DMCA", "copyright infringement", "all rights reserved"
- "patent pending", "trademark"
- Multi-paragraph EULA-style language
- "by accessing this file you agree"

**Fix**: Move legalese to dedicated pages (`/terms`, `/privacy`). Reference from llms.txt as content links, not embedded legalese.

## #6 — Cloaking-style description mismatch

**Detection** (manual sample):
- Pick 5 random URLs from the file
- Visit each page
- Compare description in llms.txt to actual page content
- Flag any mismatch

**Severity**: 🔴 Critical if any major mismatch (description promises detail that doesn't exist). Could trigger cloaking penalty if Google ever enforces parity.

**Fix**: Audit all descriptions. Rewrite to match actual page content.

## #7 — Broken URLs

**Detection**: Run link-check from `../../../templates/validate.sh`.
- HEAD request to each URL with 10s timeout
- 4xx response → 🔴 Critical
- 5xx response → 🟠 High (could be transient)
- Timeout / 0 → 🟠 High
- 301 → 2xx → 🟢 OK
- Long redirect chain (3+) → 🟡 Medium

**Fix**: Update or remove broken URLs. Re-test before deploy.

## #8 — Forgetting to regenerate

**Detection**:
- `Last reviewed` metadata in file > 6 months old → 🟡 Medium
- `Last reviewed` > 12 months old → 🟠 High
- No metadata block at all → 🟡 Medium

**Fix**: Add metadata block. Set calendar reminder for quarterly review.

## #9 — Stale CDN

**Detection**:
```bash
LOCAL_HASH=$(shasum -a 256 source/llms.txt | awk '{print $1}')
LIVE_HASH=$(curl -s https://domain/llms.txt | shasum -a 256 | awk '{print $1}')
[ "$LOCAL_HASH" = "$LIVE_HASH" ] && echo "OK" || echo "MISMATCH"
```

**Severity**: 🔴 Critical if mismatch.

**Fix**: Purge CDN cache. Add purge to deploy pipeline.

## #10 — Encoding errors

**Detection**:
```bash
# File-level
file -bi llms.txt | grep -q "charset=utf-8" || echo "NOT UTF-8"

# BOM check
head -c 3 llms.txt | xxd | head -1 | grep -q "efbbbf" && echo "BOM PRESENT"

# Wire-level
curl -I https://domain/llms.txt | grep -i content-type | grep -q "charset=utf-8" || echo "NO CHARSET"
```

**Severity**: 🔴 Critical if file is not UTF-8 or if served without charset.

**Fix**: Re-save as UTF-8 without BOM. Set Nginx `default_type "text/markdown; charset=utf-8"`.

## #11 — Indexable

**Detection**:
```bash
curl -I https://domain/llms.txt | grep -i x-robots-tag | grep -q noindex || echo "NOT NOINDEX"
```

Also: site:domain.com /llms.txt — does it show in Google results?

**Severity**: 🟡 Medium.

**Fix**: Add `X-Robots-Tag: noindex` header. Don't also `Disallow:` in robots.txt.

## #12 — No CI validation

**Detection**: ask the user (can't auto-detect from file).

**Fix**: Wire `../../../templates/validate.sh` into CI pipeline.

## #13 — Unfiltered auto-generation

**Detection signal**:
- Has vendor / product URLs enumerated → 🔴 Critical (auto-gen against sitemap)
- All links lead to leaf pages, no hub pages → 🟠 High
- Faceted URLs with query strings → 🟠 High
- Pagination URLs (page=2, page=3) → 🟡 Medium

**Fix**: Hybrid generation — hand-curate the high-signal sections, auto-fetch the URL list, manually filter.

## #14 — Vendor lock

**Detection**: ask the user.

**Fix**: Periodic backup to repo. If migrating platforms, you have a baseline.

## #15 — Over-promising

**Detection**: ask the user about their stakeholder framing.

**Severity**: 🟠 High if user pitches as "AI traffic lever"; 🟢 OK if user has set realistic expectations.

**Fix**: Reframe with the three defensible reasons. See `../../../stakeholder/expectations.md`.

## Composite severity logic

For the overall audit report:

- 1+ 🔴 Critical → Overall: 🔴 Critical
- 0 Critical + 3+ 🟠 High → Overall: 🟠 High
- 0 Critical + 1-2 🟠 High → Overall: 🟡 Medium
- 0 Critical + 0 High → Overall: 🟢 Healthy

## Cross-references

- `../SKILL.md` Step 3 (Run the checks)
- `../../../knowledge/07-failure-modes.md` — full anti-pattern descriptions
- `../../../templates/validate.sh` — automated checks
- `seo-layer-checks.md` — sibling reference for SEO integration layer checks
