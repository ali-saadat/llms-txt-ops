---
name: deploy
description: >
  Produce technical deployment guidance for the user's llms.txt — Nginx /
  Apache / Caddy / Vercel / Netlify / Cloudflare server config, CI validation
  pipeline wiring, robots.txt consistency checks, CDN purge strategy,
  monitoring setup. Use when the user says "how do I deploy", "server config",
  "ship it to production", "CI for llms.txt", "robots.txt setup", or has a
  file ready and needs deployment specifics. Use specifically for
  **deployment Jira tickets** (when user says "deployment ticket", "CI
  ticket", "ops ticket", "open a deployment Jira") — the ticket scope is
  server config, CI changes, robots.txt diff, rollback playbook. For
  vanilla "write the Jira ticket description" or "draft the Jira ticket"
  requests (without "deployment" or "technical" qualifier), defer to
  `stakeholder-comms` which owns the default writing/drafting framing.
argument-hint: "[--platform nginx|apache|caddy|vercel|netlify|cloudflare] [--ticket to produce a deployment-scope Jira ticket] [--monitoring to focus only on logging/monitoring]"
---

**Note on Jira tickets**: this skill produces the **deployment** Jira ticket — technical scope, server config, CI workflow changes, robots.txt diff, rollback playbook. For a **stakeholder-facing** Jira ticket (business context, owners, communication updates), use `/llms-txt-advisor:stakeholder-comms` instead.

# Deploy — Production Deployment Guidance

## Step 1 — Profile check

Bounce-on-placeholder pattern. The deployment skill needs to know the user's hosting platform, CDN, and CI choice from the profile.

If profile has those fields as `[PLACEHOLDER]` or `[PENDING]`, do a mini-interview before proceeding:

```
A few deployment specifics I need:
1. What's the server? (Nginx, Apache, Caddy, Vercel, Netlify, Cloudflare Workers, other)
2. CDN in front? (Cloudflare, Fastly, Akamai, AWS CloudFront, none)
3. CI/CD pipeline? (GitHub Actions, GitLab CI, CircleCI, other)
```

Save answers to profile before proceeding.

## Step 2 — Generate server config

Based on platform, emit the relevant block from `templates/nginx-config.conf` adapted to the user's setup:

### Required headers (all platforms)

- `Content-Type: text/markdown; charset=utf-8`
- `X-Robots-Tag: noindex`
- `Cache-Control: public, max-age=3600`
- `Access-Control-Allow-Origin: *`

### Platform-specific snippets

| Platform | Approach |
|---|---|
| Nginx | `location = /llms.txt { ... }` block with `add_header` directives |
| Apache | `<Files "llms.txt"> ... </Files>` with `Header set` directives |
| Caddy | `@llms_txt path /llms.txt` matcher with `header` directives |
| Vercel | `vercel.json` `headers` array with source matching `/llms.txt` |
| Netlify | `netlify.toml` `[[headers]]` block |
| Cloudflare Workers | Worker script that intercepts `/llms.txt` requests and adds headers |

Produce the actual config snippet inline. Reference `templates/nginx-config.conf` for the Nginx canonical version.

## Step 3 — CI validation wiring

Reference `templates/validate.sh`. Produce a CI job snippet for the user's CI platform.

### GitHub Actions example

```yaml
- name: Validate llms.txt
  run: |
    chmod +x ./templates/validate.sh
    ./templates/validate.sh ./llms.txt
```

### GitLab CI example

```yaml
validate_llms_txt:
  script:
    - chmod +x ./templates/validate.sh
    - ./templates/validate.sh ./llms.txt
```

Include the SHA-256 hash from the current file as the pinned-source check:

```bash
./templates/validate.sh ./llms.txt $EXPECTED_HASH
```

## Step 4 — robots.txt consistency

Load the user's robots.txt (from profile or by fetching `https://{domain}/robots.txt`). For each AI user-agent declared in the user's profile:

- Verify URLs in the llms.txt are `Allow:` (not `Disallow:`)
- Flag inconsistencies as 🟠 high-severity findings

Reference `reference/ai-bots.md` for the full bot inventory and the per-purpose decision pattern.

If profile says "I want search bots but not training bots", emit a sample robots.txt snippet implementing that policy.

## Step 5 — CDN purge

Based on profile's CDN choice, emit a purge command.

### Cloudflare example

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"files":["https://example.com/llms.txt","https://example.com/llms-full.txt"]}'
```

Tell the user where to put this in their deploy pipeline.

## Step 6 — Post-deploy verification

Always include this step in the deployment plan:

```bash
# After deploy, verify the served file is byte-identical to the source
LOCAL_HASH=$(shasum -a 256 llms.txt | awk '{print $1}')
LIVE_HASH=$(curl -s https://yoursite.com/llms.txt | shasum -a 256 | awk '{print $1}')
[ "$LOCAL_HASH" = "$LIVE_HASH" ] || { echo "FAIL: deployed file differs from source"; exit 1; }
```

This catches CDN transformations, proxy mutations, and accidental wrong-file deploys.

## Step 7 — Monitoring setup

Reference `knowledge/06-deployment.md` for the full monitoring section. Key outputs:

- Server log format including User-Agent
- Per-user-agent fetch counter
- Bing Webmaster Tools AI Performance setup pointer (the only first-party AI-citation telemetry available as of May 2026)
- Realistic-expectations note: per OtterlyAI study, expect <1% of AI bot traffic. Set alerts only for sudden drops.

## Step 8 — Produce the deployment spec

If user passed `--ticket`, format the output as a Jira-ready ticket description:

```markdown
## Task
Deploy llms.txt v[X] to production.

## Acceptance criteria
- [ ] File served at https://[domain]/llms.txt
- [ ] Content-Type header includes `charset=utf-8`
- [ ] X-Robots-Tag: noindex header set
- [ ] Cache-Control: public, max-age=3600
- [ ] Validation script wired into CI; passing
- [ ] CDN purge step added to deploy pipeline
- [ ] Post-deploy SHA-256 verification passes
- [ ] robots.txt updated for AI user-agent consistency (see section below)
- [ ] Monitoring: per-user-agent fetches logged

## Pinned source hash
SHA-256: [hash from current file]

## Server config block
[Nginx / Apache / etc. config block]

## CI validation
[GitHub Actions / GitLab CI / etc. snippet]

## robots.txt changes
[Diff of robots.txt changes needed]

## Rollback plan
- Restore prior file from Git
- CDN purge
- Validation re-run
- Source hash check

## Monitoring
- Bing Webmaster Tools AI Performance: [verified / to verify]
- Server log per-user-agent: [enabled / to enable]
- Realistic expectations: <1% of AI bot traffic per OtterlyAI study (Feb 2026)
```

## Step 9 — Offer next steps

```
Deployment spec ready. What now?

1. Save to file (`deployment-spec.md`) for the dev team
2. Walk through the validation script details
3. Help draft the email to the dev team / SEO team / leadership → `/llms-txt-advisor:stakeholder-comms`
```

## Guardrails

- **Never tell the user to skip the `noindex` header.** Mueller-confirmed appropriate; default to including it.
- **Never recommend `Disallow: /llms.txt` in robots.txt.** It breaks the `noindex` directive (noindex needs crawlability).
- **Realistic expectations on monitoring.** Tell users to expect <1% of AI bot traffic, not "you'll see ChatGPT crawling daily."
- **The file is a draft until SHA-256 matches.** Post-deploy verification is required, not optional.

## Cross-references

- `templates/nginx-config.conf` — Nginx canonical config
- `templates/validate.sh` — the CI script
- `knowledge/06-deployment.md` — full deployment guide
- `reference/ai-bots.md` — AI crawler user-agents and access patterns
- `case-study/deployment-spec.md` — the ExampleMart example spec
