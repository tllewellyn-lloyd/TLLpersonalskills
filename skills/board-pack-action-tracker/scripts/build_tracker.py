#!/usr/bin/env python3
"""
Build the standard board-pack action tracker workbook from structured JSON data.

Usage:
    python build_tracker.py data.json output.xlsx

Input JSON schema:
{
  "assumptions": ["free text assumption", ...],
  "outstanding": [
    {"action": "...", "business": "CADS", "pillar": "Sales Effectiveness",
     "owner": "Aaron Wright", "deadline": "2026-08-18"}, ...
  ],
  "removed": [
    {"action": "...", "business": "CADS", "pillar": "...", "owner": "...",
     "deadline": "...", "reason": "BAU action - ..."}, ...
  ],
  "completed": [
    {"action": "...", "business": "RMS", "pillar": "Sales Effectiveness"}, ...
  ],
  "decisions": [
    {"decision": "...", "business": "RMS", "detail": "..."}, ...
  ],
  "minutes": [
    {"source": "RMS + SIL Board Meeting (16/07/2026)", "category": "Attendees",
     "note": "..."}, ...
  ]
}

All top-level keys are optional except at least one of outstanding/completed/
decisions/minutes should be present for the workbook to be useful. Missing
keys simply produce an empty (header-only) sheet.
"""

import json
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

FONT_NAME = "Arial"
HEADER_FILL = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
HEADER_FONT = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
BODY_FONT = Font(name=FONT_NAME, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="top", horizontal="center")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Cycled through for any business/entity name encountered, in first-seen order.
# Add more if a pack regularly has >4 portfolio companies in it.
BUSINESS_PALETTE = ["FCE4D6", "D9E1F2", "E2EFDA", "FFF2CC", "EAD1DC", "D9D2E9"]


def business_fill_map(*record_lists):
    """Assign a stable fill color to each distinct business value encountered."""
    seen = []
    for records in record_lists:
        for rec in records:
            b = rec.get("business")
            if b and b not in seen:
                seen.append(b)
    return {
        b: PatternFill(start_color=c, end_color=c, fill_type="solid")
        for b, c in zip(seen, BUSINESS_PALETTE * (len(seen) // len(BUSINESS_PALETTE) + 1))
    }


def style_header(ws, ncols, row=1):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left")
        cell.border = BORDER
    ws.freeze_panes = ws.cell(row=row + 1, column=1).coordinate
    ws.auto_filter.ref = ws.dimensions


def write_table(ws, headers, rows, business_col=None, fills=None, center_cols=None):
    ws.append(headers)
    r = 2
    center_cols = center_cols or []
    for row in rows:
        for c, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = BODY_FONT
            cell.alignment = WRAP_CENTER if c in center_cols else WRAP
            cell.border = BORDER
        if business_col and fills:
            biz = row[business_col - 1]
            fill = fills.get(biz)
            if fill:
                ws.cell(row=r, column=business_col).fill = fill
        r += 1
    style_header(ws, len(headers))
    return r


def autosize(ws, widths):
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def build(data: dict, out_path: str):
    wb = openpyxl.Workbook()

    outstanding = data.get("outstanding", [])
    removed = data.get("removed", [])
    completed = data.get("completed", [])
    decisions = data.get("decisions", [])
    minutes = data.get("minutes", [])
    assumptions = data.get("assumptions", [])

    fills = business_fill_map(outstanding, removed, completed)

    # Assumptions (first sheet)
    ws = wb.active
    ws.title = "Assumptions"
    write_table(ws, ["Assumption"], [[a] for a in assumptions])
    autosize(ws, {"A": 130})
    for r in range(2, len(assumptions) + 2):
        ws.row_dimensions[r].height = 30

    # Outstanding Actions
    ws1 = wb.create_sheet("Outstanding Actions")
    rows = [[o["action"], o["business"], o["pillar"], o["owner"], o["deadline"]] for o in outstanding]
    write_table(ws1, ["Action", "Business", "VC Pillar", "Owner", "Deadline"], rows,
                business_col=2, fills=fills, center_cols=[4, 5])
    autosize(ws1, {"A": 78, "B": 10, "C": 20, "D": 18, "E": 13})

    # Removed Actions
    ws2 = wb.create_sheet("Removed Actions")
    rows = [[o["action"], o["business"], o["pillar"], o["owner"], o["deadline"], o["reason"]] for o in removed]
    write_table(ws2, ["Action", "Business", "VC Pillar", "Owner", "Deadline", "Reason for removal"], rows,
                business_col=2, fills=fills, center_cols=[4, 5])
    autosize(ws2, {"A": 78, "B": 10, "C": 20, "D": 18, "E": 13, "F": 55})

    # Completed Actions
    ws3 = wb.create_sheet("Completed Actions")
    rows = [[o["action"], o["business"], o["pillar"]] for o in completed]
    write_table(ws3, ["Action", "Business", "VC Pillar"], rows, business_col=2, fills=fills)
    autosize(ws3, {"A": 90, "B": 10, "C": 20})

    # Decisions Made
    ws4 = wb.create_sheet("Decisions Made")
    rows = [[o["decision"], o["business"], o["detail"]] for o in decisions]
    write_table(ws4, ["Decision", "Business", "Detail"], rows, business_col=2, fills=fills)
    autosize(ws4, {"A": 32, "B": 10, "C": 90})

    # Minutes & Context
    ws5 = wb.create_sheet("Minutes & Context")
    rows = [[o["source"], o["category"], o["note"]] for o in minutes]
    write_table(ws5, ["Source", "Category", "Note"], rows)
    autosize(ws5, {"A": 34, "B": 22, "C": 95})

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return out_path


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_tracker.py <data.json> <output.xlsx>")
        sys.exit(1)
    data_path, out_path = sys.argv[1], sys.argv[2]
    with open(data_path) as f:
        data = json.load(f)
    path = build(data, out_path)
    print(f"saved {path}")
    print(f"  outstanding: {len(data.get('outstanding', []))}")
    print(f"  removed:     {len(data.get('removed', []))}")
    print(f"  completed:   {len(data.get('completed', []))}")
    print(f"  decisions:   {len(data.get('decisions', []))}")
    print(f"  minutes:     {len(data.get('minutes', []))}")


if __name__ == "__main__":
    main()
