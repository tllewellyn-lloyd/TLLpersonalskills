---
name: deal-data-request
description: >
  Build a populated Tern Capital financial analysis Excel workbook from a seller's data request file. Use this skill whenever the user has received a completed data request from a target company and wants to process it into the standard Tern deal workbook. Trigger phrases include "process the data request", "build the Excel for this deal", "populate the template", "create the deal workbook", "turn this into our format", "set up the Excel file for X", or any variation where a seller has returned a data file and James wants it turned into Tern's 6-tab analysis format. Also trigger when the user uploads or references a file named like "TC Data Request [Company].xlsx" or similar and asks to do something with it. The output is a .xlsx file saved to the deal's Google Drive folder with 6 tabs: L, PL, CB, CH, KM, PP.
---

# Deal Data Request — Excel Workbook Builder

This skill takes a seller's completed Tern Capital data request file and produces the standard 6-tab Tern deal workbook. The workbook is then saved to the deal's Google Drive folder.

## Tab structure

| Tab | Full name | Contents |
|-----|-----------|----------|
| L | Legend | Tab index, colour coding guide, abbreviations |
| PL | Profit & Loss | Historic financials + Tern Y1 budget model |
| CB | Team | Headcount and compensation data |
| CH | Churn | Recurring revenue churn analysis |
| KM | Key Metrics | Top customers and headcount metrics |
| PP | Pipeline | Sales pipeline data |

## Step 1 — Locate the source file

Check in order:
1. File uploaded in the current conversation
2. Google Drive deal folder (search for "TC Data Request" or the company name)
3. Ask the user if not found

The source file is typically named `TC Data Request [Company].xlsx` and contains sheets: L, Summary, Churn, Metrics, Team, Pipeline.

Also identify the Google Drive deal folder ID so the output can be saved there. Ask the user if it's not clear from context.

## Step 2 — Build the workbook

Use `openpyxl` in Python (via the bash tool). Work in the outputs directory.

### L tab (Legend)

Create a header row in Tern orange (`FFEB5C32`) with white bold text, then populate two sections:

**Tab index** — one row per tab:

| Tab | Full Name | Description |
|-----|-----------|-------------|
| L | Legend | This sheet — tab index, colour coding, abbreviations |
| PL | Profit & Loss | Historic P&L and Tern Y1 budget |
| CB | Team | Headcount and fully-loaded compensation |
| CH | Churn | Recurring revenue churn analysis |
| KM | Key Metrics | Top customers and headcount |
| PP | Pipeline | Sales pipeline (CRM data) |

**Colour coding guide** (below the tab index, with a blank row separating):

| Colour | Meaning |
|--------|---------|
| Blue text | Hardcoded inputs — raw source data |
| Black text | Formulas and calculated values |
| Green text | Cross-sheet references |
| Orange header | Section or tab header |

**Abbreviations** (below colour coding, with a blank row):

FY = Fiscal Year, LTM = Last Twelve Months, LC = Local Currency, ARR = Annual Recurring Revenue, NRR = Net Revenue Retention, GRR = Gross Revenue Retention

### PL tab (Profit & Loss)

This is the most important tab. It has two parts:

**Part 1 — The template (rows 1 to ~110)**

Copy the EXACT structure of the `Summary` sheet from the source file, cell by cell:
- Preserve all text labels, merged cells, formatting, and layout
- The `E` column (LTM / most recent period) is the live column — it will be fed by formulas from Part 2
- Columns B, C, D (historic years) keep their original hardcoded values from the source
- Use green font (RGB 0,128,0) for all formulas in the E column that reference Part 2 raw data below

**Part 2 — Raw source data (starting ~row 112, after a clearly labelled separator)**

Copy all numeric data from the source `Summary` sheet's LTM/current column below the template:
- Label the separator row clearly: `--- RAW SOURCE DATA (TC Data Request [Company].xlsx — Summary sheet) ---`
- Each row should have: the line item label, and the raw value in blue font (RGB 0,0,255)
- The formula in Part 1's E column for each line should be `=E{raw_row}` pointing to the corresponding raw data row below

If the source has named ranges or `#NAME?` errors in historic columns, hardcode the date values directly (e.g. `datetime.date(2021,12,31)`) rather than copying broken formulas.

### CB tab (Team)

Copy data from the source `Team` sheet. Include:
- Employee/role listing with fully-loaded costs
- Department breakdown if available
- Header row in Tern orange

### CH tab (Churn)

Copy data from the source `Churn` sheet. Include:
- Recurring revenue waterfall (opening ARR, new, expansion, contraction, churn, closing ARR)
- By year, as provided
- Header row in Tern orange

### KM tab (Key Metrics)

Copy data from the source `Metrics` sheet. Include:
- Top customers table (customer name, ARR, tenure, etc.)
- Headcount by department if available
- Header row in Tern orange

### PP tab (Pipeline)

Copy data from the source `Pipeline` or weighted pipeline file. Include:
- Pipeline by opportunity (customer, stage, value, weighting, weighted value)
- Summary totals at the bottom
- Header row in Tern orange

## Step 3 — Formatting rules

Apply consistently across all tabs:

- **Headers**: Tern orange fill (`FFEB5C32`), white bold text, font Calibri
- **Blue text** (`FF0000FF`): hardcoded inputs and raw source data values
- **Green text** (`FF008000`): formulas referencing other rows/sheets within the workbook
- **Black text** (`FF000000`): calculated formulas and totals
- **Number format**: `#,##0;(#,##0);-` for £ figures (thousands); `0.0%` for percentages; `0.0x` for multiples
- **Column widths**: set sensibly — label columns at least 35–40 wide, value columns 12–15 wide
- **Zero values**: display as `-` using format string, not the number 0

## Step 4 — Verify

Run the LibreOffice recalc script to check for formula errors:

```bash
python /path/to/skills/xlsx/scripts/recalc.py output.xlsx
```

Fix any `#REF!`, `#DIV/0!`, `#VALUE!`, or `#NAME?` errors before proceeding. Common causes:
- Named ranges from the source file that don't exist in the new workbook — hardcode these
- Separator rows that start with `=` — prefix with a single quote to force plain text
- Date formulas referencing missing named ranges — hardcode as `datetime.date` objects with `number_format = 'DD-MMM-YY'`

## Step 5 — Name and save

Name the file: `H{YYMMDD}_{Ticker}_Financial_Analysis.xlsx`  
Where `{YYMMDD}` is today's date and `{Ticker}` is a short company code (ask the user if unclear).

Save to the deal's Google Drive folder. If the file exceeds what can be uploaded via the MCP tool in one call, present it to the user for manual download and ask them to drag it into the folder. Also note the Google Drive folder link for them.

## Notes

- Do not save any files to `G:\Shared drives\20 Deals\10 Live\H251201 - CDS-Cortus\10 Dataroom\40 P-Contractors` — that is a separate deal folder
- Always present the file to the user after saving, with a direct computer:// link
- If a pipeline file is separate from the main data request (e.g. a "Weighted Pipeline" xlsx), pull it in for the PP tab automatically if it's in the same Google Drive folder
