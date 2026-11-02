# Notion page output template

Exact Markdown structure to use as the body content of the Notion page. Notion-flavored Markdown — the `notion-create-pages` tool parses this directly.

## Rules

- Do **not** include the company name as an H1 at the top. The Notion page title comes from the `Name` property; the body starts with H2.
- Use H2 (`##`) for each of the six section headings. Don't deviate from the section names below — keeping them consistent makes the pipeline easier to scan.
- Use GFM tables (with leading and trailing `|`) for the financial summary.
- Use bullets for everything else; prose only where genuinely needed (e.g. the company overview opener).
- For numeric values, match the IM's units (£m, $m, %, etc.). Don't convert.
- If a section has no data in the IM, still include the heading and write a single line: *"Not disclosed in IM — see Questions section."* Don't omit the heading.

## Template

```markdown
## Company overview

[1–3 sentence factual description of what the business does, the sector / sub-vertical, and any genuinely material context.]

- **Founded:** [year]
- **Headquarters:** [city, country]
- **Ownership:** [founder-owned / PE-backed by X / EOT / etc.]
- **Sector:** [B2B Enterprise Software — sub-vertical]
- **Milestones:** [optional — only if material; bullet 1–3 items]

## Products & use cases

- **[Product 1]** — [one-line description]. Used by [persona / customer type] to [problem solved].
- **[Product 2]** — [...]
- **[Product 3]** — [...]

**Deployment:** [SaaS / on-prem / hybrid]
**Pricing:** [per-seat / usage / flat fee / tiered — if disclosed]
**Tech stack:** [only if material — e.g. ".NET on Azure"; otherwise omit this line]

## Financial summary

| Year | Revenue | Recurring Revenue | EBITDA |
|------|---------|-------------------|--------|
| FY23 | £X.Xm   | £X.Xm             | £X.Xm  |
| FY24 | £X.Xm   | £X.Xm             | £X.Xm  |
| FY25 | £X.Xm   | £X.Xm             | £X.Xm  |
| FY26B | £X.Xm  | £X.Xm             | £X.Xm  |

[Optional one-line note below the table — e.g. "EBITDA is adjusted; reported FY25 was £X.Xm." Only if there's something the partners need to know.]

## Key commercial points

- **Customers:** [N total] (FY25), up from [N] in FY23
- **Top customers:** [Customer A, B, C — if disclosed by name]
- **Concentration:** Top 1 = X% of revenue, Top 5 = Y%, Top 10 = Z%
- **NRR:** X%  |  **GRR:** Y%  |  **Logo churn:** Z% p.a.
- **ACV:** £X
- **Sales motion:** [inbound / outbound / channel]
- **Geography:** [UK X%, US Y%, RoW Z%]

## Headcount & org

- **Total FTEs:** [N]  (FY25), up from [N] in FY23
- **By function:** Engineering [N], Product [N], Sales [N], Marketing [N], CS [N], G&A [N]
- **Locations:** UK [N], US [N], offshore [N]
- **Key management:**
  - [Name], CEO — [tenure / background, one line]
  - [Name], CFO — [tenure]
  - [Name], CTO — [tenure]
  - [Add others material to the deal]

## Questions for the advisor

1. [Specific, single-question phrased as you'd email the advisor]
2. [...]
3. [...]
4. [...]
```

## Worked example (truncated)

For a fictional company "Acme Compliance Limited":

```markdown
## Company overview

Acme provides regulatory compliance software for UK financial advisers — the platform automates suitability assessments, file reviews and FCA reporting. Sold direct to IFA networks and individual advisory firms.

- **Founded:** 2014
- **Headquarters:** Manchester, UK
- **Ownership:** Founder-owned (CEO holds 78%)
- **Sector:** B2B Enterprise Software — RegTech for UK financial services
- **Milestones:** Launched flagship product in 2016; added FCA Consumer Duty module in 2023

## Products & use cases

- **Acme Suitability** — automated suitability assessment workflow. Used by IFA paraplanners to generate FCA-compliant suitability reports.
- **Acme Review** — file review automation. Used by compliance officers to sample and review client files at scale.
- **Acme Reporting** — regulatory reporting. Used by network compliance heads to produce FCA returns.

**Deployment:** SaaS (multi-tenant, AWS-hosted)
**Pricing:** Per-seat tiered SaaS, with implementation fees

## Financial summary

| Year  | Revenue | Recurring Revenue | EBITDA |
|-------|---------|-------------------|--------|
| FY23  | £4.1m   | £3.6m             | £0.9m  |
| FY24  | £5.8m   | £5.2m             | £1.4m  |
| FY25  | £7.4m   | £6.9m             | £2.0m  |
| FY26B | £9.2m   | £8.7m             | £2.7m  |

EBITDA is adjusted (founder remuneration normalised); reported FY25 was £1.6m.

## Key commercial points

- **Customers:** 312 (FY25), up from 198 in FY23
- **Top customers:** [Network A], [Network B], [Network C]
- **Concentration:** Top 1 = 14% of revenue, Top 5 = 38%, Top 10 = 52%
- **NRR:** 118%  |  **GRR:** 96%  |  **Logo churn:** 4% p.a.
- **ACV:** £22k
- **Sales motion:** Inbound + outbound; growing channel motion via networks
- **Geography:** UK 100%

## Headcount & org

- **Total FTEs:** 48 (FY25), up from 31 in FY23
- **By function:** Engineering 18, Product 4, Sales 9, CS 6, G&A 11
- **Locations:** UK 42, offshore (India contractor) 6
- **Key management:**
  - Jane Doe, CEO & founder — 11 years; ex-FCA
  - John Smith, CFO — 2 years; ex-Big 4
  - Priya Patel, CTO — 4 years; ex-fintech scaleup

## Questions for the advisor

1. Can you share a revenue split by product (Suitability / Review / Reporting) for FY24 and FY25?
2. What is the NRR by customer cohort (vintages 2018–2022)?
3. Could we get an anonymised top-50 customer file with ACV, contract end date and renewal status?
4. Bridge from reported EBITDA (£1.6m FY25) to adjusted (£2.0m) — what's in the £0.4m of adjustments?
5. Are any of the top 10 customer contracts on auto-renew, and do any have change-of-control consent rights?
6. What's the Q1 FY26 trading actuals vs. budget?
7. Confirm IP ownership — is all source code held by the UK trading entity?
```
