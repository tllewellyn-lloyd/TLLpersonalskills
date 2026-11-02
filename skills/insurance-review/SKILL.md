---
name: "insurance-review"
description: "Review a target company's insurance documentation for buy-side due diligence and populate the user's insurance review template (Excel) with a structured row per cover section. Use whenever the user provides a folder or set of insurance documents for a deal (policy schedules, statements of fact, certificates, payment schedules, policy wordings, broker reports) plus a review template, or asks to \"review the insurance\", \"fill in the insurance template\", \"go through these insurance docs\", \"build the insurance review spreadsheet\", \"what insurance does the target have\", or any variation where insurance documents need to be read against a fixed set of review fields and the findings tabulated. Works for any Tern Capital deal, any insurer and any cover type. Output is the user's template, populated, plus a document index and premium reconciliation."
---

# Insurance Review

Reads a target company's insurance documentation and fills in the user's insurance-review
template — **one row per cover section**, one column per review field — for buy-side due
diligence. Developed on a real Tern deal (a primary-care software target insured with Hiscox),
but the steps apply to any insurer, any programme and any deal.

Output is the populated template plus two supporting tabs (document index, premium
reconciliation) and a short written summary of what matters for the deal.

## Core context — get this right first

This is **buy-side DD on an acquisition target**. Tern is the buyer; the insured is the
target. Two consequences shape the whole review:

- **Everything is read as inherited exposure.** A gap in the target's cover, or a
  disclosure defect that lets the insurer reduce or refuse a claim, becomes the buyer's
  problem on completion. The question is never just "is there a policy" but "will it pay,
  and will it still pay after we own it".
- **The deal itself is an insurance event.** Change of control on completion may be a
  material change requiring notification; a continuing-cover policy may auto-renew into
  the buyer's ownership; and if the programme is re-broked post-completion, claims-made
  covers can silently lose their history (see retroactive dates below).

Confirm the framing with the user if it isn't obvious which company is the target.

## Step 1 — Gather the inputs

1. **The review template** (Excel). The user provides this at the start. **Read its header
   row** to determine the exact field set — do not assume a fixed list of columns. Note any
   columns already pre-filled: preserve them, don't overwrite.
2. **The insurance documents** — a folder of PDFs. List the folder first and count them.
   A typical pack contains: policy schedule and statement of fact, generic policy summary,
   summary of wording changes, payment schedule, one certificate per compulsory or
   customer-facing cover, and the full policy wording booklet.

Ask the user for anything missing. If no folder is mounted, request access.

**If the deal folder can't be written from the sandbox** (a common situation with Google
Drive shared drives), build in the outputs directory, present the file, and tell the user
to move it into the dataroom folder.

## Step 2 — Read the documents, in the right order

Not all documents carry equal weight. Read in this order:

1. **Policy schedule and statement of fact — the primary document.** Every limit, excess,
   premium, date, endorsement, insurer and declared value comes from here. Everything else
   is corroboration. Read it in full.
2. **Certificates** — one per cover. Use only to cross-check the schedule and to record
   what the target can hand to a customer as evidence of cover.
3. **Payment schedule** — premium instalments, payment method, account details.
4. **Summary of change** — tells you where cover was *narrowed* at the last renewal, which
   is often more interesting than where it was broadened.
5. **Generic policy summary and full policy wording** — standard market paper, no
   target-specific content. Read at summary level for exclusions. Only go clause-by-clause
   if a specific coverage question arises (e.g. whether patient data falls inside the cyber
   and PI cover).

Read the PDFs directly with the Read tool where they're image-light; for long wordings
extract text with `pypdf`/`pdfplumber` tagging page numbers so findings can cite pages.

**Cite page numbers for every material finding.** The user will be asked "where does it say
that" and needs to be able to point at it.

## Step 3 — Row logic

**One row per cover section, not per file.** A single business policy routinely bundles
professional indemnity, public and products liability, employers' liability, property
(contents / away and in transit / money), cyber and data (own losses / third-party claims /
crime), legal protection and crisis containment — each with its own limit, excess, basis and
premium. Collapsing those into one row per PDF destroys the analysis.

Then add a **total row** carrying the policy-level facts: total premium, payment method,
insured entity and address, declared turnover and wage roll, renewal basis, and the
deal-level outstanding points.

Where a cover has a materially different sub-limit and its own premium (cyber crime is the
usual example), give it its own row.

## Step 4 — Fill the template's columns

Populate whatever columns the template has. For the standard Tern field set:

