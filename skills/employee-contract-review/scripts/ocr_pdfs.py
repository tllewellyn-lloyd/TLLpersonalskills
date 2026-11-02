#!/usr/bin/env python3
"""
Resumable, time-boxed OCR for scanned/redacted employment PDFs.

Usage:
    python3 ocr_pdfs.py <pdf_dir> <out_txt_dir> [offset stride] [--budget SECONDS] [--width PX]

Why this exists (lessons from a real run):
- These documents are scans with no text layer, so pdf text extraction returns nothing — OCR is
  required. Check first: if fitz `page.get_text()` is empty on page 1, OCR the file.
- Some scans have huge page mediaboxes; rendering at a fixed DPI then produces enormous images and
  OCR crawls. So we normalise the RENDER WIDTH (~1200px) regardless of the page's declared size.
- The sandbox kills background processes between bash calls and `ProcessPoolExecutor` tends to
  hang, so this runs sequentially in the FOREGROUND and is designed to be called repeatedly. It
  skips files already done and, given a time budget, only starts a file it can finish — so nothing
  is left half-written. Call it again (or launch several in parallel with different offset/stride)
  until every PDF has a matching .txt.

offset/stride: process files[offset::stride] — use e.g. `0 4`, `1 4`, `2 4`, `3 4` as four parallel
bash calls to go ~4x faster. Omit to process all files in one (repeatable) pass.

Requires: pymupdf (fitz), pytesseract, pillow, and the tesseract binary. Install if missing:
    pip install pymupdf pytesseract pillow --break-system-packages   (tesseract via apt if needed)
"""
import sys, os, glob, io, time

def main():
    args = [a for a in sys.argv[1:]]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    pdf_dir, out_dir = args[0], args[1]
    offset, stride = 0, 1
    pos = [a for a in args[2:] if not a.startswith("--")]
    if len(pos) >= 2:
        offset, stride = int(pos[0]), int(pos[1])
    budget = 40.0
    width = 1200.0
    if "--budget" in args: budget = float(args[args.index("--budget") + 1])
    if "--width" in args:  width = float(args[args.index("--width") + 1])

    import fitz, pytesseract
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    files = [os.path.basename(f) for f in sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))]
    mine = files[offset::stride]
    start = time.time()
    done = 0
    for f in mine:
        op = os.path.join(out_dir, os.path.splitext(f)[0] + ".txt")
        if os.path.exists(op):
            continue
        doc = fitz.open(os.path.join(pdf_dir, f))
        npages = len(doc)
        # only start a file we can finish within the remaining budget (~4.7s/page observed)
        if time.time() - start + npages * 4.7 > budget:
            continue
        parts = []
        for i, pg in enumerate(doc):
            zoom = width / pg.rect.width
            pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            parts.append(f"\n===== PAGE {i+1} =====\n" + pytesseract.image_to_string(img))
        with open(op, "w") as fh:
            fh.write("".join(parts))
        done += 1
        print("ok", f, flush=True)

    remaining = [f for f in files
                 if not os.path.exists(os.path.join(out_dir, os.path.splitext(f)[0] + ".txt"))]
    print(f"done this call: {done} | remaining overall: {len(remaining)}")
    if remaining:
        print("Call again (or in parallel with offset/stride) until remaining = 0.")

if __name__ == "__main__":
    main()
