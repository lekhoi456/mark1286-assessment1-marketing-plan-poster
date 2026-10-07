"""Render the Section 6 sales-loop candidate as editable, self-contained SVG and PNG."""

from base64 import b64encode
from html import escape
from pathlib import Path
import subprocess

from PIL import ImageFont

HERE = Path(__file__).resolve().parent
PREFIX = "06-v04-candidate"
WIDTH, HEIGHT = 1800, 1260
PAPER, NAVY, CYAN, GOLD = "#fffdf5", "#173a47", "#26c6cf", "#ffd400"
LOGO = HERE / "shared-logo.png"
SVG_OUT = HERE / f"{PREFIX}.svg"
PNG_OUT = HERE / f"{PREFIX}.png"

title_font = ImageFont.truetype("/System/Library/Fonts/MarkerFelt.ttc", 80, index=0)
label_font = ImageFont.truetype("/System/Library/Fonts/MarkerFelt.ttc", 38, index=0)
body_font = ImageFont.truetype("/System/Library/Fonts/Noteworthy.ttc", 40, index=0)

cards = [
    {
        "title": "Awareness",
        "lines": [
            "Copenhagen visibility.",
            "Installs are leads,",
            "not sales.",
        ],
    },
    {
        "title": "Book",
        "lines": [
            "Book directly in the app.",
            "Sale is a",
            "completed, paid",
            "trip.",
            "DKK30 first-trip",
            "discount, capped at",
            "400 riders",
            "(DKK12,000 reserve).",
        ],
    },
    {
        "title": "Experience",
        "lines": [
            "Target: excellent",
            "app, driver, vehicle",
            "+ support.",
            "Verify staffed-help and",
            "operations standards first.",
        ],
    },
    {
        "title": "Feedback",
        "lines": [
            "Ask post-ride",
            "feedback.",
            "Unpaid app-store",
            "review after a",
            "resolved/well-rated trip.",
        ],
    },
    {
        "title": "Repeat",
        "lines": [
            "With consent: app",
            "notifications.",
            "Repeat voucher pilot.",
            "Monthly bundle pilot:",
            "tailored, capped,",
            "time-limited.",
            "Fund both separately",
            "only if observed rider",
            "frequency + unit",
            "economics fit.",
        ],
    },
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
    '<title>6. From Clicks to Rides — Sales Strategy</title>',
    f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
    '<defs>',
    '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#26c6cf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker>',
    '</defs>',
    '<path d="M34 39 Q470 27 900 36 T1766 39 Q1777 620 1764 1221 Q1330 1235 900 1225 T35 1220 Q24 620 34 39Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M45 50 Q880 42 1755 50" fill="none" stroke="#68c9cd" stroke-width="2" opacity=".62"/>',
]

text_records = []


def add_text(value, x, baseline, size, font, role, align="left", fill=NAVY, min_size=None):
    min_size = min_size or size
    scale = size / font.size
    while font.getlength(value) * scale > (278 if role.startswith("stage-") else 780) and size > min_size:
        size -= 1
        scale = size / font.size
    if font.getlength(value) * scale > (278 if role.startswith("stage-") else 780):
        raise ValueError(f"Text exceeds allowed width: {value!r} ({size}px)")
    if align == "centre":
        x -= font.getlength(value) * scale / 2
    raw_box = font.getbbox(value, anchor="ls")
    box = [
        round(x + raw_box[0] * scale, 3),
        round(baseline + raw_box[1] * scale, 3),
        round(x + raw_box[2] * scale, 3),
        round(baseline + raw_box[3] * scale, 3),
    ]
    if box[0] < 35 or box[1] < 35 or box[2] > WIDTH - 35 or box[3] > HEIGHT - 35:
        raise ValueError(f"Text outside canvas: {value!r} {box}")
    family = "Marker Felt" if font in (title_font, label_font) else "Noteworthy"
    anchor = "middle" if align == "centre" else "start"
    output_x = x + font.getlength(value) * scale / 2 if align == "centre" else x
    parts.append(
        f'<g id="text-{len(text_records):02d}" data-role="{escape(role, quote=True)}" data-copy="{escape(value, quote=True)}">'
        f'<title>{escape(value)}</title><text x="{output_x:.3f}" y="{baseline}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" fill="{fill}">{escape(value)}</text></g>'
    )
    text_records.append({"copy": value, "bbox": box, "role": role, "size": size})
    return box


