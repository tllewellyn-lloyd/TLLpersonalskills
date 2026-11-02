#!/usr/bin/env python3
"""
Populate a user-supplied employee-contract-review template from extracted data.

Usage:
    python3 build_review.py <template.xlsx> <data.json> <output.xlsx> [--sheet SheetName] [--header-row N]

- Reads the template's header row to discover the field columns (works with ANY template).
- Matches each field in the JSON to a template column by normalised header text (case/space/
  punctuation-insensitive, with employment-specific aliases), so you don't hard-code column letters.
- Writes one row per EMPLOYEE. Rows are matched to existing template rows by the Name key if present
  (so pre-filled columns like "Name" and "Dataroom Ref" are PRESERVED, not overwritten); otherwise
  rows are appended. Employees you omit stay blank; that's expected for people with no documents.
- Colour-codes a "Satisfactory?" column (green = satisfactory, amber = investigate) if present.
- Applies light formatting: bold header, wrapped text, frozen header row, sensible widths/heights.

data.json format:
{
  "row_key_header": "Name",                 # header used to match rows to the template (default "Name")
  "rows": [
     { "Name": "Employee 1",                # values keyed by TEMPLATE header text (or an alias)
       "Type": "Standard ...",
       "Salary (per annum)": "£33,750 ...",
       "Satisfactory?": "Investigate",
       ... one key per field you want to write ...
     },
     ...
  ]
}
Only keys that map to a template column are written; unknown keys are reported and skipped.
Columns you omit for a row are left as-is (pre-filled data is preserved).
"""
import sys, json, re
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def norm(s):
    if s is None:
        return ""
    s = str(s).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

# alias groups -> slightly different template wording still matches the same field
ALIASES = {
    "name": ["employee", "employee name", "staff member"],
    "type": ["contract type", "type of contract"],
    "document name": ["documents", "document names", "files", "file name", "source documents"],
    "dataroom ref": ["data room ref", "dataroom reference", "ref"],
    "date signed": ["signed", "signature date", "dates signed", "execution"],
    "signature redaction status": ["redaction", "redaction status", "signature redaction"],
    "commencement date": ["start date", "start", "commencement", "date employment started"],
    "job title": ["title", "role", "position"],
    "salary per annum": ["salary", "salary pa", "annual salary", "salary per year", "gross salary"],
    "payment date": ["pay date", "salary payment date", "payment day"],
    "commission additional payments": ["commission", "bonus", "additional payments",
                                       "commission bonus", "commission additional payments"],
    "pension": ["pension contribution", "pension scheme"],
    "benefits": ["other benefits", "company benefits"],
    "hours": ["working hours", "hours of work"],
    "holidays": ["holiday", "holiday entitlement", "annual leave", "leave"],
    "sick pay": ["sickness", "sick pay ssp", "sickness absence"],
    "restrictive covenants": ["covenants", "non compete", "non solicitation",
                              "post termination restrictions", "restrictive covenant"],
    "confidentiality": ["confidential", "confidentiality clause"],
    "notice period": ["notice", "notice period employer terminating and employee terminating",
                      "notice periods"],
    "termination conditions": ["termination", "termination clause", "termination conditions"],
    "ip": ["intellectual property", "ipr", "ip ownership", "intellectual property rights"],
    "data protection": ["gdpr", "data protection dp", "data privacy"],
    "governing law": ["law", "jurisdiction", "governing law and jurisdiction"],
    "redundancy pay": ["redundancy", "redundancy pay statutory or enhanced"],
    "comments": ["comment", "notes", "summary"],
    "outstanding points": ["outstanding", "open points", "queries", "follow up"],
    "satisfactory": ["satisfactory?", "satisfactory or investigate", "verdict", "status"],
}
ALIAS_TO_CANON = {}
for c, al in ALIASES.items():
    ALIAS_TO_CANON[c] = c
    for a in al:
        ALIAS_TO_CANON[norm(a)] = c

def canon(h):
    return ALIAS_TO_CANON.get(norm(h), norm(h))

