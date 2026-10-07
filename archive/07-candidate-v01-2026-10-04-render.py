"""Render the standalone Section 7 budget infographic with local glyph paths."""

from pathlib import Path
from html import escape
import base64
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '07-candidate-v01-2026-10-04'
COPY_PATH = HERE / '07-copy-v01-2026-10-04.md'
ART_PATH = HERE / (PREFIX + '-generated-art.png')
GLYPH_SCRIPT = HERE / (PREFIX + '-glyphs.swift')
W, H = 1800, 1640

class TextEngine:
    def __init__(self, script):
        self.process = subprocess.Popen(['/usr/bin/swift', str(script)], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    def outline(self, value, font, size):
        request = json.dumps({'text': value, 'font': font, 'size': size}, ensure_ascii=False)
        self.process.stdin.write(request + '\n')
        self.process.stdin.flush()
        response = json.loads(self.process.stdout.readline())
        if 'error' in response:
            raise RuntimeError(response['error'])
        if response.get('text') != value:
            raise RuntimeError('CoreText returned a mismatched line')
        return response

    def close(self):
        self.process.stdin.close()
        self.process.wait(timeout=10)


class CoreTextFont:
    def __init__(self, name, engine):
        self.font_name = name
        self.engine = engine
        self.cache = {}

    def result(self, value, size):
        key = (value, size)
        if key not in self.cache:
            self.cache[key] = self.engine.outline(value, self.font_name, size)
        return self.cache[key]

    def width(self, value, size):
        return self.result(value, size)['width']

    def svg(self, value, x, baseline, size):
        path = escape(self.result(value, size)['path'], quote=True)
        return f'<path d="{path}" transform="translate({x:.3f} {baseline:.3f}) scale(1 -1)" fill="{INK}"/>'


engine = TextEngine(GLYPH_SCRIPT)
title_font = CoreTextFont('Marker Felt', engine)
body_font = CoreTextFont('Noteworthy', engine)

INK = '#173a47'
CYAN = '#26c6cf'
GOLD = '#ffd400'
PAPER = '#fffdf5'
MUTED = '#7d9da2'
texts = []
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
    '<defs>',
    f'<image id="budget-art" href="data:image/png;base64,{base64.b64encode(ART_PATH.read_bytes()).decode()}" width="2048" height="768"/>',
    '</defs>',
    '<path d="M34 37 Q452 27 900 35 T1766 38 Q1779 821 1764 1602 Q1328 1614 899 1608 T35 1604 Q23 816 34 37Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M48 49 Q881 40 1750 49" fill="none" stroke="#68c9cd" stroke-width="2" opacity=".62"/>',
    '<path d="M83 151 Q430 144 845 151" fill="none" stroke="#f7cc46" stroke-width="13" stroke-linecap="round" opacity=".74"/>',
]


def glyph_box(line, x, baseline, size, font):
    left, bottom, right, top = font.result(line, size)['bounds']
    return [round(x + left, 3), round(baseline - top, 3),
            round(x + right, 3), round(baseline - bottom, 3)]


def add_text(value, x, baseline, size, font=body_font, role='display', lines=None, line_height=None, centered=False):
    lines = lines or [value]
    assert ' '.join(lines) == value, (value, lines)
    if centered:
        x = (W - max(font.width(line, size) for line in lines)) / 2
    identifier = f'text-{len(texts):02d}'
    parts.append(f'<g id="{identifier}" data-role="{role}" aria-label="{escape(value, quote=True)}">')
    boxes = []
    for index, line in enumerate(lines):
        y = baseline + index * (line_height or size * 1.3)
        parts.append(font.svg(line, x, y, size))
        boxes.append({'text': line, 'bbox': glyph_box(line, x, y, size, font)})
    parts.append('</g>')
    texts.append({'id': identifier, 'text': value, 'role': role, 'font_size': size,
                  'font': font.font_name, 'lines': boxes})
    return identifier


def centered_text(value, baseline, size, font=body_font, role='display'):
    return add_text(value, 0, baseline, size, font, role, centered=True)


def rect(x, y, width, height, fill='none', stroke=MUTED, stroke_width=2, radius=20, opacity=1):
    parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{stroke_width}"/>')


def rule(x1, y1, x2, y2, colour=MUTED, width=2, opacity=.7):
    parts.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2} {y1 + 2} {x2} {y2}" fill="none" stroke="{colour}" stroke-width="{width}" opacity="{opacity}"/>')


def bar(x, y, width, colour=CYAN, max_width=150):
    parts.append(f'<rect x="{x}" y="{y}" width="{max_width}" height="12" rx="6" fill="#e6f1ee"/>')
    visible = max(4, max_width * width / 108000)
    parts.append(f'<path d="M{x} {y+6} Q{x+visible/2} {y+3} {x+visible} {y+6}" fill="none" stroke="{colour}" stroke-width="9" stroke-linecap="round"/>')


