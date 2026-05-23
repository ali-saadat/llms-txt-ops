# Email-by-Email Walkthrough

*Detailed scenario-specific guidance for drafting each email type. Load when the user invokes `/stakeholder-comms` with a specific scenario.*

## Initial recommendation email

**When to use**: First time pitching llms.txt work to a manager / team.

**Structure**:
1. Open with appreciation for being asked / trust
2. Brief problem statement (one paragraph max)
3. Comparison table (current state vs proposed)
4. What this unlocks (real benefits, not AI traffic)
5. Honest expectations preview (one paragraph)
6. Concrete next steps

**Key elements that must be present**:
- Brief honest framing of empirical record
- Three real reasons that survive scrutiny
- Cost / effort estimate
- Specific next-step request (approve to proceed, open Jira ticket, etc.)

**Length target**: ~300-500 words. Avoid walls of text in initial communication.

**Example opener** (from ExampleMart case):
> "First — genuine thanks for bringing me into this. The fact that [Site] already ships an llms.txt at all puts you ahead of roughly 90% of sites worldwide, and the instinct to question whether 'longer is better' is exactly the right one. Most teams never get that far."

This achieves: gratitude, framing the current state as already-good-but-improvable, validating the manager's instinct.

## Follow-up after feedback

**When to use**: After receiving multiple feedback sets (SEO review + manager questions), responding to all.

**Structure**:
1. Open thanking each stakeholder by name + their specific contribution
2. Address the most detailed feedback first (usually SEO)
3. Answer structural questions (usually from manager)
4. Surface "beyond what was asked" benefits
5. Honest expectations section
6. Concrete next steps
7. Close with offer to discuss

**Key elements that must be present**:
- Point-by-point response to each feedback item
- Explicit "what I'm adding beyond your suggestion" notes
- The three-reasons framing for the honest section
- Specific next-step ownership (who does what when)

**Length target**: Longer is OK here — ~1000-2000 words. Stakeholders gave detailed feedback; matching depth respects that.

**Critical**: never skip the honest-expectations section even in follow-up. Stakeholders need consistent framing across emails.

## Encoding-issue / quality dispute response

**When to use**: SEO expert or stakeholder reports corruption / quality issue you can't reproduce.

**Structure**:
1. Open with explicit appreciation for the specific examples shared
2. List the verification steps performed (table format)
3. Conclusion based on the verification
4. Most likely explanation if your verification disagrees with their observation
5. Defensive measures added regardless
6. Offer to verify together (screen share)
7. Close with continued thanks

**Key elements**:
- Never make them feel wrong
- Always validate that their observation was real (the issue, not the diagnosis)
- Add defensive measures regardless of where the diagnosis lands
- Offer collaboration to verify

**Tone**: extremely careful. The risk is making the reporter feel dismissed.

**Template structure** (from ExampleMart case Template 3):
> "Thank you for the careful review and the specific examples — that lets us run a real verification. We took your concern seriously and ran [N] independent checks: [findings table]. Our conclusion: [findings]. The likely root cause is [display/transit layer], not the source file. To prevent this from being ambiguous again, we're adding [defensive measures]. If you'd like to verify together, I'm happy to do a quick screen share..."

## Pushback response (skeptical stakeholder)

**When to use**: Stakeholder dismisses llms.txt entirely; you need to defend a narrow case.

**Structure**:
1. Partial agreement (yes, not a citation lever)
2. The three real reasons survive scrutiny
3. Specific application to this site
4. Cost / risk
5. Offer to skip if they prefer

**Key elements**:
- Lead with agreement, not disagreement
- Concrete reasons specific to their situation
- Don't oversell

**Example**:
> "I agree it's not a citation lever — the studies are clear. But for our specific site: [reason 1 specific to them], [reason 2], [reason 3]. Cost is a half-day. Risk is zero. If you'd rather skip, I'll write the recommendation memo with the higher-leverage alternatives. Your call."

## Pushback response (over-believer stakeholder)

**When to use**: Stakeholder believes llms.txt will drive AI traffic; you need to redirect.