def find_header_row(ws, hint=None):
    if hint:
        return hint
    for r in range(1, 6):
        vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        nonempty = [v for v in vals if isinstance(v, str) and v.strip()]
        if len(nonempty) >= 3:
            return r
    return 1

def main():
    args = list(sys.argv[1:])
    if len(args) < 3:
        print(__doc__); sys.exit(1)
    template, data_path, out_path = args[0], args[1], args[2]
    sheet = args[args.index("--sheet") + 1] if "--sheet" in args else None
    header_row = int(args[args.index("--header-row") + 1]) if "--header-row" in args else None

    with open(data_path) as f:
        data = json.load(f)
    rows = data.get("rows", [])
    row_key_header = data.get("row_key_header", "Name")

    wb = openpyxl.load_workbook(template)
    ws = wb[sheet] if sheet else wb.active
    hr = find_header_row(ws, header_row)

    col_by_canon, headers = {}, {}
    for c in range(1, ws.max_column + 1):
        h = ws.cell(row=hr, column=c).value
        if isinstance(h, str) and h.strip():
            col_by_canon[canon(h)] = c
            headers[c] = h

    key_col = col_by_canon.get(canon(row_key_header)) if row_key_header else None
    sat_col = col_by_canon.get("satisfactory")
    existing = {}
    if key_col:
        for r in range(hr + 1, ws.max_row + 1):
            v = ws.cell(row=r, column=key_col).value
            if isinstance(v, str) and v.strip():
                existing[norm(v)] = r

    unmatched, next_row, written = set(), ws.max_row + 1, 0
    for rec in rows:
        r = None
        if key_col and rec.get(row_key_header):
            r = existing.get(norm(rec[row_key_header]))
        if r is None:
            r = next_row; next_row += 1
        for k, val in rec.items():
            col = col_by_canon.get(canon(k))
            if not col:
                unmatched.add(k); continue
            if col == key_col and ws.cell(row=r, column=col).value:
                continue  # never overwrite a pre-filled Name
            ws.cell(row=r, column=col).value = val
        written += 1

    # formatting
    wrap = Alignment(wrap_text=True, vertical="top")
    last_row, last_col = ws.max_row, ws.max_column
    for r in range(hr + 1, last_row + 1):
        for c in range(1, last_col + 1):
            ws.cell(row=r, column=c).alignment = wrap
    hdr_fill = PatternFill("solid", fgColor="1F3864")
    hdr_font = Font(bold=True, color="FFFFFF", size=10)
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c in range(1, last_col + 1):
        cell = ws.cell(row=hr, column=c)
        cell.fill = hdr_fill; cell.font = hdr_font
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for r in range(hr, last_row + 1):
        for c in range(1, last_col + 1):
            ws.cell(row=r, column=c).border = border
    for c in range(1, last_col + 1):
        ws.column_dimensions[get_column_letter(c)].width = 40
    ws.row_dimensions[hr].height = 42
    for r in range(hr + 1, last_row + 1):
        ws.row_dimensions[r].height = 200

    # colour-code the Satisfactory column
    if sat_col:
        for r in range(hr + 1, last_row + 1):
            v = ws.cell(row=r, column=sat_col).value
            if not isinstance(v, str):
                continue
            if "investigat" in v.lower():
                ws.cell(row=r, column=sat_col).fill = PatternFill("solid", fgColor="FFF2CC")
                ws.cell(row=r, column=sat_col).font = Font(bold=True, color="BF8F00", size=10)
            elif "satisf" in v.lower():
                ws.cell(row=r, column=sat_col).fill = PatternFill("solid", fgColor="E2EFDA")
                ws.cell(row=r, column=sat_col).font = Font(bold=True, color="548235", size=10)

    ws.freeze_panes = ws.cell(row=hr + 1, column=2).coordinate
    wb.save(out_path)
    print(f"Wrote {written} row(s) to {out_path} (header row {hr}).")
    if unmatched:
        print("WARNING: these data keys did not match any template column and were skipped:")
        for k in sorted(unmatched):
            print("  -", k)

if __name__ == "__main__":
    main()
