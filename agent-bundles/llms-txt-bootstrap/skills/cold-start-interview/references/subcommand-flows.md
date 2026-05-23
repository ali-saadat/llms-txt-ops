# Subcommand Flows

*Detailed handling of cold-start-interview subcommand flags. Load when the user passes any of these flags.*

## `--quick` — 2-minute path

Run only:
- Part 0 (Site identity — questions 1-3 only)
- Part 1 (Goals — questions 1-2 only; if goal is "AI visibility", invoke the honest-expectations script anyway)
- Part 4 (IA — minimal version: just the top 5-10 most important pages)
- Part 7 (Deployment — confirm the defaults block, no questions)

Skip:
- Part 3 (Stack details)
- Part 5 (Schema)
- Part 6 (SEO context)
- Part 8 (Outputs preferences)
- Part 9 (Stakeholder communication)

Mark all skipped sections with `[PENDING — refine later with /llms-txt-advisor:customize]`.

Estimated time: 2 minutes.

## `--full` — 15-20 minute path

Run every part. No shortcuts. This is the default if no flag is specified.

## `--redo` — Re-run on already-configured profile

1. Read existing `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md`
2. Back up to `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md.bak.YYYYMMDD-HHMMSS`
3. Confirm with user: "This will overwrite your existing profile. The current file has been backed up to `[path]`. Proceed?"
4. On yes, proceed with full or quick path depending on additional flag
5. On no, abort and tell user the backup is in place if they want to manually edit

## `--section <name>` — Re-run only one section

Valid section names:
- `identity` (Part 0)
- `goals` (Part 1)
- `existing-state` (Part 2)
- `stack` (Part 3)
- `ia` (Part 4)
- `schema` (Part 5)
- `seo-context` (Part 6)
- `deployment` (Part 7)
- `outputs` (Part 8)
- `stakeholder` (Part 9)

Flow:
1. Read existing profile
2. Display the current values for the named section
3. Ask: "Update this section? (Type 'edit' to step through questions, or paste new content directly)"
4. If 'edit', step through that section's questions only
5. If paste, validate and merge
6. Update profile with timestamp

If the named section doesn't exist (typo), list valid section names and abort.

## `--check-integrations` — Re-probe MCP / data sources only

Skip the interview entirely. Just check:

1. **Sitemap.xml reachable** — HEAD request to the URL in profile. Update status.
2. **robots.txt reachable** — HEAD request. Update status.
3. **Existing llms.txt reachable** (if profile has one configured) — HEAD request. Note size, content-type.
4. **MCP connectors available** — call list_tools() or equivalent. Update the integrations table in profile.
5. **Bing Webmaster Tools** — ask the user (can't auto-probe).
6. **GA / Plausible / Adobe Analytics** — ask the user.

Update only the integrations-related sections of the profile. Don't touch any other section.

Output: a summary of what changed and what's now reachable vs. unreachable.

## `--language <code>` — Override language for this interview session

Use the language file at `../../knowledge/languages/<code>.md` for:
- Greeting and pacing language
- Honest-expectations script translation
- Stakeholder communication preferences default

Doesn't change the language of any artifacts that aren't directly user-facing in the interview.

## Combination patterns

| Combination | Meaning |
|---|---|
| `--quick --section ia` | Update IA section in 2-min mode |
| `--redo --quick` | Backup + re-run in quick mode |
| `--full --language tr` | Full interview in Turkish |
| `--section seo-context --language es` | Update SEO context section in Spanish |
| `--check-integrations` (any other flag ignored) | Just re-probe |

## Pause / resume

If the user says "let me come back to this" or doesn't answer a key question after one re-prompt:

1. Write a `[PENDING — answer this question to complete profile]` marker for the unanswered field
2. Add `<!-- SETUP PAUSED AT: [section name] -->` HTML comment at the top of the file
3. Save the profile as-is
4. Tell the user: "Saved your progress. When you're ready to resume, run `/llms-txt-advisor:cold-start-interview` again — I'll pick up where we left off."

On next invocation, detect the paused marker and resume from that section.

## Already-configured detection

If the profile exists, has no `[PLACEHOLDER]` markers, and no `[PENDING]` markers, and no paused marker, then the profile is fully configured. Behavior:

- Without `--redo`: announce "Your profile is configured. Use `--redo` to re-run from scratch, `--section <name>` to update specific sections, or just proceed with `/llms-txt-advisor:advise`."
- With `--redo`: proceed with backup + re-run.

## Cross-references

- `../SKILL.md` — main flow
- `sector-question-banks.md` — for Part 4 details per sector
- `honest-expectations-script.md` — for Part 1 honest-expectations conversation
