"""Render the exact-copy section-6 candidate as a self-contained SVG and PNG."""

from html import escape
from pathlib import Path
import base64
import subprocess

from PIL import ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = "06-v02-candidate"
ART = HERE / "06-v02-generated-art.png"
OUTPUT = HERE / f"{PREFIX}.svg"
WIDTH, HEIGHT = 1800, 1600
PAPER, NAVY, CYAN, GOLD = "#fffdf5", "#173a47", "#26c6cf", "#ffd400"

title_font = ImageFont.truetype("/System/Library/Fonts/MarkerFelt.ttc", 80, index=0)
body_font = ImageFont.truetype("/System/Library/Fonts/Noteworthy.ttc", 40, index=0)

cards = [
    {
        "title": "Lead",
        "lines": [
            "The proposed route",
            "runs from search/social",
            "to the local information",
            "page, then to an app",
            "install or account.",
            "The website informs and",
            "directs riders to the app.",
            "Installs and accounts",
            "are leads, not sales.",
        ],
    },
    {
        "title": "Prospect",
        "lines": [
            "Proposed prospecting",
            "sends one opted-in",
            "message to people who",
            "installed the app but",
            "have not taken a ride,",
            "with the verified",
            "service area and help",
            "route.",
        ],
    },
    {
        "title": "First paid ride",
        "lines": [
            "Direct app booking",
            "→ completed, paid",
            "trip = sale.",
            "Proposed DKK30",
            "voucher · once per",
            "new rider · cap 400.",
        ],
    },
    {
        "title": "After-sales help",
        "lines": [
            "The plan includes a",
            "trip reference, staffed",
            "help route and one",
            "clarity question.",
            "The in-car help card",
            "shows the trip reference",
            "and support route. It is",
            "never a booking card.",
        ],
    },
    {
        "title": "Consented repeat",
        "lines": [
            "Relationship selling:",
            "with consent,",
            "a relevant reminder",
            "→ another paid trip.",
        ],
    },
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
    '<title>6. From Clicks to Rides — Sales Strategy</title>',
    f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
    '<defs>',
    f'<image id="art-sheet" href="data:image/png;base64,{base64.b64encode(ART.read_bytes()).decode("ascii")}" width="2172" height="724"/>',
    '<marker id="flow-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="none" stroke="#26c6cf" stroke-width="1.6"/></marker>',
    '</defs>',
    '<path d="M34 38 Q470 26 900 35 T1765 38 Q1778 810 1764 1563 Q1330 1577 900 1570 T35 1565 Q23 810 34 38Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M45 49 Q870 40 1751 49" fill="none" stroke="#68c9cd" stroke-width="2" opacity=".62"/>',
]

text_boxes = []


def add_text(value, x, baseline, size, font=body_font, role="copy", align="left", fill=NAVY):
    if align == "centre":
        x -= font.getlength(value) * size / font.size / 2
    scale = size / font.size
    raw_box = font.getbbox(value, anchor="ls")
    box = [
        round(x + raw_box[0] * scale, 3),
        round(baseline + raw_box[1] * scale, 3),
        round(x + raw_box[2] * scale, 3),
        round(baseline + raw_box[3] * scale, 3),
    ]
    if box[0] < 35 or box[1] < 35 or box[2] > WIDTH - 35 or box[3] > HEIGHT - 35:
        raise ValueError(f"Text outside canvas: {value!r} {box}")
    group_id = f"text-{len(text_boxes):02d}"
    family = "Marker Felt" if font is title_font else "Noteworthy"
    anchor = "middle" if align == "centre" else "start"
    output_x = x + font.getlength(value) * scale / 2 if align == "centre" else x
    parts.append(
        f'<g id="{group_id}" data-role="{escape(role, quote=True)}" '
        f'data-copy="{escape(value, quote=True)}" aria-label="{escape(value, quote=True)}">'
        f'<title>{escape(value)}</title><text x="{output_x:.3f}" y="{baseline}" '
        f'text-anchor="{anchor}" font-family="{family}" font-size="{size}" '
        f'fill="{fill}">{escape(value)}</text></g>'
    )
    text_boxes.append({"id": group_id, "copy": value, "bbox": box, "role": role})
    return box


def add_sprite(crop, target, label):
    cx, cy, cw, ch = crop
    x, y, width, height = target
    parts.append(
        f'<svg data-illustration="{escape(label, quote=True)}" x="{x}" y="{y}" '
        f'width="{width}" height="{height}" viewBox="{cx} {cy} {cw} {ch}" '
        'overflow="hidden" preserveAspectRatio="xMidYMid meet"><use href="#art-sheet"/></svg>'
    )


# Header: the title carries the required number; the subtitle remains unnumbered.
title_box = add_text("6. From Clicks to Rides", 76, 129, 80, title_font, "title")
parts.append(
    f'<path d="M73 153 Q{title_box[2] + 28:.1f} 145 {title_box[2] + 55:.1f} 153" '
    f'fill="none" stroke="{GOLD}" stroke-width="13" stroke-linecap="round" opacity=".78"/>'
)
subtitle_box = add_text("Sales Strategy", 82, 207, 43, body_font, "subtitle")
parts.append('<path d="M82 220 Q245 225 402 218" fill="none" stroke="#26c6cf" stroke-width="4" stroke-linecap="round" opacity=".72"/>')
parts.append('<path d="M66 251 Q900 258 1735 250" fill="none" stroke="#68b8bd" stroke-width="2" opacity=".62"/>')

