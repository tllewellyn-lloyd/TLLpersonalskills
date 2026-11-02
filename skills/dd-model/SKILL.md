---
name: dd-model
description: Build a Tern Capital due diligence (DD) financial model as an Excel workbook from a folder of seller/dataroom files. Use this skill whenever the user asks to build, start, refresh, or extend a DD model, GS model, or deal model for a target company — e.g. "build the model for X", "start the DD model", "set up the model from the dataroom", "refresh the model with the new files" — or whenever the user points at a folder of seller-provided files (accounts, payroll, revenue listings, contracts) and wants a financial model, P&L build, or Tern Y1 view produced from them. Also use it to add new source data into an existing DD model workbook following Tern conventions. The deliverable is a single .xlsx master workbook per deal (plus an optional companion source-data workbook when the full verbatim source is wanted).
---

# Tern Capital DD Model Builder

Build the master due-diligence workbook for a deal, from a folder of seller files, following Tern Capital's modelling conventions (derived from the Notion "Due Diligence GS Model" playbook and the Dizions Master reference model).

One deal = one live master workbook, named `<Target> Master.xlsx`. Everything the deal team learns from the seller's data lives in this one file, structured so any tab can be refreshed mechanically when new data arrives.

## Before starting

Read these reference files as you reach each phase (not all upfront):

| File | Read when |
|---|---|
| `references/tab-structure.md` | Phase 2 — tab taxonomy, Legend layout, section-marker system |
| `references/conventions.md` | Phase 2–3 — font and palette, colour coding, provenance labels, version-control hygiene |
| `references/pl-methodology.md` | Phase 4 — Y1 P&L build rules and the standard line taxonomy |
| `references/tab-layouts.md` | Phase 4 — cell-level layouts for PL, CB, WC, EB, NTA, ARR testing blocks |

Also read the `xlsx` skill's SKILL.md before writing any workbook — it governs how to produce clean Excel files. **Where the xlsx skill conflicts with "House formatting" below, House formatting wins** — it is the current Tern standard, taken from `MASTER_template_PL.xlsx`.

If the seller files are on the user's computer (connected folder), stage them into the session first; work on local copies only.

Clarify with the user before starting if genuinely unclear: which folder is the dataroom, the target's financial year end, and whether a model already exists for this deal (extend it — never build a parallel one). If the model exists, refresh datasets by replacing values in the same shape rather than adding V2 tabs (see conventions.md).

Where the dataroom leaves a genuine modelling choice open — which period Y1 should mirror, which of two accounting bases to default to, the reporting currency — put it to the user before building rather than picking silently. These choices change the shape of the workbook and are expensive to reverse once the tabs are wired.

### Execution environment

This skill runs on two surfaces. Detect which and adapt:

- **openpyxl / container path** (a folder of files, deliver a .xlsx): `scripts/` and `references/` are available. Use them, then follow the recalculate-and-inject step in Phase 5.
- **Live Excel add-in path** (building directly into an open workbook via `execute_office_js`): the scripts and references may not be present, so build to the conventions in this file directly, including House formatting. Constraints learned on this surface:
  - Tool functions (`set_cell_range`, `execute_office_js`, …) are not callable from inside the code-execution container, and uploaded source files cannot be pulled into the browser sandbox. Either read the data in the container, print modest JSON blocks and write them with `execute_office_js` as inline 2D arrays, or build a companion `.xlsx` in the container and deliver it as a file.
  - Formulas written natively into Excel recalculate automatically, so the empty-cached-value problem in Phase 5 does not apply.
  - `range.insert(Excel.InsertShiftDirection.right)` shifts cells and auto-adjusts formula references — use it to reposition a block (for example to clear column A) without rewriting formulas.
  - After any formatting, number-format or alignment change, re-read the affected cells (values and displayed format) before reporting done. Confirm dates and percentages survived any blanket number-format pass.

## House formatting (every workbook, every tab)

Taken from `MASTER_template_PL.xlsx`. Apply it as a final pass over the whole workbook, after the scaffold script has run.

**Font.** Nunito 11 throughout, every tab, every cell. Preserve bold / italic / colour already set; only the family and size are forced. The xlsx skill's Arial default does not apply to Tern models.

**Palette.**

