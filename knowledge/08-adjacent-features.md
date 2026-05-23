# 08 — Adjacent Topic: Building LLM-Powered Features ON Your Website

*Status: Compiled May 15, 2026. A separate problem from llms.txt. Included because users adapting their website for LLMs usually have questions about both. Findings validated against primary sources.*

## When to load this file

Load this file when a user's question shifts from **external discoverability** (llms.txt, AI crawlers, AI Overviews) to **building AI features into the site itself** (chatbots, RAG, support assistants, AI-generated content).

This is a different engineering problem with a different risk surface. The empirical record on building LLM features is clearer than on llms.txt — the wins and losses are well-documented.

## Two different problems, one common framing

| Problem | Goal | This skill's primary focus |
|---|---|---|
| llms.txt | External discoverability — being found by AI agents | Yes — primary scope |
| LLM features on the website | Internal capability — answering user queries with AI | Adjacent — covered here |

Note: shipping llms.txt as **internal grounding** for your own RAG/chatbot is the bridge use case. See `04-decision-framework.md` Case 3.

## Reference architecture for LLM features on websites

For most websites, **server-side orchestration is the default right answer**. It centralizes API keys, rate limiting, caching, retrieval, moderation, observability, and policy enforcement. Browser-local inference (WebLLM, Transformers.js) is real but best for narrow privacy-first workloads.

**Core pattern**:

```
User browser
   ↓
API gateway (rate limiter, auth)
   ↓
Orchestrator (safety checks, prompt+response cache, query rewrite, routing)
   ↓
Hybrid retrieval (vector DB + metadata filters + reranker)
   ↓
Tool layer (CMS, catalog, transaction APIs — schema-validated calls)
   ↓
Model tier (fast model for median, escalation to frontier for complex)
   ↓
SSE streaming back to UI (WebSockets only for voice/co-browse)
   ↓
Tracing and eval logs (continuous evaluation)
```

For self-hosting, **vLLM is the practical serving default** — features include PagedAttention, continuous batching, chunked prefill, prefix caching, speculative decoding, and quantization.

## Model landscape (May 2026, prices verified against primary sources)

### Managed API tiers

| Provider | Model | Input / Output ($/1M tokens) | Notes |
|---|---|---|---|
| OpenAI | GPT-5.5 | $5 / $30 | 1M context, hardest reasoning |
| OpenAI | GPT-5.4 mini | $0.75 / $4.50 | Default production workhorse |
| OpenAI | GPT-5.4 nano | $0.20 / $1.25 | Routing / classification |
| Anthropic | Claude Opus 4.7 | (premium tier) | Long context, strong reasoning |
| Anthropic | Claude Haiku 4.5 | $1 / $5 | Fastest tier (200K context) |
| Google | Gemini 3.1 Pro | $2 / $12 (≤200K); $4 / $18 above | Search grounding, multimodal |
| Google | Gemini 2.5 Flash | $0.30 / $2.50 | Low-latency default |
| Google | Gemini 3.1 Flash-Lite | $0.25 / $1.50 | Scale economics |
| DeepSeek | V4-Flash | $0.14 / $0.28 | 1M context, very cheap |
| DeepSeek | V4-Pro | $0.435 / $0.87 (promo through May 31, 2026) | List $1.74 / $3.48 after |
| Mistral | Small 4 | $0.15 / $0.60 | Strong open-weight + API |
| Mistral | Medium 3.5 | $1.50 / $7.50 | Frontier tier |
| Mistral | Large 3 | $0.50 / $1.50 | Open-weight multimodal |

### Open-weight options

- **Llama 4 Scout** — 17B active, 16 experts, **10M context**, single-H100 with int4 quantization
- **Llama 4 Maverick** — 17B active, 128 experts, 1M context, natively multimodal
- **Qwen3.6** — 262K token context (base LM). Note: Qwen3 Embedding is a separate family with 8K max length — don't confuse the two.
- **Mistral Small 4 / Large 3** — credible across efficient and larger tiers
- **DeepSeek V4** — MIT-licensed open weights on Hugging Face

