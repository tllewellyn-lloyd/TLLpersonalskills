"""`ch` command line for the Companies House API. Prints JSON to stdout.

Run from this skill's folder: python3 ch <command> ...  (needs CH_API_KEY in the environment).
"""
import argparse
import json
import os
import re
import sys

import requests

from ch_cli.client import (
    CH,
    PSC_KINDS,
    STREAM_RESOURCES,
    CHError,
    normalise_number,
)

# name, help, path template, positional arguments, mode ("get" or "list")
ENDPOINTS = [
    ("profile", "Company profile", "/company/{company}", ["company"], "get"),
    ("registered-office", "Registered office address", "/company/{company}/registered-office-address", ["company"], "get"),
    ("registers", "Statutory registers held at Companies House", "/company/{company}/registers", ["company"], "get"),
    ("insolvency", "Insolvency information", "/company/{company}/insolvency", ["company"], "get"),
    ("exemptions", "Exemptions from filing requirements", "/company/{company}/exemptions", ["company"], "get"),
    ("officers", "Company officers (all pages)", "/company/{company}/officers", ["company"], "list"),
    ("appointment", "One officer appointment", "/company/{company}/appointments/{appointment_id}", ["company", "appointment_id"], "get"),
    ("officer-appointments", "Every appointment held by one officer (all pages)", "/officers/{officer_id}/appointments", ["officer_id"], "list"),
    ("charges", "Charges over the company's assets (all pages)", "/company/{company}/charges", ["company"], "list"),
    ("charge", "One charge", "/company/{company}/charges/{charge_id}", ["company", "charge_id"], "get"),
    ("filings", "Filing history (all pages, most recent first)", "/company/{company}/filing-history", ["company"], "list"),
    ("filing", "One filing history item", "/company/{company}/filing-history/{transaction_id}", ["company", "transaction_id"], "get"),
    ("psc", "Persons with significant control (all pages)", "/company/{company}/persons-with-significant-control", ["company"], "list"),
    ("psc-get", "One PSC notification; KIND is one of: " + ", ".join(PSC_KINDS), "/company/{company}/persons-with-significant-control/{kind}/{notification_id}", ["company", "kind", "notification_id"], "get"),
    ("psc-statements", "PSC statements (all pages)", "/company/{company}/persons-with-significant-control-statements", ["company"], "list"),
    ("psc-statement", "One PSC statement", "/company/{company}/persons-with-significant-control-statements/{statement_id}", ["company", "statement_id"], "get"),
    ("psc-notifications", "Notifications for one PSC id across companies (all pages)", "/persons-with-significant-control/{psc_id}/notifications", ["psc_id"], "list"),
    ("uk-establishments", "UK establishments of an overseas company (all pages)", "/company/{company}/uk-establishments", ["company"], "list"),
    ("disqualified-natural", "Disqualifications for a natural officer", "/disqualified-officers/natural/{officer_id}", ["officer_id"], "get"),
    ("disqualified-corporate", "Disqualifications for a corporate officer", "/disqualified-officers/corporate/{officer_id}", ["officer_id"], "get"),
    ("search", "Search all Companies House records (all pages)", "/search", ["q"], "list"),
    ("search-companies", "Search companies by name (all pages)", "/search/companies", ["q"], "list"),
    ("search-officers", "Search officers by name (all pages)", "/search/officers", ["q"], "list"),
    ("search-disqualified", "Search disqualified officers by name (all pages)", "/search/disqualified-officers", ["q"], "list"),
    ("advanced-search", "Advanced company search; filters go in --param (all pages)", "/advanced-search/companies", [], "list"),
    ("alphabetical-search", "Companies in alphabetical order; filters go in --param (all pages)", "/alphabetical-search/companies", [], "list"),
    ("dissolved-search", "Dissolved companies; filters go in --param (all pages)", "/dissolved-search/companies", [], "list"),
]
ENDPOINTS_BY_NAME = {spec[0]: spec for spec in ENDPOINTS}


