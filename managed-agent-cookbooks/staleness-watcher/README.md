# Staleness Watcher — Managed Agent Cookbook

Headless deployment of the staleness-watcher agent via the Claude Managed Agents API. Runs on a schedule (typically weekly) and produces structured reports per monitored domain.

## Architecture: three-tier security split

Pattern adapted from `anthropics/financial-services` managed-agent-cookbooks. The split prevents prompt-injection attacks where a hostile domain could inject instructions via its llms.txt content.

```
┌─────────────────────────────────────────────────────────────┐
│ Orchestrator                                                 │
│  (system prompt from ../../agents/staleness-watcher.md)     │
│  Tools: Read, Grep, Glob, Bash, MCP (read-only)             │
│  NO Write tools.                                            │
└──┬─────────────────────┬──────────────────────┬─────────────┘
   │                     │                      │
   ↓ delegates to        ↓ delegates to         ↓ delegates to
┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ crawler      │  │ analyzer         │  │ report-writer        │
│ (Tier 1)     │  │ (Tier 2)         │  │ (Tier 3 — Write)     │
├──────────────┤  ├──────────────────┤  ├──────────────────────┤
│ Touches      │  │ Receives JSON    │  │ Receives JSON        │
│ UNTRUSTED    │  │ findings.        │  │ analysis.            │
│ HTML.        │  │ NO raw HTML.     │  │ NO raw HTML.         │
│              │  │                  │  │                      │
│ Tools:       │  │ Tools:           │  │ Tools:               │
│ Read, Grep,  │  │ Read, Grep,      │  │ Read, Write, Edit    │
│ Bash         │  │ MCP (trusted)    │  │                      │
│              │  │                  │  │ Write path constrained│
│ NO MCP       │  │ NO Write         │  │ to ./out/<domain>/   │
│ NO Write     │  │                  │  │                      │
└──────────────┘  └──────────────────┘  └──────────────────────┘
```

**Key invariants:**

1. Only the crawler touches untrusted external content (HTML fetched from arbitrary URLs)
2. The crawler has NO MCP and NO Write — its sole output is schema-validated JSON
3. The analyzer has trusted MCP access (Bing AI Performance, Profound, GitHub source-of-truth) but cannot fetch arbitrary URLs and has NO Write
4. The report-writer has Write but NO access to raw HTML and NO MCP — its writes are constrained to `./out/<domain>/` by the system prompt and by the orchestrator (which doesn't pass arbitrary paths)
5. Even if a hostile domain injects instructions into its llms.txt, those instructions can only reach the crawler — which strips them to schema-validated JSON before they reach the analyzer

## Deployment

```bash
# Set environment variables for MCP servers
export GITHUB_MCP_URL="https://..."
export BING_WEBMASTER_MCP_URL="https://..."
export PROFOUND_MCP_URL="https://..."
export TARGET_DOMAINS="example.com,foo.com,bar.com"

# Deploy via the managed-agents API
# (adapt deploy.sh from anthropics/financial-services/scripts/)
./scripts/deploy-managed-agent.sh staleness-watcher

# Schedule via cron or your orchestrator (Temporal, Airflow, etc.)
# Example: weekly Monday 9am
0 9 * * 1 curl -X POST ${AGENT_API}/v1/agents/staleness-watcher/run \
    -H "Authorization: Bearer ${API_KEY}" \
    -d '{"target_domains": ["example.com"]}'
```

## Output

For each target domain, three files in `./out/<domain>/`:

- **staleness-report-YYYY-MM-DD.md** — full report with all findings
- **summary.md** — one-line status: 🟢/🟡/🟠/🔴
- **alert.md** — only emitted if overall_severity == "red"; formatted for notification

## Severity scale (matches the canonical scale)

| Emoji | Severity | Example finding |
|---|---|---|
| 🟢 | Healthy | All links 2xx, hash matches, headers correct, recent review |
| 🟡 | Medium | Quarterly review overdue; some descriptions could be tightened |
| 🟠 | High | Some links returning 5xx (transient?); 1+ headers missing |
| 🔴 | Critical | Hash mismatch (file mutated between source and serve); broken links; missing required header |

## Threat model

Documented in `agent.yaml`. Key points:

1. **Hostile llms.txt content**: a compromised site could inject instructions into its llms.txt. The crawler is the only tier that reads this; it returns schema-validated JSON. Even if instructions slip through, they're data, not commands, when the analyzer sees them.

2. **Hostile linked URLs**: URLs in llms.txt could point to attacker-controlled domains. The crawler HEAD-checks them; it does not fetch full content of arbitrary linked URLs.

3. **Prompt injection in MCP responses**: trusted MCPs (Bing, Profound, GitHub) are assumed to return clean data. If an MCP is compromised, the analyzer's findings could be poisoned, but the report-writer's constrained output paths limit damage.

4. **Write path constraints**: report-writer's output_schema regex enforces `^./out/[A-Za-z0-9.-]+/[A-Za-z0-9.-]+\.md$` — no directory traversal, no arbitrary writes.

## Related patterns

- `agents/staleness-watcher.md` — the interactive (non-headless) version
- Pattern source: [`anthropics/financial-services` managed-agent-cookbooks](https://github.com/anthropics/financial-services/tree/main/managed-agent-cookbooks)
- Three-tier split origin: `anthropics/financial-services/managed-agent-cookbooks/gl-reconciler/`

## Cross-references

- `../../knowledge/06-deployment.md` — deployment standards being checked
- `../../knowledge/07-failure-modes.md` — anti-patterns being detected
- `../../templates/validate.sh` — local validation; this cookbook runs the equivalent headlessly
