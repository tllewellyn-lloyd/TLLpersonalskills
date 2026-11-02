# IM Extraction Checklist

Detailed guidance for each of the six sections, plus rules for inferring the Type property.

## 1. Company overview

**Where to look:** executive summary, "About the Company", "Business Overview", "Introduction", first 3–5 pages.

**Extract:**

- One-sentence description of what the business does (avoid the IM's own marketing phrasing if it's vague — say what it actually does)
- Headquarters (city, country)
- Year founded
- Current ownership (founder-owned, PE-backed by X, EOT, etc.)
- Key milestones: funding rounds, prior acquisitions, pivots, product launches — only if material to the deal
- Sector positioning — what sub-vertical of B2B software (e.g. "field service management", "compliance for financial services", "DevOps tooling")

Skip generic boilerplate — "passionate team", "innovative leader", awards lists.

## 2. Products & use cases

**Where to look:** "Products", "Solutions", "Platform Overview", "What we do".

**Extract:**

- Each main product — name and one-line description of what it does
- Use cases — what problem the customer is solving (preferably with the persona named: "HR teams use it for onboarding", not just "talent management")
- Deployment model — SaaS / cloud-hosted / on-premises / hybrid
- Tech stack (only if mentioned and material — e.g. ".NET on Azure" matters; the front-end framework probably doesn't)
- Pricing model — per-seat, per-transaction, flat fee, tiered, freemium — if disclosed

## 3. Financial summary

**Where to look:** "Financial Performance", "Financials", "Trading", "Historical Financials", appendix tables. Often the cleanest numbers are in a single summary table.

**Output:** a Markdown table with columns `Year | Revenue | Recurring Revenue | EBITDA`. One row per year shown — typically 3 historic FYs + current FY budget + maybe 1 forecast. Match the IM's labelling for years (FY23, CY23, 2023A, etc.).

**Rules:**

- Pull exact numbers as stated. Don't recompute or normalise.
- If the IM shows both reported and adjusted/normalised EBITDA, capture both — add a row note like "(adjusted)".
- If the IM uses MRR rather than ARR, use what the IM uses. Add a one-line note below the table if the metric is unusual.
- If a cell is blank in the source (e.g. EBITDA not disclosed for FY23), write "n/d" — don't leave it empty and don't guess.

## 4. Key commercial points

**Where to look:** "Customers", "Market & Customers", "Commercial Performance", "Customer Metrics", "KPIs".

**Extract as bullets:**

- Total customer count — current, plus the trend if the IM gives it (e.g. "240 customers, up from 180 in FY23")
- Named top customers, if the IM discloses them — list the top 5–10 by name. If the IM uses anonymised "Customer A" labels, capture the breakdown but not fake names.
- Customer concentration — % of revenue from top 1, top 5, top 10. If the IM only gives one of these, capture what's there.
- Gross revenue retention (GRR), net revenue retention (NRR), logo churn — whichever the IM reports, in the units the IM uses
- Average contract value (ACV) and / or average revenue per customer
- Sales motion — inbound / outbound / channel / partner-led
- Geographic split of customers (UK / EU / US / RoW) if material

If the IM is a "teaser" rather than a full IM, most of this will be missing — that's fine, capture what's there and put the rest into Questions.

## 5. Headcount & org

**Where to look:** "People", "Team", "Organisation", "Management", "Employees".

**Extract:**

- Total FTE count. Trend if available.
- Breakdown by function — Engineering / Product / Sales / Marketing / CS / G&A — at whatever granularity the IM provides
- Locations — UK, US, offshore, with FTE counts per location
- Key management — name + title for the CEO, CFO, CTO, founder(s), and anyone else material to the deal (e.g. a rainmaker sales lead, a technical co-founder)
- If there's an org chart in the IM, describe its shape in prose ("flat sales org reporting into the CEO"). Don't recreate the chart visually in Notion.

## 6. Questions for the advisor

This is the most valuable section. After extracting sections 1–5, list out the things that *should* be in an IM at this stage but aren't, or are unclear / inconsistent. This is what the deal team will email back to the sell-side advisor.

**Phrase each question as something you'd actually email** — specific, neutral, single-question. "What was Q4 ARR?" is more useful than "ARR data is missing."

**Common gaps to check for:**

- Revenue split by product
- Revenue split by customer cohort / vintage
- Cohort retention curves
- Cost base detail — people vs. tech vs. other; which line is what
- Working capital movement
- Capex history and forward run-rate
- Anonymised customer logo file (if not provided)
- Tech stack and IP ownership — who built it, where the code lives, any third-party dependencies
- Key contracts — auto-renew terms? change-of-control clauses?
- Management equity / option pool
- Reason for sale (often glossed over in the IM)
- Pipeline / new business won post the trading period shown
- Reported vs. adjusted EBITDA bridge
- Tax position / R&D credit treatment
- Any pending litigation or regulatory matters

Don't pad this list — only include items that are genuinely material and missing. A short, specific list is better than a long, generic one.

## Type inference (Healthy vs. Distressed)

The Type property must be set on every page. Default to **Healthy** unless you see clear signs of distress.

**Distressed signals — count how many appear:**

- Mentions of administration, CVA, accelerated sale process
- Recent declining revenue or ARR (year on year)
- Going-concern flag in the financial statements
- Cash crunch or short runway language
- Forced founder exit or management buyout under pressure
- "Restructuring" or "turnaround" language in the IM body
- Process timeline highly compressed (e.g. bids due in <4 weeks)
- Limited or partial financial disclosure (could be either, but combined with the above suggests urgency)

**Rule of thumb:** 2 or more distressed signals → mark `Distressed`. Otherwise `Healthy`.

If you're unsure, default to `Healthy` and flag the uncertainty in the preview to the user — they can override.
