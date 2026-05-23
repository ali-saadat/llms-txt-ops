# Role-Based Workflow Recommendations

*Detailed workflow recommendations by user role. Load when `/setup-recommender` needs to recommend a sequence of skills.*

## Engineer

**Typical context**: Wants to ship something concrete; values clear technical steps; wants minimal handholding.

**Recommended workflow**:

```
1. /llms-txt-advisor:cold-start-interview --quick     (2 min — get the basics)
2. /llms-txt-advisor:audit                            (if existing file)
   OR
   /llms-txt-advisor:generate                         (if from scratch)
3. /llms-txt-advisor:deploy --ticket                  (Jira-ready spec)
4. (deploy + verify)
5. /llms-txt-advisor:advise                           (only if specific questions arise)
```

**Skip for engineers (usually):**
- Long stakeholder-comms drafting (engineer can write their own ticket)
- Detailed audit unless replacing an existing file
- Deep cold-start (quick path usually sufficient)

## SEO specialist

**Typical context**: Wants tailored SEO routing + decision framework; cares about empirical evidence; needs to defend decisions to stakeholders.

**Recommended workflow**:

```
1. /llms-txt-advisor:advise                           (decision framework discussion first)
2. /llms-txt-advisor:cold-start-interview --full      (15-20 min — proper SEO integration)
3. /llms-txt-advisor:audit                            (if existing file)
4. /llms-txt-advisor:generate                         (with full SEO layer)
5. /llms-txt-advisor:stakeholder-comms                (draft framing for team)
```

**Why this order**: SEO experts want to engage with the empirical record first before committing to ship. The honest-expectations conversation matters most here.

## Product manager / Engineering manager

**Typical context**: Coordinates across teams; needs Jira-ready outputs; cares about stakeholder alignment.

**Recommended workflow**:

```
1. /llms-txt-advisor:advise                           (decision context)
2. /llms-txt-advisor:cold-start-interview --quick     (2 min — get oriented)
3. /llms-txt-advisor:stakeholder-comms                (draft initial recommendation email)
4. (delegate cold-start --full to engineer / SEO)
5. /llms-txt-advisor:deploy --ticket                  (when ready to execute)
```

## Leadership / executive

**Typical context**: Decides yes/no, doesn't execute; needs concise summary; cares about cost / risk / strategic fit.

**Recommended workflow**:

```
1. /llms-txt-advisor:advise                           (5-min decision conversation)
2. /llms-txt-advisor:stakeholder-comms --type status-update  (concise written summary)
3. (delegate execution to engineering / SEO)
```

**Skip entirely**:
- Cold-start interview (too granular for leadership)
- Audit / generate / deploy (execution roles)

## Small business owner

**Typical context**: Wears many hats; limited engineering capacity; needs realistic recommendations.

**Recommended workflow**:

```
1. /llms-txt-advisor:advise                           (likely answer is "skip, invest here instead")
2. If skipping: /llms-txt-advisor:stakeholder-comms   (recommendation memo)
   If proceeding: /llms-txt-advisor:cold-start-interview --quick + /generate
```

**Important**: be especially honest with small business owners about ROI. They have less engineering capacity to spare on null-leverage investments.

## Consultant advising a client

**Typical context**: Working on behalf of someone else's site; needs to produce client-deliverable artifacts; may be on a fixed scope.

**Recommended workflow**:

```
1. /llms-txt-advisor:cold-start-interview --full      (capture client profile carefully)
2. (Create llms-txt-advisor.local.md in client repo for project-scoped overrides)
3. /llms-txt-advisor:audit                            (assess client's current state)
4. /llms-txt-advisor:generate                         (produce v1 for client review)
5. /llms-txt-advisor:deploy --ticket                  (handoff spec for client's eng team)
6. /llms-txt-advisor:stakeholder-comms                (draft handoff email to client)
```

**Tips for consultants**:
- Document everything in the project-level local override file
- Set realistic expectations with the client upfront (the honest-expectations conversation is for THEM, not just you)
- Provide the deployment spec as a deliverable they can hand to their team

## Developer Relations / DX team

**Typical context**: Has dev-docs site; wants the file optimized for coding-agent users (Cursor, Claude Code).

**Recommended workflow**:

```
1. /llms-txt-advisor:cold-start-interview --full      (capture API surface details)
2. /llms-txt-advisor:audit                            (if Mintlify/Fern auto-gen is in place)
3. /llms-txt-advisor:generate                         (with dev-docs template)
4. (Consider also building llms-full.txt — concatenated full markdown)
5. /llms-txt-advisor:deploy
6. Set up monitoring for Cursor / Claude Code user-agent fetches
```

**This is the highest-value use case** per the empirical record. Expect real usage.

## Mixed / unsure role

If the user can't easily classify their role:

```
1. /llms-txt-advisor:advise --quick                   (3-question triage)
2. /llms-txt-advisor:cold-start-interview --quick     (2-min config)
3. (follow up based on what came up)
```

## Workflow modifiers

### "I'm in a hurry"

Compress to:
```
1. /llms-txt-advisor:setup-recommender --quick        (60 seconds)
2. /llms-txt-advisor:cold-start-interview --quick     (2 minutes)
3. /llms-txt-advisor:generate                         (immediate output)
```

### "I want to do this thoroughly"

Expand to:
```
1. /llms-txt-advisor:setup-recommender                (full triage)
2. /llms-txt-advisor:advise                           (decision discussion)
3. /llms-txt-advisor:cold-start-interview --full      (15-20 min)
4. Read knowledge/04-decision-framework.md + knowledge/sectors/<type>.md
5. /llms-txt-advisor:audit                            (if existing file)
6. /llms-txt-advisor:generate
7. /llms-txt-advisor:deploy --ticket
8. /llms-txt-advisor:stakeholder-comms
9. Set up staleness-watcher for ongoing monitoring
```

### "I'm not sure if we even need this"

```
1. /llms-txt-advisor:advise                           (decision framework, may end here with "skip")
```

If the answer is "skip", produce a recommendation memo. The user may not need any other skill.

## Cross-references

- `../SKILL.md` — main flow
- `../../advise/SKILL.md` — decision discussions
- `../../cold-start-interview/SKILL.md` — configuration
- `../../../README.md` — full skill catalog
