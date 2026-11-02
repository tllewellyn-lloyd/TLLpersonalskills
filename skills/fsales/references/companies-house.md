# Companies House CLI (`ch`)

Official Companies House API, read through `ch`, the CLI bundled in the fsales folder. Run it as `cd <base directory> && python3 ch <command>`. Every command prints JSON. Needs Python 3.9+, `requests`, and `CH_API_KEY` in the environment.

Auth: HTTP Basic, key as username, empty password (handled by the client). Never print or commit the key. The key allows 600 requests per 5 minutes. A 429 waits for the window in `X-Ratelimit-Reset` and retries (up to 4 times). Each run ends with `Companies House API calls this run: N` on stderr.

## Commands

Company numbers are normalised (`445790` becomes `00445790`; `sc123456` becomes `SC123456`). List commands read every page unless `--limit N` is given. `--param KEY=VALUE` (repeatable) passes any extra query parameter, such as `register_view=true`, `category=accounts`, `order_by=surname`, or `items_per_page`. A 404 prints `{"found": false}`.

| Command | Reads | Spec endpoint |
| --- | --- | --- |
| `profile NUM` | Company profile | `/company/{n}` |
| `registered-office NUM` | Registered office address | `/company/{n}/registered-office-address` |
| `registers NUM` | Statutory registers held at Companies House | `/company/{n}/registers` |
| `insolvency NUM` | Insolvency information | `/company/{n}/insolvency` |
| `exemptions NUM` | Filing exemptions | `/company/{n}/exemptions` |
| `officers NUM` | Officers, all pages | `/company/{n}/officers` |
| `appointment NUM APPT_ID` | One officer appointment | `/company/{n}/appointments/{id}` |
| `officer-appointments OFFICER_ID` | Every appointment held by one officer | `/officers/{id}/appointments` |
| `charges NUM` | Charges, all pages | `/company/{n}/charges` |
| `charge NUM CHARGE_ID` | One charge | `/company/{n}/charges/{id}` |
| `filings NUM` | Filing history, most recent first | `/company/{n}/filing-history` |
| `filing NUM TRANSACTION_ID` | One filing history item | `/company/{n}/filing-history/{id}` |
| `psc NUM` | Persons with significant control | `/company/{n}/persons-with-significant-control` |
| `psc-get NUM KIND ID` | One PSC notification | `/company/{n}/persons-with-significant-control/{kind}/{id}` |
| `psc-statements NUM` | PSC statements | `/company/{n}/persons-with-significant-control-statements` |
| `psc-statement NUM STATEMENT_ID` | One PSC statement | `/company/{n}/persons-with-significant-control-statements/{id}` |
| `psc-notifications PSC_ID` | Notifications for one PSC id across companies | `/persons-with-significant-control/{id}/notifications` |
| `uk-establishments NUM` | UK establishments of an overseas company | `/company/{n}/uk-establishments` |
| `disqualified-natural OFFICER_ID` | Natural officer disqualifications | `/disqualified-officers/natural/{id}` |
| `disqualified-corporate OFFICER_ID` | Corporate officer disqualifications | `/disqualified-officers/corporate/{id}` |
| `search QUERY` | Search all records | `/search` |
| `search-companies QUERY` | Company name search | `/search/companies` |
| `search-officers QUERY` | Officer name search | `/search/officers` |
| `search-disqualified QUERY` | Disqualified officer search | `/search/disqualified-officers` |
| `advanced-search --param ...` | Advanced company search (filters in `--param`) | `/advanced-search/companies` |
| `alphabetical-search --param ...` | Companies in alphabetical order | `/alphabetical-search/companies` |
| `dissolved-search --param ...` | Dissolved companies | `/dissolved-search/companies` |

All 34 Public Data API endpoints in the developer spec are covered by the table above.

Other commands:

- `get PATH [--param ...] [--paged] [--limit N]` reads any Public Data API path, including ones not in the table.
- `document REF [--save FILE] [--accept TYPE]` uses the Document API. `REF` is the `links.document_metadata` URL from a filing item, or its id. Without `--save` it prints metadata. With `--save` it writes the file (PDF by default). Tested: a 3-page filing PDF downloaded and opened correctly.
- `stream RESOURCE [--timepoint N] [--max-events N]` uses the Streaming API. **Not working with the REST key yet**: the stream host returns `401 Invalid Authorization`. Streaming needs its own access on the Companies House developer hub, so raise it with Karthik before relying on it.
- `company-all NUM [--out DIR] [--no-deep] [--docs N]` reads everything for one company into a folder (default `./ch-data/NUMBER`). It writes one JSON file per section (`profile`, `registered_office`, `registers`, `insolvency`, `exemptions`, `officers`, `charges`, `filing_history`, `uk_establishments`, `psc`, `psc_statements`), plus `psc_detail` and `officer_detail` (each officer's full appointment list and disqualifications) unless `--no-deep`. `--docs N` also downloads the PDFs of the N most recent filings into `documents/`. `manifest.json` lists the counts, the call total and any document errors. `"not found"` in a section means the company has no such record (for example, no insolvency).

## Which command for which question

- Owners and control: `psc NUM`, then `psc-get` on any corporate PSC's own company number (`profile` on its `identification.registration_number`) to follow the chain up.
- Who runs it, and their other directorships: `officers NUM`, then `officer-appointments OFFICER_ID`.
- Liquidation and strike-off: `profile` (`company_status`, `date_of_cessation`), `insolvency`, and `filings` (look for DISS40 and the liquidation filings). The Gazette is not in the API, so use Exa for it.
- Losses and going concern: `filings` for the accounts, then `document` on the accounts PDF (small companies often file abridged accounts with no P&L).
- Debt: `charges NUM`.
- Finding a company from a name: `search-companies "NAME"`, then `profile` on the number. Check for same-name companies before deciding which one is meant.
