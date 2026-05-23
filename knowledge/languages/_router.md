# Languages Router

Map a stakeholder's primary business language to the relevant reference file. Each language file covers business email conventions, formality markers, common phrases for honesty/expectation-setting, and cultural notes specific to llms.txt advisory communication.

## Core language policy

**End-user preference always wins.** Three distinct language axes:

| Axis | Default | Override |
|---|---|---|
| **llms.txt file content** (the deployed file) | **English** | User explicit request — *"generate the file in Spanish"*, profile preference, or site is monolingual non-English |
| **Stakeholder communication** (emails, memos) | Match user's typing language | User explicit request, profile preference |
| **Conversation tone** (Claude's responses to user) | Match user's typing language | User explicit request |
| **Templates & references** (this plugin's content) | English | n/a — internal documentation stays English |

### Why the asymmetric default for the llms.txt file

- llms.txt is read by AI agents and crawlers, which overwhelmingly process English well
- English is the universal default for technical web standards (robots.txt, sitemap.xml, JSON-LD)
- Multilingual sites typically include a bilingual summary blockquote rather than translating the whole file
- For genuinely non-English sites or those serving non-English-speaking users primarily, the user can request a non-English file — but they should be explicit about it

### Why match user's typing language for conversation

- Lowest-friction experience for the user
- Respects their cultural and linguistic context
- Doesn't force the user to switch languages mid-conversation

## How language detection works in this plugin

Resolution order for each axis:

### For llms.txt file content (write/generate operations)

1. **User explicitly requested** specific language in this turn — *"draft it in French"*
2. **Project-level override** in `llms-txt-advisor.local.md` `language` field
3. **User profile setting** in `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` (`Primary language` field)
4. **Default: English** — even if site is multilingual, English is the safe default unless explicitly overridden

### For stakeholder communication (drafts of emails, memos)

1. **User explicitly specified** via `--language <code>` argument or "draft this in [language]"
2. **Match user's typing language** in the current conversation
3. **User profile setting** in `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` (`Communication language(s) for stakeholder docs` field)
4. **Project-level override** in `llms-txt-advisor.local.md`
5. **Default**: match the conversation language; fall back to English if uncertain

### For conversation tone (Claude's responses)

1. **Match user's typing language** in the current message
2. **User explicit request** if they say "respond in [language]"
3. **Default**: English

## Available language files

## Available language files

| Language | Code | Coverage |
|---|---|---|
| English | `en` | `en.md` — universal default |
| Turkish | `tr` | `tr.md` — formal `siz` form, `Hanım`/`Bey` honorifics |
| Spanish | `es` | `es.md` — formal `usted` vs informal `tú`, regional variation |
| German | `de` | `de.md` — formal `Sie` vs informal `du`, `Herr`/`Frau` honorifics |
| French | `fr` | `fr.md` — formal `vous` vs informal `tu`, `Monsieur`/`Madame` |
| Japanese | `ja` | `ja.md` — keigo system, honorific forms, kaisha context |
| Mandarin Chinese | `zh` | `zh.md` — formal vs informal address, Mainland vs Taiwan conventions |
| Arabic | `ar` | `ar.md` — RTL, formal address, regional dialects |
| Portuguese | `pt` | `pt.md` — Brazilian vs European variants |
| Italian | `it` | `it.md` — formal `Lei` form, `Signor/Signora` honorifics |
| Dutch | `nl` | `nl.md` — formal `u` vs informal `je`, generally direct tone |
| Korean | `ko` | `ko.md` — formal speech levels (`존댓말`), `님` honorific |
| Russian | `ru` | `ru.md` — formal `вы`, patronymic naming, `Уважаемый/ая` |

## Universal patterns across all languages

These apply regardless of language:

1. **Match the formality of the conversation thread.** If colleagues are using first names casually, match. If everyone uses honorifics, use honorifics.
2. **Technical terms stay in English.** UTF-8, SHA-256, Jira, MCP, llms.txt, robots.txt, schema.org — these are international standards and don't translate.
3. **Cite empirical evidence in original language.** When citing the SE Ranking study or Mueller statements, reference them in English (with translation if helpful) — these are the original sources.
4. **Use the language's natural business closing.** "Best Regards" ≠ "Saygılarımla" ≠ "Mit freundlichen Grüßen" ≠ "敬具" — pick the one that matches local convention.
5. **Don't translate names.** "the SEO Lead" stays "the SEO Lead" regardless of email language.
6. **Numeric / date formats follow locale.** 2026-05-15 in English, 15.05.2026 in German, 15/05/2026 in French, 2026年5月15日 in Japanese.

## When the user's language isn't in the list

1. Use English as the lingua franca for stakeholder communication
2. Note in the practice profile that this language isn't yet covered
3. Apply universal patterns above
4. Offer to draft in English with translation notes

To add a new language file, follow the template pattern from `es.md` or any other existing language file. PRs welcome.

## Cross-references

- `../../stakeholder/email-templates-en.md` — full English email templates
- `../../stakeholder/email-templates-tr.md` — full Turkish email templates
- `../../stakeholder/expectations.md` — framing language (language-agnostic core)
- `../../skills/stakeholder-comms/SKILL.md` — the skill that uses these files
