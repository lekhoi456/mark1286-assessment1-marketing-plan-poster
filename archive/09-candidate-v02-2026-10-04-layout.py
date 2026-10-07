"""Render Section 9 v02 with controlled handwriting and hand-drawn vector marks.

Run with the existing section-9 typography helper and rsvg-convert. No model
lettering or generated artwork; source claims and limits live in the companion
provenance note.
"""
from html import unescape
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
STEM = '09-candidate-v02-2026-10-04'
COPY_FILE = '09-copy-v02-2026-10-04.md'
helper = importlib.util.spec_from_file_location(
    'section9_lettering_v02', HERE / '09-candidate-v01-2026-10-04-lettering.py'
)
module = importlib.util.module_from_spec(helper)
helper.loader.exec_module(module)

INK, CYAN, GOLD, PAPER = '#173a47', '#26c6cf', '#ffd400', '#fffdf5'
PALE_CYAN, PALE_GOLD, RULE = '#f4ffff', '#fff9df', '#8cabad'
W, H = 1800, 1700
lettering = module.Lettering(INK)
shapes = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']


def path(d, colour=INK, width=2.8, fill='none', opacity=1):
    shapes.append(
        f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'
    )


def frame(x, y, width, height, fill='none', colour=RULE, thick=2.4):
    d = (
        f'M{x+7} {y+2} Q{x+width*.47} {y-3} {x+width-5} {y+3} '
        f'Q{x+width+2} {y+height*.46} {x+width-3} {y+height-5} '
        f'Q{x+width*.52} {y+height+3} {x+4} {y+height-2} '
        f'Q{x-3} {y+height*.52} {x+7} {y+2}Z'
    )
    path(d, colour, thick, fill)


def marker(x, y, width, height=17, colour=GOLD, opacity=.25):
    for i in range(4):
        yy = y + height * (i + .5) / 4
        path(
            f'M{x+i%2*2} {yy} Q{x+width*.5} {yy-2+i%3} {x+width-i%2*2} {yy+1}',
            colour, height/4*1.18, opacity=opacity,
        )


def arrow(x1, y1, x2, y2, colour=RULE, width=3):
    midx, midy = (x1+x2)/2, (y1+y2)/2
    path(f'M{x1} {y1} Q{midx} {midy-3} {x2} {y2}', colour, width)
    if abs(x2-x1) >= abs(y2-y1):
        sign = 1 if x2 > x1 else -1
        path(f'M{x2-sign*12} {y2-7} L{x2} {y2} L{x2-sign*12} {y2+8}', colour, width)
    else:
        sign = 1 if y2 > y1 else -1
        path(f'M{x2-7} {y2-sign*12} L{x2} {y2} L{x2+8} {y2-sign*12}', colour, width)


def text(value, x, y, size, kind='body', maximum=None, role='display', centre=False):
    return lettering.text(value, x, y, size, kind, maximum, role, centre)


def icon_booking(cx, cy):
    # An app tile and a pencilled route pin.
    path(f'M{cx-53} {cy-40} Q{cx-24} {cy-44} {cx+5} {cy-40} L{cx+3} {cy+43} Q{cx-26} {cy+46} {cx-52} {cy+41}Z', fill=PALE_CYAN)
    path(f'M{cx-39} {cy-25} Q{cx-25} {cy-27} {cx-10} {cy-24} M{cx-39} {cy-9} L{cx-9} {cy-10}', CYAN, 3.2)
    path(f'M{cx+26} {cy-31} Q{cx+48} {cy-34} {cx+49} {cy-11} Q{cx+47} {cy+3} {cx+28} {cy+20} Q{cx+9} {cy+2} {cx+8} {cy-12} Q{cx+9} {cy-31} {cx+26} {cy-31}Z', GOLD, 3.4, PALE_GOLD)
    path(f'M{cx+20} {cy-13} Q{cx+27} {cy-20} {cx+34} {cy-13}', INK, 2.6)


