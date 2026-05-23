---
title: Post-Processors
tags:
  - quality
  - deterministic
aliases:
  - post_processors.py
  - deterministic fixes
created: 2026-05-23
updated: 2026-05-23
---

# Post-Processors

> [!info] Stage 4 of [[Quality Refinement Pipeline]]
> Deterministic fixes for things prompt engineering can't reliably prevent. Pure functions: `str -> str`. Composable.

## What each processor does

| Processor | Why it exists |
|---|---|
| `strip_emojis` | LLM occasionally leaks ⚠️ ✅ etc. into prose despite "no emojis" rule |
| `strip_scaffolding_headings` | Catches `## Step 3 — URL Inventory` if [[generate]]'s OUTPUT BOUNDARY rule fails |
| `strip_placeholders` | Removes lines with `<pending>`, `<TBD>`, `<REVIEW>`, `[insert...]`, `SHA-256: <...>` |
| `enforce_iso_dates` | Replaces `2025-Q3` style with ISO 8601 (`2026-05-23`) |
| `enforce_single_h1` | Spec violation — demotes extra H1s to H2 |
| `validate_domains` (Levenshtein) | Flags `testmarketmarket.local` (typo) vs `www.weddinghero.com.au` (legitimate external) |
| `normalize_whitespace` | Collapses triple newlines, strips trailing whitespace |

## The Levenshtein insight

Naive domain allowlist would flag ALL non-allowed domains as "typos" — but sister-brand URLs are legitimately external. Using `difflib.get_close_matches(cutoff=0.75)` distinguishes "this looks like a typo of an allowed domain" from "this is a different domain entirely".

```python
allowed = ['example.com', 'api.example.com']
'testmarketmarket.local' similar to 'example.com'? NO    # not flagged
'examplexample.com' similar to 'example.com'?      YES   # flagged
'www.sister-brand.com' similar to anything?         NO    # not flagged (legitimate)
```

## Usage

```bash
python3 scripts/post_processors.py draft.md \
    --iso-date 2026-05-23 \
    --domain yoursite.com --domain api.yoursite.com \
    --audit \
    --output cleaned.md
```

Returns: cleaned text + a JSON audit report (emojis removed, lines removed, domain typos).

## Source

- `../scripts/post_processors.py`
- `../knowledge/09-quality-refinement.md` § Stage 4

## Related

- [[Quality Refinement Pipeline]]
- [[Self-Refine]] — Stage 3 (what runs before this)
- [[LLM Judge]] — Stage 5 (what runs after this)