## Retrieval and context

- **Hybrid retrieval** (dense + sparse) outperforms purely dense for website queries that mix semantic intent with exact lexical anchors (SKUs, error codes, policy names)
- **Reranking** lifts relevance materially (Cohere Rerank, Jina, Voyage, BGE Reranker)
- **Metadata filters** enforce business constraints embeddings don't capture
- **Chunking** is still a major lever — page-based / DOM-blind chunking performs badly because navigation chrome and mixed topics pollute retrieval. Semantic or late chunking is usually better for narrative content.
- **Long context is not a substitute for retrieval.** [Lost in the Middle (Liu et al., arXiv 2307.03172)](https://arxiv.org/abs/2307.03172) shows performance is highest when relevant info is at the start or end of context and degrades significantly in the middle — regardless of context window size. Use long context for a small number of carefully selected documents, not as an excuse to skip retrieval.

## Evaluation and safety

- **Treat genAI as a systems problem, not a model demo.** OpenAI's eval guidance and Anthropic's prompt engineering docs converge on this.
- **OWASP LLM Top 10** — prompt injection, insecure output handling, model DoS, supply chain, sensitive info disclosure
- **NIST Generative AI profile** — confabulation, privacy, information integrity, human-AI configuration
- **Structured outputs for state-changing actions** — JSON schema validation on tool calls; never let free-form text trigger transactions
- **Prompt injection** — treat retrieved and user-provided text as untrusted; separate instructions from content
- **Prompt caching** — OpenAI, Anthropic, Google, and DeepSeek all support some form. OpenAI: up to 80% reduction in TTFT and 90% input cost. Keep prompt prefixes stable; isolate dynamic user content toward the end.

## Failure cases — what went wrong

These are the public failures every team building LLM features should study before launch:

### Air Canada chatbot tribunal case

**What happened**: Chatbot gave incorrect bereavement-fare guidance. Tribunal held airline liable for negligent misrepresentation.

**Outcome**: **C$812.02 in damages** (C$650.88 fare difference + C$36.14 pre-judgment interest + C$125 tribunal fees).

**Source**: [Moffatt v. Air Canada — McCarthy Tétrault analysis](https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot)

**Root cause**: No grounding to canonical policy pages. No high-risk-domain controls. Over-trust on a transactional surface.

**Lesson**: If the answer changes money / policy / eligibility, the assistant must cite source policy and escalate. Disclaimers don't transfer liability.

### NYC MyCity chatbot

**What happened**: Chatbot reportedly told businesses to break labor laws, housing-voucher rules, and cash-acceptance rules.

**Outcome**: City left it online with disclaimers initially. Incoming Mamdani administration announced removal Jan 2026.

**Source**: [The Markup original reporting, March 2024](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law). (Note: often misattributed to AP; the actual primary source is The Markup.)

**Root cause**: Legal/regulatory use case shipped without authoritative retrieval or approval workflow. Disclaimer used as substitute for control.

**Lesson**: Disclaimers do not neutralize hallucination risk in legal/compliance surfaces.

### DPD chatbot incident

**What happened**: Chatbot swore and called DPD "the worst delivery firm in the world" after a system update.

**Outcome**: DPD disabled the AI component.

**Source**: [TIME](https://time.com/6564726/ai-chatbot-dpd-curses-criticizes-company/)

**Root cause**: Insufficient adversarial testing. Weak output constraints. Poor update gating.

**Lesson**: Every prompt or model change needs red-team tests, output filters, and a rollback path.

### Klarna — the partial reversal

**Initial wins**: 2.3M conversations, 2/3 of support chats, work of 700 agents, 25% fewer repeat inquiries, <2 min vs 11 min resolution, $40M profit improvement in 2024 ([Klarna press release, Feb 2024](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/)).

**The reversal**: **Klarna later rehired humans for customer service** ([CX Dive coverage](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/)).

**Root cause**: Quality of resolution didn't hold up at scale. Over-reliance on automation degraded experience for complex cases.

**Lesson**: Headline metrics can be real and the long-term outcome can still be a partial walk-back. Plan for it. Don't optimize for "what % did the AI handle" without measuring "how satisfied were the people whose cases the AI handled."

## Success cases

| Case | Outcomes | Why it worked |
|---|---|---|
| **Vagaro / Zendesk AI** | [44% AI resolution rate, resolution time 3 hours → 23 minutes, CSAT 87% → 92% in three months](https://www.zendesk.com/customer/vagaro/) | Structured support workflows, corpus dominated by recurring answerable issues |
| **NOBULL / Zendesk AI** | [90–91% AI CSAT (vs 95% human), ~50% chat-channel resolution, ~30% cross-channel, 49% YoY ticket reduction](https://www.zendesk.com/customer/nobull/) | Brand tuning, task scoping, QA monitoring, separation of repetitive vs revenue-generating work |

**The consistent pattern**: failures happen when an unconstrained model sits behind a surface users interpret as authoritative. Successes happen when the org narrowed the task, connected the model to the right data, measured actual resolution, and preserved escalation paths.

## Bounded-scope checklist for LLM features

Before launching any AI feature on a website:

- [ ] **Domain bounded** — does the assistant know what it can and can't answer?
- [ ] **Grounded retrieval** — does it cite source pages, not invent facts?
- [ ] **Escalation path** — when does it hand off to a human or a structured tool?
- [ ] **Policy guardrails** — what queries are explicitly out of scope?
- [ ] **Output validation** — for any state-changing action, is the model output schema-validated?
- [ ] **Prompt injection defense** — are retrieved/user-provided text treated as untrusted?
- [ ] **Eval discipline** — is there a continuous-evaluation pipeline with golden datasets?
- [ ] **Monitoring** — are abandonment, escalation, CSAT, and accuracy tracked?
- [ ] **Rollback plan** — how do you disable the feature in <5 minutes if it misbehaves?
- [ ] **Liability review** — has legal reviewed for transactional / regulatory surfaces?

## How llms.txt fits with LLM features on websites

Two interactions worth understanding:

### 1. llms.txt as internal grounding map

The curated link set in your llms.txt IS the source-of-truth grounding map for your own RAG / chatbot. Use the same file:

- Crawl every URL in llms.txt → embed → store in vector DB
- The directives block becomes your system-prompt scaffolding
- The SEO routing table becomes your query → URL routing logic
- The transactional guidance becomes your handoff rules

This is "one file, two audiences" — and it's the strongest pragmatic reason to ship a high-quality llms.txt.

### 2. llms.txt as discovery surface for your AI tooling

If your llms.txt points to a hypothetical future MCP endpoint:

```markdown
**Planned / future:**
- MCP server — planned Model Context Protocol endpoint exposing venue search, quote-request, and availability tools for AI agents. Contact [URL] for partnership discussion.
```

…then external AI agents discovering your llms.txt have a path to your tools. This is the "agentic commerce" pattern — speculative as of May 2026 but the direction the ecosystem is moving.

## Open problems (May 2026)

- **Long context vs retrieval** — context windows keep growing, but retrieval-selection quality and information position still matter (Lost in the Middle)
- **Leaderboard realism** — [The Leaderboard Illusion (arXiv 2504.20879, NeurIPS 2025)](https://arxiv.org/abs/2504.20879) shows Chatbot Arena rankings are distorted by undisclosed private testing and data-access asymmetries. Run workload-specific evals on your own content.
- **Tool-use security under prompt injection** — attack surface grows as soon as the assistant can act. Schema constraints and moderation help; the security community treats this as a systems problem.

## Cross-references

- For why llms.txt as internal grounding is the strongest pragmatic case → `04-decision-framework.md` Case 3
- For implementation of LLM features as a full topic → out of scope for this skill; consider a separate skill for chatbot/RAG architecture
- For ExampleMart's planned llms-full.txt + MCP roadmap → `../case-study/example-marketplace-case.md`