# Exact heading and envelope summary.
add_text('7. Budget & Resources', 80, 126, 76, title_font)
add_text('PROPOSED MARKET-ENTRY ENVELOPE · 12 MONTHS · EXCL. VAT', 88, 194, 31, title_font)
rule(82, 207, 1718, 207, CYAN, 2, .6)
rect(82, 226, 1636, 128, fill='#fbfcf5', stroke='#8aa9a6', stroke_width=2, radius=28)
add_text('TOTAL PROPOSED ALLOCATION', 118, 264, 26, title_font)
add_text('DKK600,000', 116, 338, 74, title_font)
parts.append('<svg x="1070" y="188" width="590" height="221" viewBox="0 0 2048 768" overflow="hidden" preserveAspectRatio="xMidYMid meet"><use href="#budget-art"/></svg>')

# People, the four costed company roles, and the seven other budget lines.
rect(80, 390, 790, 422, fill='#fffefa', stroke='#afc6c2', stroke_width=2, radius=24)
rect(930, 390, 790, 422, fill='#fffefa', stroke='#afc6c2', stroke_width=2, radius=24)
add_text('PEOPLE · 460 PROFESSIONAL HOURS', 110, 432, 31, title_font)
add_text('Assumed DKK600 per hour · company delivery roles', 112, 472, 22, body_font)
add_text('ROLE', 112, 506, 19, title_font, 'column-label')
add_text('AMOUNT', 610, 506, 19, title_font, 'column-label')
add_text('SHARE', 778, 506, 19, title_font, 'column-label')

people = [
    ('Research / analytics · 60h', 36000, 'DKK36,000', '6.00%'),
    ('Creative / localisation · 120h', 72000, 'DKK72,000', '12.00%'),
    ('Campaign management · 160h', 96000, 'DKK96,000', '16.00%'),
    ('CRM / support coordination · 120h', 72000, 'DKK72,000', '12.00%'),
]
for index, (label, amount, amount_label, share) in enumerate(people):
    y = 549 + index * 51
    add_text(label, 112, y, 21, body_font)
    bar(465, y - 15, amount, CYAN, 128)
    add_text(amount_label, 610, y, 22, title_font)
    add_text(share, 778, y, 20, body_font)
    if index < len(people) - 1:
        rule(110, y + 13, 840, y + 13, '#c9d9d5', 1, .7)
add_text('Hours by role: 60 · 120 · 160 · 120', 112, 765, 21, title_font)
add_text('Outside budget: cars · drivers · charging · frontline support', 112, 795, 18, body_font)

add_text('CHANNELS, TOOLS & RESERVES', 960, 432, 31, title_font)
add_text('Screens: planned 200,000 impressions ÷ 1,000 × DKK191 CPM = DKK38,200', 962, 463, 17, body_font)
add_text('Published 2026 rate card · DKK4,995 setup · not a supplier quote', 962, 486, 17, body_font)
add_text('LINE', 962, 516, 19, title_font, 'column-label')
add_text('AMOUNT', 1433, 516, 19, title_font, 'column-label')
add_text('SHARE', 1602, 516, 19, title_font, 'column-label')
items = [
    ('Paid search · proposed envelope', 108000, 'DKK108,000', '18.00%'),
    ('Paid social · proposed envelope', 90000, 'DKK90,000', '15.00%'),
    ('Street screens · published rate card', 38200, 'DKK38,200', '6.37%'),
    ('Screen setup · published rate card', 4995, 'DKK4,995', '0.83%'),
    ('Tools · DKK2,500 monthly', 30000, 'DKK30,000', '5.00%'),
    ('Vouchers · 400 × DKK30 cap', 12000, 'DKK12,000', '2.00%'),
    ('Contingency · residual, uncommitted', 40805, 'DKK40,805', '6.80%'),
]
for index, (label, amount, amount_label, share) in enumerate(items):
    y = 547 + index * 36
    add_text(label, 962, y, 19, body_font)
    bar(1270, y - 14, amount, GOLD, 125)
    add_text(amount_label, 1433, y, 20, title_font)
    add_text(share, 1602, y, 19, body_font)
    if index < len(items) - 1:
        rule(960, y + 10, 1688, y + 10, '#c9d9d5', 1, .6)