def path(d, fill="none", stroke=NAVY, width=5, extra=""):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def circle(cx, cy, r, fill, stroke=NAVY, width=4, extra=""):
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>')


def rect(x, y, w, h, rx=6, fill="none", stroke=NAVY, width=4, extra=""):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>')


# Header, with the supplied hand-drawn logo embedded byte-for-byte as a data URI.
title_box = add_text("6. From Clicks to Rides", 76, 124, 78, title_font, "title")
path(f'M72 148 Q{title_box[2] + 25:.1f} 143 {title_box[2] + 48:.1f} 151', stroke=GOLD, width=12, extra='opacity=".78"')
subtitle = add_text("Sales Strategy", 80, 211, 43, body_font, "subtitle")
path("M79 224 Q245 229 395 222", stroke=CYAN, width=4, extra='opacity=".72"')
logo_data = b64encode(LOGO.read_bytes()).decode("ascii")
parts.append(f'<image id="green-sm-logo" data-role="brand-logo" href="data:image/png;base64,{logo_data}" x="1425" y="54" width="322" height="107" preserveAspectRatio="xMidYMid meet"/>')
path("M66 263 Q900 270 1734 262", stroke="#68b8bd", width=2, extra='opacity=".62"')

# Wavy, hand-drawn cards leave a clear arrow gutter and room for the illustrations.
card_xs = [50, 400, 750, 1100, 1450]
card_y, card_w, card_h = 342, 300, 700
centres = [x + card_w / 2 for x in card_xs]
for i, x in enumerate(card_xs):
    stroke = NAVY if i == 1 else "#526d74"
    parts.append(
        f'<path d="M{x+9} {card_y+9} Q{x+145} {card_y-1} {x+card_w-9} {card_y+8} '
        f'L{x+card_w-5} {card_y+card_h-12} Q{x+146} {card_y+card_h+1} {x+7} {card_y+card_h-8}Z" '
        f'fill="#fffefa" stroke="{stroke}" stroke-width="2.5"/>'
    )
    if i == 1:
        path(f'M{x+28} {card_y+18} Q{x+150} {card_y+12} {x+card_w-27} {card_y+18}', stroke=GOLD, width=9, extra='opacity=".58"')

# Icon 1: Copenhagen street / visible local awareness.
cx = centres[0]
circle(cx + 70, 392, 27, GOLD, width=3)
for ray in range(8):
    import math
    a = ray * math.pi / 4
    path(f'M{cx+70+36*math.cos(a):.1f} {392+36*math.sin(a):.1f} L{cx+70+48*math.cos(a):.1f} {392+48*math.sin(a):.1f}', stroke=GOLD, width=5)
path(f'M{cx-119} 510 L{cx-119} 436 L{cx-73} 402 L{cx-25} 436 L{cx-25} 510Z', fill="#dff8f6", width=4)
path(f'M{cx-124} 436 L{cx-72} 397 L{cx-20} 436', stroke=NAVY, width=5)
for dx in (-102, -78, -54, -31):
    rect(cx+dx, 452, 12, 15, 2, fill=CYAN, width=2)
path(f'M{cx-15} 510 L{cx-15} 420 L{cx+24} 384 L{cx+64} 420 L{cx+64} 510Z', fill="#fff4c5", width=4)
path(f'M{cx-20} 420 L{cx+24} 379 L{cx+69} 420', stroke=NAVY, width=5)
for dx in (0, 24, 47):
    rect(cx+dx, 435, 12, 15, 2, fill=CYAN, width=2)
