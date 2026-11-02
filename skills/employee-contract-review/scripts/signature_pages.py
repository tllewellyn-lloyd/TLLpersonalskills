#!/usr/bin/env python3
"""
Render one signature-block composite image per employee, for the visual signature check.

Usage:
    python3 signature_pages.py <pdf_dir> <out_img_dir> [--empkey "Employee (\\d+)"]

Why: in redacted documents, OCR cannot tell a redacted-but-signed block (a black box) from a
genuinely blank, unsigned one — both come out as empty text. So signatures MUST be judged by eye.
This crops each document's signature block and stacks a labelled composite per employee, so you can
open ~one image per person and record, per document: did each party sign, the dates, and whether
the signature is redacted.

Crop bands (tuned to this employer's templates, adjust if a template differs):
- Letters (variation / resignation / acceptance / leaver): signature is near the BOTTOM of page 1
  -> crop the lower ~70%.
- Contracts / obligations / apprenticeship agreements: signature sits near the TOP of the FINAL
  page (the rest of that page is usually blank) -> crop the 5%–62% band of the last page.

Files are grouped by an employee key parsed from the file name (default "Employee <n>"). Adjust
--empkey for other naming schemes.

Requires: pymupdf (fitz), pillow.
"""
import sys, os, glob, re, io

def main():
    args = [a for a in sys.argv[1:]]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    pdf_dir, out_dir = args[0], args[1]
    empkey = r"Employee (\d+)"
    if "--empkey" in args:
        empkey = args[args.index("--empkey") + 1]

    import fitz
    from PIL import Image, ImageDraw

    os.makedirs(out_dir, exist_ok=True)
    files = [os.path.basename(f) for f in glob.glob(os.path.join(pdf_dir, "*.pdf"))]
    groups = {}
    for f in files:
        m = re.search(empkey, f, re.IGNORECASE)
        key = m.group(1) if m else "_unmatched_" + f
        groups.setdefault(key, []).append(f)

    def is_letter(name):
        n = name.lower()
        return any(k in n for k in ["variation", "resignation", "acceptance", "leaver"])

    def crop_sig(name):
        doc = fitz.open(os.path.join(pdf_dir, name))
        pg = doc[len(doc) - 1]                      # last page holds the signature block
        zoom = 1500.0 / pg.rect.width
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        w, h = img.size
        if is_letter(name):
            return img.crop((0, int(h * 0.30), w, h))
        return img.crop((0, int(h * 0.05), w, int(h * 0.62)))

    def sort_key(k):
        return (0, int(k)) if str(k).isdigit() else (1, str(k))

    for key in sorted(groups, key=sort_key):
        flist = sorted(groups[key])
        crops = []
        for f in flist:
            c = crop_sig(f)
            bar = Image.new("RGB", (c.width, 26), (30, 60, 110))
            ImageDraw.Draw(bar).text((6, 7), f.replace("_Redacted.pdf", "")[:120], fill=(255, 255, 255))
            crops.append(bar); crops.append(c)
        maxw = max(c.width for c in crops)
        comp = Image.new("RGB", (maxw, sum(c.height for c in crops)), (255, 255, 255))
        y = 0
        for c in crops:
            comp.paste(c, (0, y)); y += c.height
        if comp.height > 5200:                       # keep it legible for the viewer
            r = 5200 / comp.height
            comp = comp.resize((int(comp.width * r), 5200))
        safe = re.sub(r"[^A-Za-z0-9]+", "_", str(key))
        comp.save(os.path.join(out_dir, f"emp_{safe}.png"))
        print("wrote", f"emp_{safe}.png", f"({len(flist)} docs)")

if __name__ == "__main__":
    main()
