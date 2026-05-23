---
name: audit
description: >
  Review an existing llms.txt file against best practices, spec compliance, and
  anti-patterns. Use when the user says "review my llms.txt", "audit our file",
  "what's wrong with my llms.txt", "check this llms.txt", "is our llms.txt
  any good", or shares an llms.txt URL or file path. Produces a structured
  report with severity-tagged findings and a recommended action list.
argument-hint: "[file path | URL | paste]"
---

# Audit — Review an Existing llms.txt

## Step 1 — Profile check

Same bounce-on-placeholder pattern as other skills. If `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` has placeholders, bounce to `/llms-txt-advisor:cold-start-interview` OR proceed in PROVISIONAL mode (tag every finding `[PROVISIONAL]`).

## Step 2 — Acquire the file

| Input | Action |
|---|---|
| URL | Fetch it. Check Content-Type header. Check size. |
| File path | Read it. |
| Pasted content | Use the pasted content directly. |
| No input — but profile has a domain | Try `https://{domain}/llms.txt`. |

Note the **served Content-Type header** — that's a real audit finding distinct from the file's internal encoding.

## Step 3 — Run the checks

Load `knowledge/07-failure-modes.md` for the full anti-pattern list. For each, check the audited file and report findings.

### Mechanical checks (run first)

1. **File size** — under 50 KB target? Under 200 KB hard limit?
2. **Encoding** — UTF-8 without BOM? Verify via byte-level inspection.
3. **Exactly one H1** — required by spec.
4. **`## Optional` section present and correctly named?** — case-sensitive per spec.
5. **All link URLs return 2xx** — run the link-check from `templates/validate.sh`.
6. **Served `Content-Type` header includes `charset=utf-8`** — if URL was provided.
7. **Served `X-Robots-Tag: noindex`** — if URL was provided.
8. **robots.txt consistency** — fetch the site's robots.txt and check that URLs in llms.txt are `Allow:` for AI user-agents declared in the user's profile.

### Anti-pattern checks (load `knowledge/07-failure-modes.md` for the full list)

For each of the 17 anti-patterns, check and tag:

| Anti-pattern | Detection signal |
|---|---|
| #1 Bloated enumeration | >50 KB AND >1000 links |
| #2 robots.txt confusion | `User-agent:` directives inside llms.txt |
| #3 Marketing-speak descriptions | grep for "revolutionize", "cutting-edge", "industry-leading", "empowering" |
| #4 Listing everything | >100 links without clear URL-pattern structure |
| #5 Legal document mode | grep for "DMCA", "all rights reserved", legalese |
| #6 Cloaking-style mismatch | Sample 5 random URLs; check description matches actual page |
| #7 Broken URLs | Link-check found any 4xx/5xx |
| #8 Forgetting to regenerate | Last-reviewed date >6 months old in metadata |
| #9 Stale CDN | Local file SHA-256 ≠ served URL SHA-256 |
| #10 Encoding errors | UTF-8 fail OR served without charset OR BOM present |
| #11 Indexable | No `X-Robots-Tag: noindex` on served file |
| #12 No CI validation | Ask user — can't detect from file |
| #13 Unfiltered auto-gen | Hub URLs missing; vendor/product URLs enumerated |
| #14 Vendor lock | Ask user — can't detect from file |
| #15 Over-promising | Ask user about stakeholder framing |
| #16 PII leakage | Phone-number / email / address regex hits inline next to vendor URLs (>10 hits = Critical) |
| #17 Non-markdown format | Magic-byte check: file starts with `{\rtf`, `<htm`, `<!DO`, `%PDF`; or `file` reports non-text |

### SEO-layer checks (Stripe-pattern modern best practices)

Load `knowledge/03-seo-perspective.md` and check presence of:

- [ ] `## For AI Systems — Read This First` directives block
- [ ] Local intent / "near me" directive
- [ ] `## SEO Routing — Which Page Should Answer Which Query` section
- [ ] `## SEO Priority Pages — Selection Hierarchy` section
- [ ] `## Transactional Guidance` section (if commercial site)
- [ ] `## Structured Data on [Site]` section
- [ ] Intent router (`## How to Find the Right Page`)
- [ ] Entity facts block
- [ ] File metadata block (last reviewed, cadence, version, encoding)

## Step 4 — Severity assignment

Use a canonical 4-level scale. Downstream actions inherit this severity floor — don't silently demote.

| Severity | Marker | Examples |
|---|---|---|
| Critical | 🔴 | Bloated enumeration; encoding broken; all URLs return 4xx; description-content mismatch (cloaking risk) |
| High | 🟠 | Marketing-speak descriptions throughout; no instructions block; robots.txt blocks URLs llms.txt advertises |
| Medium | 🟡 | Missing SEO routing layer; no last-reviewed metadata; over 50 KB but under 200 KB |
| Low | 🟢 | Could use more concrete descriptions; URL pattern not declared for long-tail |

## Step 5 — Produce the report

```markdown
# llms.txt Audit Report — [Site domain]

*Audited [date]. File at [URL or path], size [X KB], [N] links.*

## Critical findings (🔴)

[List with explanation and fix recommendation, citing knowledge files]

## High-severity findings (🟠)

[Same]

## Medium-severity findings (🟡)

[Same]

## Low-severity findings (🟢)

[Same]

## SEO integration layer assessment

[Stripe-pattern checklist with status per item]

## Recommended action

[Highest-impact 3-5 changes in priority order]

## How to act on this report

- Apply all critical and high-severity fixes → `/llms-txt-advisor:generate --from-audit`
- Update a specific section only → `/llms-txt-advisor:customize --section <name>`
- Deploy after fixes → `/llms-txt-advisor:deploy`
```

## Step 6 — Offer concrete next steps

> "Three options:
> 1. Apply all critical + high-severity fixes — I'll regenerate the file. → `/llms-txt-advisor:generate --from-audit`
> 2. Pick specific findings to fix — I'll customize section by section. → `/llms-txt-advisor:customize`
> 3. Just keep this report and act later — your call."

## Guardrails

- **No silent demotion** of severity. If a finding is 🔴 in audit, it stays 🔴 in downstream skills' priority lists.
- **Cite anti-pattern numbers** from `knowledge/07-failure-modes.md` for traceability.
- **Don't pretend issues are subjective** if they're spec violations. A file missing the H1 is broken, not a matter of taste.
- **Acknowledge what's working** — audits aren't only finding faults. Note what the file does well.

## Cross-references

- `knowledge/07-failure-modes.md` — all 15 anti-patterns with detection
- `knowledge/05-implementation.md` — what "good" looks like
- `knowledge/03-seo-perspective.md` — SEO integration layer checks
- `templates/validate.sh` — automated checks
- `case-study/example-marketplace-case.md` — the bloated-enumeration recovery example
