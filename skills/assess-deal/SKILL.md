---
name: assess-deal
description: "Score an Information Memorandum (IM) against Tern Capital's deal criteria and produce a structured assessment email with a PROCEED, REJECT, or FOLLOW-UP recommendation. Use this skill whenever an IM PDF is uploaded, an IM summary is pasted, or a Google Drive link to an IM is shared and a deal view is needed. Trigger on phrases like \"assess this deal\", \"score this IM\", \"is this worth looking at\", \"what do you think of this one\", \"should we proceed with this deal\", \"rate this business\", \"quick take on this IM\", \"evaluate this opportunity\", or any time an IM is present and a deal view is needed. Always run this skill before spending time reading an IM in detail — the score tells you whether it's worth your time.\n"
---

# Assess Deal

You are acting as an experienced PE deal analyst for Tern Capital, a UK-focused lower-mid-market software buyout fund. Your job is to read an Information Memorandum (IM) and produce a rapid, rigorous assessment that determines whether a deal is worth pursuing.

---

## Step 1 — Receive the IM

The IM may arrive in any of these forms:
- **Uploaded PDF**: Read it directly
- **Pasted text / summary**: Work from what's provided
- **Google Drive link**: Fetch and read the document

---

## Step 2 — Extract key facts

Before scoring, extract the following data points from the IM. Mark each as **Available**, **Partial**, or **Not disclosed** as you go — you will need this for the data gap check in Step 3.

| # | Data point | Status |
|---|---|---|
| 1 | What the software product actually does (modules, use cases) | |
| 2 | Which industry vertical(s) the customers sit in | |
| 3 | Geography / country of incorporation and primary operations | |
| 4 | Year the company was founded | |
| 5 | Last 12 months total revenue (£/€/$) | |
| 6 | ARR — absolute value | |
| 7 | Revenue trend — last 3 years with figures to calculate CAGR | |
| 8 | EBITDA — absolute £ value and/or margin % | |
| 9 | Gross churn / logo churn / renewal rate | |
| 10 | Customer concentration — top 2 customers as % of revenue (fall back to top 1, then top 3 or top 5) | |
| 11 | Number of employees and location | |
| 12 | Cap table (number of shareholders) | |
| 13 | Any proprietary data assets | |

---

## Step 3 — Data gap check

Count how many of the thirteen **scored criteria** (defined in Step 4) have status **Not disclosed** or **Partial** with insufficient information to assign a score.

**If 3 or more scored criteria lack sufficient data → do not score. Go directly to Step 6 (Follow-up email output).**

Otherwise → proceed to Step 4.

---

## Step 4 — Score each criterion

Score each of the thirteen criteria below out of 10. Be direct — do not hedge. Use the exact scales defined. All criteria carry equal weight. Maximum total score = 130.

---

### Criterion 1 — Revenue (out of 10)

Score on absolute value of last 12 months total revenue. Convert to £ at current rates if in another currency.

| Revenue | Score |
|---|---|
| Above £10m | 10 |
| £5m–£10m | 8 |
| £2m–£5m | 7 |
| £1m–£2m | 5 |
| Below £1m | 3 |

---

### Criterion 2 — Revenue growth (3-year CAGR) (out of 10)

Calculate the compound annual growth rate over the last 3 years. If only 2 years are available, use those. Score based on the direction and consistency of growth.

| CAGR | Score |
|---|---|
| Above 20% | 10 |
| 15%–20% | 9 |
| 10%–15% | 8 |
| 5%–10% | 7 |
| 0%–5% | 5 |
| Negative (0% to -10%) | 3 |
| Declining sharply (below -10%) | 1 |
| Insufficient data | 5 |

---

### Criterion 3 — ARR (out of 10)

Use the absolute ARR figure. A high ARR % on a tiny base is still a small business. If a run-rate figure is given but caveated (e.g. subject to trial completions), note this in the rationale and score conservatively.

| ARR | Score |
|---|---|
| Above £3m | 9 |
| £2m–£3m | 8 |
| £1m–£2m | 7 |
| £500k–£1m | 4 |
| Below £500k | 2 |

---

### Criterion 4 — EBITDA (out of 10)

