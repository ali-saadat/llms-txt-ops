# Connectors — Category Dictionary for llms.txt Advisor

This plugin is **tool-agnostic**. Skills describe workflows in terms of **categories** (`~~category`) rather than specific vendors. The `.mcp.json` pre-configures some specific MCP servers, but any MCP server in the same category works.

If a skill says "fetch via `~~git`", and your team uses GitLab instead of GitHub, the skill will use whichever git MCP you have connected. If a skill says "post results to `~~chat`", and you're on Microsoft Teams instead of Slack, it goes to Teams.

## Category table

| Category | Placeholder | Included servers in `.mcp.json` | Other options users can substitute |
|---|---|---|---|
| **Git / version control** | `~~git` | GitHub | GitLab, Bitbucket, Gitea, Azure DevOps, Gitee (CN) |
| **Docs storage** | `~~docs-storage` | Google Drive, Notion | Microsoft 365 (OneDrive/SharePoint), Box, Confluence, Dropbox, Obsidian, Yuque (CN), Lark/Feishu (CN) |
| **Chat / notifications** | `~~chat` | Slack, Notion | Microsoft Teams, Discord, Mattermost, Webex, WeChat Work (CN), DingTalk (CN), Line (JP/TW), KakaoTalk (KR) |
| **CMS** | `~~cms` | WordPress, Contentful, Sanity | Strapi, Ghost, Drupal, Storyblok, Builder.io, Webflow, Wix |
| **E-commerce platform** | `~~ecommerce` | Shopify | WooCommerce, BigCommerce, Magento, Squarespace Commerce, PrestaShop, Tmall (CN), JD.com (CN), Taobao (CN), Lazada (SEA), Mercado Libre (LatAm), Coupang (KR) |
| **Hosting / serverless** | `~~hosting` | Vercel | Netlify, Cloudflare Pages, Fly.io, Railway, AWS Amplify, Render, Alibaba Cloud (CN), Tencent Cloud (CN), Naver Cloud (KR) |
| **CDN** | `~~cdn` | Cloudflare | Fastly, Akamai, AWS CloudFront, Bunny, KeyCDN, Alibaba Cloud CDN (CN), Tencent Cloud CDN (CN) |
| **Search console** | `~~search-console` | Bing Webmaster | Google Search Console (if/when an MCP is available), Yandex Webmaster (RU), Baidu Webmaster (CN), Naver Search Advisor (KR) |
| **AI visibility tracking** | `~~ai-visibility` | Profound, Peec AI, OtterlyAI | Goodie, AIPRM, BrightEdge AI module |
| **SEO tools** | `~~seo-tools` | Ahrefs, Semrush | Moz, SE Ranking, Sistrix, Conductor, BrightEdge, SearchPilot |
| **Web analytics** | `~~analytics` | Google Analytics, Plausible | Adobe Analytics, Matomo, Fathom, Mixpanel, Heap, Amplitude, Yandex Metrica (RU), Baidu Tongji (CN), Umami |
| **Headless browser** | `~~headless-browser` | (none preconfigured) | Browserbase, Browserless, Playwright MCP, Puppeteer MCP, Apify |
| **Docs platform** | `~~docs-platform` | (none preconfigured) | Mintlify, Fern, GitBook, ReadMe, Redocly, Bump.sh |

## Category usage rules (the "Standalone vs Supercharged" contract)

