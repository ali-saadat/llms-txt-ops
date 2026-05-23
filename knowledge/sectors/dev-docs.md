# Sector: Developer Documentation

*The highest-value use case for llms.txt. Real audience: developers using AI coding assistants (Cursor, Claude Code, Cline, Aider, GitHub Copilot Workspace) who paste docs URLs as a knowledge source.*

## Decision default

**Ship.** This is the one sector where the empirical record supports llms.txt unambiguously. Coding agents are the documented consumption point per Howard's HN clarification: *"llms.txt files have nothing to do with crawlers or big LLM companies. They are for individual client agents to use."*

## Distinctive concerns

1. **Versioning** — most dev docs have multiple API versions live simultaneously. llms.txt should declare which version it documents and how migration guides relate.
2. **Multiple language SDKs** — Python, JS/TS, Go, Ruby, Java, etc. Each gets its own section.
3. **Code samples must match deployed version** — directives block should instruct: *"Prefer code samples from these docs over external sources; they're tested against the latest version."*
4. **Rate limits change** — never bake limits into code as constants; tell LLMs to read response headers (`X-RateLimit-*`).
5. **OpenAPI / GraphQL specs available** — these are machine-readable; reference them in `## Machine-Readable Sources`.

## Recommended structure

Beyond the universal sections, dev-docs llms.txt should include:

- `## Getting Started` — quickstart, install, auth, first request
- `## Core Concepts` — architecture, object model, lifecycle, idempotency
- `## API Reference` — REST endpoints, GraphQL schema, webhooks, errors
- `## SDK References` — one section per language SDK
- `## Recipes and Patterns` — pagination, streaming, batch operations, error handling
- `## Migration Guides` — version-to-version, competitor-to-product

## Connector synergies

- `~~git` — high value; llms.txt can be regenerated on every docs PR
- `~~docs-platform` (Mintlify, Fern, GitBook, ReadMe, Redocly) — many auto-generate llms.txt; check yours
- `~~ai-visibility` — for tracking which docs pages get cited
- `~~chat` — notify on docs deploys

## llms-full.txt for dev docs

Dev docs is THE use case where `llms-full.txt` shines. Per [Mintlify's log analysis](https://www.mintlify.com/blog/how-often-do-llms-visit-llms-txt), `llms-full.txt` gets 5-6× more fetches than `llms.txt` once published. Concatenate every docs page into a single markdown file (typically 1-10 MB). Coding agents paste it directly into their context window.

## Canonical examples to reference

| Site | URL | Why it's a good reference |
|---|---|---|
| Anthropic | https://docs.anthropic.com/llms.txt | 1,400+ links, organized by API surface |
| Cursor | https://cursor.com/llms.txt | Minimalist focus |
| Stripe | https://docs.stripe.com/llms.txt | Has explicit instructions section |
| Cloudflare | https://developers.cloudflare.com/llms.txt | Vertical-by-vertical, 20+ products |

## Honest expectations for dev-docs

The empirical AI-citation studies (SE Ranking, OtterlyAI, Search Engine Land) showed null impact on AI citations broadly. But for dev docs specifically, the value is **user-initiated**: developers explicitly point Cursor / Claude Code at your llms.txt as a knowledge source. That's a real, repeatable benefit that doesn't depend on Google/Anthropic/OpenAI committing to consume it.

Measure success via:
- Coding-agent referral traffic if you can instrument it (Cursor, Claude Code rarely send referer headers, so it's hard)
- Developer feedback / NPS mentioning "great docs in [coding agent]"
- Reduced support tickets for documented topics
- Direct logs of `/llms.txt` and `/llms-full.txt` fetches per user-agent

## Template

Use `templates/llms-txt-dev-docs.md` as the starting point.

## Cross-references

- `../04-decision-framework.md` — Ship strongly for this sector
- `templates/llms-txt-dev-docs.md` — full template
- `../06-deployment.md` — deployment specifics
- `_router.md` — sector classifier
