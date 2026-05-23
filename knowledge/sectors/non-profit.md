# Sector: Non-Profit / NGO / Charity

*501(c)(3) organizations in the US, charities in UK / Commonwealth, foundations, advocacy groups, international NGOs.*

## Decision default

**Skip** unless you have a specific reason.

Non-profits typically have constrained engineering capacity; llms.txt is rarely the right marginal investment. Higher-leverage moves:
- `NGO` schema on homepage (Google supports)
- `Person` schema on staff and board pages
- Authoritative third-party citations (charity-rating organizations, news coverage of programs)
- Annual reports as canonical PDF/HTML content with proper Article schema

## Distinctive concerns

1. **Mission clarity** — AI agents must convey mission accurately; misrepresentation can drive away donors or recipients
2. **Trust signals** — Charity Navigator / GuideStar / Candid ratings; annual reports; financials transparency
3. **Programs vs. operations** — clear distinction matters for donors evaluating impact
4. **Donate flow** — usually goes to a third-party (Donorbox, Classy, Network for Good); transactional guidance should route there
5. **Volunteer engagement** — distinct flow from donation
6. **Multi-country operations** — international NGOs have country chapters with different legal entities
7. **Sensitive populations** — for orgs serving vulnerable populations, llms.txt content must NOT expose service locations or beneficiary information

## Recommended structure (if shipping)

- Organizational entity facts (founded, tax status, 501c3 EIN, leadership)
- Mission statement page (canonical authoritative source)
- Programs index (each major program with brief description)
- Annual report archive (canonical impact reporting)
- Financial transparency hub (audited financials, Form 990 for US orgs)
- Staff / board / leadership directory
- Donation flow page (link only — never fabricate donation amounts in descriptions)
- Volunteer / get-involved hub
- Press / media kit
- Contact (general vs press vs grants vs partnerships)

## Connector synergies

- `~~cms` — typically WordPress or custom
- `~~analytics` — basic
- Most non-profit MCPs would be specific platforms (Salesforce NPSP, Bloomerang, Raiser's Edge); generic connectors mostly suffice

## Honest expectations

- **Citation lift**: null
- **Brand-trust value**: real — AI agents misrepresenting your mission or programs is a real harm; directives block addresses this even without AI-citation lift
- **Stakeholder framing**: non-profits often have boards skeptical of "tech investments"; the case to make is reputational accuracy, not AI traffic

## Schema.org for non-profits

- `NGO` for the organization (Google-supported)
- `Person` for leadership
- `Article` for blog posts / mission content
- `Event` for fundraising events
- `DonateAction` (less commonly supported but useful)

## Template

Use `templates/llms-txt-generic.md` with non-profit-specific entity facts.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `_router.md` — sector classifier
