# Sector: Generic

*Use when the site doesn't fit cleanly into any specific sector, or when classification is uncertain.*

## Decision default

**Apply the universal decision framework from `../04-decision-framework.md`.** Without sector-specific context, fall back to the three defensible reasons:

1. Replacing a broken existing file (status quo improvement)
2. Internal grounding for the site's own AI work
3. Forward-compatibility insurance

If none of those apply, skip.

## Distinctive concerns

When classification is uncertain:

1. **Identify the primary consumer of the site's content** — devs? customers? students? general public?
2. **Identify the conversion / action moment** — purchase? signup? donate? read?
3. **Identify the IA backbone** — categorical (e-commerce style), hierarchical (docs style), temporal (publisher style), or flat (single-product)?

These three questions usually unlock a specific sector classification.

## When to actually use this file

- During cold-start interview before user has chosen a site type
- For PROVISIONAL mode when profile isn't configured
- For multi-purpose sites that legitimately span sectors
- For new sectors not yet covered by the specific files

## Recommended structure (defaults)

- Brand entity facts (always)
- Whatever-the-top-categories-are hubs (3-10)
- Contact / about / policies basic set
- Sitemap pointers
- Optional section

## Connector synergies

- `~~cms` — most sites have one; figure out which
- `~~analytics` — most sites have one
- Otherwise no strong prior

## Honest expectations

Default to null AI-citation lift. The user can override during cold-start if they have specific context.

## Template

Use `templates/llms-txt-generic.md`.

## Cross-references

- `../04-decision-framework.md`
- `_router.md` — sector classifier (try one more time)
