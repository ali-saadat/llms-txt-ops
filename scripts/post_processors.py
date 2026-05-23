#!/usr/bin/env python3
"""Deterministic post-processors for generated llms.txt content.

Applied AFTER the LLM produces the file. Catches the deterministic-rule
violations that prompt engineering can't reliably prevent:

  - Process scaffolding leaks (headings like "## Step 3", "## Pass 1")
  - Emoji leaks (when no-emoji is the house style)
  - Non-ISO date formats in file metadata
  - Multiple H1s (spec violation)
  - Placeholder values (`<pending>`, `<TBD>`, `SHA-256: <...>`)
  - Domain inconsistency (URL typos like `testmarketmarket.local`)

Each post-processor is a pure function: `str -> str`. Composable via `apply_all()`.

These run after the LLM output and BEFORE the user sees the file. They are
the deterministic counterpart to the LLM's stochastic generation — together
they form the production quality pipeline.

References:
  - Self-Refine pattern: Madaan et al. 2023 (https://selfrefine.info)
  - The pattern of deterministic post-processing on LLM output is standard
    in production agent stacks (e.g., Anthropic's claude-for-legal applies
    similar deterministic filters before showing legal drafts to users).
"""

from __future__ import annotations

import re
from typing import Callable


# Standard emoji ranges (covers most modern emoji + symbols often misused)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F700-\U0001F77F"  # alchemical
    "\U0001F780-\U0001F7FF"  # geometric extended
    "\U0001F800-\U0001F8FF"  # supplemental arrows
    "\U0001F900-\U0001F9FF"  # supplemental symbols + pictographs
    "\U0001FA00-\U0001FA6F"  # chess + symbols
    "\U0001FA70-\U0001FAFF"  # symbols extended
    "☀-⛿"          # misc symbols
    "✀-➿"          # dingbats
    "⬀-⯿"          # arrows
    "⏩-⏳"          # control symbols
    "⏸-⏺"          # control symbols
    "■-◿"          # geometric shapes
    "✅"                 # white check mark
    "⚠-⚡"          # warning + lightning
    "✨"                 # sparkles
    "]+",
    flags=re.UNICODE,
)


# Lines that look like leaked process scaffolding from the generate skill's
# Step 3 (inventory) or Step 5 (validation) — these should never appear in
# the final file.
SCAFFOLDING_HEADING_PATTERN = re.compile(
    r"^##\s*(Step\s*\d|Pass\s*\d|URL\s*Inventory|Section\s*Outline|"
    r"Quality\s*Self.?Audit|Validation\s*Checklist|Completeness\s*Check|"
    r"Internal\s*Inventory)\b.*$",
    flags=re.IGNORECASE | re.MULTILINE,
)


# Placeholder patterns that should never ship
PLACEHOLDER_PATTERNS = [
    re.compile(r"^.*<pending>.*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*<TBD>.*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*<REVIEW>.*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*\[insert\b.*\].*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*SHA-?256:\s*<[^>]+>.*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^.*TODO:.*$", re.MULTILINE),
]


# Non-ISO date patterns (quarter abbreviations etc.) on metadata lines
NON_ISO_DATE_PATTERN = re.compile(
    r"(Last\s+reviewed[:\s]+)(20\d{2}\s*[-\s]\s*Q[1-4]|"
    r"20\d{2}\s*[-\s]\s*[A-Za-z]+(?:\s+\d{4})?)",
    flags=re.IGNORECASE,
)


# -----------------------------------------------------------------------
# Individual post-processors
# -----------------------------------------------------------------------


def strip_emojis(text: str) -> str:
    """Remove emojis from the text. Leaves leading/trailing whitespace tidy."""
    cleaned = EMOJI_PATTERN.sub("", text)
    # Tidy up "  - foo" → "- foo" (where the emoji was leading)
    cleaned = re.sub(r"^[ \t]+([-*+•])", r"\1", cleaned, flags=re.MULTILINE)
    # Collapse double spaces left by emoji removal
    cleaned = re.sub(r"  +", " ", cleaned)
    return cleaned


def strip_scaffolding_headings(text: str) -> str:
    """Remove H2 sections that look like leaked process scaffolding.

    Drops both the heading AND the body up to the next H2 (or EOF).
    """
    lines = text.split("\n")
    out = []
    skip = False
    for line in lines:
        if SCAFFOLDING_HEADING_PATTERN.match(line):
            skip = True
            continue
        if skip and line.startswith("## ") and not SCAFFOLDING_HEADING_PATTERN.match(line):
            skip = False
            out.append(line)
        elif not skip:
            out.append(line)
    return "\n".join(out)


