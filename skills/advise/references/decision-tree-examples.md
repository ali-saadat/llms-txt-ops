# Decision Tree — Worked Examples

*Worked examples of the decision framework for `/advise`. Load when the user asks "should we ship for our specific situation".*

## Worked example 1: B2B SaaS docs

**Input**:
- Site type: B2B SaaS, docs subdomain on Mintlify
- Goal: developer adoption — want Cursor / Claude Code users to find our docs cleanly
- Current state: Mintlify auto-generates llms.txt
- Stakeholder dynamic: engineering team supportive, marketing skeptical

**Decision**: **SHIP (already done by Mintlify) — keep auto-gen, optionally curate further**

**Reasoning**:
- Dev docs is the one sector where the empirical record supports llms.txt
- Mintlify auto-gen is already production-ready
- The audience (Cursor / Claude Code users) is real
- Effort is essentially zero (already shipped)

**Next steps**:
- Audit the auto-generated file for completeness (`/audit`)
- Consider adding instructions block + SEO routing on top of auto-gen
- Set up Bing AI Performance monitoring to track citations

## Worked example 2: Marketing site for fintech startup

**Input**:
- Site type: marketing site (no docs subdomain), fintech (consumer payments)
- Goal: AI search visibility for "best payment processor" queries
- Current state: no llms.txt
- Stakeholder dynamic: CMO believes llms.txt will drive AI traffic

**Decision**: **SKIP llms.txt; invest in alternatives**

**Reasoning**:
- Marketing sites have null AI-citation lift per empirical record
- Stated goal (AI visibility) is not what llms.txt does
- Honest framing required to manage CMO expectations

**Next steps**:
- Use `/advise` to surface empirical evidence with CMO
- Draft stakeholder communication explaining the decision
- Pivot engineering hours to:
  - Schema.org on key product pages (Organization, Service, Offer)
  - Reddit / Hacker News thread strategy
  - Earned third-party citations (industry analyst quotes)
  - First-party data publication

## Worked example 3: Marketplace (ExampleMart pattern)

**Input**:
- Site type: marketplace (services vendors, 60K vendors across 81 provinces)
- Goal: replace bloated existing llms.txt
- Current state: 12.5 MB enumerated file (anti-pattern #1)
- Stakeholder dynamic: SEO lead wants tailored output; manager wants Jira-ready spec

**Decision**: **SHIP curated replacement** (the canonical ExampleMart playbook)

**Reasoning**:
- Replacing broken existing file = unambiguously better (reason #1)
- Marketplace has the right URL-pattern technique applicability
- SEO team input adds real value (sector + transactional layer)

**Next steps**:
- Cold-start interview to capture IA + SEO routing
- Generate v3 file with URL pattern (12.5 MB → ~30 KB target)
- Deployment spec for Jira ticket
- Stakeholder communication addressing SEO + manager separately

## Worked example 4: News publisher

**Input**:
- Site type: news / publisher (mid-sized regional newspaper)
- Goal: not being misrepresented in AI summaries
- Current state: no llms.txt; some Article schema on stories
- Stakeholder dynamic: editorial team concerned about AI scraping/training

**Decision**: **SKIP llms.txt for content; SHIP minimal one for editorial standards**

**Reasoning**:
- News content shouldn't be enumerated in llms.txt (changes too fast)
- Editorial standards + corrections policy + author directory ARE worth surfacing
- Primary AI-citation lever is author E-E-A-T + earned Wikipedia citations
- Robots.txt strategy matters more than llms.txt (AI training opt-out)

**Next steps**:
- robots.txt configuration for AI training bots (block) vs search bots (allow)
- Ship a small llms.txt pointing to editorial standards page
- Invest in Author Person schema with verified bylines
- Invest in original investigation / data journalism (Information Gain)

## Worked example 5: Healthcare provider

**Input**:
- Site type: hospital system, multi-language site (English + Spanish)
- Goal: not having AI agents give wrong medical advice citing the site
- Current state: no llms.txt; standard hospital website CMS
- Stakeholder dynamic: legal team cautious about anything that might create liability

**Decision**: **SKIP llms.txt for clinical content; consider for practitioner-facing reference docs only**

**Reasoning**:
- Patient-facing content shouldn't be summarized by AI without strong guardrails
- Air Canada liability precedent applies
- Higher value: clear schema + clear "consult your provider" disclaimers
- Defensible llms.txt would be clinical-reference-only with mandatory medical-safety directives

**Next steps**:
- Strong robots.txt with AI bot policy (decided by legal)
- Schema.org for MedicalOrganization, Hospital, Physician on entity pages
- Maybe a llms.txt with ONLY the medical-safety directives + emergency contact info, no service enumeration

## Decision matrix shortcut

For quick triage:

| Question | If YES → | If NO → |
|---|---|---|
| Site type is dev-docs / developer-facing? | Ship | Continue |
| Existing llms.txt is bloated / broken? | Ship (replacement) | Continue |
| Building internal RAG / chatbot? | Ship (internal grounding bonus) | Continue |
| Heavy commercial site with multi-region IA? | Consider (marketplace pattern) | Continue |
| Regulated industry with high liability risk? | Selective ship (with directives) | Continue |
| Marketing-only site, no docs subdomain? | Skip; invest in alternatives | Reconsider |
| News / editorial publisher? | Skip; invest in E-E-A-T | Reconsider |
| Genuinely uncertain? | Use `/setup-recommender` first | n/a |

## Cross-references

- `../SKILL.md` — main router
- `../../../knowledge/04-decision-framework.md` — full decision framework
- `../../../knowledge/sectors/*` — per-sector decision defaults
- `../../../case-study/example-marketplace-case.md` — worked example 3 in full detail
