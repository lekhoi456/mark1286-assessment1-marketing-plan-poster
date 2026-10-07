"""Compose the approved Section 5 words and text-free illustration atlas."""
from pathlib import Path
from html import escape
import base64
import json
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = "05-v09-candidate-2026-10-04"
INK, CYAN, GOLD, PAPER = "#173a47", "#28bdbf", "#e3bb42", "#fffdf5"
W, H = 1800, 1400
FONT = "ChalkboardSE"
SHIFT = 0
proc = subprocess.Popen(["/usr/bin/swift", str(HERE / "05-v09-glyphs-2026-10-04.swift")],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True)
texts, placements = [], []
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
atlas = HERE / "05-v09-illustration-atlas-2026-10-04.png"
data = base64.b64encode(atlas.read_bytes()).decode("ascii")


def text(value, x, y, size=28, font=FONT, role="body", align="left"):
    proc.stdin.write(json.dumps({"text": value, "font": font, "size": size}, ensure_ascii=False) + "\n")
    proc.stdin.flush()
    glyph = json.loads(proc.stdout.readline())
    if "error" in glyph:
        raise RuntimeError(glyph["error"])
    if align == "center":
        x -= glyph["width"] / 2
    x0, y0, x1, y1 = glyph["bounds"]
    box = [round(x+x0, 2), round(y-y1+SHIFT, 2), round(x+x1, 2), round(y-y0+SHIFT, 2)]
    identifier = f"text-{len(texts):02d}"
    parts.append(f'<g id="{identifier}" aria-label="{escape(value, quote=True)}" data-role="{role}">'
                 f'<path d="{escape(glyph["path"], quote=True)}" transform="translate({x:.3f} {y:.3f}) scale(1 -1)" fill="{INK}"/></g>')
    texts.append({"id": identifier, "text": value, "font": font, "size": size, "role": role, "bbox": box})


def title(value, x, y, size=30):
    text(value, x, y, size, "MarkerFelt-Wide", "heading")


def line(path, color=INK, width=2, opacity=1):
    parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')


def box(x, y, w, h, fill="none", stroke=INK, width=2, r=12):
    path = (f'M{x+r} {y+2} Q{x+w/2} {y-1} {x+w-r} {y+2} '
            f'Q{x+w+2} {y+h/2} {x+w-1} {y+h-r} '
            f'Q{x+w/2} {y+h+2} {x+r} {y+h-1} Q{x-1} {y+h/2} {x+r} {y+2}Z')
    parts.append(f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')


def arrow(path, end_x, end_y, color=CYAN, direction="right", width=4):
    line(path, color, width)
    if direction == "up":
        line(f'M{end_x-8} {end_y+12} L{end_x} {end_y} L{end_x+8} {end_y+12}', color, width)
    else:
        line(f'M{end_x-11} {end_y-7} L{end_x} {end_y} L{end_x-11} {end_y+7}', color, width)


def art(name, source, x, y, w, h, stretch=False):
    crop = " ".join(map(str, source))
    aspect = "none" if stretch else "xMidYMid meet"
    clip = f'illustration-clip-{len(placements)}'
    sx, sy, sw, sh = source
    parts.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{crop}" preserveAspectRatio="{aspect}" overflow="hidden" aria-label="{name}">'
                 f'<defs><clipPath id="{clip}"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}"/></clipPath></defs>'
                 f'<image x="0" y="0" width="1536" height="1024" clip-path="url(#{clip})" href="data:image/png;base64,{data}"/></svg>')
    placements.append({"asset": atlas.name, "name": name, "source_viewbox": source,
                       "destination": [x, y+SHIFT, w, h], "stretch": stretch})


