---
name: statutory-register-review
description: "Reconstruct and review a UK company's statutory registers from uploaded source documents. Use this skill whenever a user uploads files (spreadsheets, PDFs, Companies House forms, stock transfer forms, share certificates, board minutes, resolutions) and asks to review, reconstruct, audit, or check statutory registers, share register, register of members, cap table, or shareholding history under UK company law. Trigger phrases include \"review the stat books\", \"reconstruct the registers\", \"build the share register\", \"audit the company records\", \"check the statutory registers\", \"who are the current shareholders\", \"piece together the company history\", \"review these Companies House forms\", or \"what's missing from these records\". Covers register of members, register of directors, PSC register, register of secretaries, and register of charges. Even if the user only mentions shares, use this skill — it handles the full set of statutory registers.\n"
---

# Statutory Register Review

Reconstruct a UK company's statutory registers from a set of uploaded source documents and produce a single Excel workbook summarising the complete corporate history, including a register of transfers and a document checklist showing what is present, missing, or incomplete for every corporate event.

## What this skill does

Users typically arrive with a jumble of documents — Companies House filings, stock transfer forms, board minutes, emails, spreadsheets — and need someone to piece together the company's statutory registers from scratch or verify an existing set. The skill:

1. Reads and classifies every uploaded document
2. Extracts every corporate event in chronological order
3. Reconstructs each statutory register
4. Builds a dedicated register of transfers
5. Produces a document checklist showing required vs available evidence per event
6. Identifies missing information and compliance gaps
7. Produces a single Excel workbook with the full picture

## Output specification

**Filename:** `[Legal Entity Name] - Stat Register.xlsx`

Use the company's registered name as it appears in the documents. If unclear, ask the user.

**Tabs (in this order):**

| Tab | Purpose |
|-----|---------|
| **Event Timeline** | Every corporate event in chronological order |
| **Register of Members** | Full register: current and former members with shareholdings |
| **Current Shareholding** | Snapshot of who holds what today, with percentages and values |
| **Register of Transfers** | Dedicated transfer-by-transfer record with full parties, consideration, and certificate references |
| **Document Checklist** | RAG-coded checklist of required documents for every transfer, allotment, sub-division, and cancellation event |
| **Register of Directors** | Current and former directors with all required fields |
| **Register of Secretaries** | Current and former secretaries (include even if blank) |
| **PSC Register** | Persons with significant control |
| **Missing Information** | Every gap, inconsistency, and red flag identified |

---

## Required documents by event type

These are the documents that must exist to support each type of corporate event. Use these as the basis for the Document Checklist tab and as the framework for identifying gaps.

### Share transfer

| Document | Notes |
|----------|-------|
| **J30 stock transfer form** (or J10 for partly-paid shares) | Required as the proper instrument of transfer under s.770 CA 2006. Must be signed by the transferor. |
| **Stamp duty payment / HMRC confirmation letter** | Required only if consideration exceeds £1,000. HMRC must authenticate the J30 and issue a confirmation letter before the company can legally register the transfer. An unauthenticated form must not be registered. |
| **Board approval** | Most articles require director approval before registration. Evidence is typically board minutes approving the transfer. |
| **PSC register update** | Required if the transfer causes any person's holding to cross a 25%, 50%, or 75% threshold in either direction, or causes a PSC to cease to qualify. Notification to Companies House within 14 days. |
| **New share certificate** | Must be issued to the transferee within 2 months of registration of the transfer (s.769 CA 2006). Cancelled certificate(s) should be noted. |

### Share allotment

| Document | Notes |
|----------|-------|
| **Board resolution with s.551 authority to allot** | Directors need authority from the members (or from the articles) to allot equity securities. An ordinary resolution is normally sufficient for private companies. |
| **Pre-emption rights waiver (if applicable)** | Existing members have statutory pre-emption rights on new allotments of equity securities (s.561 CA 2006). These must either be followed (offer pro-rata to existing members first) or dis-applied by special resolution (s.570). |
| **SH01 — Return of allotment** | Must be filed at Companies House within one month of the allotment (s.555 CA 2006). Note: SH01 does NOT name the allottees — allottee identity must come from board minutes, share certificates, or a cap table. |
| **Share certificates** | Must be issued within 2 months of allotment (s.769 CA 2006). |

