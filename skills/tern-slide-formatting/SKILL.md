---
name: tern-slide-formatting
description: "Formatting rules for Tern Capital PowerPoint slide decks. Use this skill whenever creating, editing, or reviewing a Tern Capital presentation (.pptx). Triggers include: any mention of 'Tern deck', 'Tern slides', 'Tern presentation', 'investment deck', 'HoldCo deck', 'portfolio presentation', or when the user asks to create slides that follow the Tern Capital brand. Also trigger when reviewing or formatting any slide content for Tern Capital, including deal decks, investor presentations, portfolio reviews, case studies, or appendix slides. If the user references the Tern brand guidelines or asks for slides 'in the Tern format', use this skill."
---

# Tern Capital — Slide Deck Formatting Rules

These rules define the exact visual formatting for all Tern Capital PowerPoint (.pptx) slide decks. Every slide produced for Tern Capital must follow these rules precisely.

Read the pptx SKILL.md (`/mnt/skills/public/pptx/SKILL.md`) before creating any slides — it covers the tooling and QA process. This skill only defines the formatting rules.

> **Near-black colour note:** The master brand guidelines define Near Black as `#1a1a18` (26, 26, 24). This slide-formatting skill uses `#000000` (pure black) as the implementation value in OOXML and pptxgenjs code — this is a known discrepancy. Until resolved, use `#1a1a18` for brand outputs (letterheads, HTML, documents) and `#000000` for slide XML/code. Visually indistinguishable at presentation scale.

---

## 1. Slide canvas

