"""Render Section 7 v04 as a hand-drawn, data-led budget panel."""

from html import escape
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = "07-v04-candidate-2026-10-04"
COPY = HERE / "07-v03-copy-2026-10-04.md"
W, H = 1800, 1540
INK, CYAN, GOLD = "#173a47", "#26c6cf", "#ffd400"
PAPER, MUTED = "#fffdf5", "#7d9da2"


class Glyphs:
    def __init__(self):
        self.proc = subprocess.Popen(["/usr/bin/swift", str(HERE / "07-v04-glyphs.swift")],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
        self.cache = {}

    def get(self, value, font, size):
        key = (value, font, size)
        if key not in self.cache:
            request = json.dumps({"text": value, "font": font, "size": size}, ensure_ascii=False)
            self.proc.stdin.write(request + "\n")
            self.proc.stdin.flush()
            response = json.loads(self.proc.stdout.readline())
            if "error" in response:
                raise RuntimeError(response["error"])
            self.cache[key] = response
        return self.cache[key]

    def close(self):
        self.proc.stdin.close()
        self.proc.wait(timeout=10)
        error = self.proc.stderr.read()
        if self.proc.returncode:
            raise RuntimeError(error)


engine = Glyphs()
texts = []
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']


def text(value, x, baseline, size, font="Noteworthy", role="display"):
    response = engine.get(value, font, size)
    x0, y0, x1, y1 = response["bounds"]
    bounds = [round(x + x0, 2), round(baseline - y1, 2),
              round(x + x1, 2), round(baseline - y0, 2)]
    identifier = f"text-{len(texts):02d}"
    path = escape(response["path"], quote=True)
    parts.append(f'<g id="{identifier}" data-role="{role}" aria-label="{escape(value, quote=True)}">'
                 f'<path d="{path}" transform="translate({x:.3f} {baseline:.3f}) scale(1 -1)" fill="{INK}"/></g>')
    texts.append({"id": identifier, "text": value, "role": role, "font": font,
                  "font_size": size, "bbox": bounds})


def title(value, x, y, size): text(value, x, y, size, "Marker Felt", "heading")


def line(d, colour=MUTED, width=2, opacity=1):
    parts.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')


def box(x, y, w, h, fill="none", stroke=MUTED, width=2, radius=12):
    d = (f'M{x+radius} {y+2} Q{x+w/2} {y-2} {x+w-radius} {y+2} '
         f'Q{x+w+2} {y+h/3} {x+w-1} {y+h-radius} '
         f'Q{x+w/2} {y+h+2} {x+1} {y+h-radius} Q{x-2} {y+h/2} {x+radius} {y+2}Z')
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')


def bar(x, y, width, colour, height=27):
    parts.append(f'<path d="M{x} {y+4} Q{x+width*.48} {y-1} {x+width} {y+3} '
                 f'L{x+width} {y+height-3} Q{x+width*.56} {y+height+1} {x} {y+height-2}Z" '
                 f'fill="{colour}"/>')


def icon(kind, x, y, colour):
    if kind == "people":
        line(f'M{x+2} {y+34} Q{x+3} {y+17} {x+17} {y+17} Q{x+31} {y+17} {x+33} {y+34}', INK, 3)
        line(f'M{x+27} {y+34} Q{x+29} {y+22} {x+39} {y+22} Q{x+49} {y+22} {x+51} {y+34}', INK, 3)
        for cx, cy in [(x+18, y+10), (x+40, y+15)]:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{PAPER}" stroke="{colour}" stroke-width="4"/>')
    elif kind == "search":
        parts.append(f'<circle cx="{x+17}" cy="{y+17}" r="12" fill="none" stroke="{INK}" stroke-width="3"/>')
        line(f'M{x+26} {y+26} L{x+41} {y+41}', colour, 5)
    elif kind == "social":
        line(f'M{x+4} {y+19} L{x+35} {y+8} L{x+35} {y+34} L{x+4} {y+24}Z', INK, 3)
        line(f'M{x+10} {y+26} L{x+15} {y+39} L{x+23} {y+39} L{x+19} {y+29}', colour, 3)
        line(f'M{x+41} {y+13} Q{x+48} {y+21} {x+41} {y+29}', GOLD, 3)
    elif kind == "screen":
        box(x+3, y+1, 41, 37, "#e5f7f5", INK, 2, 4)
        line(f'M{x+10} {y+10} Q{x+24} {y+8} {x+37} {y+10}', colour, 3)
        line(f'M{x+10} {y+18} Q{x+23} {y+16} {x+36} {y+18}', colour, 3)
    elif kind == "reserve":
        line(f'M{x+4} {y+8} Q{x+20} {y+3} {x+39} {y+9} L{x+36} {y+29} Q{x+21} {y+42} {x+7} {y+29}Z', INK, 3)
        line(f'M{x+14} {y+20} L{x+20} {y+26} L{x+31} {y+14}', colour, 4)
    elif kind == "tools":
        parts.append(f'<circle cx="{x+23}" cy="{y+21}" r="16" fill="none" stroke="{INK}" stroke-width="3"/>')
        parts.append(f'<circle cx="{x+23}" cy="{y+21}" r="6" fill="{PAPER}" stroke="{colour}" stroke-width="3"/>')
        for angle in range(0, 360, 60):
            import math
            a = math.radians(angle)
            line(f'M{x+23+18*math.cos(a):.1f} {y+21+18*math.sin(a):.1f} L{x+23+24*math.cos(a):.1f} {y+21+24*math.sin(a):.1f}', INK, 3)
    else:
        line(f'M{x+5} {y+10} L{x+40} {y+10} L{x+40} {y+31} L{x+5} {y+31}Z', INK, 3)
        line(f'M{x+13} {y+10} L{x+13} {y+31}', colour, 3)
        line(f'M{x+23} {y+10} L{x+23} {y+31}', colour, 3)


# Shared Section 5/6/8 language: marker lettering, cream stock, ink frame, cyan rules and yellow emphasis.
line("M34 38 Q452 28 900 36 T1766 39 Q1778 770 1764 1494 Q1328 1504 899 1500 T35 1494 Q23 766 34 38Z", "#264654", 3)
line("M48 50 Q881 40 1750 50", "#68c9cd", 2, .8)
title("7. Budget & Resources", 80, 113, 68)
line("M82 151 Q420 159 835 151", GOLD, 9)
text("DKK600,000 · 12 months · excluding VAT · proposed allocation", 82, 185, 25)
line("M72 207 Q880 203 1728 207", CYAN, 2, .75)

# Allocation bars use one common DKK scale; the complete envelope is reconciled across seven visible groups.
box(77, 225, 1645, 475, "#fffefa", "#9ab0b1", 2, 10)
title("WHERE THE MONEY GOES", 103, 262, 25)
text("Local delivery and paid trial lead. Screens wait for repeat evidence.", 104, 288, 19)
items = [
    ("Marketing delivery team", "460h × assumed DKK600/hour", 276000, "46.0%", "people", "#26c6cf"),
    ("Paid search", "Proposed channel envelope", 108000, "18.0%", "search", "#26c6cf"),
    ("Paid social", "Proposed channel envelope", 90000, "15.0%", "social", "#26c6cf"),
    ("Street screens + setup", "200k planned impressions · held until Gate B", 43195, "7.2%", "screen", GOLD),
    ("Uncommitted contingency", "Separate reserve · outside release stages", 40805, "6.8%", "reserve", GOLD),
    ("Analytics + CRM tools", "12 months · assumed DKK2,500/month", 30000, "5.0%", "tools", "#82cdd0"),
    ("First-ride vouchers", "Capped at 400 × DKK30", 12000, "2.0%", "voucher", GOLD),
]
bar_x, bar_w = 625, 620
max_scale = 300000
row_top, row_step = 322, 51
for index, (label, note, amount, share, icon_name, colour) in enumerate(items):
    y = row_top + index * row_step
    icon(icon_name, 102, y - 24, colour)
    title(label, 165, y + 1, 21)
    text(note, 166, y + 23, 16)
    parts.append(f'<path d="M{bar_x} {y-17} Q{bar_x+bar_w/2} {y-20} {bar_x+bar_w} {y-17} '
                 f'L{bar_x+bar_w} {y+12} Q{bar_x+bar_w/2} {y+15} {bar_x} {y+12}Z" fill="#e9f0ed"/>')
    bar(bar_x, y - 17, bar_w * amount / max_scale, colour, 29)
    title(f"DKK{amount:,}", 1270, y + 1, 20)
    text(share, 1535, y + 1, 19)
    if index in (0, 3):
        line(f"M165 {y+31} Q870 {y+33} 1690 {y+31}", "#b8c8c5", 1, .6)

for value, label in [(0, "0"), (100000, "100k"), (200000, "200k"), (300000, "300k")]:
    x = bar_x + bar_w * value / max_scale
    line(f"M{x:.1f} 682 L{x:.1f} 688", MUTED, 1.5)
    text(label, x - (7 if value == 0 else 20), 691, 13)
text("Four roles: research/service checks · local creative · campaign management · CRM/help handover.", 104, 718, 16)
text("Screens: 2026 rate-card estimate. Outside marketing budget: cars · drivers · charging · frontline support.", 104, 744, 16)

# Five stage labels carry the M1–M12 sequence without repeating every stage allocation.
title("12-MONTH RELEASE ROUTE", 82, 780, 27)
stages = [("M1–2", "Prepare"), ("M3–4", "Gate A · end of M4"), ("M5–6", "Gate B · end of M6"),
          ("M7–9", "Screens if mature 90-day repeat ≥35%"), ("M10–12", "Review")]
stage_x = [78, 408, 738, 1068, 1398]
stage_width = 300
for i, ((period, label), x) in enumerate(zip(stages, stage_x)):
    box(x, 792, stage_width, 95, "#f0fafa" if i % 2 == 0 else "#fffbea", "#68878c", 2, 12)
    line(f"M{x+14} 802 Q{x+stage_width/2} 798 {x+stage_width-14} 803", CYAN if i % 2 == 0 else GOLD, 6)
    title(period, x + 17, 839, 23)
    text(label, x + 17, 869, 16)
    if i < 4:
        line(f"M{x+stage_width+5} 841 Q{x+stage_width+16} 833 {x+stage_width+27} 841", CYAN, 3)

# Exposure bar gives the two release gates a visible scale against the full budget.
box(78, 904, 1644, 205, "#fffefa", "#9ab0b1", 2, 12)
title("CASH EXPOSED BEFORE EACH GATE", 104, 941, 24)
text("Fail: hold, fix, retest · full thresholds in Section 8 · total envelope DKK600,000", 105, 967, 17)
gx, gw, gy = 122, 1500, 1026
parts.append(f'<path d="M{gx} {gy-14} Q{gx+gw/2} {gy-17} {gx+gw} {gy-14} L{gx+gw} {gy+17} Q{gx+gw/2} {gy+20} {gx} {gy+17}Z" fill="#e9f0ed"/>')
bar(gx, gy - 14, gw * 265000 / 600000, CYAN, 31)
bar(gx, gy - 14, gw * 177000 / 600000, GOLD, 31)
marker_a = gx + gw * 177000 / 600000
marker_b = gx + gw * 265000 / 600000
line(f"M{marker_a:.1f} 1012 L{marker_a:.1f} 1056", INK, 2)
line(f"M{marker_b:.1f} 1012 L{marker_b:.1f} 1056", INK, 2)
text("M4 · Gate A · DKK177,000 · 29.5%", 115, 1007, 15)
text("M6 · Gate B · DKK265,000 · 44.2%", 715, 1007, 15)
text("DKK335,000 remains unreleased at M6, including the separate DKK40,805 contingency.", 105, 1085, 16)

# Economics keeps the approved market-entry trade-off honest and legible.
box(78, 1127, 1644, 330, "#fff9dc", "#d2bc44", 2, 18)
title("YEAR ONE · ILLUSTRATIVE CASE DOES NOT BREAK EVEN", 105, 1168, 24)
title("676 rides", 108, 1224, 38)
text("modelled", 110, 1250, 17)
line("M302 1224 Q490 1217 671 1224", CYAN, 4)
title("8,811 rides", 703, 1224, 38)
text("needed to cover DKK600,000 at assumed 30% contribution", 705, 1250, 17)
text("Illustrative rides as a share of break-even", 110, 1293, 17)
track_x, track_w, track_y = 110, 1420, 1313
parts.append(f'<path d="M{track_x} {track_y} Q{track_x+track_w/2} {track_y-3} {track_x+track_w} {track_y}L{track_x+track_w} {track_y+19}Q{track_x+track_w/2} {track_y+22} {track_x} {track_y+19}Z" fill="#e7e9df"/>')
bar(track_x, track_y, track_w * 675.675 / 8811, CYAN, 20)
title("~8% of break-even rides", 110, 1354, 17)
title("About DKK554,000 remains unrecovered.", 110, 1390, 25)
text("Assumptions: DKK227 fare proxy · 30% contribution · no lifetime value claimed. Market entry, not year-one payback.", 110, 1427, 16)
line("M1210 1447 Q1390 1440 1660 1448", GOLD, 7, .85)

parts.append("</svg>")
engine.close()
svg_path = HERE / f"{PREFIX}.svg"
svg_path.write_text("\n".join(parts), encoding="utf-8")
for suffix, args in [(".png", []), ("-small.png", ["-w", "900"])]:
    subprocess.run(["/opt/homebrew/bin/rsvg-convert", *args, "-o", str(HERE / f"{PREFIX}{suffix}"), str(svg_path)], check=True)

manifest = {
    "panel": 7,
    "status": "V04 artwork and v03 copy accepted by the student for assembly on 4 October 2026; no group or A0 approval claimed",
    "dimensions": [W, H],
    "copy_source": COPY.name,
    "design_reference": ["05-v07-candidate-2026-10-04.png", "06-v06-candidate.png", "08-v04.png"],
    "visible_text": texts,
    "allocation_rows": [{"item": item[0], "amount_dkk": item[2], "share": item[3]} for item in items],
    "internal_decisions": ["D-032", "D-033"],
    "internal_evidence": ["E-029"],
    "visual_notes": "Logo-free Section 5/6/8 marker style, proportional DKK allocation bars, five-stage route, cash exposure scale and illustrative break-even comparison.",
    "scope_limits": ["A0 fit and print-distance legibility untested", "All proposed line items and assumptions remain subject to the recorded approval state"],
}
(HERE / f"{PREFIX}-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Rendered {svg_path.name}; {len(texts)} outlined text groups")
