---
name: loi-drafter
description: Draft a formal Letter of Intent (LOI) as a Word document for Tern Capital acquisitions. Use this skill whenever the user mentions LOI, letter of intent, formal offer letter, or wants to turn an IOI/indicative offer into a binding-ready LOI document. Also trigger when the user uploads deal documents (IOI slide deck, IM, financial model) and asks to "draft the LOI", "write up the LOI", "create the offer letter", "put together the LOI", "formalise the offer", or similar. This skill produces a .docx file based on the Tern Capital LOI template — it does NOT produce emails (use the indicative-offer-email skill for that) and it does NOT produce slide deck IOIs.
---

# LOI Drafter

You are drafting a formal Letter of Intent (LOI) as a Word document on behalf of Karthik Dasari, Managing Director of Tern Capital Limited, a UK-based private equity firm that acquires software companies.

The LOI is a **formal document** — not an email. It follows a fixed template structure and is produced as a `.docx` file built directly from the TC LOI Template uploaded by the user at the start of the session.

## When This Skill Triggers

This skill triggers when the user wants to produce a formal LOI document. The user will typically provide one or more of:
- An Indication of Interest (IOI) — usually a slide deck (PDF/PPTX)
- An Information Memorandum (IM) for the target business
- A financial model (Excel)
- Verbal/written deal terms and assumptions

The skill extracts as much information as possible from these documents and only asks the user for what's genuinely missing or ambiguous.

---

## Workflow

### Phase 0: Request LOI template upload, then read deal documents

**Step 1 — Template upload (mandatory, before anything else):**
Before reading any deal documents or asking any deal questions, check whether the user has uploaded a Word document (`.docx`) that is the LOI template. If they have not, ask them to upload it now:

> "Before we begin, please upload the latest Tern Capital LOI template as a Word document (.docx). I will use only this file as the base for the output — I will not use any previously stored version."

Do not proceed until the template `.docx` has been uploaded. Save the uploaded template path for use in Step 2 of the Output section.

**Step 2 — Read deal documents:**
Once the template is received, read all other uploaded documents (IOI slide deck, IM, financial model, etc.). Extract every piece of deal information you can find: company name, directors, deal terms, financials, assumptions, value creation plans, etc. Build a working data model of the deal from these documents.

### Phase 1: Auto-resolve and confirm basic deal info
For each field, try to resolve it automatically. Only ask the user when you genuinely cannot determine the answer.

**Fields to auto-resolve:**

1. **Target company legal name** — Extract from uploaded documents. If ambiguous (e.g. multiple entities mentioned), present options for the user to select from, never ask open-ended.

2. **Target short form name** — Generate abbreviation suggestions from the legal name. Rules: if the name is "ABC Limited", suggest "AL". If "ABC XYZ Limited", suggest "AXL". Take initials of each word excluding "Limited"/"Ltd". Present 2-3 options for the user to pick.

3. **Recipient names** — Search Companies House (via web search) for the target company name to find current directors. The recipients are ALL directors of the target company. Present the list for confirmation. Use query like: `[company name] directors companies house`.

4. **Target company registered address** — Also from Companies House lookup. Present for confirmation, don't ask open-ended.

5. **Date** — Always today's date. Never ask.

6. **Shares acquired** — Default to "100% of the share capital". Confirm with user (almost always 100%).

7. **Acquisition vehicle** — Present three options:
   - Primus Innovations Limited ("Primus") — for sports/media/entertainment vertical
   - Noveva Software Group Limited ("NSG") — for public sector/local authority vertical
   - Forma Innovations Limited ("Forma") — for automotive/transportation vertical
   The user selects one. If the target's sector is clear from the documents, suggest the most likely vehicle.

8. **Share purchase vs asset purchase** — Default to share purchase. Confirm with user. Note: "In most cases this is a share purchase."

### Phase 2: Deal terms (extract from documents, confirm with user)

Present what you've extracted from the uploaded documents and ask the user to confirm or correct. Use selection-based questions wherever possible.

Key deal terms to extract/confirm:

9. **Total enterprise value (£)** — Extract from IOI/documents. Note: IOI narrative and payment tables may differ — always confirm which figure is correct before drafting.

