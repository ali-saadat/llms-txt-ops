# Sector: Education

*K-12, universities, online courses (Coursera, edX, MOOCs), LMS platforms, professional training, language learning, tutoring services.*

## Decision default

**Skip** for student-facing marketing pages.

**Selective ship** for:
- Course catalogs and curriculum documentation
- Open-access educational resources (OERs)
- Faculty / instructor directories (with `ProfilePage` schema)
- Glossaries and reference content

## Distinctive concerns

1. **Multiple audience tiers** — students, parents, faculty, administrators, prospective applicants, alumni. Each consumes different pages.
2. **Accreditation visibility** — for higher ed, accreditation status is canonical knowledge AI agents should cite correctly.
3. **Academic calendar / enrollment cycles** — content freshness matters; AI agents giving stale enrollment deadlines is a real harm.
4. **Multiple campuses / programs** — like a marketplace dimension; URL patterns for location × program.
5. **FERPA / COPPA / GDPR for student data** — never expose individual student information; never include URLs that require login.
6. **Reading-level alignment** — content for K-12 should be machine-readable as such (not necessarily a Schema.org type but worth noting in directives).

## Recommended structure

- Brand entity facts (institution name, founding, accreditation, enrollment size, location)
- Academic programs / courses / curricula (top-level only — not every section)
- Faculty / staff directory hub
- Admissions process and deadlines (with explicit "verify current deadlines" directive)
- Tuition and financial aid hubs (with "verify current rates" directive)
- Academic calendar / important dates hub
- Open educational resources (if any)
- Library / research databases (if public)
- Contact for prospective students vs current students vs media

## Connector synergies

- `~~cms` — typically a complex multi-site CMS (Drupal common in higher ed)
- `~~analytics` — track which programs / pages get AI traffic
- For LMS platforms (Canvas, Moodle, Blackboard): these usually live behind auth and should NOT be in llms.txt

## Honest expectations

- **No measurable AI-citation lift** for education sites per the empirical baseline. The high-leverage moves are:
  - `Course` schema on course pages
  - `EducationalOrganization` schema on the institution page
  - `Person` schema on faculty pages
  - Authoritative external citations (research mentions, news coverage)

- **Verify-current directives** are critical for education because so much information is time-sensitive (enrollment deadlines, tuition, course schedules). Build "fetch the canonical page; don't trust stale data" into the AI directives block.

## AI hallucination risks specific to education

- LLMs frequently hallucinate course numbers, faculty names, deadlines, and tuition figures. The llms.txt directives block should explicitly tell AI agents to fetch canonical hub URLs and disclaim uncertainty about specifics.
- Avoid listing individual course pages in llms.txt unless the catalog is small (< 200 courses). Use URL pattern for the long tail.

## Special considerations

- **Multi-language**: many education sites serve multiple languages. Use per-locale llms.txt files (`/en/llms.txt`, `/es/llms.txt`).
- **Academic integrity**: some institutions have official policies on AI use; reference those.
- **Open courseware** (MIT OCW, Stanford Online, etc.): for these, llms.txt makes more sense — the content is explicitly designed for distribution.

## Template

Adapt `templates/llms-txt-generic.md` with the structure above.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `_router.md` — sector classifier
- `../languages/` — multi-language patterns for international education sites