rect(cx+5, 470, 36, 40, 2, fill="#fffdf5", width=3)
rect(cx+68, 435, 42, 75, 7, fill="#eaf8f5", width=4)
path(f'M{cx+77} 455 Q{cx+89} 451 {cx+101} 455 M{cx+77} 469 Q{cx+89} 465 {cx+101} 469', stroke=CYAN, width=4)
path(f'M{cx-128} 519 Q{cx-20} 525 {cx+117} 516', stroke=CYAN, width=4)

# Icon 2: first-trip voucher and the paid-trip close.
cx = centres[1]
path(f'M{cx-111} 395 Q{cx-53} 386 {cx+66} 395 L{cx+104} 444 L{cx+66} 493 Q{cx-40} 501 {cx-111} 490 L{cx-130} 444Z', fill="#fff2ab", width=5)
path(f'M{cx-81} 399 L{cx-81} 486', stroke=CYAN, width=4, extra='stroke-dasharray="7 9"')
circle(cx+54, 441, 42, GOLD, width=5)
circle(cx+54, 441, 30, "#ffe66a", stroke="#efbd00", width=2)
path(f'M{cx+42} 441 Q{cx+54} 430 {cx+66} 441 M{cx+43} 453 Q{cx+54} 462 {cx+65} 453', stroke=NAVY, width=3)
path(f'M{cx-98} 526 Q{cx-48} 519 {cx-6} 525 M{cx+14} 526 Q{cx+66} 519 {cx+119} 526', stroke=CYAN, width=4)

# Icon 3: app, employed driver, vehicle and customer care as the experience target.
cx = centres[2]
rect(cx-118, 386, 48, 93, 10, fill="#e7f7f5", width=5)
rect(cx-108, 400, 28, 54, 3, fill="#fffdf5", stroke=CYAN, width=3)
circle(cx-94, 466, 4, GOLD, width=1)
path(f'M{cx-59} 477 Q{cx-47} 439 {cx-9} 436 L{cx+31} 436 Q{cx+58} 439 {cx+75} 477 L{cx+98} 484 L{cx+94} 508 L{cx-62} 508 L{cx-69} 488Z', fill="#20c4ce", width=5)
path(f'M{cx-23} 442 L{cx+25} 442 Q{cx+44} 444 {cx+56} 469 L{cx-37} 469Z', fill="#e8f7f5", width=3)
circle(cx-35, 508, 14, NAVY, width=3)
circle(cx+65, 508, 14, NAVY, width=3)
circle(cx+1, 460, 12, "#ffd7b0", width=2)
path(f'M{cx-10} 456 Q{cx+1} 438 {cx+13} 456', stroke=NAVY, width=5)
path(f'M{cx+107} 405 C{cx+88} 390 {cx+76} 414 {cx+107} 438 C{cx+138} 414 {cx+126} 390 {cx+107} 405Z', fill="#fff0a0", width=4)
path(f'M{cx+91} 450 Q{cx+106} 446 {cx+121} 451', stroke=GOLD, width=5)

# Icon 4: feedback bubble, clarity marks and an unpaid rating invitation.
cx = centres[3]
path(f'M{cx-107} 394 Q{cx-104} 378 {cx-83} 378 L{cx+83} 378 Q{cx+109} 378 {cx+109} 402 L{cx+109} 469 Q{cx+108} 491 {cx+84} 491 L{cx-29} 491 L{cx-78} 521 L{cx-67} 491 Q{cx-105} 488 {cx-107} 465Z', fill="#e8f8f6", width=5)
for dx in (-50, -4, 42):
    circle(cx+dx, 432, 8, CYAN, width=2)
path(f'M{cx+85} 481 L{cx+96} 502 L{cx+119} 505 L{cx+102} 521 L{cx+106} 544 L{cx+85} 533 L{cx+65} 544 L{cx+69} 521 L{cx+52} 505 L{cx+75} 502Z', fill=GOLD, width=3)

