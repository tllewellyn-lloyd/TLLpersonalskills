---
name: "mm-questions"
description: "Build the list of questions to ask a target's management team on a management call, derived from what an Information Memorandum does NOT answer, and prepend them to that company's page in the Tern Capital Deals database in Notion. Use whenever there is an IM (PDF, teaser, CIM, pasted summary, or an existing Notion deal page) and a management meeting coming up. Trigger on \"questions for the management meeting\", \"questions for the MM\", \"what should I ask them\", \"build the MM questions\", \"what is not answered in the IM\", \"prep me for the management call\", \"questions for the call with [target]\", or any variation where you need to walk into a call with a target knowing what to ask. Also trigger when an IM has just been processed into a deal page and a call is mentioned, or when asked for meeting prep on a live deal. Produces Notion page content, not an email - use agenda-builder for an advisor agenda email, and tern-deal-page-from-im for pre-NDA written data requests."
---

# Management Meeting Questions

Turns an IM into the list of questions James actually asks out loud on a management call, and files it at the top of the target's page in the Tern Deals database so he can annotate answers inline during the meeting.

The finished artefact is a `## Questions for MM` section, split by theme, that James types answers straight into as the call happens. Six weeks later that page is the only record of what management said.

## Why this is a different job from "Questions for the advisor"

`tern-deal-page-from-im` already puts a *Questions for the advisor* list on the deal page. Those are written data requests — "can you provide a revenue split by product for FY24 and FY25?" — sent by email, answered by a spreadsheet.

These are different. A management call is the one chance to hear an unrehearsed answer from the person who runs the business. So the questions that belong here are the ones where **the answer's texture matters more than the number**: why they lose deals, what breaks if a key person leaves, what they would do first if they were buying it. If a question can be fully answered by sending a file, it belongs in the advisor list, not this one.

Two practical consequences:

- **Write questions as they would be spoken.** "Can you walk us through the pricing model — is it per seat, per device, per rep?" not "Provide pricing model detail." James reads these off a screen while talking to a founder; stilted data-request phrasing makes him sound like an auditor.
- **Quote the IM back when challenging it.** Sell-side documents make claims without evidence constantly. The strongest question in the list is usually the seller's own adjective handed back to them: *"You've said low churn but there are no numbers — what's your annual logo churn over the last three years, and can you give examples of customers you've lost and why?"* That is much harder to deflect than "what is churn?", and it signals the document was read properly.

## Workflow

1. **Get the IM.** Usually a PDF in `uploads/`. Use the `pdf` skill for text extraction; if the PDF is image-only, OCR it (`pdftoppm` then `tesseract`) rather than giving up — blind teasers are often scans, and they are exactly the cases that need this most. If several documents cover the same deal, merge them rather than picking one; sell-side often circulates an operational version and a strategic version with different disclosures, and the differences between them are informative.

2. **Establish the company's real identity.** The IM may be blind — a broker reference like `CN03-ABS` and no name. If the name is not in the document or the conversation, ask. Without a name you cannot research, and the research is where the good questions come from. Don't invent an identity from circumstantial detail; if you infer one, say so and ask for confirmation before relying on it.

3. **Research outside the IM** (see below). This is what separates a list of obvious gaps from a list that makes management sit up.

4. **Draft the list** against the themes below.

5. **Prepend to the Notion deal page** (mechanics below).

6. **Report back in chat**: the Notion link, the question count, and the three or four questions that would most change the deal view, with one line each on why. Don't reproduce the whole list in chat — James is about to open the page.