def icon(kind, x, y, scale=1):
    parts.append(f'<g transform="translate({x} {y}) scale({scale})">')
    if kind == "car":
        line('M0 25 L8 10 Q23 4 40 10 L49 25 L47 35 L2 35Z', CYAN, 3)
        parts.append(f'<circle cx="11" cy="36" r="5" fill="{INK}"/><circle cx="39" cy="36" r="5" fill="{INK}"/>')
    elif kind == "tag":
        line('M0 7 L32 7 L48 23 L32 39 L0 39Z', INK, 3)
        parts.append(f'<circle cx="10" cy="17" r="4" fill="{GOLD}"/>')
    elif kind == "pin":
        line('M24 43 Q0 18 12 7 Q24 -4 36 7 Q48 18 24 43Z', CYAN, 3)
        parts.append(f'<circle cx="24" cy="14" r="5" fill="{GOLD}"/>')
    elif kind == "speaker":
        line('M0 17 L33 5 L33 35 L0 27Z M7 28 L13 42 L24 42 L20 31', INK, 3)
        line('M39 9 L47 5 M40 20 L50 20 M39 31 L47 36', GOLD, 4)
    elif kind == "search":
        parts.append(f'<circle cx="15" cy="15" r="10" fill="none" stroke="{INK}" stroke-width="3"/>')
        line('M23 23 L36 36', CYAN, 4)
    elif kind == "faq":
        box(0, 0, 42, 42, "#e5f7f5", INK, 2, 5)
        line('M8 11 L34 11 M8 20 L34 20 M8 29 L34 29', CYAN, 3)
    elif kind == "video":
        box(0, 0, 47, 58, "#e5f7f5", INK, 2, 6)
        parts.append(f'<path d="M15 15 L15 42 L37 28Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>')
    elif kind == "consent":
        box(0, 2, 25, 25, "#e5f7f5", INK, 2, 3)
        line('M5 14 L11 20 L21 7', CYAN, 3)
    elif kind == "privacy":
        line('M3 11 L3 27 L25 27 L25 11Z M8 11 L8 6 Q14 -3 20 6 L20 11', INK, 2.5)
        parts.append(f'<circle cx="14" cy="18" r="3" fill="{GOLD}"/>')
    elif kind == "access":
        parts.append(f'<circle cx="8" cy="10" r="7" fill="none" stroke="{INK}" stroke-width="2.5"/>')
        line('M14 14 L28 28 M23 23 L27 18 M27 27 L32 22', CYAN, 3)
    parts.append('</g>')


# Tight title and horizontal evidence strip preserve scope beside each number.
line('M30 31 Q894 20 1771 32 L1767 1370 Q888 1382 31 1371Z', INK, 3)
line('M52 47 Q878 41 1745 49', CYAN, 2, .6)
title('5. Digital Marketing', 72, 94, 60)
line('M73 105 Q408 111 757 104', GOLD, 9)
text('Copenhagen · ages 25–44 · repeat self-paying taxi riders', 74, 137, 28)
title('5.1 CUSTOMER INSIGHT', 73, 177, 29)
box(65, 189, 1668, 126, '#eefafa', '#81b9bc', 2, 12)
text('DENMARK · INSTALLED TAXI APPS · n=1,005', 87, 220, 24)
text('CAPITAL REGION · last-trip app-choice reasons · n=79', 796, 220, 24)
title('40–50%', 85, 282, 57)
text('have one app.', 304, 273, 30)
title('57%', 795, 278, 53)
text('lower price', 905, 270, 28)
text('·', 1067, 270, 28)
title('22%', 1100, 278, 53)
text('usual app', 1211, 270, 28)
text('· multi-select.', 1370, 270, 24)
text('Separate samples · not specific to ages 25–44.', 87, 308, 23, role='caveat')

# The four Ps use small relevant icons and no unsupported operational claim.
parts.append('<g transform="translate(0 -12)">')
SHIFT = -12
title('5.2 MARKETING MIX · 4Ps', 73, 355, 29)
mix = [(87, 'PRODUCT', 'ELECTRIC RIDE +', 'CONTROLLED SERVICE*', 'car'),
       (510, 'PRICE', 'CLEAR FARE +', 'TRIAL OFFER*', 'tag'),
       (932, 'PLACE', 'COPENHAGEN PAGE →', 'GREEN SM APP', 'pin'),
       (1350, 'PROMOTION', 'SEARCH + SOCIAL +', 'REMINDERS', 'speaker')]
for x, label, first, second, kind in mix:
    icon(kind, x, 367, .85)
    title(label, x+59, 399, 28)
    text(first, x, 432, 28)
    text(second, x, 464, 28)
text('*Proposed service and trial offer.', 88, 493, 23, role='caveat')
line('M70 507 Q902 502 1731 507', CYAN, 2, .7)
parts.append('</g>')
SHIFT = 0

# Three concrete acquisition specimens converge on one connected service route.
parts.append('<g transform="translate(0 -35)">')
SHIFT = -35
title('5.3 OMNI CHANNEL', 74, 548, 31)
for kind, label, x in [('consent', 'consent', 1280), ('privacy', 'privacy', 1440), ('access', 'access', 1600)]:
    icon(kind, x, 523, .9)
    text(label, x+34, 548, 23, role='safeguard')
