# Field guide — customer contract review

How to extract each standard review field. The user's template may use slightly different column
names or a subset/superset of these — match on meaning. Always cite clause numbers and quote
figures. Where a field is genuinely not covered, write "Not specified in contract".

Read every field from the **target's perspective** (the target is usually the supplier/licensor;
the counterparty is the customer).

## Identification & status

- **File name** — the original contract file name(s). If one customer has several files (e.g. a
  base agreement + an extension/variation), list them together and review as one row.
- **Status** — "Reviewed" if complete; "Outstanding" if there are unresolved queries (e.g. missing
  signature, ambiguous pricing, missing schedule).
- **Contract type** — detect and name it. Common types:
  - *Standard supplier template* (the target's own paper, e.g. "Software Licence & Maintenance
    Agreement") — usually the most supplier-favourable.
  - *Public-sector framework call-off* (e.g. CCS **G-Cloud** RM1557.xx, **GP IT Futures / GPITF**
    Lot 1) — customer (buyer) paper; incorporates framework terms by reference.
  - *Bespoke customer paper* (e.g. a Government/Authority services agreement) — usually the most
    onerous on the target; may be under a non-UK law.
  Identifying the type tells you where to look and often that several contracts share one template.

## Term

- **Start date** — commencement/effective date (dd/mm/yyyy). Watch for a gap between the signature
  date and a stated "covers the dates from…" period — note both.
- **Duration** — length of term. Distinguish a headline multi-year "cover period" from the operative
  clause: many templates grant only a rolling 12-month licence that auto-renews, despite a
  "2026-2028" heading. Say so.
- **End date** — expiry of the current term (and note auto-renewal if it rolls on).

## Renewal, price-increase notice & termination timing

- **Latest date for price increase notification** — by when must the target notify the customer of
  a rise. Quote the clause. In auto-renewing templates this is often "on or prior to the Renewal
  Date", with an RPI default if not confirmed. In fixed-term call-offs, often "charges cannot be
  amended during the term".
- **Auto renewal clause** — is there one, and the mechanics (e.g. "renews automatically for a
  further 12 months on each anniversary unless terminated"). Framework call-offs usually have NO
  auto-renewal (they expire; extension is at the buyer's option).
- **Termination notification deadline** — the notice period / date by which notice to terminate
  must be given, by either side. Note the distinction between a mid-term right and an
  anniversary-only break (e.g. "14 days' notice, but only expiring on an anniversary" = a
  once-a-year non-renewal right, NOT a right to leave mid-term).

## Pricing & ARR (do the maths)

- **Total contractual Pricing (rate card)** — the full pricing in detail: setup/installation fee,
  annual subscription/licence fee, total contract value, any day-rate card, per-unit (e.g.
  per-patient/per-seat) rate, and per-product breakdown from the pricing schedule. Quote exact
  figures and state ex/inc VAT.
- **Recalculated ARR** — the annualised **recurring** revenue going forward. Method:
  - Use the **annual** recurring fee, not the total contract value. If only a multi-year TCV is
    given, divide by the number of years (state this).
  - **Strip out one-off, non-recurring items** (setup/installation fees, one-off consultancy,
    especially where they are refundable).
  - Where pricing is per-unit, reconcile: `unit rate x volume` should tie to the stated total; if
    it doesn't, work out whether a **volume discount** or a **different period/patient count**
    explains the gap, and show the reconciliation.
  - Watch for **cumulative-vs-per-period** value tables (a table headed "how the value has varied
    since inception" is cumulative — take the *increment* of the latest period and annualise it).
  - If two different totals appear for the same period, that's an **internal inconsistency** — flag
    it for the seller, don't silently choose one.
  - Always state your assumptions.

## Legal terms

- **Governing law** — the governing law and jurisdiction (watch non-UK, e.g. Jersey law).
- **Licence** — scope of the licence granted to the customer (non-exclusive / non-transferable /
  object-code-only / term-limited vs perpetual). Flag any **perpetual/irrevocable** licence over
  the target's IP (customer-favourable) — common in bespoke public-sector paper, rare in the
  target's own template.
- **Services/Products** — what is supplied (list the products/modules from the schedule).
- **Assignment clause** — can the **target** assign/novate freely (often "on written notice")? Can
  the **customer** (usually only with consent)? In framework call-offs the supplier usually CANNOT
  assign without buyer/authority consent while the authority can transfer to another public body.
- **Termination** — every ground and its notice/cure period: anniversary/convenience, non-payment
  (cure period), material breach (cure period), insolvency, failure to take updates, force majeure.
  Note asymmetry — public-sector buyers often have terminate-for-convenience at will while the
  supplier can only exit for cause.

## Change of control — CRITICAL

Answer clearly: **does the customer get a right to terminate on a change of control of the target,
and must the target notify the customer if Tern acquires it?** State YES/NO and quote the clause.

- The target's **own standard templates** are often **silent** on change of control — a share sale
  is not an assignment/novation, so it triggers no customer consent, notice or termination right.
  That is **favourable** for the acquisition.
- **Framework call-offs** (G-Cloud, GPITF) typically **incorporate framework change-of-control
  clauses** (e.g. CCS Framework cl.5.4-5.6) giving the buyer a notification right and a termination
  right on a change of control — plus, for critical contracts, corporate-resolution-planning
  notification duties. These are **risk-register items** — flag them.
- **Bespoke customer/authority paper** often has an **explicit** change-of-control termination
  right and immediate notification duty. Flag it.
- The framework text is usually incorporated by reference and not reproduced — note that the exact
  trigger/period should be confirmed against the framework agreement.

## Commercial & risk terms

- **Payment terms** — invoicing basis and payment window (e.g. "within 30 days of a valid
  undisputed invoice"; annually/monthly in advance), late-payment interest, set-off.
- **Price increase terms** — can the target raise prices, and on what basis (RPI/CPI, per-unit
  volume growth e.g. patient-population ≥5%, usage overage)? Is any uplift **capped** (e.g.
  CPI-0.5% or 2%; RPI)? Framework call-offs are often fixed for the term.
- **Data protection** — brief: who is **Controller** vs **Processor** (usually customer =
  Controller, target = Processor of the personal data), governing DP law (UK GDPR/DPA 2018, or
  local), and any joint/independent-controller carve-out for business contact details. Note if the
  detail is deferred to a separate DPA, or if the data-categories schedule is left blank.
- **Warranties / Indemnities** — brief: conformance warranty (e.g. 90 days), exclusion of implied
  terms, IP-infringement indemnity (note if uncapped), any customer indemnities.
- **Intellectual Property** — who owns what. Typically the **target owns its software/IP** (no
  transfer; customer gets only a use licence) and the **customer owns its own data**. Flag the
  exceptions: perpetual/irrevocable/sub-licensable licences over the target's IP, assignment of
  "Project-Specific"/foreground IP to the customer, and any **open-source publication** right — all
  reduce defensibility/lock-in. Distinguish ownership (retained) from licence (may be very broad).
- **Limitation of liability** — the cap and its basis (e.g. capped at one year's fees; or the
  greater of £X or Y% of charges), and the uncapped carve-outs (death/PI, fraud, data-protection,
  IP indemnity). Note when a cap floor is disproportionate to a small contract value.
- **Insurance requirements** — is the target required to carry insurance and at what levels (PI,
  public/products, employers' liability), and for how long post-term? The target's own templates
  often require none; framework/bespoke paper usually mandates cover (and can be disproportionate).
- **SLA / Penalties** — service levels, support hours, priority/response/resolution targets, and
  crucially whether there are **service credits / financial penalties** (often none in the target's
  own template; a formal service-credit regime in GPITF).
- **New releases / software updates** — obligation to provide maintenance releases/new versions,
  and any right to terminate if the customer won't install them.
- **Escrow agreement** — is a source-code escrow required? (Usually not for cloud/SaaS.)
- **Parent company guarantee (PCG) / performance security** — does the contract require the supplier (the target) to procure a **parent company guarantee, guarantee, bond or other form of security** for its obligations? Check for a dedicated guarantee clause/schedule (e.g. a "Guarantee" schedule, or a "Parent company guarantee" line in a fees/terms schedule). Three patterns to watch: (i) the target's own templates usually have **no** PCG provision; (ii) public-sector framework call-offs (G-Cloud, GPITF) carry a **standard guarantee mechanism** that is only live if the Order Form / guarantee schedule is marked "applicable" — it is often marked **"Not applicable"**, so no PCG is required as drafted; (iii) bespoke customer/authority paper often contains a PCG **placeholder** (e.g. "delete if not required") or a right for the customer to **demand** security — even if unpopulated, flag it as a live hook. State clearly **Yes / No / Not required as drafted (but contemplated)** and quote the clause. This matters for the acquisition: if a PCG is required, the buyer's HoldCo may have to provide/assume it post-completion.

## Commentary & close-out

- **Comments** — the material issues for the deal, in your own words (the CoC position, lock-in,
  liability, IP, execution status, any inconsistencies).
- **Signed?** — is it executed by **both** parties? Check the signature block and any e-signature
  (Zoho Sign / DocuSign) completion certificate. Blank name/date fields or a missing certificate =
  treat as unsigned and flag it.
- **Outstanding points** — specific items to go back to the seller on (missing signed copies,
  ambiguous pricing/ARR, schedules not completed, framework terms to obtain, inconsistencies).