def strip_placeholders(text: str) -> str:
    """Remove lines containing placeholder values like <pending> or <TBD>."""
    for pattern in PLACEHOLDER_PATTERNS:
        text = pattern.sub("", text)
    # Clean up triple newlines from removed lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def enforce_iso_dates(text: str, default_date: str | None = None) -> str:
    """Replace quarter-format dates ('2025-Q3') with ISO 8601 if a default is
    provided; otherwise remove the metadata line entirely (placeholder rule).
    """
    if default_date:
        # Use \g<1> backref form to be unambiguous when followed by digits
        # (raw r"\1..." can be misread as \12 backref in Python re)
        return NON_ISO_DATE_PATTERN.sub(rf"\g<1>{default_date}", text)
    # Otherwise: strip the line containing the non-ISO date
    lines = text.split("\n")
    return "\n".join(line for line in lines if not NON_ISO_DATE_PATTERN.search(line))


def enforce_single_h1(text: str) -> str:
    """If multiple H1s exist, keep the first one and demote the rest to H2."""
    h1_count = 0
    lines = text.split("\n")
    out = []
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            h1_count += 1
            if h1_count > 1:
                # Demote to H2
                out.append("## " + line[2:])
                continue
        out.append(line)
    return "\n".join(out)


def normalize_whitespace(text: str) -> str:
    """Collapse triple+ newlines to double, strip trailing whitespace on lines."""
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def validate_domains(
    text: str, allowed_domains: list[str], typo_threshold: float = 0.75
) -> tuple[str, list[str]]:
    """Scan for URL typos against an allowlist. Returns (text, list_of_typos_found).

    Uses difflib similarity to distinguish "this looks like a typo of an
    allowed domain" (e.g., `testmarketmarket.local` vs `testmarketplace.local`)
    from "this is a legitimate unrelated external domain" (e.g., sister-brand
    URLs at completely different hostnames).

    Only flags domains that are >= typo_threshold similar to an allowed
    domain. Default 0.75 catches most typos while ignoring external brands.
    """
    if not allowed_domains:
        return text, []
    import difflib

    pattern = re.compile(r"https?://([^/\s)\]]+)")
    domains_in_text = set(pattern.findall(text))
    allowed = set(allowed_domains)
    candidates = domains_in_text - allowed

    typos = []
    for d in sorted(candidates):
        # If it's close to an allowed domain, it's likely a typo
        matches = difflib.get_close_matches(d, list(allowed), n=1, cutoff=typo_threshold)
        if matches:
            typos.append(d)
        # Otherwise it's a legitimate external URL (sister brand, sitemap CDN, etc.)
    return text, typos


def strip_url_less_brand_bullets(text: str) -> str:
    """Bullets in the Sister Brands / International section that lack a URL
    are usually low-signal — convert to a single sentence or remove.

    Heuristic: lines starting with `- ` and containing brand-keyword + region
    but NO `http`. We keep them but warn.
    """
    # This is a soft post-processor — we just normalize formatting
    # to avoid stripping legitimate content. No change here yet; placeholder
    # for future logic.
    return text


# -----------------------------------------------------------------------
# Orchestrator
# -----------------------------------------------------------------------


def apply_all(
    text: str,
    iso_date: str | None = None,
    allowed_domains: list[str] | None = None,
    strip_emojis_flag: bool = True,
) -> tuple[str, dict[str, object]]:
    """Apply the full post-processing pipeline.

    Returns (cleaned_text, audit_report) where audit_report is a dict of
    per-stage findings (e.g., emojis_removed, scaffolding_headings_dropped,
    domain_typos_found).
    """
    report: dict[str, object] = {}

    if strip_emojis_flag:
        before = len(EMOJI_PATTERN.findall(text))
        text = strip_emojis(text)
        report["emojis_removed"] = before

    before_lines = text.count("\n")
    text = strip_scaffolding_headings(text)
    text = strip_placeholders(text)
    report["lines_removed_by_scaffolding_or_placeholder"] = before_lines - text.count("\n")

    text = enforce_iso_dates(text, iso_date)
    text = enforce_single_h1(text)
    text = normalize_whitespace(text)

    if allowed_domains:
        text, typos = validate_domains(text, allowed_domains)
        report["domain_typos"] = typos

    return text, report


# -----------------------------------------------------------------------
# CLI for ad-hoc usage
# -----------------------------------------------------------------------


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    p = argparse.ArgumentParser(description="Apply deterministic post-processors to an llms.txt draft.")
    p.add_argument("input", help="Path to draft file (or - for stdin)")
    p.add_argument("--output", "-o", help="Output path (default: stdout)")
    p.add_argument("--iso-date", help="Date to use for `Last reviewed:` fields")
    p.add_argument("--domain", action="append", help="Allowed domain (repeat for multiple)")
    p.add_argument("--no-strip-emoji", action="store_true", help="Don't strip emojis")
    p.add_argument("--audit", action="store_true", help="Print audit report to stderr as JSON")
    args = p.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8")

    cleaned, report = apply_all(
        text,
        iso_date=args.iso_date,
        allowed_domains=args.domain,
        strip_emojis_flag=not args.no_strip_emoji,
    )

    if args.audit:
        print(json.dumps(report, indent=2), file=sys.stderr)

    if args.output:
        Path(args.output).write_text(cleaned, encoding="utf-8")
        print(f"Wrote {len(cleaned):,} chars to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(cleaned)
