"""Compose a proposed Section 9 with exact handwriting and preserved blank art.

Run: uv run --no-project --with fonttools python -B <this file>
No image-model lettering, live-feature claim or font redistribution.
"""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
STEM = '09-candidate-v01-2026-10-04'
ART_SOURCE = Path('/Users/KHOILQ/.codex/generated_images/01a10027-ee09-7f53-8a59-14552f63a1f2/exec-ab9fab4d-30af-486f-96da-db3618a85cd1.png')
helper = importlib.util.spec_from_file_location('section9_lettering', HERE / (STEM + '-lettering.py'))
module = importlib.util.module_from_spec(helper)
helper.loader.exec_module(module)
INK, CYAN, GOLD, PAPER = '#173a47', '#26c6cf', '#ffd400', '#fffdf5'
W, H = 1800, 1700
lettering = module.Lettering(INK)
shapes = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']


def path(d, colour=INK, width=2.8, fill='none', opacity=1):
    shapes.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')


def marker(x, y, width, height, colour=GOLD):
    for i in range(4):
        yy = y + height * (i + .5) / 4
        path(f'M{x+i%2*2} {yy} Q{x+width*.52} {yy-2+i%3} {x+width-i%2*2} {yy+1}', colour, height/4*1.22, opacity=.23)


def arrow(x1, y1, x2, y2):
    path(f'M{x1} {y1} Q{(x1+x2)/2} {(y1+y2)/2-3} {x2} {y2}', '#668e94', 2.4)
    if abs(x2-x1) > abs(y2-y1):
        path(f'M{x2-12} {y2-7} L{x2} {y2} L{x2-12} {y2+8}', '#668e94', 2.4)
    else:
        path(f'M{x2-7} {y2-11} L{x2} {y2} L{x2+7} {y2-11}', '#668e94', 2.4)


path('M33 38 Q865 30 1767 42 L1762 1657 Q910 1666 37 1659 Q28 857 33 38Z', width=2.6)
path('M47 50 Q827 46 1750 53', CYAN, 1.8, opacity=.45)
marker(73, 130, 700, 20)
lettering.text('9. Ride Innovation', 70, 108, 76, 'heading', role='heading')
lettering.text('Proposed repeat reminder', 70, 197, 48, 'heading', role='proposal qualifier')
lettering.text('Illustrative message:', 70, 248, 32, role='specimen qualifier')
art_bytes = ART_SOURCE.read_bytes()
shutil.copyfile(ART_SOURCE, HERE / (STEM + '-art.png'))
shapes.append(f'<image id="s9-blank-art" x="70" y="255" width="720" height="596" href="data:image/png;base64,{base64.b64encode(art_bytes).decode()}"/>')
lettering.text('“Your usual Thursday ride. Pre-book it now.”', 283, 442, 32, 'strong', maximum=187, role='illustrative reminder')
lettering.text('Personalisation:', 890, 253, 43, 'heading')
for i, label in enumerate(('consent', 'rider’s own trip history', 'relevant reminder', 'intended repeat ride')):
    lettering.text(label, 890, 330+i*91, 40, 'strong', role='proposed reminder mechanism')
    if i < 3:
        arrow(869, 350+i*91, 869, 384+i*91)
lettering.text('Uses the rider’s own trip history. No purchased profiles.', 890, 689, 34, maximum=800, role='data limit')
marker(69, 873, 1190, 15, CYAN)
lettering.text('Existing advertised feature: pre-booking up to 30 days.', 70, 864, 40, role='E-016 advertised feature')
path('M70 911 Q868 906 1728 912', CYAN, 2, opacity=.45)
lettering.text('Proposed joined journey', 70, 973, 47, 'heading', role='proposal qualifier')
marker(630, 1005, 525, 17)
lettering.text('One trip reference:', 900, 1014, 41, 'strong', centre=True)
centres = [190, 545, 900, 1255, 1610]
labels = ['local info page', 'app', 'in-car help card', 'follow-up', 'help.']
for i, (cx, label) in enumerate(zip(centres, labels)):
    if i < 4:
        arrow(cx+86, 1080, centres[i+1]-86, 1080)
    if i == 0:
        path(f'M{cx-37} 1046 L{cx+38} 1048 L{cx+36} 1110 L{cx-38} 1108Z', fill=PAPER)
        path(f'M{cx-36} 1060 Q{cx} 1059 {cx+36} 1062', CYAN, 4)
        path(f'M{cx-23} 1080 L{cx+19} 1080 M{cx-23} 1095 L{cx+8} 1095', width=2)
    elif i == 1:
        path(f'M{cx-25} 1042 Q{cx} 1039 {cx+26} 1043 L{cx+24} 1116 Q{cx} 1120 {cx-26} 1114Z', fill=PAPER)
        path(f'M{cx-11} 1051 L{cx+11} 1051 M{cx-5} 1107 L{cx+5} 1107', CYAN, 3)
    elif i == 2:
        path(f'M{cx-43} 1054 L{cx+42} 1051 L{cx+44} 1104 L{cx-42} 1107Z', fill=PAPER)
        marker(cx-30, 1066, 50, 9, CYAN)
        path(f'M{cx-29} 1090 L{cx+22} 1089', width=2)
    elif i == 3:
        path(f'M{cx-40} 1054 L{cx+41} 1056 L{cx+39} 1105 L{cx-41} 1102Z', fill=PAPER)
        path(f'M{cx-39} 1056 L{cx} 1082 L{cx+40} 1057', CYAN, 3)
    else:
        path(f'M{cx-35} 1097 L{cx-34} 1076 Q{cx-32} 1041 {cx} 1041 Q{cx+34} 1041 {cx+35} 1077 L{cx+33} 1097', CYAN, 5)
        path(f'M{cx-36} 1076 L{cx-23} 1075 L{cx-23} 1101 L{cx-36} 1101Z M{cx+24} 1075 L{cx+36} 1076 L{cx+36} 1100 L{cx+24} 1101Z', fill=PAPER)
        path(f'M{cx+33} 1100 Q{cx+31} 1111 {cx+5} 1111', width=2.5)
    lettering.text(label, cx, 1160, 34, maximum=285, centre=True, role='proposed journey touchpoint')
