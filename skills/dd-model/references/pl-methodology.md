# P&L methodology — historic mapping and the Tern Y1 build

## The PL tab's job

One table that puts the target's historicals (stat and management accounts) and Tern's Year-1 view side by side, every line mapped to a standard taxonomy, every Y1 judgement explained in its comment. It must reconcile back to the statutory accounts — that is why the layout runs all the way to PBT even though decisions are made at EBITDA.

## Standard column pattern

```
line item | Grouping | FY..A | ... | FY..F | ... | (gap) | Tern Y1 PL | Comments - Tern Y1 basis
```

The `P&L` section starts on row 1 — no title row above it. Row 3 carries the
financial year end in column C (`31st May YE`) and nothing else: no basis
banner, no "Tern view" header.

Carry **every year the seller provided**, forecast as well as actual, suffixed
`A` or `F`, and note under the section title that the F years are unsupported.
**Nothing goes to the right of the Y1 comment column**: no Difference column,
no CAGR column. Y1 comments are one short line each. The Check rows span every
year column.

## Standard line taxonomy

Revenue and COGS split recurring vs non-recurring first, then by stream. Include all standard lines even when zero — a zero line documents that the stream was considered.

```
Turnover - Recurring - Software
Turnover - Recurring - Maintenance
Turnover - Recurring - Managed Services
Turnover - Recurring - Transactions
Turnover - Non-Recurring - Software
Turnover - Non-Recurring - Prof Services
Turnover - Non-Recurring - Hardware
Turnover - Non-Recurring - Other income
Total Revenue                              (+ YoY growth % row beneath)

COGS - Recurring - Software
COGS - Recurring - Maintenance
COGS - Recurring - Managed Services
COGS - Recurring - Transactions
COGS - Non-Recurring - Software
COGS - Non-Recurring - Prof Services
COGS - Non-Recurring - Hardware
COGS - Indirect
Total COGS

Net Revenue/Gross Profit                   (+ GM % row beneath)

C&B                    | Contractors      | Recruitment
Professional Fees      | Marketing        | IT & Systems
Insurance              | Property         | Travel & Subsistence
Interest expense       | Depreciation     | Amortisation
Other
Total Overheads

Profit Before Taxes (PBT/EBT)
  add back: Interest Expense, Amortisation, Depreciation, R&D tax credit
EBITDA
  Addback 1..4 (named in Comments, e.g. "Director costs for exiting owner", "One-off advisory fees")
Adj EBITDA

Check    (source-total minus mapped-total; must be 0 for every column)
```

Costs are negative, revenue positive; the sign convention makes every subtotal a plain SUM.

## Mapping the source accounts

Below the P&L, each source dataset is its own section (see tab-layouts.md) with a **Tern mapping** column assigning every source line to one taxonomy line. The P&L's historic columns are then formula-driven (SUMIF on the mapping column), so re-mapping a line updates the P&L automatically. The Check row catches anything unmapped.

Where useful, add an annualised column next to part-year actuals (`28 Feb 2026 (£)` → `28 Feb 2026 annualised (£)`) and a flag column such as `Assumed supplier run?` for costs expected to continue.

## Building the Tern Y1 P&L

1. **Y1 is based on the current financial year** — the seller's forecast for the year in progress (FY2027F where the last actual is FY2026A), not the last actual and not the final forecast year. Mirroring a forecast imports management's growth assumptions wholesale, so state that in the Y1 basis comment and make the forecast's support a Critical data request. The Y1 column is a same-sheet formula linking to the latest year's data: `=G{row}` (or whichever column holds the most recent financials). This means Y1 starts as an exact mirror of the latest year with **no adjustments applied** — no cost-saving guesses, no assumptions about what might change. Adjustments, if any, are made later by the deal team after review. Use black font for the Y1 column (same-sheet formula convention).
2. **Items not in the Sage/source detail** (e.g. depreciation from stat accounts only) get a blue-font hardcoded value in the latest-year column, and Y1 still links to it via formula.
3. **Exception — payroll is built, not mirrored.** Y1 `C&B` and Y1 `Contractors` are SUMIFS over the CB staff listing, filtered on employment type and the `K or N` keep flag:

   ```
   C&B          =-SUMIFS(CB!<cost>,CB!<employment type>,"Permanent",CB!<K or N>,"K")
   Contractors  =-SUMIFS(CB!<cost>,CB!<employment type>,"Contractor",CB!<K or N>,"K")
   ```

   Green font, since these are cross-sheet links, and both tabs must be in the same units. The deal team then drives Y1 payroll by flipping individual rows on CB from K to N, with no formula edits.

   Two consequences to handle explicitly. First, Y1 payroll will not equal the latest year, so the Y1-vs-latest difference is a *movement*, not a check — show it as a labelled row beneath the Check rows and say what drives it. Second, if contractor costs already sit inside COGS in the seller's P&L (they usually do, where there is no separate Contractors line), adding them to the Y1 overhead counts them twice. Flag that in the Y1 comment and raise it as a Critical data request rather than silently netting it off.
4. **Conservatism is stated, not silent.** "Assume current ARR with no increases", "Minimum of historicals", "Assume 0" — write the stance in the Comments cell so the reader knows the number is a choice.
5. **Addbacks** normalise historic EBITDA (owner costs, one-offs, non-recurring pension payments) — each named, each its own line. Addback values are blue-font inputs in the historic columns; Y1 links to them via formula.

## Cost summary blocks

Every material cost category feeding the Y1 P&L (cost of sales, marketing, professional fees, other/sundry...) gets its own formula-driven summary block, mirroring the Revenue treatment. This is what makes refreshes mechanical: paste new source data in the same shape and everything downstream recalculates, instead of the P&L needing re-wiring each time.

## Hardcodes

Never bury a hardcoded override inside a formula (`=262000*2` is a red flag). Surface it in a labelled cell — on the Assumptions tab if one exists, otherwise in a clearly labelled cell near the point of use — with a note on its source, and reference that cell.
