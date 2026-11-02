---
name: tern-investment-deck
description: "Build, populate, or review Tern Capital investment review decks (.pptx). Use this skill whenever the user asks to create an investment deck, deal review, investment review, deal memo, or investment committee presentation for Tern Capital. Also trigger when the user asks to add slides to or review an existing investment deck, references a target company in the context of a deck, or says things like 'create a deck for X', 'investment review for X', 'build the deck', 'populate the slides', 'update the investment deck', or 'review the deck structure'. This skill defines mandatory and optional slide sections, exact content rules per section, and key metrics definitions. Always combine this skill with tern-brand-guidelines and tern-slide-formatting — if any conflict exists between this skill and tern-brand-guidelines, tern-brand-guidelines takes precedence."
---

# Tern Capital — Investment Deck Skill

This skill defines the structure, mandatory/optional sections, and content rules for all Tern Capital investment review decks.

**Always load these two skills before building or reviewing any slide:**
- `/mnt/skills/organization/tern-brand-guidelines/SKILL.md` — master brand reference (takes precedence on conflicts)
- `/mnt/skills/organization/tern-slide-formatting/SKILL.md` — full slide layout and element rules

**For PPTX tooling and QA:** read `/mnt/skills/public/pptx/SKILL.md`.

---

## Table of contents

