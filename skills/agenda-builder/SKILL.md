---
name: agenda-builder
description: Build a Tern Capital management-meeting agenda from an Information Memorandum (IM) and create a draft email in Superhuman, addressed to the seller or their advisor. Trigger whenever the user uploads or references an IM and asks to build / draft / put together an agenda, or says things like "agenda for the management call", "agenda for the mgt meeting", "draft an agenda email", "send the agenda to [advisor/seller]", or any variation where an IM-driven management-meeting agenda needs to be turned into a Superhuman draft. Also trigger when the user pastes IM contents or links to an IM and mentions a forthcoming management call. Output is always a Superhuman draft using the canonical Tern agenda template, enriched with IM page references and key proper nouns (product names, sector names, customer types).
---

# Agenda Builder

## What this skill does

Turns an IM (Information Memorandum / CIM / teaser) into a polished management-meeting agenda email and saves it as a Superhuman draft. The agenda follows Tern Capital's canonical template — never invent new sections, never reorder them, never drop sub-bullets — and is enriched at the section-title level with **IM page references** and **key proper nouns** (product names, customer sectors, etc.) so the agenda reads as bespoke to the target.

The output is **always** a Superhuman draft, created via `create_or_update_draft` with `type="new"` and the agenda passed in `body` (HTML). Use `body` not `instructions` — the agenda must go in verbatim; we don't want Superhuman's writer paraphrasing structured bullets or page references.

## When to use

Trigger this skill whenever James asks for a management-meeting agenda for a software acquisition target, especially when an IM is attached or referenced. Common phrasings:

- "Build the agenda for [target]"
- "Draft an agenda email to [advisor]"
- "Agenda for the call with [target] / [seller name]"
- "Put together the agenda for the management meeting"
- "Send the agenda over to [advisor]"

Even if the user just says "agenda" plus uploads an IM, trigger this skill — that's the most common shorthand.

## Inputs

The skill needs:

1. **The IM** — usually a PDF in `uploads/`, but may be a Notion deal page, .docx, or pasted text. Extract page numbers from a PDF wherever possible (use the `pdf` skill if helpful).
2. **The target company name** — derived from the IM cover, or from the user's prompt.
3. **Recipient details** — who the email goes to. Always ask if not obvious:
   - Is it going to the **advisor/broker** or **direct to the seller**?
   - Recipient name + email
   - If via advisor, who's on the other side (e.g. "Naresh & Alpa") so the framing line names them
4. **Meeting timing context** — a short phrase that fits naturally into the opener: "later today", "next week", "tomorrow morning", "on Thursday", etc. If unclear, ask.

If anything in 3 or 4 is missing, ask using AskUserQuestion before drafting. Don't guess on recipient email — getting that wrong is worse than asking.

## The canonical agenda template

This is **the** template. Use it exactly. The bullet structure below is the source of truth — not the past-email examples. Always include every section and every sub-bullet, even if the IM is light on a particular topic (it's the seller's job to fill in gaps in the meeting, not yours to omit the line).

```
Background, intros and rationale for sale
Product and market
  Key products and services + relevant use cases
  Key competitors and USPs
  Product demo (if possible)
Commercial
  Pricing model/LTV and contract structure
  Growth opportunities
  Sales process - marketing, lead generation, conversion rates
  Current pipeline - size and shape + review of top opportunities
  Typical reasons for a) losing customers and b) losing pipeline opportunities
Team
  Team structure, key roles and responsibilities
Technology and software
  Tech stack
  Architecture
Financials
  Last financial year P&L + YTD performance against forecast
  Revenue split - by product/service, by customer sector, by anonymised customer
  Gross margins - by product/service
  EBITDA definition - does it include/exclude R&D costs, normalised management costs, furlough income, R&D tax credit
```

The verbatim template is also in `assets/template.md` — read that file first before drafting and treat it as immutable.

## Enrichment rules (the bit that makes it feel bespoke)

After laying out the template, enrich each main section header with two things:

### 1. Page references from the IM

Add `(pp. X–Y)` — or `(p. X)` for a single page — to each main section, and to sub-bullets where useful. Use an en-dash `–` for ranges, not a hyphen. Multi-region refs are fine: `(pp. 9–14, 20–22)`.

If the IM has a clear table of contents, use that. Otherwise scan section headers and pick the page range covering each topic. If you genuinely can't find a page range for a section (e.g. the IM is light), it's fine to omit the page ref for that one — never invent one.

### 2. Key proper nouns (titles, not sentences)

Slip in a *short* parenthetical or trailing fragment with target-specific names. **Names only — never full sentences and never opinions.** Examples of the kind of enrichment that's allowed:

- `Product Demo – SCANNER / VERIFY / SHIELD (pp. 10–12)` ← product names
- `Market positioning (ERP / JD Edwards focus)` ← tech / niche
- `Target customers and sectors (Medical & Pharma)` ← sectors
- `Key products and services (WhosOff + WhosOffice)` ← product names
- `Pipeline & Geographic Expansion (p. 17)` ← topic emphasis from IM

Rules of thumb:

- Maximum ~6 words of enrichment per line
- Only add it where the IM gives you a genuine, distinctive name (product, sector, geography, technology stack). If nothing distinctive jumps out for a section, leave the template wording alone.
- Never invent. If the IM doesn't name a product, don't make one up.
- Don't add commentary, opinions, or USP claims — just titles/names.

This is the single most important style point. The point of enrichment is to make the recipient feel the agenda was written *for them*, not pulled off a shelf. Generic agendas signal a tourist; specific ones signal that James has read their IM.

## Email structure

### Opening line

Match James's two standard openers — pick whichever fits the recipient and timing:

**Via advisor (most common):**
> Hi [First name],
>
> Please see below for a proposed agenda for the management call [timing], would you be able to circulate this with the [Target] team?

**Via advisor, with named principals:**
> Hi [First name],
>
> Please see below for an agenda for the call [timing] with [Principal names], would you be able to forward this over to them before the call?

**Direct to seller:**
> Hi [First name],
>
> Please see below for a proposed agenda for our call [timing] — looking forward to it.

Use British English. Lowercase after the comma in "would you be able to..." matches James's actual style — keep it.

### Agenda body

Render as bullets. Numbering (1., 2., 3.) is optional — both numbered and unnumbered work; default to **unnumbered** unless the user asks otherwise. Sub-bullets indented one level. Page refs go on the section header line; sub-bullet enrichments stay short.

### Sign-off

End with `Best regards,` on its own line. **Do not** type the signature block — Superhuman appends James's signature automatically. Just `Best regards,` and stop.

## Composing the Superhuman draft

Build the HTML body yourself and pass it via `body` (not `instructions`). Use this skeleton:

```html
<p>Hi [First name],</p>
<p>Please see below for a proposed agenda for the management call [timing], would you be able to circulate this with the [Target] team?</p>
<ul>
  <li>Background, intros and rationale for sale (pp. X–Y)</li>
  <li>Product and market (pp. X–Y)
    <ul>
      <li>Key products and services + relevant use cases (PRODUCT_A / PRODUCT_B)</li>
      <li>Key competitors and USPs</li>
      <li>Product demo (if possible)</li>
    </ul>
  </li>
  <!-- ...remaining sections... -->
</ul>
<p>Best regards,</p>
```

Then call:

```
create_or_update_draft(
  type="new",
  to=["advisor.name@firm.com"],
  subject="[Target] — proposed agenda for management call",
  body=<the HTML above>
)
```

Subject line conventions:
- If replying inside an existing thread (advisor already emailed about the IM), call with `type="reply"` and pass `thread_id` — Superhuman handles the subject prefix.
- For a fresh thread, use `[Target] — proposed agenda for management call` or `[Project codename] — agenda for management meeting` if a project codename is being used.

## Handling tricky IMs

- **Scanned PDF / no extractable text:** invoke the `pdf` skill to OCR, then re-read.
- **Missing page numbers:** treat a printed page number on the IM cover as page 1 of references. If the IM has both a cover-numbered scheme and a PDF-page scheme, use the printed numbers.
- **Generic IMs with no distinctive product names:** it's OK to skip enrichment. Bland is better than fabricated.
- **No financial pages in IM:** still include the full Financials section — just without page refs. The point of the agenda is to flag what we want to discuss, not just what's already covered.

## Working examples (for calibration)

### Example A — via advisor, same-day call (MCP Insight pattern)

> Hi Mary,
>
> Please see below for a proposed agenda for the management call later today, would you be able to circulate this with the MCP team?
>
> - Background, Introductions & Investment Rationale (pp. 3–4)
> - Product & Market (pp. 9–14, 20–22)
>     - Key Products & Use Cases (pp. 9–14)
>     - Competitive Landscape & Differentiation (pp. 6, 22)
>     - Product Demo – SCANNER / VERIFY / SHIELD (pp. 10–12)
> - Commercial Overview (pp. 4, 7, 15–17)
>     - Revenue Model & Contract Structure (p. 4)
>     - Growth Opportunities (p. 7)
>     - Sales & Customer Base / Revenue Mix (pp. 15–16)
>     - Pipeline & Geographic Expansion (p. 17)
>     - Customer / Market Risks & Churn Drivers (pp. 13, 18)
> - Team & Organisation (pp. 24–25)
> - Technology & Platform (pp. 6, 10–12)
> - Financials (pp. 5, 27–28)
>     - Historical Performance & Forecast (pp. 5, 27)
>     - Revenue Breakdown (pp. 15–16)
>     - Margins & EBITDA (pp. 5, 27)
>     - Balance Sheet & Key Ratios (p. 28)
>
> Best regards,

### Example B — via advisor, named principals, numbered (Exiom pattern)

> Hi Oliver,
>
> Please see below for an agenda for the call next week with Naresh & Alpa, would you be able to forward this over to them before the call?
>
> 1. Background, Introductions & Rationale for Sale (pp. 1–2)
>     - Introduction to Tern and interest in Exiom
>     - Introduction to Exiom
>     - Business background and history
>     - Ownership structure
>     - Rationale for sale
> 2. Product & Market Overview (pp. 3–5)
>     - Market positioning (ERP / JD Edwards focus)
>     - Target customers and sectors (Medical & Pharma)
> ... (remaining sections per template)
>
> Best regards,

Notice: Example B keeps full descriptive sub-bullets in section 1 ("Introduction to Tern and interest in Exiom" etc.) — this is fine when the IM gives you the substance to fill them in. Example A is tighter. Both are valid; lean tighter unless the IM gives you something concrete to elaborate.

## Workflow checklist

1. Read the IM (use `pdf` skill if needed for OCR/text extraction).
2. Pull out: target name, product/service names, customer sectors, geography, tech stack hints, and a rough page-by-section map.
3. If recipient/timing aren't clear from context, ask via AskUserQuestion.
4. Read `assets/template.md` and lay out the agenda using that exact structure.
5. Enrich each main section with page refs and (where genuinely available) short proper-noun fragments.
6. Compose the opener using the right framing for advisor vs direct-to-seller.
7. Build the HTML body.
8. Call `create_or_update_draft(type="new", to=[...], subject=..., body=<html>)`.
9. Tell James the draft is in Superhuman and offer to tweak before he sends.

Do **not** send the draft — only create it. James reviews and sends himself.