**If time is short** (the call is imminent and the research step won't finish), say so and offer the choice: a fast IM-only list now, or the researched version. Don't silently skip the research — the omission needs to be visible, because a list built without it looks complete while missing the sharpest questions.

## Section structure

Use these headings, in this order. They match how a management call actually runs, so James can follow the page top to bottom during the meeting rather than hunting.

```
## Questions for MM
### Introduction & rationale for sale
### Commercial
### Product & technology
### People
### Finance
### Transaction & post-deal
```

Under the H2, add one italic line orienting the reader — how much the IM disclosed, and therefore how much of the list is a genuine gap rather than a follow-up. For a blind teaser: *"Blind teaser only — no financials, no product name, no named management, no competitors. Almost everything below is a gap rather than a follow-up."* For a full IM with audited numbers, say so; the list will be shorter and sharper.

Mark the questions that would change the deal view with ⭐ specifically — not ★, not bold, not "(priority)" — at the start of the bullet, and state that convention in the italic line. Consistency matters because James searches across deal pages for starred items. Expect roughly 10-20% starred; if a third of the list is starred, nothing is.

## Calibrating length

A blind teaser leaves 60-80 questions on the table. A detailed 90-page IM with three years of audited accounts might leave 25. Let the document set the length — don't pad a good IM to look thorough, and don't truncate a bad one to look concise.

What matters more than count is that **every question is genuinely unanswered**. Asking management something the IM states plainly on page 12 is the fastest way to look like the document wasn't read. Before finalising, re-scan the IM for each question and cut any already answered. If a question is *partially* answered, reframe it to start from what is disclosed: "The IM shows top 10 at 19% of revenue — who are they, and are any at risk?"

## Where the sharpest questions come from

Four patterns produce most of the questions that actually move a deal.

- **Adjectives without arithmetic.** "Low churn", "highly retained", "market-leading", "consistently profitable". Each is a claim with a number behind it that the IM chose not to print. Ask for the number.
- **Euphemism in the reason for sale.** The most heavily drafted section of any IM. One teaser said the sale was driven by "shareholder portfolio transition **and industry evolution**" — the second half was doing a lot of quiet work in a market facing disruption, and it became the highest-value question in the list. Read that section adversarially.
- **The gap between the IM and the outside world.** The website, app stores and Companies House will contradict or complete the IM: products the IM didn't name, a founding date that doesn't match, an Android app that doesn't exist, a holding company incorporated the month of the MBO.
- **Growth stories resting on unbuilt product.** IMs routinely list customer-requested modules as the growth case. The question isn't whether customers want them — it's why, with customers asking, they were never built. The answer is usually capacity, capability or conviction, and all three matter.

## Adjusted EBITDA deserves special attention

Owner-managed UK software businesses are almost always marketed on an adjusted EBITDA that strips out director costs. When the directors are also the people running the business and they are all leaving, that number is not the earnings a buyer inherits.

So whenever the IM presents an adjusted or normalised EBITDA, the list needs three questions rather than one: what is in the adjustment, what the directors currently take in total comp (salary, dividends, pension, benefits), and **what it would cost to hire replacements at market rate**. Ask that last one directly — "what would it cost to replace what the three of you do?" — because management have usually thought about it, and the answer reveals how much of the business sits in their heads.

---

## Research before writing

An IM is a marketing document produced by the seller. Twenty minutes outside it surfaces things the seller chose not to print. Do this before drafting, not after — what you find reshapes the whole list rather than adding a footnote.

### The company's website

Fetch the homepage, product pages and integrations page.

- **Product names.** Blind teasers withhold them; the site publishes them. Naming products back to management is the clearest signal the homework was done.
- **The full product set.** Teasers often describe one product when there are four. A second product can change the thesis — a self-service ordering product sitting alongside a rep-facing app answers the disruption question the teaser raised.
- **Platform coverage.** Which operating systems, devices and browsers are named. Absences matter: an iOS-only app in a market where buyers use Android is a live commercial gap.
- **Named customers and testimonials.** The IM anonymises; the website brags. Cross-reference for concentration and sector mix.
- **Integrations.** Which ERP, accounting and CRM systems — tells you the customer profile and where switching costs sit.
- **Staleness signals.** Copyright dates, discontinued devices in the copy, a blog that stopped, case studies from six years ago. Weak evidence alone, but combines with other signals about investment levels.
- **Founding date**, which often disagrees with the IM. Small in itself, but establishes that the two sources don't reconcile.

### Companies House

Search the name at `find-and-update.company-information.service.gov.uk`. Useful pages: overview, `/officers`, `/persons-with-significant-control`, `/filing-history`, `/charges`.

- **Group structure.** A holding company above the trading company usually means a transaction happened; its incorporation date dates that transaction.
- **PSC history.** Ceased PSCs and their control bands show who sold and roughly what they held; active PSCs show the current split. This answers ownership questions the IM leaves vague — and PSC filings sometimes contradict each other, which is itself a question.
- **Director appointment and resignation dates.** A resignation on the same date a new holdco's PSCs were notified is the transaction date.
- **Charges.** Registered charges point to bank debt; an unsatisfied charge is a question the IM won't have raised.
- **Filed accounts.** Even filleted small-company accounts give net assets and often employee numbers — a sanity check against the IM. Watch for a shortened accounting period, which makes a headline revenue figure not comparable.

Report Companies House findings as public-record rather than IM content, and keep them in a clearly separated block on the deal page. Mixing verified filings with seller claims makes the page less useful later, when it matters which was which.

### App stores, if there is a mobile product

Check what is actually published: platforms, last update date, version history, review volume. An app last updated two years ago says something the IM won't.

### Turning research into questions

Findings become questions in one of three shapes.

- **Reconciliation**, where the IM and the outside world disagree: "The website says established 1981 but the IM says 1983 — which is right?"
- **Gap**, where the outside world reveals an omission: "The app looks to be iOS-only — is there an Android version, and how often does that cost you a deal?"
- **Reframing**, where research changes what's worth asking. The most valuable kind. If the teaser raises a disruption risk and the website shows they already sell the disruptive product, the question stops being "are you about to be disrupted?" and becomes "what share of revenue is that product today, and is it growing faster than the legacy one?"

---

## Question themes by section

Prompts to adapt, not text to paste — a question naming the target's own products, numbers and sectors lands very differently from a generic one. Skip any theme the IM already answers properly.

### Introduction & rationale for sale

Hear the real reason for sale in their own words, and find out whether the shareholders are aligned. Misalignment between sellers is the most common reason a process dies late.

- History of the business and the major pivots — especially for a long-established company, where the current product may be the third or fourth generation
- Why sell, and why now. Ask plainly, then stay quiet. If the IM used a euphemism, quote it back and ask what it means.
- Prior transactions — MBO, MBI, prior PE, partial exit: when, from whom, how funded, and **whether any deferred consideration, loan note or bank debt is still outstanding**, since that sits ahead of Tern's money and changes the effective price
- Shareholding split, and whether every shareholder is aligned on a full exit now
- What each of them wants to do afterwards; whether any would stay or reinvest
- Whether they've run a process before or had approaches, and what happened
- How they arrived at the asking price

### Commercial

Usually where the IM is thinnest relative to its claims, and where the value case is won or lost.

- **Pricing model in detail** — per seat, per device, per rep, per transaction, tiered — and what a typical customer actually pays per year. Frequently omitted entirely.
- **Churn and retention with actual numbers** over at least three years, plus named examples of customers lost and why. Insist on the "why" — the pattern in lost customers is the most predictive thing in a management call.
- Renewal mechanics: auto-renew or annual opt-in? Price escalation rights? When did they last raise prices, and have they passed through inflation? A business that has never raised price has hidden upside; one that cannot has a problem.
- Customer concentration — who the top customers are, tenure, and whether any are at risk
- Shape of the base: size distribution, and how much is very small accounts costing more to serve than they generate
- New logos won and lost per year, not just the net count
- **Competitors by name, and who they lose to and why.** IMs often name none at all, which is itself informative.
- Lead sources and sales motion — inbound, outbound, channel, partner, reputation. If headcount shows no sales team, ask how growth is supposed to happen.
- Pipeline now, and typical sales cycle length
- Any freemium or trial tier: size, what it includes, historical conversion
- Implementation and onboarding — charged or free, and how long. Long unpaid implementations are a hidden cost of sale.
- Contract quality: signed contracts or just licence terms and an invoice? Change-of-control and assignment provisions?
- Geographic mix, and how non-domestic customers are won and supported
- Any expansion sectors or products the IM flags as opportunities — attempted, and what happened?

### Product & technology

Separate a real platform from a long-lived codebase with a marketing site.

- Get a **demo**, specifically of the workflow that matters most to the customer
- Revenue by product; how many customers sit on legacy or end-of-life products, and the plan for those
- Age of the codebase and their honest view of technical debt. For an old company this is the central technical question.
- Platform coverage gaps — mobile OS, browser, offline capability — and how often a gap costs them a deal
- Multi-tenant SaaS or single instances per customer? Anything still on customer premises? Drives cost to serve and migration burden.
- Hosting arrangements and annual cost; single points of failure
- Integrations: which systems, how built, how maintained, by whom
- Who writes the code — in-house, contractors, offshore — and who the single most critical technical person is
- What has actually shipped in the last two years versus what was on the roadmap
- **Why the customer-requested modules in the growth story were never built**, and what building them would cost
- How they see the technology shifts in their market — AI, self-service, marketplace disruption of their channel. What are customers asking for?
- IP and source code ownership, including whether contractor work was ever done without a written assignment
- Security and data protection posture: certifications, pen tests, customer questionnaires they struggle with
- Material outages, data incidents or escalated complaints in the last three years

### People

Key person risk is the biggest unpriced risk in a small owner-managed software business.

- Walk through the team: roles, tenure, salary. Ask verbally even if a schedule is coming later — how they describe their own people is informative.
- What the sellers actually do day to day, and what happens to that work when they leave
- **What breaks if the most critical person left tomorrow** — ask about the technical lead and the support lead specifically
- Who owns sales and marketing today
- Attrition over three years, and whether leavers were replaced
- Share options, bonus schemes, profit shares; anyone outside the shareholders who expects equity
- Contract hygiene: employment contracts, restrictive covenants, IP assignment; consultants or overseas contractors who should be employees
- How the support model works at their headcount — ticket volume, cover during holiday and sickness
- What a market-rate management structure would look like post-exit, and what it would cost

### Finance

- The full pack: three years of statutory accounts, current-year management accounts, current budget
- **The bridge from statutory operating profit to the adjusted EBITDA being marketed**, item by item
- Total director remuneration across salary, dividends, pension and benefits
- **What replacing the directors at market rate would cost** — the question that resets the multiple
- Revenue in each of the last five years. Growing, flat or declining is what the IM most often avoids by showing only the current year.
- Revenue split by product, by customer sector, by geography
- Recurring revenue confirmed in cash terms, and exactly what sits in the non-recurring remainder
- Billing and working capital: invoiced annually in advance? Deferred income balance? Intra-year cash profile?
- Gross margin, and what sits in cost of sales — hosting, third-party licences, support
- Largest overhead lines and how each moved over three years
- Capex and capitalised development; how much development cost is expensed versus capitalised
- R&D tax credits — claimed, how much, on what basis
- Cash position; any debt, overdraft, invoice finance or director loan balances
- Net assets, and how much cash they expect to leave in the business
- Bad debt history and current arrears
- Anything pending: litigation, disputes, HMRC enquiries, property dilapidations

### Transaction & post-deal

- Process and timetable, and whether other parties are involved
- Deal perimeter: single company or several entities? Any assets held personally, such as IP or property?
- What handover they envisage in practice, and what they expect to be paid for it
- Whether any of them would reinvest and stay involved
- Finish with a version of: *"If you were buying this business, what's the first thing you'd do — and what worries you most about the next five years?"* It goes last because by then the founder has relaxed, and it reliably surfaces the risk no amount of document review would have found. Keep it.

---

## Writing to the Notion deal page

The Tern Deals database sits at `https://www.notion.so/terncapital/a46453609e794e1eb554b88baa576691`, data source ID `0ac4c7f1-9dbc-4d84-988b-fee41f6101a3`, under Sourcing then Deals.

### Finding the page

Query the data source by company name:

```
notion-query-data-sources, mode "sql":
  data_source_urls: ["collection://0ac4c7f1-9dbc-4d84-988b-fee41f6101a3"]
  query: SELECT url, "Name" FROM "collection://0ac4c7f1-9dbc-4d84-988b-fee41f6101a3" WHERE "Name" LIKE ?
  params: ["%Blue Alligator%"]
```

Match loosely — pages are titled inconsistently ("Eurosoft Tech Limited", "Blue Alligator"), so search on the distinctive word rather than the full legal name. `notion-search` scoped to the data source also works and tolerates fuzzier input.

If more than one page matches, ask which. If none matches, the deal page doesn't exist yet: say so and offer to run `tern-deal-page-from-im` first. Don't silently create a page — this skill's job is the questions, and a page created without the IM extraction will be missing the context that makes the questions readable later.

Then `notion-fetch` the page before writing, to confirm it's the right company and to check whether a `## Questions for MM` section already exists.

### Writing

Prepend with `notion-update-page`, `command: "insert_content"`, `position: {"type": "start"}`. The questions go above the IM summary because during the call that's what James is looking at; the summary is reference material he has already read.

Date the heading when there could be more than one round of meetings — `## Questions for MM - 14/07/2026`. A single first meeting can just be `## Questions for MM`.

If a `## Questions for MM` section already exists with answers annotated underneath, **do not overwrite it**. Those annotations are the record of what management said and cannot be regenerated. Add a new dated section above it instead, and say that's what you did.

### Markdown that works

Notion-flavoured Markdown, kept simple:

- `##` for the section heading, `###` for each theme
- `-` bullets, one question each, no numbering — numbers imply an order a real conversation won't follow
- `*italic*` for the orienting line under the H2
- `**bold**` sparingly, for the occasional emphasised phrase inside a question
- `⭐` at the start of a bullet for priority questions
- Blank line before every list and after every heading, or the rendering breaks

Avoid nested bullets — a flat list per theme is easier to read on a screen mid-call and easier to type answers into.

