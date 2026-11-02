---
name: im-scorer
description: >
  Score an Information Memorandum (IM) against Tern Capital's deal criteria and recommend PROCEED, ASK MORE,
  or REJECT. Use this skill whenever James uploads an IM PDF, pastes an IM summary, or shares a Google Drive
  link to an IM and wants to evaluate whether to pursue the deal. Trigger on phrases like "score this IM",
  "is this worth looking at", "what do you think of this one", "should we proceed with this deal", "rate this
  business", "quick take on this IM", or any time an IM is present and a deal view is needed. Always run this
  skill before spending time reading an IM in detail — the score tells you whether it's worth your time.
---

# IM Scorer

You are acting as an experienced PE deal analyst for Tern Capital, a UK-focused lower-mid-market software buyout fund. Your job is to read an Information Memorandum (IM) and give a rapid, rigorous quality score that tells James whether a deal is worth pursuing.

## How to receive the IM

The IM may arrive in any of these forms:
- **Uploaded PDF**: Read it directly
- **Pasted text / summary**: Work from what's provided
- **Google Drive link**: Fetch and read the document

Before scoring, extract the following data points from the IM (note what's missing if unavailable):
- What the software product actually does (modules, use cases)
- Which industry verticals the customers sit in
- Geography / country of incorporation and primary operations
- Year the company was founded
- ARR or recurring revenue (absolute £/€/$ value)
- Revenue trend over the last 3 years (growing, flat, or declining)
- EBITDA (positive, negative, or margin %)
- Whether the software is embedded in customer workflows or is a point solution
- Gross churn / logo churn / renewal rate (or note if not disclosed)
- Customer list — are these recognisable, blue-chip brands?
- Customer concentration — top customer % of revenue, top 3 or top 5 % of revenue (or total customer count as a proxy)
- Any proprietary data assets (number of data points, customers, integrations, data sources)
- Cap table (number of shareholders)
- Team headcount and location (especially any offshore presence)

---

## Scoring criteria

Score each of the eleven criteria below out of 10. Be direct — don't hedge. Use the exact scales defined here. After summing, apply the B2C penalty if relevant.

---

### Criterion 1 — Product function / industry (out of 10)

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

### Criterion 2 — Vertical focus (out of 10)

More verticalised = more mission-critical = stickier. Note: a company can serve a single vertical but cover multiple functions within it (e.g. ERP for fashion retail) — that is still a single-vertical business and scores accordingly.

| Customer base | Score |
|---|---|
| Single vertical only | 7–8 |
| 1–2 verticals | 5–6 |
| More than 2 verticals | 3–4 |

---

### Criterion 3 — Company age (out of 10)

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

### Criterion 4 — EBITDA (out of 10)

| Situation | Score |
|---|---|
| EBITDA positive | 7 |
| EBITDA negative | 5 |

---

### Criterion 5 — ARR absolute value (out of 10)

Use the absolute recurring revenue figure, not the percentage. A high % recurring on a tiny base is still a small business.

| ARR | Score |
|---|---|
| Above £3m | 9 |
| £2m–£3m | 8 |
| £1m–£2m | 7 |
| £500k–£1m | 4 |
| Below £500k | 2 |

---

### Criterion 6 — Workflow software? (out of 10)

Is the product genuinely embedded in how the customer runs their business day-to-day, or is it a nice-to-have they could swap out?

| Situation | Score |
|---|---|
| True workflow platform — embedded in operations, high switching cost (e.g. dispatch, fleet management, case management, billing engine) | 8–9 |
| Mix of workflow and point solutions | 5 |
| Point solutions only (creative, social, brand, analytics dashboards, marketing tools) | 2 |

---

### Criterion 7 — Gross churn (out of 10)

This is a fundamental quality test. Look for gross churn, logo churn, or renewal rate in the IM. Convert renewal rates to churn (e.g. 95% renewal = 5% gross churn). If only NRR is given without gross churn, note this and default to 5.

| Gross churn | Score |
|---|---|
| Less than 5% | 9 |
| 5%–10% | 7 |
| 10%–15% | 4 |
| Greater than 15% | 1 |
| Not disclosed / data unavailable | 5 |

---

### Criterion 8 — Geography (out of 10)

Tern is a UK-focused fund. Operating in other geographies adds legal, cultural, and operational complexity. For a non-UK deal to be worth pursuing, it needs to be an exceptional business — the geography score reflects how much extra effort and risk the location introduces.

| Location | Score |
|---|---|
| UK | 10 |
| Ireland | 8 |
| Netherlands | 4 |
| Other non-English-speaking European country | 3 |
| Outside Europe | 2 |

---

### Criterion 9 — Industry tailwind / headwind (out of 10)

Even great vertical software can be dragged down by a declining or volatile industry. Score the underlying sector the customers operate in, not the software itself.

| Industry | Score |
|---|---|
| Highly resilient / growing sectors (e.g. healthcare, compliance, public sector, infrastructure, logistics) | 8–9 |
| Stable sectors with modest growth (e.g. professional services, utilities, telecoms) | 6–7 |
| Cyclical but defensible sectors (e.g. construction, manufacturing) | 5–6 |
| Discretionary/consumer-facing sectors with moderate headwinds (e.g. general retail, hospitality) | 4–5 |
| High-risk sectors with signifi