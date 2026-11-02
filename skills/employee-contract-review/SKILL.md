---
name: employee-contract-review
description: >
  Review a target company's employee contracts for buy-side due diligence and populate the user's
  employee-contract-review template (Excel) with one row per employee. Use whenever the user
  provides a folder of employment documents for a deal plus a review template and asks to "review
  the employee contracts", "fill in the contract review template", "do the employee contract
  review", "go through these contracts", or "build the contract review spreadsheet". Handles
  statements of main terms, apprenticeship agreements, variation/appraisal letters,
  obligations/restrictive-covenant addenda, and leaver documents — consolidating all of an
  employee's documents into their single row. Works for any Tern Capital deal. Documents are
  usually scanned and redacted PDFs, so OCR and visual signature checking are built in. Adapts to
  whatever columns the template contains. Output is the user's template, populated, saved to the
  deal folder.
---

# Employee Contract Review

Reads a target's employment documents and fills in the user's contract-review template — **one row
per employee, one column per review field** — for buy-side due diligence. Developed interactively
on a real Tern deal (a primary-care software target), but the steps apply to any deal.

## Core context — get this right first

This is buy-side DD on an acquisition target. "We" are the buyer, reading each contract from the
**employer's** perspective (what the target company owes and is bound by, and what protects it).
The employer is the target; the counterparties are its employees.

Two framing rules that shape everything:

- **One row per employee, not per document.** An employee typically has several documents — a main
  contract, one or more variation letters, an obligations/restrictive-covenant addendum, and
  sometimes leaver documents. Read them **together** and consolidate into that employee's single
  row. File names almost always make the mapping obvious (e.g. "…Employee 7…").
- **Preserve what's pre-filled.** The template usually already has the employee list (Name) and the
  Dataroom Ref filled in. Never overwrite these — populate the empty review columns only.

Handle these edge cases explicitly (confirm with the user only if genuinely ambiguous):

- **An employee on the list with no documents** → leave that row blank (don't invent terms).
- **A document with no matching employee on the list** → still review it, add a row, and leave the
  Name blank but make clear which document it is.
- **Directors/owners** may appear on the list with no employment contract (they're the signatory,
  not an employee) → leave blank with a short note.

## Step 1 — Gather the inputs

Locate two things; if either is missing, ask for it (request folder access if none is mounted):

1. **The review template** (Excel). Read its **header row** to get the exact field set — don't
   assume a fixed column list; use whatever the template has. Note pre-filled columns (Name,
   Dataroom Ref) so they're preserved.
2. **The documents** — a folder of PDFs. List them and group by employee. Watch for one employee
   with multiple files (contract + variation(s) + obligations + leaver docs).

## Step 2 — OCR the documents (nearly always required)

These documents are typically **scanned and redacted PDFs with no text layer**, so plain text
extraction returns nothing. Check the first page of one file: if `get_text()` is empty, OCR
everything. Use `scripts/ocr_pdfs.py`, which handles the traps that cost real time here:

- It **normalises render width** (~1200px) instead of using a fixed DPI, because some scans have
  huge page mediaboxes that otherwise produce enormous images and make OCR crawl.
- It is **resumable and time-boxed** — it skips files already done and only starts a file it can
  finish, so you can call it repeatedly (or as several parallel bash calls) within the shell's
  per-call time limit. Background processes do **not** survive between bash calls, and
  `ProcessPoolExecutor` tends to hang in the sandbox, so run OCR as repeated/parallel foreground
  calls rather than one long job or a forked pool.

Run: `python3 scripts/ocr_pdfs.py <pdf_dir> <out_txt_dir> [offset stride]`. Text is written one
`.txt` per PDF, with `===== PAGE n =====` markers so findings can cite pages.

## Step 3 — Review each employee against the fields

For each employee, read the **full OCR text** of all their documents and extract every field in the
template. Read `references/field-guide.md` first — it defines each standard field and how to pull
it, including the salary/variation logic and the standard clause wording these contracts reuse.

- **Detect the document template early.** Most staff are on an identical "Statement of Main Terms
  of Employment" plus a standard obligations addendum, so once you've read one carefully you can
  extract the rest quickly and, crucially, **spot deviations** (a different notice period, a
  probation clause, SSP-only sick pay, an apprenticeship agreement, etc.). Deviations are the
  findings that matter.
- **Apply variations on top of the base contract.** Salary, job title, hours and pension often
  change via later letters. Report the **current** position and note the original in brackets
  (e.g. "£33,750 (from Oct 2025; originally £28,400)").
- **Quote figures and cite where useful.** If a field is genuinely not addressed, say so plainly
  (e.g. "Not addressed — statutory only") rather than inventing.
- **For volume, parallelise.** With many employees, dispatch subagents (Task tool,
  general-purpose), each handling 2-3 employees, each returning one clearly-delimited
  `Field: value` block per employee so results parse straight into the template. Give every
  subagent the field guide and the core context above.

## Step 4 — Check signatures visually (don't trust OCR here)

Signature status is a key DD output, but in redacted documents OCR **cannot** tell a
redacted-but-signed block (a black box) from a genuinely blank, unsigned one — both read as empty
text. So verify signatures by **looking at the pages**, not from the OCR.

Use `scripts/signature_pages.py <pdf_dir> <out_img_dir>` to render one composite image per employee
showing each document's signature block (it crops the right band per document type — contracts and
obligations sign near the top of the final page, letters at the bottom). Then open each composite
with the image viewer and record, per document: whether each party signed, the signing dates, and
**whether the signature is redacted**. The recurring pattern to expect: the **employee** signature
and printed name are redacted (dates usually left visible); the **company** signatory is not
redacted. Flag anything that breaks the pattern:

- A contract with **no signature block at all** → unsigned; flag it.
- A block signed by one party only, or with the date/printed name left blank → incomplete
  execution; flag it.
- A name left **un-redacted** where it should be redacted → a redaction slip worth raising with
  the seller.

## Step 5 — Populate the template

Use `scripts/build_review.py`. It reads the user's template, matches your extracted values to the
template's own column headers (so it works whatever the columns are, with employment-specific
aliases built in), writes one row per employee **matched to the existing Name row so pre-filled
columns are preserved**, and applies light formatting. Save as a **new** file
(e.g. `<template name> - COMPLETED.xlsx`) so the original is untouched.

Note on the working environment: the sandbox can often **create** files in the user's folder but
not overwrite an existing one. If a save fails, write to a new filename and tell the user which
file is current — don't keep retrying the overwrite.

## Step 6 — Verify, save, present, summarise

- Check **no expected cell is empty** for employees who have documents (blank rows for
  no-document employees are fine).
- **Spot-check** salaries against the latest variation, and dates (commencement vs continuous
  employment — see field guide; the continuous-service date is the one that drives statutory
  liability). For high-stakes work, run a subagent to sanity-check the sheet against the sources.
- Save the completed template to the **deal folder** (if it can't be written, save to an accessible
  folder and say so) and present it with the file-sharing tool.
- Give a **short** written summary of the cross-cutting findings that matter: **signatures**
  (unsigned/partially-executed contracts), **non-standard terms** (unusual notice periods,
  probation, SSP-only sick pay, apprenticeships/fixed terms), **leavers**, large undocumented pay
  jumps, and any **restrictive-covenant** concerns. Offer to consolidate the "Outstanding points"
  column into a single seller query list.

## Files

- `references/field-guide.md` — definition of each standard review field, how to extract it, the
  standard clause wording these contracts reuse (sick pay, restrictive covenants, IP, notice), and
  the commencement-vs-continuous-employment distinction. Read this before reviewing.
- `scripts/ocr_pdfs.py` — resumable, time-boxed OCR for scanned/redacted PDFs (normalised render).
- `scripts/signature_pages.py` — renders one signature-block composite image per employee for the
  visual signature check.
- `scripts/build_review.py` — populates the user's template from extracted data (header-matched,
  preserves pre-filled columns, formats). `python3 build_review.py <template.xlsx> <data.json> <output.xlsx>`.