# The generated strip stays uncut so every complete pictogram remains visible.
add_sprite((0, 71, 2172, 647), (48, 258, 1704, 508), "five-step pictogram ribbon; transparent-margin crop only")

# Five cards form the left-to-right sales process. No stage numbers are added.
card_xs = [60, 408, 756, 1104, 1452]
card_y, card_w, card_h = 770, 300, 504
for index, card in enumerate(cards):
    x = card_xs[index]
    outline = "#526d74" if index != 2 else NAVY
    parts.append(
        f'<path d="M{x+10} {card_y+8} Q{x+148} {card_y-1} {x+card_w-8} {card_y+9} '
        f'L{x+card_w-5} {card_y+card_h-12} Q{x+151} {card_y+card_h+1} {x+8} {card_y+card_h-7}Z" '
        f'fill="#fffefa" stroke="{outline}" stroke-width="2.3"/>'
    )
    if index == 2:
        parts.append(f'<path d="M{x+28} {card_y+18} Q{x+150} {card_y+13} {x+card_w-26} {card_y+18}" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" opacity=".56"/>')
    heading_size = 36
    while title_font.getlength(card["title"]) * heading_size / title_font.size > card_w - 28:
        heading_size -= 1
    heading = add_text(card["title"], x + card_w / 2, 872, heading_size, title_font, f"stage-{index+1}", "centre")
    parts.append(
        f'<path d="M{x+31} 888 Q{x+150} 894 {x+card_w-32} 887" fill="none" '
        f'stroke="{CYAN if index % 2 == 0 else GOLD}" stroke-width="7" stroke-linecap="round" opacity=".58"/>'
    )
    baseline = 926
    for line in card["lines"]:
        size = 27
        while body_font.getlength(line) * size / body_font.size > card_w - 30:
            size -= 1
        box = add_text(line, x + card_w / 2, baseline, size, body_font, f"stage-{index+1}-body", "centre")
        if box[0] < x + 13 or box[2] > x + card_w - 13:
            raise ValueError(f"Card text outside its card: {line!r} {box}")
        baseline += 38

# The hand-drawn arrows sit in the gutters and connect the five stages.
for left in range(4):
    start_x = card_xs[left] + card_w + 7
    end_x = card_xs[left + 1] - 8
    parts.append(
        f'<path d="M{start_x} 903 Q{(start_x+end_x)/2:.1f} 895 {end_x} 903" '
        'fill="none" stroke="#26c6cf" stroke-width="3.4" stroke-linecap="round" marker-end="url(#flow-arrow)"/>'
    )
    parts.append(
        f'<path d="M{start_x+2} 909 Q{(start_x+end_x)/2:.1f} 905 {end_x-4} 909" '
        f'fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" opacity=".65"/>'
    )

# Two selling techniques and one readiness condition close the process.
parts.append('<path d="M75 1300 Q900 1307 1724 1300" fill="none" stroke="#68b8bd" stroke-width="2" opacity=".65"/>')
parts.append('<path d="M73 1318 Q458 1312 863 1320 L862 1455 Q458 1461 74 1454Z" fill="#f4fbf8" stroke="#aebdb7" stroke-width="2"/>')
parts.append('<path d="M929 1318 Q1325 1312 1725 1320 L1724 1454 Q1328 1462 930 1454Z" fill="#fffaf0" stroke="#d5c99c" stroke-width="2"/>')
add_text("Value-based selling", 104, 1364, 35, title_font, "selling-technique")
add_text("Clear fare terms + available help.", 104, 1421, 34, body_font, "selling-technique-copy")
add_text("Soft selling", 960, 1364, 35, title_font, "selling-technique")
add_text("Invite an app-store review after a", 960, 1406, 29, body_font, "selling-technique-copy")
add_text("resolved or well-rated trip. Never pay for it.", 960, 1443, 28, body_font, "selling-technique-copy")

parts.append('<path d="M73 1468 Q900 1462 1724 1468 L1720 1518 Q900 1523 78 1518Z" fill="#eef9f5" stroke="#b8d7d4" stroke-width="2"/>')
add_text("Delivery check", 104, 1504, 30, title_font, "delivery-condition")
add_text("Brief employed drivers. Confirm help-route staffing + response standards before advertising.", 408, 1504, 26, body_font, "delivery-condition-copy")

parts.append('</svg>')
svg = "\n".join(parts)
OUTPUT.write_text(svg, encoding="utf-8")
subprocess.run(
    ["/opt/homebrew/bin/rsvg-convert", "-o", str(HERE / f"{PREFIX}.png"), str(OUTPUT)],
    check=True,
)

# Geometry checks run during rendering: every text path is inside the canvas,
# and no stage copy falls outside its own card.
for left_index, left in enumerate(text_boxes):
    for right in text_boxes[left_index + 1:]:
        a, b = left["bbox"], right["bbox"]
        overlap_x = min(a[2], b[2]) - max(a[0], b[0])
        overlap_y = min(a[3], b[3]) - max(a[1], b[1])
        if overlap_x > 0 and overlap_y > 0:
            raise ValueError(f"Text overlap: {left['copy']!r} / {right['copy']!r}")

print(f"Rendered {OUTPUT.name} and {PREFIX}.png at {WIDTH}x{HEIGHT}.")
print(f"Checked {len(text_boxes)} text groups: canvas bounds and pairwise overlap clear.")
print(f"Header title: {title_box}; subtitle: {subtitle_box}.")
