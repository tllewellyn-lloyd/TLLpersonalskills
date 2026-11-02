#!/usr/bin/env python3
"""
build_excel.py — Creates the SPA Review Excel spreadsheet for Tern Capital.

Usage:
    python build_excel.py --data <path_to_issues.json> --output <output_path.xlsx> [--deal-name "Company Name"]

Input JSON format:
    [
        {
            "clause": "Clause 6.2",
            "issue": "Seller requests basket be increased from 0.25% to 2.0% of completion consideration.",
            "response": "Reject — Tern's position is 0.25% CC. We may accept 0.5% as a compromise but no higher.",
            "status": "Reject"
        },
        ...
    ]

Status values: "Reject", "Accept", "Negotiate", "Needs review"
"""

import json
import sys
import argparse
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("Installing openpyxl...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "--break-system-packages", "-q"])
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter


STATUS_FILLS = {
    "Reject":       PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid"),
    "Accept":       PatternFill(start_color="CCFFCC", end_color="CCFFCC", fill_type="solid"),
    "Negotiate":    PatternFill(start_color="FFFACC", end_color="FFFACC", fill_type="solid"),
    "Needs review": PatternFill(start_color="FFE5CC", end_color="FFE5CC", fill_type="solid"),
}

HEADER_FILL = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
BODY_FONT = Font(name="Calibri", size=10)

THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)

COLUMNS = [
    ("Clause / Schedule Reference", 22),
    ("Issue Raised by Seller",       55),
    ("Tern's Proposed Response",     60),
    ("Accept / Reject / Negotiate",  20),
]


def build(issues: list, output_path: str, deal_name: str = "") -> str:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SPA Review"

    # Title row
    title = f"SPA Review{' — ' + deal_name if deal_name else ''}"
    ws.merge_cells("A1:D1")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.font = Font(bold=True, name="Calibri", size=13, color="1F3864")
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 22

    # Header row
    for col_idx, (header, width) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=2, column=col_idx, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.row_dimensions[2].height = 28

    # Freeze header rows
    ws.freeze_panes = "A3"

    # Data rows
    for row_idx, issue in enumerate(issues, start=3):
        clause   = issue.get("clause", "")
        seller   = issue.get("issue", "")
        response = issue.get("response", "")
        status   = issue.get("status", "Negotiate")

        row_data = [clause, seller, response, status]
        status_fill = STATUS_FILLS.get(status, STATUS_FILLS["Negotiate"])

        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = BODY_FONT
            cell.fill = status_fill
            cell.border = THIN_BORDER
            cell.alignment = Alignment(
                wrap_text=True,
                vertical="top",
                horizontal="left" if col_idx < 4 else "center",
            )

        # Auto-height hint (openpyxl doesn't auto-calc, so set a generous minimum)
        ws.row_dimensions[row_idx].height = max(40, min(150, 15 * max(1, len(seller) // 60)))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    print(f"Saved: {output_path}")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Build SPA Review Excel from JSON issues list")
    parser.add_argument("--data", required=True, help="Path to issues JSON file")
    parser.add_argument("--output", required=True, help="Output .xlsx path")
    parser.add_argument("--deal-name", default="", help="Deal / company name for title")
    args = parser.parse_args()

    with open(args.data) as f:
        issues = json.load(f)

    build(issues, args.output, args.deal_name)


if __name__ == "__main__":
    main()
