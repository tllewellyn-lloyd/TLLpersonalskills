#!/usr/bin/env python3
"""
Populate a user-supplied contract-review template from extracted contract data.

Usage:
    python3 build_review.py <template.xlsx> <data.json> <output.xlsx> [--sheet SheetName] [--header-row N]

- Reads the template's header row to discover the field columns (works with ANY template).
- Matches each field in the JSON to a template column by normalised header text
  (case/space/punctuation-insensitive, with common aliases), so you don't have to hard-code
  column letters.
- Writes one row per contract. Rows are matched to existing template rows by the customer/row key
  if present (so pre-filled columns like "Customer name" and "Dataroom Ref" are PRESERVED and not
  overwritten); otherwise rows are appended.
- Applies light formatting: bold header, wrapped text, frozen header row, sensible widths/heights.

data.json format:
{
  "row_key_header": "Customer name",         # optional: header used to match rows to the template
  "rows": [
     { "Customer name": "ACME ICB",          # values keyed by TEMPLATE header text (or an alias)
       "File name": "acme.pdf",
       "Status": "Reviewed",
       "Recalculated ARR": "£123,000 p.a. ...",
       ... one key per field you want to write ...
     },
     ...
  ]
}
Only keys that map to a template column are written; unknown keys are reported and skipped.
Columns you omit for a row are left as they are in the template (pre-filled data is preserved).
"""
import sys, json, re
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def norm(s):
    if s is None:
        return ""
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return s

# common alias groups -> all normalise to the same key so slightly different template wording matches
ALIASES = {
    "file name": ["file", "filename", "document", "file names"],
    "status": ["review status"],
    "contract type": ["type", "type of contract"],
    "start date": ["commencement date", "start"],
    "duration": ["term", "length", "contract length"],
    "end date": ["expiry date", "expiry", "end"],
    "latest date for price increase notification": ["price increase notification", "price rise notice"],
    "auto renewal clause": ["auto renewal", "automatic renewal", "renewal"],
    "termination notification deadline": ["termination notice", "notice to terminate"],
    "total contractual pricing rate card": ["total contractual pricing", "pricing", "rate card", "total pricing"],
    "recalculated arr": ["arr", "recalculated arr", "annual recurring revenue"],
    "governing law": ["law", "jurisdiction", "governing law and jurisdiction"],
    "licence": ["license", "licence non exclusive non transferable"],
    "services products": ["services", "products", "services products"],
    "assignment clause": ["assignment"],
    "termination": ["termination clause"],
    "change of control notification required": ["change of control", "coc", "change of control notification"],
    "payment terms": ["payment", "invoice terms"],
    "price increase terms": ["price increase", "price increases", "price increase term"],
    "data protection": ["gdpr", "data protection dp"],
    "warranties indemnities": ["warranties", "indemnities", "warranties indemnities"],
    "intellectual property": ["ip", "ipr", "intellectual property rights"],
    "limitation of liability": ["liability", "liability cap", "limitation of liability"],
    "insurance requirements": ["insurance"],
    "sla penalties": ["sla", "penalties", "service levels", "sla penalties"],
    "new releases software updates": ["new releases", "software updates", "updates"],
    "escrow agreement": ["escrow"],
    "comments": ["comment", "notes"],
    "signed": ["signed", "signed by both parties", "execution", "executed"],
    "outstanding points": ["outstanding", "outstanding points", "open points", "queries"],
}
# reverse map: normalised alias -> canonical normalised header
ALIAS_TO_CANON = {}
for canon, al in ALIASES.items():
    ALIAS_TO_CANON[canon] = canon
    for a in al:
        ALIAS_TO_CANON[norm(a)] = canon

def canon(h):
    n = norm(h)
    return ALIAS_TO_CANON.get(n, n)

def find_header_row(ws, hint=None):
    if hint:
        return hint
    # pick the first row (within first 5) that has >=3 non-empty string cells
    for r in range(1, 6):
        vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        nonempty = [v for v in vals if isinstance(v, str) and v.strip()]
        if len(nonempty) >= 3:
            return r
    return 1

