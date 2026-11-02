#!/usr/bin/env python3
"""Scaffold a Tern Capital DD model workbook.

Creates <Target> Master.xlsx with: Legend (L) tab wired to the chosen tab
list (tab map only), tab colours by group, QA tab skeleton, and the
standard PL skeleton (full line taxonomy, formula subtotals, Tern Y1 PL
and its comment column, Check row). Section headers have yellow
background fill.

Usage:
    python scaffold_model.py --config scaffold_config.json --output "Target Master.xlsx"

Config schema (JSON):
{
  "deal_name": "Asset Guardian",
  "tabs": [                       // in desired physical order; L, QA auto-added if omitted
    {"code": "PL", "description": "Tern Y1 PL and historic financials", "group": "Finance"},
    {"code": "CB", "description": "Compensation and benefits", "group": "Finance"},
    {"code": "R",  "description": "Revenue", "group": "Revenue"}
  ],
  "historic_columns": [           // left-to-right on the PL tab; include the
    {"label": "FY2024A"},         // seller's forecast years as well as actuals
    {"label": "FY2025A"},
    {"label": "FY2026A"},
    {"label": "FY2027F"}
  ],
  "year_end": "31st May YE"       // shown in PL!C3
}

Group -> tab colour: Finance=green, Commercial=red, Revenue=pink, Other=blue.
Font convention: blue=input, black=formula, green=cross-sheet link.

House style (MASTER_template_PL.xlsx): Nunito 11 throughout; section header
rows yellow FFFF00; table column headers orange F79646 with white bold text;
subtotal rows grey EFEFEF bold. Financial tabs are held in GBP FULL UNITS and
formatted #,##0,"K" - restate seller data given in GBP '000 by x1,000 on
ingestion, or the trailing comma scales it a second time.
"""
import argparse
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

TAB_COLOURS = {"Finance": "00B050", "Commercial": "FF0000",
               "Revenue": "FF66CC", "Other": "00B0F0"}

# House style, per MASTER_template_PL.xlsx
FONT = "Nunito"
FONT_SIZE = 11
BLUE = Font(name=FONT, size=FONT_SIZE, color="0000FF")            # input
BLUE_B = Font(name=FONT, size=FONT_SIZE, color="0000FF", bold=True)
BOLD = Font(name=FONT, size=FONT_SIZE, bold=True)
PLAIN = Font(name=FONT, size=FONT_SIZE)
HDR = Font(name=FONT, size=FONT_SIZE, bold=True, color="FFFFFF")  # on orange
YELLOW = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
HDRFILL = PatternFill(start_color="F79646", end_color="F79646", fill_type="solid")
GREYFILL = PatternFill(start_color="EFEFEF", end_color="EFEFEF", fill_type="solid")
# Financial tabs are held in GBP FULL UNITS - the trailing comma scales by
# 1,000. Seller data given in GBP '000 must be restated x1,000 on ingestion.
KFMT = '#,##0,"K"'
KFMT1 = '#,##0.0,"K"'     # Tern check / reconciliation rows only
PCTFMT = "0.00%"


def style_header(ws, row, cols):
    """Table column header: orange fill, white bold text, right-aligned."""
    for ci in cols:
        c = ws.cell(row=row, column=ci)
        if c.value is None:
            continue
        c.font = HDR
        c.fill = HDRFILL


def style_subtotal(ws, row, first_col=2, last_col=15):
    """Subtotal / total row: bold on light grey."""
    for ci in range(first_col, last_col + 1):
        c = ws.cell(row=row, column=ci)
        c.fill = GREYFILL
        c.font = BOLD


def apply_house_font(wb):
    """Force Nunito 11 everywhere, preserving bold/italic/colour."""
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        for row in ws.iter_rows():
            for c in row:
                o = c.font
                c.font = Font(name=FONT, size=FONT_SIZE, bold=o.bold,
                              italic=o.italic, color=o.color,
                              underline=o.underline)

