# Model conventions — formatting, provenance, hygiene

## Font and palette

Taken from `MASTER_template_PL.xlsx`. This is the current Tern standard and
overrides any generic guidance from the `xlsx` skill.

- **Font: Nunito 11 throughout**, every tab, every cell. Preserve bold, italic
  and font colour already set; only family and size are forced.
- **Section header rows** (`x` in column A): yellow `FFFF00` fill, black bold
  text, across the full row width.
- **Table column header rows**: orange `F79646` fill, white `FFFFFF` bold text,
  right-aligned over value columns.
- **Sub-header / banner rows**: orange `FF6600` fill, white bold text.
- **Subtotal and total rows**: grey `EFEFEF` fill, black bold text.
- Gridlines off on every sheet.
- Merge period-spanning header cells rather than repeating the label in each
  column. Set explicit row heights on rows with long wrapped comments: Excel
  auto-fits them, previews and PDF exports do not.

## Colour coding (font colours)

Keep the standard convention with exactly these meanings — do not overload them:

| Colour | Meaning |
|---|---|
| **Blue** | Input / hardcoded value (pasted source data, assumptions) |
| **Black** | Formula computed on the same sheet |
| **Green** | Cross-sheet link (formula referencing another tab) |
| **Red** | External link (another file) — avoid these; if the model needs a number from elsewhere, paste it as a blue input with provenance |

Do not use red text for narrative flags or comments — that overloads the meaning. Commentary lives in Comments columns/cells in normal text.

## Number formats and units

Financial statement tabs (PL, BS, R, CH) are held in **GBP full units** and
display in thousands with a `K` suffix: number format `#,##0,"K"`, where the
trailing comma does the scaling.

**Sellers routinely submit in GBP '000.** Restate those figures ×1,000 on
ingestion — exact, no rounding — and state it in the section's note. Never
apply `#,##0,"K"` to data already expressed in thousands: it divides by 1,000
a second time and silently renders £10,016K as £10K. Tabs whose source is
already in full units (staff listings, CRM pipeline exports) stay in units and
use `#,##0`.

Tern check and reconciliation rows use `#,##0.0,"K"` so that sub-£1k breaks
stay visible rather than rounding to `1K` — a £0.9k break displayed as `1K`
defeats the purpose of the check. This is the only place the one-decimal
variant is used.

Detail/raw sections otherwise keep the source's own precision. Percentages one
or two decimals (two on churn and other rates). Multiples `0.0x`. Dates
`DD/MM/YYYY`. Negative costs shown with a minus, not brackets, matching the
sign convention where costs are negative numbers.

### PL tab column widths

Per the master template: column A 5.0, line items 48.75, mapping 24.63, gap
columns 5.88, Tern Y1 24.63, comment columns 50–62, year columns ~14.

## Provenance labels

Every dataset section title states what it is and where it came from, using the `— Source:` format:

- `<what> — Source: <exact source filename>` for files (e.g. `FY26 staff listing — Source: Staff Breakdown & Costs.xlsx`)
- `<what> — Source: <filename>, <filename>` when a section draws from multiple files
- `<what> - received DD/MM/YYYY` or `- provided on DD/MM/YYYY` for dated deliveries
- `<what> - taken from "<email subject>" email DD Month YYYY` for numbers from emails
- `(Tern)` suffix on any section Tern computed rather than received, e.g. `CB summary (Tern) — Source: Staff Breakdown & Costs.xlsx, Management Accounts 2526.pdf`
- `- last updated DD/MM/YYYY` on living sections (QA data-request log, NTA adjustments)

The exact source filename is what lets anyone re-find the file in the dataroom months later.

## Version control hygiene

- When a new dataset supersedes an old one (new forecast, new pipeline export), **delete the superseded section/tab from the live model** — never stack V1/V2/V3. Stale tabs cause formulas silently pointing at outdated numbers.
- Before deleting, log in the QA tab's data-request log (the Legend no longer carries a change log): what was removed, when, what superseded it.
- If a genuine before/after comparison is needed, keep it in a separate backup spreadsheet outside the live master.
- When refreshing a same-shaped dataset, paste-values into the existing section rather than importing a new tab — paste-values preserves every downstream formula link.
- Rename default-named tabs (`Sheet1`, `Lookup (1)`, `Copy of ...`) before the model circulates. Raw system exports must be renamed, logged in the Legend, and wired into their standard tab by formula — never left as orphan dumps.
- Delete deprecated tabs (e.g. `Hosting and Software OLD`) once replaced. If history must be kept, use a clearly marked archive tab or a separate backup file.

## Section header formatting

All section header rows (rows with `x` in column A) must have a **yellow background fill** (`#FFFF00`) across the full row width (columns 1–15). This makes sections visually scannable when scrolling through a tab. Apply the fill programmatically in the scaffold and in any ingestion code.

Table column header rows inside a section take the orange `F79646` treatment, and subtotal rows the grey `EFEFEF` treatment, per **Font and palette** above. Re-apply the whole palette as a final pass after `scaffold_model.py` has run, since the scaffold writes its own interim styling.

## General layout habits

- Column A is reserved for `x` section markers; content starts in column B.
- Each section separated by one or two blank rows.
- Notes rows directly under a section title state methodology or caveats (e.g. `Note: per the LOI - "Deduction for one month of normalised costs (excluding owner's salary)"`).
- Tern recalculation sections show their method as numbered steps before the numbers (see the ARR testing layout in tab-layouts.md).
- Merged cells only for period-spanning headers (e.g. month names over Actual/Budget column pairs); avoid elsewhere.
