---
name: board-pack-action-tracker
description: Consolidate a Tern Capital portfolio company's board pack(s) (PDF, pptx, or xlsx) and related Notion notes (EOS/L10 appendices, account plans, etc.) into a single formatted Excel action tracker with Outstanding Actions, Removed (BAU) Actions, Completed Actions, Decisions Made, and Minutes & Context tabs. Use this whenever the user uploads or references a board pack, board meeting notes, or L10/EOS notes and wants a table, tracker, or summary of actions/decisions/minutes built from it - even if they don't use the words "action tracker" - e.g. "pull together the actions from this board meeting", "what came out of the CADS/RMS/SIL board pack", "build me a table of outstanding actions", or "turn the board pack and my Notion notes into a spreadsheet". Also use this to revise a tracker the skill already produced once the user has reviewed it and marked up which actions to exclude or merge.
---

# Board Pack Action Tracker

Turns a portfolio company's board pack(s) plus supporting Notion notes into one
Excel workbook the user can hand to the board or push into Smartsheet. This
mirrors a workflow developed interactively for Tern Capital's CADS, RMS, and
SIL board reviews, but the same steps apply to any portfolio company.

## Overview of the workflow

1. **Read every source** - board pack(s) and any Notion pages the user
   references or that you can find (EOS/L10 appendices, account plans, Rocks,
   etc. are often buried in draft Notion docs but contain genuine dated,
   owned actions - don't skip them just because the page looks informal).
2. **Extract** four categories of content: Outstanding Actions, Completed
   Actions, Decisions Made, and Minutes & Context (see "What goes where"
   below).
3. **Apply the default assumptions** (see below) to fill gaps - and
   record every assumption you made in an "Assumptions" tab so the user can
   see and challenge them.
4. **Filter and consolidate** the Outstanding Actions list so the board only
   sees board-level items (see "BAU filtering and consolidation").
5. **Build the workbook** using `scripts/build_tracker.py` (see "Building the
   workbook").
6. **Flag anything you weren't sure about** in your reply - don't silently
   guess on judgment calls that materially change what the board sees.

## What goes where

- **Outstanding Actions**: `Action | Business | VC Pillar | Owner | Deadline`.
  Anything still open, with a named or inferable owner and deadline.
- **Removed Actions**: same columns plus `Reason for removal`. Everything
  filtered out of Outstanding Actions in step 4 lands here, not in the
  ether - the user needs to be able to audit and reverse any call you made.
- **Completed Actions**: `Action | Business | VC Pillar`. Things explicitly
  described as done, launched, resolved, agreed, or won since the last board
  meeting.
- **Decisions Made**: `Decision | Business | Detail`. Board-level calls -
  approvals, sign-offs, strategic choices - distinct from actions someone
  still has to go and do.
- **Minutes & Context**: `Source | Category | Note`. Narrative discussion and
  KPI/financial context that isn't itself an action or decision, grouped by
  which meeting or board pack it came from (e.g. "RMS + SIL Board Meeting
  (16/07/2026)", "CADS Board Pack - KPIs / Financials (context, not
  actioned)"). Keep each note short and in your own words rather than
  reproducing pack text at length.

"VC Pillar" refers to the value-creation pillar the action sits under -
typically Sales Effectiveness, Talent, Financial Rigour, Technology, or
Systems & Processes. Infer it from context if the pack doesn't label it
explicitly.

## Default assumptions

Use these only where the source material doesn't give something more
specific, and always list them on the Assumptions tab:

- **Default deadline**, when no real one is stated: two weeks from today.
- **Default owners**, used only when no more specific person is named in the
  source: ask the user once per portfolio company if you don't already know
  (e.g. from earlier in the conversation or from memory), rather than
  guessing - getting an owner wrong is worse than leaving it blank.
- **Same-day conflicts**: if a board pack and the meeting notes from the same
  day disagree (e.g. the pack says a project is proceeding but the minutes
  say it was paused in the meeting), treat the meeting notes as the newer,
  more authoritative source.
- **"Next board meeting" placeholder date**: several actions are often
  phrased as "update the board next time" rather than having their own
  deadline. Look across the pack for a recurring near-term date used for
  several unrelated items in this way (it's usually the date of the next
  scheduled board meeting) and use that consistently, rather than inventing
  separate dates for each.

## BAU filtering and consolidation

Boards don't want to see routine day-to-day running of the business - only
items that are strategically material, at risk, or require a board-level
decision or awareness. Use judgment, not a fixed keyword list, but here's the
distinction that matters:

**Keep as a board-level Outstanding Action** if it involves: material
financial value or risk, a named strategic decision or trade-off, headcount
or organisational restructuring, a systemic technology/process issue (a
platform migration, a system outage, a compliance certification), an account
flagged as at risk with a live escalation, or a multi-quarter initiative.

**Move to Removed Actions as BAU** if it's a routine, single-step, business-
as-usual task that any competent operator would just do without board
oversight - chasing a single PO or overdue invoice, following up a single
support ticket or bug fix, a routine sales follow-up call, a minor product
release step, or small admin/logistics housekeeping. Write a short, honest
reason for each (e.g. "BAU action - not a high level board action in a
material area of the business.").

**Consolidate rather than exclude** when several outstanding actions are
really sub-steps of one initiative (a single account's engagement plan, a
sequence of product release milestones, a headcount/restructure process that
spans two related actions). Rather than listing each sub-step separately,
create one Outstanding Action along the lines of "Provide an update on
[initiative] at the next board meeting", assign it to the initiative's overall
owner, and set its deadline to the next-board-meeting date. Move all the
original sub-step rows into Removed Actions with a reason noting what they
were merged into, so the detail isn't lost, just tidied up for the board view.

When a call is genuinely borderline, it's fine to keep it in Outstanding
Actions and mention in your reply that you weren't certain - that's better
than silently guessing wrong on something the board will read.

## Building the workbook

Assemble your extracted data into the JSON schema documented at the top of
`scripts/build_tracker.py`, write it to a temp file, then run:

```bash
python scripts/build_tracker.py data.json /mnt/user-data/outputs/<Company>_Board_Actions_Decisions_Minutes.xlsx
```

The script handles all styling (bold white-on-navy headers, per-business
colour coding, frozen header row, autofilter, column widths) so you don't
need to write openpyxl code by hand - just populate the JSON accurately.
Business colours are assigned automatically in first-seen order, so it works
for any portfolio company name, not just CADS/RMS/SIL.

After saving, present the file with `present_files` and give a short summary
of the counts (outstanding / removed / completed / decisions) rather than
repeating the whole table in chat - the user can inspect it in the workbook.

## Revising a tracker after user markup

Sometimes the user comes back with the workbook you produced, having added a
column of exclude/merge/keep notes (typically column F on the Outstanding
Actions tab) after reviewing it. When this happens:

1. Read the annotated file and treat the note column as authoritative -
   it overrides your own BAU/consolidation judgment from the first pass.
2. "Exclude" notes move that row to Removed Actions with the reason taken
   from (or lightly cleaned up from) their note.
3. "Merge with row X" / "merge these into one action" notes: consolidate the
   named rows into a single new Outstanding Action. If one row's note gives
   explicit replacement text (e.g. "change this to provide an update on
   X"), use that as the new action's text; otherwise write a sensible
   consolidated action yourself and say so in your reply so the user can
   correct the wording if needed.
4. Rebuild the workbook with `scripts/build_tracker.py` as before, keeping
   Completed Actions / Decisions Made / Minutes & Context unchanged unless the
   user also marked those up.
5. Mention any merge where you had to pick which row's owner/deadline/pillar
   to keep, since that's a judgment call worth a second pair of eyes.
