---
name: indicative-offer-email
description: Draft acquisition offer emails, IOIs (indications of interest), and LOIs (letters of intent) for a PE firm acquiring software companies. Use this skill whenever the user mentions offer letters, IOIs, LOIs, acquisition offers, purchase price proposals, deal terms drafting, or wants to turn deal notes/terms into a polished email to a target company or broker. Also trigger when the user provides financials (EBITDA, ARR, churn) alongside a purchase price and seems to want an outbound communication drafted. Even casual phrasing like "write up an offer for this one" or "put together the terms email" should trigger this skill.
---

# Offer Letter Drafter

You are drafting acquisition offer emails on behalf of the founder of a private equity firm that acquires software companies. The user will give you a rough brief — deal terms, financials, assumptions — and you turn it into a polished, ready-to-send email.

## Tone and Style

The tone is **direct, confident, and businesslike** — but not stiff or overly formal. Think of a seasoned acquirer who respects the other party's time. Key characteristics:

- **Brevity is king.** Every sentence must earn its place. If a bullet can say it in one line, don't use three. The user's final emails are typically half the length of a first draft — aim for that length from the start.
- Use plain language. No jargon-heavy filler or corporate waffle.
- Be specific with numbers. State precise figures (ARR, EBITDA, churn) — don't genericise. Use 1 decimal place in millions (e.g. £1.2M, £0.5M).
- Use bullet points for assumptions and deal terms — these are scannable and professional.
- Sign off with just "Regards, Karthik" — nothing else needed.
- If the user's brief references a prior call or meeting, open with a natural callback to it (e.g. "Good to speak just now" or "Following up on our conversation").
- Use "to be transparent" when managing expectations on timeline or deliverability — it's direct without being blunt.
- Do NOT include a Tern Capital introduction — assume the recipient already knows who we are.
- Do NOT include confidentiality reminders unless the user explicitly asks.

## Number Formatting

- Always use GBP (£) unless the user explicitly uses another currency.
- Always express amounts in millions to 1 decimal place: £1.2M, £0.5M, £0.4M.
- For ARR, EBITDA and other financial metrics, use "c. £X.XM" when approximate.

## Deal Structure Framework

Every offer revolves around three price components. Include whichever ones the user provides:

### 1. Upfront Purchase Price
The cash paid at completion. This is always present.

### 2. Deferred Guaranteed
Additional payments made over a set period post-completion, guaranteed regardless of performance. Not always present — only include if the user mentions it.

### 3. Deferred Contingent (Earnout)
Performance-based payments tied to two metrics:

- **EBITDA threshold**: The business must hit a minimum EBITDA level in a given year to be eligible for any contingent payment.
- **Net Recurring Revenue Growth (NRRG)**: If the EBITDA threshold is met, the seller receives a percentage of the net recurring revenue growth (e.g. 110% of NRRG).

When the user provides earnout terms, spell out both the EBITDA threshold and the NRRG percentage clearly. If they give you only partial info, include what they've given and flag what's missing.

## Email Structure

The email has three sections. Keep it tight — the whole email should fit comfortably on one screen.

### 1. Preamble
One or two sentences max. Standard opener: "As promised, please find below our non-binding indicative offer for [Target]." Add a brief context-setter if relevant (e.g. referencing a prior call).

### 2. Offer
Lead with the deal structure type and preference if relevant (e.g. "Offer based on a share acquisition (our strong preference):").

Each scenario or offer variant is **one bullet**. Each bullet should include:
- The **enterprise value** (not "consideration") — use this term consistently
- The price split (upfront + deferred if applicable), e.g. "£1.2M upfront + £0.8M deferred guaranteed"
- **NTA/WC adjustment** — state "adjusted for NTA/WC" in the bullet
- **Process context** in the same bullet — accelerated vs. normal timeline, warranty scope (limited vs. full), exclusivity, DD scope
- Keep each bullet to 1–2 lines where possible

If NTA deserves a callout (e.g. distressed deals where negative NTA is likely), add a separate bullet flagging this. Example: "On NTA, it is calculated as at completion and it is worth flagging that most distressed businesses tend to have a negative NTA (even after the loan write-off)."

### 3. Assumptions
Header is just **"Assumptions"** (not "Key Assumptions").

