---
name: companies-house
description: Pull everything Companies House holds on a UK company — profile, officers (and their other appointments), PSCs, charges, insolvency, full filing history and every filed PDF (accounts, confirmation statements, incorporation docs) — and save it to a local folder the user chooses, so the documents can be read and analysed later. Use this whenever the user asks for a Companies House pull, CH data, CH filings, "get the accounts from Companies House", "download the filings for X", "who are the directors/PSCs of X", or gives a UK company name or 8-character company number (e.g. 07528947, SC123456) and wants its public records, even if they don't say "Companies House" explicitly. Also use it as the first step when a due diligence, statutory register review or deal assessment needs a target's public filings.
---

# Companies House pull

Downloads all public Companies House data for **one** company to a local folder: one JSON file per API endpoint plus every filed document as a PDF. The point is to have the raw source documents on disk so they can be read later (by the user or by Claude in a follow-up task such as a statutory register review or DD model), so always download the PDFs.

Scripts live in `scripts/` next to this file:
- `companies_house.py`: API client. Run it directly to search by name: `python companies_house.py <name words>` prints up to 10 matches as `number  status  name`.
- `dump_company.py`: `python dump_company.py <number> --root <parent folder>` does the full pull into `<parent folder>/<number> - <Company Name>` (the script makes the folder name Windows-safe). It downloads PDFs by default; `--no-pdfs` skips them for a quick profile-only check. It also writes `facts.md`, a mechanical digest of the key facts and filing signals. `--out <exact folder>` uses a folder as given instead of `--root`. By default it fetches other appointments only for **current** officers, to save calls on the shared rate limit. Add `--include-former-officers` to also fetch them for resigned officers (use it when the user asks about past directors' other roles, or for deeper due diligence on a target's management history).

Requires Python 3 and the `requests` package. If `import requests` fails, run `pip install -r "<skill dir>/requirements.txt"` first.

**Windows vs macOS/Linux.** The scripts run on all three. Only the shell commands differ. In this file, `python` means `python3` on macOS and Linux (try `python3` if `python` is missing or is Python 2). The default save folder is `%USERPROFILE%\Documents\Companies House` on Windows and `~/Documents/Companies House` elsewhere. Key setup is in Troubleshooting, with a variant for each.

## Steps

1. **Identify the company.** If you have a company number, use it. If you only have a name, run the search and show the user the likely matches (number, status, name). Ask them to confirm the right one. Similar names are common, and pulling the wrong company wastes time and could mislead a deal decision. Skip the confirmation only when exactly one active company matches the name exactly.

2. **Ask where to save it.** Ask the user which local folder to save into. Offer a sensible default: `%USERPROFILE%\Documents\Companies House` on Windows, `~/Documents/Companies House` on macOS/Linux. The script creates the `<number> - <Company Name>` subfolder inside it. If that subfolder already exists it is reused; the script skips PDFs it already has, so a rerun only adds new filings.

3. **Run the pull.**
   ```
   python "<skill dir>/scripts/dump_company.py" <number> --root "<folder the user chose>"
   ```
   The first output line shows the full path of the subfolder it created; use that path in step 4.
   A typical company takes about a minute. Companies with long histories (hundreds of filings) take longer because each PDF is a separate download, so allow a generous timeout (e.g. 10 minutes). The script prints a count for each section; "-" means Companies House has no record of that kind (e.g. no insolvency), which is normal. The documents line reads `N filings: X downloaded, Y already on disk, Z with no document, F failed`. Rate-limit waits (HTTP 429) are handled automatically and can pause the run for a few minutes. If `F` is above zero, rerun the same command; it only retries the missing PDFs.