lettering.text('Intended benefit: less repetition when resolving a trip problem.', 70, 1240, 36, role='intended benefit')
marker(67, 1286, 1620, 23)
lettering.text('Both proposals need local implementation. Supports O3: repeat rides.', 70, 1295, 38, 'strong', role='implementation qualifier and objective')
path('M70 1341 Q870 1337 1728 1342', CYAN, 2, opacity=.45)
lettering.text('Proposed usage model and limits', 70, 1407, 45, 'heading', role='proposed model')
lettering.text('Pay per trip: usage-based charging.', 70, 1461, 36)
for x, label, detail in (
    (70, 'Subscription:', 'defer until frequent repeat is demonstrated.'),
    (647, 'AI chatbot:', 'defer until a reliable human FAQ exists.'),
    (1220, 'Neuromarketing:', 'not selected. Ordinary surveys test clarity.'),
):
    lettering.text(label, x, 1524, 39, 'heading', role='innovation boundary')
    lettering.text(detail, x, 1573, 34, maximum=500, role='reason and condition')

prefix = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>9. Ride Innovation — proposed repeat reminder and joined journey</title>'
for suffix, face in (('.svg', lettering.portable), ('-editable.svg', lettering.native)):
    (HERE / (STEM+suffix)).write_text(prefix+''.join(shapes)+''.join(face)+'</svg>')
manifest = {
    'section': 9, 'heading': '9. Ride Innovation', 'status': 'Candidate awaiting parent review; no new group approval claimed',
    'canvas': {'width': W, 'height': H, 'physical_a0_verified': False},
    'text_objects': lettering.objects, 'copy_file': '09-copy-v01-2026-10-04.md',
    'typography': {'explicit_font_files': module.FILES, 'portable_outlines': True, 'native_editable_companion': True, 'font_files_redistributed': False},
    'art': {'file': STEM+'-art.png', 'sha256': hashlib.sha256(art_bytes).hexdigest(), 'native_bytes_retained': True, 'x':70, 'y':255, 'width':720, 'height':596, 'tool':'built-in image_gen__imagegen'},
    'source_mapping': {'E-016': {'key':'green-sm-denmark-aps-ndb', 'file':'../04_references/green-sm-denmark-aps-ndb-green-sm-car.pdf', 'page':3, 'sha256':'eb6fd110419430e9ce53ae84c5131fc747163eab4a2678df4902784c9cd06b5b', 'claim':'Existing advertised pre-booking up to 30 days; not a tested fulfilment guarantee'}},
    'concepts': ['personalisation','omnichannel','artificial-intelligence','usage-based-model','subscription-model','subscription-challenges','neuromarketing'],
    'proposal_limits': ['Consent and rider’s own trip history only; no purchased profiles','Reminder and joined journey need local implementation','Pay-per-trip model proposed; subscription and chatbot deferred','Neuromarketing not selected; ordinary clarity surveys'],
    'alignment': {'O3':'Repeat rides; effect remains intended, not observed','S5':'Consented follow-up','S6':'After-sales and local help','S8':'90-day repeat cohort and clarity measures','S10':'Repeat-led growth with service integrity'},
}
(HERE / (STEM+'-manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for suffix, width, height in (('.png',W,H),('-small-preview.png',900,850)):
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-h',str(height),str(HERE/(STEM+'.svg')),'-o',str(HERE/(STEM+suffix))],check=True)
print(f'Complete Section 9 PNG ready; {len(lettering.objects)} controlled text objects.')
