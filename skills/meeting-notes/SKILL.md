---
name: meeting-notes
description: "Turn meeting transcripts into clean summaries with action items and deadlines. Use this skill when the user says \"meeting notes\", \"summarize this meeting\", \"action items\", \"what did we decide\", \"process this transcript\", \"meeting summary\", or pastes a block of transcript text and wants it organized into notes.\n"
---

# Meeting Notes → Action Items

You turn raw meeting transcripts into clean, organized notes with clear action items. The goal: everyone who attended (or didn't) knows exactly what was discussed, what was decided, and who needs to do what by when.

## Input

Accept any of these formats:
- Raw transcript text (pasted directly)
- Otter.ai / Fireflies / other transcription tool output
- The user's own messy notes from a meeting
- Audio file summary or dictation

If the input is messy or unclear, do your best. Flag anything you're unsure about with [UNCLEAR] so the user can fill in gaps.

## Output Structure

```
# 📝 Meeting Notes — [Meeting Title]

**Date:** [Date]
**Attendees:** [Names, if mentioned]
**Duration:** [Approximate, if determinable]

---

## Summary
[3-4 sentences. What was this meeting about? What was the main outcome?]

## Key Decisions
- ✅ [Decision 1 — what was agreed on]
- ✅ [Decision 2 — what was agreed on]
- ✅ [Decision 3 — what was agreed on]

## Discussion Points
### [Topic 1]
[Brief summary of what was discussed and any conclusions]

### [Topic 2]
[Brief summary of what was discussed and any conclusions]

### [Topic 3]
[Brief summary of what was discussed and any conclusions]

## Action Items
| Who | What | Due |
|-----|------|-----|
| [Name] | [Task description] | [Date] |
| [Name] | [Task description] | [Date] |
| [Name] | [Task description] | [Date] |

## Open Questions
- ❓ [Anything unresolved that needs follow-up]
- ❓ [Anything that was tabled for later]

## Next Meeting
[Date/time if mentioned, or "TBD"]
```

## Rules

- Be specific with action items. "Follow up on the proposal" is bad. "Send revised proposal to Sarah with updated pricing by Friday" is good.
- Attribute action items to specific people whenever possible. If names aren't clear from the transcript, use role descriptions (e.g., "the designer", "the project lead").
- For deadlines: if an exact date was mentioned, use it. If someone said "by end of week" or "next Tuesday", calculate the actual date.
- Keep discussion summaries brief. 2-3 sentences per topic maximum. The user was in the meeting — they don't need a recap of every word.
- If the meeting had no clear decisions or action items, say so explicitly. Don't invent them.
- Separate facts from opinions. If someone expressed a preference vs. made a decision, note the difference.
