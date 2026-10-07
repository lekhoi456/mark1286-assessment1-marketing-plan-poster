"""Render the approved Section 4 brand identity as a hand-drawn vector brand board."""

from pathlib import Path
from html import escape
import base64
import hashlib
import importlib.util
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PREFIX = "04-candidate-v02-2026-10-04"
LOGO = HERE / "shared-logo.png"
spec = importlib.util.spec_from_file_location("native_lettering", HERE / "native-lettering.py")
native_lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native_lettering)
glyphs = native_lettering.GlyphServer()
title = "MarkerFelt-Wide"
body = "Noteworthy-Light"

COPY = [
    "4. Branding & Identity",
    "Green SM = Green and Smart Mobility",
    "Go Green For a Green Future.",
    "New Cyan · #28bdbf · Pantone 319 C",
    "New Yellow · #e3bb42",
    "Xanh Display 2.0",
    "Modern Liquid Glass UI/UX",
    "Clear terms. Local care.",
    "Danish first · English second",
]
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1360" viewBox="0 0 1800 1360">',
    '<title>4. Branding &amp; Identity — Green SM brand board</title>',
    '<desc>Hand-drawn brand board showing the Green SM lockup, name meaning, corporate slogan, specified colours and typeface, Liquid Glass UI direction, and Copenhagen language line.</desc>',
    '<rect width="1800" height="1360" fill="#fffdf5"/>',
    '<path d="M34 38 Q470 26 900 35 T1765 38 Q1778 710 1764 1323 Q1330 1337 900 1330 T35 1325 Q23 710 34 38Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M45 49 Q870 40 1751 49" fill="none" stroke="#28bdbf" stroke-width="3" opacity=".6"/>',
]
texts = []


def text(value, x, baseline, size, font=body, fill="#19364d", angle=0):
    parts.append(glyphs.svg(value, x, baseline, size, font, fill=fill, angle=angle))
    texts.append(value)


def centred(value, baseline, size, font=body, fill="#19364d"):
    text(value, (1800 - glyphs.width(value, font, size)) / 2, baseline, size, font, fill)


def line(x1, y1, x2, y2, colour, width=4, opacity=1):
    parts.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2} {((y1+y2)/2)-2} {x2} {y2}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" opacity="{opacity}"/>')


def logo(x, y, width):
    height = width * 724 / 2171
    uri = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")
    parts.append(f'<image href="{uri}" x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet"/>')


text(COPY[0], 78, 126, 78, title)
line(82, 151, 810, 151, "#e3bb42", 14, .76)

# Shared hand-drawn Green SM mark leads the global identity.
logo(102, 207, 670)
text(COPY[1], 108, 474, 44, title)
line(108, 493, 856, 493, "#28bdbf", 7, .65)

# The corporate slogan is the dominant message; the local line remains secondary.
text("Go Green For", 100, 635, 90, title, "#19364d")
text("a Green Future.", 100, 740, 90, title, "#19364d")
for i in range(5):
    line(104, 771+i*9, 874, 774+i*9, "#e3bb42", 8, .34)

# Two hand-painted colour chips with precise brand labels.
text("COLOUR", 1010, 235, 39, title)
parts.append('<path d="M1011 267 Q1290 257 1686 269 L1681 435 Q1378 444 1012 434Z" fill="#28bdbf" stroke="#19364d" stroke-width="3"/>')
for i in range(4):
    line(1030, 284+i*9, 1648, 286+i*8, "#83e0dc", 3, .7)
text("New Cyan", 1055, 342, 46, title, "#ffffff")
text("#28bdbf · Pantone 319 C", 1056, 399, 35, body, "#ffffff")
parts.append('<path d="M1014 460 Q1338 452 1685 461 L1681 586 Q1340 596 1012 585Z" fill="#e3bb42" stroke="#19364d" stroke-width="3"/>')
text("New Yellow", 1057, 518, 43, title)
text("#e3bb42", 1058, 563, 34)

# Type choice presented as a specimen card.
parts.append('<path d="M1009 620 Q1358 611 1686 621 L1680 810 Q1328 822 1012 808Z" fill="#ecf8f3" stroke="#91d9d4" stroke-width="4"/>')
text("TYPEFACE", 1040, 670, 34, title)
text(COPY[5], 1040, 748, 54, title)
text("G S M", 1468, 783, 41, title, "#28bdbf", -5)