### Share sub-division or consolidation

Sub-division (splitting) and consolidation (combining) are distinct from allotment — they change the nominal value and number of shares without creating new capital. They require different forms and authority. Do not treat a sub-division as an allotment; they use SH02, not SH01.

| Document | Notes |
|----------|-------|
| **Authorising resolution** | Typically an ordinary resolution (check articles). |
| **SH02 — Notice of sub-division or consolidation** | Must be filed at Companies House within one month of the event (s.621 CA 2006). |
| **Updated share certificates** | Old certificates become void and new certificates must be issued reflecting the post-sub-division or post-consolidation holding. |

### Company purchase of own shares (buyback) and cancellation

| Document | Notes |
|----------|-------|
| **SH03 — Return of purchase of own shares** | Filed at Companies House under s.707 CA 2006. Contains shares purchased, consideration, and delivery date. Must be submitted to HMRC for stamping before filing at Companies House if consideration exceeds £1,000 (stamp duty at 0.5%, rounded up to nearest £5). |
| **HMRC authentication code on SH03** | HMRC must authenticate the SH03 if stamp duty is payable. A blank authentication code field is a Critical gap — the buyback may be void if Companies House accepted an unauthenticated form. |
| **SH06 — Notice of cancellation of shares** | Filed at Companies House under s.708 CA 2006. Contains the cancellation date and the updated statement of capital. |
| **Board resolution** | The board must resolve to approve the buyback and recommend it to shareholders. |
| **Members' ordinary resolution** | Shareholders must approve the buyback under s.690 CA 2006. Written resolution signed by members holding a simple majority of eligible voting shares is sufficient for a private company. Note: the selling member cannot vote on this resolution. |
| **Buyback contract** | The terms of purchase should be set out in a formal contract. |
| **Updated share certificates** | Best practice is to reissue or confirm share certificates for remaining holders after cancellation to reflect the updated capital position. |

---

## Workflow

Before starting, read `references/uk-statutory-registers.md` — it contains the legal requirements for each register, the fields required for each event type, the document recognition guide, and the common gaps to watch for.

### Step 1 — Gather and read all files

Read every uploaded file. Use the file-reading skill if file contents are not already in context. For PDFs, use the pdf-reading skill. For .docx files, use python-docx or the docx skill. For .xlsx/.csv files, use openpyxl or pandas.

List all files received and classify each one before proceeding.

### Step 2 — Identify and classify each document

For each file, determine what type of document it is using the recognition guide in `references/uk-statutory-registers.md` (Section 7). Label each document clearly — e.g., "SH01 dated 15 March 2022", "J30 transfer Smith to Jones", "Board minutes 1 January 2023".

If a file contains multiple documents (e.g., a PDF bundle or a spreadsheet with multiple tabs), break them out individually.

If you cannot confidently identify a document, describe what you see and ask the user.

### Step 3 — Extract events chronologically

Go through every document and extract each discrete corporate event. An event is anything that changes the state of a register — a share allotment, a transfer, a director appointment, a PSC change, etc.

For each event, capture:

| Field | Description |
|-------|-------------|
| **Date** | The date the event occurred (not the filing date, unless the event date is unavailable) |
| **Event type** | Incorporation, Allotment, Transfer, Sub-division, Consolidation, Buyback, Cancellation, Director Appointment, Director Resignation, Secretary Appointment, Secretary Cessation, PSC Change, etc. |
| **Description** | Plain-English summary of what happened |
| **Parties affected** | Names of members/directors/PSCs involved |
| **Share details** | Class, number, nominal value, consideration, amount paid (if share-related) |
| **Source document** | Which uploaded file this comes from |
| **Notes / Issues** | Any problems spotted (missing data, inconsistency, unsigned, etc.) |

Sort all events by date. Where two events share the same date, order them logically (e.g., allotment before transfer of the same shares would not make sense — flag it).

