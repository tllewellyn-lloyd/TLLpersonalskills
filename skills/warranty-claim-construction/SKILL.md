---
name: warranty-claim-construction
description: "Construct, draft, review or advise on warranty claims under a Share Purchase Agreement (SPA) for a UK software business acquisition. Use this skill whenever the user asks about warranty claims, breach of warranties, claim quantum, notice of claim letters, claim methodology, SPA set-off rights, King's Counsel opinions, deferred consideration set-off, or anything related to pursuing sellers for breach of warranty post-acquisition. Also trigger when the user asks about Sofco / Carrington / Galderma warranty issues, or says things like \"how do we calculate the claim\", \"what approach should we use\", \"draft the warranty letter\", \"what documents do we need\", or \"run me through the checklist\". This skill contains Tern Capital's full working knowledge of warranty claim construction — always load it before advising on any SPA post-completion dispute.\n"
---

# Warranty Claim Construction

This skill documents Tern Capital's working approach to constructing, quantifying and serving
warranty claims under a UK SPA following the acquisition of a software business. It is grounded
in live experience on the Sofco Limited acquisition (completion: 26 September 2025).

**Before advising on any claim, read this skill in full. For the internal checklist, also read
`references/internal-checklist.md`. For the Sofco-specific precedent, read
`references/sofco-precedent.md`.**

---

## 1. When Does a Warranty Claim Arise?

A warranty claim arises when a representation made by the Sellers in the SPA at the date of
completion proves to have been false, misleading or incomplete — and that breach causes the
Buyer a loss. Common triggers in software acquisitions:

- A key customer cancels or reduces spend shortly after completion, where pre-completion
  notification was received but not disclosed (breach of Warranties 10.5, 10.8, 11.3.1)
- A fixed-price implementation order was disclosed with X man-days remaining, but the true
  scope was materially greater or the product could not perform as required (breach of 10.3, 10.1.3)
- EBITDA or revenue figures in the management accounts are misstated
- Undisclosed liabilities, contracts or legal proceedings exist
- IP ownership or licensing is not as warranted

**Key threshold:** Under Tern's standard SPA, two minimum conditions must be satisfied before
the Sellers are liable:
1. Individual claim liability must exceed **£2,000**
2. Aggregate claim liability must exceed **£20,000** (the "basket") — once crossed, the Sellers
   are liable for the **whole** amount, not just the excess

---

## 2. Quantum Methodology — Approaches and Trade-offs

There are two principal methodologies for quantifying warranty claim losses. Choose carefully:
the approach shapes how the claim letter is drafted and how easily it can be defended.

### Approach A: Completion Multiple Applied to EBITDA Loss (RECOMMENDED)

**How it works:**
- Identify the Completion Multiple: Total Consideration (upfront + deferred, excl. contingent)
  divided by Completion EBITDA
- Identify the EBITDA loss caused by each breach (e.g. lost ARR that falls entirely to profit)
- Apply: **Claim Value = Completion Multiple × EBITDA Loss per breach**
- Each breach produces its own claim line; they sum to a total

**Example — Sofco:**
- Completion Multiple: £1,985,686.76 / £252,984.75 = **7.85×**
- Galderma loss: £81,215 ARR (100% EBITDA drop) → 7.85 × £81,215 = **£637,538**
- Carrington loss: £39,000 ARR → 7.85 × £39,000 = **£306,150**
- **Total claim: £943,688**

**Pros:**
- Objectively anchored to the actual deal economics — hard to dispute the multiple
- Clean formula: acquisition multiple is a matter of contract record
- Mirrors precisely how the price was set — the Sellers themselves implicitly agreed the
  multiple was appropriate
- Produces per-warranty claim lines that are independently defensible
- Straightforward for King's Counsel to opine on and for a court to follow

**Cons:**
- Does not capture multiple contraction (the argument that a buyer would have paid a
  lower multiple for a smaller, riskier business)
- Tends to produce a lower headline number than Approach B when the re-rated multiple
  would have been significantly lower

---

### Approach B: Diminution in Value (Re-rated Multiple)

**How it works:**
- Calculate Warranty True Value (WTV): Completion EBITDA × Completion Multiple = Total Consideration
- Calculate Warranty False Value (WFV): Actual EBITDA × Revised (lower) Multiple
- **Loss = WTV − WFV**

**Example:**
- WTV: £252,984.75 × 7.85 = £1,985,686.76
- Actual EBITDA: £252,984.75 − £120,215 = £132,769.75
- Revised Multiple: 4× (smaller, riskier business)
- WFV: £132,769.75 × 4 = £531,079
- **Loss: £1,985,686.76 − £531,079 = £1,454,607**

**Pros:**
- Produces a higher headline number
- Captures multiple contraction — the real-world principle that a buyer pays less per £
  of EBITDA for a smaller, less profitable, riskier business
- Aligned with conventional corporate finance valuation theory