# Icon 5: app notification plus a limited-validity bundle card.
cx = centres[4]
rect(cx-111, 382, 81, 133, 13, fill="#eaf8f6", width=5)
rect(cx-100, 399, 59, 91, 5, fill="#fffdf5", stroke=CYAN, width=3)
circle(cx-70, 502, 5, GOLD, width=2)
circle(cx-36, 405, 11, GOLD, width=2)
path(f'M{cx-70} 418 L{cx-70} 438 M{cx-82} 438 Q{cx-70} 431 {cx-58} 438', stroke=NAVY, width=3)
path(f'M{cx-14} 417 Q{cx+48} 403 {cx+98} 415 L{cx+104} 499 Q{cx+50} 506 {cx-7} 499Z', fill="#fff1a6", width=4)
path(f'M{cx+5} 437 Q{cx+45} 430 {cx+82} 437 M{cx+6} 455 Q{cx+45} 448 {cx+83} 455 M{cx+8} 476 Q{cx+45} 468 {cx+84} 476', stroke=CYAN, width=4)
circle(cx+93, 421, 5, GOLD, width=2)

# Stage titles, underlines and controlled display copy.
for i, (x, card) in enumerate(zip(card_xs, cards)):
    cx = centres[i]
    heading_size = 36
    while label_font.getlength(card["title"]) * heading_size / label_font.size > card_w - 24:
        heading_size -= 1
    add_text(card["title"], cx, 600, heading_size, label_font, f"stage-{i+1}-title", "centre")
    path(f'M{x+26} 618 Q{cx} 624 {x+card_w-25} 617', stroke=CYAN if i % 2 == 0 else GOLD, width=7, extra='opacity=".62"')
    baseline = 672
    for line in card["lines"]:
        size = 26 if i != 4 else 24
        box = add_text(line, cx, baseline, size, body_font, f"stage-{i+1}-body", "centre", min_size=20)
        if box[0] < x + 12 or box[2] > x + card_w - 12 or box[3] > card_y + card_h - 26:
            raise ValueError(f"Card text outside card: {line!r} {box}")
        baseline += 30 if i == 4 else 38

# Short left-to-right arrows connect the five stages.
for i in range(4):
    sx, ex = card_xs[i] + card_w + 7, card_xs[i + 1] - 8
    path(f'M{sx} 558 Q{(sx+ex)/2:.1f} 551 {ex} 558', stroke=CYAN, width=3.5, extra='marker-end="url(#arrow)"')
    path(f'M{sx+1} 564 Q{(sx+ex)/2:.1f} 561 {ex-5} 564', stroke=GOLD, width=2, extra='opacity=".75"')

# Return loop: a repeat offer is a test that may lead to another paid app booking.
path('M1596 1060 C1596 1103 1495 1115 1368 1115 L620 1115 C566 1115 550 1098 550 1061', stroke=CYAN, width=4, extra='marker-end="url(#arrow)"')
path('M1579 1066 C1566 1097 1458 1097 1358 1097 L638 1097', stroke=GOLD, width=2.5, extra='opacity=".78"')

parts.append('</svg>')
SVG_OUT.write_text("\n".join(parts), encoding="utf-8")
subprocess.run(["/opt/homebrew/bin/rsvg-convert", "-o", str(PNG_OUT), str(SVG_OUT)], check=True)

for i, left in enumerate(text_records):
    for right in text_records[i + 1:]:
        a, b = left["bbox"], right["bbox"]
        if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
            raise ValueError(f"Text overlap: {left['copy']!r} / {right['copy']!r}")

print(f"Rendered {SVG_OUT.name} and {PNG_OUT.name} at {WIDTH}x{HEIGHT}.")
print(f"Checked {len(text_records)} text groups for canvas bounds and pairwise text overlap.")
print(f"Logo bytes embedded: {len(LOGO.read_bytes())}; title bounds: {title_box}; subtitle bounds: {subtitle}.")
