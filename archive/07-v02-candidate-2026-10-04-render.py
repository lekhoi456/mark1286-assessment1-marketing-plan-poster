"""Render the standalone Section 7 budget infographic with local glyph paths."""

from pathlib import Path
from html import escape
import base64
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '07-v02-candidate-2026-10-04'
COPY_PATH = HERE / '07-v02-copy-2026-10-04.md'
LOGO_PATH = HERE / 'shared-logo.png'
GLYPH_SCRIPT = HERE / '07-v02-glyphs.swift'
W, H = 1800, 1540

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
    f'<image id="shared-logo" href="data:image/png;base64,{base64.b64encode(LOGO_PATH.read_bytes()).decode()}" width="2171" height="724"/>',
    '</defs>',
    '<path d="M34 37 Q452 27 900 35 T1766 38 Q1779 770 1764 1494 Q1328 1504 899 1500 T35 1494 Q23 766 34 37Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M48 49 Q881 40 1750 49" fill="none" stroke="#68c9cd" stroke-width="2" opacity=".62"/>',
    '<path d="M83 180 Q430 173 845 180" fill="none" stroke="#f7cc46" stroke-width="7" stroke-linecap="round" opacity=".74"/>',
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


# Section 5 header system: exact panel label, short subtitle and the supplied shared lockup.
add_text('7. Budget & Resources', 80, 112, 68, title_font)
add_text('Market-entry envelope · 12 months · excluding VAT', 82, 166, 25, body_font)
logo_uri = base64.b64encode(LOGO_PATH.read_bytes()).decode()
parts.append(f'<image id="display-logo" x="1420" y="40" width="300" height="100" href="data:image/png;base64,{logo_uri}" preserveAspectRatio="xMidYMid meet"/>')
rule(72, 194, 1728, 194, CYAN, 2, .65)

# The hero strip makes the cap and decision status immediate.
rect(76, 211, 1648, 105, fill='#e3f7f5', stroke=CYAN, stroke_width=2.5, radius=22)
add_text('TOTAL PROPOSED INVESTMENT', 108, 251, 24, title_font)
add_text('DKK600,000', 108, 300, 56, title_font)
add_text('12 months · excl. VAT · line items are proposed', 615, 275, 25, body_font)
add_text('Allocation shares · 100.00%', 615, 305, 20, title_font)
parts.append('<path d="M1330 237 Q1460 231 1670 239" fill="none" stroke="#f4d844" stroke-width="8" stroke-linecap="round"/>')

# Three allocation cards follow the Section 5 panel structure. Shares are labelled, not inferred by bar length.
cards = [
    (76, 'PEOPLE · 460 COMPANY HOURS', 'Assumed DKK600 per hour', [
        ('Research / service checks · 60h', 'DKK36,000', '6.00%'),
        ('Creative / translation · 120h', 'DKK72,000', '12.00%'),
        ('Campaign management · 160h', 'DKK96,000', '16.00%'),
        ('CRM / help-route handover · 120h', 'DKK72,000', '12.00%'),
    ]),
    (632, 'CHANNELS · PROPOSED ENVELOPES', 'Paid reach + gated screen spend', [
        ('Paid search', 'DKK108,000', '18.00%'),
        ('Paid social', 'DKK90,000', '15.00%'),
        ('Street screens · after Gate B', 'DKK38,200', '6.37%'),
        ('Screen setup · rate card', 'DKK4,995', '0.83%'),
    ]),
    (1188, 'TOOLS · CUSTOMER TRIAL · RESERVE', 'Ring-fenced operating assumptions', [
        ('Analytics / CRM tools · monthly', 'DKK30,000', '5.00%'),
        ('First-ride vouchers · cap 400 × DKK30', 'DKK12,000', '2.00%'),
        ('Contingency · separate, uncommitted', 'DKK40,805', '6.80%'),
    ]),
]
card_width = 536
accents = [CYAN, GOLD, CYAN]
for card_index, (x, heading, note, rows) in enumerate(cards):
    rect(x, 339, card_width, 413, fill='#fffefa', stroke='#244956', stroke_width=2, radius=8)
    parts.append(f'<path d="M{x+18} 359 Q{x+card_width/2} 354 {x+card_width-18} 360" fill="none" stroke="{accents[card_index]}" stroke-width="8" stroke-linecap="round"/>')
    add_text(heading, x + 23, 398, 22, title_font)
    add_text(note, x + 24, 429, 18, body_font)
    for row_index, (label, amount, share) in enumerate(rows):
        y = 477 + row_index * 59
        add_text(label, x + 24, y, 18, body_font)
        add_text(amount, x + 24, y + 27, 20, title_font)
        add_text(share, x + card_width - 106, y + 27, 18, body_font)
        if row_index < len(rows) - 1:
            rule(x + 22, y + 38, x + card_width - 22, y + 38, '#b7c9c6', 1.2, .65)

add_text('200,000 planned impressions ÷ 1,000 × DKK191 CPM = DKK38,200', 657, 710, 14, body_font)
add_text('Screens: published 2026 rate-card estimate · setup DKK4,995 · not a supplier quote', 657, 736, 12, body_font)
add_text('EXCLUDED OPERATING COSTS · CARS · DRIVERS · CHARGING · FRONTLINE SUPPORT', 100, 779, 16, title_font)