| Element | Fill | Text |
|---|---|---|
| Section header row (`x` in column A) | yellow `FFFF00` | black, bold |
| Table column header row | orange `F79646` | white `FFFFFF`, bold, right-aligned for value columns |
| Sub-header / banner row | orange `FF6600` | white `FFFFFF`, bold |
| Subtotal and total rows | grey `EFEFEF` | black, bold |

Font colours keep their standard meanings and are never overloaded: blue `0000FF` = input/hardcode, black = same-sheet formula, green `008000` = cross-sheet link, red = external-file link (avoid entirely).

**Units and number format.** Financial statement tabs (PL, BS, R, CH) are held in **GBP full units** and displayed with `#,##0,"K"` — the trailing comma does the scaling. Sellers routinely submit in GBP '000; restate those figures ×1,000 on ingestion (exact, no rounding) and say so in the section's note. Never apply `#,##0,"K"` to data already in thousands — it divides by 1,000 a second time and silently shows £10,016K as £10K. Tabs whose source is already in full units (staff listings, pipeline exports) stay in units and use `#,##0`.

Tern check and reconciliation rows use `#,##0.0,"K"` so sub-£1k breaks stay visible instead of rounding away — a £0.9k break reading "1K" defeats the check.

Percentages `0.0%` (two decimals on churn and other rates), multiples `0.0x`, dates `DD/MM/YYYY`.

**PL tab column widths** (from the template): A 5.0, line items 48.75, mapping 24.63, gap columns 5.88, Tern Y1 24.63, comment columns 50–62. Year columns ~14.

**Layout.** Merge period-spanning header cells (a single "basis of column" label across the historic years) rather than repeating the text in each one. Set explicit row heights on rows carrying long wrapped comments — Excel auto-fits, but previews and PDF exports do not, and the text clips. Turn gridlines off on every sheet.

## Phase 1 — Inventory the folder

Walk the folder recursively and classify every file before opening any of them in depth. Ignore junk (`__MACOSX`, `.DS_Store`, temp files). Classify into the categories that map to tabs: statutory accounts, management accounts, budgets/forecasts, payroll/staff costs, revenue/ARR/customer listings, churn data, aged debtors/creditors, bank statements, VAT/tax, pipeline (CRM exports), contracts, corporate/Companies House, IM and qualitative documents.

A single completed data-request template counts as a dataroom: index each of its sheets as a separate row.

Record where each file ended up. The Legend is the tab map only (see Phase 2), so the audit trail of what the seller gave us lives in the QA tab's data-request log rather than a dataroom index on L.

## Phase 2 — Scaffold the workbook

Decide which tabs this folder's data supports (see `references/tab-structure.md` for the full Pre-LOI/Post-LOI taxonomy). Always include: **L** (Legend), **PL**, **CB**, **R**, **QA**. Add others (BS, C, WC, EB, B, AR, AP, CA, T, ARR, CH, PP, CN, SD...) only when the folder actually contains that material — an empty tab is clutter, and a missing dataset belongs in QA as a data request instead.

Then run the scaffolding script:

```bash
python scripts/scaffold_model.py --config scaffold_config.json --output "<Target> Master.xlsx"
```

The config specifies deal name, tab list with groups, and historic year labels; the script builds the Legend (tab map only), tab colours, the full standard PL skeleton with formulas, and the QA tab headers, all in the house font and palette. See the script's docstring for the config schema. After scaffolding, keep the physical tab order matching the Legend order at all times.

**The Legend is the tab map and nothing else.** One section, titled `<Deal> - Tern Capital DD master model`, then a blank row, then the map: Sheet | Grouping | Description | Colour | Comments/Questions. No change log, no dataroom index, no section index — the scaffold no longer writes them, and nothing should be added below the map. Keep column A free of anything but the `x` marker: `audit_model.py` reads column B below the header as tab codes, so any stray text there becomes a phantom tab.

Write each **Colour** cell in the colour it names — "Green" in green, "Pink" in pink — so the tab bar and the map read together at a glance.

Keep **Comments/Questions** to one or two short sentences per tab: the two or three live issues, not a paragraph. It is a prompt for the reader, not the analysis.

Two things to know about what the scaffold produces, before wiring anything to it:

