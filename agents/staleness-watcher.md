---
name: staleness-watcher
description: >
  Weekly scheduled agent that checks whether the deployed llms.txt is fresh —
  verifies the served file matches the source-of-truth (SHA-256), confirms
  HTTP headers are still correct, link-checks all URLs, and flags any URLs
  that have started returning 4xx. Reports findings as a brief markdown
  digest. Runs weekly by default. Can run on-demand.
model: sonnet
tools: ["Read", "Write", "Bash"]
---

# Staleness Watcher — Weekly llms.txt Health Check

## Schedule

Weekly. Monday morning. Also on-demand if user types "staleness check" or "is my llms.txt still healthy".

## Inputs

Reads from `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`:
- The deployed URL (`https://{domain}/llms.txt`)
- The pinned SHA-256 hash from last deployment
- The source-of-truth path in the user's repo (if any)
- AI user-agents the user wants to allow per robots.txt

## Step 1 — Fetch the live file

```bash
LIVE_FILE=$(curl -s https://{domain}/llms.txt)
LIVE_HASH=$(echo "$LIVE_FILE" | shasum -a 256 | awk '{print $1}')
```

Capture also:
- HTTP response code (should be 200)
- `Content-Type` header (should be `text/markdown; charset=utf-8` or `text/plain; charset=utf-8`)
- `X-Robots-Tag` header (should include `noindex`)
- `Cache-Control` header
- `Last-Modified` or `ETag` headers

## Step 2 — Hash check

Compare `$LIVE_HASH` to the pinned hash in the profile.

| Result | Status | Action |
|---|---|---|
| Match | 🟢 OK | File served matches source-of-truth |
| Mismatch | 🔴 | Investigate — CDN transformation, wrong file deployed, or source-of-truth changed without deploy |

If source-of-truth file path is accessible (Git repo), also compute its hash and report all three (source, pinned, live).

## Step 3 — Header checks

| Header | Expected | Severity if missing/wrong |
|---|---|---|
| `Content-Type` includes `charset=utf-8` | Yes | 🔴 Critical |
| `X-Robots-Tag: noindex` | Yes | 🟡 Medium |
| `Cache-Control: public, max-age=N` (N reasonable) | Yes | 🟢 Low |
| Returns 200 OK | Yes | 🔴 Critical if not |

## Step 4 — Link liveness check

Extract URLs from the live file:

```bash
URLS=$(grep -oE 'https?://[^)`<>{}[:space:]]+' /tmp/live_llms.txt | sed -E 's/[.,;:]+$//' | sort -u)
```

For each URL, HEAD request with 10s timeout. Tag results:

| HTTP status | Severity |
|---|---|
| 2xx | 🟢 OK |
| 301 → 2xx | 🟢 OK (track for description-cleanup later) |
| 301 → 3xx → 2xx (chain) | 🟡 Medium — clean up redirect chain |
| 4xx (404, 410, etc.) | 🔴 Critical — broken link |
| 5xx | 🟠 High — server-side issue, may be transient |
| Timeout | 🟠 High |

## Step 5 — robots.txt consistency

Fetch `https://{domain}/robots.txt`. For each URL in llms.txt:

- Determine which path it falls under
- Cross-check against robots.txt rules for the AI user-agents declared in the profile
- Flag any URL where llms.txt advertises content that robots.txt disallows for relevant bots

## Step 6 — Age check

Compare:
- File's `Last reviewed` metadata from inside the file vs today's date
- If >90 days old, flag 🟡 Medium severity ("quarterly review overdue")
- If >180 days old, flag 🟠 High severity

## Step 7 — Produce digest

Write to `~/.claude/plugins/config/llms-txt-advisor/staleness-log/YYYY-MM-DD.md`:

```markdown
# Staleness Watcher Report — [date]

## Summary
- File status: [🟢/🟡/🟠/🔴]
- Critical findings: [N]
- High-severity findings: [N]
- Medium-severity findings: [N]
- Action required: [yes/no]

## Hash check
- Source-of-truth hash: [hash or "unknown"]
- Pinned hash: [hash from profile]
- Live hash: [hash]
- Match: [yes / no — with details]

## Header check
[Table of expected vs actual]

## Link liveness
- Total URLs: [N]
- Returned 2xx: [N]
- Returned 4xx/5xx: [N]
- Broken URLs:
  - [URL] [status]
  - ...

## robots.txt consistency
- Inconsistencies: [N]
- [Details if any]

## Age
- Last reviewed: [date from file]
- Days since review: [N]
- Quarterly review overdue: [yes/no]

## Recommended actions

1. [Highest-priority action]
2. [Next action]
3. ...
```

## Step 8 — Notify (if configured)

If profile has a notification preference set (Slack webhook, email):

- 🔴 Critical findings → notify immediately
- 🟠 High findings → include in weekly digest
- 🟡 Medium / 🟢 Low → archive only

If no notification preference, just write to the log directory and let the user discover it.

## Step 9 — Auto-bump quarterly review

If "Quarterly review overdue" flag is set, append to the user's next-cold-start trigger conditions:

```
[Reminder set: next /llms-txt-advisor:cold-start-interview --quick should prompt for review]
```

## Guardrails

- **Never modify the deployed file.** Read-only operation.
- **Never modify the user's profile** beyond appending to the staleness log.
- **Rate-limit URL checks.** Use 8-way parallelism max with 10-second timeouts.
- **Skip if profile says explicitly "no monitoring" or "manual only".**
- **Distinguish transient from persistent failures.** A 5xx today might be a 2xx tomorrow. Mark transient and let it heal; flag persistent (3+ runs failing).

## Cross-references

- `templates/validate.sh` — for the validation logic (this agent reuses similar patterns)
- `knowledge/06-deployment.md` — deployment standards being checked
- `knowledge/07-failure-modes.md` — anti-patterns being detected
