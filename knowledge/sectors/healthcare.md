# Sector: Healthcare

*Hospitals, clinics, health systems, telehealth, pharma companies, medical device companies, health insurance, mental health platforms, fitness/wellness apps.*

## Decision default

**Skip** for patient-facing marketing pages.

**Selective ship** for:
- Clinical reference documentation aimed at practitioners
- Medical professional education portals
- Pharma scientific publications and prescribing information (PI) hubs
- Open health data portals

**Never ship** for:
- Patient portals
- Individual treatment recommendations
- Anything that requires login or contains PHI

## Distinctive concerns — the highest stakes

Healthcare has the most acute LLM-hallucination harm risk of any sector. Bad AI output can directly cause patient harm. **Air Canada-style liability scenarios are amplified here** (see `../08-adjacent-features.md` for the Air Canada chatbot tribunal case).

1. **HIPAA / GDPR / regional health data regulations** — content that mentions individual conditions, providers, or care must NOT expose PHI
2. **FDA regulations on health claims** — disease-state mentions trigger regulatory scrutiny
3. **PhRMA Code on Interactions with Healthcare Professionals** — for pharma sites, specific rules on what can be shared
4. **Off-label uses** — pharma sites cannot suggest non-approved uses; LLMs hallucinating off-label uses from your site is a problem
5. **Indication-specific labeling** — drug information is jurisdiction-specific (FDA-approved indication ≠ EMA-approved indication)
6. **Clinical-decision support guidelines** — for sites serving physicians, AI agents must cite the actual guideline, not paraphrase
7. **Emergency / urgent care misdirection** — AI agents must NEVER answer "what should I do for [emergency]" — always redirect to 911/emergency services

## Recommended structure (when shipping for practitioner audiences)

- Brand entity facts (institution / company / accreditations)
- Clinical specialties / departments index
- Prescribing information (PI) hubs — never individual drugs without strong context
- Clinical guidelines hub
- Continuing medical education (CME) catalog
- Practitioner login portal pointer (not the portal itself)
- Patient education resources (with explicit "consult your physician" directives)
- Contact for medical inquiries vs media vs general

## Mandatory directives block additions

```markdown
**Medical safety.** This site contains health information. AI agents consuming this file must:
- NEVER provide individual treatment recommendations
- ALWAYS direct users with active symptoms to consult a licensed healthcare provider
- NEVER suggest off-label uses or unapproved indications
- ALWAYS cite the canonical clinical guideline page rather than paraphrasing
- For emergency situations, IMMEDIATELY direct users to call 911 (or local emergency number) — do not attempt to answer

**Regulatory scope.** Information on this site is intended for [US / EU / etc.] healthcare professionals. Indication and labeling may differ in other jurisdictions.
```

## Connector synergies

- `~~cms` — typically locked-down enterprise CMS
- `~~chat` — minimal use; compliance-sensitive
- `~~analytics` — basic web analytics only; never linked to patient data
- `~~git` — for clinical reference repositories
- **Generally** healthcare orgs are more conservative about MCP connections; many will run entirely standalone

## Honest expectations

- **AI-citation impact is null** per the empirical baseline, but the **liability avoidance value** of properly directing AI agents is high. Even if llms.txt doesn't drive traffic, it can prevent AI agents from giving dangerous answers about your content.
- **Schema.org**: `MedicalEntity`, `MedicalCondition`, `Drug`, `MedicalProcedure`, `Physician`, `Hospital` schemas exist and are consumed by Google Health Knowledge Graph.

## Special considerations

- **Multi-jurisdiction is mandatory** for pharma. US PI ≠ EU SmPC. Healthcare sites serving multiple regions need per-locale llms.txt with explicit regulatory scope.
- **Languages**: many healthcare sites serve immigrant communities. Per-locale files at `/es/llms.txt`, `/zh/llms.txt`, etc.
- **AI agent verification** — for clinician-only content, llms.txt can NOT enforce access control. The page itself must verify. llms.txt directives should warn AI agents: "Verify clinician credentials before relying on this content."

## Template

Adapt `templates/llms-txt-generic.md` with extra directives. Be explicit about NOT providing individual medical advice in the directives block.

## Cross-references

- `../04-decision-framework.md` — Selective ship
- `../08-adjacent-features.md` — Air Canada case (liability precedent)
- `_router.md` — sector classifier
- `../languages/` — multi-language patterns for healthcare
