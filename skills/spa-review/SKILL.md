---
name: spa-review
description: "Review a Seller's tracked changes or comments on the Tern Capital SPA and produce an Excel summary spreadsheet with a row per issue showing the clause/schedule reference, the Seller's exact position, and Tern's proposed response — all grounded in Tern's buy-side negotiation playbooks. Use this skill whenever a Seller-modified SPA document is provided (Google Doc link, Word .docx, PDF, or pasted text of changes), or when the user says things like \"go through what the seller changed\", \"create the SPA review spreadsheet\", \"process the seller's redlines\", \"summarise the seller's comments\", or \"here are the seller's tracked changes\". Also trigger when the user pastes a list of seller clause changes inline. Applies ONLY when Tern is the BUYER — not when Tern is selling.\n"
---

# SPA Review Skill

This skill helps Tern Capital review a Seller's tracked changes and comments on the standard Tern SPA template. The output is an Excel spreadsheet that Karthik can use directly in deal negotiations.

## Output format

Produce an Excel file named `SPA Review - [Deal Name or date].xlsx` (use today's date if deal name unknown) saved to the workspace folder. The spreadsheet has the following columns:

| Column | Header | Notes |
|--------|--------|-------|
| A | **Clause / Schedule Reference** | e.g. "Clause 6.2", "Schedule 6 Para 3.1", "Schedule 5 Part 1" |
| B | **Issue Raised by Seller** | Faithful, verbatim or near-verbatim summary — do NOT editorialise or reframe the seller's position |
| C | **Tern's Proposed Response** | Tern's recommended counter-position, grounded in the playbook (see reference file) |
| D | **Accept / Reject / Negotiate** | A simple status: "Reject", "Accept", or "Negotiate" |

Apply light formatting: bold headers, freeze top row, auto-fit column widths. Column B and C should wrap text. Use red fill for "Reject" rows, green for "Accept", yellow for "Negotiate".

## Step-by-step workflow

### Step 1 — Obtain the document

The Seller's SPA may arrive as any of these:

- **Google Doc link** — use the `google_drive_fetch` tool with the document ID extracted from the URL
- **Word .docx file** — use the docx skill or python-docx to extract tracked changes and comments
- **PDF** — use the pdf skill or pypdf2/pdfplumber to extract annotations and text
- **Pasted text** — the user may paste the seller's changes directly into the chat

The Tern standard SPA template (what we sent the Seller) is at:
`https://docs.google.com/document/d/1xuqwAO6gmd18eZQwuxKbZQCSqWypyVPi4MWY7LWg3N4`

> **Important note on Google Docs tracked changes:** The `google_drive_fetch` tool returns the document's accepted/current text. It does NOT surface tracked changes (suggestions) directly. If the Seller returned a Google Doc with suggestions, the user may need to share a version with changes accepted/visible, export it as a Word doc, or paste the changes as text. If you can't detect changes in the fetched content, tell the user and ask them to paste the seller's changes directly.

### Step 2 — Extract each issue

Go through the document carefully and identify every place the Seller has:
- Made a tracked change (insertion, deletion, substitution)
- Left a comment requesting a change
- Proposed alternative wording

For each issue, note:
1. The specific clause or schedule reference (be precise — e.g. "Clause 11.3(b)" not just "Clause 11")
2. What exactly the Seller is requesting or changing (their position, verbatim where possible)

### Step 3 — Draft Tern's response

For each issue, open `references/playbook.md` and identify the relevant Tern position. Apply it to draft a concise response. If a topic is not covered in the playbook, use reasonable judgment consistent with a buy-side PE firm perspective, and flag it as "Needs review" in the response.

The response should be direct and practical — the kind of thing Karthik would say to a Seller's solicitor. For example:
- "Reject — Tern's position is basket at 0.25% of CC. We would accept 0.5% as a compromise."
- "Reject — business warranties must run for 48 months. We will not agree to less than 36 months."
- "Negotiate — we are open to discussing this if Seller provides justification."

### Step 4 — Produce the Excel

Use `openpyxl` (via Bash/Python) to create the spreadsheet. See the helper script at `scripts/build_excel.py` — run it with the collected data as a JSON input, or adapt it as needed.

Save the final file to `/sessions/sweet-epic-hypatia/mnt/SPA Review/` and provide the user with a `computer://` link.

## Reference material

Read `references/playbook.md` before drafting any responses — it contains all of Tern's buy-side positions on limitations (quantum and time periods), joint & several, set-off, awareness, locked box, earn-outs, and deferred consideration.

## Tone

Tern's responses should be confident and precise — this is a PE firm that knows its positions. Avoid wishy-washy language. Say "Reject" when you mean it, and give a clear reason. Where a compromise exists in the playbook (e.g. basket up to 0.5%), mention it explicitly.