REVENUE_LINES = [
    ("Turnover - Recurring - Software", "Recurring Revenue"),
    ("Turnover - Recurring - Maintenance", "Recurring Revenue"),
    ("Turnover - Recurring - Managed Services", "Recurring Revenue"),
    ("Turnover - Recurring - Transactions", "Recurring Revenue"),
    ("Turnover - Non-Recurring - Software", "Non-Recurring Revenue"),
    ("Turnover - Non-Recurring - Prof Services", "Non-Recurring Revenue"),
    ("Turnover - Non-Recurring - Hardware", "Non-Recurring Revenue"),
    ("Turnover - Non-Recurring - Other income", "Non-Recurring Revenue"),
]
COGS_LINES = [
    ("COGS - Recurring - Software", "Recurring Cost of Sales"),
    ("COGS - Recurring - Maintenance", "Recurring Cost of Sales"),
    ("COGS - Recurring - Managed Services", "Recurring Cost of Sales"),
    ("COGS - Recurring - Transactions", "Recurring Cost of Sales"),
    ("COGS - Non-Recurring - Software", "Non-Recurring Cost of Sales"),
    ("COGS - Non-Recurring - Prof Services", "Non-Recurring Cost of Sales"),
    ("COGS - Non-Recurring - Hardware", "Non-Recurring Cost of Sales"),
    ("COGS - Indirect", "COS - Indirect"),
]
OVERHEAD_LINES = [
    ("C&B", "C&B - Staff"), ("Contractors", "C&B - Contractors"),
    ("Recruitment", "Recruitment"), ("Professional Fees", "Professional Fees"),
    ("Marketing", "Marketing"), ("IT & Systems", "IT & Software"),
    ("Insurance", "Insurance"), ("Property", "Property"),
    ("Travel & Subsistence", "Other"), ("Interest expense", ""),
    ("Depreciation", ""), ("Amortisation", ""), ("Other", "Other"),
]


def section(ws, row, title, level=0):
    """Write an x section marker with yellow fill. level 0 -> col A/B, level 1 -> col B/C."""
    ws.cell(row=row, column=1 + level, value="x")
    c = ws.cell(row=row, column=2 + level, value=title)
    c.font = BOLD
    for ci in range(1, 16):
        ws.cell(row=row, column=ci).fill = YELLOW
    return row + 1


def build_legend(ws, tabs, deal_name):
    """Legend is the tab map and nothing else - keep it to one screen."""
    ws.sheet_properties.tabColor = TAB_COLOURS["Other"]
    title = f"{deal_name} - Tern Capital DD master model" if deal_name \
        else "Tern Capital DD master model"
    r = section(ws, 1, title)
    r += 1                      # blank row between the title and the table
    headers = ["Sheet", "Grouping", "Description", "Colour", "Comments/Questions"]
    for i, h in enumerate(headers):
        ws.cell(row=r, column=2 + i, value=h).font = BOLD
    style_header(ws, r, range(2, 2 + len(headers)))
    r += 1
    for t in tabs:
        ws.cell(row=r, column=2, value=t["code"]).font = BOLD
        ws.cell(row=r, column=3, value=t["group"] if t["code"] != "L" else None)
        desc = "Legend - this sheet" if t["code"] == "L" else t["description"]
        ws.cell(row=r, column=4, value=desc)
        if t["code"] != "L":
            hexcode = TAB_COLOURS[t["group"]]
            colour_name = {"00B050": "Green", "FF0000": "Red",
                           "FF66CC": "Pink", "00B0F0": "Blue"}[hexcode]
            # the Colour cell is written IN that colour
            c = ws.cell(row=r, column=5, value=colour_name)
            c.font = Font(name=FONT, size=FONT_SIZE, bold=True, color=hexcode)
        r += 1
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 52
    ws.column_dimensions["E"].width = 10
    ws.column_dimensions["F"].width = 62