def icon_data(cx, cy):
    # Three first-party signal nodes feeding a small insight chart.
    for dx, dy in [(-42, -27), (-39, 24), (1, 2)]:
        path(f'M{cx+dx+11} {cy+dy} Q{cx+26} {cy+dy+6} {cx+43} {cy+5}', RULE, 2.5)
        path(f'M{cx+dx} {cy+dy-9} Q{cx+dx+11} {cy+dy-11} {cx+dx+20} {cy+dy-8} L{cx+dx+18} {cy+dy+9} Q{cx+dx+8} {cy+dy+12} {cx+dx-1} {cy+dy+8}Z', CYAN, 2.6, PALE_CYAN)
    path(f'M{cx+34} {cy+31} L{cx+34} {cy-7} M{cx+51} {cy+31} L{cx+51} {cy-28} M{cx+68} {cy+31} L{cx+68} {cy-47} M{cx+26} {cy+32} Q{cx+50} {cy+36} {cx+77} {cy+32}', GOLD, 5)


def icon_journey(cx, cy):
    # App, car, and person-to-support arc.
    path(f'M{cx-67} {cy-27} Q{cx-44} {cy-31} {cx-22} {cy-27} L{cx-23} {cy+25} Q{cx-45} {cy+28} {cx-67} {cy+24}Z', fill=PALE_CYAN)
    path(f'M{cx-58} {cy-14} L{cx-34} {cy-14} M{cx-58} {cy-2} L{cx-39} {cy-2}', CYAN, 3)
    path(f'M{cx-7} {cy+16} Q{cx+4} {cy-6} {cx+23} {cy-6} L{cx+42} {cy-6} Q{cx+56} {cy+4} {cx+61} {cy+16} L{cx+57} {cy+28} L{cx-10} {cy+28}Z', GOLD, 3, PALE_GOLD)
    path(f'M{cx+8} {cy-5} L{cx+20} {cy-22} L{cx+39} {cy-21} L{cx+48} {cy-5}', INK, 2.8)
    for wx in (cx+4, cx+45):
        path(f'M{wx-7} {cy+28} Q{wx} {cy+19} {wx+7} {cy+28} Q{wx+6} {cy+38} {wx-1} {cy+37} Q{wx-9} {cy+36} {wx-7} {cy+28}Z', INK, 2.3, PAPER)
    path(f'M{cx+67} {cy+26} Q{cx+83} {cy+20} {cx+82} {cy+3} Q{cx+80} {cy-21} {cx+99} {cy-25}', CYAN, 4)
    path(f'M{cx+92} {cy-37} Q{cx+100} {cy-41} {cx+108} {cy-37} L{cx+106} {cy-12} Q{cx+99} {cy-9} {cx+92} {cy-13}Z', INK, 2.5, PALE_CYAN)


def icon_package(cx, cy):
    # A monthly calendar above a prepaid trip bundle.
    path(f'M{cx-51} {cy-34} Q{cx-22} {cy-38} {cx+8} {cy-34} L{cx+7} {cy+22} Q{cx-21} {cy+26} {cx-52} {cy+22}Z', fill=PALE_CYAN)
    path(f'M{cx-51} {cy-17} Q{cx-23} {cy-20} {cx+8} {cy-17}', CYAN, 4)
    for bx in (cx-34, cx-18, cx-2):
        path(f'M{bx} {cy-5} l7 0 m-7 13 l7 0', INK, 2)
    path(f'M{cx+27} {cy-29} Q{cx+50} {cy-32} {cx+58} {cy-14} L{cx+48} {cy+28} Q{cx+25} {cy+30} {cx+16} {cy+13}Z', GOLD, 3, PALE_GOLD)
    path(f'M{cx+29} {cy-10} Q{cx+39} {cy-14} {cx+48} {cy-9} M{cx+27} {cy+4} Q{cx+37} {cy+1} {cx+46} {cy+6}', INK, 2.5)


def node(x, y, width, title, detail, number):
    frame(x, y, width, 190, PALE_CYAN if number % 2 else '#fffef9', RULE, 2.1)
    marker(x+16, y+42, width-35, 12, GOLD if number % 2 else CYAN, .2)
    text(title, x+25, y+38, 32, 'heading', maximum=width-48, role='feedback-loop node')
    text(detail, x+25, y+91, 27, 'body', maximum=width-48, role='feedback-loop detail')


# Outer frame and shared Section 5–10 hand-drawn palette/type treatment.
frame(32, 35, W-64, H-70, 'none', INK, 2.7)
path(f'M50 51 Q{W/2} 47 {W-50} 53', CYAN, 2, opacity=.55)
marker(69, 129, 750, 18)
text('9. Ride Innovation', 70, 108, 76, 'heading', role='exact required heading')

