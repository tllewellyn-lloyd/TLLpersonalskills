# Tab layouts — cell-level patterns from the Dizions Master reference model

These are the proven layouts for the analytical blocks. Adapt line items to the deal; keep the shapes.

## PL tab

Section 1 is `P&L` and starts on **row 1** — no title row above it. Column
pattern:

```
A    B            C            D       E       F       G       H       I      J   K           L
x    P&L
     <note: A = actual, F = seller forecast, unsupported>
                  31st May YE
     line item    Grouping     FY2024A FY2025A FY2026A FY2027F FY2028F FY2029F    Tern Y1 PL  Comments - Tern Y1 basis
```

Row 3 holds the financial year end in column C and nothing else — `31st May
YE`, `31st Dec YE`. No basis banner and no "Tern view" header.

Carry **every year the seller provided**, forecast as well as actual, suffixed
`A` or `F`. Tern Y1 mirrors the current financial year's forecast column.

**Nothing to the right of the Y1 comment column.** No Difference column, no
CAGR column, no second comment column. Y1 comments are one short line each.
The Check rows span every year column.

Subtotal rows (Total Revenue, Total COGS, Gross Profit, Total Overheads, PBT,
EBITDA, Adj EBITDA) take the grey `EFEFEF` bold treatment; the column header
row takes orange `F79646` with white bold text.

Below the summary: the Check rows, then one section per source document, each
with a Tern mapping column, e.g.:

```
x  Feb-26 adjusted accounts taken from "Dizions Limited Accounts 28 Feb 2026"

   Category            | 28 Feb 2026 (£) | 31 Mar 2025 (£) | Tern mapping                     | Assumed supplier run?
   Sales               | 1,334,822       | 1,448,647       | Turnover - Recurring - Software  | N
   Purchases           | 73,236          | 108,996         | COGS - Recurring - Software      | Y
   Directors salaries  | 130,706         | 200,579         | C&B                              | N
   ...
```

The PL does **not** carry a seller-vs-Tern subtotal reconciliation section or
an EBITDA bridge section. Where the seller's own subtotals disagree with their
line detail, say it in a Y1 comment and raise a QA data request.

Management accounts and stat accounts each get their own section per year.

## B (Budget) tab

The target's budget/actuals in their own shape — months across, with Actual|Budget column pairs under merged month headers, Annual Total and prior-year columns at left. Append two Tern columns at the right of every row: the annual figure (formula) and **Tern mapping** to the standard taxonomy. This is what lets the PL tab SUMIF straight off the target's own budget layout.

## CB (Compensation & benefits) tab

**Staff listing comes first**, summary blocks below.

The listing ends at **Fully loaded annual cost**:

```
Ref | Job title | Location | Work pattern | Legal entity / BU | Division / dept |
Employment type | Date of birth | Start date | Currency | Fully loaded annual cost | K or N
```

Do not carry the seller's salary / bonus / benefits component columns into the
listing. Where they are incomplete or do not foot, note it beside the table and
raise it on QA.

**`K or N`** sits immediately after the cost column and is Tern's, not the
seller's: K = keep in the Tern Y1 payroll, N = exclude. Set every row to `K` on
first build, with a note saying the deal team flips rows to N as leavers and
post-completion changes are agreed. The PL tab's Y1 `C&B` and `Contractors`
lines are SUMIFS over this listing filtered on employment type and this flag,
so the Y1 payroll updates the moment a row changes.

Sections below the listing:

1. `CB summary (Tern)` — heads and fully loaded cost by division and employment
   type, formula-driven off the listing.
2. `C&B reconciliation (Tern)` — listing total, less contractors, less anyone
   who started after the year end, against the P&L C&B charge, with the
   residual in GBP and as a % of the charge.
3. Headcount, leases, and any deal-specific recalculations (bonus schemes,
   redundancy costs by age and service, holiday accrual, pension testing).

Directly beneath the listing total, add `Check - CB listing vs latest P&L C&B
(<year>) (Tern)`:

```
   Total C&B cost per the CB listing above (K rows)   | <formula>  | Fully loaded, permanent and contractor
   less: P&L C&B charge, <latest year>               | =-PL!<C&B> | Link to the PL tab
   Difference - listing over the P&L charge          | =SUM(..)   |
   of which contractors                              | =SUMIFS(..)| No Contractors line in the seller P&L
   Difference excluding contractors                  | <formula>  | Like-for-like, permanent only
   as % of the <latest year> C&B charge              | <formula>  | Negative = listing below the charge
```

The P&L holds costs as negatives, so the difference row is a SUM and the
percentage divides by the negated charge.

## WC (Working capital) tab

```
x  WC calculation (Tern) - <Month-YY> P&L
   Note: per the LOI - "<exact LOI wording of the WC deduction>"
   Working capital (1 month)   | <value>
   Owner's monthly salary      | <value>
   WC adjustment               | <value = WC minus owner salary>

   Category                    | <period> | Tern mapping
   ...one row per P&L cost line for the reference month, mapped...
   Total Costs                 | <sum>
```

Run it for more than one reference month when the months differ materially; keep both sections.

## BS tab and NTA block

Balance sheets in a **consolidated table** — one row per line item, one column per period (newest first). This gives a single scannable view across years rather than separate sections per period:

```
x  Balance sheets — Source: <files>
   Line item             | 31 May 2025 | 31 May 2024 | 31 May 2023
   Fixed Assets
     Tangible assets      | 53,169      | 55,790      | 49,172
     Investments          | 115,269     | 111,113     | 100,168
   Current Assets
     Debtors              | 487,283     | 450,723     | 366,802
     Cash at bank         | 1,005,652   | 829,483     | 605,929
   ...
   Net Assets             | 1,206,805   | 1,057,019   | 854,207
```