**Cons:**
- The revised multiple is **subjective and contested** — the Sellers will argue it should
  be higher (e.g. 6× or 8×), significantly eroding the claim value
- Expert evidence is typically required to substantiate a re-rated multiple, adding cost
  and delay
- Available comparable transactions almost always involve larger, cleaner businesses,
  making a small-business size discount hard to evidence
- Exposes detailed working to the Sellers, allowing them to attack individual assumptions
- Risk of double-counting if paired with per-warranty EBITDA loss claims (see Schedule 6
  para 1.5 on limitations)

**When to use B:**
- Only if the transaction was large enough to justify expert valuation costs
- Only if the size/risk discount is clearly demonstrable from market data
- Only as a **starting position** in a high-value dispute, with expert support lined up

---

### Approach C: Direct Loss (Operational)

**How it works:**
- Quantify the actual cash cost of the breach: remediation costs, replacement revenue
  required, management time, external contractors, legal costs

**Pros:** Grounded in documented expenditure

**Cons:** Rarely adequate for SPA warranty claims — operational costs are often modest
relative to the valuation impact. Better suited as a supplementary claim alongside A or B.

---

### Tern's Preferred Approach

**Use Approach A (Completion Multiple × EBITDA Loss) as the primary methodology.**

Reasons:
1. The multiple is an agreed fact from the transaction — the contract itself records it
2. No expert evidence required; the arithmetic is transparent and simple
3. Each breach is separately quantified, making the claim modular and extensible
4. Aligned with HD's advice and standard market practice for disputes of this scale
5. Additional Losses (management time, external legal costs) are reserved separately as
   a supplementary claim without needing to quantify them upfront

**Always add a general reservation** for management time and external legal costs as
additional Losses (as defined in the SPA) not yet quantified but expressly reserved.

---

## 3. Structure of the Warranty Claim Letter

The notice letter must satisfy the SPA's notification requirements (typically clause 24).
It is a legal document — every section has a purpose.

### Mandatory sections (in order):

**Header / Addressee**
- FAO the Sellers' Representative (typically one named seller)
- Copy to Sellers' solicitors (Ward Hadaway LLP in Sofco)
- And by email to personal email addresses of all Sellers + solicitors
- Date (must be within the limitation period — typically 2nd anniversary of completion)
- Hill Dickinson reference / Sarah Emerson details

**Introduction (paras 1–6)**
- Confirm who is acting (HD for Forma)
- Reference the SPA (date, parties, definitions)
- State that investigations are ongoing and rights to amend are reserved
- Confirm this constitutes formal notice under the SPA
- Confirm copy to Sellers' solicitors
- State all documents referred to are enclosed at Appendix 1

