# Tab structure and naming

One master workbook per deal. Tabs are short codes; the Legend maps codes to names. Physical tab order in the workbook must always match the order in the Legend — that keeps the tab bar navigable without opening the Legend.

## Standard tab taxonomy

### Pre-LOI tabs

| Code | Name | Group |
|---|---|---|
| L | Legend | Other |
| A | Assumptions | Finance |
| S | Summary analysis | Finance |
| KM | Key Metrics | Finance |
| CH* | Key charts and graphs | Finance |
| PL | P&L (actuals and forecasts) — Tern Y1 PL and historic financials | Finance |
| BS | Balance Sheet | Finance |
| CF | Cash Flow | Finance |
| T | Corporation tax, PAYE/NI, VAT, R&D | Finance |
| CB | Compensation & benefits | Finance |
| PP | Sales Pipeline / forecast (CRM data, pipeline models) | Commercial |
| R | Revenue | Revenue |

*Note: in the Dizions model, CH was used for Churn data (Revenue group) and S for Support ticket data — codes get reused per deal. What matters is that the Legend defines what each code means for THIS deal.*

### Post-LOI tabs

| Code | Name | Group |
|---|---|---|
| CN | Contracts review | Commercial |
| CO | Corporate (Companies House) | Other |
| AR | Accounts Receivable / aged receivables | Finance |
| AP | Accounts Payable / aged payables | Finance |
| DI | Deferred Income | Revenue |
| DL | Debt-like items | Finance |
| OL | Other Liabilities | Finance |
| IC | Intercompany reconciliation | Finance |
| OBS | Other Balance Sheet items | Finance |
| QA | Questions & Answers | Other |

### Additional tabs seen in practice (add to the Legend when a deal introduces one)

| Code | Name | Group |
|---|---|---|
| C | Costs breakdown | Finance |
| WC | Working capital adjustment | Finance |
| EB | Equity bridge / entry assumptions | Finance |
| B | Budget | Finance |
| CA | Cash testing | Finance |
| EBb | (avoid duplicates — one code, one meaning) | — |
| SAR | Statutory accounts reconciliation | Finance |
| MA | Management accounts | Finance |
| ARR | Annual recurring revenue | Revenue |
| RD | Revenue data (raw) | Revenue |
| SD | Stickiness data | Commercial |
| SR | Stat register review | Other |
| Slides | Slides/output for investment deck (may replace S + CH — note the per-deal choice in the Legend) | Other |

Year-specific data tabs (e.g. `FY25`) and personal working-notes tabs (e.g. `KD`) are allowed but must be in the Legend.

## Tab groups and colours

Set the tab colour by group so the tab bar reads at a glance:

- **Finance** — green
- **Commercial** — red
- **Revenue** — pink
- **Other** (Legend, QA, Slides, SR) — blue

## Legend (L) tab layout

The Legend is the **tab map and nothing else**. One section, then the map. No
change log, no dataroom index, no section index — they crowded out the only
thing anyone opens the Legend for.

```
x    <Deal> - Tern Capital DD master model
     (blank row)
     Sheet   Grouping   Description                        Colour   Comments/Questions
     L                  Legend - this sheet                         <1-2 short sentences>
     PL      Finance    Tern Y1 PL and historic financials  Green   <1-2 short sentences>
     ...one row per tab, in physical tab order...
```

Write each **Colour** cell in the colour it names: "Green" in green `00B050`,
"Red" in red `FF0000`, "Pink" in pink `FF66CC`, "Blue" in blue `00B0F0`. The
map then reads together with the tab bar at a glance.

**Comments/Questions** is one or two short sentences per tab — the live issues,
not the analysis. A paragraph here is a sign it belongs on the tab itself or in
a QA data request.

Nothing goes in column A but the `x` marker, and nothing at all goes below the
map: `audit_model.py` reads column B under the header as tab codes, so stray
text there becomes a phantom tab and fails the audit.

The audit trail of seller files lives in the QA tab's data-request log.

## Section markers (the `x` convention)

Within every tab, each section is marked with an `x` in column A on the section-title row, with the section title in column B. Sub-sections use `x` in column B, title in column C. This makes every tab's contents queryable.

The `x` markers are what matter: they make every tab's sections queryable, and they are the only thing allowed in column A. The Legend carries no section index.

## QA (Questions & Answers) tab

Two sections:
1. `Q&A` — Question | Answer, capturing management's answers verbatim as received.
2. `Data requests / questions` — What's needed | Why / what it feeds | Target tab | Status. This is the running info request to the seller.
