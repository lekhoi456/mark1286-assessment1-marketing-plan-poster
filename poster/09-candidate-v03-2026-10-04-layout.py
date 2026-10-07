"""Render Section 9 v03 with illustrated mechanisms and controlled lettering.

Use Python with fonttools available; keep runtime dependencies outside iCloud.
The two companions separate drawing primitives from rendering/export metadata.
"""
from html import unescape
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
STEM = '09-candidate-v03-2026-10-04'
W, H = 1800, 1700


def local_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


draw = local_module('section9_drawing', STEM+'-drawing.py')
letters = local_module('section9_lettering', '09-candidate-v01-2026-10-04-lettering.py').Lettering(draw.INK)
INK, CYAN, GOLD, PAPER = draw.INK, draw.CYAN, draw.GOLD, draw.PAPER
path, frame, marker, arrow = draw.path, draw.frame, draw.marker, draw.arrow


def text(value, x, y, size=32, kind='body', maximum=None, role='label', centre=False):
    return letters.text(value, x, y, size, kind, maximum, role, centre)


def asset(name, cx, cy, scale=1):
    draw.shapes.append(f'<g transform="translate({cx} {cy}) scale({scale})">')
    getattr(draw, 'icon_'+name)(0, 0)
    draw.shapes.append('</g>')


def card(x, y, heading):
    frame(x, y, 775, 480, '#fffef9', '#82a8a9', 2.5)
    marker(x+26, y+68, 380, 13)
    text(heading, x+27, y+60, 43, 'heading', role='stage heading')


draw.shapes.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
frame(32, 35, W-64, H-70, 'none', INK, 2.7)
marker(69, 128, 680, 16)
text('9. Ride Innovation', 70, 108, 76, 'heading', role='exact required heading')
frame(70, 164, 1660, 132, draw.PALE_CYAN, '#75acaf', 2.3)
text('ADVERTISED: COPENHAGEN', 94, 212, 31, 'heading', maximum=470, role='baseline heading')
asset('phone', 609, 226, .74)
text('App booking', 650, 240, 32, maximum=235, role='advertised feature')
asset('calendar', 915, 226, .8)
text('Pre-book: max 30 days', 964, 240, 30, maximum=328, role='advertised pre-booking maximum')
asset('clock', 1349, 225, .72)
text('Performance untested', 1395, 236, 28, maximum=303, role='performance limit')
text('PROPOSED PILOTS', 72, 352, 42, 'heading', role='proposal status')
LEFT, RIGHT, TOP, BOTTOM = 75, 950, 390, 930

# Trip records pass a consent gate before AI personalisation reaches a rider.
card(LEFT, TOP, '01 Target S1')
asset('trip_stack', LEFT+145, TOP+182, 2.05)
asset('brain', LEFT+391, TOP+182, 2.05)
asset('phone', LEFT+640, TOP+182, 1.94)
asset('person', LEFT+707, TOP+226, .76)
arrow(LEFT+220, TOP+182, LEFT+295, TOP+182)
asset('shield', LEFT+257, TOP+155, .62)
arrow(LEFT+473, TOP+182, LEFT+576, TOP+182)
text('Consented first-party data', LEFT+145, TOP+296, 31, maximum=236, centre=True, role='first-party data proposal')
text('Big Data + AI', LEFT+391, TOP+296, 33, maximum=245, centre=True, role='marketing mechanism')
text('Reminders', LEFT+640, TOP+296, 33, maximum=200, centre=True, role='personalisation output')
frame(LEFT+24, TOP+361, 727, 91, draw.PALE_CYAN, draw.RULE, 1.9)
asset('shield', LEFT+66, TOP+404, .72)
text('Purpose/quality/access', LEFT+114, TOP+397, 32, maximum=588, role='data-use gate')
text('No bought/sensitive profiles', LEFT+114, TOP+434, 28, maximum=588, role='excluded data sources')

# No time saving is drawn; icons identify what the future pilot must measure.
card(RIGHT, TOP, '02 Dispatch AI')
asset('phone', RIGHT+126, TOP+174, 1.76)
asset('brain', RIGHT+385, TOP+174, 1.95)
asset('car', RIGHT+640, TOP+182, 1.72)
asset('person', RIGHT+703, TOP+153, .66)
arrow(RIGHT+175, TOP+174, RIGHT+293, TOP+174)
arrow(RIGHT+463, TOP+174, RIGHT+565, TOP+174)
for value, xx in [('Booking',126), ('AI match',385)]:
    text(value, RIGHT+xx, TOP+282, 32, centre=True, role='dispatch mechanism')
