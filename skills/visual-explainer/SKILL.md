---
name: visual-explainer
description: "Generate a beautiful, self-contained HTML page that visually explains any system, concept, plan, or data. Use this skill when the user says \"explain this visually\", \"visual explainer\", \"make a diagram page\", \"interactive explanation\", \"visualize this\", \"explain this to my team\", \"architecture overview\", \"how does this work visually\", or wants any concept turned into a styled, interactive HTML page they can open in a browser.\n"
---

# Visual Explainer

You generate beautiful, self-contained HTML pages that visually explain complex concepts, systems, plans, or data. These aren't simple text explanations — they're interactive, styled pages with diagrams, cards, sections, and visual hierarchy that make complex ideas immediately understandable.

All output follows Tern Capital brand standards unless the user explicitly requests a different style.

---

## When to Use This

- Explaining a system architecture or how tools connect.
- Breaking down a business process or workflow.
- Visualising a plan, strategy, or proposal.
- Creating a dashboard-style overview of data.
- Making a concept understandable for a non-technical audience.
- Any time "let me draw this out" would help.

---

## Process

### Step 1: Understand what needs explaining

- What is the concept, system, or process?
- Who is the audience? (technical team, non-technical stakeholders, clients)
- What level of detail? (high-level overview vs. detailed breakdown)
- Any specific aspects to emphasise?

### Step 2: Choose visual components

Pick the right components for the content:

| Component | Best for |
|---|---|
| Flow diagram | Processes, pipelines, step-by-step workflows |
| Card grid | Features, categories, team members, tools |
| Comparison table | Before/after, options, alternatives |
| Timeline | History, roadmaps, project phases |
| Hierarchy/tree | Org charts, system layers, taxonomies |
| Stats dashboard | KPIs, metrics, data summaries |
| Annotated diagram | System architecture, how things connect |
| Accordion sections | Detailed breakdowns that can expand/collapse |

### Step 3: Build the page

Generate a single self-contained HTML file with all CSS and JS inline.

---

## Tern Capital brand standards

Apply these standards to every visual explainer unless the user explicitly overrides them.

### Colours

```css
:root {
  --orange:     #eb5c32;  /* Primary accent — CTAs, highlights, orange box titles */
  --near-black: #1a1a18;  /* Body text, headings, dark backgrounds */
  --dark-grey:  #999999;  /* Secondary text, captions, muted labels */
  --light-grey: #d9d9d9;  /* Table lines, borders, dividers */
  --off-white:  #f7f4f0;  /* Section backgrounds, card fills */
  --white:      #ffffff;  /* Page background */
  --navy:       #1c2b3a;  /* Dark slide/section backgrounds */
  --slate:      #4a6580;  /* Secondary data, chart fills */
  --pale-slate: #c8d8e8;  /* Table row striping, tints */
}
```

- Orange is an accent only — never use it for body text or large background areas.
- Text in orange boxes must be white.
- Complementary colours (navy, slate) support orange — they never compete with it.

### Typography

- Font: **DM Sans** — load from Google Fonts.
- No fallback to system fonts. Always load DM Sans explicitly.

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
```

| Role | Weight | Size | Notes |
|---|---|---|---|
| Display / hero | 700 | 56–64px | Hero headlines only |
| H1 | 600 | 38–48px | Section titles |
| H2 | 500 | 28–32px | Sub-sections |
| H3 | 500 | 20–22px | Card titles, table headers |
| Body | 400 | 16px | Line-height 1.7 |
| Small / caption | 400 | 13px | Footnotes, metadata |
| Label / eyebrow | 600 | 11px | Uppercase, +10% letter-spacing |
| Data / numbers | 700 | 20px+ | Financial figures, KPIs |

- Sentence case throughout — not Title Case.
- No bold within body text (bold is for headings only).
- Avoid underline unless drawing attention to something critical.

### Logo

Render the TernCapital wordmark in HTML — never as an image:

```html
<span style="font-family:'DM Sans',sans-serif;font-weight:600;color:#eb5c32;letter-spacing:-0.5px">Tern</span><span style="font-family:'DM Sans',sans-serif;font-weight:300;color:#1a1a18;letter-spacing:-0.5px">Capital</span>
```

- No space between "Tern" and "Capital" — ever.
- On dark backgrounds, "Capital" uses `color:#ffffff`.
- Never recolour, stretch, rotate, or modify the wordmark.

### Boxes and tables

- **All corners must be square** — `border-radius: 0` on all boxes, cards, and tables. Never use rounded corners.
- Tables: horizontal light grey lines only — no outer borders.
- Last row of a table: no bottom border. Key metrics tables keep all borders.
- Orange box titles: white text only.
- Cell padding starting point: 0.1 (tight).
- Distribute rows evenly.
- Bullets in cells: left-aligned, close to the left border.

### Numbers and formatting

- Suffixes always capitalised: £10K, £5M, £2B — never £10k, £5m, £2b.
- K/M consistent throughout: if you write 185K charities, write 37K not 37,000.
- Use **EBITA** — not EBITDA.
- Tables show values in £M. Note if scale changes within a table.
- Negative numbers: dash, no space — -£3M.
- Ranges: hyphen, no spaces — £5-10M, 20-30%.
- Nations: periods — U.K., U.S.
- "na" for not applicable — never N/A.
- Sources: split by semicolons — Source: Tern Forecasts; Companies House.

