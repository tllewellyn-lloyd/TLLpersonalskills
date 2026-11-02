#!/usr/bin/env python3
"""Audit a Tern Capital DD model workbook against house conventions.

Usage: python audit_model.py "Target Master.xlsx"

Checks (FAIL = must fix before delivery, WARN = judgement call):
  1. Legend exists and lists every tab; no phantom Legend entries    FAIL
  2. Physical tab order matches Legend order                         FAIL
  3. No default-named tabs (Sheet1, Copy of..., Lookup (1), ...)     FAIL
  4. Every tab has at least one 'x' section marker                   WARN
  5. Column A used only for section markers                          WARN
  6. Legend Comments/Questions column has at least some entries      WARN
  7. PL tab has a Check row                                          WARN
  8. No external-file references in formulas ([Book1.xlsx]...)       FAIL

Exit code 1 if any FAIL. Formula *values* can't be checked here (openpyxl
doesn't calculate) - recalc by opening the file or via LibreOffice headless.
"""
import re
import sys
from openpyxl import load_workbook

DEFAULT_NAMES = re.compile(r"^(Sheet\d+|Copy of .*|Lookup( \(\d+\))?|.*\(\d+\))$", re.I)


def main(path):
    wb = load_workbook(path)
    fails, warns = [], []

    # Legend
    if "L" not in wb.sheetnames:
        fails.append("No 'L' (Legend) tab")
        legend_codes = []
    else:
        ws = wb["L"]
        legend_codes, comments = [], 0
        header_row = None
        for row in ws.iter_rows(min_col=2, max_col=6, max_row=80):
            vals = [c.value for c in row]
            if vals[0] == "Sheet":
                header_row = row[0].row
                continue
            if header_row and vals[0] and isinstance(vals[0], str):
                if any(vals[0].startswith(p) for p in ("Change log", "Section index", "Dataroom index")):
                    break
                legend_codes.append(vals[0].strip())
                if vals[4]:
                    comments += 1
        if not legend_codes:
            fails.append("Legend tab map is empty or header row 'Sheet' not found")
        if comments == 0:
            warns.append("Legend Comments/Questions column is completely blank")

    sheets = wb.sheetnames
    for code in legend_codes:
        if code not in sheets:
            fails.append(f"Legend lists '{code}' but no such tab exists")
    for s in sheets:
        if legend_codes and s not in legend_codes:
            fails.append(f"Tab '{s}' missing from Legend")
    if legend_codes:
        in_both = [s for s in sheets if s in legend_codes]
        expected = [c for c in legend_codes if c in sheets]
        if in_both != expected:
            fails.append(f"Tab order {in_both} != Legend order {expected}")

    for s in sheets:
        if DEFAULT_NAMES.match(s):
            fails.append(f"Default/copy-named tab: '{s}' - rename and log in Legend")

    ext_ref = re.compile(r"\[[^\]]+\.xls[xmb]?\]")
    for s in sheets:
        ws = wb[s]
        has_marker, bad_a = False, 0
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if c.column == 1 and v is not None:
                    if str(v).strip().lower() == "x":
                        has_marker = True
                    else:
                        bad_a += 1
                if isinstance(v, str) and v.startswith("=") and ext_ref.search(v):
                    fails.append(f"External file reference in {s}!{c.coordinate}")
        if not has_marker:
            warns.append(f"Tab '{s}' has no 'x' section markers")
        if bad_a:
            warns.append(f"Tab '{s}': {bad_a} non-marker value(s) in column A")

    if "PL" in sheets:
        pl_text = " ".join(str(c.value) for row in wb["PL"].iter_rows(min_col=2, max_col=2)
                           for c in row if c.value)
        if "Check" not in pl_text:
            warns.append("PL tab has no Check row")

    for f in fails:
        print(f"FAIL  {f}")
    for w in warns:
        print(f"WARN  {w}")
    if not fails and not warns:
        print("OK    All checks passed")
    print(f"\n{len(fails)} fail(s), {len(warns)} warn(s). "
          "Remember: recalc the workbook to verify formula values - this audit checks structure only.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
