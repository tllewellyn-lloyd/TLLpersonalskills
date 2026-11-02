---
name: customer-contract-review
description: >
  Review a target company's customer contracts for buy-side due diligence and populate a
  contract-review template (Excel) with a structured row per contract. Use this skill whenever
  the user provides a folder/set of customer (or supplier) contracts for a deal plus a review
  template and asks to "review the contracts", "fill in the contract review template", "do the
  contract review", "go through these contracts", "build the contract review spreadsheet", or any
  variation where multiple contracts need to be read against a fixed set of review fields and the
  findings tabulated. Works for any Tern Capital deal and any contract type (bespoke customer
  paper, standard supplier templates, and public-sector framework call-offs such as G-Cloud or
  GP IT Futures). The user supplies the review template at the start; the skill adapts to whatever
  columns that template contains. Output is the user's template, populated, saved to the deal folder.
---

# Customer Contract Review

Reads a set of a target's customer contracts and fills in the user's contract-review
template — one row per contract, one column per review field — for buy-side due diligence.
Developed interactively on a real Tern deal (a primary-care software target), but the steps
apply to any deal and any contract type.

## Core context — get this right first

This is almost always **buy-side DD on an acquisition target**. Before reviewing anything,
establish **who the target is** and therefore whose side "we" are on:

- The target (the company Tern is buying) is usually the **supplier/licensor** in these
  contracts; the counterparties are its **customers**.
- So when a field asks about **change of control**, it means: *if Tern acquires the target
  (a change of control of the supplier), does the customer get a right to terminate, and must
  the target notify the customer?* This is one of the most important fields — see the field guide.
- IP, liability, assignment etc. are all read from the **target's** perspective ("what do we
  own / owe / risk").

Confirm this framing with the user if it is not obvious from the documents.

## Step 1 — Gather the inputs

Ask for / locate two things:

1. **The review template** (Excel). The user provides this at the start. **Read its header row**
   to determine the exact field set — do not assume a fixed list of columns; use whatever the
   template has. Note any columns that are **already pre-filled** (e.g. Customer name, Dataroom
   Ref) — these must be **preserved, not overwritten**.
2. **The contracts** — a folder of PDFs (or Word/scans). Confirm how many there are and map each
   contract file to the correct template row (match on customer name; watch for one customer with
   multiple files, e.g. a base agreement plus an extension/variation — review those together as a
   single row if the user asks).

If either input is missing, ask for it before proceeding. If no folder is mounted, request access.

## Step 2 — Extract the contract text

Convert every contract to text so it can be read in full (contracts here run 50-100+ pages):

- Use `pypdf` / `pdfplumber` via the bash tool to extract text to per-file `.txt` files, tagging
  page numbers (e.g. `===== PAGE n =====`) so findings can cite pages/clauses.
- If a PDF is a scan (little/no extractable text), OCR it (see the `pdf` skill).
- Extraction across many large PDFs can be slow — run it in batches and re-run for any file that
  times out rather than assuming it failed.

## Step 3 — Review each contract against the fields

For each contract, read the **full text** (don't skim) and extract every field in the template.
Use `references/field-guide.md` for what each standard field means and how to pull it reliably,
including the ARR recalculation logic and the change-of-control test.

- **Cite clauses and quote figures** wherever possible (e.g. "cl.12.1", "£15,434.21", "Schedule 1").
- If a field is genuinely not addressed, write **"Not specified in contract"** — don't invent.
- Detect the **contract type** early (standard template vs framework call-off vs bespoke customer
  paper); it drives many answers (see field guide) and lets you spot when several contracts share
  an identical template so you can review them efficiently and consistently.

**For volume, parallelise.** With many contracts, dispatch subagents (Task tool, general-purpose),
each handling a few contracts, each returning one clearly-delimited block per contract in a fixed
`Field: value` format so the results can be parsed straight into the template. Give every subagent
the core context above (who is supplier vs customer) and the field guide. Keep each subagent to
~2-3 contracts so quality stays high.

## Step 4 — Populate the template

Use `scripts/build_review.py`. It reads the user's template, matches your extracted field values
to the template's own column headers (so it works whatever the columns are), writes one row per
contract, **preserves pre-filled columns**, and applies light formatting (wrapped text, bold
header, frozen header row, sensible column widths/row heights). Save the output as a new file
(e.g. `<template name> - COMPLETED.xlsx`) so the original is untouched.

## Step 5 — Verify before delivering

- Check **no expected cell is empty** across all rows/fields.
- **Spot-check figures** and reconcile the **ARR** for each contract against the stated pricing
  (annual fee, or TCV ÷ years, or unit rate × volume). Where numbers don't tie, work out the
  discount/period basis and flag any internal inconsistency (contracts often carry two different
  totals — that's a query, not a silent pick).
- For high-stakes work, run a subagent to sanity-check the compiled sheet against the sources.

## Step 6 — Save, present, summarise

- Save the completed template to the **deal folder** the user is working in (if that folder can't
  be written from the sandbox, save to an accessible user folder and tell the user, and always
  present the file). Present it with the file-sharing tool.
- Give a **short** written summary of the cross-cutting findings that matter for the deal, e.g.:
  - **Change of control** — which contracts let the customer terminate / require notice if the
    target is acquired (the risk register items) vs which are silent (clean).
  - **Signatures** — which contracts are unsigned/only partially executed.
  - **ARR** — the recalculated figures and any anomalies or figures needing seller confirmation.
  - **Other themes** — lock-in / termination-for-convenience, liability caps, IP ownership,
    insurance, escrow, and any **parent company guarantee / performance security** the supplier
    must provide (or a customer could demand).
- Offer to consolidate the "Outstanding points" column into a single seller query list.

## Files

- `references/field-guide.md` — definition of each standard review field, how to extract it, the
  ARR recalculation method, and the change-of-control test. Read this before reviewing.
- `scripts/build_review.py` — populates the user's template from extracted data (header-matched,
  preserves pre-filled columns, formats). Run with `python3 build_review.py <template.xlsx> <data.json> <output.xlsx>`.