Section headings within the table (Fixed Assets, Current Assets, Current Liabilities, etc.) are bold. Sub-totals and Net Assets are also bold. Account-level detail breakdowns (office equipment, other debtors, prepayments, accruals…) as separate sections below if available.

```
x  NTA calculation (Tern)
   Note: per LOI "<exact LOI NTA definition, including the LBD>"
   Opening NTA from <LBD> BS   | <value>
   Adjustments:
   <named adjustment>          | <-value> | <reasoning / source>
   ...
   Adjusted NTA                | <value>
```

Every adjustment named with reasoning — unaccrued bonuses, pre-completion pension payments, accrued CT, accrued audit fees, irrecoverable AR, etc.

## EB (Equity bridge / entry assumptions) tab

Sections: `Entry Assumptions`, `Valuation at entry`, `Investment return metrics (sources and uses)`, `Summary included in OFFER LETTER`, `Key metrics for investment deck`, `MoM Multiple`.

Entry Assumptions block — left column of deal metrics, right block of cash balances as of a stated date:

```
   ARR                                  | <K> | Tern Y1 PL     ← link, green
   EBITDA                               | <K> | Tern Y1 PL
   Enterprise Value (Total)             | <K>
   Enterprise Value (Day 1)             | <K>
   EV (Total) / EBITDA x                | <x>
   NTA                                  | <K>
   <NTA-to-equity adjustments, named>   | <-K> | <reasoning>
   Working Capital                      | <-K> | <basis, consistent with LOI>
   Equity Value (Total / Day 1)         | <K>
   Up front / Deferred guaranteed / Deferred Yr-3 | <K>
   Day 1 EV/ARR x, Day 1 EV/EBITDA x, Funds drawn/EBITDA x
```

Sources and uses: two columns (Sources GBP | Uses GBP) with footnoted comments; totals must equal.

`Summary included in OFFER LETTER`: payments table — Day 1 | End of Y1 | End of Y2 | End of Y3 | Total, with an NTA/WC adjustment row.

## R / ARR tabs

`R summary` first, then Tern testing and pivots, each `taken from '<source>'`: revenue by customer, sales by income stream, recurring vs one-off split, customer mapping. ARR testing methodology is written as numbered steps before the table:

```
x  ARR testing (Tern)
   Methodology
   1. Extract the ARR breakdown from the "ARR" tab for the N customers tested (top 30 + random sample)
   2. Take the ARR per the contracts provided in the "CN" tab
   3. Compare the two
   4. For differences, request explanations/documentation supporting the seller-provided ARR
   5. Final ARR based on contract testing in column <X>
   6. Customers that "failed" ARR testing → cash testing on tab "CA"

   Customer Ref | Name | Licence Type | Payment frequency | Total ARR || Billing frequency | Services/Products | Start date | Initial end date | Auto-renewal clause | Effective end date | Total annual pricing || Difference vs contract | ...
```

### Gross churn calculation (its own section, below revenue by customer)

A full section in its own right — `x` in column A, title in column B, values
from column B across. Not an indented sub-section.

```
   Gross churned revenue (£)  | <formula> | <formula> | <formula> | <formula>
   Gross churn rate (%)       | <formula> | <formula> | <formula> | <formula>

   Note: Gross churn does not net off expansion revenue from existing customers.
   It measures only revenue lost from customers whose revenue decreased or who churned entirely.
```

Formula for churned revenue per year: `=SUMPRODUCT((prior_col-current_col)*((prior_col-current_col)>0))` across all customer rows. This sums only the decreases (where prior > current), ignoring expansion. Blank cells are treated as zero.

Gross churn rate: `=IFERROR(churned_revenue/prior_year_total,"")`. The first year has no prior column and is left blank.

Churn analysis (CH) per revenue stream: total recurring, then per-product cuts, with churn-reason listings from the seller as their own sections.

## PP (Pipeline) tab

Pipeline and forecast data with probability weightings and risk-adjusted values. Use formulas for computed columns so the table recalculates when inputs change.

```
x  FY27 pipeline and forecast — Source: <file>
   Category                     | Gross value (£) | Probability | Risk-adjusted (£) | % of total | Commentary
   Contracted revenue           | 350,000         | 100%        | =C{r}*D{r}        | =formula   | Revenue already secured...
   Expected renewals             | 1,200,000       | 98%         | =C{r}*D{r}        | =formula   | Based on renewal history...
   Existing customer expansion   | 500,000         | 50%         | =C{r}*D{r}        | =formula   | Upsell/cross-sell...
   New business pipeline         | 900,000         | 33%         | =C{r}*D{r}        | =formula   | Weighted by sales stage...
   Services / implementation     | 300,000         | 90%         | =C{r}*D{r}        | =formula   | Includes contracted...
   Total                        | =SUM            |             | =SUM              | 100%       |
```

Risk-adjusted column is a formula (`=gross × probability`). % of total is a formula (`=IFERROR(risk_adjusted/total,"")`). Gross values and probabilities are blue-font inputs. Commentary explains the basis for each probability weighting.

## Slides tab

Output staging for the investment deck: key metrics, P&L for deck, customer concentration/tenure, churn reasons, pipeline, competitor comparison — each section `- last updated DD/MM/YYYY`. Whether Slides replaces S+CH is a per-deal choice noted in the Legend.