10. **Valuation basis** — EBITDA multiple, EBITA multiple, or blended. Extract the metric, the multiple, and the basis period. E.g. "5.0x sustainable EBITDA of £0.8M".

11. **Sustainable EBITDA/EBITA figure and basis** — Extract from documents.

12. **Upfront consideration** — Amount (£) and percentage of EV if stated.

13. **Guaranteed deferred consideration** — If present: amount, number of instalments, payment schedule.

14. **Contingent consideration / earnout** — If present: metrics (NRR growth, EBITDA thresholds, gross profit), specific targets and payouts per year, capped/uncapped, catch-up mechanisms.

15. **NTA adjustment** — Locked box date and estimated NTA if available.

16. **Working capital mechanism** — Completion accounts or locked box. Any specific definitions.

17. **Pre-completion leakage** — Any permitted leakage (pension withdrawals, dividends, bonuses).

18. **Management incentives** — Growth shares, observation period, retention requirements.

### Phase 3: Investment rationale & value creation

Extract from uploaded documents. Ask user to confirm or supplement:

19. **Sector/vertical** — Extract from documents.

20. **Strategic fit** — Standalone, bolt-on to existing platform (name which), or new platform.

21. **3-5 key value creation levers** — Extract from IOI's value creation section. Present for confirmation.

22. **Portfolio synergies** — Any specific synergies with existing Tern companies (CADS, CCube, SchoolScreener, MetaBroadcast, Mind of My Own, RMS, Storespace, Sofco, Prosper, etc.)

### Phase 4: Assumptions

Extract from uploaded documents. The assumptions section is heavily deal-specific. Common categories to look for:

23. **ARR** — Current figure and composition (SaaS, support & maintenance, transactional, data services).
24. **Churn** — Gross churn rate, any known losses.
25. **Non-recurring revenue** — PSO, implementation, training. Is it in line with historic levels?
26. **Cost of sales** — Hosting, outsourced dev, payment processing.
27. **Payroll** — Steady-state cost, any restructuring (redundancies, salary adjustments).
28. **Intercompany/group items** — Balances to unwind, shared services, VAT group status.
29. **Pensions** — DB scheme, transfer arrangements.
30. **Security/charges** — Debentures to release.
31. **Regulatory** — FCA, accreditations, NSIA.
32. **IP** — Ownership, third-party claims.
33. **Liabilities** — Onerous, contingent, off-balance sheet.
34. **Debtors/HMRC** — Overdue amounts, TTP arrangements.
35. **Tax losses** — Available to offset.
36. **Customer references** — Any requirements.
37. **EBITDA definition** — UK GAAP, R&D expensed, excludes credits/grants.
38. **Any other deal-specific assumptions** — Present what you've found, ask if anything is missing.

### Phase 5: Transitional services arrangement (conditional)

Ask the user explicitly:

> "Does this deal involve a carve-out or shared services that would require a Transitional Services Agreement (TSA) section in the LOI?"

- If **yes** → include Section 4 (TSA) in the ToC and draft the following:
  - 39. **Carve-out details** — Parent services, transition period, novation of contracts.
  - 40. **Key employee transitions** — Who is staying, leaving, transitioning.
- If **no** → omit Section 4 (TSA) entirely from the ToC and body. Renumber subsequent sections accordingly.

### Phase 6: Boilerplate and closing

41. **Track record section** — Before drafting, ask the following questions one batch at a time:

   **Batch A — Content toggles (ask together):**
   - "Should we include our carve-out references in the Track Record section?"
   - "Should we include a paragraph on experience in the public sector?"
   - "Does this business rely on or work with partners (e.g. Oracle, Microsoft)?" — If yes, include the sentence: "Mark has significant experience and contacts working with partners (Oracle at COA and Microsoft at m-hance)." If no, omit it entirely.

   **Batch B — Named deal examples (ask each individually):**
   - "Include Telsis as a named deal example under Track Record?"
   - "Include MetaBroadcast as a named deal example under Track Record?"
   - "Include CCube as a named deal example under Track Record?"

   Only include the deals and paragraphs the user confirms. Omit any that are declined. Use standard Tern boilerplate from `references/boilerplate.md` for all included content.

42. **Advisors appointed** — Extract from documents or ask. Typical: Hill Dickinson or Freeths (legal), RSM (tax), others as applicable.