1. [Deck structure overview](#1-deck-structure-overview)
2. [Mandatory slides — detailed rules](#2-mandatory-slides--detailed-rules)
3. [Optional slides — detailed rules](#3-optional-slides--detailed-rules)
4. [Key metrics definitions](#4-key-metrics-definitions)
5. [Exec summary decision rules](#5-exec-summary-decision-rules)
6. [Deal facts — inclusion thresholds](#6-deal-facts--inclusion-thresholds)
7. [Cross-cutting content rules](#7-cross-cutting-content-rules)
8. [Slide order](#8-slide-order)

---

## 1. Deck structure overview

| # | Section | Slides | Mandatory? |
|---|---------|--------|------------|
| 1 | Cover | 1 | Yes |
| 2 | Disclaimer | 1 | Yes |
| 3 | Section divider — Executive summary | 1 | Yes |
| 4 | Executive summary | 1–2 | Yes |
| 5 | Section divider — Investment thesis | 1 | Yes |
| 6 | Investment thesis | 1 | Yes |
| 7 | Section divider — Product, customers & market | 1 | Yes |
| 8 | Key products | 1 | Yes |
| 9 | Customer metrics | 1 | Yes |
| 10 | Target market analysis (TAM/SAM/SOM) | 1 | Yes |
| 11 | Market overview | 1 | Yes |
| 12 | Competitive analysis | 1 | **No** (either/or — see §3) |
| 13 | Section divider — Value creation & growth | 1 | Yes |
| 14 | Value creation summary | 1 | Yes |
| 15 | Cross-sell potential | 1 | Yes |
| 16 | AI plan | 1 | Yes |
| 17 | Updated org structure | 1 | Yes |
| 18 | On-prem to cloud migration | 1 | No |
| 19 | Section divider — Financials & key metrics | 1 | Yes |
| 20 | RR growth + gross/net churn | 1 | Yes |
| 21 | Historic P&L | 1 | Yes |
| 22 | LTM vs Y1 EBITA bridge | 1 | Yes |
| 23 | 52W cash flow forecast | 1 | No |
| 24 | Cash flow upside | 1 | No |
| 25 | Key risks & mitigation | 1 | Yes |
| 26 | Sources & uses of capital | 1 | Yes |
| 27 | MoM — EBITA multiple matrix | 1 | Yes |
| 28 | Section divider — Appendix | 1 | No |
| 29 | Primary interviewees / customer reference calls | 1 | No |

---

## 2. Mandatory slides — detailed rules

### 2.1 Cover slide

- Background: Tern Orange (#EB5C32).
- Company name: large, bold, white, vertically centred or slightly above centre.
- Title: "Investment Review" (or deal-specific subtitle, e.g. "Buy & Build Platform").
- Confidentiality: "FOR DISCUSSION" bold 11pt white; "Strictly private and confidential" 8pt Tern Orange on white pill, bottom-centre.
- TernCapital wordmark: top-right, reversed variant (white "Capital").
- No slide number on cover.

### 2.2 Disclaimer

- Full-page 8–9pt legal disclaimer text.
- TernCapital wordmark top-left.
- Slide number bottom-right.
- No orange bars, no KPI boxes.
- Standard disclaimer text covers: not a prospectus; not investment advice; financial promotion carve-outs under FSMA; no liability; confidentiality obligations; restrictions on distribution.

### 2.3 Section divider slides

- Use between each major section.
- Background white; orange ink nature sketch illustration right ~60% of slide.
- Bold 24–32pt title, near-black, left-centre. Sentence case.
- Slide number bottom-right. No footnotes.
- Standard section titles: "Executive summary", "Investment thesis", "Product, customers & market", "Value creation & growth", "Financials & key metrics", "Appendix".

### 2.4 Executive summary (1–2 slides)

**Every exec summary slide must include:**

- **Overview of business** (left column, body text): what the business does, who it serves, why it is mission critical, key integrations.
  - If business is > 15 years old: state the age prominently. The Lindy effect is a positive signal.
  - Include key product use cases and explain mission criticality.
  - If lots of data integrations in and out: explain them.
- **Deal facts box** (see §6 for thresholds): always included.
- **Key metrics table** (see §4 for definitions): always included.
- **Customer logos**: show top 5 household names from top 10 customers. If fewer than five household names, remove this section entirely.
- **RR growth chart OR EBITA bridge** (not both — see §5 for decision rule).
- **Value creation bullets**: brief, punchy. Include commercial (lead gen, cross-sell, price increase) and cost savings. Standalone bullet style.
- **Investment returns** (if applicable): funding structure summary, other pipeline context.

Footnote every key metric in the table. See §4 for standard footnote definitions.

### 2.5 Investment thesis

One content slide. Three sub-sections in orange header bars:

1. **Market context**: why now. Regulatory tailwinds, macro factors, demand drivers.
2. **Why [company]**: product/competitive differentiation, customer tenure, key financial highlights, any notable discounts vs benchmark.
3. **Financially attractive**: gross margin, tax losses, contracted ARR, valuation multiple vs benchmark.

Each sub-section uses the orange header bar format (white text, 11pt, square corners).
KPI callout column on right: pull out 2–4 key stats (e.g. average tenure, ARR secured, % discount vs benchmark).
Include footnotes for every referenced figure.

### 2.6 Key products

One content slide. Use orange header bar per product module.

For each product: 3–6 standalone bullet points describing functionality. All bullets end with a full stop.
Additional modules (lower priority): list with brief one-line descriptions.
Footnotes for any version/compatibility caveats.

### 2.7 Customer metrics

One content slide. Full customer table with these columns:
- Customer name
- ARR (£K)
- On-prem / cloud
- Customer tenure
- Live integrations
- Support tickets p.a.
- Contract expiry

Below the table: 4–5 KPI callout boxes. Standard KPIs:
- Average customer tenure (years)
- % ARR contracted until [date]
- Customers migrated to cloud
- Average customer integrations
- On-prem upsell opportunity (number of customers)

Footnotes: explain any customers without signed contracts; explain any managed services vs software distinctions; note completion deliverables.

### 2.8 Target market analysis (TAM/SAM/SOM)

One content slide. Orange header bar for introductory context paragraph.
Structured table with rows: PIMSS Average ARR, TAM, SAM, SOM. Columns: per product (Asset Management, Compliance, Viability, etc.).
KPI callout: total ARR uplift potential (e.g. "£2.3–3.6M ARR uplift potential").
Footnotes: define TAM, SAM, SOM; source the data.

### 2.9 Market overview

One content slide. Mix of:
- Body bullets: market size, market context, concentration, regulatory urgency, government funding, structural shifts.
- KPI callouts: market size (£), key growth metric (e.g. £10B repairs spend), % still on spreadsheets, pricing advantage.

Source line at bottom: split with semicolons. Example: `Source: 2025 Global Accounts; Expert interviews.`

### 2.10 Value creation summary

One content slide. Four orange header bars covering:
1. Commercial — new lead gen (Tern playbook)
2. Commercial — new customer targets, cross-sell potential
3. Commercial — price increase potential
4. Cost savings from integration / operational improvements

Each bar: 2–4 standalone bullets. All bullets end with a full stop.

### 2.11 Cross-sell potential

One content slide. Two sub-sections:
1. Additional products to existing customers.
2. All products to other group customers (HoldCo cross-sell).

Use orange header bars per sub-section. Include a table or matrix if quantified ARR uplift is available.

### 2.12 AI plan

One content slide. Cover:
- Current AI usage (if any) in the product.
- Proposed AI initiatives post-acquisition.
- Expected impact on product quality, margin, or competitive positioning.
Use orange header bars to separate current vs planned. Avoid vague statements; be specific about use cases.

### 2.13 Updated org structure

One content slide. Org chart diagram. Show:
- Current structure (grey/light tones).
- Proposed changes post-acquisition (Tern Orange for new hires/roles, orange bars for reporting lines added).
- NED and Tern representation at board level.

### 2.14 RR growth + gross/net churn

One content slide. Two elements:
1. **RR growth chart** (from GSheets, Roboto font): show ARR by year with CAGR label.
2. **Gross churn table** and **net churn table**: year-by-year. If churn is low and a selling point, include explanatory note on stickiness.

Include margin analysis if it helps understand profitability or churn by product line.

### 2.15 Historic P&L

One content slide. Table: years as columns, P&L lines as rows (Revenue, Recurring Revenue, Gross Profit, EBITA, EBITA margin %).
Actuals labelled FY##A; forecasts FY##F. Show as £K or £M — be consistent.
Footnotes: any accounting adjustments, normalisation assumptions.

### 2.16 LTM vs Y1 EBITA bridge

One content slide. Waterfall chart or structured table showing:
- LTM EBITA starting point.
- Cost reduction items (labelled individually).
- Revenue growth assumption.
- Y1 EBITA.

Footnote: standard Y1 EBITA footnote (see §4). Note: use EBITA not EBITDA throughout.

### 2.17 Key risks & mitigation

One content slide. Table: three columns: Risk, Detail, Mitigation.
Use orange header bar as table header row. Rows: light grey horizontal lines only, no outer border.
Cover: customer concentration, key person dependency, contract status, competitive risk, regulatory risk, technology risk.

### 2.18 Sources & uses of capital

One content slide. Two-section layout (orange header bars):
1. **Sources**: equity, existing cash on balance sheet, deferred payments.
2. **Uses**: Day 1 consideration, WC adjustments, transaction costs (if applicable), deferred payments, management fee.

Present as £K table. Ensure sources = uses. Footnote assumptions.

### 2.19 MoM — EBITA multiple matrix

One content slide. Matrix: rows = exit EBITA multiples; columns = MoM return multiples (or years to exit). Show base / upside / downside scenarios.
Title: "MoM — EBITA and EBITA multiple matrix". Use EBITA not EBITDA in all labels.

---

## 3. Optional slides — detailed rules

### 3.1 Competitive analysis (include one of the following)

Must include **one** of:

**Option A — Product feature / pricing comparison table:**
- Rows: competitors. Columns: key features, pricing tier.
- Use ✓ / ✗ / ~ for feature presence. Orange header bar for column headers.

**Option B — Competitor matrix:**
- 2×2 or similar visual matrix (e.g. Specialist vs Generalist × Low cost vs High cost).
- Company names plotted as labels. PIMSS highlighted in Tern Orange.

Decision: use Option A if there are clear feature differentiators. Use Option B if the positioning story is primarily about market segment or price.

### 3.2 On-prem to cloud migration

Include if on-prem to cloud migration is a key value creation lever. Show: number of on-prem customers, ARR at risk vs ARR opportunity, migration timeline, expected ARR uplift.

### 3.3 52W cash flow forecast

Include if liquidity management is a material concern post-acquisition. 12-month rolling CF table.

### 3.4 Cash flow upside

Include if there are identifiable near-term CF catalysts (e.g. tax loss recovery, VAT reclaim, deferred income release).

### 3.5 Appendix — primary interviewees / customer reference calls

Include if primary research was conducted. Table: Name, Company, Role, Date, Key insights (1–2 bullets).

---

## 4. Key metrics definitions

These definitions are fixed. Use them verbatim in the key metrics table and footnotes.

| Metric | Definition |
|--------|-----------|
| ARR | Latest available software ARR. In select sales, include highly repeatable recurring revenue where: the service is mission critical, customer tenure is long, and revenue does not fluctuate more than +/−10% YoY. |
| EBITA Y1 | Tern's view of the target's first year EBITA based on predictable cost reductions and conservative revenue forecasts. Always EBITA — never EBITDA. |
| Day 1 payment | Day 1 consideration + one-off redundancy costs if known (exclude if not) + WC/NTA/Net Debt adjustments if clearly known (exclude if not). Excludes transaction costs. |
| Deferred guaranteed | Only show amounts guaranteed and not dependent on any performance of the business. |
| Enterprise value (EV) | Sum of Day 1 payment + deferred guaranteed. |
| Equity / EBITA | Day 1 payment ÷ EBITA. |
| EV / EBITA | Enterprise value ÷ EBITA. |

### Standard footnote definitions (copy verbatim into slide footnotes)

| Reference | Footnote text |
|-----------|--------------|
| ARR | ARR includes [describe any non-standard recurring revenue included]. |
| Day 1 EV | Day 1 enterprise value without adjustments for NTA/WC. |
| Deferred guaranteed | Deferred payment split over [X] years and is guaranteed. There is an additional £[X]M deferred contingent based on [condition]. |
| Funds drawn | Additional drawdown to cover working capital, deferred payments (not funded from internally generated cash) and Tern management fee. |
| EV (distressed) | Total cash commitment for purchase price and working capital. |
| EV (healthy) | Total consideration + earnout in base case scenario. |
| Y1 EBITA | Based on: 1) cost reductions; 2) revenue growth based on average of previous three years; 3) including NED costs; 4) excluding Tern costs. |
| Benchmark multiple | Benchmark [X]x EBITA multiple based on the most comparable acquisitions from [source companies] where the equity (upfront consideration) as a multiple of EBITA is provided. |

---

## 5. Exec summary decision rules

### RR growth chart vs EBITA bridge

- If RR CAGR > 15% each year: **show RR growth chart.** Do not show EBITA bridge on exec summary.
- If RR CAGR ≤ 15%: **show EBITA bridge instead.** Do not show RR growth chart on exec summary.
- The RR growth chart and EBITA bridge will both appear in the Financials section regardless of this decision.

---

## 6. Deal facts — inclusion thresholds

Show the deal facts box on the exec summary. Only call out each fact if it meets its threshold:

| Fact | Include if… |
|------|-------------|
| Off-market | Yes → list |
| Mission critical software | Yes → list |
| % recurring revenue | > 90% → list |
| Y1 EBITA margin | > 30% → list |
| RR CAGR | > 15% → list |
| Median customer tenure | > 5 years → list |
| Average contract term | > 3 years → list |
| Gross churn | < 7% → list |

If a fact does not meet its threshold, omit it from the deal facts box entirely.

---

## 7. Cross-cutting content rules

These rules apply across all slides in any investment deck.

### Numbers and metrics

- Always EBITA — never EBITDA.
- Suffixes always capitalised: £10K, £5M, £2B. No space between number and letter.
- Ranges: hyphen, no spaces. £5-10M, 20-30%.
- K/M consistency: use the same unit throughout. Do not mix 185K and 37,000.
- Date format: DD-MMM-YY or DD-MMM only. Never DD/MM/YY.
- Actuals / forecasts: suffix with A or F. FY24A, FY25F.
- Negative numbers: dash, no space. -£3M.
- Months: first three letters only, no periods. Jan, Jun, Dec.
- Nations: use periods. U.K., U.S.

### Language

- Sentence case throughout — not Title Case.
- Active voice. "We will consult" not "a consultation will be undertaken".
- "We" not "I". Always "we" or "our".
- Spell out contractions where space permits. "do not" not "don't".
- Spell out one to ten; numerals for 11 and above (exceptions: units, tables, percentages).
- "na" for not applicable. Never "N/A".
- Omit "The" / "A" to shorten headings where possible.
- Bullets end with a full stop. Always.
- Sources split by semicolons. `Source: Tern Forecasts; Companies House.`

### Footnotes

- Format: `Notes: 1) [text]. 2) [text].`
- Space after closing parenthesis.
- Full stop at end of each footnote.
- Left to right, top to bottom ordering. Footnote 3 cannot precede footnote 2.
- Every figure referenced in the slide body must have a footnote below.
- Separate from main content with a light grey horizontal rule.
- "PRELIMINARY" label only on slides where data is not clearcut (feature comparisons, some CF slides). Not on standard data slides.

### Tables

- Horizontal light grey lines only — no outer borders.
- No bottom border on last row. Exception: key metrics tables keep all borders.
- Orange box / table header text: white only.
- Square corners on all boxes. Never rounded.
- Column headers as short as possible. Avoid word-wrap.

---

## 8. Slide order

The canonical slide order is:

1. Cover
2. Disclaimer
3. Section divider — Executive summary
4. Executive summary (1–2 slides)
5. Section divider — Investment thesis
6. Investment thesis
7. Section divider — Product, customers & market
8. Key products
9. Customer metrics
10. Target market analysis
11. Market overview
12. Competitive analysis *(optional — if included, place here)*
13. Section divider — Value creation & growth
14. Value creation summary
15. Cross-sell potential
16. AI plan
17. Updated org structure
18. On-prem to cloud migration *(optional)*
19. Section divider — Financials & key metrics
20. RR growth + gross/net churn
21. Historic P&L
22. LTM vs Y1 EBITA bridge
23. 52W cash flow forecast *(optional)*
24. Cash flow upside *(optional)*
25. Key risks & mitigation
26. Sources & uses of capital
27. MoM — EBITA multiple matrix
28. Section divider — Appendix *(optional)*
29. Primary interviewees *(optional)*
