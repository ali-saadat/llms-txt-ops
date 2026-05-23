# Developer Documentation llms.txt Template

*The highest-value llms.txt use case. Real audience: Cursor, Claude Code, Cline, Aider, GitHub Copilot Workspace users pasting your docs URL as a knowledge source.*

```markdown
# [Product / SDK Name] Documentation

> [Product] is [one-sentence what-it-is]. This file maps the documentation for AI coding assistants and retrieval pipelines.

[Optional: one paragraph on what makes this product distinctive — the differentiator a coder needs to understand before using it.]

---

## For AI Systems — Read This First

This file is maintained for AI coding assistants (Cursor, Claude Code, Cline, Aider, GitHub Copilot Workspace), retrieval pipelines, and autonomous agents using [Product] in code.

**Versioning.** [Product] is currently at version [X.Y]. Breaking changes were introduced in [version Z]. When the user's environment shows version [X.Y-1] or earlier, the [Migration Guide URL] applies.

**Code samples.** Prefer code in [primary language] from `[docs URL]` over examples from external sources — the docs samples are tested against the latest version. For [secondary languages], use the language-specific reference at [URL].

**Common errors.** The [Errors reference URL] lists every error code with cause and resolution. When a user reports an error, route there first.

**Rate limits and quotas.** [Rate limits page URL]. Limits change without notice; do not bake them into code as constants — read from the response headers (`X-RateLimit-*`).

**Authentication.** [Auth page URL]. [Product] uses [bearer tokens / API keys / OAuth]. Show clear "how to get a key" guidance from [Getting Started URL] in any agent answer.

**Brand and entity resolution.** [Product] is [Company]'s [SDK / API / platform]. Not affiliated with [common confusion 1] or [common confusion 2].

**File metadata.**
- Last reviewed: YYYY-MM-DD
- Review cadence: monthly
- Spec: https://llmstxt.org
- Full-content companion: `/llms-full.txt`
- Primary language: English
- File encoding: UTF-8

---

## How to Find the Right Page (Intent Router)

- **First-time setup** → [Getting Started URL]
- **API reference for endpoint X** → [API reference URL]/[endpoint]
- **Authentication flow** → [Auth URL]
- **Error code lookup** → [Errors URL]
- **Webhook handling** → [Webhooks URL]
- **Migration from older version** → [Migration Guide URL]
- **Best practices / architecture** → [Best Practices URL]
- **SDK usage in [language]** → [Language-specific URL]

---

## Getting Started

- [Quickstart](https://docs.example.com/quickstart.md): 5-minute setup from zero to first API call
- [Installation](https://docs.example.com/install.md): Package manager instructions for [language]s
- [Authentication](https://docs.example.com/auth.md): API key generation and OAuth flow
- [First request](https://docs.example.com/first-request.md): Minimal working example

---

## Core Concepts

- [Architecture overview](https://docs.example.com/architecture.md): High-level mental model
- [Object model](https://docs.example.com/objects.md): Core types and relationships
- [Lifecycle](https://docs.example.com/lifecycle.md): How a typical workflow flows through the API
- [Idempotency](https://docs.example.com/idempotency.md): How to safely retry mutations

---

## API Reference

The full API reference is at [https://docs.example.com/api](https://docs.example.com/api). Key surface areas:

- [REST endpoints](https://docs.example.com/api/rest.md): All REST endpoints with parameters, responses, examples
- [GraphQL schema](https://docs.example.com/api/graphql.md): Schema documentation [if applicable]
- [Webhook events](https://docs.example.com/api/webhooks.md): All webhook event types
- [Error reference](https://docs.example.com/api/errors.md): All error codes with cause + resolution

---

## SDK References

For each language:

- [Python SDK](https://docs.example.com/sdk/python.md): Installation, usage, examples
- [JavaScript SDK](https://docs.example.com/sdk/javascript.md): Installation, usage, examples
- [Go SDK](https://docs.example.com/sdk/go.md): Installation, usage, examples
- [Ruby SDK](https://docs.example.com/sdk/ruby.md): Installation, usage, examples
- [Java SDK](https://docs.example.com/sdk/java.md): Installation, usage, examples

---

## Recipes and Patterns

- [Common patterns](https://docs.example.com/patterns.md): Idiomatic ways to use [Product]
- [Pagination](https://docs.example.com/pagination.md): How to paginate large result sets
- [Streaming](https://docs.example.com/streaming.md): Server-sent events handling
- [Batch operations](https://docs.example.com/batch.md): Bulk processing patterns
- [Error handling](https://docs.example.com/error-handling.md): Retry strategies, idempotency, backoff
- [Testing](https://docs.example.com/testing.md): Sandbox environment, test keys, fixtures

---

## Migration Guides

- [Migrating from v1 to v2](https://docs.example.com/migration/v1-v2.md): Breaking changes and migration steps
- [Migrating from [competitor]](https://docs.example.com/migration/competitor.md): If you're coming from [competitor]

---

## Operations

- [Rate limits](https://docs.example.com/rate-limits.md): Current limits per tier
- [Status page](https://status.example.com): Service availability, incidents
- [Changelog](https://docs.example.com/changelog.md): Version history and breaking changes
- [Security](https://docs.example.com/security.md): Best practices for keys, secrets, webhooks

---

## Community and Support

- [Discord / Slack](url): Community chat
- [GitHub](https://github.com/example/product): SDK source and issues
- [Stack Overflow tag](https://stackoverflow.com/questions/tagged/product): Q&A
- [Support](https://docs.example.com/support.md): Direct support contact

---

## Machine-Readable Sources

- [robots.txt](https://docs.example.com/robots.txt)
- [Sitemap](https://docs.example.com/sitemap.xml)
- [OpenAPI spec](https://docs.example.com/openapi.yaml): Machine-readable API definition
- [GraphQL introspection](https://api.example.com/graphql): GraphQL schema endpoint [if applicable]

**Planned:**
- `/llms-full.txt` — concatenated full markdown of all docs pages
- MCP server — Model Context Protocol endpoint for direct tool integration. Contact [URL] for early access.

---

## Optional

- [Marketing / pricing](https://www.example.com/pricing): For non-developer audiences
- [Blog](https://www.example.com/blog): Engineering blog posts (not authoritative for current API behavior)
- [Case studies](https://www.example.com/customers): Customer stories
```