# Section 6 process-card language carries through the five cash stages and two approval gates.
rule(74, 804, 1726, 804, CYAN, 2, .55)
add_text('STAGED CASH RELEASE', 80, 842, 30, title_font)
add_text('Contingency stays outside the five stages', 485, 840, 20, body_font)
stage_cards = [
    ('M1–2', 'DKK101,000', 'Build'),
    ('M3–4', 'DKK76,000', 'Gate A test'),
    ('M5–6', 'DKK88,000', 'Review'),
    ('M7–9', 'DKK183,695', 'Gate B scale'),
    ('M10–12', 'DKK110,500', 'Refine'),
]
stage_xs = [76, 411, 746, 1081, 1416]
for index, ((period, amount, note), x) in enumerate(zip(stage_cards, stage_xs)):
    rect(x, 862, 300, 112, fill='#f2fbfa' if index % 2 == 0 else '#fffdf5', stroke='#59747a', stroke_width=2, radius=12)
    parts.append(f'<path d="M{x+17} 873 Q{x+148} 868 {x+281} 874" fill="none" stroke="{GOLD if index % 2 == 0 else CYAN}" stroke-width="6" stroke-linecap="round"/>')
    add_text(period, x + 18, 911, 22, title_font)
    add_text(amount, x + 18, 943, 21, title_font)
    add_text(note, x + 18, 966, 15, body_font)
    if index < 4:
        parts.append(f'<path d="M{x+305} 916 Q{x+321} 908 {x+335} 916" fill="none" stroke="{CYAN}" stroke-width="3" marker-end="url(#arrow)"/>')

parts.insert(4, '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#26c6cf" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker>')
add_text('Stage cash DKK559,195 + separate uncommitted DKK40,805 = DKK600,000', 82, 1006, 21, title_font)
add_text('Committed before Gate A · DKK177,000', 1090, 1006, 19, body_font)
# Two gate cards echo the five journey cards in Section 6.
rect(76, 1020, 815, 150, fill='#fffefa', stroke='#46636b', stroke_width=2, radius=8)
rect(920, 1020, 804, 150, fill='#fffefa', stroke='#46636b', stroke_width=2, radius=8)
add_text('Gate A · M4', 102, 1051, 26, title_font)
add_text('Completed/accepted ≥95% · service cancellations ≤2%', 104, 1084, 17, body_font)
add_text('Referenced complaints answered within 24h ≥90%', 104, 1111, 17, body_font)
add_text('Search ≥1.5% · social ≥0.8% · agree minimum volume with operations', 104, 1138, 16, body_font)
add_text('Fail: hold, fix, retest · pass releases M5–6', 104, 1160, 16, title_font)
add_text('Gate B · M6', 946, 1051, 26, title_font)
add_text('Mature 90-day repeat ≥20% · paid cost / first rider ≤DKK1,829', 948, 1084, 16, body_font)
add_text('Continue if both thresholds pass', 948, 1111, 17, body_font)
add_text('Repeat ≥35% releases screens · otherwise stop scale-up', 948, 1144, 17, title_font)

# Economics note stays visible but subordinate to the budget and release logic.
rect(76, 1195, 1648, 264, fill='#fff9dc', stroke='#d4bd3e', stroke_width=2, radius=18)
add_text('ILLUSTRATIVE ECONOMICS · ASSUMPTIONS, NOT OBSERVED COMPANY SPENDING', 106, 1235, 23, title_font)
add_text('378 first riders · about 676 rides · DKK227 fare proxy · assumed 30% contribution', 108, 1276, 22, body_font)
add_text('About DKK554,000 unrecovered · break-even requires 8,811 rides', 108, 1320, 28, title_font)
add_text('Year-one market entry is not self-funding in this illustrative case.', 108, 1361, 19, body_font)
add_text('Plan assumptions · impressions earn no ride/conversion credit · no lifetime value claimed', 108, 1400, 17, body_font)
parts.append('<path d="M1250 1435 Q1400 1421 1655 1437" fill="none" stroke="#f0d33d" stroke-width="7" stroke-linecap="round"/>')

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
    'screen_cost_treatment': 'Estimate based on E-029 published 2026 rate card; rate excludes VAT and production. DKK4,995 setup included separately. Not a supplier quote. Planned impressions are an assumption, not observed spend or rides.',
    'excluded_operating_costs': ['cars', 'drivers', 'charging', 'frontline support'],
    'shared_logo_sha256': hashlib.sha256(LOGO_PATH.read_bytes()).hexdigest(),
    'svg_sha256': hashlib.sha256(svg_path.read_bytes()).hexdigest(),
    'visible_citations': False,
    'text_as_glyph_paths': True,
    'visual_plan': 'Section 5 header, subtitle, shared lockup and three allocation cards; Section 6 five-stage process cards, paired gate cards and native line illustrations.',
}
(HERE / (PREFIX + '-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
engine.close()
print('Rendered complete Section 7 candidate:', (HERE / (PREFIX + '.png')).resolve())
