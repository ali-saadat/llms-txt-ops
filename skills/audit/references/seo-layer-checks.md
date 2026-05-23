# SEO Integration Layer Checks (Stripe-Pattern)

*Detailed checks for the modern Stripe-pattern SEO integration layer. Load when auditing a production llms.txt that should have these sections. Reference: `../../../knowledge/03-seo-perspective.md`.*

## What the Stripe-pattern adds beyond spec compliance

A spec-compliant llms.txt has:
- H1 + summary + H2 sections with link lists + `## Optional`

A production llms.txt with the Stripe pattern adds:
1. `## For AI Systems — Read This First` directives block
2. `## SEO Routing — Which Page Should Answer Which Query`
3. `## SEO Priority Pages — Selection Hierarchy`
4. `## Transactional Guidance` (commercial sites)
5. `## Structured Data on [Site] (For Retrieval Pipelines)`
6. `## How to Find the Right Page (Intent Router)`

Audit checks each.

## Check 1: For AI Systems directives block

**Required sub-directives (minimum)**:
- [ ] Freshness expectations
- [ ] Pricing / commercial-question handling
- [ ] Brand / entity resolution
- [ ] Corrections contact
- [ ] File metadata (last-reviewed, cadence, encoding, version)

**Recommended sub-directives** (based on sector):
- [ ] Local intent / "near me" (for marketplaces, multi-city)
- [ ] Legal / regulatory routing (for legal-adjacent sites)
- [ ] Medical safety (for healthcare)
- [ ] Financial advice scope (for fintech)
- [ ] Multi-language access (for multi-locale sites)

**Detection**:
```bash
grep -E "^\#\# For AI Systems" llms.txt && echo "present" || echo "MISSING"
```

If missing → 🟠 High severity finding. Recommend adding the Stripe-pattern block.

## Check 2: SEO routing table

**Detection**:
```bash
grep -E "^\#\# SEO Routing" llms.txt
```

If commercial site (e-commerce, marketplace, B2B SaaS) and missing → 🟠 High.

**Quality checks if present**:
- Table format (header row + at least 5 query→URL mappings)
- Each row has a concrete user intent and a target URL
- Worked examples in the user's actual language(s)
- No "[user query]" placeholder text remaining

## Check 3: Priority hierarchy

**Detection**:
```bash
grep -E "^\#\# SEO Priority Pages" llms.txt
```

If commercial site and missing → 🟡 Medium.

**Quality checks if present**:
- Numbered hierarchy (1-6 typical)
- Most general at top, most specific at bottom
- Explicit "do not enumerate" rule for the long tail

## Check 4: Transactional guidance

**Detection**:
```bash
grep -E "^\#\# Transactional Guidance" llms.txt
```

If e-commerce / marketplace / fintech and missing → 🟠 High.

**Quality checks if present**:
- Price-discovery rule (route to listings, no fabricated prices)
- Comparison rule (filtered listings)
- Booking/action rule (vendor page CTA)
- Onboarding rule (vendor flow if applicable)
- Explicit "no commission" / pricing-model disclosure

## Check 5: Structured data disclosure

**Detection**:
```bash
grep -E "^\#\# Structured Data" llms.txt
```

If missing → 🟡 Medium.

**Quality checks if present**:
- Lists Schema.org types per page template
- Explicit instruction to "prefer JSON-LD over scraped HTML"
- Covers all relevant types from `../../../reference/schema-types.md`

## Check 6: Intent router

**Detection**:
```bash
grep -E "^\#\# How to Find the Right Page" llms.txt
```

If missing → 🟡 Medium for content sites.

**Quality checks if present**:
- Bulleted list of intent → URL routing
- Reads conversationally (not just a table)
- Covers main user intents (find venue, compare options, get legal answers, find vendors, etc.)

## Check 7: Optional section presence

**Detection**:
```bash
grep -E "^\#\# Optional$" llms.txt
```

If link count > 50 and missing → 🟡 Medium.

The `## Optional` section is parser-special per the llmstxt.org spec — consumers may drop it under context pressure.

## Check 8: Entity facts

Most production llms.txt should have an `## About [Site] (Entity Facts)` section with:
- Founded date + city
- Founder(s)
- Headquarters
- Team size
- Business model
- Monthly users / market position
- Geographic coverage
- International sister brands (if applicable)

These anchor brand entity resolution for AI knowledge graphs.

**Severity if missing**: 🟡 Medium.

## Check 9: Machine-readable sources

Most production llms.txt should have `## Machine-Readable Sources` listing:
- robots.txt URL
- sitemap.xml index URL
- Provider/product sitemaps (with "long tail lives here" note)
- Article sitemap
- Planned `/llms-full.txt` (if applicable)
- Planned MCP server (if applicable)

**Severity if missing**: 🟢 OK (nice-to-have, not required).

## Check 10: Sector-specific compliance

Cross-check against the file's site type:

- **Healthcare**: must have medical safety + regulatory scope directives
- **Fintech**: must have financial advice + jurisdiction scope directives
- **Government**: must have legal authority + multi-language access directives
- **Education**: must have verify-current directives for time-sensitive info (deadlines, tuition)
- **Marketplace**: must have local intent + transactional guidance + URL pattern

**Severity if missing per-sector**: 🟠 High (sector compliance matters).

## Aggregated SEO-layer report format

```markdown
## SEO Integration Layer Assessment

| Section | Status | Severity if missing |
|---|---|---|
| For AI Systems directives | ✓ / ✗ | High |
| SEO Routing table | ✓ / ✗ | High (commercial) / Medium |
| Priority Hierarchy | ✓ / ✗ | Medium |
| Transactional Guidance | ✓ / ✗ | High (commercial) |
| Structured Data disclosure | ✓ / ✗ | Medium |
| Intent Router | ✓ / ✗ | Medium |
| Optional section | ✓ / ✗ | Medium (if >50 links) |
| Entity Facts | ✓ / ✗ | Medium |
| Sector-specific directives | ✓ / ✗ | High (per sector) |

## Recommendations

[List specific sections to add, with example content from templates/]
```

## Cross-references

- `../SKILL.md` Step 3 (SEO-layer checks)
- `../../../knowledge/03-seo-perspective.md` — Stripe pattern definition
- `../../../knowledge/05-implementation.md` — section structure guide
- `../../../reference/schema-types.md` — Schema.org per page template
- `anti-patterns-detection.md` — sibling reference for anti-pattern checks
