#!/usr/bin/env python3
"""Generate PDF(s) from CSV input.

By default this script renders the entire CSV as a single table in a PDF located at
`resume-machine/artifacts/csv-table.pdf`. If `--per-row` is given, one PDF per row is written to
`resume-machine/artifacts/rows/` named `row-<N>.pdf`.

Usage examples:
  python scripts/csv_to_pdf.py scripts/sample.csv
  python scripts/csv_to_pdf.py scripts/sample.csv --per-row
"""
import argparse
import csv
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def render_table_pdf(rows, headers, out_path, pagesize=A4):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    doc = SimpleDocTemplate(out_path, pagesize=pagesize)
    styles = getSampleStyleSheet()
    elems = []

    title = Paragraph("CSV Table Export", styles["Heading2"])
    elems.append(title)
    elems.append(Spacer(1, 12))

    data = [headers] + rows
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
    )
    elems.append(table)
    doc.build(elems)


def render_row_pdf(row_dict, out_path, pagesize=A4):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    doc = SimpleDocTemplate(out_path, pagesize=pagesize)
    styles = getSampleStyleSheet()
    elems = []

    title = Paragraph("CSV Row Export", styles["Heading2"])
    elems.append(title)
    elems.append(Spacer(1, 12))

    for k, v in row_dict.items():
        elems.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))
        elems.append(Spacer(1, 6))

    doc.build(elems)


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = [list(r.values()) for r in reader]
    return headers, rows


def load_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main(argv=None):
    p = argparse.ArgumentParser(description="Render CSV to PDF(s)")
    p.add_argument("csv", help="Path to CSV file")
    p.add_argument("--per-row", action="store_true", help="Produce one PDF per CSV row")
    p.add_argument("--out", default="resume-machine/artifacts/csv-table.pdf", help="Output PDF path or directory for per-row")
    args = p.parse_args(argv)

    if args.per_row:
        rows = load_csv_rows(args.csv)
        out_dir = args.out if os.path.isdir(args.out) or args.out.endswith(os.sep) else os.path.join(args.out)
        out_dir = out_dir if out_dir.endswith(os.sep) else out_dir
        base_dir = out_dir.rstrip(os.sep) if out_dir else "resume-machine/artifacts/rows"
        os.makedirs(base_dir, exist_ok=True)
        for i, r in enumerate(rows, start=1):
            out_path = os.path.join(base_dir, f"row-{i}.pdf")
            render_row_pdf(r, out_path)
            print("Wrote", out_path)
    else:
        # table export
        with open(args.csv, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            print("CSV is empty")
            return 1
        headers = rows[0]
        body = rows[1:]
        render_table_pdf(body, headers, args.out)
        print("Wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