### Step 4 — Reconstruct each register

Walk through the event timeline and build each register entry by entry.

**Register of Members:** Start with incorporation (subscriber shares). Apply each subsequent allotment, transfer, buyback, cancellation, consolidation, sub-division, etc. in order. For each member, track their running shareholding at each point. The final state is the current register of members.

**Register of Directors:** Start with first directors on incorporation (from IN01). Apply each AP01/TM01/CH01 event. Track appointment and cessation dates.

**Register of Directors' Residential Addresses:** Populate from AP01 forms (which contain residential addresses) and any CH01 changes. Include historical entries for past directors and secretaries, not just current ones.

**Register of Secretaries:** Start with any secretary appointed on incorporation. Apply AP03/TM02/CH03 events. If no secretary was ever appointed, include the tab but note "No secretary appointed". Note any extended vacancy.

**PSC Register:** For events from 6 April 2016 onwards, determine who qualifies as a PSC after each share event. Use the shareholding percentages and the five conditions of significant control. Apply PSC01–PSC09 events where filed.

### Step 5 — Build the Register of Transfers

Create a dedicated tab listing every share transfer in chronological order. For a company buyback, include it as the final entry with the company as the transferee and note the cancellation. For each entry capture:

| Field | Notes |
|-------|-------|
| Transfer number | Sequential |
| Date | Execution date of J30 (or board approval date if J30 absent) |
| Transferor name and address | As shown on J30 or internal register — note any discrepancy |
| Transferee name and address | As shown on J30 or internal register — note any discrepancy between documents |
| Share class | |
| Number of shares transferred | |
| Consideration (£) | Formatted as currency; note "Gift / nil consideration" if applicable |
| Price per share | |
| Old certificate(s) cancelled | Certificate numbers and original holding |
| New certificate issued | Certificate number and new holding; note if none issued |
| Notes | Discrepancies, missing documents, or issues |

### Step 6 — Build the Document Checklist

Create a tab with four sections (A–D) covering each event type. For each event, show the status of each required document using RAG coding:

- **✓ Present** — document is in the bundle and appears complete (green fill)
- **✗ Missing** — document should exist but has not been provided (red fill)
- **⚠ Partial** — document exists but has a material deficiency (amber fill)
- **N/A** — not applicable to this specific event (grey fill)

**Section A — Transfers:** Columns for J30, Stamp Duty applicable (yes/no), Stamp Duty Paid/HMRC Letter, Board Approval, PSC Update, New Certificate.

**Section B — Allotments:** Columns for Board Resolution (s.551 authority), Pre-emption Rights Waived, SH01, Share Certificates.

**Section C — Sub-divisions / Consolidations:** Columns for Authorising Resolution, SH02, Updated Certificates.

**Section D — Cancellations (Buybacks):** Columns for SH03, SH06, Stamp Duty / HMRC Authentication Code, Board Resolution, Members' Resolution, Updated Certificates.

Include a notes column in each section for context. Add a legend at the top of the tab.

### Step 7 — Identify missing information

Cross-reference the reconstructed registers against what the law requires (see Section 9 of the reference file). For every gap, create an entry in the Missing Information tab with:

| Field | Description |
|-------|-------------|
| **Register affected** | Which register has the gap |
| **Event / Date** | Which event the gap relates to (or "General" if systemic) |
| **What's missing** | Specific description of the missing information |
| **Why it matters** | Legal requirement or practical consequence |
| **Severity** | Critical / Important / Minor |
| **Suggested action** | What the user should do to fix it |

**Severity guide:**

- **Critical** — the register cannot be accurately maintained without this, or there is genuine title uncertainty (e.g., identity mismatch between physical certificates and internal register; transfer without a J30; HMRC authentication code blank on a chargeable SH03; SH02 not filed for a sub-division; no evidence of who current shareholders are)
- **Important** — a compliance gap that should be fixed but does not prevent reconstruction (e.g., missing board approval for a transfer, SH01 not evidenced, no pre-emption waiver on file, PSC cessation date incorrect)
- **Minor** — a best-practice gap (e.g., residential address register incomplete for historical directors; long-running secretary vacancy; AR01 amount-paid field incorrectly £0)