43. **Exclusivity period** — Extract or ask. Express as a duration (e.g. "3 months", "6 weeks") from the date of signing.

44. **Target completion date / closing period** — Extract or ask. Express as "within X weeks of signing exclusivity" per template style.

45. **Expense arrangements** — Default: each party bears own costs. Flag if different.

46. **Proof of Funding appendix** — Always ask the user whether to include a Proof of Funding appendix. Do not include it by default.

47. **Value Creation appendix** — Always include as the final appendix (Appendix 1 if no Proof of Funding; Appendix 2 if Proof of Funding is included).

---

## Question Presentation

When asking questions, follow these rules:

1. **Batch questions by phase.** Don't dump all questions at once. Ask Phase 1 first, then Phase 2, etc.
2. **Use selection-based questions** (via `ask_user_input_v0` tool) wherever possible — multiple choice, not open-ended.
3. **Pre-fill with extracted data.** Show what you've found and ask the user to confirm or correct.
4. **For complex deal terms** (earnout structures, assumptions), present what you've extracted in structured text and ask the user to review/edit.
5. **Flag gaps explicitly.** If a document doesn't contain something you need, say so clearly.
6. **Minimise questions.** If you can infer it, don't ask. If it's standard boilerplate, don't ask.

---

## Tone and Style (for the LOI document itself)

Read `references/boilerplate.md` for the standard Tern boilerplate text that goes into every LOI.

The LOI tone is:
- **Formal but not stiff.** Professional, confident, direct.
- **Specific with numbers.** Always use precise figures. Use £X.XM format (1 decimal place in millions). Use "c." prefix when approximate.
- **GBP (£) always** unless the user explicitly uses another currency.
- **Bullet points for assumptions** — each bullet is punchy, 1-2 sentences max. Be specific.
- **"Enterprise value"** not "consideration" for the headline number.
- **Sections follow the template structure exactly** — don't reorder or rename sections.
- **No italics anywhere** in the document body.
- **No bold outside section headers** — body text, bullets, assumptions and boilerplate are all plain weight.

## Number Formatting

- Always GBP: £1.2M, £0.5M, £3.4M
- Use "c." for approximations: c. £0.8M
- Percentages: 100%, 85%, not "one hundred percent"
- EBITDA multiples: 5.0x, 7.2x
- Deferred payment schedules: "three equal instalments of £0.12M at the 1st, 2nd and 3rd anniversary dates"
- **Units — use these abbreviations exactly, no alternatives:**
  - Billions: **B** (not Bn, bn, or bil) — e.g. £1.2B
  - Millions: **M** (not Mn, m, or mn) — e.g. £3.4M
  - Thousands: **K** (not k, Th, or thou) — e.g. £850K

---

## LOI Document Structure

The LOI follows this exact structure. Sections in the table of contents are numbered. Section headings adapt to the deal but the order is fixed:

1. **Deal terms** — Always "Deal terms"
2. **Investment rationale & value creation plan** — Always present
3. **Due diligence & key assumptions** — Always present
4. **Transitional services arrangement** — Only if user confirms a TSA is required (see Phase 5). Omit entirely if not applicable, and renumber subsequent sections.
5. **Track record and why us** — Standard boilerplate with deal-specific additions
6. **Exclusivity and expenses** — Always present
7. **Approval process** — Standard boilerplate

If a section is not applicable (e.g. TSA for a standalone company), omit it from the table of contents and the body entirely.

---

## Output

### Step 1: Write the full LOI content in structured text

Before generating the Word document, write out the complete LOI content in the conversation as structured text so the user can review it. This is critical — it lets the user catch errors before the document is generated.

### Step 2: Generate the .docx file

Once the user approves the content, generate the Word document by writing a new `document.xml` directly into a copy of the user-uploaded TC LOI Template. **Do not use the `docx` npm package** — build the XML manually and inject it into the template zip. Use the path of the `.docx` file uploaded by the user in Phase 0 as the source template. This preserves the template's header (Tern logo image), footer, fonts, styles, page margins, and numbering definitions exactly.

#### Technical approach