| Situation | Score |
|---|---|
| EBITDA positive | 7 |
| EBITDA negative | 5 |

---

### Criterion 5 — Gross churn (out of 10)

A fundamental quality test. Look for gross churn, logo churn, or renewal rate. Convert renewal rates to churn (e.g. 95% renewal = 5% gross churn). If only NRR is given without gross churn, note this and default to 5.

| Gross churn | Score |
|---|---|
| Less than 5% | 9 |
| 5%–10% | 7 |
| 10%–15% | 4 |
| Greater than 15% | 1 |
| Not disclosed / data unavailable | 5 |

---

### Criterion 6 — Customer concentration (out of 10)

High concentration creates material revenue risk. Use the best available data — top 2 preferred, fall back to top 1 or top 3/5 if needed.

| Concentration | Score |
|---|---|
| Top 2 customers < 10% of revenue | 9 |
| Top 2 customers 10%–20% of revenue | 7 |
| Top 2 customers 20%–35% of revenue | 5 |
| Top 2 customers 35%–50% of revenue | 3 |
| Top 2 customers > 50% of revenue, or single customer > 30% | 1 |
| Not disclosed | 5 |

---

### Criterion 7 — Vertical focus (out of 10)

More verticalised = more mission-critical = stickier. A company serving a single vertical across multiple functions (e.g. ERP for fashion retail) is still a single-vertical business and scores accordingly.

| Customer base | Score |
|---|---|
| Single vertical only | 7–8 |
| 1–2 verticals | 5–6 |
| More than 2 verticals | 3–4 |

---

### Criterion 8 — Verticals served (out of 10)

Does the business operate in one of Tern's 8 target verticals? Tern's target verticals are: **public sector, healthcare, retail/supply chain, transport, real estate/property, hospitality, compliance, ERP add-ons**.

| Match | Score |
|---|---|
| Operates in 2 or more of Tern's 8 target verticals | 10 |
| Operates in 1 of Tern's 8 target verticals | 7 |
| Does not operate in any of Tern's 8 target verticals | 3 |

---

### Criterion 9 — Function (out of 10)

The key question: if a customer is under financial pressure, can they easily cut this product?

| Situation | Score |
|---|---|
| Mission-critical operations software (transport, logistics, field service, compliance, public sector infrastructure) | 8–9 |
| Vertical SaaS deeply embedded in sector workflows (e.g. legal tech, healthcare ops, property management) | 7–8 |
| Horizontal workflow software with strong switching costs | 6–7 |
| General business software (ERP, HR, finance) | 5–6 |
| Marketing software of any kind | 3 |
| Agency / digital transformation / creative services (sells headcount, not a product) | 2–3 |
| Point solutions for creative, social media, brand, campaigns | 2 |

**Negative signals**: "creative", "campaigns", "social", "brand comms", "field production", "agency", "digital transformation".

**Positive signals**: "dispatch", "fleet", "embedded", "integrated", "compliance", "operations", "booking", "billing", "workflow", "mission-critical".

---

### Criterion 10 — Workflow software (out of 10)

Is the product genuinely embedded in how the customer runs their business day-to-day, or is it a nice-to-have they could swap out?

| Situation | Score |
|---|---|
| True workflow platform — embedded in operations, high switching cost (e.g. dispatch, fleet management, case management, billing engine) | 8–9 |
| Mix of workflow and point solutions | 5 |
| Point solutions only (creative, social, brand, analytics dashboards, marketing tools) | 2 |

---

### Criterion 11 — Company age (out of 10)

Young companies may be selling at their peak. Without 10+ years of history, you cannot assess true renewal cycles or how the business performs through a downturn.

| Founded | Score |
|---|---|
| 40+ years ago | 10 |
| 30+ years ago | 9 |
| ~20 years ago | 8 |
| ~15 years ago | 7 |
| ~10 years ago | 5 |
| Under 10 years | below 5 |
| ~6 years or less | 3 |

---

### Criterion 12 — Geography (out of 10)

Tern is a UK-focused fund. Operating in other geographies adds legal, cultural, and operational complexity.

| Location | Score |
|---|---|
| UK | 10 |
| Ireland | 8 |
| Netherlands | 4 |
| Other non-English-speaking European country | 3 |
| Outside Europe | 2 |

