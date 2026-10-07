"""Focused Section 7 arithmetic, copy, SVG, bounds and writing-gate checks."""

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import base64
import hashlib
import itertools
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '07-candidate-v01-2026-10-04'
COPY_PATH = HERE / '07-copy-v01-2026-10-04.md'
MANIFEST_PATH = HERE / (PREFIX + '-manifest.json')
SVG_PATH = HERE / (PREFIX + '.svg')
PNG_PATH = HERE / (PREFIX + '.png')
ART_PATH = HERE / (PREFIX + '-generated-art.png')
manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
copy = COPY_PATH.read_text(encoding='utf-8')
svg = ET.parse(SVG_PATH).getroot()
checks = []


def check(name, result, detail):
    checks.append({'check': name, 'pass': bool(result), 'detail': detail})


def table_rows(markdown):
    marker = '<!-- budget-table -->'
    section = markdown.split(marker, 1)[1]
    rows = []
    for line in section.splitlines():
        if not line.startswith('|'):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if cells and not all(set(cell) <= set('-: ') for cell in cells):
            rows.append(cells)
    return rows


rows = table_rows(copy)
expected_headers = ['Item', 'Amount', 'Share (%)', 'Basis']
check('Exact section heading and budget', '## 7. Budget & Resources\n<!-- budget: 270 -->' in copy,
      'Required numbered display heading and 270-word panel budget')
check('Exact financial table schema', bool(rows) and rows[0] == expected_headers,
      rows[0] if rows else 'No financial allocation table found')
allocations = rows[1:-1] if len(rows) >= 3 else []
total_row = rows[-1] if rows else []
amounts = [Decimal(row[1]) for row in allocations]
shares = [Decimal(row[2]) for row in allocations]
total_amount = Decimal(total_row[1]) if len(total_row) > 1 else Decimal(0)
total_share = Decimal(total_row[2]) if len(total_row) > 2 else Decimal(0)
check('All eleven approved allocation rows present', len(allocations) == 11,
      f'{len(allocations)} rows; {[(r[0], r[1], r[2]) for r in allocations]}')
check('Allocation amounts sum exactly to DKK600,000', sum(amounts) == total_amount == Decimal(600000),
      f'{sum(amounts)} = table total {total_amount}')
check('Shares sum exactly to 100.00%', sum(shares) == total_share == Decimal('100.00'),
      f'{sum(shares)} = table total {total_share}')
rounding = Decimal('0.01')
share_matches = all(
    (amount / total_amount * Decimal(100)).quantize(rounding, rounding=ROUND_HALF_UP) == share
    for amount, share in zip(amounts, shares)
)
check('Each rounded share matches its allocation', share_matches,
      'Shares are independently recalculated from each DKK amount')
screen_amount = Decimal(200000) / Decimal(1000) * Decimal(191)
check('Sourced screen costs reconcile to planned volume', screen_amount == Decimal(38200) and
      screen_amount + Decimal(4995) == Decimal(43195),
      '200,000 planned impressions / 1,000 × published DKK191 CPM + DKK4,995 setup = DKK43,195')

people = [(Decimal(60), Decimal(36000)), (Decimal(120), Decimal(72000)),
          (Decimal(160), Decimal(96000)), (Decimal(120), Decimal(72000))]
check('People role hours and costs reconcile', sum(h for h, _ in people) == 460 and
      sum(c for _, c in people) == 276000 and all(h * 600 == c for h, c in people),
      '60 / 120 / 160 / 120 hours at assumed DKK600 per hour')
stage_amounts = [Decimal(101000), Decimal(76000), Decimal(88000), Decimal(183695), Decimal(110500)]
contingency = Decimal(40805)
check('Five stage releases plus separate contingency equal total',
      sum(stage_amounts) == Decimal(559195) and sum(stage_amounts) + contingency == total_amount,
      f'{stage_amounts}; stage sum {sum(stage_amounts)} + {contingency} = {total_amount}')
check('Pre-gate cumulative exposure reconciles',
      sum(stage_amounts[:2]) == 177000 and sum(stage_amounts[:3]) == 265000,
      f'Gate A {sum(stage_amounts[:2])}; Gate B {sum(stage_amounts[:3])}')
illustrative_contribution = Decimal('675.7') * Decimal(227) * Decimal('0.30')
unrecovered = Decimal(600000) - illustrative_contribution
break_even = (Decimal(600000) / (Decimal(227) * Decimal('0.30'))).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
check('Illustrative negative economics reproduce',
      unrecovered.quantize(Decimal('1E3'), rounding=ROUND_HALF_UP) == Decimal('5.54E5') and break_even == 8811,
      f'675.7 rides yield DKK{illustrative_contribution}; unrecovered DKK{unrecovered}; break-even {break_even} rides')

text_items = manifest['visible_text']
display_text = '\n'.join(item['text'] for item in text_items)
check('Required numbered title is first visible text', text_items[0]['text'] == '7. Budget & Resources', text_items[0]['text'])
check('All line amounts and shares appear on the visual', all(
    cell in display_text for row in allocations for cell in (f"DKK{int(Decimal(row[1])):,}", f"{Decimal(row[2]):.2f}%")),
      'All allocation amounts and percentages are present in controlled display strings')
check('Panel 5/6/8 interfaces and exclusions appear', all(token in display_text for token in [
    'DKK108,000', 'DKK90,000', '400 × DKK30 cap', 'frontline support',
    '≥95%', '≤2%', '≥1.5%', '≥0.8%', 'DKK1,829', '≥35%', 'M7–9']),
      'Search/social, voucher cap, service scope, both gate thresholds and post-Gate-B screen stage')