def build_pl(ws, historic_columns, year_end=None):
    ws.sheet_properties.tabColor = TAB_COLOURS["Finance"]
    n_hist = len(historic_columns)
    # Column layout: A=x, B=line, C=Grouping, D..=historics, gap, Tern Y1,
    # Comments. Nothing to the right of the Y1 comment column.
    first_hist = 4
    col_y1 = first_hist + n_hist + 1
    col_y1c = col_y1 + 1
    last_col = col_y1c

    r = section(ws, 1, "P&L")
    r += 1
    # row 3 carries the financial year end, nothing else
    if year_end:
        ws.cell(row=r, column=3, value=year_end).font = BOLD
    r += 1
    hdr_row = r
    ws.cell(row=r, column=3, value="Grouping").font = BOLD
    for i, hc in enumerate(historic_columns):
        ws.cell(row=r, column=first_hist + i, value=hc["label"]).font = BOLD
    ws.cell(row=r, column=col_y1, value="Tern Y1 PL").font = BOLD
    ws.cell(row=r, column=col_y1c, value="Comments - Tern Y1 basis").font = BOLD
    style_header(ws, r, range(3, col_y1c + 1))
    r += 1

    value_cols = [first_hist + i for i in range(n_hist)] + [col_y1]

    def diff_formula(row):
        return None     # Difference columns removed - PL ends at the Y1 comment

    def line_rows(lines):
        start = r_holder[0]
        for name, mapping in lines:
            rr = r_holder[0]
            ws.cell(row=rr, column=2, value=name)
            if mapping:
                ws.cell(row=rr, column=3, value=mapping)
            for c in value_cols:
                cell = ws.cell(row=rr, column=c, value=0)
                cell.font = BLUE
                cell.number_format = KFMT
            diff_formula(rr)
            r_holder[0] += 1
        return start, r_holder[0] - 1

    subtotal_rows = []

    def total_row(label, start, end):
        rr = r_holder[0]
        ws.cell(row=rr, column=2, value=label).font = BOLD
        for c in value_cols:
            L = get_column_letter(c)
            cell = ws.cell(row=rr, column=c, value=f"=SUM({L}{start}:{L}{end})")
            cell.font = BOLD
            cell.number_format = KFMT
        diff_formula(rr)
        subtotal_rows.append(rr)
        r_holder[0] += 1
        return rr

    r_holder = [r]
    rev_s, rev_e = line_rows(REVENUE_LINES)
    total_rev = total_row("Total Revenue", rev_s, rev_e)
    # YoY growth row
    rr = r_holder[0]
    for i in range(1, n_hist):
        c = first_hist + i
        L, P = get_column_letter(c), get_column_letter(c - 1)
        cell = ws.cell(row=rr, column=c,
                       value=f"=IFERROR({L}{total_rev}/{P}{total_rev}-1,\"\")")
        cell.number_format = PCTFMT
    r_holder[0] += 2

    cogs_s, cogs_e = line_rows(COGS_LINES)
    total_cogs = total_row("Total COGS", cogs_s, cogs_e)
    r_holder[0] += 1

    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="Net Revenue/Gross Profit").font = BOLD
    for c in value_cols:
        L = get_column_letter(c)
        cell = ws.cell(row=rr, column=c, value=f"={L}{total_rev}+{L}{total_cogs}")
        cell.font = BOLD
        cell.number_format = KFMT
    gp_row = rr
    diff_formula(rr)
    r_holder[0] += 1
    rr = r_holder[0]
    for c in value_cols:
        L = get_column_letter(c)
        cell = ws.cell(row=rr, column=c, value=f"=IFERROR({L}{gp_row}/{L}{total_rev},\"\")")
        cell.number_format = PCTFMT
    r_holder[0] += 2

    oh_s, oh_e = line_rows(OVERHEAD_LINES)
    total_oh = total_row("Total Overheads", oh_s, oh_e)
    # remember rows of interest/dep/amort inside overheads
    int_row = oh_s + 9
    dep_row = oh_s + 10
    amo_row = oh_s + 11

    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="Profit Before Taxes (PBT/EBT)").font = BOLD
    for c in value_cols:
        L = get_column_letter(c)
        cell = ws.cell(row=rr, column=c, value=f"={L}{gp_row}+{L}{total_oh}")
        cell.font = BOLD
        cell.number_format = KFMT
    pbt_row = rr
    diff_formula(rr)
    r_holder[0] += 1

    addback_src = [("Interest Expense", int_row), ("Amortisation", amo_row),
                   ("Depreciation", dep_row)]
    ab_rows = []
    for label, src in addback_src:
        rr = r_holder[0]
        ws.cell(row=rr, column=2, value=label)
        for c in value_cols:
            L = get_column_letter(c)
            cell = ws.cell(row=rr, column=c, value=f"=-{L}{src}")
            cell.number_format = KFMT
        ab_rows.append(rr)
        r_holder[0] += 1
    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="R&D tax credit")
    for c in value_cols:
        cell = ws.cell(row=rr, column=c, value=0)
        cell.font = BLUE
        cell.number_format = KFMT
    ab_rows.append(rr)
    r_holder[0] += 1

    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="EBITDA").font = BOLD
    for c in value_cols:
        L = get_column_letter(c)
        terms = "+".join(f"{L}{a}" for a in ab_rows)
        cell = ws.cell(row=rr, column=c, value=f"={L}{pbt_row}+{terms}")
        cell.font = BOLD
        cell.number_format = KFMT
    ebitda_row = rr
    diff_formula(rr)
    r_holder[0] += 1

    first_ab = r_holder[0]
    for i in range(1, 5):
        rr = r_holder[0]
        ws.cell(row=rr, column=2, value=f"Addback {i}")
        for c in value_cols:
            cell = ws.cell(row=rr, column=c, value=0)
            cell.font = BLUE
            cell.number_format = KFMT
        r_holder[0] += 1
    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="Adj EBITDA").font = BOLD
    for c in value_cols:
        L = get_column_letter(c)
        cell = ws.cell(row=rr, column=c,
                       value=f"={L}{ebitda_row}+SUM({L}{first_ab}:{L}{first_ab + 3})")
        cell.font = BOLD
        cell.number_format = KFMT
    diff_formula(rr)
    adj_ebitda_row = rr
    r_holder[0] += 2

    rr = r_holder[0]
    ws.cell(row=rr, column=2, value="Check").font = BOLD
    ws.cell(row=rr, column=3,
            value="Source total minus mapped total per column - wire to source sections; must be 0")
    for c in value_cols:
        cell = ws.cell(row=rr, column=c, value=0)
        cell.font = BLUE
        cell.number_format = KFMT1     # sub-GBP-1k breaks must stay visible

    for rr in subtotal_rows + [gp_row, pbt_row, ebitda_row, adj_ebitda_row]:
        style_subtotal(ws, rr, 2, last_col)

    # widths per MASTER_template_PL.xlsx
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 48.75
    ws.column_dimensions["C"].width = 24.63
    for c in value_cols:
        ws.column_dimensions[get_column_letter(c)].width = 14
    ws.column_dimensions[get_column_letter(col_y1)].width = 24.63
    ws.column_dimensions[get_column_letter(first_hist + n_hist)].width = 5.88
    ws.column_dimensions[get_column_letter(col_y1c)].width = 62
    ws.freeze_panes = ws.cell(row=hdr_row + 1, column=4)