**The SPA (paras 7–8)**
- Extract verbatim the key SPA provisions that underpin the claim:
  - Relevant definitions (Claim, Losses, Disclosed, Recurring Revenue Contracts, etc.)
  - Warranty clauses being relied upon (10.1.3, 10.3, 10.5, 10.6.1, 10.8, 11.3.1)
  - Set-off provisions (Clause 7 — Buyer's Right of Set Off)
  - Schedule 6 limitations (especially para 1.7 on fraud exclusion and para 3.1 on time limits)
- State which SPA provisions the Disclosure Letter did NOT specifically disclose against

**Events following Completion**
- Separate subheadings for each breach/claim
- For each: factual narrative → breach identified → warranty(ies) breached → quantum impact
- Cross-reference supporting documents using Appendix 1 reference numbers

**Right of Set-Off (paras 18–21)**
- Confirm this is a Qualifying Claim for clause 7.1.1
- State intention to set-off against Deferred and/or Contingent Consideration
- Set out the Deferred Consideration schedule (amounts, dates)
- Invite Sellers to confirm liability and quantum in writing before the first payment date

**Quantum (paras 22–24)**
- Lead with: "Our client's best estimate of its Losses is set out at Appendix 2 in the sum
  of £[X]"
- State the conventional basis (difference between warranted and actual value)
- Explain the 7.85× Completion Multiple and how it was derived
- Apply it per breach line (Galderma = E × F, Carrington = E × G)
- Reserve management time and legal costs as additional unquantified Losses

**Next Steps (paras 25–28)**
- Acknowledge receipt within 7 days
- Invite proposals within 14 days
- Reserve right to obtain King's Counsel opinion under clause 7.2.2
- State that KC costs will be set off per clause 7.5

**Sign-off**
- "Yours faithfully / Hill Dickinson LLP"

**Appendix 1 — Documents** (numbered table: Ref. | Document)
**Appendix 2 — Calculation of Claim** (Input/Value/Source table, then claim formula lines)
**Appendix 3 — Churned Customers** (if relevant — supports warranty context)

---

## 4. Supporting Documents Required

### Core transaction documents
| Ref. | Document | Purpose |
|------|----------|---------|
| 1 | Share Purchase Agreement | Foundation of all warranty obligations |
| 2 | Disclosure Letter (+ schedules) | Establishes what was and was not Disclosed |

### Per-claim supporting documents

**For a customer cancellation / reduced-spend claim:**
| Ref. | Document | Purpose |
|------|----------|---------|
| 3 | Cancellation/downgrade email from customer | Proves notification pre- or around completion |
| 4a | Internal technical write-up or contractor statement | Establishes root cause of failure |
| 4b | Signed addendum / termination agreement | Confirms ARR loss is permanent |
| 4c | Cover email transmitting the addendum | Shows process and timeline |
| 4d | Customer written confirmation of anticipated exit | Supports quantum (ARR will not return) |

**For an EBITDA / accounts-based claim:**
- Management accounts (monthly P&L for the relevant 12-month period)
- Data room references to the specific management accounts files (e.g. DR55)
- Any reforecast or updated financial information

**For an implementation / one-off order claim:**
- Copy of the relevant contract or order
- Disclosure Letter entry and data room documentation relating to man-days
- Evidence of actual man-days spent / outstanding scope
- Customer communications confirming scope gap

### General supporting documents
- Any pre-completion communications that show the Sellers were aware of the relevant facts
- Call transcripts or meeting notes (use carefully — consider disclosure obligations)
- Third-party assessments (e.g. external developer's codebase assessment)
- Any post-completion board or management communications referencing the issue

**Note on disclosure:** Once you attach documents to a notice letter, you may be required
to disclose the full email chain if the dispute escalates. Only attach documents where you
are comfortable with full chain disclosure. PDFs of individual emails are preferred over
forwarded chains.

---

## 5. Drafting Rules and Red Lines

- **Strict liability:** The SPA notification provisions are typically strict. A late or
  defective notice loses the claim. Always check the exact notification clause and deadline.
- **Reservation of rights:** Always include in every notice: right to amend/expand as
  further facts emerge; right to recover all Losses as defined; right to recover legal costs.
- **Multiple warranties:** Plead every applicable warranty separately. Each warranty is
  independent (SPA clause 5.3) — if one fails, others may still succeed.
- **Schedule 6 knowledge bar (para 4):** Check whether the named buyer-side knowledge
  representatives (Karthik, James Hang, Tom Llewellyn-Lloyd in Sofco) had actual knowledge
  of the breach pre-completion. Stuart Lowe (post-acquisition CEO) is not a named individual
  for this purpose. The knowledge bar applies only to the named individuals.
- **Fraud carve-out (Schedule 6 para 1.7):** State expressly that investigations are ongoing
  and that if wilful misconduct, wilful concealment or dishonesty is established, the Schedule
  6 limitations will not apply. This preserves optionality.
- **Total Consideration figure:** Use Completion Consideration + Deferred Consideration only.
  Do not include Contingent Consideration in the WTV calculation — it was not guaranteed at
  completion.
- **Rounding:** Be consistent. The Completion Multiple (e.g. 7.85×) should match the
  arithmetic: Total Consideration / Completion EBITDA. Show the derivation in Appendix 2.
- **Do not overload with narrative:** The initial notice letter is not the place for a
  26-page call transcript or full technical analysis. Attach concise supporting documents;
  keep detailed forensics for the KC bundle.
- **Without prejudice discussions:** Once the letter is served, without-prejudice settlement
  discussions can proceed without lawyers present — but always frame them explicitly as WP
  before the call, ideally with a confirming email, so nothing can be used in open
  correspondence.

---

## 6. Timeline and Process After Service

| Milestone | Timing | SPA mechanism |
|-----------|--------|---------------|
| Notice served | Day 0 | Clause 24 |
| Sellers' acknowledgment sought | Day 7 | — |
| Sellers' proposals invited | Day 14 | — |
| Agree KC appointment (or fail) | Within 10 business days of notification | Clause 7.2.2 |
| Bar Council appoints KC if not agreed | After 10 business days | Clause 7.2.2 fallback |
| **Internal KC opinion deadline** | **31 August** (for Sept 26 payment) | Internal |
| First Deferred Consideration payment | 12 months post-completion | Schedule 11 |
| Claim limitation deadline | 2nd anniversary of completion | Schedule 6 para 3.1 |

**KC process notes:**
- The KC opinion must confirm: (a) on balance of probabilities the Buyer will succeed, and
  (b) the likely quantum
- The SPA requires "reasonable endeavours" to agree KC within 10 business days; if not
  agreed, the Bar Council selects independently
- KC is typically instructed by solicitors (HD), not directly by the Buyer — both costs
  are incurred but HD will minimise duplication
- If KC opinion supports the claim, KC costs are recoverable by set-off against Deferred
  Consideration under clause 7.5

---

## 7. Reference Files

Read these files for additional depth:

- **`references/internal-checklist.md`** — Complete pre-service checklist covering all items
  to verify before the notice letter goes out
- **`references/sofco-precedent.md`** — Sofco-specific worked example: warranty selection,
  quantum derivation, Appendix 2 table, key dates and amounts