- The script writes the P&L skeleton at fixed row positions. If this deal needs an extra line inside a block, insert the row **immediately after scaffolding and before writing any source sections**, then rewrite the affected subtotal formulas yourself. openpyxl's `insert_rows` does not shift references inside existing formulas, so inserting later silently breaks every formula below the insertion point. (In live Excel, `range.insert` does adjust references.)
- Settle the row coordinates of the source sections before writing them. Compute the start and end row of each block as variables and assert the block lands where the P&L formulas expect it, rather than counting rows by hand.

## Phase 3 — Ingest source data

Paste each classified dataset into its home tab as a **provenance-labelled section**: `x` in column A, section title in column B stating what it is, with the source filename cited using the format `— Source: <exact filename>`. Examples of the house style:

- `P&L — Source: Updated P&L.xlsx`
- `FY26 Sage P&L (detail) — Source: FY26 P&L.pdf`
- `Revenue by customer — Source: Revenue by Customer.xlsx`
- `FY26 staff listing — Source: Staff Breakdown & Costs.xlsx`

Rules that make refreshes mechanical:

- One dataset, one section. Keep the source's own column shape so a refresh is paste-values in the same shape.
- Raw data is input: blue font. Never retype numbers you can link.
- Anything Tern computed (recalculations, reconciliations) gets `(Tern)` in the section title.
- PDFs (stat accounts, mgmt accounts): extract the P&L and balance sheet tables faithfully — line names as printed, one column per period — into the relevant tab, titled with the document name. Use the `pdf` skill for extraction if the tables are hard to parse.
- Superseded data is deleted, not stacked — log the removal in the QA tab's data-request log first (see conventions.md).
- Where Tern convention needs costs negative but the source prints them positive, flip the sign once at ingestion and say so in a note row under the section title. Never flip signs inside downstream formulas.
- **Column A discipline:** column A holds only the `x` section markers, on every tab. When a source block would place its own values in column A (cost codes, titles, notes), shift the whole block one column right and put the `x` back on each header row.
- In imported source blocks, put text descriptions in the wide left columns (B, then C) and numeric codes to the right. Move only label columns; never move numeric, month or formula columns.
- Image-only PDFs need OCR: transcribe faithfully but flag on the tab that the figures are OCR-derived and to be verified.

### Importing the full verbatim source

When the team wants every source tab and not just summaries, choose per constraint:

1. **Stacked below the summary on the home tab, with live formulas.** Each source tab becomes a block under its own yellow `x` header naming file and tab. Shift every row reference by the block's row offset and remap same-file cross-sheet references to the other block's in-workbook position. Flattening an interlinked multi-tab workbook onto one sheet often breaks cross-sheet and positional formulas, so this suits only loosely coupled sources.
2. **Companion consolidated `.xlsx` (preferred for full fidelity).** Copy every source tab into one workbook **preserving the original tab names**, so all intra-file cross-tab formulas resolve and recalculate untouched. Deliver it alongside the master.

Some source formulas cannot recompute standalone once copied: structured-table references, external-workbook links, and self-referential or circular sums. Recalculate a copy, scan for `#N/A`, `#NAME?`, `#VALUE!` and `#REF!`, then overwrite each flagged cell with the seller's cached (`data_only`) value and note it.

### When two source files disagree

Sellers routinely supply the same period twice on different bases — a management pack reissued on a different accounting treatment, a restated comparative, a tracker that disagrees with a system export. This is a diligence finding in its own right and must never be resolved silently.

- Do **not** pick one file and discard the other. Ingest both.
- Wire one in as the primary source, stated explicitly in the section title and in the Legend's Comments column, and ingest the other as a clearly labelled comparison section that is **not** wired into any formula.
- Add a `(Tern)` reconciliation block quantifying the gap on every line that moves, with a row showing the difference.
- Make the disagreement the top-priority row in the QA data requests, phrased as "which basis does management stand behind" rather than as a request for more data.
- Log in the QA data-request log that the comparison section is retained deliberately, and under what condition it should be deleted.

The same applies within a single file: if a seller's listing does not agree with its own summary sheets, say so on the tab and raise it. It is a finding about the quality of their data, not a build error to paper over.

## Phase 4 — Analyse and build the Tern view

This is where the model earns its keep. Read `references/pl-methodology.md` and `references/tab-layouts.md` now.

