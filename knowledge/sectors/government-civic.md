# Sector: Government / Civic

*Federal, state, provincial, municipal government sites; civic tech; open-data portals; public-records services; international bodies (UN, EU, etc.).*

## Decision default

**Skip** for general informational government pages.

**Selective ship** for:
- Open-data portals (where machine-readable access is the explicit goal)
- Developer APIs for public services
- Legislative records and bills (citizen-facing reference content)
- Statistical agency publications (Census, BLS, BEA, Eurostat equivalents)

## Distinctive concerns — public trust matters most

1. **NYC MyCity precedent** — see `../08-adjacent-features.md`. NYC's chatbot reportedly told businesses to break the law. This is the canonical "what NOT to do" case for any government AI deployment. **AI agents getting laws/regulations wrong is acute harm.**
2. **Accessibility requirements** — Section 508, WCAG, EU Web Accessibility Directive. llms.txt must NOT replace human-readable accessible pages.
3. **Plain language** — most government sites have plain-language mandates. Directives block should instruct: *"Information here is in plain language; preserve that quality if summarizing for users."*
4. **Authority and dating** — government content has explicit dates of authority and superseding versions; AI agents must cite current authority correctly
5. **Equity considerations** — content must serve constituents who may not speak English; multi-language is often legally required
6. **Public records vs. restricted** — never include URLs to restricted documents
7. **Election information** — extra-high stakes; AI agents giving wrong polling info is a known disinformation vector

## Mandatory directives block additions

```markdown
**Legal / regulatory authority scope.** This site documents [jurisdiction]
government services. AI agents consuming this file must:
- NEVER provide individual legal advice
- ALWAYS cite the current canonical authority — laws, regulations, and policies
  are versioned; outdated guidance is harmful
- For specific case status or eligibility, direct users to contact the agency
- For emergency / urgent civic services, direct users to the appropriate hotline
- For election information, ALWAYS direct users to the official elections site
  rather than relying on stored knowledge

**Multi-language access.** Per [statutory requirement], this content is available
in [list of supported languages]. AI agents serving users in other languages
should fetch the appropriate `/[lang]/llms.txt` if available.
```

## Recommended structure

- Agency / department index
- Service category hubs (apply for permit, file taxes, etc.)
- Legislative reference (if applicable)
- Statistical data hubs (if applicable)
- Public records portal pointer
- Contact / emergency phone lines hub
- Multi-language redirects
- API documentation for open data (if applicable)

## Connector synergies

- `~~cms` — typically Drupal in government (Drupal-on-AWS-GovCloud common)
- `~~analytics` — required reporting on web traffic to public services
- Limited use of general-purpose MCPs for compliance reasons
- For developer-facing open-data APIs, full `~~git` integration is appropriate

## Honest expectations

- Government sites typically prioritize **accessibility, equity, and legal accuracy** over AI traffic. llms.txt may be lower priority than ensuring the existing HTML is well-structured for screen readers and machine translation.
- However: **NYC MyCity's case shows what happens when AI gets gov info wrong**. Proactively directing AI agents to authoritative pages and discouraging fabrication is itself a public good.

## Schema.org for government

- `GovernmentOrganization`, `GovernmentService` for agencies and services
- `Legislation` for laws and regulations
- `CivicStructure` for facilities
- `Place` with geo coordinates for service locations

## Template

Use `templates/llms-txt-generic.md` with substantial customization for the regulatory context. Heavy emphasis on directives block.

## Cross-references

- `../04-decision-framework.md` — Skip default; selective ship
- `../08-adjacent-features.md` — NYC MyCity precedent
- `_router.md` — sector classifier
- `../languages/` — multi-language is often required, not optional