**Structure**:
1. Validate the goal (they want AI visibility — legitimate)
2. Present empirical evidence honestly
3. Higher-leverage alternatives (the GEO toolkit)
4. What llms.txt CAN do (the three real reasons)
5. Offer to ship for the right reasons

**Key elements**:
- Don't make them feel naive
- Show, don't tell — cite specific studies with numbers
- Redirect to higher-leverage investments
- Leave the door open for llms.txt as a smaller, honest bet

## Status update to leadership

**When to use**: Periodic project update.

**Structure**:
1. Bullet status (concrete, no padding)
2. Honest expectations restated
3. No action needed flag (or specific asks)

**Length target**: ~150-300 words. Brevity respects executive time.

**Example**:
```
Quick status on llms.txt:

- Current file (12.5 MB, 43k links) replaced with curated v3 (27.8 KB, 153 links). Same coverage via URL patterns; 600× smaller.
- SEO team review integrated — six structural improvements.
- Deployment spec ready for engineering to open Jira ticket.
- CI validation script in place.

Honest expectations: this doesn't drive measurable AI citations. The wins are (1) fixing the broken current file, (2) the file doubles as internal grounding for our future RAG/chatbot work, (3) forward-compatibility with the IETF AIPREF standardization path.

No action needed from you — flagging for visibility.
```

## Vendor pushback (vendor pitching AI optimization service)

**When to use**: External vendor reaches out claiming they can optimize your llms.txt for AI citation lift.

**Structure**:
1. Polite acknowledgment of outreach
2. State the empirical baseline you operate from
3. Ask for their evidence base
4. Distinguish vendor anecdotes from controlled studies
5. Open to engagement if their evidence holds up

**Tone**: neither rude nor credulous. Vendors deserve a fair hearing; evidence deserves scrutiny.

**Example**:
> "Appreciate the outreach. Before we engage on AI-search optimization, I want to understand the empirical basis for your approach. The independent studies I'm aware of (SE Ranking n=300k, OtterlyAI 90-day logs, Search Engine Land 10-site test) all found no measurable AI-citation lift from llms.txt. What's the evidence base your optimization is built on? If you have controlled studies with statistical methodology, I'd be very interested. If your evidence is vendor case studies or anecdotal, that's worth knowing too — I'd want to factor it differently."

## Internal Q&A (FAQ for the team)

**When to use**: Team asks "what's the deal with this llms.txt thing"; you produce a one-pager.

**Structure**:
- Q&A format
- Anticipate common questions
- Link out to detailed knowledge files

**Typical Q&As to include**:
- "What is llms.txt?"
- "Why are we shipping it?"
- "Does it actually drive AI traffic?"
- "Why aren't we doing X (schema, content, etc.) instead?"
- "How do we measure success?"
- "What happens if we don't ship it?"
- "How do we maintain it?"

**Length target**: 1-2 pages.

## Cross-cultural considerations

For Turkish, Japanese, Arabic, etc. — load the appropriate language file from `../../../knowledge/languages/<code>.md` for tone and convention rules. Specifically:

- **Turkish**: formal `siz` form throughout; `the SEO Lead` / `the Sponsor` honorifics; `Saygılarımla` closing
- **Japanese**: keigo polite-to-formal levels; `さん` honorific; standard `お世話になっております` opening; `何卒よろしくお願いいたします` closing
- **German**: formal `Sie` form (unless du-Kultur is established); `Sehr geehrte/r Herr/Frau` opening; `Mit freundlichen Grüßen` closing
- **Arabic**: RTL formatting; honorifics like `الأستاذ` / `الدكتور` / `المهندس`; consider religious-secular calibration

## Cross-references

- `../SKILL.md` — main flow
- `../../../stakeholder/expectations.md` — framing language by camp
- `../../../stakeholder/email-templates-en.md` — full English templates
- `../../../stakeholder/email-templates-tr.md` — full Turkish templates
- `../../../knowledge/languages/<code>.md` — per-language conventions
- `../../../case-study/example-marketplace-case.md` — worked example with Turkish and English emails