def emit(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def params_from(pairs):
    out = {}
    for pair in pairs or []:
        key, sep, value = pair.partition("=")
        if not sep or not key.strip():
            raise CHError(f"--param needs KEY=VALUE, got {pair!r}")
        out[key.strip()] = value
    return out


def count(data):
    if data is None:
        return "not found"
    if isinstance(data, dict) and "items" in data:
        return len(data["items"])
    return "ok"


def safe_name(text):
    return re.sub(r"[^A-Za-z0-9._-]", "_", text)


def run_endpoint(ch, spec, args):
    name, _, template, names, mode = spec
    values = {n: getattr(args, n) for n in names}
    if "company" in values:
        values["company"] = normalise_number(values["company"])
    if "kind" in values and values["kind"] not in PSC_KINDS:
        raise CHError(f"kind must be one of: {', '.join(PSC_KINDS)}")
    path = template.format(**{k: v for k, v in values.items() if k != "q"})
    params = params_from(args.param)
    if "q" in values:
        params["q"] = values["q"]
    if mode == "list":
        return ch.paged(path, params, allow_404=True, limit=args.limit)
    return ch.get(path, params or None, allow_404=True)


def company_all(ch, number, out_dir, deep, docs):
    number = normalise_number(number)
    base = f"/company/{number}"
    out_dir = out_dir or os.path.join("ch-data", number)
    os.makedirs(out_dir, exist_ok=True)
    summary = {}

    def write(section, data):
        with open(os.path.join(out_dir, f"{section}.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        summary[section] = count(data)
        return data or {}

    write("profile", ch.get(base))
    write("registered_office", ch.get(f"{base}/registered-office-address", allow_404=True))
    write("registers", ch.get(f"{base}/registers", allow_404=True))
    write("insolvency", ch.get(f"{base}/insolvency", allow_404=True))
    write("exemptions", ch.get(f"{base}/exemptions", allow_404=True))
    officers = write("officers", ch.paged(f"{base}/officers", allow_404=True))
    write("charges", ch.paged(f"{base}/charges", allow_404=True))
    filings = write("filing_history", ch.paged(f"{base}/filing-history", allow_404=True))
    write("uk_establishments", ch.paged(f"{base}/uk-establishments", allow_404=True))
    psc = write("psc", ch.paged(f"{base}/persons-with-significant-control", allow_404=True))
    write("psc_statements", ch.paged(f"{base}/persons-with-significant-control-statements", allow_404=True))

    if deep:
        psc_detail = [ch.get(item["links"]["self"], allow_404=True) for item in psc.get("items", [])]
        write("psc_detail", psc_detail)

        officer_detail = {}
        for item in officers.get("items", []):
            link = (item.get("links") or {}).get("officer", {}).get("appointments")
            if not link:
                continue
            officer_id = link.split("/")[2]
            kind = "corporate" if "identification" in item else "natural"
            officer_detail[officer_id] = {
                "name": item.get("name"),
                "appointments": ch.paged(link, allow_404=True),
                "disqualifications": ch.get(f"/disqualified-officers/{kind}/{officer_id}", allow_404=True),
            }
        write("officer_detail", officer_detail)

    saved, errors = 0, []
    if docs:
        doc_dir = os.path.join(out_dir, "documents")
        os.makedirs(doc_dir, exist_ok=True)
        for item in filings.get("items", [])[:docs]:
            ref = (item.get("links") or {}).get("document_metadata")
            if not ref:
                continue
            try:
                content, ctype = ch.document_content(ref)
            except CHError as err:
                errors.append(str(err))
                continue
            ext = "pdf" if "pdf" in ctype else "bin"
            name = safe_name(f"{item.get('date', 'nodate')}_{item.get('type', '')}_{item.get('transaction_id', '')}.{ext}")
            with open(os.path.join(doc_dir, name), "wb") as fh:
                fh.write(content)
            saved += 1
        summary["documents"] = saved

    summary["api_calls"] = ch.calls
    manifest = {"company_number": number, "folder": out_dir, "sections": summary, "document_errors": errors}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    return manifest


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ch",
        description="Read Companies House data. Every command prints JSON; 'found: false' means the API returned 404.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name, help_text, _, names, mode in ENDPOINTS:
        sp = sub.add_parser(name, help=help_text, description=help_text)
        for arg in names:
            sp.add_argument(arg, help=arg)
        sp.add_argument("--param", action="append", metavar="KEY=VALUE", help="extra query parameter, repeatable")
        if mode == "list":
            sp.add_argument("--limit", type=int, help="stop after this many items")

    sp = sub.add_parser("get", help="GET any Public Data API path, e.g. get /company/00445790/officers --paged")
    sp.add_argument("path", help="path starting with /, such as /company/00445790/charges")
    sp.add_argument("--param", action="append", metavar="KEY=VALUE")
    sp.add_argument("--paged", action="store_true", help="follow every page and merge items")
    sp.add_argument("--limit", type=int)

    sp = sub.add_parser("document", help="Document API: metadata for a filing document, or save its content")
    sp.add_argument("ref", help="document id, or the document_metadata URL from a filing-history item")
    sp.add_argument("--save", metavar="FILE", help="write the document to FILE instead of printing metadata")
    sp.add_argument("--accept", default="application/pdf", help="content type to request (default application/pdf)")

    sp = sub.add_parser("stream", help=f"Streaming API: read a few events then stop. Resources: {', '.join(STREAM_RESOURCES)}")
    sp.add_argument("resource", help="stream resource name, e.g. companies or filings")
    sp.add_argument("--timepoint", type=int, help="start from this timepoint instead of now")
    sp.add_argument("--max-events", type=int, default=10)

    sp = sub.add_parser("company-all", help="Read everything Companies House holds on one company into a folder")
    sp.add_argument("company", help="company number, e.g. 00445790 or SC123456")
    sp.add_argument("--out", help="folder to write (default ./ch-data/NUMBER)")
    sp.add_argument("--no-deep", action="store_true", help="skip per-PSC detail and per-officer appointment lookups")
    sp.add_argument("--docs", type=int, default=0, help="also download PDFs of the N most recent filings")

    return parser


def run(ch, args):
    if args.cmd in ENDPOINTS_BY_NAME:
        return run_endpoint(ch, ENDPOINTS_BY_NAME[args.cmd], args)
    if args.cmd == "get":
        params = params_from(args.param) or None
        if args.paged:
            return ch.paged(args.path, params, allow_404=True, limit=args.limit)
        return ch.get(args.path, params, allow_404=True)
    if args.cmd == "document":
        if args.save:
            content, ctype = ch.document_content(args.ref, args.accept)
            with open(args.save, "wb") as fh:
                fh.write(content)
            return {"saved": args.save, "bytes": len(content), "content_type": ctype}
        return ch.document_metadata(args.ref)
    if args.cmd == "stream":
        return {"resource": args.resource, "events": ch.stream(args.resource, args.timepoint, args.max_events)}
    if args.cmd == "company-all":
        return company_all(ch, args.company, args.out, not args.no_deep, args.docs)
    raise CHError(f"unknown command {args.cmd}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        ch = CH()
        data = run(ch, args)
        emit(data if data is not None else {"found": False})
        print(f"Companies House API calls this run: {ch.calls}", file=sys.stderr)
        return 0
    except CHError as err:
        print(f"ch: {err}", file=sys.stderr)
        return 1
    except requests.RequestException as err:
        print(f"ch: network error: {err}", file=sys.stderr)
        return 1