def main():
    args = [a for a in sys.argv[1:]]
    if len(args) < 3:
        print(__doc__); sys.exit(1)
    template, data_path, out_path = args[0], args[1], args[2]
    sheet = None; header_row = None
    if "--sheet" in args:
        sheet = args[args.index("--sheet") + 1]
    if "--header-row" in args:
        header_row = int(args[args.index("--header-row") + 1])

    with open(data_path) as f:
        data = json.load(f)
    rows = data.get("rows", [])
    row_key_header = data.get("row_key_header")

    wb = openpyxl.load_workbook(template)
    ws = wb[sheet] if sheet else wb.active
    hr = find_header_row(ws, header_row)

    # map canonical header -> column index
    col_by_canon = {}
    headers = {}
    for c in range(1, ws.max_column + 1):
        h = ws.cell(row=hr, column=c).value
        if isinstance(h, str) and h.strip():
            col_by_canon[canon(h)] = c
            headers[c] = h

    # build lookup of existing rows by row-key value (to preserve pre-filled columns)
    key_col = col_by_canon.get(canon(row_key_header)) if row_key_header else None
    existing = {}
    if key_col:
        for r in range(hr + 1, ws.max_row + 1):
            v = ws.cell(row=r, column=key_col).value
            if isinstance(v, str) and v.strip():
                existing[norm(v)] = r

    unmatched_keys = set()
    next_row = ws.max_row + 1
    written = 0
    for rec in rows:
        # decide target row
        r = None
        if key_col and row_key_header and rec.get(row_key_header):
            r = existing.get(norm(rec[row_key_header]))
        if r is None:
            r = next_row; next_row += 1
        for k, val in rec.items():
            cc = canon(k)
            col = col_by_canon.get(cc)
            if not col:
                unmatched_keys.add(k); continue
            # never overwrite the row-key column itself if it is already filled
            if col == key_col and ws.cell(row=r, column=col).value:
                continue
            ws.cell(row=r, column=col).value = val
        written += 1

    # formatting
    wrap = Alignment(wrap_text=True, vertical="top")
    last_row = ws.max_row
    last_col = ws.max_column
    for r in range(hr + 1, last_row + 1):
        for c in range(1, last_col + 1):
            ws.cell(row=r, column=c).alignment = wrap
    hdr_fill = PatternFill("solid", fgColor="1F3864")
    hdr_font = Font(bold=True, color="FFFFFF", size=10)
    hdr_align = Alignment(wrap_text=True, vertical="center", horizontal="center")
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c in range(1, last_col + 1):
        cell = ws.cell(row=hr, column=c)
        cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = hdr_align
    for r in range(hr, last_row + 1):
        for c in range(1, last_col + 1):
            ws.cell(row=r, column=c).border = border
    for c in range(1, last_col + 1):
        ws.column_dimensions[get_column_letter(c)].width = 40
    ws.row_dimensions[hr].height = 42
    for r in range(hr + 1, last_row + 1):
        ws.row_dimensions[r].height = 220
    ws.freeze_panes = ws.cell(row=hr + 1, column=2).coordinate

    wb.save(out_path)
    print(f"Wrote {written} row(s) to {out_path} (header row {hr}).")
    if unmatched_keys:
        print("WARNING: these data keys did not match any template column and were skipped:")
        for k in sorted(unmatched_keys):
            print("  -", k)
    # report any empty data cells for visibility
    empties = []
    for r in range(hr + 1, last_row + 1):
        for c in range(1, last_col + 1):
            v = ws.cell(row=r, column=c).value
            if v is None or (isinstance(v, str) and not v.strip()):
                empties.append(f"{get_column_letter(c)}{r} ({headers.get(c,'?')})")
    if empties:
        print(f"NOTE: {len(empties)} empty cell(s) remain — verify these are intentional:")
        for e in empties[:40]:
            print("  -", e)

if __name__ == "__main__":
    main()
