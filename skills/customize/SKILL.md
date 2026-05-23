---
name: customize
description: >
  Update a specific section of the user's practice profile or an existing
  llms.txt file. Use when the user wants to refine without re-running the full
  cold-start interview — and they name what to update. Triggers require a
  TARGET section: "update the SEO routing", "add more cities to the city
  list", "fix the directives block", "tweak the transactional guidance",
  "change one URL in [section]", or any surgical change with a named target.
  Faster than re-running cold-start; more targeted than regenerating from
  scratch. **Ambiguity policy**: bare verbs without a target ("update my
  llms.txt", "change it", "fix it", "modify the file") do NOT route here —
  they should go to `advise` for disambiguation (or `audit` if the user
  wants a review of what should change). Use customize only when the user
  has named a specific section or URL to update.
argument-hint: "[--section <name>] [--profile to update the profile] [--file to update an llms.txt file directly]"
---

# Customize — Targeted Updates to Profile or File

## Step 1 — Determine target

Ask the user (or infer from argument flags):

| What | Argument | Action |
|---|---|---|
| Profile section | `--profile --section <name>` | Update `~/.claude/plugins/config/llms-txt-advisor/CLAUDE.md` |
| File section | `--file --section <name>` | Edit the user's deployed llms.txt directly |
| Either | (no flag) | Ask the user which |

Valid `--section` values for the profile (from cold-start interview parts):
- `identity`, `goals`, `existing-state`, `stack`, `ia`, `schema`, `seo-context`, `deployment`, `outputs`, `stakeholder`

Valid `--section` values for the file:
- `directives` (the `## For AI Systems` block)
- `seo-routing`, `priority-hierarchy`, `transactional-guidance`, `schema-disclosure`
- `intent-router`, `entity-facts`
- Any other section name from the file's H2 headings

## Step 2 — Load current state

For profile updates: read the user-config CLAUDE.md.
For file updates: read the file from disk or fetch from URL.

## Step 3 — Targeted interview

Run ONLY the questions relevant to the target section. Same pacing rules as cold-start (max 2-3 questions per turn).

### Examples by section

**`--section seo-routing`**: ask for new query → URL mappings the user wants to add. Show current mappings, ask which to keep / update / add. Re-emit the section.

**`--section ia`**: ask which categories to add / remove / reorder. Show current list, get changes.

**`--section directives`**: ask which directives to add / modify (freshness, pricing, local-intent, legal routing, brand resolution, file metadata).

**`--section schema-disclosure`**: ask for newly-shipped schema types or removals.

**`--section deployment`**: confirm any infrastructure changes (CDN switch, new hosting platform, etc.).

## Step 4 — Apply changes

For profile: edit the user-config CLAUDE.md, preserve all other sections, update the `Last reviewed` date.

For file: produce the updated section, ask the user to confirm before writing to disk. If writing, also update the file's `last-reviewed` metadata.

## Step 5 — Validate and offer next steps

After any change, run the relevant checks from `knowledge/06-deployment.md`:

- If file was modified: run `templates/validate.sh` (size, encoding, links, spec shape)
- If profile was modified: confirm no `[PLACEHOLDER]` markers were reintroduced

Offer:

> "Section updated. Want me to:
> 1. Apply this change to other places (e.g., regenerate the deployed file with the new profile value)? → `/llms-txt-advisor:generate`
> 2. Update the deployment / robots.txt to match? → `/llms-txt-advisor:deploy`
> 3. Stop here, you're done."

## Guardrails

- **Preserve unchanged sections exactly.** Don't accidentally reformat or modify sections the user didn't ask about.
- **Never introduce new `[PLACEHOLDER]` markers.** If the user removes content, leave a `[PENDING]` instead (semantically distinct — placeholder = never filled; pending = explicitly deferred).
- **Backup before file modifications.** Save the prior version to `.bak.YYYYMMDD` extension.
- **Confirm before destructive changes.** "I'm removing the SEO routing block entirely — confirmed?"

## Cross-references

- `knowledge/05-implementation.md` — section-by-section structure
- `knowledge/03-seo-perspective.md` — SEO integration layer specifics
- `templates/validate.sh` — post-change validation
