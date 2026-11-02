"""Dump everything the Companies House API holds on one company.

Usage:
  python dump_company.py <company_number> --root DIR [--no-pdfs] [--include-former-officers]
  python dump_company.py <company_number> --out DIR  [--no-pdfs] [--include-former-officers]

--root DIR puts the pull in DIR/"<number> - <Company Name>" (name made safe for Windows).
--out DIR uses DIR itself. Either way the script writes one JSON file per endpoint,
other appointments of current officers (--include-former-officers adds resigned ones),
every filed document as a PDF via the Document API (--no-pdfs skips them), and facts.md,
a deterministic digest of the key facts and filing signals.
"""
import argparse
import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from companies_house import CompaniesHouse

ILLEGAL_PATH_CHARS = r'\/:*?"<>|'


def save(out, name, data):
    (out / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    count = len(data) if isinstance(data, list) else ("-" if data is None else 1)
    print(f"  {name:<40} {count}")


def folder_name(number, company_name):
    """'<number> - <Company Name>' with characters Windows rejects removed."""
    safe = "".join(c for c in company_name if c not in ILLEGAL_PATH_CHARS).strip().rstrip(".")
    return f"{number} - {safe}"


def _iso(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _ago(value, days, today):
    d = _iso(value)
    return d is not None and today - d <= timedelta(days=days)


def write_facts(out, profile, officers, pscs, charges, insolvency, filings, appts_mode, pdf_stats, today=None):
    """Write facts.md: everything here is read straight from the JSON, with no interpretation."""
    today = today or date.today()
    acc = profile.get("accounts", {})
    last_acc = acc.get("last_accounts", {})
    next_acc = acc.get("next_accounts", {})
    cs = profile.get("confirmation_statement", {})
    ro = profile.get("registered_office_address", {})
    L = [f"# {profile['company_name']} ({profile['company_number']}): facts", "",
         f"Generated {today.isoformat()} from Companies House data. Facts only; no interpretation.", "",
         "## Company",
         f"- Status: {profile.get('company_status')}"
         + (f" ({profile.get('company_status_detail')})" if profile.get("company_status_detail") else ""),
         f"- Type: {profile.get('type')}; jurisdiction: {profile.get('jurisdiction')}",
         f"- Incorporated: {profile.get('date_of_creation')}"
         + (f"; dissolved: {profile['date_of_cessation']}" if profile.get("date_of_cessation") else ""),
         "- Registered office: " + ", ".join(str(v) for v in ro.values() if v),
         f"- SIC codes: {', '.join(profile.get('sic_codes', [])) or 'none'}",
         "- Previous names: " + ("; ".join(f"{p['name']} (to {p.get('ceased_on')})"
                                         for p in profile.get("previous_company_names", [])) or "none"),
         "", "## Accounts and confirmation statement",
         f"- Accounting reference date: {acc.get('accounting_reference_date', {}).get('day')}/"
         f"{acc.get('accounting_reference_date', {}).get('month')}",
         f"- Last accounts: type {last_acc.get('type', 'none')}, made up to {last_acc.get('made_up_to', 'n/a')}",
         f"- Next accounts: period to {next_acc.get('period_end_on', 'n/a')}, due {next_acc.get('due_on', 'n/a')}, "
         f"overdue: {next_acc.get('overdue', acc.get('overdue'))}",
         f"- Confirmation statement: last made up to {cs.get('last_made_up_to', 'n/a')}, "
         f"next due {cs.get('next_due', 'n/a')}, overdue: {cs.get('overdue')}"]

    L += ["", "## Officers"]
    current = [o for o in officers if not o.get("resigned_on")]
    former = [o for o in officers if o.get("resigned_on")]
    L.append(f"- Current: {len(current)}; resigned: {len(former)}")
    for o in current:
        L.append(f"  - {o['name']}: {o.get('officer_role')}, appointed {o.get('appointed_on')}")
    for o in sorted(former, key=lambda o: o["resigned_on"], reverse=True)[:15]:
        L.append(f"  - (resigned {o['resigned_on']}) {o['name']}: {o.get('officer_role')}, "
                 f"appointed {o.get('appointed_on')}")
    if len(former) > 15:
        L.append(f"  - ... {len(former) - 15} more resigned officers in officers.json")
    L.append(f"- Other appointments fetched for: {appts_mode}")

    L += ["", "## Persons with significant control"]
    live_pscs = [p for p in pscs if not p.get("ceased")]
    L.append(f"- Current: {len(live_pscs)}; ceased: {len(pscs) - len(live_pscs)}")
    for p in live_pscs:
        L.append(f"  - {p.get('name')}: notified {p.get('notified_on')}; "
                 f"{', '.join(p.get('natures_of_control', [])) or 'no nature of control listed'}")

    L += ["", "## Charges"]
    out_ch = [c for c in charges if c.get("status") == "outstanding"]
    L.append(f"- Total: {len(charges)}; outstanding: {len(out_ch)}")
    for c in charges:
        holders = ", ".join(p.get("name", "") for p in c.get("persons_entitled", []))
        L.append(f"  - {c.get('status')}: created {c.get('created_on')}, "
                 f"{c.get('classification', {}).get('description', 'n/a')}; holder(s): {holders or 'n/a'}")

    L += ["", "## Filing history", f"- {len(filings)} filings, "
          + ", ".join(f"{k} {v}" for k, v in Counter(f.get("category", "other") for f in filings).most_common())]
    if pdf_stats:
        L.append(f"- PDFs: {pdf_stats}")
    else:
        L.append("- PDFs: not downloaded (--no-pdfs)")

    signals = []
    if next_acc.get("overdue") or acc.get("overdue"):
        signals.append("Accounts overdue")
    if cs.get("overdue"):
        signals.append("Confirmation statement overdue")
    if profile.get("has_insolvency_history") or insolvency:
        signals.append("Insolvency history recorded")
    if out_ch:
        signals.append(f"{len(out_ch)} outstanding charge(s)")
    gaz = [f for f in filings if f.get("category") == "gazette"]
    if gaz:
        signals.append("Gazette filing(s): " + "; ".join(
            f"{f['date']} {f.get('description', f.get('type'))}" for f in gaz[:5]))
    if profile.get("company_status") not in (None, "active"):
        signals.append(f"Company status is {profile.get('company_status')}")
    n_ro = sum(1 for f in filings if f.get("type") == "AD01" and _ago(f.get("date"), 730, today))
    if n_ro:
        signals.append(f"{n_ro} registered office change(s) in the last 2 years")
    n_name = sum(1 for p in profile.get("previous_company_names", []) if _ago(p.get("ceased_on"), 730, today))
    if n_name:
        signals.append(f"{n_name} name change(s) in the last 2 years")
    n_res = sum(1 for o in former if _ago(o["resigned_on"], 365, today))
    n_app = sum(1 for o in officers if _ago(o.get("appointed_on"), 365, today))
    if n_res or n_app:
        signals.append(f"Officer changes in the last year: {n_app} appointed, {n_res} resigned")
    if any(f.get("type") == "RP01CS01" or str(f.get("type", "")).startswith("RP") for f in filings):
        signals.append("Replacement/rectification filing(s) present (type RP*): see filing_history.json")
    L += ["", "## Signals (mechanical checks)"] + ([f"- {s}" for s in signals] or ["- None triggered"])

    (out / "facts.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"  {'facts.md':<40} written ({len(signals)} signal(s))")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("company_number")
    dest = ap.add_mutually_exclusive_group(required=True)
    dest.add_argument("--root", help='parent folder; creates "<number> - <Company Name>" inside it')
    dest.add_argument("--out", help="exact output folder")
    ap.add_argument("--no-pdfs", action="store_true", help="skip downloading filed documents")
    ap.add_argument("--pdfs", action="store_true", help=argparse.SUPPRESS)  # old flag; PDFs are now the default
    ap.add_argument("--include-former-officers", action="store_true",
                    help="also fetch other appointments of resigned officers (default: current officers only)")
    args = ap.parse_args()

    n = args.company_number.strip().upper().zfill(8)
    if not re.fullmatch(r"[A-Z0-9]{8}", n):
        raise SystemExit(f'"{args.company_number}" is not a company number (8 characters, e.g. 07528947 or SC123456). '
                         "To search by name: python companies_house.py <name words>")

    ch = CompaniesHouse()
    profile = ch.company(n)
    if profile is None:
        raise SystemExit(f"Company {n} not found. Check the number, or search by name: "
                         "python companies_house.py <name words>")
    out = Path(args.out) if args.out else Path(args.root) / folder_name(n, profile["company_name"])
    out.mkdir(parents=True, exist_ok=True)
    print(f"{profile['company_name']} ({n}) -> {out.resolve()}")
    save(out, "profile", profile)

    save(out, "registered_office", ch.registered_office(n))
    save(out, "officers", officers := ch.officers(n))
    save(out, "filing_history", filings := ch.filing_history(n))
    save(out, "pscs", pscs := ch.pscs(n))
    save(out, "psc_statements", list(ch._paged(f"/company/{n}/persons-with-significant-control-statements")))
    save(out, "charges", charges := list(ch._paged(f"/company/{n}/charges")))
    save(out, "insolvency", insolvency := ch.insolvency(n))
    save(out, "exemptions", ch.get(f"/company/{n}/exemptions"))
    save(out, "registers", ch.get(f"/company/{n}/registers"))
    save(out, "uk_establishments", ch.get(f"/company/{n}/uk-establishments"))

    # Other appointments held by officers. Current officers only unless --include-former-officers,
    # because each officer costs at least one call against the shared rate limit.
    appointments = {}
    for o in officers:
        if o.get("resigned_on") and not args.include_former_officers:
            continue
        m = re.match(r"/officers/([^/]+)/appointments", o.get("links", {}).get("officer", {}).get("appointments", ""))
        if m and m.group(1) not in appointments:
            appointments[m.group(1)] = {"name": o["name"], "appointments": ch.officer_appointments(m.group(1))}
    save(out, "officer_appointments", appointments)

    pdf_stats = None
    if not args.no_pdfs:
        pdf_dir = out / "documents"
        pdf_dir.mkdir(exist_ok=True)
        downloaded = present = failed = no_doc = 0
        for f in filings:
            meta_url = f.get("links", {}).get("document_metadata")
            if not meta_url:
                no_doc += 1
                continue
            path = pdf_dir / f"{f['date']}_{f.get('category', 'other')}_{f['type']}_{f['transaction_id']}.pdf"
            if path.exists():
                present += 1
                continue
            r = ch.request(meta_url + "/content", headers={"Accept": "application/pdf"}, timeout=60)
            if r.ok:
                path.write_bytes(r.content)
                downloaded += 1
            else:
                failed += 1
                print(f"  ! {path.name}: HTTP {r.status_code}")
        pdf_stats = (f"{len(filings)} filings: {downloaded} downloaded, {present} already on disk, "
                     f"{no_doc} with no document, {failed} failed")
        print(f"  {'documents (pdf)':<40} {pdf_stats}")
        if failed:
            print("  Some downloads failed; rerun the same command to retry only those.")

    write_facts(out, profile, officers, pscs, charges, insolvency, filings,
                "current and former officers" if args.include_former_officers else "current officers only",
                pdf_stats)


if __name__ == "__main__":
    main()