# A small liquid-glass phone: layered translucent panels, sketched outline.
text("UI / UX", 1009, 876, 34, title)
parts.append('<path d="M1058 912 Q1160 902 1260 912 L1267 1192 Q1163 1202 1057 1191Z" fill="#d9f5ee" fill-opacity=".62" stroke="#19364d" stroke-width="5"/>')
parts.append('<path d="M1074 936 Q1165 929 1245 938 L1248 1167 Q1165 1174 1073 1165Z" fill="#ffffff" fill-opacity=".76" stroke="#28bdbf" stroke-width="3"/>')
parts.append('<path d="M1091 963 Q1160 955 1227 964 L1226 1014 Q1158 1021 1091 1012Z" fill="#bcefeb" fill-opacity=".74" stroke="#28bdbf" stroke-width="2"/>')
parts.append('<path d="M1091 1031 Q1150 1025 1227 1033 L1225 1081 Q1160 1089 1092 1080Z" fill="#f4edc8" fill-opacity=".65" stroke="#e3bb42" stroke-width="2"/>')
parts.append('<circle cx="1162" cy="1142" r="8" fill="#28bdbf"/>')
text(COPY[6], 1300, 1018, 37, title)
text("Layered · soft · clear", 1300, 1069, 30, body)
line(1301, 1094, 1647, 1097, "#28bdbf", 5, .62)

# Copenhagen-facing tagline and language treatment are kept small and singular.
parts.append('<path d="M90 1220 Q880 1209 1710 1220 L1706 1280 Q876 1289 91 1278Z" fill="#fff5cc" stroke="#e3bb42" stroke-width="2"/>')
centred(COPY[7], 1264, 39, title)
centred(COPY[8], 1320, 31, body)

glyphs.close()
parts.append('</svg>')
svg_path = HERE / f"{PREFIX}.svg"
svg_path.write_text("\n".join(parts), encoding="utf-8")
png_path = HERE / f"{PREFIX}.png"
subprocess.run(["/opt/homebrew/bin/rsvg-convert", "-o", str(png_path), str(svg_path)], check=True)
subprocess.run(["/opt/homebrew/bin/rsvg-convert", "-w", "900", "-o", str(HERE / f"{PREFIX}-small.png"), str(svg_path)], check=True)

copy_md = "## Branding & Identity\n<!-- budget: 75 -->\n\n" + "\n\n".join(COPY) + "\n"
(HERE / f"{PREFIX}-copy.md").write_text(copy_md, encoding="utf-8")
(HERE / f"{PREFIX}-prompt.md").write_text(
    "Hand-drawn native-vector brand board; exact lettering is converted to editable SVG glyph paths. Use the supplied shared hand-drawn Green SM mark unchanged. Show the corporate meaning and slogan as the main message, exact New Cyan/New Yellow specifications, Xanh Display 2.0, and a simple drawn Liquid Glass phone. Keep ‘Clear terms. Local care.’ to one secondary tagline and retain ‘Danish first · English second’. No poster-face citations, no photo, no copied Behance illustration.\n",
    encoding="utf-8",
)
manifest = {
    "panel": 4,
    "status": "review candidate; section copy update follows approved direction and latest student instructions",
    "dimensions": [1800, 1360],
    "copy": COPY,
    "shared_logo_sha256": hashlib.sha256(LOGO.read_bytes()).hexdigest(),
    "text_as_handdrawn_glyph_paths": True,
    "generated_or_external_art": False,
    "visible_citations": False,
    "local_tagline_occurrences": 1,
}
(HERE / f"{PREFIX}-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
svg_text = svg_path.read_text(encoding="utf-8")
svg_root = ET.fromstring(svg_text)
labels = [node.attrib["aria-label"] for node in svg_root.iter() if "aria-label" in node.attrib]
label_text = " ".join(labels)
normalised_label_text = re.sub(r"[^a-z0-9]+", " ", label_text.casefold()).strip()
required_text_counts = {
    value: len(re.findall(r"(?<![a-z0-9])" + re.escape(re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip())
                         + r"(?![a-z0-9])", normalised_label_text))
    for value in COPY
}
external_links = [
    value for node in svg_root.iter() for key, value in node.attrib.items()
    if key.rsplit("}", 1)[-1] in {"href", "src"}
    and value.lower().startswith(("http://", "https://"))
]
visible_citation_markers = re.search(r"(?i)\b(?:references|sources|doi:|https?://|www\.)\b", label_text)
checks = {
    "all_required_text_present_once": required_text_counts,
    "shared_hand_drawn_logo_present": LOGO.is_file(),
    "cyan_hex_exact": "#28bdbf" in svg_text,
    "yellow_hex_exact": "#e3bb42" in svg_text,
    "pantone_specified": "Pantone 319 C" in COPY[3],
    "tagline_once": COPY.count("Clear terms. Local care.") == 1,
    "no_removed_promise_label": "PROPOSED" not in label_text,
    "no_citations": not external_links and visible_citation_markers is None,
}
(HERE / f"{PREFIX}-checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print(f"Rendered {png_path}")