Also perform these cross-checks:

1. **Statement of capital reconciliation** — does the running share capital (total nominal value per class) after all events match the most recent CS01, SH01, SH02, SH03, or SH06 statement of capital? Flag any discrepancy.
2. **PSC threshold check** — after each share event from April 2016 onwards, check if any person's percentage crosses 25%, 50%, or 75% in either direction. Verify a PSC notification exists for each crossing.
3. **PSC cessation date precision** — for buybacks, the PSC cessation date should be the cancellation date (SH06), not the delivery date (SH03). These frequently differ — flag if the PSC register uses the wrong one.
4. **Director minimum** — verify the company has at least one natural-person director at all times.
5. **Chronological consistency** — verify no one transfers shares they don't hold, and no allotments occur without authority.
6. **Certificate number sequencing** — cross-check certificate numbers on physical certificates against those in the internal allotments register and members ledger. Transposition errors (attributing a certificate number to the wrong shareholder) are a common mistake and create title uncertainty. Physical certificates are authoritative.
7. **AR01/CS01 amount paid per share** — the field is sometimes left at £0 even for fully paid shares due to Companies House form defaults. Cross-check against the allotments register and note any discrepancy.

### Step 8 — Produce the Excel workbook

Use the helper script at `scripts/build_register_excel.py` for the core tabs. Build the Register of Transfers and Document Checklist tabs directly using openpyxl after the helper script runs.

Formatting standards:

