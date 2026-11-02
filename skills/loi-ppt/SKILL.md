---
name: loi-ppt
description: "Generate a Tern Capital non-binding Letter of Intent (LOI) PowerPoint deck for acquiring a B2B Enterprise Software business in the UK. Use whenever the user says 'LOI deck', 'LOI presentation', 'create an LOI slide deck', 'non-binding indication of interest deck', 'IOI deck', or asks to produce a PowerPoint deck for a software acquisition offer. This skill produces a full 11-slide .pptx that is an exact replica of the Tern LOI template, then populates slides 3 (market overview), 4 (our interest & value creation thesis), and 8 (offer terms) from uploaded documents."
---

# Tern Capital — LOI PowerPoint Deck Skill

## Overview

This skill produces a full 11-slide PowerPoint deck that is an **exact replica** of the Tern Capital LOI template. It then auto-populates slides 3, 4, and 8 using the user's uploaded documents (financial model, IM, and market research).

**Core mechanic:** The user uploads the LOI template `.pptx` alongside their deal documents. Claude uses `store_blob` to load the template, then `insertSlidesFromBase64` to copy all 11 slides verbatim into the current presentation — preserving every image, logo, icon, and layout exactly. Only slides 1, 3, 4, and 8 are then edited with deal-specific content. Slides 2, 5, 6, 7, 9, 10, and 11 are never touched after insertion.

**Template file handling:**
1. User uploads the `.pptx` as a file attachment — it arrives via `container_upload`
2. Use `store_blob` with the file's `file_id` to load it into the browser sandbox as `"loi-template"`
3. Then use `blobs.getBase64("loi-template")` and `blobs.getSlideIds("loi-template")` inside `execute_office_js`

Always load `tern-brand-guidelines` and `tern-slide-formatting` skills before starting.

---

## Step 1 — Document collection

On first invocation, ask the user to upload the following. Use `ask_user_question` for this:

> "To build the LOI deck, please upload:
> 1. **The Tern LOI template .pptx** — the master template file (used to copy all fixed slides verbatim, including images and logos)
> 2. **Financial model** (Excel or PDF) — used to extract ARR, EBITA, churn, valuation assumptions
> 3. **Information Memorandum (IM)** (PDF or Word) — used to extract company overview, products, market position
> 4. **Market research** (any format) — used to populate the market overview slide

Once uploaded, also ask:
- **Company name** (full legal name)
- **Date** for the cover slide (format: DD Month YYYY, e.g. "17 February 2026")
- **Offer price** (total, e.g. "£1.25M")
- **Upfront consideration** (e.g. "£650K")
- **Deferred/contingent consideration** details if any

If the user does not upload the deal documents, you can still build the deck with placeholder text in slides 3, 4, and 8 — note which sections need completing.

**The LOI template .pptx is required.** If the user does not provide it, explain that it is needed to preserve all images and logos on the fixed slides (especially slides 2 and 6), and ask them to upload it before proceeding.

---

## Step 2 — Parse uploaded documents

Use `code_execution` (Python with pandas/pdfplumber/python-docx) to extract the following from each document:

### From the financial model:
- ARR (Annual Recurring Revenue) — look for ARR, recurring revenue, or subscription revenue figures
- EBITA (NOT EBITDA — always EBITA per Tern standards)
- Gross churn / net revenue retention
- Revenue split (recurring vs non-recurring)
- Period of accounts (e.g. "year ended 31 August 2025")
- NTA calculation if available
- Any locked box date

