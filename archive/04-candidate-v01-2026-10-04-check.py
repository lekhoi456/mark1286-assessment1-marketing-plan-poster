"""Focused checks for the new standalone Section 4 candidate."""

from pathlib import Path
import base64
import hashlib
import itertools
import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '04-candidate-v01-2026-10-04'
manifest = json.loads((HERE / (PREFIX + '-manifest.json')).read_text())
svg = ET.parse(HERE / (PREFIX + '.svg')).getroot()
checks = []


def check(name, result, detail):
    checks.append({'check': name, 'pass': bool(result), 'detail': detail})


check('Complete exact approved copy', [t['text'] for t in manifest['texts'] if t['role'] == 'master'] == manifest['approved_copy'], '10 approved strings, including numbered heading and exact punctuation')
elements = {e.attrib['id']: e for e in svg.iter() if e.attrib.get('data-role')}
check('Visible path groups match the manifest', all(elements[t['id']].attrib['aria-label'] == t['text'] for t in manifest['texts']), '13 controlled groups: 10 approved objects and 3 exact promise repetitions')
check('Every specimen repeats the selected promise', [t['text'] for t in manifest['texts'] if t['role'] == 'specimen-repeat'] == ['Clear terms. Local care.'] * 3, 'Taxi, generic app and local ad')
ns = '{http://www.w3.org/2000/svg}'
images = list(svg.iter(ns + 'image'))
embedded = {e.attrib['id']: base64.b64decode(e.attrib['href'].split(',', 1)[1]) for e in images}
logo_bytes = (HERE / 'shared-logo.png').read_bytes()
check('Exact shared logo embedded', embedded['shared-logo'] == logo_bytes, hashlib.sha256(logo_bytes).hexdigest())
check('Four lockup instances use one shared definition', sum(e.attrib.get('href') == '#shared-logo' for e in svg.iter()) == 4, 'One global identity lockup plus three specimens; aspect ratio preserved')
check('SVG self-contained', all(e.attrib.get('href', '').startswith(('data:', '#')) for e in svg.iter() if 'href' in e.attrib), 'All raster assets embedded; lettering uses paths')
check('No font text nodes', len(list(svg.iter(ns + 'text'))) == 0, 'Exact lettering is stored as local glyph paths')
check('Generated alpha retained', embedded['illustration-sheet'] == (HERE / (PREFIX + '-generated-art.png')).read_bytes(), 'Original generated PNG bytes retained without alpha stripping')
art = Image.open(HERE / (PREFIX + '-generated-art.png'))
check('Actual transparent generated sheet', art.mode == 'RGBA' and art.getchannel('A').getextrema() == (0, 255), f'{art.size}; RGBA alpha 0–255')
png = Image.open(HERE / (PREFIX + '.png'))
proof = Image.open(HERE / (PREFIX + '-small.png'))
check('Full dimensions', png.size == (1800, 1400), str(png.size))
check('900px proof dimensions', proof.size == (900, 700), str(proof.size))
line_boxes = [(t['id'], line['text'], line['bbox']) for t in manifest['texts'] for line in t['lines']]
check('Text inside frame safety area', all(65 <= b[0] < b[2] <= 1735 and 55 <= b[1] < b[3] <= 1340 for _, _, b in line_boxes), 'Actual glyph bounds compared with a conservative interior rectangle')
collisions = []
for (a, ta, ba), (b, tb, bb) in itertools.combinations(line_boxes, 2):
    if min(ba[2], bb[2]) > max(ba[0], bb[0]) and min(ba[3], bb[3]) > max(ba[1], bb[1]):
        collisions.append([ta, tb])
check('No text-to-text collision', not collisions, collisions)
logo_collisions = []
for _, value, b in line_boxes:
    for item in manifest['logos']:
        lb = item['bbox']
        if min(b[2], lb[2]) > max(b[0], lb[0]) and min(b[3], lb[3]) > max(b[1], lb[1]):
            logo_collisions.append([value, item['name']])
check('Text and lockup boxes separated', not logo_collisions, logo_collisions)
visible = '\n'.join(t['text'] for t in manifest['texts'])
check('Removed content absent', all(s not in visible for s in ['57%', '22%', '18%', '11%', 'APP-CHOICE', 'CAMPAIGN RESPONSE', 'Plain and respectful', '→', 'E-010', 'E-185']), 'No old cues, funnel arrow, extra voice claim, E-IDs or visible source labels')
with tempfile.TemporaryDirectory(prefix='mark1286-panel4-candidate-') as tmp:
    headings = Path(tmp) / 'headings.txt'
    headings.write_text('Branding and Identity\n')
    command = ['python3', '-B', '/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py', str(HERE / (PREFIX + '-copy.md')), '--mode', 'poster', '--headings', str(headings), '--registry', str(ROOT / '04_references/references.json'), '--sources', str(ROOT / '04_references'), '--concepts', str(ROOT / '03_course_materials/concept-list.txt'), '--strict-scope', '--json']
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    gate = json.loads(result.stdout)
    (HERE / (PREFIX + '-writing-check.json')).write_text(json.dumps({'exit_code': result.returncode, 'result': gate}, indent=2) + '\n')
check('Writing gate effective base categories', all(n == 0 for n in gate['effective_base_hard_by_category'].values()), gate['effective_base_hard_by_category'])
check('Standalone word budget', gate['genre']['total_words'] <= 75, f"{gate['genre']['total_words']}/75 words, headings and specimen repeats included")
check('Only expected standalone table omissions', gate['genre']['errors'] == ['Expected exactly one <!-- budget-table --> marker; found 0', 'Expected exactly one <!-- kpi-table --> marker; found 0'], f'Exit {result.returncode}; no whole-poster pass claimed')
report = {'checks': checks, 'passed': sum(c['pass'] for c in checks), 'total': len(checks),
          'text_bounds': line_boxes, 'logos': manifest['logos'],
          'full_png_sha256': hashlib.sha256((HERE / (PREFIX + '.png')).read_bytes()).hexdigest(),
          'limits': 'Mechanical bounds supplement full and 900px visual inspection; no A0 print acceptance'}
(HERE / (PREFIX + '-checks.json')).write_text(json.dumps(report, indent=2) + '\n')
print(f"Focused checks: {report['passed']}/{report['total']}")
print(f"Writing gate: {gate['genre']['total_words']}/75 words; detector {gate['base']['anti_slop']['score']}; exit {result.returncode}")
for item in checks:
    if not item['pass']:
        print('FAIL:', item)