```python
import shutil, zipfile, io, os, re
import xml.etree.ElementTree as ET

# 1. Copy the template (path from user-uploaded file in Phase 0)
src = '<path-to-user-uploaded-LOI-template.docx>'  # set from Phase 0 upload
dst = '/home/claude/YYMMDD-CompanyName-LOI.docx'
shutil.copy2(src, dst)

# 2. Read all files from the zip
with open(dst, 'rb') as f:
    buf = io.BytesIO(f.read())
with zipfile.ZipFile(buf, 'r') as zin:
    files = {n: zin.read(n) for n in zin.namelist()}

# 3. Build document.xml (see XML generation rules below)
doc_xml = build_document_xml()

# 4. Patch styles.xml to inject DM Sans (use lambda replacement to avoid backslash issues)
styles = files['word/styles.xml'].decode('utf-8')
# ... patch Heading2 and rPrDefault (see Styles patching below)

# 5. Validate both XMLs before writing
ET.fromstring(doc_xml)
ET.fromstring(styles)

# 6. Write back
files['word/document.xml'] = doc_xml.encode('utf-8')
files['word/styles.xml'] = styles.encode('utf-8')
out_buf = io.BytesIO()
with zipfile.ZipFile(out_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in files.items():
        zout.writestr(name, data)
with open(dst, 'wb') as f:
    f.write(out_buf.getvalue())
```

#### XML generation rules — CRITICAL

**Font:** DM Sans throughout. Body: 24 half-points (12pt). Section headers: 26 half-points (13pt), bold.

**Every `<w:rPr>` must explicitly set font:**
```xml
<w:rFonts w:ascii="DM Sans" w:cs="DM Sans" w:eastAsia="DM Sans" w:hAnsi="DM Sans"/>
```

**Body paragraphs must suppress inherited bold** via rPr inside pPr:
```xml
<w:pPr>
  <w:spacing w:before="80" w:after="80"/>
  <w:rPr>
    <w:rFonts w:ascii="DM Sans" w:cs="DM Sans" w:eastAsia="DM Sans" w:hAnsi="DM Sans"/>
    <w:b w:val="0"/>
  </w:rPr>
</w:pPr>
```

**CRITICAL — the rPr must be INSIDE `<w:pPr>...</w:pPr>`, not after the closing tag.** The most common bug is producing `</w:pPr><w:rPr>` (rPr outside pPr), which creates invalid XML `/><<w:rPr>`. Always build pPr as a single string with rPr nested inside before the closing `</w:pPr>`.

**Section headers (Heading2 style):**
```xml
<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="DM Sans" w:cs="DM Sans" w:eastAsia="DM Sans" w:hAnsi="DM Sans"/>
      <w:b/><w:bCs/>
      <w:color w:val="000000"/>
      <w:sz w:val="26"/><w:szCs w:val="26"/>
    </w:rPr>
    <w:t>1.  Deal terms</w:t>
  </w:r>
</w:p>
```

**Numbered list (Deal Terms clauses):** numId=1, ilvl=0 for top-level (1. 2. 3.), ilvl=1 for sub-clauses (a. b. c.)

**Bullet list (Assumptions, Track Record, Value Creation):** numId=3, ilvl=0 for top-level bullets, ilvl=1 for sub-bullets.

**Page break:**
```xml
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

**Signature blocks use dots, not underscores:**
```
.............................................
Karthik Dasari
Director, for and on behalf of Tern Capital Limited
```

**No italics anywhere.** Never use `<w:i/>` or `<w:iCs/>` in any run.

**No bold in body text.** `<w:b/>` appears only in section header runs and "SUBJECT TO CONTRACT".

**XML escaping:** Always escape `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;` in text content.

**Whitespace preservation:** Add `xml:space="preserve"` to `<w:t>` when text starts or ends with a space.

#### Styles patching

Patch `styles.xml` to override Heading2 and document defaults with DM Sans. **Always use a lambda for regex replacement** (not an rf-string with `\1`/`\2` backreferences) to avoid backslash-doubling bugs:

```python
# Patch Heading2
old_h2 = re.search(r'(<w:style[^>]*w:styleId="Heading2"[^>]*>.*?</w:style>)', styles, re.DOTALL)
if old_h2:
    new_rpr = ('<w:rPr>'
               '<w:rFonts w:ascii="DM Sans" w:cs="DM Sans" w:eastAsia="DM Sans" w:hAnsi="DM Sans"/>'
               '<w:b/><w:bCs/><w:color w:val="000000"/>'
               '<w:sz w:val="26"/><w:szCs w:val="26"/>'
               '</w:rPr>')
    patched = re.sub(r'<w:rPr>.*?</w:rPr>', new_rpr, old_h2.group(1), count=1, flags=re.DOTALL)
    styles = styles.replace(old_h2.group(1), patched)