| Column | How to fill it |
|---|---|
| **File name** | The source document(s) for that row — normally the schedule, plus the certificate where one exists. |
| **Insurer** | The **risk carrier**, not the broker or the underwriting agent. Distinguish carefully: an agent (e.g. Hiscox Underwriting Ltd) arranges cover *on behalf of* the carrier (e.g. Hiscox Insurance Company Limited). Record the carrier and note the agent. **Check every section** — legal expenses is frequently written by a different carrier (ARAG, DAS) with its own reference. |
| **Dataroom ref** | As the user specifies (they'll usually give you a single value for the whole pack). |
| **Legal entity covered** | The named insured, exactly as written. Record whether there are additional insureds and whether subsidiaries are covered — the statement of fact's turnover breakdown tells you if any exist. |
| **Broker** | Frequently **not named anywhere in the pack** even though the documents refer to "your broker". If so, say "Not stated in documents provided" and put it in Outstanding. Don't infer a broker from the insurer's name. |
| **Policy no.** | One policy number usually covers every section. Note any separate section reference. |
| **Insurance type** | Plain name of the cover (Professional Indemnity, Employers' Liability, Cyber and Data). |
| **Coverage limit** | The headline limit for that section. Say whether a sub-limit sits **within** or **in addition to** the main limit — the schedule always states this and it changes the number materially. |
| **Coverage** | **Keep it short — one or two lines.** Main cover heads plus any material sub-limit or express exclusion. Users consistently ask for this column to be cut down, so write it condensed first. Long extension lists belong in Comments or nowhere. |
| **Start / End date** | The period of insurance. Check the schedule effective date and each section's cover start date — a mid-term endorsement can make them differ. |
| **Price** | Annual premium per section, exclusive of IPT (the schedule breaks this out). At policy level give both net and gross of IPT, and the instalment amount. |
| **Excess** | Amount plus what it applies to. Note where it's nil, and any special excesses on particular perils. |
| **Comments** | The analytical column. Basis of limit, whether defence costs erode it, relevant statement-of-fact declarations, endorsements, obligations on the insured, and anything that makes the number less good than it looks. |
| **Outstanding** | What to obtain or clarify. Prefix genuinely material items with `PRIORITY` so they can be filtered and highlighted. |

**Add extra columns after the user's columns** where the documents support them — the user
wants these by default, not on request. The set that earns its place:

- **Basis of limit** — aggregate vs each-and-every, and whether costs are inside or outside
- **Excess basis** — per claim, per claimant, per incident
- **Retroactive date**
- **Geographical limits / applicable courts**
- **Certificate on file** — yes/no per section
- **Renewal basis** — continuing cover (auto-renewing) vs fixed term

If a field is genuinely not addressed, write "Not specified in documents provided". Never
invent a figure.

## Step 5 — The analysis that makes this worth doing

Anyone can transcribe a schedule. The value is in these tests. Work through all of them.

### Basis of limit — the number on the certificate is not the cover

A limit expressed **"in the aggregate, including all costs"** is far weaker than the same
number **"each and every claim, excluding defence costs"**. In the first case defence costs
erode the limit and one bad year exhausts it. Professional indemnity is usually written on
the weaker basis and public liability on the stronger one. State the basis every time.

### Retroactive dates and claims-made cover

Professional indemnity and cyber are **claims-made**: they respond to claims *notified
during* the policy year, whatever year the work was done, but pay nothing arising from work
performed before the **retroactive date**.

Three tests:

1. **Does the retro date reach back to incorporation?** Check the actual Companies House
   incorporation date against the retro date and against the statement of fact's "when was
   your organisation established". A gap means uninsured historic trading.
2. **Is the continuity real?** A 2015 retro date on a current policy *implies* unbroken
   cover since 2015 but doesn't prove it. Request prior-year schedules. If cover ever
   lapsed, or a renewal moved the date forward, the historic work is unprotected whatever
   today's schedule says.
3. **Will it survive completion?** This is the one that matters for the buyer. A defect in
   old code that surfaces years later is covered only if the policy then in force carries
   the *original* retro date. If the programme is re-broked post-completion and the new
   insurer defaults the retro date to completion, every claim relating to pre-completion
   work falls outside cover and the warranties become the only recourse. Flag that whoever
   places the post-completion cover must match the original date or take the policy over.

Also check for extensions carrying their **own, later** retro date (abuse/molestation on
public liability is a common one) — and question why an unusual extension is on the policy
at all.

### Declared values and maximum allowables — the highest-value test in the review

Schedules commonly carry a **declared value** (turnover for PI/PL/cyber, wage roll for EL)
and a **maximum allowable** above it, typically 25% higher. The mechanism: the insured need
not notify increases *provided* the original declaration was accurate **and** they neither
exceed nor **reasonably expect to exceed** the maximum.

- **Get the target's actual current-year revenue and wage roll** and compare. This is a
  five-minute check against the financial pack that regularly finds a live problem.
- The test is **forward-looking**. The duty bites when the overrun becomes foreseeable, not
  when it happens.
- **Exceeding the ceiling does not increase the cover.** Limits stay as scheduled. Raising
  one needs a request and the insurer's agreement, usually with additional premium.
- **Timing determines severity.** If turnover grew after renewal, it's a failure to notify
  mid-term — fixable. If the declared figure was already wrong *when given*, it's a fair
  presentation problem under the Insurance Act 2015, which is materially worse.
- **The remedy is proportionate, not binary.** Turnover-rated covers pay a reduced share of
  any claim reflecting the premium that would have been charged on the correct figure.
  Avoidance is available if the insurer would have declined the risk outright.
- Remediation is cheap while no claim is outstanding and expensive afterwards. Recommend
  written notification to the broker with actual and forecast figures, and a mid-term
  endorsement, **before completion**, with written insurer confirmation that cover is
  unaffected.

### Statement of fact answers — test them against what the business actually does

The statement of fact is where policies get avoided. Read every question and answer and ask
whether it is *true of this business*, not whether it's internally consistent. The answers
that repay attention:

- does the business process, transact or store **personal data**?
- does it hold **medical information**, card data, bank details or government ID?
- does it provide **hosting, SaaS, PaaS or IaaS**?
- does it use **sub-contractors or consultants**?
- does it design **medical, safety-critical or financial systems**?
- does it always work to **signed contracts** and always **cap its liability**?
- **claims and circumstances**: any prior claim, or awareness of anything that might give
  rise to one?

A healthcare software business declaring that it holds no personal data and no medical
information, or a SaaS business declaring it provides no hosting, is a material
misrepresentation risk affecting both the PI and cyber cover. Flag as PRIORITY, get
management's written confirmation, and if wrong, corrected disclosure to the insurer
pre-completion.

Nil declared claims and circumstances supports the seller's warranty position but is an
assertion — always request a **claims experience letter for the last three to five years**
from the broker or insurer for independent confirmation.

### Employers' liability, the ERN and ELTO

Schedules require the insured to provide, for each entity insured under the EL section,
the employer name, full address and **HMRC Employer Reference Number**, and to notify
changes immediately.

The ERN is the key that files the policy onto the **Employers' Liability Tracing Office**
database, so a former employee claiming years later can identify which insurer covered the
employer at the date of exposure. EL is the longest-tail liability in the programme —
stress, repetitive strain and industrial disease claims surface long after employment ends,
and the responding policy is the one in force at exposure. If the ELTO record is missing or
misfiled, a future claimant may be unable to trace the insurer and the claim lands on the
company as employer of last resort — i.e. on the buyer.

Request: the ERN, written confirmation it has been notified, an ELTO search confirming the
record resolves, and whether any staff transferred in under TUPE or the PAYE scheme changed
(historic ERNs would then need their own traceable records).

Also check the statutory certificate is displayed at each place of business, and note that
such certificates often state the statutory minimum (£5m) while the schedule shows a higher
actual limit.

### Gaps — what isn't there

Check explicitly for these and flag each absence:

- **Directors' and officers' / management liability**, and **employment practices liability**
- **Business interruption** — both property BI and **cyber business interruption**. Cyber BI
  is frequently marked "Not covered" on the schedule while the certificate says nothing
  about it. For a software business with no BI cover of any kind, a ransomware event or
  outage produces no income protection at all. Also check **bricking**.
- **Buildings** cover where premises are leasehold — usually correctly absent, but confirm
  the lease doesn't require it
- **Key person**, product recall, or anything a customer contract mandates

### Adequacy, not just existence

- Reconcile property sums insured to the **fixed asset register** — underinsurance triggers
  averaging.
- Check the **per-vehicle / in-transit limit** against the declared maximum load. These
  routinely contradict each other on the same schedule.
- Cross-check every limit against the **minimum insurance levels required by the target's
  material customer contracts** and public-sector frameworks (GP IT Futures, G-Cloud). If a
  contract review has been done for the same deal, tie the two together.
- Sanity-check limits against turnover and the largest single contract value.
- Note where cover is **UK-only** but the business travels or contracts abroad.

### Premium, payment and the money trail

- Sum the section premiums and tie them to the charged premium on the schedule. They should
  reconcile exactly; a variance means a section has been missed.
- Count the instalments on the payment schedule and multiply by the instalment amount. If it
  doesn't reach the total premium, one or more collections predate the schedule — confirm
  premiums are paid up to date and no instalment is unpaid (unpaid direct debits typically
  let the insurer cancel immediately rather than on 30 days' notice).
- Check whose **bank account** pays the premium. A personal name in the account-holder field
  may simply be the mandate signatory on a business account — so raise it as a question, not
  a finding, and close it out from the target's bank statements. If the premiums don't appear
  in the company's own records, it's a director-funded cost and a related-party /
  normalisation item.

### Change of control and renewal

Note whether the policy is **continuing cover** (auto-renews for a further 12 months unless
cancelled or the risk changes) or a fixed term. Confirm whether change of control on
completion is a material change requiring notification, whether cover continues
post-completion or must be re-broked, and what notice period applies each way.

### Where cover was narrowed at renewal

The summary of change document shows both improvements and reductions. The reductions are
the finding — e.g. legal expenses cover losing data protection and hacking-related claims,
or new exclusions being added. Record them in Comments for the affected section.

## Step 6 — Build the workbook

Three tabs.

**Tab 1 — the populated review template.** Keep the user's exact tab name and column
headers where they've supplied them. One row per cover section plus a total row.

**Tab 2 — Document Index.** Every file in the folder: number, file name, dataroom ref,
document type, what it contains, whether reviewed, and comments. This proves nothing was
missed and tells the user which documents are load-bearing and which are standard market
paper. Mark the policy schedule as the primary document.

**Tab 3 — Premium Recon.** Section limits, excesses and premiums; a `SUM` of the sections;
the charged premium from the schedule; a variance formula (must be nil); then IPT, total
gross premium, instalment amount, instalment count, value of listed instalments, and the
unreconciled amount.

Use `openpyxl`. Requirements:

- **Arial throughout.** Navy (`1F3864`) header row with white bold text, banded fill on
  alternating rows, thin grey borders, wrapped text, top-aligned cells.
- **Freeze panes** after the identifying columns and **add an autofilter** over the table.
- Highlight `PRIORITY` cells in the Outstanding column (amber fill `FFF2CC`, dark red text).
- Shade the total row (`DDEBF7`) and bold it.
- **Use real formulas** for every total and variance, never Python-computed values.
- Set generous column widths and row heights — but recheck row heights after condensing the
  Coverage column, or the sheet looks empty.
- Save as a **new file** (`<template name> - COMPLETED.xlsx` or similar) so the original
  template is untouched.
- **Run the xlsx skill's `scripts/recalc.py`** on the output and confirm zero formula errors
  before delivering.
- If the file is locked because the user has it open in Excel, save a `v2` rather than
  failing.

## Step 7 — Verify before delivering

- **Premium tie-out**: sum of section premiums equals the schedule's charged premium exactly.
- **Cross-document consistency**: policy number, insured name, period of insurance and every
  limit agree between the schedule and each certificate. Any mismatch is a finding.
- **Completeness**: no expected cell empty; every file in the folder appears on the index;
  every cover section on the schedule's summary table has a row.
- **Arithmetic**: instalments × amount reconciled to total premium.
- For high-stakes packs, dispatch a subagent to check the compiled sheet against the sources.

## Step 8 — Save, present, summarise

Save to the deal folder (or an accessible folder, telling the user, if the deal folder can't
be written). Present with the file-sharing tool.

Then give a **short** summary — four or five bullets, not a recital of the table. Lead with
whatever would change the buyer's view: disclosure defects in the statement of fact, missing
covers, business interruption gaps, an unnamed broker, a declared-value overrun. State the
programme's shape in one sentence first (single policy vs several, insurer, period, total
premium) because it explains the row structure.

Offer to consolidate the Outstanding column into a single seller query list, and to trim the
Comments and Outstanding columns if the user wants them shorter.

## Tone when the user asks follow-up questions

Users interrogate this output — "what page is that on", "where does it say this", "what's the
point of X". Answer with the page reference and keep it tight. If an earlier statement was
firmer than the document supports, correct it plainly rather than defending it. Add "not
insurance advice, the broker should confirm" only where the user is asking what *they* should
do, not on every answer.