Every skill in this plugin is written to **work standalone** — i.e., with no MCP connectors at all, accepting pasted content or URLs. When connectors ARE connected, skills automatically gain enhanced capabilities. This pattern is borrowed from `anthropics/knowledge-work-plugins` (see "Standalone + Supercharged" tables in every plugin's README).

### What works standalone (no MCP needed)

- User pastes their current llms.txt content, sitemap.xml, or robots.txt
- User describes their site's structure
- Web search for general best practices
- Reading files the user explicitly shares
- All knowledge files in this plugin

### What's supercharged with connectors

| Skill | Standalone | With `~~git` | With `~~cms` | With `~~ai-visibility` | With `~~headless-browser` |
|---|---|---|---|---|---|
| **cold-start-interview** | Conversational, manual answers | Auto-extract repo paths | Pull category structure from CMS | Skip "do we have monitoring" question (already wired) | Auto-fetch existing llms.txt + robots.txt + sample pages |
| **audit** | User pastes content | Read the source file from repo | Cross-check CMS pages match listed URLs | Check whether listed URLs are actually being cited | Live-crawl listed URLs to verify content matches descriptions |
| **generate** | Use template + user answers | Write the file directly to repo via PR | Pull category hub URLs from CMS | Suggest URLs based on actual citation data | Validate every URL exists and renders |
| **customize** | Edit text inline | Open a branch for the change | Sync CMS taxonomy changes | n/a | n/a |
| **deploy** | Hand the user the config block | Open a PR with server config + CI workflow | n/a | n/a | n/a |
| **stakeholder-comms** | Draft to clipboard | n/a | n/a | Reference citation data in email | n/a |

## Detection pattern (used by every skill)

Each skill follows this contract at the start of its body:

```
### Connector probe
Before doing substantive work:

1. Check which ~~categories are connected. Identify by calling list_tools()
   or checking available MCP servers.
2. Note which categories from the table above are AVAILABLE vs UNAVAILABLE.
3. For UNAVAILABLE categories, the skill operates in standalone mode for that
   feature — fall back to web search, user-pasted content, or skip the
   enhanced capability while announcing the degradation clearly.
4. NEVER claim a feature works that depends on an unavailable connector.
```

This pattern is documented in `knowledge/03-seo-perspective.md` and used in `skills/cold-start-interview/SKILL.md` Step 6 (Seed-doc ingestion).

## Degradation matrix

| Missing connector | Effect | User-facing message |
|---|---|---|
| `~~git` | Can't auto-write file to repo; user must commit manually | "I'll produce the file here in chat — you commit it to your repo manually" |
| `~~headless-browser` | Can't live-crawl URLs; assumes user-provided content is current | "I'll validate links via HTTP HEAD only — won't fetch full page content" |
| `~~ai-visibility` | No real-time citation data; rely on the empirical baseline from research | "I'll use the three-studies baseline rather than your live citation telemetry" |
| `~~cms` | Can't auto-sync category structure | "Tell me your top-level categories manually — I can't probe your CMS" |
| `~~chat` | No notification on deploy | "I won't post results to your team chat — you'll need to share manually" |
| `~~search-console` | Can't pull AI Performance report (Bing) data | "Set up Bing AI Performance manually post-deploy for citation telemetry" |
| `~~analytics` | Can't auto-detect top-traffic cities/categories | "Tell me your top-12 cities/categories by traffic manually" |

## Connector selection guidance per site type

| Site type | Most-useful connectors (in order) |
|---|---|
| Developer documentation | `~~git`, `~~docs-platform`, `~~ai-visibility` |
| Marketing site / blog | `~~cms`, `~~analytics`, `~~ai-visibility` |
| E-commerce | `~~ecommerce`, `~~analytics`, `~~cdn`, `~~ai-visibility` |
| Marketplace | `~~ecommerce` (or `~~cms`), `~~headless-browser`, `~~analytics` |
| News / publisher | `~~cms`, `~~analytics`, `~~search-console` |
| Education | `~~cms`, `~~analytics` |
| Healthcare | `~~cms`, `~~analytics`, `~~git` (for compliance trails) |
| Fintech / banking | `~~cms`, `~~chat` (for compliance notifications), `~~git` |
| Government / civic | `~~cms`, `~~analytics`, `~~search-console` |
| Gaming | `~~cms`, `~~analytics`, `~~ai-visibility` |
| B2B SaaS | `~~docs-platform`, `~~cms`, `~~ai-visibility`, `~~git` |
| Non-profit | `~~cms`, `~~analytics` |
| Media / entertainment | `~~cms`, `~~analytics`, `~~ai-visibility` |

## How to add a new connector category

If your team needs a category not listed here:

1. Add an entry to the category table above
2. Add the placeholder (e.g., `~~podcast-platform`) to whichever skills should use it
3. Add an entry to `.mcp.json` with `"url": ""` (empty slot)
4. Document any standalone fallback in the degradation matrix
5. Update the SKILL.md frontmatter `description` field if the category enables new trigger phrases

## Authentication notes

- Most MCP servers use HTTP/OAuth — the OAuth flow runs through Claude Code's `/mcp` command when the user first invokes the server
- Slack and a few others embed OAuth metadata in `.mcp.json`; everything else is URL-only
- Per-tenant URLs (e.g., `${WORDPRESS_MCP_URL}`) should be set via environment variables, not hard-coded in `.mcp.json`
- For self-hosted MCP servers (custom internal CMS, etc.), set the URL directly in user/project settings, not in the plugin's `.mcp.json`

## Cross-references

- [`.mcp.json`](.mcp.json) — the actual MCP server configuration
- [`README.md`](README.md) — plugin overview
- [`knowledge/06-deployment.md`](knowledge/06-deployment.md) — server config and CI patterns
- [`reference/ai-bots.md`](reference/ai-bots.md) — AI crawler user-agents (distinct from MCP)
- Pattern source: [`anthropics/knowledge-work-plugins`](https://github.com/anthropics/knowledge-work-plugins) — see any plugin's `CONNECTORS.md`