text('Local baseline comparison', RIGHT+27, TOP+340, 29, role='pilot comparator')
text('Gain unproven', RIGHT+553, TOP+340, 28, 'strong', maximum=200, role='evidence limit')
for name, label, xx in [('clock','Match time',115), ('license','Fulfilment',300), ('stop','Cancellations',488), ('scale','Fairness',672)]:
    asset('shield' if name=='license' else name, RIGHT+xx, TOP+388, .73)
    text(label, RIGHT+xx, TOP+447, 27, maximum=178, centre=True, role='pilot measure')

# All care touchpoints share a reference; a FAQ trial has a visible human exit.
card(RIGHT, BOTTOM, '03 Connect care')
frame(RIGHT+249, BOTTOM+89, 278, 50, draw.PALE_CYAN, CYAN, 2)
text('ONE TRIP ID', RIGHT+388, BOTTOM+125, 30, 'strong', centre=True, role='shared reference')
path(f'M{RIGHT+250} {BOTTOM+113} Q{RIGHT+148} {BOTTOM+112} {RIGHT+110} {BOTTOM+155}', CYAN, 2.8)
path(f'M{RIGHT+388} {BOTTOM+140} L{RIGHT+388} {BOTTOM+163}', CYAN, 2.8)
path(f'M{RIGHT+527} {BOTTOM+113} Q{RIGHT+616} {BOTTOM+108} {RIGHT+650} {BOTTOM+155}', CYAN, 2.8)
asset('phone', RIGHT+110, BOTTOM+208, 1.7)
asset('car', RIGHT+385, BOTTOM+208, 1.63)
asset('person', RIGHT+650, BOTTOM+210, 1.5)
path(f'M{RIGHT+626} {BOTTOM+181} Q{RIGHT+650} {BOTTOM+155} {RIGHT+675} {BOTTOM+181} L{RIGHT+675} {BOTTOM+202}', CYAN, 4)
text('Support', RIGHT+650, BOTTOM+292, 32, centre=True, role='care touchpoint')
asset('star', RIGHT+631, BOTTOM+337, .82)
text('Ratings', RIGHT+658, BOTTOM+350, 28, maximum=97, role='feedback invitation')
frame(RIGHT+27, BOTTOM+373, 722, 77, draw.PALE_CYAN, draw.RULE, 1.9)
asset('message', RIGHT+73, BOTTOM+409, .78)
text('Test FAQ bot', RIGHT+114, BOTTOM+422, 29, role='chatbot trial')
arrow(RIGHT+310, BOTTOM+407, RIGHT+386, BOTTOM+407)
asset('person', RIGHT+440, BOTTOM+412, .83)
text('Human hand-off', RIGHT+487, BOTTOM+422, 29, maximum=246, role='human escalation')

# Parallel cohorts are compared only after frequency/contribution measurement.
card(LEFT, BOTTOM, '04 Test retention')
text('First: frequency + contribution', LEFT+28, BOTTOM+116, 31, maximum=714, role='measurement before subscription test')
frame(LEFT+43, BOTTOM+153, 271, 171, draw.PALE_CYAN, CYAN, 2.4)
frame(LEFT+418, BOTTOM+153, 310, 171, draw.PALE_GOLD, GOLD, 2.4)
asset('car', LEFT+178, BOTTOM+214, .96)
asset('calendar', LEFT+569, BOTTOM+213, 1.13)
asset('trip_stack', LEFT+657, BOTTOM+215, .77)
text('Pay-per-trip', LEFT+178, BOTTOM+286, 32, centre=True, role='control cohort')
asset('scale', LEFT+366, BOTTOM+236, .76)
text('Prepaid/monthly', LEFT+574, BOTTOM+279, 32, centre=True, role='proposed subscription cohort')
text('Needs-matched', LEFT+574, BOTTOM+311, 25, centre=True, role='offer fit condition')
path(f'M{LEFT+178} {BOTTOM+325} L{LEFT+178} {BOTTOM+349} L{LEFT+383} {BOTTOM+349} M{LEFT+574} {BOTTOM+325} L{LEFT+574} {BOTTOM+349} L{LEFT+383} {BOTTOM+349}', CYAN, 2.8)
arrow(LEFT+383, BOTTOM+349, LEFT+383, BOTTOM+376)
asset('gauge', LEFT+383, BOTTOM+409, .84)
text('Retention + margin', LEFT+29, BOTTOM+425, 32, maximum=287, role='retention measures')
asset('stop', LEFT+493, BOTTOM+408, .78)
text('Stop if either falls', LEFT+535, BOTTOM+414, 29, maximum=200, role='stop rule')