# Verified local baseline, visually separated from proposed work.
frame(70, 205, 1660, 150, PALE_CYAN, '#75acaf', 2.3)
text('VERIFIED IN COPENHAGEN', 100, 252, 38, 'heading', role='evidence status')
text(
    'App booking and pre-booking up to 30 days advertised.',
    100, 300, 28, 'body', maximum=1580, role='verified advertised feature',
)
text('Licensed dispatch-office register: Green SM Denmark ApS. Performance untested.', 100, 337, 28, 'body', maximum=1580, role='verified register status and performance limit')

# The proposed marketing roadmap.
marker(69, 421, 695, 16)
text('PROPOSED ROADMAP', 70, 418, 43, 'heading', role='roadmap heading')

cards = [(70, 465, 400), (505, 465, 400), (940, 465, 400), (1375, 465, 355)]
card_data = [
    (
        '01 Target S1',
        'Repeat self-paying taxi riders, 25–44, service area. Big Data + marketing AI use consented first-party trip data for targeting and personalised reminders. Check purpose/quality/access. No bought/sensitive profiles.',
        icon_booking,
    ),
    (
        '02 Dispatch AI',
        'Future Big Data + AI driver-task pilot, separately costed. Gate data/privacy, tech/ops checks, approval. Test booking-to-driver-match time, fulfilment, cancellations, fairness vs local baseline. Gain unproven.',
        icon_data,
    ),
    (
        '03 Connect care',
        'One trip reference across app, driver, car, support. Invite ratings. Human-review issues. Test chatbot FAQs with human hand-off.',
        icon_journey,
    ),
    (
        '04 Test retention',
        'Measure frequency and contribution first. Cohort-test needs-matched prepaid/monthly bundles vs pay-per-trip. Track retention, margin. Stop if either falls.',
        icon_package,
    ),
]
for index, ((x, y, width), (heading, detail, draw_icon)) in enumerate(zip(cards, card_data), start=1):
    frame(x, y, width, 530, '#fffef9' if index % 2 else '#fffdf4', '#82a8a9', 2.4)
    draw_icon(x+width/2, y+86)
    marker(x+18, y+173, width-34, 15, CYAN if index == 2 else GOLD, .21)
    text(heading, x+20, y+170, 34, 'heading', maximum=width-40, role=f'roadmap stage {index}')
    text(detail, x+22, y+231, 29, 'body', maximum=width-46, role=f'roadmap stage {index} mechanism and gate')
    if index < 4:
        arrow(x+width+2, y+291, x+width+29, y+291, CYAN, 3)

# Data and service loop, with the last node returning to learning.
text('FEEDBACK LOOP', 70, 1045, 41, 'heading', role='loop heading')
loop_nodes = [
    (70, 1083, 365, 'CONSENT', 'Trip data'),
    (505, 1083, 365, 'CHECK', 'Purpose, quality, access'),
    (940, 1083, 365, 'TARGET', 'S1 + care'),
    (1375, 1083, 355, 'MEASURE', 'Match, rating, repeat'),
]
for i, (x, y, width, title, detail) in enumerate(loop_nodes, start=1):
    node(x, y, width, title, detail, i)
    if i < 4:
        arrow(x+width+8, y+95, loop_nodes[i][0]-12, y+95, CYAN, 3)
path('M1640 1286 Q1610 1382 900 1382 Q263 1382 188 1284', GOLD, 3.5)
path('M199 1294 L188 1284 L202 1278', GOLD, 3.5)
text('REFINE', 726, 1342, 27, 'strong', role='feedback action')

# Keep the changed strategy and uncosted implementation plainly qualified.
text('FUNDING BOUNDARY', 70, 1424, 38, 'heading', role='guardrail heading')
frame(70, 1444, 1660, 167, PALE_GOLD, '#d4bb55', 2.4)
text(
    'Strategic subscription change. Group approval and separate costing needed.',
    96, 1498, 28, 'body', maximum=1585, role='subscription approval and measurement gate',
)
text(
    'DKK600,000 excludes app/platform build and vehicle/driver/frontline operations. AI dispatch/chatbot unpriced.',
    96, 1548, 27, 'body', maximum=1585, role='budget and feasibility boundary',
)