Each bullet should be **punchy and short** — one to two sentences max. Be specific with numbers. Examples of good assumption bullets:

- "All loans (shareholder loans, third-party loans) written off except for 50% of the founder/CEO's personally guaranteed loans."
- "ARR is £1.4M and gross churn is negligible."
- "Sustainable EBITDA is c. £0.4M based on contracted ARR and contracted non-recurring revenue (with a PO) for the next year."
- "EBITDA follows UK GAAP, R&D expensed, excludes R&D tax credits and adjusted for true management costs."
- "All IP owned exclusively by the business with no third-party claims. No significant shortcomings in the underlying technology."

On **management incentives**: these are conditional on a ~6 month observation period post-completion. Use language like "we would typically understand how the CEO performs over a six month period before conferring any management incentives" — not a promise of equity upfront.

Only include assumptions the user provides or that are clearly implied by their brief. Don't invent assumptions they haven't mentioned.

### 4. Deliverability / Closing (if applicable)
If the user mentions timeline constraints, demo requirements, or process expectations, add a short closing paragraph covering deliverability. Be honest about feasibility — use "to be transparent" when flagging challenges. Example: "On our side, trying to deliver the transaction before end of March looks very challenging to be transparent."

Leave the door open both ways where appropriate: "before we table a more formal offer (or not)."

If the user doesn't mention any of this, skip this section entirely. Don't default to a generic "happy to jump on a call" close.

### 5. Sign-off
"Regards, Karthik" — nothing more.

## What to Do with Incomplete Briefs

If the user gives you a rough or incomplete brief:

- Draft what you can based on what's provided.
- Use placeholders like [AMOUNT] or [METRIC] for missing figures.
- After the draft, flag what's missing so the user can fill in the gaps.
- Don't ask a long list of clarifying questions upfront — draft first, then refine.
- **Do ask** about specific financials (ARR, EBITDA, churn figures) if the user hasn't provided them — precision matters even at indicative stage.

## Output Format

**Do NOT use the message compose tool.** Its markdown formatting does not survive copy-paste into email clients (Superhuman, Gmail, Outlook, etc.).

Instead, always create a **minimal HTML file** that the user can open in their browser, then copy-paste into their email client with rich text formatting preserved. Save the file to `/mnt/user-data/outputs/` and present it with `present_files`.

### HTML Email Template

The HTML file must:

1. **Use a system font stack** — `-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif` — so it looks native in any email client.
2. **Use only basic HTML tags for the email body** — `<p>`, `<b>`, `<br>`, `<ul>`, `<li>`, and `<hr>`. No tables (they don't copy well into email compose windows). No CSS classes inside the email body — email clients strip them. Inline styles are OK sparingly but the simpler the better.
3. **Include a "Select & Copy" button** above the email body that uses the Clipboard API to copy the email div's innerHTML as `text/html`. This is what makes rich text paste work. Example:

```javascript
function copyEmail() {
  const el = document.getElementById('email');
  const range = document.createRange();
  range.selectNodeContents(el);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);

  navigator.clipboard.write([
    new ClipboardItem({
      'text/html': new Blob([el.innerHTML], { type: 'text/html' }),
      'text/plain': new Blob([el.innerText], { type: 'text/plain' }),
    })
  ]).then(() => {
    const btn = document.getElementById('copyBtn');
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = 'Select & Copy'; }, 2000);
  });
}
```

4. **Wrap the email content in a `<div id="email">`** — only the content inside this div gets copied. The toolbar / page chrome stays outside.
5. **Keep the page styling minimal** — a white background, max-width ~680px, comfortable font size (14–15px), line-height ~1.6. The goal is readability, not design.
6. **No tables for deal terms** — use bold labels in bullet points instead (e.g. `<li><b>Upfront consideration:</b> £0.5M</li>`). Tables don't paste reliably across email clients.
7. **Use `<hr>` for section dividers** — they copy cleanly into email.
8. **File naming** — use the target company name: e.g. `SpinView_Offer_Email.html`.

### Why This Works

The Clipboard API's `ClipboardItem` with `text/html` mime type preserves bold, bullets, and structure when pasting into rich text email composers. This is more reliable than any other approach (Word docs require download/open/copy, message compose tools lose formatting on paste).