- **Headers:** Bold, dark navy background (#2C3E50), white text, frozen top row on every tab
- **Section headers (Document Checklist):** Darker navy (#283747), white bold text, merged across columns
- **Column widths:** Set explicitly for readability — do not rely solely on auto-fit for wide notes columns; cap description/notes columns at ~55 characters with text wrapping
- **Date format:** DD/MM/YYYY (UK format)
- **Currency:** GBP unless documents specify otherwise — format monetary values with £ symbol and 2 decimal places
- **Missing Information tab:** Red fill (#F5B7B1) for Critical, amber (#FAD7A0) for Important, light yellow (#FEF9E7) for Minor
- **Document Checklist RAG cells:** Green (#D5F5E3) / red (#F5B7B1) / amber (#FAD7A0) / light grey (#F2F3F4) with centred bold text
- **Current vs former rows:** Green fill (#D5F5E3) for Current, grey fill (#F2F3F4) for Former
- **Alternating row fills** on Register of Transfers: white / light blue (#D6EAF8)
- **Row heights** on Register of Transfers and Document Checklist: set explicitly (65–80pt for data rows, 120pt for complex notes rows) — openpyxl auto-height does not render reliably for wrapped text

Save the file to `/mnt/user-data/outputs/` using the naming convention: `[Legal Entity Name] - Stat Register.xlsx`

---

## Presenting results

After producing the Excel, give the user a concise summary in the chat covering:

1. **Company snapshot** — name, company number (if known), date of incorporation, current share capital structure
2. **Key events count** — how many events were extracted and from how many documents
3. **Current shareholding** — a brief table of who holds what
4. **Current directors** — who is currently in office
5. **Top issues** — the 3–5 most critical items from the Missing Information tab, leading with any identity or title uncertainty issues before process/compliance gaps

Do NOT reproduce the entire Excel content in the chat. The workbook is the deliverable — the chat summary is just the headline.

---

## Patterns to watch for (learned from live reviews)

These are specific patterns that arise frequently in practice and are not always obvious from the documents alone.

**Identity mismatch between physical certificates and internal register.** The name on physical share certificates or a J30 may differ from the name recorded in the internal allotments register or members ledger. This can mean: (a) the same person operates under a different or former name; (b) the register was populated incorrectly; or (c) a completely different person holds the shares. Always cross-check every name across all source documents. Any discrepancy is Critical — it creates genuine title uncertainty and must be resolved before any transaction.

**Certificate number transposition.** Internal registers sometimes record certificate numbers in the wrong order — particularly where two allotments occur on the same date. Physical certificates are authoritative. Always cross-check certificate numbers on physical certs against the allotments register and members ledger. A transposition must be corrected in the register.

**Sub-division misclassified as allotment.** Small companies often record a sub-division in their internal register as the old shares being "cancelled" and new shares being "re-issued." A sub-division does not create new capital and is governed by SH02 (not SH01). Flag this distinction clearly — a missing SH02 is a common and significant gap.

**Stamp duty authentication code blank on SH03.** The SH03 form has a dedicated field for the HMRC authentication code confirming stamp duty has been paid. This field is frequently left blank. Where consideration exceeds £1,000, a blank code is a Critical gap — Companies House should not accept an unauthenticated SH03 and the buyback may be void. Always check and flag this.

**PSC cessation date: delivery vs cancellation.** In a buyback, the seller's PSC status ceases on the cancellation date (SH06), not the delivery date (SH03). The two dates differ and the PSC register is often updated with the wrong one. Cross-check both dates and flag any mismatch as Important.

**Address errors in internal ledgers.** Copy-paste errors when building internal registers sometimes result in one member's address being recorded against another member's name — particularly where multiple entries are made at the same time. Always cross-check addresses in the internal register against physical certificates, J30 forms, and Companies House filings.

**Dispute settlements contemporaneous with share transfers.** Where a loan account, accounting ledger, or legal correspondence shows financial payments made around the time of a share transfer, consider whether those payments may represent undisclosed additional consideration. Stamp duty is calculated on total consideration paid — undisclosed consideration creates a potential HMRC liability. Flag this for the user to take advice on.

**AR01/CS01 "amount paid" incorrectly £0.** The Companies House electronic filing system sometimes defaults the "amount paid per share" field to £0. This does not mean the shares are unpaid — cross-check against the allotments register. If shares are fully paid in the register but recorded as £0 in the annual return, note the discrepancy as Minor so it does not mislead future reviewers.

**Long-running secretary vacancy.** Private companies are not required to have a secretary, but a vacancy persisting for many years (e.g., more than five years) is an indicator that secretarial housekeeping may have been neglected across the board. Note the vacancy start date and duration in the Register of Secretaries and the Missing Information tab.

**Transfers "on appointment" or "on termination."** Owner-managed companies sometimes transfer shares to a person when they join in a key role and require them back on exit. These transfers are often informally documented or undocumented. Where board minutes refer to a transfer "on appointment as secretary" or "on termination," ensure a J30 exists and that the share price is commercially reasonable — a below-market exit price may attract HMRC scrutiny or indicate undisclosed side arrangements.

---

## Edge cases

**Multiple share classes:** Track each class separately throughout. The Current Shareholding tab should break down by class, with sub-totals per class and a grand total.

**Partly-paid shares:** Track the amount paid and the amount unpaid separately. Flag any shares that remain partly paid in the current register.

**Treasury shares:** If a buyback resulted in shares being held in treasury rather than cancelled, track these separately — they are not allocated to any member but still exist as issued capital.

**Pre-2006 Act companies:** Older companies incorporated under the Companies Act 1985 or earlier may have different historical document formats. The principles are the same, but the form numbers differ. Focus on extracting the substance (who, what, when, how many shares) rather than matching specific form numbers.

**Dormant companies:** May have very few events (just incorporation and annual filings). The skill should still produce the full set of tabs, even if most are nearly empty.

**Companies limited by guarantee:** These have members but no share capital. The register of members records guarantee amounts rather than shares. Adapt the output accordingly — the Current Shareholding tab becomes "Current Members" with guarantee amounts instead of shares. The Register of Transfers and Document Checklist will be empty or minimal.

---

## What this skill does NOT do

- It does not file anything at Companies House
- It does not provide legal advice — it identifies gaps and flags them for a solicitor or company secretary to resolve
- It does not create the statutory registers in their formal legal format (e.g., a bound register book) — it produces a practical Excel summary
- It does not verify the authenticity of documents — it takes them at face value and flags inconsistencies
