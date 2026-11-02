---
name: financial-screenshot-to-excel
description: "Convert a screenshot or photo of financial data (statutory accounts, schedules to detailed accounts, P&L, invoices, expense breakdowns, or any tabular financial figures) into a formatted, working Excel workbook. Use this skill whenever the user uploads or pastes an image of financial figures and asks for it as a spreadsheet, table, or downloadable file, or says things like 'convert this into a table', 'put this in Excel', 'make this a spreadsheet', 'turn this screenshot into a downloadable table', or 'can you get this into Excel'. Trigger even if the user doesn't name Excel explicitly — any request to make an image of numbers editable, sortable, or usable in a spreadsheet qualifies. Always cross-check computed subtotals against the totals printed in the source image and reconcile any mismatch before delivering the file — screenshots often have a blurry or ambiguous digit, and a mismatched total is the tell."
---

# Financial screenshot to Excel

Turn an image of financial figures into an Excel workbook that reproduces the source faithfully, computes its totals with live formulas instead of copied numbers, and — critically — catches the transcription errors that screenshots are prone to before the user ever sees them.

The hard part of this task is never the openpyxl mechanics. It's that screenshots of financial tables are often slightly blurry, low-res, or have one or two digits that are genuinely ambiguous (a `3` that could be an `8`, a `6` vs a `9`). The source document already tells you the right answer, though: it prints subtotals. If your transcription is correct, your formula-computed subtotal will match the printed one exactly. If it doesn't, one of your line items is wrong, and you have enough constraints (often two: this year's total and last year's) to solve for the one figure that fixes both.

## Workflow

### 1. Read every section of the source

Look at the image(s) closely (they may already be visible in the conversation — use that rather than re-reading files unnecessarily). Transcribe:
- the document title and any company name / period heading
- every section header (e.g. "Turnover", "Cost of sales", "Administration expenses")
- every line item with its label and figure(s) — most of these schedules show two columns (current year, prior year)
- every printed subtotal or total row, and its figure(s)

If more than one screenshot is provided, treat them as one document — they're usually sequential pages of the same schedule. Preserve the order they came in.

### 2. Build the workbook, subtotals as formulas

Read the `xlsx` skill for the mechanics (openpyxl gotchas, `recalc.py`, formula compatibility, number formats) and follow it — this skill is a workflow layered on top, not a replacement.

Structure the sheet to mirror the source:
- section headers bold, on their own row
- a year header row per section (e.g. `2023 | 2022`) if the source repeats it per section — match the source's convention rather than only putting it once at the top
- line items in source order, one row each
- **subtotal rows as `=SUM(...)` formulas referencing the line items above**, never as the hardcoded number you read off the image. This is what lets step 3 catch errors, and it's also just correct practice — a workbook whose totals don't recalculate is barely better than the screenshot it came from.

Use a professional font (Arial), thousands separators, negative numbers in parentheses, and bold + a top border on total rows. If a line is genuinely blank/nil in the source, use `0` with a number format that renders it as `-` rather than leaving the cell empty (empty cells break `SUM`).

### 3. Reconcile against the source's printed totals — do this before anything else ships

Run `recalc.py` (see the note on *where* to run it, below), then load the recalculated file with `data_only=True` and compare every formula-computed subtotal to the figure printed in the source image, for every column.

**If they match:** good, move to formatting/delivery.

**If they don't match:** don't just ship the discrepancy or silently accept the printed total over your formula (that reintroduces a hardcoded, unverifiable number). Instead:
- Compute the difference for each mismatched column (`printed_total − your_sum`).
- Scan the line items in that section for the one(s) most likely misread — usually the smallest, blurriest, or most visually ambiguous figure, and note if the same line item shows a plausible mis-scan in *both* the current-year and prior-year column.
- If the same row explains the gap in every mismatched column simultaneously (as it usually will, since it's one bad transcription, not two), that's very strong evidence for the correction — solve for the value that makes every column tie exactly, and use it.
- If no single row cleanly explains all the gaps, don't guess: flag the section instead. Highlight the subtotal row (yellow fill) and add a cell comment stating the printed total and your computed total side by side, so the user can check the source themselves.
- Whenever you do correct a figure, leave a cell comment on that cell recording the original (ambiguous) reading, the corrected value, and the reasoning ("printed subtotals for both years only tie out if this figure is £3,963 rather than the ~£3,863/£3,983 the image suggests").

This reconciliation is the main value of this skill over a plain "type up what you see" transcription — always do it, even when the user seems to be in a hurry.

### 4. Where to build and recalculate — avoid the lock-file trap

Do **not** build and repeatedly recalculate the workbook directly inside the final output folder. That folder typically won't let you delete or rename files, and a LibreOffice recalculation that times out or fails leaves behind a `.~lock.<filename>#` file that will hang every subsequent recalculation attempt on a file of that name — and you can't clean it up because you can't delete from that folder.

Instead:
1. Build and iterate in a scratch/temp directory.
2. Run `recalc.py` there, as many times as you need while fixing formulas or reconciling totals.
3. Only once the file is finished, correct, and clean, copy the final `.xlsx` into the output folder the user will actually see. Never loop `recalc.py` against a copy that already lives in the output folder.

### 5. Name and deliver

Name the file after the document, e.g. `<Company Name> Schedule.xlsx` or `<Company Name> Detailed Accounts.xlsx` — read the title off the source rather than using a generic name. Present the finished file to the user with the file-sharing tool; keep the accompanying message short (what it contains, and call out explicitly if you had to correct any figure to make totals tie, so the user can double check against their own copy of the source).

## Multiple statements in one image set

If the screenshots contain genuinely distinct statements (e.g. a P&L and a separate balance sheet, or schedules for two different companies), use one worksheet tab per statement rather than stacking them all into a single sheet — it's easier to scan and matches how the source itself is usually organized (separate pages/sections with their own headers).