check('No source or decision IDs appear on the poster face',
      not re.search(r'\b(?:E|D)-\d{3}\b', display_text), 'IDs remain internal in copy comments and provenance')
check('Screen basis explicitly avoids supplier-quote implication',
      'not a supplier quote' in display_text.lower() and manifest['internal_evidence'] == ['E-029'],
      'Published rate-card basis; internal evidence ID E-029')
check('Screen formula explicitly divides impressions by 1,000',
      'planned 200,000 impressions ÷ 1,000 × DKK191 CPM = DKK38,200' in display_text,
      'Visible formula distinguishes planned impression volume from sourced CPM')

svg_ns = '{http://www.w3.org/2000/svg}'
image_elements = list(svg.iter(svg_ns + 'image'))
embedded = {item.attrib['id']: base64.b64decode(item.attrib['href'].split(',', 1)[1])
            for item in image_elements}
check('SVG is self-contained', all(item.attrib.get('href', '').startswith(('data:', '#'))
      for item in svg.iter() if 'href' in item.attrib), 'Generated illustration is embedded; no linked project assets')
check('Generated illustration bytes embedded unchanged', embedded.get('budget-art') == ART_PATH.read_bytes(),
      hashlib.sha256(ART_PATH.read_bytes()).hexdigest())
art = Image.open(ART_PATH).convert('RGBA')
check('Blank illustration has genuine transparency', art.getpixel((0, 0))[3] == 0 and
      art.getchannel('A').getextrema()[1] >= 250, f'{art.size}; alpha extrema {art.getchannel("A").getextrema()}')
check('SVG contains vector glyph paths, not font-dependent text nodes',
      len(list(svg.iter(svg_ns + 'text'))) == 0 and len(list(svg.iter(svg_ns + 'path'))) > 50,
      'All lettering is outlined with local CoreText glyph paths')
groups = {node.attrib.get('id'): node for node in svg.iter() if node.attrib.get('data-role')}
check('Visible SVG groups match the manifest', len(groups) == len(text_items) and all(
    groups[item['id']].attrib['aria-label'] == item['text'] for item in text_items),
      f'{len(groups)} controlled text groups')
line_boxes = [(item['text'], line['bbox']) for item in text_items for line in item['lines']]
check('All glyph bounds remain within the panel frame', all(
    60 <= box[0] and box[2] <= 1740 and 55 <= box[1] and box[3] <= 1590
    for _, box in line_boxes), 'Glyph bounds compared with conservative interior safe area')
collisions = []
for (left_text, left), (right_text, right) in itertools.combinations(line_boxes, 2):
    overlaps = min(left[2], right[2]) > max(left[0], right[0]) + .5 and min(left[3], right[3]) > max(left[1], right[1]) + .5
    if overlaps:
        collisions.append([left_text, right_text])
check('No glyph-block collisions', not collisions, collisions)

full = Image.open(PNG_PATH)
small = Image.open(HERE / (PREFIX + '-small.png'))
check('Full PNG dimensions', full.size == (1800, 1640), str(full.size))
check('Small proof dimensions', small.size == (900, 820), str(small.size))

with tempfile.TemporaryDirectory(prefix='mark1286-panel7-writing-') as temp:
    headings = Path(temp) / 'headings.txt'
    headings.write_text('7. Budget & Resources\n', encoding='utf-8')
    command = [
        'python3', '-B',
        '/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py',
        str(COPY_PATH), '--mode', 'poster', '--headings', str(headings),
        '--registry', str(ROOT / '04_references/references.json'),
        '--sources', str(ROOT / '04_references'),
        '--concepts', str(ROOT / '03_course_materials/concept-list.txt'),
        '--strict-scope', '--json',
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    gate = json.loads(result.stdout)
    (HERE / (PREFIX + '-writing-check.json')).write_text(json.dumps(
        {'exit_code': result.returncode, 'result': gate}, indent=2) + '\n', encoding='utf-8')

errors = gate['genre']['errors']
expected = ['Expected exactly one <!-- kpi-table --> marker; found 0']
genre_reviews = gate['genre_review']
check('Existing writing gate: no hard stops beyond expected standalone KPI omission',
      all(value == 0 for value in gate['effective_base_hard_by_category'].values()) and
      gate['genre']['total_words'] <= 270 and errors == expected and result.returncode == 2 and
      gate['hard_stops'] == 1 and all(item['type'] == 'label_colon' for item in genre_reviews),
      f"{gate['genre']['total_words']}/270 words; detector {gate['base']['anti_slop']['score']}; exit {result.returncode}; {errors}; label review {len(genre_reviews)}")

report = {
    'checks': checks,
    'passed': sum(item['pass'] for item in checks),
    'total': len(checks),
    'writing_gate_exit': result.returncode,
    'writing_gate_words': gate['genre']['total_words'],
    'writing_gate_expected_standalone_error': errors,
    'writing_gate_label_reviews': genre_reviews,
    'text_bounds': line_boxes,
    'text_collision_count': len(collisions),
    'full_png_sha256': hashlib.sha256(PNG_PATH.read_bytes()).hexdigest(),
    'limits': 'Full image was visually inspected; standalone gate omits the whole-poster KPI table. A0 assembly and print proof remain untested.',
}
(HERE / (PREFIX + '-checks.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f"Focused checks: {report['passed']}/{report['total']}")
print(f"Writing gate: {gate['genre']['total_words']}/270 words; detector {gate['base']['anti_slop']['score']}; exit {result.returncode}")
for item in checks:
    if not item['pass']:
        print('FAIL:', item)
