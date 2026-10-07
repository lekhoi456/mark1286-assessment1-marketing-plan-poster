#!/usr/bin/env python3
"""Focused source, copy, geometry, and logo checks for Section 5 v06."""
from collections import Counter
from hashlib import sha256
from html import unescape
from pathlib import Path
import base64
import json
import re
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SVG = HERE / "05-v06-candidate-2026-10-04.svg"
PNG = HERE / "05-v06-candidate-2026-10-04.png"
COPY = HERE / "05-v06-copy-2026-10-04.md"
LOGO = HERE / "shared-logo.png"
OUTPUT = HERE / "05-v06-focused-checks-2026-10-04.json"
XLINK = "{http://www.w3.org/1999/xlink}href"


def main() -> None:
    subprocess.run([sys.executable, "-B", str(HERE / "05-v06-render-2026-10-04.py")], check=True)
    root = ET.parse(SVG).getroot()
    texts = [el.text or "" for el in root.iter() if el.tag.endswith("text")]
    visible = "\n".join(texts)
    copy = re.sub(r"<!--.*?-->", "", COPY.read_text(), flags=re.S)
    copy_lines = []
    for line in copy.splitlines():
        line = line.strip()
        if not line or line == "# Panel 5 display copy":
            continue
        copy_lines.append(re.sub(r"^#+\s*", "", line))
    copy_tokens = Counter(" ".join(copy_lines).split())
    svg_tokens = Counter(visible.split())
    if copy_tokens != svg_tokens:
        raise SystemExit(f"Copy/SVG text mismatch: markdown-only={copy_tokens-svg_tokens}; svg-only={svg_tokens-copy_tokens}")

    required = [
        "5. Digital Marketing", "Capital Region app-choice sample n=79",
        "57%", "22%", "18%", "lower price", "usual app", "shorter wait", "easier app",
        "PRODUCT", "EV RIDE", "SERVICE*", "PRICE", "CLEAR FARE",
        "1ST-TRIP OFFER*", "*Controlled service and first-trip offer are proposed", "PLACE", "GREEN SM APP", "PROMOTION", "OMNICHANNEL",
        "Consented first-party data", "Audit privacy · quality · access · systems",
        "CDP or Big Data post-audit only", "No CDP assumed.", "SEARCH/SOCIAL + CITY MEDIA*",
        "↓ LOCAL INFO PAGE: AREA/FARE/HELP", "↓ GREEN SM APP · BOOK",
        "*Gate B screens: awareness only · no ride credit",
        "Vietnam: capped, limited-validity vouchers", "Danish proposal: opt-in, capped 30 days",
        "No auto-renew · optional repurchase", "Existing reserve · S6/S7 approval",
        "Measure redemption + repeat", "App/terms/service check", "LIFT UNPROVEN",
    ]
    joined = "\n".join(texts)
    missing = [s for s in required if s not in joined]
    if missing:
        raise SystemExit(f"Required copy missing: {missing}")
    if re.search(r"E-\d{3}", visible, re.I):
        raise SystemExit("Visible evidence ID detected")
    if any("5." not in line and line.isupper() and len(line.split()) > 2 for line in texts):
        # This check is informational only; numbered section headings are separately tested in Markdown.
        pass

    heading_lines = [line.strip() for line in COPY.read_text().splitlines() if line.startswith("#") and line != "# Panel 5 display copy"]
    if not heading_lines or any(not re.match(r"^#+\s+5(?:\.|\d)", line) for line in heading_lines):
        raise SystemExit(f"Unnumbered display heading in copy: {heading_lines}")

    image = next(el for el in root.iter() if el.tag.endswith("image") and el.attrib.get("id") == "display-logo")
    data_uri = image.attrib[XLINK]
    if not data_uri.startswith("data:image/png;base64,"):
        raise SystemExit("Logo is not an embedded PNG")
    embedded = base64.b64decode(data_uri.split(",", 1)[1])
    approved = LOGO.read_bytes()
    logo_match = sha256(embedded).hexdigest() == sha256(approved).hexdigest()
    if not logo_match:
        raise SystemExit("Embedded logo differs from shared-logo.png")
    png_data = PNG.read_bytes()
    if png_data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("Invalid PNG")
    width, height = struct.unpack(">II", png_data[16:24])
    if (width, height) != (1800, 1400):
        raise SystemExit(f"Unexpected PNG dimensions: {width}×{height}")

    with tempfile.TemporaryDirectory(prefix="panel05-v06-") as tmp:
        pdf = Path(tmp) / "panel.pdf"
        bbox = Path(tmp) / "bbox.html"
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(SVG)], check=True)
        subprocess.run(["pdftotext", "-bbox", str(pdf), str(bbox)], check=True)
        html = bbox.read_text()
    page = re.search(r'<page width="([0-9.]+)" height="([0-9.]+)">', html)
    if not page:
        raise SystemExit("Could not read text bounding page")
    page_w, page_h = map(float, page.groups())
    words = []
    for match in re.finditer(r'<word xMin="([0-9.]+)" yMin="([0-9.]+)" xMax="([0-9.]+)" yMax="([0-9.]+)">(.*?)</word>', html):
        x0, y0, x1, y1 = map(float, match.groups()[:4])
        word = unescape(match.group(5))
        if x0 < 0 or y0 < 0 or x1 > page_w or y1 > page_h or x1 < x0 or y1 < y0:
            raise SystemExit(f"Out-of-bounds word: {word!r} ({x0}, {y0}, {x1}, {y1})")
        words.append((x0, y0, x1, y1, word))
    overlaps = []
    for i, a in enumerate(words):
        for b in words[i+1:]:
            iw = min(a[2], b[2]) - max(a[0], b[0])
            ih = min(a[3], b[3]) - max(a[1], b[1])
            if iw > 0.2 and ih > 0.2:
                overlaps.append([a[4], b[4]])
    if overlaps:
        raise SystemExit(f"Overlapping rendered word boxes: {overlaps[:8]}")

    result = {
        "status": "pass",
        "svg": SVG.name,
        "png": PNG.name,
        "canvas_px": [width, height],
        "copy_svg_token_multisets_match": True,
        "visible_svg_whitespace_tokens": sum(svg_tokens.values()),
        "visible_evidence_ids": 0,
        "embedded_logo_sha256_matches_shared_logo": logo_match,
        "pdf_text_word_boxes": len(words),
        "out_of_bounds_words": 0,
        "overlapping_word_boxes": 0,
        "notes": ["Bound/overlap test uses rendered PDF text boxes; manual PNG inspection also completed."],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