| Property | Value |
|----------|-------|
| Slide size | 10 x 5.625 inches (960 x 540 px equivalent, standard 16:9) |
| EMU dimensions | cx = 9,144,000 / cy = 5,143,500 |
| Background | White (#FFFFFF) for all content slides; Tern Orange (#EB5C32) for title/cover slide |

> **Verified against source file**: confirmed from an actual Tern Capital investment deck (CDS deck, Jun 2026). Do not use 13.333 x 7.5in — that was an earlier incorrect assumption in this skill.

---

## 2. Font

DM Sans is the only font. It replaces Ubuntu across the entire deck.

| Element | Font | Weight | Size (pt) | Colour | Notes |
|---------|------|--------|-----------|--------|-------|
| Cover title | DM Sans | Bold (700) | 32 | White (#FFFFFF) | Centre-aligned on orange background |
| Cover subtitle | DM Sans | Regular (400) | 11 | White (#FFFFFF) | Below title |
| Cover confidentiality | DM Sans | Regular (400) | 8 | Tern Orange (#EB5C32) on white pill | Bottom of cover |
| Slide title (H1) | DM Sans | Regular (400) | 18 | Near-black (#000000) | Top-left, sentence case. NOT bold. |
| Slide subtitle | DM Sans | Regular (400) | 12 | Near-black (#000000) | Directly below H1, flush with no gap |
| Section divider title | DM Sans | Bold (700) | 24-32 | Near-black (#000000) | Centre-left, with orange illustration |
| Orange box header text | DM Sans | Regular (400) | 11 | White (#FFFFFF) | Inside EB5C32-filled rectangle |
| Body text | DM Sans | Regular (400) | 11 | Near-black (#000000) | Left-aligned; primary content size |
| Body text (tight) | DM Sans | Regular (400) | 9 | Near-black (#000000) | When space is constrained |
| Small / caption | DM Sans | Regular (400) | 9-10 | Dark grey (#999999) | Labels, descriptions |
| KPI / stat number | DM Sans | Regular (400) | 21 | Tern Orange (#EB5C32) | Large callout figures |
| KPI label | DM Sans | Regular (400) | 11 | Near-black (#000000) | Below KPI number |
| Table header | DM Sans | Regular (400) | 11 | White (#FFFFFF) | On orange (#EB5C32) background |
| Table body | DM Sans | Regular (400) | 11 | Near-black (#000000) | Left-aligned text; right-aligned numbers |
| Footnotes | DM Sans | Regular (400) | 6 | Near-black (#000000) | Bottom of slide |
| Slide number | DM Sans | Regular (400) | Auto | Near-black (#000000) | Bottom-right corner |
| "PRELIMINARY" label | DM Sans | Bold (700) | 11 | Tern Orange (#EB5C32) | Top-right, only on uncertain-data slides |
| Section chapter number | DM Sans | Regular (400) | 10 | Near-black (#000000) | Inside numbered circle markers |

Bold usage is minimal. Bold (700) is reserved for: cover title, section divider titles, occasional emphasis of a single word in body text, and the PRELIMINARY label. Slide titles and subtitles are Regular, not bold. Body text is never fully bold.

---

## 3. Colour palette

### Primary colours

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Tern Orange | #EB5C32 | 235, 92, 50 | Logo "Tern", orange header bars, table headers, KPI numbers, numbered step markers, section labels, CTAs. The dominant accent colour. |
| Near-black | #000000 | 0, 0, 0 | Slide titles, body text, table text. (Brand guidelines define this as #1a1a18 — see note at top of skill.) |
| White | #FFFFFF | 255, 255, 255 | Slide backgrounds, text on dark/orange fills, table body rows. |

### Greys

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Dark grey | #999999 | 153, 153, 153 | Subtitles, captions, secondary text. Also the colour for table row border lines. |
| Border grey | #CCCCCC | 204, 204, 204 | Legacy dividers; data table borders in comps tables. |
| Light grey | #D9D9D9 | 217, 217, 217 | Category label boxes only. |
| Divider grey | #D0D0D0 | 208, 208, 208 | Horizontal and vertical slide divider lines. |
| Off-white | #EFEFEF | 239, 239, 239 | Subtle background areas. Not used for table rows. |

### Colour rules

- Orange is for accents only — never for large background areas on content slides (title/cover is the exception). Never use orange for body text.
- White text only appears on orange or dark fills. Never place white text on a white or light background.
- Grey label boxes (#D9D9D9 fill) are used for small category labels only.
- No other colours are used in the deck except for embedded chart images or external logos.

---

## 4. Slide types

### 4a. Title / cover slide

- Background: Solid Tern Orange (#EB5C32) fill.
- TernCapital logo: Top-right area.
- Title text: Large (32pt), bold, white, vertically centred or slightly above centre.
- Subtitle: 11pt, white, below title.
- Confidentiality label: Bottom-centre area.
- No slide number on the cover.

### 4b. Section divider slide

- Background: White.
- Illustration: An AI-generated nature sketch in Tern Orange ink occupying the right ~60% of the slide.
- Title: Large (24-32pt), bold, near-black, positioned left-centre or bottom-left. Sentence case.
- Slide number: Bottom-right.
- No subtitle, no footnotes, no tables.

### 4c. Content slide (standard)

Anatomy from top to bottom:

```
  Slide title (18pt regular, near-black)
  Slide subtitle (12pt regular, near-black) - flush below title, no gap
  +------------------------------------------+  +--------+
  | Orange header bar (EB5C32, white text)   |  | KPI    |
  +------------------------------------------+  | callout|
  | Body content area                        |  | boxes  |
  | (bullets, text, native tables)           |  |        |
  +------------------------------------------+  |        |
  | Orange header bar 2                      |  |        |
  +------------------------------------------+  |        |
  | More body content                        |  +--------+
  +------------------------------------------+
  | Footnotes (6pt)                       [#]|
  +------------------------------------------+
```

No logo on content slides — the Tern wordmark/logo appears only on the title/cover slide and section divider slides (verified: an actual Tern content slide carries no logo at all).

Positioning details — canvas is 10 x 5.625in (9,144,000 x 5,143,500 EMU):

| Element | Position (EMU) | Position (inches) | Notes |
|---------|---------------|--------------------|-------|
| Slide title | x = 154,406 / y = 112,425 | x = 0.169" / y = 0.123" | Box 9.55" x 0.303" (8,736,600 x 277,200 EMU). 18pt regular. |
| Slide subtitle | x = 154,406 / y = 383,888 | x = 0.169" / y = 0.420" | Box 9.55" x 0.202" (8,736,600 x 184,800 EMU). 12pt regular. Sits flush under title, no visible gap. |
| Orange header bars | x approx 141,000 / y varies | x approx 0.154" | Width spans content area, height ~0.175" |
| Body content | x approx 141,000 | x approx 0.154" | Below header bars, left-aligned |
| KPI callout column | x approx 7,150,000 | Right side | Scale proportionally from the old 13.333in spec (ratio 10/13.333) if adapting existing layouts |
| Footnotes | x approx 141,000 / y approx 4,900,000 | Near bottom | 6pt |
| Slide number | x = 8,964,518 / y = 4,979,245 | x = 9.804" / y = 5.445" | Box 0.168" x 0.147" (153,900 x 134,700 EMU). Centre-aligned text. Bottom-right corner, ~0.2" from each edge. Identical position on every slide (except cover). |

> **Note on legacy KPI/orange-bar coordinates above**: these were originally specified for a 13.333 x 7.5in canvas and have not yet been re-verified against a real 10 x 5.625in file. Treat as approximate until confirmed against another source slide; title, subtitle, and slide number are confirmed exact.

### 4d. Table slide

Same header/footer structure as content slides but the body is dominated by a data table. **Build the table as a native PowerPoint table object** (`addTable` in pptxgenjs, or `<a:tbl>` in OOXML) — never simulate a table by positioning individual text boxes in a grid. See section 6 for table formatting rules.

### 4e. Disclaimer slide

- Full-page small text (8-9pt) with the legal disclaimer.
- Slide number bottom-right.
- No orange bars or KPI boxes.
- No logo (logo is cover/divider only — see 4c).

---

## 5. Recurring visual elements

### 5a. Orange header bars

- Fill: Tern Orange (#EB5C32).
- Height: ~253,500 EMU (~0.28 inches).
- Width: Spans the content area (~9,872,000 EMU).
- Text: White (#FFFFFF), 11pt DM Sans Regular. Left-aligned with ~0.1" internal padding.
- Corners: Always square — never rounded.

### 5b. KPI callout boxes

- Fill: Tern Orange (#EB5C32).
- Structure: Large number (21pt, Tern Orange) on top, descriptive label (11pt, near-black) below.
- Position: Right column, stacked vertically.
- Separated from main content by a thin vertical orange line (#ED5C32, ~1px / 9,525 EMU width).

### 5c. Grey category label boxes

- Fill: Light grey (#D9D9D9).
- Text: 11pt DM Sans, near-black.
- Corners: Square.

### 5d. Numbered step circles

- Shape: Circle, **0.5cm x 0.5cm** (180,000 x 180,000 EMU, ~0.197 inches diameter).
- Fill: White (#FFFFFF).
- Border: Grey (#B2B2B2) outline.
- Text: Single digit, 10pt DM Sans, near-black (#000000), centre-aligned.
- This size applies everywhere the circle appears, including when reused inside slide headers on subsequent slides — do not let header-embedded copies drift to a different size than the body copy.

### 5e. Orange numbered step circles (alternative)

- Some slides use orange (#EB5C32) filled circles with white text.
- Same size as above: 0.5cm x 0.5cm (180,000 x 180,000 EMU).

### 5f. Footnote block

- Position: Bottom of the slide, above the slide number.
- Format: "Notes: 1) [text]. 2) [text]." — space after closing parenthesis, full stop after each note.
- Font: 6pt DM Sans Regular, near-black.

### 5g. Slide number

- Position: x = 8,964,518 / y = 4,979,245 EMU (x = 9.804" / y = 5.445"), box 153,900 x 134,700 EMU (0.168" x 0.147"), centre-aligned text. Verified from source file.
- Identical position on every content, table, and disclaimer slide.
- Not shown on title/cover slides.

### 5h. TernCapital logo

- On light slides: "Tern" in orange (#EB5C32) semi-bold, "Capital" in near-black, with grey chevrons.
- On the title/cover slide: "Tern" in orange, "Capital" in white, grey chevrons.
- **Scope: title/cover slide and section divider slides only.** Content, table, and disclaimer slides do NOT carry the logo — confirmed from a real Tern content slide, which has no logo anywhere on it. This overrides any earlier instruction to place the logo on every slide.

---

## 6. Table formatting

### Structure

| Rule | Detail |
|------|--------|
| Construction | Always a native PowerPoint table object (`addTable` in pptxgenjs, `<a:tbl>` in OOXML). Never simulate a table with a grid of individually positioned text boxes. |
| Header row fill | Tern Orange (#EB5C32) — always, on every table without exception |
| Header text | White (#FFFFFF), 11pt DM Sans Regular, left-aligned |
| Header borders | NO borders on the header row — all four sides set to w="0" with noFill |
| Body row fill | White (#FFFFFF) only — no shading, no alternating fills |
| Body text | 11pt DM Sans, near-black (#000000) |
| Cell alignment | All text left-aligned horizontally; all cells vertically centred (anchor="ctr") |
| Row borders | Dark grey (#999999) horizontal lines between data rows only. Use lnT on each data row (not on header row). Add lnB on the last row only to close the table. |
| Column borders | None — lnL and lnR always set to w="0" with noFill on every cell |
| Corners | Always square — never rounded |
| Column headers | As short as possible to avoid word-wrap |
| tblPr | Set bandRow="0" firstRow="1" to prevent PowerPoint re-applying stripe fills |

### Date format in tables

Dates in table cells use DD-MMM (DDD) format — day number, three-letter month, day-of-week abbreviation in parentheses.

| Rule | Example |
|------|---------|
| Date only | 01-May (Thu) |
| Date with time | 01-May (Thu) / 4-5pm GMT |
| Two-hour sessions | 29-May (Thu) / 4-6pm GMT (2 hrs) |
| Never use | DD/MM/YY, DD-MMMM-YY, or MM/DD |

### Number formatting in tables

| Rule | Example |
|------|---------|
| Add commas to large numbers | 1,832 not 1832 |
| Remove decimals where obvious | Show 25% not 25.00% |
| Remove currency symbols where obvious | If column header says £M, cells show 2.3 not £2.3M |
| Suffixes always capitalised | £10K, £5M, £2B — never £10k |
| No space between number and suffix | £10K not £10 K |
| Ranges use hyphen, no spaces | £5-10M, 20-30% |
| "na" for not applicable | Lowercase, no slash — never "N/A" |
| Negative numbers | Dash, no space: -£3M. Or parentheses: (3.0) |
| Actuals / Forecasts suffix | FY24A, FY25F |
| Sources | Split by semicolons: "Source: Tern Forecasts; Companies House." |

---

## 7. Content slide composition rules

### Margins and spacing

| Property | Value |
|----------|-------|
| Left margin | ~141,000-154,000 EMU (~0.15-0.17 inches) from slide edge |
| Top margin (title) | Title starts at y = 112,425 EMU (0.123") — see section 4c for verified title/subtitle coordinates |
| Bottom margin (above footnotes) | Not yet re-verified on the 10 x 5.625in canvas — footnote sits above the slide number (y = 4,979,245 EMU / 5.445"), leave enough clearance so it doesn't collide |
| Gap between orange header bar and body content | Proportionally similar to before, not yet re-verified on new canvas |
| Gap between stacked KPI boxes | Not yet re-verified on new canvas |

### Bullet paragraph spacing

| Property | Value |
|----------|-------|
| Line spacing | Always Single (100%) — never Multiple or Exact |
| Space before | 1pt on every bullet paragraph |
| Space after | 1pt on every bullet paragraph |
| Hanging indent | marL 0.197" (180,000 EMU) with indent -0.166" (-152,400 EMU) — this is what creates the gap between the bullet glyph and the text; do not use manual spaces to fake it |
| Bullet glyph, top level | Solid round bullet (●), DM Sans, sized to match the body text |
| Bullet glyph, sub-level | Hyphen (-), not a round bullet |

### Slide layout

Every slide except the title/cover slide and section dividers uses the Google Slides / PowerPoint layout **"Slide Title & Content 4"**. Remove any other unused layouts from the deck so the template doesn't drift.

### Text rules

| Rule | Detail |
|------|--------|
| Sentence case throughout | Not Title Case — "Investment strategy" not "Investment Strategy" |
| No bold in body text | Bold is for titles/headers only. Exception: occasional single-word emphasis. |
| Bullets end with a full stop | Every bullet point ends with "." |
| No hanging lines | Avoid lines with only one or two words. Rewrite to resolve. |
| "We" not "I" | Always "we" or "our" — never "I" or "my" |
| Active voice | "We will consult" not "a consultation will be undertaken" |
| Contractions | Spell out where space permits — "do not" not "don't" |
| Nations | Use periods: U.K., U.S. |
| Numbers in text | Spell out one to ten; numerals for 11+. Exceptions: units, tables, percentages. |
| EBITA not EBITDA | Always EBITA — never EBITDA |
| K/M consistency | Use the same unit throughout — 185K and 37K, not 185K and 37,000 |
| Thousands separator | Numbers of 1,000+ take a comma, even before a K/M/B suffix — 1,424K not 1424K |

### Footnote rules

| Rule | Detail |
|------|--------|
| Format | "Notes: 1) [text]. 2) [text]." — space after closing parenthesis |
| Font | 6pt DM Sans Regular |
| Every footnote referenced in body must appear below | None missed |
| Ordering | Left to right, top to bottom on the slide |
| Full stop at end of each footnote | Required |
| "PRELIMINARY" label | Only on slides where data is not clearcut |

---

## 8. Boxes and shapes

| Rule | Detail |
|------|--------|
| Box corners | Always square — never rounded |
| Orange box titles | White text only |
| Vertical divider lines | Tern Orange (#ED5C32), ~1px width (9,525 EMU), full height of content area |
| Horizontal dividers | Light grey (#CCCCCC or #D0D0D0), ~1px |

---

## 9. Section divider slides

1. Background: White.
2. Illustration: AI-generated orange ink sketch (nature themes). Occupies the right portion of the slide. No text in the illustration.
3. Title: Bold, 24-32pt, near-black, positioned left or centre-left.
4. Chapter number indicator: Some section dividers include a small orange section number.
5. Slide number: Bottom-right.

---

## 10. Colour usage by element — quick reference

| Element | Fill colour | Text colour |
|---------|------------|-------------|
| Slide background | White #FFFFFF | — |
| Title/cover background | Tern Orange #EB5C32 | White #FFFFFF |
| Slide title text | — | Near-black #000000 |
| Orange header bar | #EB5C32 | White #FFFFFF |
| KPI number | — | Tern Orange #EB5C32 |
| KPI label | — | Near-black #000000 |
| Body text | — | Near-black #000000 |
| Secondary/caption text | — | Dark grey #999999 |
| Footnotes | — | Near-black #000000 |
| Table header row | #EB5C32 | White #FFFFFF |
| Table body rows | White #FFFFFF | Near-black #000000 |
| Table row border lines | — (stroke #999999) | — |
| Grey label box | #D9D9D9 | Near-black #000000 |
| Step circle (white variant) | White #FFFFFF, border #B2B2B2 | Near-black #000000 |
| Step circle (orange variant) | #EB5C32 | White #FFFFFF |
| Vertical divider line | — (stroke #ED5C32) | — |

---

## 11. Do's and don'ts

### Do

- Use DM Sans everywhere — no other fonts.
- Use square corners on all boxes and tables.
- Write £10K, £5M, £2B — always capitalised, no space.
- Write EBITA — not EBITDA.
- Start footnotes with "Notes: 1) " — space after parenthesis; full stop after each footnote.
- Split sources with semicolons: "Source: Tern Forecasts; Companies House."
- End all bullets with a full stop.
- Use "na" for not applicable.
- Keep orange as an accent colour only.
- Place the TernCapital logo top-right on the title/cover slide and section dividers ONLY — never on content, table, or disclaimer slides.
- Use the vertical orange divider line to separate the KPI column from main content.
- Build tables as native table objects — never a grid of text boxes.
- Table headers: always orange (#EB5C32) background, white text, no borders on any side.
- Table body rows: always white, no shading, no alternating fills.
- Table row borders: dark grey (#999999) horizontal lines between data rows only — no vertical borders.
- Table dates: DD-MMM (DDD) format, e.g. 01-May (Thu) / 4-5pm GMT.
- Set bandRow="0" on tblPr to prevent PowerPoint re-applying stripe fills.
- Use layout "Slide Title & Content 4" for every slide except the title/cover slide and section dividers. Delete any other unused layouts from the deck.
- Numbered step circles are always 0.5cm x 0.5cm — including copies reused in slide headers.
- Numbers of 1,000+ take a comma thousands separator, even before a K/M/B suffix: 1,424K not 1424K.
- Top-level bullets use a solid round bullet (●); sub-bullets use a hyphen (-).

### Don't

- Never add a space between "Tern" and "Capital" in the logo or split the wordmark across two lines.
- Never place the logo on a content, table, or disclaimer slide.
- Never simulate a table using individually positioned text boxes.
- Never use rounded corners on any box or table.
- Never use orange for body text or large background areas (except the title/cover slide).
- Never write EBITDA — always EBITA.
- Never write £10k, £5m, £2b — lowercase suffixes are wrong.
- Never mix K and full numbers in the same context (e.g. 185K and 37,000).
- Never write a thousands-plus number without a comma (e.g. 1424K) — always 1,424K.
- Never split sources with commas.
- Never use "N/A" or "Not Applicable" — write "na".
- Never leave a hanging line with only one or two words — reword the bullet so it doesn't orphan.
- Never use bold for the slide title or subtitle — both are Regular weight.
- Never use bold for body text (bold is for headers/titles only).
- Never use colours outside the defined palette.
- Never use alternating row shading in tables — all body rows are white.
- Never add vertical (column) borders to tables.
- Never add borders to the header row.
- Never use #CCCCCC grey or any other colour as a table header fill — the header is always orange.
- Never use DD/MM/YY date format in tables.

---

## 12. OOXML table construction pattern

When building tables via edit_slide_xml, follow this exact pattern.

COLOURS:
  ORANGE   = "EB5C32"   (table header fill, orange bars)
  WHITE    = "FFFFFF"   (all body row fills, header text)
  NEAR_BLK = "000000"   (all body text)
  DK_GREY  = "999999"   (row border colour only)

tblPr: bandRow="0" firstRow="1"
  This disables PowerPoint automatic stripe fills.

Header row cells — orange fill, white text, NO borders:
  tcPr children:
    lnL  w="0"     noFill
    lnR  w="0"     noFill
    lnT  w="0"     noFill
    lnB  w="0"     noFill
    solidFill  srgbClr val="EB5C32"

Data row cells — white fill, dark grey top border, no side borders:
  tcPr children:
    lnL  w="0"      noFill
    lnR  w="0"      noFill
    lnT  w="9525"   solidFill srgbClr val="999999"
    lnB  w="0"      noFill   (last row: w="9525" solidFill val="999999")
    solidFill  srgbClr val="FFFFFF"

Cell text body — left-aligned, vertically centred:
  bodyPr anchor="ctr" lIns="91440" rIns="91440" tIns="45720" bIns="45720"
  pPr algn="l"
  rPr lang="en-GB" sz="1100"
    solidFill srgbClr val="000000"  (or FFFFFF for header row)
    latin typeface="DM Sans"

---

## 13. Applying these rules in code (pptxgenjs)

When creating slides programmatically with pptxgenjs, use these mappings. Canvas is confirmed 10 x 5.625in — use `pres.layout = 'LAYOUT_16x9'` (pptxgenjs's default 10x5.625in layout), NOT `LAYOUT_WIDE`.

  TERN_ORANGE  = 'EB5C32'
  NEAR_BLACK   = '000000'
  WHITE        = 'FFFFFF'
  DARK_GREY    = '999999'    table row borders
  BORDER_GREY  = 'CCCCCC'    legacy/divider use only
  LIGHT_GREY   = 'D9D9D9'    category label boxes
  OFF_WHITE    = 'EFEFEF'    subtle backgrounds (not tables)
  DIVIDER_GREY = 'D0D0D0'    horizontal/vertical slide dividers

  FONT = 'DM Sans'

  Standard slide title (verified from source file):
    x: 0.169, y: 0.123, w: 9.55, h: 0.303, fontSize: 18, bold: false,
    fontFace: FONT, color: NEAR_BLACK

  Standard slide subtitle (verified from source file):
    x: 0.169, y: 0.420, w: 9.55, h: 0.202, fontSize: 12, bold: false,
    fontFace: FONT, color: NEAR_BLACK
    // sits flush directly under the title box, no gap

  Bullet paragraphs (all levels):
    lineSpacing set to single/100%; paraSpaceBefore: 1, paraSpaceAfter: 1
    top-level bullet: bullet: { code: '25CF' } (solid round) — never a unicode character typed into the string
    sub-level bullet: bullet: { code: '2013' } or a literal "-" per indentLevel, not a round bullet

  Orange header bar:
    x: 0.17, y: varies, w: 8.10, h: 0.21, fill: TERN_ORANGE,
    fontSize: 11, fontFace: FONT, color: WHITE, valign: 'middle'
    // not yet re-verified against a real 10x5.625in file — treat as approximate

  Body text:
    fontSize: 11, fontFace: FONT, color: NEAR_BLACK

  Footnotes:
    fontSize: 6, fontFace: FONT, color: NEAR_BLACK
    // position above the slide number (y ≈ 5.445); not yet precisely re-verified, leave clearance

  Slide number (verified from source file):
    x: 9.804, y: 5.445, w: 0.168, h: 0.147, align: 'center',
    fontFace: FONT, color: NEAR_BLACK
    // identical position on every non-cover slide

  KPI box:
    x: 8.51, y: varies, w: 1.41, h: 0.83,
    fontSize: 21 (number) / 11 (label), fontFace: FONT,
    color: TERN_ORANGE (number) / NEAR_BLACK (label)
    // not yet re-verified against a real 10x5.625in file — treat as approximate

  Logo: do NOT add to content/table/disclaimer slides. Only add on the title/cover slide and section dividers.

---

## 14. TernCapital wordmark rules

- "Tern" — DM Sans Semi-bold (600), Tern Orange (#EB5C32).
- "Capital" — DM Sans Light (300), Near-black (#000000) on light backgrounds or White (#FFFFFF) on dark/orange backgrounds.
- No space between "Tern" and "Capital" — the wordmark is a single unbroken unit.
- The grey chevron icon sits immediately to the upper-right of "Capital".
- When the wordmark cannot be rendered as styled text, use the brand logo image files instead.
- Appears ONLY on the title/cover slide and section divider slides — never on content, table, or disclaimer slides.