def build_qa(ws):
    ws.sheet_properties.tabColor = TAB_COLOURS["Other"]
    r = section(ws, 1, "Q&A")
    r += 1
    ws.cell(row=r, column=3, value="Question").font = BOLD
    ws.cell(row=r, column=4, value="Answer").font = BOLD
    style_header(ws, r, (3, 4))
    r += 12
    r = section(ws, r, "Data requests / questions")
    r += 1
    cols = ["What's needed", "Why / what it feeds", "Target tab", "Priority",
            "Status"]
    for i, h in enumerate(cols):
        ws.cell(row=r, column=2 + i, value=h).font = BOLD
    style_header(ws, r, range(2, 2 + len(cols)))
    for col, w in zip("BCDEF", (50, 50, 12, 12, 14)):
        ws.column_dimensions[col].width = w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    cfg = json.load(open(args.config))

    tabs = list(cfg["tabs"])
    codes = [t["code"] for t in tabs]
    if "L" not in codes:
        tabs.insert(0, {"code": "L", "description": "Legend - this sheet", "group": "Other"})
    if "QA" not in codes:
        tabs.append({"code": "QA", "description": "Questions & Answers", "group": "Other"})

    wb = Workbook()
    wb.remove(wb.active)
    for t in tabs:
        ws = wb.create_sheet(title=t["code"])
        ws.sheet_properties.tabColor = TAB_COLOURS.get(t["group"], "00B0F0")

    build_legend(wb["L"], tabs, cfg.get("deal_name", ""))
    if "PL" in wb.sheetnames:
        build_pl(wb["PL"], cfg.get("historic_columns", []),
                 cfg.get("year_end"))
    build_qa(wb["QA"])
    # every other tab gets its first section marker so the x-convention is seeded
    done = {"L", "PL", "QA"}
    for t in tabs:
        if t["code"] not in done:
            ws = wb[t["code"]]
            section(ws, 1, f"{t['code']} summary")
            ws.column_dimensions["B"].width = 45

    apply_house_font(wb)
    wb.save(args.output)
    print(f"Scaffolded {args.output}: tabs {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