# Five stages plus the separately held reserve.
rule(86, 842, 1714, 842, CYAN, 2, .55)
add_text('STAGED RELEASE · CASH BY PERIOD', 88, 884, 34, title_font)
add_text('Five proposed stages · contingency remains separate', 90, 918, 22, body_font)
stages = [
    ('M1–2', 101000, 'DKK101,000'),
    ('M3–4', 76000, 'DKK76,000'),
    ('M5–6', 88000, 'DKK88,000'),
    ('M7–9', 183695, 'DKK183,695'),
    ('M10–12', 110500, 'DKK110,500'),
]
stage_x = [90, 420, 750, 1080, 1410]
for (period, amount, amount_label), x in zip(stages, stage_x):
    rect(x, 944, 300, 106, fill='#fffefa', stroke='#afc6c2', stroke_width=2, radius=18)
    add_text(period, x + 16, 981, 25, title_font)
    add_text(amount_label, x + 16, 1021, 28, title_font)
    track = min(260, 260 * amount / 183695)
    parts.append(f'<path d="M{x+18} 1038 Q{x+18+track/2} 1035 {x+18+track} 1038" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>')

add_text('Stage cash DKK559,195 + separate uncommitted contingency DKK40,805 = DKK600,000', 92, 1090, 24, title_font)
add_text('Committed before Gate A · DKK177,000', 92, 1123, 22, body_font)
add_text('Committed before Gate B · DKK265,000', 930, 1123, 22, body_font)

# Gate cards use the matching panel-8 thresholds and pass/fail actions.
rect(80, 1148, 790, 252, fill='#fffefa', stroke='#9cbcb8', stroke_width=2, radius=22)
rect(930, 1148, 790, 240, fill='#fffefa', stroke='#9cbcb8', stroke_width=2, radius=22)
add_text('GATE A · M4', 110, 1190, 32, title_font)
add_text('Completed / accepted ≥95% · service cancels ≤2%', 112, 1230, 21, body_font)
add_text('Referenced complaints answered in 24h ≥90%', 112, 1265, 21, body_font)
add_text('Search conversion ≥1.5% · social ≥0.8%', 112, 1300, 21, body_font)
add_text('Agree minimum observed volume with operations', 112, 1334, 20, body_font)
add_text('Pass releases M5–6 · fail: hold, fix and retest', 112, 1372, 20, title_font)

add_text('GATE B · M6', 960, 1190, 32, title_font)
add_text('Continue: mature 90-day repeat ≥20%', 962, 1230, 22, body_font)
add_text('and paid cost / first rider ≤DKK1,829', 962, 1265, 22, body_font)
add_text('Repeat ≥35% releases street screens', 962, 1300, 22, body_font)
add_text('Otherwise stop scale-up', 962, 1350, 21, title_font)

# Transparent economics strip: modelled return remains below the envelope.
rect(80, 1416, 1640, 160, fill='#fff9dc', stroke='#e5c94c', stroke_width=2, radius=24)
add_text('ILLUSTRATIVE · ASSUMPTION-BASED · NOT OBSERVED COMPANY SPENDING', 112, 1455, 24, title_font)
add_text('378 first riders · about 676 rides · DKK227 fare proxy · 30% assumed contribution', 112, 1492, 23, body_font)
add_text('About DKK554,000 remains unrecovered · break-even requires 8,811 rides', 112, 1538, 29, title_font)

parts.append('</svg>')
svg_path = HERE / (PREFIX + '.svg')
svg_path.write_text('\n'.join(parts), encoding='utf-8')

for suffix, options in [('.png', []), ('-small.png', ['-w', '900'])]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', *options, '-o', str(HERE / (PREFIX + suffix)), str(svg_path)], check=True)

manifest = {
    'panel': 7,
    'status': 'Complete visual candidate; parent acceptance pending',
    'authority': 'Delegated by parent on 4 October 2026; no group approval claimed',
    'dimensions': [W, H],
    'copy_source': COPY_PATH.name,
    'visible_text': texts,
    'internal_decisions': ['D-032', 'D-033'],
    'internal_evidence': ['E-029'],
    'assumptions': ['DKK600/hour role cost', 'search and social envelopes', 'DKK2,500 monthly tools', '400 vouchers at DKK30', 'contingency residual', 'illustrative economics'],
    'screen_cost_treatment': 'Published 2026 rate-card basis, not a supplier quote',
    'excluded_operating_costs': ['cars', 'drivers', 'charging', 'frontline support'],
    'generated_art_sha256': hashlib.sha256(ART_PATH.read_bytes()).hexdigest(),
    'svg_sha256': hashlib.sha256(svg_path.read_bytes()).hexdigest(),
    'visible_citations': False,
    'text_as_glyph_paths': True,
}
(HERE / (PREFIX + '-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
engine.close()
print('Rendered complete Section 7 candidate:', (HERE / (PREFIX + '.png')).resolve())