1. **Summary blocks.** Every tab with material source data gets a formula-driven summary block as its first section (`PL summary`, `CB summary`, `R summary`...), computing from the raw sections below it. Formulas, never hardcodes — so pasting refreshed data recalculates everything downstream.
2. **The PL tab.** The first section is called simply `P&L` and starts on **row 1** — no title row above it. Row 3 carries the financial year end and nothing else, written as e.g. `31st May YE` or `31st Dec YE`. No "basis" or "Tern view" banner row.

   Column pattern: line item | Grouping | **every year the seller gave, actual and forecast** | gap | Tern Y1 PL | Comments - Tern Y1 basis. Label them `FY2026A` / `FY2027F` so actual and forecast are distinguishable at a glance, and say in a note under the section title that F years are unsupported seller forecast. **Nothing to the right of the Y1 comment column** — no Difference column, no CAGR column.

   Map every source P&L line to the standard taxonomy. Keep the full layout down to PBT even though decisions happen at EBITDA — it's what reconciles the model back to statutory accounts. Keep the Y1 comments to one short line each. The Check rows run across every year column, not just the actuals.

   The PL carries the summary, the seller source section, and the Check rows. It does not carry a seller-vs-Tern subtotal reconciliation or an EBITDA bridge section — anything those would have said belongs in a Y1 comment or a QA data request.
3. **Tern Y1 P&L.** Every line except payroll is a same-sheet formula mirroring **the current financial year** — the seller's forecast for the year in progress (FY2027F where the last actual is FY2026A), not the last actual and not the final forecast year. No adjustments applied; those are the deal team's to make later.

   Mirroring a forecast means Y1 inherits management's growth assumptions wholesale, so say so plainly in the Y1 basis comment and make the forecast's support a Critical data request. The conservatism rule still applies to everything Tern adds on top. Where an item is not in the source detail (e.g. depreciation), hardcode it in the latest-year column in blue and let Y1 link to it. Source sections below the summary carry a **Tern mapping** column and the summary's historic columns are driven by SUMIF against it. If the summary also has a grouping column, label it "Grouping", not "Mapping" — only one column can be the SUMIF key and the reader must know which.

   **When there is no usable current-year forecast or no historic full P&L** (for example only revenue actuals plus a forward forecast), do not pick silently. Ask the user which scenario column(s) Y1 should be based on, and support more than one Y1 column if they want (a cost-adjusted case and a pipeline case side by side). Show the remaining scenarios as comparison columns and keep every scenario tied to the source forecast to the penny.

   **Payroll is the exception.** Y1 `C&B` and Y1 `Contractors` are built bottom-up from the CB staff listing, not mirrored, using the keep/not flag:

   ```
   C&B          =-SUMIFS(CB!<cost>,CB!<employment type>,"Permanent",CB!<K or N>,"K")
   Contractors  =-SUMIFS(CB!<cost>,CB!<employment type>,"Contractor",CB!<K or N>,"K")
   ```

   Green font (cross-sheet link). Both tabs must be in the same units for this to work. Because Y1 payroll is deliberately not a mirror, do not treat the Y1/latest-year difference as a check — show it as a labelled movement row under the Check rows and say what drives it.

   **Flag the double-count risk every time.** If contractor costs already sit inside COGS in the seller's P&L — they usually do, with no separate Contractors line — then adding them to the Y1 overhead builds them in twice. Say so in the Y1 comment and raise it as a Critical data request; do not quietly net it off.
4. **CB tab.** Staff listing comes first, followed by the CB summary below it, so the reader sees who is in the business before the aggregate numbers. The listing ends at **Fully loaded annual cost** — ref, job title, location, work pattern, legal entity, division, employment type, date of birth, start date, currency, fully loaded cost. Do not carry the seller's salary / bonus / benefits component columns into it; note any problems with them beside the table and raise them on QA.

   Immediately after the cost column add a Tern **`K or N`** column: K = keep this person in the Tern Y1 payroll, N = exclude. Populate every row with `K` on first build and say so in a note — the deal team switches rows to N as leavers, duplicate roles and post-completion changes are agreed, and the PL tab's Y1 payroll updates automatically.

   Two reconciliations, both required:

   - **Against the latest P&L year** (the year Y1 is based on), directly beneath the listing total: listing total, less the P&L C&B charge for that year, difference, of which contractors, difference excluding contractors, and that residual as a % of the charge. Watch the signs — the P&L holds costs as negatives, so the difference is a SUM, not a subtraction.
   - **Against the latest actual year**, as its own block: listing total, less contractors, less anyone who started after the year end, against the actual charge, with the residual in GBP and as a % of it. This is the seller's own payroll cross-check and it tests the listing against something that really happened.
   If salaries are redacted, build the roster (title, department, hire date, tenure) and a headcount summary, take aggregate staff cost from the PL, and raise per-head cost as a QA data request.