prefix = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}"><title>9. Ride Innovation — consented marketing, conditional dispatch pilot, connected care and gated retention</title>'
    '<desc>Verified Danish app-booking, pre-booking and dispatch-office evidence is separated from proposals. Marketing AI and operations AI are distinct. Dispatch, chatbot and subscription remain gated; no outcome is claimed.</desc>'
)
svg_paths = {}
for suffix, face in (('.svg', lettering.portable), ('-editable.svg', lettering.native)):
    svg = prefix + ''.join(shapes) + ''.join(face) + '</svg>'
    svg_paths[suffix] = svg
    (HERE / (STEM+suffix)).write_text(svg, encoding='utf-8')

copy_path = HERE / COPY_FILE
copy_text = copy_path.read_text(encoding='utf-8')
source_files = {
    'E-016': HERE.parent / '04_references/green-sm-denmark-aps-ndb-green-sm-car.pdf',
    'E-027': HERE.parent / '04_references/faerdselsstyrelsen-nd-find-koerselskontor.pdf',
    'E-188': HERE.parent / '04_references/green-sm-denmark-aps-ndb-green-sm-car.pdf',
    'E-205': HERE.parent / '04_references/feng-et-al-2020-scalable-deep-reinforcement-learning-for-ride-hailing.pdf',
}
source_hashes = {key: hashlib.sha256(file.read_bytes()).hexdigest() for key, file in source_files.items()}
source_map = {
    'E-016': {'file': '../04_references/green-sm-denmark-aps-ndb-green-sm-car.pdf', 'page': 3, 'claim': 'Up-to-30-day pre-booking is advertised; not a fulfilment claim.'},
    'E-027': {'file': '../04_references/faerdselsstyrelsen-nd-find-koerselskontor.pdf', 'page': 2, 'claim': 'Green SM Denmark ApS is listed as a nationally licensed dispatch office; licence does not prove service performance.'},
    'E-188': {'file': '../04_references/green-sm-denmark-aps-ndb-green-sm-car.pdf', 'pages': '1–2', 'claim': 'The company advertises app booking and gives app booking instructions; no booking was tested.'},
    'E-205': {'file': '../04_references/feng-et-al-2020-scalable-deep-reinforcement-learning-for-ride-hailing.pdf', 'page': 1, 'claim': 'Research proposes sequential driver-task assignment and demonstrates a numerical experiment on Didi data; no local speed or Copenhagen result.'},
}
expected_surface = [item['text'] for item in lettering.objects]
svg_surface = re.findall(r'data-text="([^"]*)"', svg_paths['.svg'])
svg_surface = [unescape(value) for value in svg_surface]
assert expected_surface == svg_surface, 'Portable SVG text differs from the layout manifest.'
def copy_tokens(value):
    return re.findall(r'\w+', unescape(value).casefold())


copy_word_tokens = copy_tokens(copy_text)
for surface in expected_surface:
    phrase = copy_tokens(surface)
    found = any(copy_word_tokens[i:i+len(phrase)] == phrase for i in range(len(copy_word_tokens)-len(phrase)+1))
    assert found, f'Visible string is absent from the copy master: {surface}'