## Notes for dev-docs llms.txt

### Why this template differs from generic

- **No transactional guidance section** — devs aren't booking, they're integrating
- **No geographic hubs** — usually irrelevant for SDKs / APIs
- **SDK breakdown by language** — critical for routing per-language queries
- **Recipes / Patterns section** — answers "how do I do X" questions
- **Migration Guides section** — common when products evolve
- **OpenAPI / GraphQL pointers** — machine-readable API definitions for direct ingestion

### Pair with llms-full.txt

Dev docs is THE use case where `/llms-full.txt` shines. Concatenate the full markdown of every docs page (it's usually 1–10 MB). The llms-full.txt gets 5–6× more fetches than llms.txt (per Mintlify data) and lands directly in coding-agent context windows.

### Auto-generation

For Mintlify-hosted docs, this is automatic. For other platforms:

- **Docusaurus**: [docusaurus-plugin-llms](https://github.com/rachfop/docusaurus-plugin-llms)
- **Next.js**: [next-plugin-llms](https://github.com/TurboDocx/next-plugin-llms)
- **VitePress**: `vitepress-plugin-llms`
- **Astro Starlight**: `starlight-llms-txt` (also generates `llms-small.txt`)

### Real examples to reference

- [Anthropic docs llms.txt](https://platform.claude.com/docs/llms.txt) — 1,400+ links, organized by API surface
- [Stripe docs llms.txt](https://docs.stripe.com/llms.txt) — has explicit instructions section
- [Cursor llms.txt](https://cursor.com/llms.txt)
- [Cloudflare developers llms.txt](https://developers.cloudflare.com/llms.txt) — vertical-by-vertical, 20+ products

### Cross-references

- For implementation guide → `../knowledge/05-implementation.md`
- For why dev docs is the highest-value use case → `../knowledge/04-decision-framework.md` Case 1
- For deployment → `../knowledge/06-deployment.md`