5. **R tab.** Revenue summary, then revenue by customer with tenure data. Below the customer table, add a **gross churn calculation** as a full section in its own right — `x` in column A and the title in column B, not an indented sub-section: churned revenue per year using `SUMPRODUCT((prior-current)*((prior-current)>0))` across all customer rows, then gross churn rate as churned revenue / prior year total. Include a note explaining that gross churn does not net off expansion. If the seller has supplied only a single period of customer revenue, churn cannot be calculated: wire the block with an empty prior-year column so it populates when the data arrives, say plainly on the tab that it cannot be calculated, and raise the multi-year listing as a data request. Do not substitute contract tenure for churn; they are different claims.
6. **BS tab.** Balance sheets from multiple periods in a **consolidated table** — one row per line item, one column per period, newest first. NTA calculation section below.
7. **PP tab.** If pipeline/forecast data is available, ingest it with probability weightings and risk-adjusted values. Use formulas for risk-adjusted (= gross × probability) and % of total. Where the seller gives a sales stage but no probability, hold the stage weightings as visible blue inputs in their own table, say in the section note that they are a Tern assumption, and raise the target's own win rates by stage as a data request.
8. **Other Tern analyses** as data allows: churn commentary, NTA / working capital / entry assumptions blocks if the deal terms are known (layouts in tab-layouts.md).
9. Reproduce every cross-check the seller asserts in their own pack as a live formula, and say plainly whether it passes.
10. Populate the Legend's Comments/Questions column with the real open issues per tab — a blank column defeats its purpose.

### Wiring the SUMIF mapping

The scaffold writes a **Grouping** column (column C) containing the taxonomy grouping — "Recurring Revenue", "C&B - Staff", "Non-Recurring Cost of Sales". Those values repeat across rows, so column C cannot be a SUMIF key. Key on the P&L **line name in column B**, which is unique, and make the source section's Tern mapping column hold those exact line names:

```
=SUMIF($F$72:$F$119,$B6,C$72:C$119)
```

Anchor the sum range column-relative, row-absolute (`C$72:C$119`) so the formula copies cleanly across year or scenario columns — a stray absolute column marker collapses the range and every column returns the same subtotal. Getting this wrong produces a P&L where several lines return the same figure, which is easy to miss because the numbers still look plausible.

### Source lines that are not Tern P&L lines

Some source lines do not belong in the Tern cost taxonomy — development expenditure capitalised and similar credits that reduce reported cost, or items the deal team wants held outside the operating view. Leave these **unmapped** so the P&L body stays a clean statement of Tern's cost base and EBITDA falls out on the Tern basis directly.

Unmapped is not dropped. Whatever is left out must be:

- listed in an explicit `Unmapped source lines (Tern)` block with its value in every period column;
- included in the Check row, which becomes *source section total less mapped PBT less unmapped total* and must still be nil for every column;
- picked up in a named reconciliation section that ties the model back to the reported bottom line of the accounts.

With items left unmapped, the PBT line is a **Tern PBT**, not the statutory PBT, and the tie to the statutory accounts lives in the reconciliation section rather than in the P&L body. Label the row accordingly and say so in a Comments cell. Where this conflicts with `references/pl-methodology.md`, this file governs.

## Phase 5 — Gaps, verification, delivery

Everything the data cannot support becomes a row in the **QA** tab's `Data requests / questions` section: what's needed, why, which tab it feeds, priority. This doubles as the next info request to the seller.

Then verify before delivering:

```bash
python scripts/audit_model.py "<Target> Master.xlsx"
```

The audit checks Legend/tab-order agreement, orphan or default-named tabs, section markers, colour conventions, and the PL check row — structure only. Fix everything it flags. Then recalculate with the `xlsx` skill's `scripts/recalc.py` and ship nothing while it reports `errors_found`. (If `recalc.py` is unavailable, use `HOME=/tmp SAL_USE_VCLPLUGIN=svp soffice --headless --convert-to xlsx --outdir /tmp/recalc "<Target> Master.xlsx"`; without those variables soffice can fail with an X11 display error.)