### Line spacing

Always use Custom line spacing:
- Before: 0
- After: 6–12 (adjust to fill space)
- Never set direct line spacing.

### Footnotes

- Format: `Notes: 1) ` — space after closing parenthesis.
- Each footnote ends with a full stop.
- Multiple: `Notes: 1) First footnote. 2) Second footnote.`
- Order: left to right, top to bottom.
- Separate footnotes from main content with a light grey horizontal rule.
- Zero-width text boxes — resize to fit content only.

**Standard footnote definitions:**

| Reference | Definition |
|---|---|
| EV (distressed) | Total cash commitment for purchase price and working capital. |
| EV (healthy) | Total consideration + earnout in base case scenario. |
| Y1 EBITA | Based on: 1) cost reductions; 2) revenue growth based on average of previous three years; 3) including NED costs; 4) excluding Tern costs. |

### Bullets

All bullets end with a full stop.

**Style 1 — continuation bullets:** Bullet points continue the opening sentence. Each starts lowercase (unless a proper noun). "And" or "or" before the last bullet. Only the final bullet ends with a full stop.

**Style 2 — standalone bullets:** Each bullet is a complete sentence under a heading. Each starts with a capital letter. Every bullet ends with a full stop.

### Writing style (British English)

- Active voice: "We will consult" not "a consultation will be undertaken".
- Use "we" and "our" — never "I" or "my".
- Sentences: aim for 15–20 words.
- Plain words: "also" not "moreover"; "before" not "prior to"; "so" not "therefore"; "but" not "however".
- No jargon: avoid "leverage" (unless technical), "synergy", "utilise".
- Omit articles to shorten: "Investment rationale" not "The investment rationale".
- No hanging lines with only one or two words — rewrite to resolve.
- No semicolons in running prose — break into two sentences instead.

---

## CSS starter template

Use this as the base for every visual explainer:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --orange: #eb5c32; --near-black: #1a1a18; --dg: #999; --lg: #d9d9d9;
  --navy: #1c2b3a; --slate: #4a6580; --pale: #c8d8e8; --ow: #f7f4f0;
  --white: #fff; --f: 'DM Sans', sans-serif;
}

body {
  font-family: var(--f); background: var(--white); color: var(--near-black);
  font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased;
}

/* Sections */
.section { max-width: 1100px; margin: 0 auto; padding: 80px 48px; }

/* Eyebrow labels */
.eyebrow {
  font-size: 11px; font-weight: 600; letter-spacing: .12em;
  text-transform: uppercase; color: var(--orange);
  display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
}
.eyebrow::after { content: ''; display: block; height: 1px; width: 36px; background: var(--orange); opacity: .4; }

/* Tables — no outer border, no last-row border */
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { font-size: 10px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
     color: var(--dg); text-align: left; padding: 8px 12px;
     background: var(--ow); border-bottom: 2px solid var(--lg); }
td { padding: 8px 12px; border-bottom: 1px solid var(--lg); vertical-align: top; line-height: 1.5; }
tr:last-child td { border-bottom: none; }

/* Cards — square corners always */
.card { background: var(--ow); border: 1px solid var(--lg); padding: 24px; }

/* Orange accent box — white title text */
.orange-box { background: var(--orange); color: white; padding: 16px 20px; }
.orange-box .title { font-weight: 600; color: white; }

/* Stats */
.stat-number { font-size: 36px; font-weight: 700; color: var(--orange); letter-spacing: -.03em; line-height: 1; }
.stat-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: var(--dg); margin-top: 4px; }

/* Footnote area */
.footnote-divider { border: none; border-top: 1px solid var(--lg); margin: 16px 0; }
.footnote-text { font-size: 8pt; color: var(--dg); line-height: 1.6; }
```

---

## Output structure

A typical visual explainer includes:

1. **Title section** — what this explains, one-line subtitle, TernCapital wordmark.
2. **Overview** — high-level summary or key stat.
3. **Main visual** — the core diagram, flow, or visualisation.
4. **Detail sections** — deeper breakdowns of each component.
5. **Summary or takeaway** — what the viewer should remember.
6. **Footnotes** (if applicable) — separated by a light grey divider, formatted as `Notes: 1) …`.

---

## Rules

- Self-contained. One HTML file. No external dependencies except Google Fonts.
- Every section must have a visual component — never just blocks of text.
- The page should be understandable in 30 seconds at a glance, with detail available for those who want to dig deeper.
- Works in any modern browser. No framework dependencies.
- **All corners square** — `border-radius: 0`. Never use rounded corners.
- If the concept has more than seven components, group them into categories first.
- Use real, specific language. "The API processes 10,000 requests/second" is better than "The API is fast."
- All bullets end with a full stop.
- EBITA not EBITDA. £10K not £10k. K/M consistent throughout.
- "na" not N/A. Sources split by semicolons.