box(87, 568, 475, 70, '#fffbea', '#b9c6bd', 1.8, 8)
title('PAID SEARCH', 102, 594, 27)
icon('search', 105, 604, .65)
text('“electric taxi Copenhagen”', 137, 627, 28)
box(87, 651, 475, 69, '#f1fafa', '#b9c6bd', 1.8, 8)
icon('faq', 105, 666, .85)
title('SEO', 158, 678, 27)
text('fare / area / booking FAQs', 158, 707, 28)
box(87, 735, 475, 97, '#fffbea', '#b9c6bd', 1.8, 8)
icon('video', 105, 755, .85)
title('SOCIAL CONTENT', 167, 763, 27)
text('short electric-ride +', 167, 794, 28)
text('booking demos', 167, 824, 28)
line('M565 602 L614 602 L614 777 L565 777', CYAN, 3)
line('M565 684 L614 684', CYAN, 3)
arrow('M614 684 L666 684', 666, 684)
art('Copenhagen information page and FAQs', [30, 78, 525, 491], 673, 592, 246, 194)
art('Green SM app route and booking screen', [632, 64, 276, 491], 1021, 570, 214, 215)
art('Electric taxi ride and help', [919, 95, 617, 440], 1368, 589, 329, 197)
arrow('M923 684 L1007 684', 1007, 684)
arrow('M1240 684 L1356 684', 1356, 684)
title('COPENHAGEN PAGE', 660, 822, 29)
title('GREEN SM APP', 1020, 822, 29)
title('RIDE + HELP', 1430, 822, 29)
text('Consistent fares, offers and help across channels.', 88, 865, 28)

# The return loop makes reminder intent a hypothesis and keeps paid repeat explicit.
for value, centre in [('Trip history', 189), ('likely need', 540), ('opt-in reminder', 909), ('paid repeat.', 1283)]:
    text(value, centre, 918, 28, align='center')
for a, b in [(287, 439), (641, 753), (1060, 1175)]:
    arrow(f'M{a} 906 L{b} 906', b, 906, GOLD, width=3.5)
arrow('M1283 928 Q1283 950 1255 950 L215 950 Q189 950 189 931', 189, 931, CYAN, 'up', 3)
art('Trip record and relevant reminder illustration', [1027, 578, 509, 370], 1467, 869, 220, 98)
columns = [(87, 'CDP* · join trip, app and', 'consent records'),
           (645, 'Big Data* · identify repeat', 'patterns at scale'),
           (1192, 'Marketing AI* · suggest', 'reminder timing/message')]
for x, first, second in columns:
    text(first, x, 993, 28)
    text(second, x, 1025, 28)
text('*Proposed after data/system checks · human review.', 88, 1055, 23, role='caveat')
parts.append('<g transform="translate(0 -31)">')
SHIFT = -66

# The voucher and paid package are distinct bounded pilot mechanics.
title('5.4 VOUCHER + 30-DAY PACKAGE', 75, 1130, 29)
text('Vietnam mechanics → Copenhagen pilot.', 88, 1164, 28)
art('One-ride discount voucher', [24, 643, 550, 289], 79, 1178, 451, 129, True)
title('10–20%', 192, 1240, 53)
text('OFF ONE RIDE', 193, 1275, 29)
box(584, 1178, 596, 129, '#effafa', '#7caeb0', 2, 11)
art('Paid 30-day package calendar', [580, 582, 440, 377], 596, 1190, 113, 106)
title('30-DAY PACKAGE', 729, 1222, 36)
text('proposed paid offer', 730, 1262, 28)
text('Measure redemption +', 1220, 1206, 28)
text('paid repeats.', 1220, 1239, 28)
text('Cost cap: align Sections 6/7.', 1220, 1280, 28)

# A real three-stage timeline retains both release gates.
title('5.5 TIMELINE', 75, 1340, 29)
stages = [(85, 498, 'M1–2', 'verify service/data'),
          (645, 502, 'M3–6', 'test content/offers · M4/M6 gates'),
          (1207, 506, 'M7–12', 'refine · scale after gates')]
for index, (x, width, month, activity) in enumerate(stages):
    box(x, 1353, width, 75, '#effafa' if index != 1 else '#fff8d9', '#7caeb0', 2, 8)
    title(month, x+16, 1388, 34)
    text(activity, x+16, 1417, 27)
    if index < 2:
        arrow(f'M{x+width+7} 1392 L{x+width+47} 1392', x+width+47, 1392, CYAN, width=3)

parts.append('</g></g></svg>')
proc.stdin.close()
proc.wait(timeout=10)
if proc.returncode:
    raise RuntimeError(proc.stderr.read())
svg = HERE / f'{PREFIX}.svg'
svg.write_text('\n'.join(parts), encoding='utf-8')
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(HERE / f'{PREFIX}.png'), str(svg)], check=True)
manifest = {'panel': 5, 'version': 'v09', 'dimensions': [W, H],
            'copy_source': '05-v09-copy-2026-10-04.md', 'approval_decision': 'D-089',
            'controlled_lettering': 'CoreText glyph outlines with aria-label metadata',
            'palette': {'paper': PAPER, 'navy': INK, 'New Cyan': CYAN, 'New Yellow': GOLD},
            'visible_text': texts, 'illustration_placements': placements,
            'generated_art': atlas.name, 'builtin_imagegen': True,
            'scope': 'Section 5 only; visual candidate, no group/A0/print acceptance claim'}
(HERE / '05-v09-placement-manifest-2026-10-04.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Rendered {svg.name}; {len(texts)} text groups; {len(placements)} illustration placements')