arrow(859, TOP+243, 941, TOP+243, CYAN, 4.3)
arrow(RIGHT+388, TOP+490, RIGHT+388, BOTTOM-10, CYAN, 4.3)
arrow(RIGHT-8, BOTTOM+243, 861, BOTTOM+243, CYAN, 4.3)
path(f'M{LEFT-2} {BOTTOM+243} L51 {BOTTOM+243} L51 {TOP+243} L{LEFT-3} {TOP+243}', GOLD, 3.7)
path(f'M{LEFT-16} {TOP+235} L{LEFT-3} {TOP+243} L{LEFT-16} {TOP+251}', GOLD, 3.7)
text('MEASURE / REFINE', 108, 909, 28, 'strong', role='learning feedback')

frame(70, 1468, 1660, 179, draw.PALE_GOLD, '#d4bb55', 2.4)
asset('shield', 116, 1550, .88)
text('BEFORE PILOTS', 177, 1510, 31, 'heading', role='shared gate heading')
text('Privacy/tech/operations + group approval', 177, 1555, 30, maximum=819, role='readiness and approval conditions')
text('Unpriced dispatch/chatbot/subscription: cost separately', 177, 1600, 30, maximum=819, role='uncosted changes')
path('M1080 1496 L1080 1625', '#d4bb55', 2.4)
text('DKK600,000', 1121, 1532, 39, 'heading', role='approved marketing envelope')
text('excludes app/platform build +', 1121, 1575, 29, maximum=554, role='budget exclusions')
text('vehicle/driver/frontline operations', 1121, 1616, 29, maximum=554, role='budget exclusions')

# Export the actual display strings as the copy master for this candidate.
copy_path = HERE / '09-copy-v03-2026-10-04.md'
copy_text = '# Section 9 — infographic candidate display copy\n\n'
for obj in letters.objects:
    prefix = '## ' if obj['role']=='exact required heading' else ('### ' if obj['role']=='stage heading' else '')
    copy_text += prefix + obj['text'] + '\n\n'
    if obj['role']=='exact required heading':
        copy_text += '<!-- budget: 100 -->\n\n'
copy_path.write_text(copy_text, encoding='utf-8')
svg_prefix = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>9. Ride Innovation</title><desc>Illustrated proposed pilots, not current capabilities or measured performance. Marketing data, dispatch, care and retention connect in a learning cycle. Readiness, approval and separate costing remain required.</desc>'
for suffix, face in [('.svg', letters.portable), ('-editable.svg', letters.native)]:
    svg = svg_prefix + ''.join(draw.shapes) + ''.join(face) + '</svg>'
    assert [unescape(t) for t in re.findall(r'data-text="([^"]*)"', svg)] == [o['text'] for o in letters.objects]
    (HERE / (STEM+suffix)).write_text(svg, encoding='utf-8')
previous = json.loads((HERE / '09-candidate-v02-2026-10-04-manifest.json').read_text())
source_map = previous['source_mapping']
for entry in source_map.values():
    actual = hashlib.sha256((HERE / entry['file']).read_bytes()).hexdigest()
    assert actual == entry['sha256'], 'Source PDF changed since v02 provenance.'
words = sum(bool(re.search(r'\w', token)) for o in letters.objects for token in o['text'].split())
manifest = {**previous, 'version': 3, 'status': 'Text and artwork accepted by the student for assembly; no group approval claimed', 'user_visual_acceptance': True, 'student_acceptance_date': '2026-10-04', 'student_acceptance_message': 'được', 'copy_file': copy_path.name, 'text_objects': letters.objects, 'surface_words': words, 'word_count_convention': 'All visible strings including numbered headings; punctuation-only tokens excluded', 'source_mapping': source_map, 'art': {'type': 'Original hand-drawn vector diagrams', 'generated_art': False, 'shared_logo_modified': False}, 'baseline_display': 'Advertised booking and pre-booking only. Licence-register evidence retained internally.'}
(HERE / (STEM+'-manifest.json')).write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
for suffix, width, height in [('.png',W,H), ('-small-preview.png',900,850)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-h',str(height),str(HERE/(STEM+'.svg')),'-o',str(HERE/(STEM+suffix))],check=True)
print(json.dumps({'rendered': STEM, 'surface_words': words, 'text_objects': len(letters.objects)}))
