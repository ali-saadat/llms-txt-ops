# Using llms-txt-advisor from n8n

n8n is a workflow automation tool with a built-in HTTP Request node. Since the llms-txt-advisor A2A server speaks standard JSON-RPC 2.0 over HTTP, you can call it from any n8n workflow without writing code.

## What you can do

| n8n workflow | What the advisor does |
|---|---|
| Schedule (cron) → Audit my llms.txt → Email if Critical findings | Weekly audit + alert |
| Webhook (from CMS) → Generate updated llms.txt → Commit to Git | Auto-regen on content change |
| Slack slash-command → Advise → Reply in thread | `/llms-advise` in Slack |
| HubSpot ticket → Stakeholder-comms (draft email) → Pre-fill ticket | SEO support automation |

## Prerequisites

1. A running A2A server. Quickest options:
   - Local dev: `docker compose up` in the repo root, server at `http://localhost:8000`
   - Deployed: see [`../../deploy/README.md`](../../deploy/README.md) for Render/Fly/Railway one-click
2. n8n installed: [n8n.io/docs/hosting](https://docs.n8n.io/hosting/)
3. (Production only) An `A2A_API_KEYS` value from your server — needed for the Bearer auth header

## Quick start: import the example workflow

The file [`workflow-llms-txt-audit.json`](workflow-llms-txt-audit.json) is a complete n8n workflow you can import directly.

**Steps**:

1. In n8n, click **Workflows** → **Add Workflow** → **⋮ menu** → **Import from File**
2. Select `workflow-llms-txt-audit.json`
3. Open the **Set** node and change `baseUrl` to your A2A server URL
4. (Production) Open the **A2A: discover** node → Headers → set `Authorization: Bearer <your-token>`
5. Click **Execute Workflow** — you'll see the agent card, then a completed audit task

## Building from scratch — node by node

If you'd rather wire it up yourself, every A2A call is just an HTTP Request node. Here's the pattern.

### Node: A2A discover (verify the agent is up)

| Field | Value |
|---|---|
| HTTP Method | `GET` |
| URL | `{{ $json.baseUrl }}/.well-known/agent-card.json` |
| Response Format | JSON |

Use the Set node (or workflow vars) to define `baseUrl` once.

### Node: A2A message/send (the main call)

| Field | Value |
|---|---|
| HTTP Method | `POST` |
| URL | `{{ $json.baseUrl }}/a2a` |
| Send Headers | toggle on |
| Header `Content-Type` | `application/json` |
| Header `Authorization` (production only) | `Bearer {{ $env.A2A_TOKEN }}` |
| Body Content Type | JSON |
| Body | see below |

**Body** (paste this — n8n will substitute the expressions):

```json
{
  "jsonrpc": "2.0",
  "id": "{{ $itemIndex }}",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "{{ $json.userText }}"
        }
      ]
    },
    "metadata": {
      "skill": "{{ $json.skill }}"
    }
  }
}
```

The response gives you `result.artifacts[0].parts[0].text` — that's the advisor's answer. Reference it downstream as `{{ $json.result.artifacts[0].parts[0].text }}`.

### Node: A2A tasks/list (for audit/monitoring workflows)

Same shape, but `method: "tasks/list"` and `params: { "limit": 50 }`.

## Available skill IDs

Pass any of these as `metadata.skill`:

| skill | What it returns |
|---|---|
| `advise` | Decision-framework answer ("ship / skip / it depends") |
| `audit` | Severity-tagged findings against 15 anti-patterns |
| `generate` | A complete `llms.txt` file body |
| `customize` | Surgical section update (requires named target in text) |
| `deploy` | Server config + CI validation steps |
| `stakeholder-comms` | Drafted email / Jira ticket text |
| `cold-start-interview` | Profile-config interview prompts (multi-turn — n8n less ideal) |
| `setup-recommender` | One-line skill recommendation |

## Real-world examples

### Example 1: weekly audit + Slack alert

```
Cron (Mon 9:00) →
  Set { baseUrl: "https://a2a.example.com", url: "https://yoursite.com/llms.txt" } →
  HTTP Request (POST /a2a, method=message/send, skill=audit, text="{{ $json.url }}") →
  IF (response contains "Critical:") →
    Slack (channel #seo, message: "{{ $json.result.artifacts[0].parts[0].text }}")
```

The same workflow as JSON: see [`workflow-llms-txt-audit.json`](workflow-llms-txt-audit.json).

### Example 2: webhook-driven regeneration on CMS publish

```
Webhook (from your CMS, triggers on content publish) →
  HTTP Request (POST /a2a, method=message/send, skill=generate, text="<diff/context>") →
  GitHub (commit file to repo /public/llms.txt)
```

### Example 3: Slack slash-command

```
Slack Trigger (slash command /llms-advise) →
  HTTP Request (POST /a2a, method=message/send, skill=advise, text="{{ $json.text }}") →
  Slack (reply to thread with response)
```

## Auth + secrets

Put the A2A bearer token in n8n's **Credentials** as a generic **Header Auth** credential:

1. n8n → **Credentials** → New → **Header Auth**
2. Name: `A2A llms-txt-advisor`
3. Name (header): `Authorization`
4. Value: `Bearer your-token-here`

Then on every HTTP Request node, set **Authentication** → **Generic** → **Header Auth** → select the credential.

## Error handling

A2A errors come back as JSON-RPC envelopes with an `error` key:

```json
{ "jsonrpc": "2.0", "id": "1", "error": { "code": -32602, "message": "Unknown skill: foo" } }
```

In n8n: add a **Switch** node after the HTTP Request that branches on `{{ $json.error !== undefined }}` → route errors to a notification / log node.

Codes:
| Code | Meaning |
|---|---|
| -32700 | Parse error (malformed JSON sent) |
| -32600 | Invalid Request (missing jsonrpc or method) |
| -32601 | Method not found |
| -32602 | Invalid params (unknown skill, missing required field) |
| -32603 | Internal error |
| -32001 | Unauthorized (bad bearer token) — but you'll get a real 401 HTTP status |
| -32002 | Rate limited |
| -32003 | Task not found |
| -32004 | Task in terminal state |

## Streaming

n8n's HTTP Request node doesn't natively handle SSE. For streaming use cases, do one of:
1. Use `message/send` instead of `message/stream` — gets the same answer, just not chunked
2. Write a small custom n8n node that handles SSE (advanced)
3. Use the Python client (`scripts/a2a-client.py`) inside an **Execute Command** node

For most workflows, `message/send` is the right choice — the chunking matters for interactive UIs, not for batch automation.