manifest = {
    'section': 9,
    'version': 2,
    'heading': '9. Ride Innovation',
    'status': 'Candidate for parent review; no group approval or budget revision claimed',
    'canvas': {'width': W, 'height': H, 'physical_a0_verified': False},
    'copy_file': COPY_FILE,
    'text_objects': lettering.objects,
    'typography': {'helper': '09-candidate-v01-2026-10-04-lettering.py', 'portable_outlines': True, 'native_editable_companion': True, 'font_files_redistributed': False},
    'art': {'type': 'hand-drawn SVG vector marks', 'generated_art': False, 'shared_logo_modified': False},
    'source_mapping': {key: {**value, 'sha256': source_hashes[key]} for key, value in source_map.items()},
    'registered_concepts': ['consumer-insights-and-big-data', 'artificial-intelligence', 'personalisation', 'omnichannel', 'ai-chatbots', 'subscription-model', 'subscription-challenges', 'ride-hailing-dispatch-rl'],
    'proposal_limits': [
        'Marketing AI and personalisation are proposals using consented first-party trip data only.',
        'AI-assisted driver-task allocation is a separate conditional operations pilot, not established Copenhagen practice or an evidenced performance result. Compare booking-to-match time, fulfilment, cancellations and fairness against a local baseline.',
        'The registered outside concept ride-hailing-dispatch-rl uses Feng et al. (2020) p.1 for sequential driver-task allocation. Its numerical experiment uses Didi data only and establishes no Copenhagen outcome or faster local matching.',
        'No observed local reminder, joined system, rating process, chatbot, retention effect or AI dispatch outcome is claimed.',
        'Subscription test is a strategic-change recommendation, requires separate cost and group approval, and is not added to DKK600,000.',
        'Dispatch AI and chatbot integration are unpriced; app/platform development and vehicle, driver and frontline operations remain outside the approved marketing budget.',
    ],
    'alignment': {'O3': 'Repeat use remains an intended outcome, to be measured against mature cohorts.', 'S5': 'Consented follow-up and campaign targeting.', 'S6': 'Local after-sales help, ratings and human escalation.', 'S8': 'Repeat, completion, rating and contribution measures.', 'S10': 'Scale only when service and contribution evidence support it.'},
}
(HERE / (STEM+'-manifest.json')).write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

normal_copy = re.sub(r'^# Section 9 — candidate display copy\s*|^## 9\. Ride Innovation\s*', '', copy_text, flags=re.M)
normal_copy = re.sub(r'<!--.*?-->', ' ', normal_copy, flags=re.S)
normal_copy = re.sub(r'[*_`#]', '', normal_copy)
normal_copy = re.sub(r'\s+', ' ', normal_copy).strip()
visible_order = ' '.join(expected_surface)
checker_body = copy_text.split('## 9. Ride Innovation', 1)[1]
checker_lines = []
for line in re.sub(r'<!--.*?-->', '', checker_body, flags=re.S).splitlines():
    line = re.sub(r'^\s*(?:#{1,6}\s+|>\s*|[-+*]\s+|\d+[.)]\s+)', '', line)
    checker_lines.append(line.replace('|', ' '))
checker_text = re.sub(r'[*_`~]', '', 'Ride Innovation\n' + '\n'.join(checker_lines))
checker_word_count = sum(bool(re.search(r'\w', token)) for token in checker_text.split())
checks = {
    'date': '2026-10-04',
    'text_objects': len(lettering.objects),
    'portable_svg_text_matches_manifest': True,
    'each_visible_string_present_in_copy_master': True,
    'copy_and_visible_order_checked_manually': True,
    'full_dimensions': [W, H],
    'small_dimensions': [900, 850],
    'source_hashes_computed': source_hashes,
    'no_visible_citations_or_evidence_ids': True,
    'no_model_generated_lettering_or_art': True,
    'heading_exact': '9. Ride Innovation',
    'verified_basis_separated_from_proposals': True,
    'advertised_features_not_fulfilment_claims': True,
    'marketing_ai_and_personalisation_proposal_only': True,
    'dispatch_outside_concept_registered': True,
    'dispatch_evidence_limit_recorded': 'Didi data only; no Copenhagen outcome or faster matching result',
    'chatbot_human_faq_and_escalation_gate_visible': True,
    'subscription_strategic_change_and_separate_approval_visible': True,
    'budget_boundary_visible': True,
    'physical_a0_verified': False,
    'group_approval_claimed': False,
    'visual_overlap_and_clip_check': 'pass; full-size raster inspected after taller cards were rendered',
    'copy_budget_words': 155,
    'word_count_convention': 'Section 9 body excluding copy-file title and exact numbered heading',
    'word_count': checker_word_count,
}
(HERE / (STEM+'-checks.json')).write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

for suffix, width, height in (('.png', W, H), ('-small-preview.png', 900, 850)):
    subprocess.run([
        '/opt/homebrew/bin/rsvg-convert', '-w', str(width), '-h', str(height),
        str(HERE / (STEM+'.svg')), '-o', str(HERE / (STEM+suffix)),
    ], check=True)
print(f'Rendered {STEM}: {len(lettering.objects)} controlled text objects; {checks["word_count"]} markdown surface words.')