### Alignment

As the last formatting step, set **every cell to top-aligned** (`vertical="top"`) — otherwise wrapped comment cells centre vertically and the row stops reading against its neighbours. Headers over numeric columns are right-aligned; row labels, grouping columns and comment columns stay left-aligned. Preserve any `wrap_text` and indent already set by building a fresh `Alignment` that carries the old values.

### Write the computed values back into the delivered file (openpyxl path)

openpyxl writes every formula with an **empty cached result**. Excel recalculates on load, but Drive preview, Google Sheets, Excel on the web and most other viewers do not, so the summary blocks appear blank while hardcoded source sections display normally. A clean `recalc.py` run verifies the formulas but does not fix this for the file being shipped, so inject the recalculated values into the delivered file:

```python
import shutil, zipfile, xml.etree.ElementTree as ET, openpyxl
MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", MAIN); Q = lambda t: f"{{{MAIN}}}{t}"
calc = openpyxl.load_workbook("/tmp/recalc/<Target> Master.xlsx", data_only=True)
order = openpyxl.load_workbook("<Target> Master.xlsx").sheetnames
vals = {f"xl/worksheets/sheet{i}.xml": {c.coordinate: c.value
         for row in calc[n].iter_rows() for c in row if c.value is not None}
        for i, n in enumerate(order, start=1)}
zin = zipfile.ZipFile("<Target> Master.xlsx"); zout = zipfile.ZipFile("tmp.xlsx", "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename in vals:
        root = ET.fromstring(data)
        for c in root.iter(Q("c")):
            if c.find(Q("f")) is None: continue
            for v in c.findall(Q("v")): c.remove(v)
            val = vals[item.filename].get(c.get("r"))
            if val is None: c.attrib.pop("t", None); continue
            v = ET.SubElement(c, Q("v"))
            if isinstance(val, bool): c.set("t", "b"); v.text = "1" if val else "0"
            elif isinstance(val, (int, float)): c.attrib.pop("t", None); v.text = str(val)
            else: c.set("t", "str"); v.text = str(val)
        data = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    zout.writestr(item, data)
zout.close(); zin.close(); shutil.move("tmp.xlsx", "<Target> Master.xlsx")
```

**This must be the last write to the file.** Any later `openpyxl...save()`, including a formatting pass, strips the cached values again; redo the recalculate-and-inject afterwards. Not needed on the live Excel path.

A clean recalc proves the formulas evaluate, not that they are right. Finish with a numbers pass:

- Every Check row reads 0, or the adjacent comment explains exactly why it cannot. The Y1-vs-latest-year movement row is not a check and will not be nil once payroll is CB-driven.
- Totals cross-foot and EBITDA reconciles to the source accounts.
- Every ingested source section foots to its own reported bottom line (net profit or loss as printed). If it does not, a line was mistyped or omitted — find it before wiring anything to it.
- Derived columns reconcile: an LTM column equals its components line by line, and a consolidated balance-sheet column equals net assets as printed.
- Cross-foot the analysis tabs: customer listings sum to the seller's stated totals, and category breakdowns account for every row with a residual row for anything uncategorised. Watch label mismatches — an em-dash in the source against a hyphen in the formula silently returns zero.
- No error cells anywhere: scan every sheet of the recalculated copy for values beginning with `#`.
- Column A contains only `x` and blanks on every tab.
- Recompute the headline figures independently from the source files and compare.
- Re-read every assertion written into a comment cell and confirm it against the source — a stated range, ratio or proportion that the data does not support is worse than no comment.
- Check the target column of every SUMIF/SUMIFS/COUNTIFS and cross-sheet link. A formula pointing one column off is the commonest defect here and it recalculates cleanly.
- Render a page to PDF and look at it. Clipped comments, overlapping headers and a number format showing "0K" only show up visually.

On high-stakes models, have a separate agent that has not seen the build verify the numbers and conventions against the source files.

Deliver the workbook (and the companion source file, if built) with a short note listing: tabs built, key assumptions, and the data-request list. Lead with anything found that materially changes the read on the deal (customer concentration, recurring-revenue mix, gross churn, a disagreement between source files). Do not narrate the whole model — the Legend does that.