4. **Write `SUMMARY.md` into the subfolder** and give the user the same summary in chat. Start from `facts.md`, which already holds the company, accounts, officers, PSCs, charges, filing counts and mechanical signals, and open the JSON files only for detail it doesn't carry. Your job is to turn it into a readable summary and add judgement on the signals; don't re-derive the facts by hand. Cover:
   - Name, number, status, type, incorporation date, registered office, SIC codes
   - Current directors and secretary (name, role, appointed date), plus notable resigned officers
   - Current PSCs and their nature of control (e.g. "75-100% shares")
   - Charges: outstanding vs satisfied, chargeholder, date created
   - Accounts: type of the last accounts filed (micro/small/full), made-up-to date, next due date, and whether overdue. Do the same for the confirmation statement.
   - Red flags worth a closer look: overdue filings, insolvency records, outstanding charges, frequent director changes, a recent change of registered office or name, a "proposal to strike off" (gazette) filing
   - The path of the folder and the PDF counts from the script's documents line (downloaded, already on disk, no document, failed). Say whether other appointments cover current officers only or former officers too.

   Keep it factual: report what the records say and don't speculate beyond them. The summary sits next to the data so a later task can get oriented without re-reading every JSON file.

## Output folder layout

```
<number> - <Company Name>/
├── SUMMARY.md          (written by Claude from facts.md)
├── facts.md            (written by the script)
├── profile.json, registered_office.json, officers.json, officer_appointments.json,
│   pscs.json, psc_statements.json, charges.json, insolvency.json, exemptions.json,
│   registers.json, uk_establishments.json, filing_history.json
└── documents/
    └── <date>_<category>_<form type>_<transaction id>.pdf
```

PDF filenames start with the filing date and category (`accounts`, `confirmation-statement`, `officers`, `capital`, `incorporation`, `mortgage`, …), so they sort chronologically and are easy to find, e.g. all accounts: `documents/*_accounts_*`. To match a PDF to its description, look up its transaction id in `filing_history.json`.

**Scanned PDFs need OCR.** Older filings (roughly pre-2010) and some paper-filed forms are images with no text layer, so text extraction returns nothing or blanks. When a later task reads these, check each PDF returns text; if not, OCR it (see the `pdf` skill) and tell the user which documents were scanned rather than treating them as empty. Modern accounts are often fine, but do not assume.

## Troubleshooting

- **API key (not bundled)**: no key is stored in the repo. The client looks for `COMPANIES_HOUSE_API_KEY` (process environment on any system, plus the Windows user environment), then `scripts/api_key.txt`. **Before step 3, check a key exists** (run the name search, or `python -c "import sys; sys.path.insert(0, r'<skill dir>/scripts'); import companies_house; companies_house.CompaniesHouse()"`). If it raises "Set COMPANIES_HOUSE_API_KEY...", tell the user no key is configured and ask them to paste a Live **REST** key (the shared Tern key, or their own from https://developer.company-information.service.gov.uk/). Save it so it survives plugin updates:
  - **Windows:** `setx COMPANIES_HOUSE_API_KEY "<key>"`. The client reads it straight from the user environment, so no restart is needed for the scripts. Also set `$env:COMPANIES_HOUSE_API_KEY` if you want it in the current PowerShell session.
  - **macOS/Linux:** append `export COMPANIES_HOUSE_API_KEY="<key>"` to `~/.zshrc` (macOS default) or `~/.bashrc`. That only reaches new terminals, and a Claude app launched outside a terminal may never load it, so for the current run prefix the command: `COMPANIES_HOUSE_API_KEY="<key>" python3 "<skill dir>/scripts/dump_company.py" ...`. The client reads only the process environment on these systems.
  - **Fallback on any system:** write the key to `scripts/api_key.txt` (on macOS/Linux also `chmod 600` it). That file is gitignored, but plugin updates may delete it.

  Never print the key or commit it.
- **HTTP 401**: the key is invalid, revoked or replaced. Ask the user for a new Live **REST** key and save it as above.
- **Rate limit**: the API allows 600 requests per 5 minutes per key, and the shared Tern key is used by the whole team. The client backs off automatically on HTTP 429, so a big pull may just pause for a while.
- **Some PDFs fail**: the script reports these with `!` and carries on; rerun the same command to retry them. Filings with no document at all (counted as "with no document") are normal for some old paper filings. Mention both in the summary.
- **"is not a company number" or "not found"**: the number is mistyped or it's a name. Search by name with `python companies_house.py <name words>`.