# Patch document defaults — use lambda, never rf-string with \1\2
new_inner = ('<w:rFonts w:ascii="DM Sans" w:cs="DM Sans" w:eastAsia="DM Sans" w:hAnsi="DM Sans"/>'
             '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-GB"/>')
styles = re.sub(
    r'(<w:rPrDefault><w:rPr>)(.*?)(</w:rPr></w:rPrDefault>)',
    lambda m: m.group(1) + new_inner + m.group(3),
    styles, flags=re.DOTALL
)
```

#### sectPr (preserve exactly from template)

```xml
<w:sectPr>
  <w:headerReference r:id="rId13" w:type="default"/>
  <w:headerReference r:id="rId14" w:type="first"/>
  <w:footerReference r:id="rId15" w:type="default"/>
  <w:footerReference r:id="rId16" w:type="first"/>
  <w:pgSz w:h="16840" w:w="11900" w:orient="portrait"/>
  <w:pgMar w:bottom="850" w:top="850" w:left="1134" w:right="560" w:header="709" w:footer="709"/>
  <w:pgNumType w:start="1"/>
  <w:titlePg w:val="1"/>
</w:sectPr>
```

#### Validation — mandatory before writing

Always call `ET.fromstring()` on both `document.xml` and `styles.xml` before writing the zip. If either fails, debug and fix before proceeding. Never deliver a file that hasn't passed XML validation.

#### Output filename

Save to `/mnt/user-data/outputs/` with filename format: `YYMMDD-[Company_Name]-LOI.docx`

---

## Formatting rules (document body)

### Section headers
- Style: Heading2
- Font: DM Sans, 13pt (26 half-points), bold, black
- No dividers, no orange, no colour

### Body text
- Font: DM Sans, 12pt (24 half-points), plain weight (no bold), black
- No italics anywhere in the document

### Table of Contents
- Plain numbered list (1. through 6. or 7.)
- No page numbers
- No hyperlinks
- Same font/size as body text

### Deal Terms clauses
- Numbered list using numId=1
- Top-level clauses: 1. 2. 3. 4. 5. 6. (ilvl=0)
- Sub-clauses indented: a. b. c. d. e. (ilvl=1)
- No sub-headings within Deal Terms — it is one continuous numbered list
- No payment schedule table

### Assumptions (Section 3)
- Single flat bullet list — no category headings, no sub-groupings
- All bullets at ilvl=0

### Track Record (Section 5)
- Bullet list with sub-bullets (ilvl=0 for main points, ilvl=1 for elaboration)
- No A/B/C/D lettering — pure bullet hierarchy

### Signature blocks
- Use dots: `.............................................`
- Not underscores

---

## Page margins and layout (from TC LOI Template)

- Page size: 11900 × 16840 DXA (A4)
- Margins: top 850, bottom 850, left 1134, right 560, header 709, footer 709
- Header: Tern logo (image2.jpg) + address text box (image6.png) — preserved from template, never regenerated

---

## Appendices

**Always ask** whether to include Proof of Funding before drafting. Do not include it by default.

Always include the Value Creation playbook as the last appendix, on a new page. Number it as Appendix 1 (if no Proof of Funding) or Appendix 2 (if Proof of Funding is included).

---

## Reference Files

- `references/boilerplate.md` — Standard Tern boilerplate text for Track Record, Exclusivity, and Approval Process sections
- `references/assumptions-library.md` — Common assumption patterns extracted from past LOIs, organised by category
- `references/deal-terms-patterns.md` — Common deal structure patterns (upfront only, upfront + guaranteed deferred, upfront + deferred + earnout)

---

## Companies House Lookup

When looking up a company on Companies House:
1. Search for the company name via web search: `"[company name]" site:find-and-update.company-information.service.gov.uk`
2. Fetch the company page to get: registered address, directors (current), company number, incorporation date
3. Present findings to user for confirmation

This is essential for populating recipient names and the target company address.