### From the Information Memorandum:
- Company full legal name and any trading name
- Product name(s) and brief description
- Number of customers / surgeries / practices
- Key customer names (for deferred consideration references)
- Exclusive partnerships or integrations
- Founding team / key personnel (e.g. founder's name and role)
- Growth story and go-to-market

### From market research:
- Market size (£ value and CAGR)
- Key market trends (regulatory, NHS mandates, technology shifts)
- Competitor landscape (main named competitors)
- Regulatory/policy drivers (NHS programmes, ICB structure, etc.)

---

## Step 3 — Build the deck

Build the deck **slide by slide**, one tool call per slide. Do NOT batch everything into a single call.

### 3a — Load the template and insert all slides

The user has uploaded the LOI template `.pptx`. Use `store_blob` to fetch it into the browser sandbox, then use `insertSlidesFromBase64` to copy all 11 slides into the current (blank) presentation. This is the ONLY correct way to preserve images, logos, and icons on slides 2 and 6.

**Workflow:**

```javascript
// 1. Get slide IDs from the template in order
const slideIds = await blobs.getSlideIds("loi-template");
// slideIds is an array in presentation order, e.g. ["256", "257", "258", ...]
// Template slide order: [0]=cover, [1]=tern-overview, [2]=market, [3]=interest,
//                        [4]=playbook, [5]=sales-playbook, [6]=divider,
//                        [7]=offer, [8]=dd-divider, [9]=dd-table, [10]=training

// 2. Insert ALL 11 slides from the template into the current presentation
const base64 = blobs.getBase64("loi-template");
await context.presentation.insertSlidesFromBase64(base64, {
  formatting: "KeepSourceFormatting"
});
await context.sync();
```

After inserting, call `execute_office_js` to list all slides and confirm all 11 are present. Note the new slideIds assigned by the current presentation (they will differ from the template's IDs).

**Fixed slides — do NOT edit after inserting:**
- Position 2: Tern overview — portfolio logos, key stats images. DO NOT TOUCH.
- Position 5: Playbook table — fixed content. DO NOT TOUCH.
- Position 6: Sales effectiveness playbook — icons/images. DO NOT TOUCH.
- Position 7: Divider — fixed orange background. DO NOT TOUCH.
- Position 9: DD timeline divider. DO NOT TOUCH.
- Position 10: DD table. DO NOT TOUCH.
- Position 11: Training academy — full-page image. DO NOT TOUCH.

**Slides to edit after inserting:**
- Position 1: Cover — update company name and date
- Position 3: Market overview — replace all bullet content
- Position 4: Our interest & thesis — replace all bullet content
- Position 8: Offer — update title, subtitle, table values, and all bullets

### 3b — Editing the inserted slides

After insertion, use `list_slide_shapes` on each slide to be edited to get the current shape refs (IDs change on insert). Then use `edit_slide_xml` to update text in place.

**NEVER delete and recreate a slide.** Always edit shapes in place on the inserted slide.

### Deck structure

| Pos | Source | Type | Title / purpose |
|-----|--------|------|-----------------|
| 1 | Template pos 1 — edit | Title slide (orange bg) | "Non-Binding Indication of Interest for [Company Name]" + date |
| 2 | Template pos 2 — FIXED | Content (white bg, logos) | "Tern overview" — do not change |
| 3 | Template pos 3 — edit | Content (white bg, bullets) | "Our understanding of the [market] and the competition" — POPULATE |
| 4 | Template pos 4 — edit | Content (white bg, 2-section) | "Our interest in [Company] and initial view of value creation thesis" — POPULATE |
| 5 | Template pos 5 — FIXED | Content (white bg, table) | Tern playbook — do not change |
| 6 | Template pos 6 — FIXED | Content (white bg, icons) | Sales playbook — do not change |
| 7 | Template pos 7 — FIXED | Divider | Orange background divider — do not change |
| 8 | Template pos 8 — edit | Content (white bg, table + bullets) | "Our offer to purchase [Company] is £X" — POPULATE |
| 9 | Template pos 9 — FIXED | Divider | DD timeline divider — do not change |
| 10 | Template pos 10 — FIXED | Content (white bg, table) | DD timeline table — do not change |
| 11 | Template pos 11 — FIXED | Content (white bg, image) | Training academy — do not change |

---

## Step 4 — Slide-by-slide build instructions

### Slide 1 — Cover

**Layout:** Orange background (Tern Orange #EB5C32). White text. Centered title.

**Shape structure (from original):**
- Shape 112: Placeholder, left=36pt, top=221pt, width=648pt, height=89pt. Center-aligned. Contains title (line 1: "Non-Binding Indication of Interest for [Company Name]", line 2: "[Date]"). Font: DM Sans, inherited from master.
- Shape 111: TextBox, left=311pt, top=372pt, width=98pt, height=18pt. Contains: "Strictly private and confidential". Color: Tern Orange (#EB5C32), sz=600 (6pt). Center-aligned.

**How to build:** The cover slide is already inserted from the template at position 1. Use `list_slide_shapes` to find the title placeholder and confidentiality textbox, then update text only using `edit_slide_xml`.

**Text XML for shape 112:**
```xml
<a:p><a:pPr marL="0" lvl="0" indent="0" algn="ctr" rtl="0"><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr><a:r><a:rPr lang="en-GB"/><a:t>Non-Binding Indication of Interest for </a:t></a:r><a:br><a:rPr lang="en-GB"/></a:br><a:r><a:rPr lang="en-GB"/><a:t>[Company Name]</a:t></a:r><a:endParaRPr/></a:p>
<a:p><a:pPr marL="0" lvl="0" indent="0" algn="ctr" rtl="0"><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr><a:r><a:rPr lang="en-GB"/><a:t>[Date]</a:t></a:r><a:endParaRPr/></a:p>
```

---

### Slide 2 — Tern overview (FIXED)

Inserted verbatim from the template. Contains logos of Tern's portfolio companies and key stats. DO NOT TOUCH.

---

### Slide 3 — Market overview (POPULATE)

**Layout:** White background. Single title bar. Full-width bullet point text box below title.

**Shape structure:**
- Shape 162: Placeholder at top (title). Left=16pt, top=11pt, width=663pt, height=27pt. DM Sans, sz=1800 (18pt), black.
- Shape 163: TextBox. Left=15pt, top=47pt, width=684pt, height=354pt. Bullet points sz=1100 (11pt), DM Sans, black.

**Title format:** "Our understanding of the [sector] market and the competition"

**Bullet format (OOXML paragraph template):**
```xml
<a:p><a:pPr marL="135000" lvl="0" indent="-114850" algn="l" rtl="0"><a:spcBef><a:spcPts val="900"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClr><a:schemeClr val="dk1"/></a:buClr><a:buSzPts val="1100"/><a:buFont typeface="Ubuntu"/><a:buChar char="•"/></a:pPr><a:r><a:rPr lang="en-GB" sz="1100"><a:solidFill><a:schemeClr val="dk1"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:rPr><a:t>[BULLET TEXT]</a:t></a:r><a:endParaRPr sz="1100"><a:solidFill><a:schemeClr val="dk1"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:endParaRPr></a:p>
```
First bullet: `<a:spcBef><a:spcPts val="0"/></a:spcBef>`. Subsequent bullets: `val="900"`. Last bullet: `<a:spcAft><a:spcPts val="900"/></a:spcAft>`.

**Content to generate (8-10 bullets) covering:**
1. Market structure (regulatory units — e.g. ICBs, PCNs, practices)
2. Market size and growth rate (£ figure + CAGR)
3. Government/NHS investment commitments
4. NHS strategic direction (NHS Long Term Plan, ICS, etc.)
5. Procurement landscape (centralisation trends)
6. Clinical systems competitive landscape (dominant players)
7. Emerging competitors / disruptors
8. Regulatory mandates creating demand (e.g. Single Patient Record, digital-first)
9. New care delivery models creating software demand
10. Target company's competitive differentiation vs named competitors

Write each bullet as a **standalone sentence ending with a full stop**. Sentence case. No bold.

---

### Slide 4 — Our interest & value creation thesis (POPULATE)

**Layout:** White background. Two vertical sections separated by a thin line. Left rotated label for each section.

**Shape structure:**
- Shape 169: Placeholder (title), left=12pt, top=7pt, width=681pt, height=27pt
- Shape 170: TextBox (top section — "Our interest"), left=25pt, top=51pt, width=690pt, height=144pt
- Shape 176: TextBox (bottom section — "Value creation"), left=27pt, top=196pt, width=690pt, height=193pt
- Shape 171: GeometricShape (rotated label "Our interest"), left=-43pt — DO NOT EDIT
- Shape 172: Line (vertical divider) — DO NOT EDIT
- Shape 173: GeometricShape (rotated label "Value creation thesis"), left=-50pt — DO NOT EDIT
- Shape 174: Line (vertical divider) — DO NOT EDIT

**Title:** "Our interest in [Company Name] and initial view of value creation thesis"

**Top section — "Our interest" bullets (4 bullets):**
```xml
<a:p><a:pPr marL="135000" lvl="0" indent="-114850" algn="l" rtl="0"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:spcBef><a:spcPts val="600"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClr><a:srgbClr val="000000"/></a:buClr><a:buSzPts val="1100"/><a:buFont typeface="Ubuntu"/><a:buChar char="•"/></a:pPr><a:r><a:rPr lang="en-GB" sz="1000" dirty="0"><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:rPr><a:t>[BULLET TEXT]</a:t></a:r><a:endParaRPr sz="1000" dirty="0"><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:endParaRPr></a:p>
```
First bullet: `<a:spcBef><a:spcPts val="0"/></a:spcBef>`. Last bullet: `<a:spcAft><a:spcPts val="600"/></a:spcAft>`.

**Our interest content (4 bullets):**
1. Why [Company] fits Tern's investment criteria (vertical market software specialist, mission-critical, recurring revenue)
2. Product strength / customer base / exclusives / integrations (specific metrics from IM)
3. Portfolio fit — connection to Tern's existing portfolio companies
4. Cross-sell opportunity (especially into Noveva/public sector group if applicable)

**Bottom section — "Value creation" bullets (5 bullets):**
```xml
<a:p><a:pPr marL="135000" lvl="0" indent="-102150" algn="l" rtl="0"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:spcBef><a:spcPts val="600"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClr><a:srgbClr val="000000"/></a:buClr><a:buSzPts val="900"/><a:buFont typeface="Ubuntu"/><a:buChar char="•"/></a:pPr><a:r><a:rPr lang="en-GB" sz="1000"><a:solidFill><a:schemeClr val="dk1"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:rPr><a:t>[BULLET TEXT]</a:t></a:r><a:endParaRPr sz="1000"><a:solidFill><a:schemeClr val="dk1"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:endParaRPr></a:p>
```
Last bullet: `<a:spcAft><a:spcPts val="200"/></a:spcAft>`.

**Value creation content (5 bullets):**
1. Cross-sell through Noveva/portfolio into NHS/ICB/PCN relationships
2. GTM strategy: tenders, sales effectiveness, Sandler methodology
3. Lead generation programme (personalised outreach, content marketing, lead scoring)
4. In-house CTO support for tech best practices (CI/CD, DevOps, automated testing)
5. M&A — bolt-on acquisitions in adjacent primary care workflow/patient engagement/population health

---

### Slides 5 & 6 — Playbook slides (FIXED)

Inserted verbatim from the template. Slide 6 contains icon images. DO NOT EDIT.

---

### Slide 7 — Divider (FIXED)

Inserted verbatim from the template. Orange background, centered title text. DO NOT EDIT.

---

### Slide 8 — Offer terms (POPULATE)

**Shape structure:**
- Shape 226: Placeholder (title), left=12pt, top=7pt, width=681pt, height=27pt
- Shape 228: TextBox (subtitle), left=15pt, top=41pt, width=676pt, height=22pt. sz=900, bold.
- Shape 233: Table (graphicFrame), left=38pt, top=61pt, width=654pt, height=106pt
- Shape 225: TextBox ("Offer" bullets), left=29pt, top=172pt, width=684pt, height=105pt
- Shape 234: TextBox ("Assumptions" bullets), left=30pt, top=288pt, width=684pt, height=114pt
- Shapes 229–232: Rotated labels + lines — DO NOT EDIT

**Title (shape 226):** "Our offer to purchase [Company Name] is £[TotalPrice]"

**Subtitle (shape 228):** "Our non-binding offer to buy 100% of the shares of [Company Name]:"

**Table (shape 233) — 1 header row + 1 data row, 6 columns:**
- Column widths (EMU): 2464550 / 985825 / 1153400 / 1340725 / 1370300 / 985825
- Header: ["", "ARR", "EBITA", "Multiple", "Upfront consideration", "Deferred consideration"]
- Data: ["[Company Name]", "£[ARR]", "£[EBITA]", "[X]x", "£[Upfront]", "£[Deferred]"]
- Header fill: #EB5C32, white text, sz=900, DM Sans
- Data fill: #FFFFFF, black text, sz=900, DM Sans

**Table header cell OOXML:**
```xml
<a:tcPr marL="28575" marR="28575" marT="19050" marB="19050" anchor="b">
  <a:lnL w="9525" cap="flat" cmpd="sng"><a:solidFill><a:srgbClr val="CCCCCC"><a:alpha val="0"/></a:srgbClr></a:solidFill><a:prstDash val="solid"/></a:lnL>
  <a:lnR w="9525" cap="flat" cmpd="sng"><a:solidFill><a:srgbClr val="CCCCCC"><a:alpha val="0"/></a:srgbClr></a:solidFill><a:prstDash val="solid"/></a:lnR>
  <a:lnT w="9525" cap="flat" cmpd="sng"><a:solidFill><a:srgbClr val="CCCCCC"><a:alpha val="0"/></a:srgbClr></a:solidFill><a:prstDash val="solid"/></a:lnT>
  <a:lnB w="9525" cap="flat" cmpd="sng"><a:solidFill><a:srgbClr val="CCCCCC"><a:alpha val="0"/></a:srgbClr></a:solidFill><a:prstDash val="solid"/></a:lnB>
  <a:solidFill><a:srgbClr val="EB5C32"/></a:solidFill>
</a:tcPr>
```

**Offer/Assumptions bullet paragraph template (sz=900):**
```xml
<a:p><a:pPr marL="203200" lvl="0" indent="-196850" algn="l" rtl="0"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="300"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClr><a:srgbClr val="000000"/></a:buClr><a:buSzPts val="900"/><a:buFont typeface="Ubuntu"/><a:buChar char="•"/></a:pPr><a:r><a:rPr lang="en-GB" sz="900"><a:solidFill><a:srgbClr val="000000"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:rPr><a:t>[BULLET TEXT]</a:t></a:r><a:endParaRPr sz="900"><a:solidFill><a:srgbClr val="000000"/></a:solidFill><a:latin typeface="DM Sans"/><a:ea typeface="Ubuntu"/><a:cs typeface="Ubuntu"/><a:sym typeface="Ubuntu"/></a:endParaRPr></a:p>
```
First bullet: `<a:spcBef><a:spcPts val="0"/></a:spcBef>`.

**Offer bullets (shape 225):**
1. £[Upfront] will be paid upfront on completion ("Upfront Consideration") adjusted for Net Tangible Assets ('NTA').
2. NTA will be calculated by taking the current assets minus all liabilities based on [Locked Box Date] ("Locked Box Date"). We will hold back two months of COS and overheads for working capital purposes.
3. £[Deferred] will be paid in [N] equal instalments at the end of Y1, Y2 and Y3 [of the renewal of [key customers]], subject to the renewal being equal to or greater than the respective current renewal prices.
4. Our valuation is based on sustainable EBITA, ARR, gross churn, along with our industry knowledge of acquiring software companies in the [sector].
5. As discussed, we are keen for [founder name] to remain in the business on a part time basis. We will support them through the growth journey.

**Assumptions bullets (shape 234):**
1. ARR is £[X] as per the "[source document]" provided in the data room.
2. Non-recurring revenue is minimal and the vast majority of the revenue is from recurring software fees.
3. Sustainable EBITA as outlined in the financial statements provided is £[X] for the period ended [date].
4. Gross churn historically is negligible and is expected to be minimal. [Key customers] are sticky customers.
5. All financials are based on generally accepted accounting principles.
6. All intellectual property rights in the products are owned exclusively by the business. There are no significant shortcomings in the underlying technology.
7. Business continues to grow and the performance of the business does not deteriorate in any significant manner.
8. The business will be acquired free from any material onerous liabilities.

---

### Slides 9–11 — Appendix (FIXED)

Inserted verbatim from the template. Slide 11 contains a full-page image. DO NOT EDIT any of these slides.

---

## Step 5 — Font enforcement

All text must use DM Sans as the primary latin typeface. The correct run property pattern:

```xml
<a:rPr lang="en-GB" sz="[SIZE]"><a:solidFill><a:schemeClr val="dk1"/></a:solidFill>
  <a:latin typeface="DM Sans"/>
  <a:ea typeface="Ubuntu"/>
  <a:cs typeface="Ubuntu"/>
  <a:sym typeface="Ubuntu"/>
</a:rPr>
```

If any shape references Ubuntu or Arial as the primary `<a:latin>` typeface (not as ea/cs/sym), update it to DM Sans.

---

## Step 6 — Verification

1. Call `verify_slides` across the full deck
2. Call `verify_slide_visual` on slides 1, 3, 4, and 8
3. Fix any overlaps, overflows, or contrast warnings
4. Confirm no placeholder text remains — no "[COMPANY NAME]", "[DATE]", "[ARR]" etc.

---

## Template visual reference

**Theme colors:**
- dk1: #000000
- dk2: #FFFFFF
- lt1: #B2B2B2
- lt2: #000000
- accent1: #99CCFF
- accent2: #FFE433
- accent3: #D5D5D5
- Tern Orange (hardcoded, not in theme): #EB5C32

**EMU reference (slide = 9,144,000 × 5,143,500 EMU):**
- 1pt = 12,700 EMU
- Slide: 720pt wide × 405pt tall
- Standard left margin: ~16pt
- Standard title top: ~11pt

**Logo:** Top-right on all content slides, ~x=689pt, y=14pt, 21×21pt. Image in slide master (rId7 in slideMaster1.xml).

---

## Step 7 — Key extraction rules

**ARR:** Look for "Annual Recurring Revenue", "ARR", "Subscription revenue". Express as £[X]M or £[X]K. Always state the period.

**EBITA (NEVER EBITDA):** Look for "EBITDA" in the model but always report as EBITA. Express as £[X]M or £[X]K. Always state the period.

**Valuation multiple:** Total Consideration ÷ EBITA. Round to one decimal (e.g. "6.3x"). Use ARR multiple only if pre-profit.

**Churn:** Express as "negligible" / "less than X%". Name specific sticky/anchor customers.

**Competitive landscape (slide 3):** Name specific competitors — never "various players". Reference NHS procurement frameworks and programmes by exact name (NHS App, Federated Data Platform, single patient record mandate, ICS/ICB structures).

---

## Quality checklist

- [ ] All 11 slides present
- [ ] Company name replaced in: slide 1 (cover), slide 3 (title), slide 4 (title + bullets), slide 8 (title + subtitle + bullets)
- [ ] Date on cover: DD Month YYYY format
- [ ] Slide 3: 8–10 specific, factual market bullets — no generic statements
- [ ] Slide 4 top: 4 bullets on Tern's interest in this specific company
- [ ] Slide 4 bottom: 5 bullets on value creation thesis
- [ ] Slide 8 table: correct ARR, EBITA, multiple, upfront, deferred figures
- [ ] Slide 8 offer bullets: correct figures and key customer names
- [ ] Slide 8 assumptions bullets: correct data sources and figures
- [ ] All fonts: DM Sans (not Ubuntu as primary latin)
- [ ] No unused placeholders with default text
- [ ] EBITA throughout — never EBITDA
- [ ] £ figures: correct capitalisation (£1.25M, £650K)
- [ ] All bullets end with a full stop
- [ ] Sentence case throughout — not Title Case