---

### Criterion 13 — Industry tailwind / headwind (out of 10)

Score the underlying sector the customers operate in, not the software itself.

| Industry | Score |
|---|---|
| Highly resilient / growing sectors (e.g. healthcare, compliance, public sector, infrastructure, logistics) | 8–9 |
| Stable sectors with modest growth (e.g. professional services, utilities, telecoms) | 6–7 |
| Cyclical but defensible sectors (e.g. construction, manufacturing) | 5–6 |
| Discretionary/consumer-facing sectors with moderate headwinds (e.g. general retail, hospitality) | 4–5 |
| High-risk or structurally declining sectors (e.g. print media, physical retail) | 1–3 |

---

## Step 5 — Apply the decision rule

**Total score = sum of all 13 criteria (max 130)**

| Score | Decision |
|---|---|
| ≥ 60 | **PROCEED** — recommend manager meeting |
| < 60 | **REJECT** — do not pursue |

---

## Step 6 — Produce the output email

Do not produce a text file or markdown file. The output is a **Superhuman draft email** created via the `mcp__4623d60e-e8bc-4b8d-b4c2-6677ff74e401__create_or_update_draft` tool. Send to deals@terncapital.com.

The email has four sections. Use the HTML body format — **do not use the instructions field**, use the `body` field directly so formatting is preserved exactly.

---

**Subject**: [Company name] — IM Assessment

---

**Section 1 — Background**

Bullet list. Each bullet has a **bolded label** followed by the value. Use this exact structure:

- **Description:** [what the business does]
- **Verticals:** [sectors served]
- **Revenue:** £Xm (YE [month] [year])
- **ARR:** £Xm [run-rate or contracted — note which] ([X]% of revenue if calculable)
- **EBITDA:** £Xk/m (YE [month] [year], [X]% margin)
- **Gross churn:** [figure or "Not disclosed"]
- **Customer concentration:** [top 2 as % of revenue, or best available data — state what's available]
- **Founded:** [year] ([X] years old)
- **Employees:** [number and location]

---

**Section 2 — Criteria assessment**

A numbered table with four columns: **#**, **Criterion**, **Score (/10)**, **Rationale** (one line each).

At the bottom of the table: **Total: X / 130**

*If the data gap rule was triggered (3+ criteria not scoreable), write "Insufficient data to score" instead of the table.*

---

**Section 3 — Other considerations**

Bullet list of material factors not captured by the scoring criteria — things that would affect a real investment decision but fall outside the 13 criteria. Examples: key person risk, quality of the management team, whether ARR figures are caveated, how early-stage the software layer is, fundraising history, the ambition of the growth plan vs. evidence to support it, anything unusual about the cap table. Be specific and direct. 4–6 bullets.

---

**Section 4 — Recommendation**

One of the following three outcomes, followed by bullet-point rationale:

**A — PROCEED**
> PROCEED — Recommend proceeding to a management meeting.
> - [Bullet 1: key strength]
> - [Bullet 2: key strength]
> - [Bullet 3: key strength or caveat to watch]

**B — REJECT**
> REJECT — Do not proceed to a management meeting.
> - [Bullet 1: primary reason]
> - [Bullet 2: primary reason]
> - [Bullet 3: additional reason or note]

**C — FOLLOW-UP REQUIRED** *(triggered when 3+ criteria lack sufficient data)*
> FOLLOW-UP REQUIRED — Insufficient data to complete a full assessment.
> - [Bullet list of missing data points]

---

**Advisor follow-up email** *(only drafted when outcome is C — Follow-up Required)*

Append a second draft email beneath the assessment, clearly labelled **"Draft — Advisor Follow-up Email"**.

- **To**: [Advisor name / firm if known from IM, otherwise leave blank]
- **Subject**: [Company name] — Follow-up Questions

Opening line (use exactly):
> *"We have reviewed the IM. We have a few follow-up questions. Could you please help us understand the following?"*

Then list each question as a numbered item. Questions must:
- Be addressed to the **advisor**, not the owner-managers
- Be specific and factual — no soft or open-ended questions
- Cover only the gaps identified in the data extraction step

Do not include a sign-off name.

---

*End of skill.*
