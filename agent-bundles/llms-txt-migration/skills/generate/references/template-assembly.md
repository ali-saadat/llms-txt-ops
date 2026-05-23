# Template Assembly Logic

*Detailed step-by-step logic for assembling an llms.txt from a template + profile. Load when running `/generate`.*

## Assembly pipeline

```
1. Read user's practice profile
   ↓
2. Select base template by site type
   ↓
3. Populate placeholders from profile fields
   ↓
4. Apply SEO integration layer (commercial sites)
   ↓
5. Apply sector-specific directives
   ↓
6. Apply language-specific tone (if non-English)
   ↓
7. Enforce size budget
   ↓
8. Validate spec shape
   ↓
9. Present + offer save
```

## Step 2: Template selection

| Profile site_type | Base template |
|---|---|
| `developer-documentation` | `templates/llms-txt-dev-docs.md` |
| `marketing-site` / `blog` | `templates/llms-txt-marketing.md` |
| `e-commerce` | `templates/llms-txt-ecommerce.md` |
| `marketplace` | `templates/llms-txt-ecommerce.md` (with marketplace adaptations) |
| `news-publisher` | `templates/llms-txt-marketing.md` (with publisher adaptations) |
| `education` | `templates/llms-txt-generic.md` (with education adaptations) |
| `healthcare` | `templates/llms-txt-generic.md` (with healthcare directives) |
| `fintech` (consumer) | `templates/llms-txt-marketing.md` |
| `fintech` (developer APIs) | `templates/llms-txt-dev-docs.md` |
| `government-civic` | `templates/llms-txt-generic.md` (with civic directives) |
| `b2b-saas` (docs subdomain) | `templates/llms-txt-dev-docs.md` |
| `b2b-saas` (marketing) | `templates/llms-txt-marketing.md` |
| `gaming` (modding APIs) | `templates/llms-txt-dev-docs.md` |
| `non-profit` | `templates/llms-txt-generic.md` |
| `media-entertainment` | `templates/llms-txt-marketing.md` |
| `generic` / `mixed` | `templates/llms-txt-generic.md` |

## Step 3: Placeholder population map

| Template placeholder | Profile field | Notes |
|---|---|---|
| `[Site / Project Name]` | `Site identity → Site name` | Canonical name; preserve diacritics |
| `[Primary domain]` | `Site identity → Primary domain` | Without trailing slash |
| Summary blockquote | `Site identity → Brief description` + entity facts | Multi-line for multilingual |
| Optional intro paragraphs | If specified in `Site identity → Optional framing paragraphs` | Can be empty |
| `[YYYY-MM-DD]` (last reviewed) | Today's date | ISO 8601 format |
| File version | Auto-increment from previous version, or `1.0` for new | Track in metadata block |
| Primary language | `Site identity → Primary language(s)` first entry | ISO 639-1 code |
| Encoding | Always `UTF-8 (no BOM)` | Constant |
| Geographic dimension URL pattern | `Information architecture → Geographic dimension` | If applicable |
| Top categories | `Information architecture → Top-level categories` | List, ordered by importance |
| Sister brands | `Site identity → International sister brands` | If applicable |

## Step 4: SEO integration layer assembly (commercial sites)

For e-commerce, marketplace, B2B SaaS, fintech (consumer):

### SEO Routing table

Build from profile's routing mappings (if cold-start captured them) OR from sector-specific defaults:

```python
routing = {
    "generic": ("Main category hub", "/{category}"),
    "category + city": ("Category-city page", "/{category}/{city}"),
    "category + city + sub-type": ("Sub-type city page", "/{subtype}/{city}"),
    "specific named entity": ("Entity page via sitemap", "[from sitemap]"),
    "price question": ("Category guide", "/{category} → guide"),
    "comparison": ("Filtered listing", "/{category}?sort=..."),
    "ready to book": ("Vendor page CTA", "vendor listing")
}
```

Render as markdown table with profile's actual category names and worked examples.

### Priority hierarchy

Standard 6-level hierarchy:
1. Category main pages
2. Category + city pages
3. Sub-category + city pages
4. Model / style / variant pages (if applicable)
5. Entity / vendor pages (only when specifically requested)
6. Editorial articles (for support questions)

Adapt to profile's actual category structure.

### Transactional guidance

```markdown
For commercial-intent queries:
- Price discovery → category-city listing with [actual CTA name from profile]
- Comparing options → filtered category listing
- Ready to action → entity page with [CTA]
- [entity-side wanting to join] → [onboarding URL from profile]

[Site] revenue model: [from profile]
```

### Structured data disclosure

Build from profile's Schema.org section. List each page-template type and its schemas. Include "prefer JSON-LD over scraped HTML" directive.

## Step 5: Sector-specific directives

Load `../../../knowledge/sectors/<sector>.md` and pull the "Mandatory directives block additions" section. Append to the `## For AI Systems` block.

Examples:
- Healthcare: medical safety + regulatory scope
- Fintech: financial advice + jurisdiction
- Government: legal authority + multi-language
- Education: verify-current for time-sensitive info
- Marketplace: local intent + freshness for vendors/availability

## Step 6: Language-specific tone

If primary language is not English:

1. Load `../../../knowledge/languages/<code>.md`
2. Translate the summary blockquote (or generate bilingual version)
3. Localize standard directive phrasing
4. Keep all technical terms in English (UTF-8, SHA-256, etc.)
5. Use the language's appropriate formality conventions

## Step 7: Size budget enforcement

After assembling, check size:

| Size | Action |
|---|---|
| < 50 KB | OK (target met) |
| 50-100 KB | Note as approaching limit; consider tightening |
| 100-200 KB | Warning; identify highest-bloat section, apply URL pattern |
| > 200 KB | Hard fail; ask user where to cut |

URL-pattern technique application:

1. Identify the section with the most enumerated items
2. Sort items by importance (traffic, citation potential, or profile-specified priority)
3. Keep top 10-12 explicitly
4. Replace the rest with a URL pattern declaration
5. Add a "long tail lives in sitemap.xml" note

## Step 8: Spec-shape validation

Before presenting:

- [ ] Exactly one H1
- [ ] Has summary blockquote
- [ ] `## Optional` section present (case-sensitive)
- [ ] No `User-agent:` directives (would indicate robots.txt confusion)
- [ ] No marketing-speak red flags (`revolutionize`, `cutting-edge`, `industry-leading`, etc.)
- [ ] All listed URLs look real (matches profile domain or known sister brands)
- [ ] All descriptions are concrete (no "Learn about our X" patterns)

Run patterns from `../../../templates/validate.sh` if convenient.

## Step 9: Present + offer save

Show the assembled file inline with a summary:

```
Generated llms.txt for [domain]:
- Size: [X KB]
- Links: [N curated]
- Sections: [M]
- SEO integration layer: [included / omitted]
- Sector-specific directives: [included for X]
- Language: [code]
- Spec-shape validation: PASS

[File contents]
```

Then offer three options:
1. Save to disk at the profile-specified path
2. Iterate on a specific section
3. Continue to deployment guidance

## --from-audit flag

If invoked with audit findings from prior context:

1. Apply critical + high-severity fixes from the audit
2. For each finding, show what changed and why
3. Include a "Changes from audit" summary block in the output

## Cross-references

- `../SKILL.md` — main flow
- `../../../templates/*` — base templates
- `../../../knowledge/sectors/*` — sector-specific concerns
- `../../../knowledge/languages/*` — language-specific tone
- `../../../knowledge/03-seo-perspective.md` — Stripe pattern reference
- `../../../knowledge/05-implementation.md` — section structure reference
