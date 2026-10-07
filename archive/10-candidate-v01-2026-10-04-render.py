"""Compose a candidate business-goal alignment panel with exact handwritten copy."""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import re
import subprocess
from PIL import Image

HERE = Path(__file__).resolve().parent
PREFIX = '10-candidate-v01-2026-10-04'
COPY = HERE / '10-copy-v01-2026-10-04.md'
ART = HERE / f'{PREFIX}-generated-art.png'
GLYPHS = HERE / f'{PREFIX}-glyphs.swift'
SPEC = importlib.util.spec_from_file_location('section10_layout', HERE / f'{PREFIX}-layout.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
W, H = 1900, 1640
LAYOUT = MODULE.Layout(W, H, GLYPHS)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
clean = re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)
strings = [s.strip().replace('**', '').removeprefix('## ') for s in clean.split('\n\n') if s.strip()]
assert len(strings) == 18
assert strings[0] == '10. Business Goals & Growth'
LAYOUT.frame('outer-pen-frame', 30, 30, W-60, H-60, stroke=MODULE.INK, thick=2.8)
LAYOUT.text(strings[0], 78, 122, size=92, font='MarkerFelt-Thin', role='heading')
LAYOUT.rule(82, 157, 1380, colour='#f6d452', thick=9)
LAYOUT.text(strings[1], 82, 211, size=40, font='Noteworthy-Light', role='proposal-qualifier')

uri = 'data:image/png;base64,' + base64.b64encode(ART.read_bytes()).decode('ascii')
im = Image.open(ART)
placements = []
def sprite(key, source, target):
    sx, sy, sw, sh = source
    x, y, w, h = target
    cid = key+'-source-clip'
    LAYOUT.parts.extend([
        f'<svg id="{key}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{sx} {sy} {sw} {sh}" preserveAspectRatio="xMidYMid meet" overflow="hidden">',
        f'<defs><clipPath id="{cid}" clipPathUnits="userSpaceOnUse"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}"/></clipPath></defs>',
        f'<g clip-path="url(#{cid})"><image href="{uri}" x="0" y="0" width="{im.width}" height="{im.height}"/></g></svg>'
    ])
    placements.append({'id':key,'source':source,'target':target,'role':'conceptual decorative scene'})

# The spine is an organising pen stroke, not a measured growth curve.
LAYOUT.parts.append('<path id="alignment-spine" d="M211 263Q199 471 211 679Q221 883 209 1208" fill="none" stroke="#a3dcde" stroke-width="9" stroke-linecap="round"/>')
rows = [
    {'top':285, 'index':2, 'crop':[0,0,768,512], 'id':'stable-service'},
    {'top':525, 'index':5, 'crop':[768,0,768,512], 'id':'local-awareness'},
    {'top':765, 'index':8, 'crop':[0,512,768,512], 'id':'electric-mission'},
    {'top':1005,'index':11,'crop':[768,512,768,512], 'id':'repeat-growth'},
]
for row in rows:
    y, i = row['top'], row['index']
    sprite(row['id'],row['crop'],[57,y-22,310,207])
    LAYOUT.text(strings[i],390,y+8,size=52,font='MarkerFelt-Thin',role='business-goal',owner=row['id'])
    LAYOUT.rule(391,y+34,1325,colour='#d2eceb',thick=4)
    LAYOUT.parts.append(f'<path d="M391 {y+84}Q594 {y+78} 819 {y+84}" fill="none" stroke="#f9e28d" stroke-width="57" stroke-linecap="round" opacity=".62"/>')
    if row['id'] == 'stable-service':
        LAYOUT.parts.append(f'<path d="M391 {y+134}Q519 {y+129} 650 {y+134}" fill="none" stroke="#f9e28d" stroke-width="51" stroke-linecap="round" opacity=".62"/>')
    LAYOUT.text(strings[i+1],391,y+91,size=39,font='Noteworthy-Light',width=370 if row['id']=='stable-service' else 430,role='marketing-objective',owner=row['id'])
    LAYOUT.parts.append(f'<path d="M850 {y+88}Q870 {y+82} 889 {y+88}M878 {y+79}L889 {y+88}L878 {y+97}" fill="none" stroke="#71979e" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
    LAYOUT.text(strings[i+2],918,y+72,size=39,font='Noteworthy-Light',width=867,role='marketing-action',owner=row['id'])
    if row['id'] != 'repeat-growth':LAYOUT.rule(390,y+190,1403,colour='#9bbab9',thick=1.6)

LAYOUT.frame('m12-decision-frame',77,1270,1746,291,fill='#fff8d8',stroke='#a0b6b1',thick=2.6)
LAYOUT.text(strings[14],102,1336,size=52,font='MarkerFelt-Thin',role='decision-heading',owner='m12')
LAYOUT.text(strings[15],103,1402,size=40,font='Noteworthy-Light',role='decision-evidence',owner='m12')
LAYOUT.parts.append('<path d="M105 1430Q740 1434 1390 1430M1381 1421L1392 1430L1381 1439" fill="none" stroke="#4b858f" stroke-width="2.7" stroke-linecap="round"/>')
LAYOUT.text(strings[16],107,1486,size=54,font='MarkerFelt-Thin',role='decision-options',owner='m12')
LAYOUT.text(strings[17],956,1484,size=39,font='Noteworthy-Light',width=790,role='economic-limit',owner='m12')
svg = LAYOUT.close()
(HERE/f'{PREFIX}.svg').write_text(svg)
manifest = {
 'section':10,'status':'delegated candidate; parent selection pending; no group approval',
 'copy_source':COPY.name,'copy_sha256':sha(COPY),'canvas_px':[W,H],
 'text_objects':LAYOUT.texts,'frames':LAYOUT.frames,'raster_placements':placements,
 'art_asset':ART.name,'art_sha256':sha(ART),'art_dimensions':list(im.size),'art_mode':im.mode,
 'art_alpha_extrema':list(im.getchannel('A').getextrema()),
 'render_source':Path(__file__).name,'layout_source':f'{PREFIX}-layout.py','glyph_source':GLYPHS.name,
 'native_image_calls':1,'native_output_original':'/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-8fe94f34-9d43-4360-a4c5-b9e11ad9023f.png',
 'citation_visible':False,'logo_used':False,'source_basis':'Approved integrated-plan-copenhagen.md section12; section10 gates/objectives; Section8 current v01',
 'evidence_ids':['E-020','E-021','E-185'],
 'objective_mapping':{'stable-service':['O4 service integrity','stage gates'],'local-awareness':['O1 awareness','O2 paid trial'],'electric-mission':['O2 paid trial','O3 repeat'],'repeat-growth':['O3 repeat']},
 'internal_source_records':[{'key': 'green-sm-denmark-aps-ndc', 'pdf': '../04_references/green-sm-denmark-aps-ndc-story-and-humanity.pdf', 'physical_pages': [1], 'evidence_ids': ['E-185'], 'sha256': 'd836ff7cf0fbd96b5935514d79d7978e93b6db8b0c56fce0d7e694ab2c346187', 'inherited_verification_date': '2026-10-03', 'new_live_verification': False}, {'key': 'konkurrence-og-forbrugerstyrelsen-2026b', 'pdf': '../04_references/konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf', 'physical_pages': [175, 179], 'evidence_ids': ['E-020', 'E-021'], 'sha256': '309669803ffbe59f7d14609b297dc0945df9dc3f457664645e240645dece3ffb', 'inherited_verification_date': '2026-10-03', 'new_live_verification': False}],
 'registered_concepts':['alignment-with-objectives','long-term-sustainable-growth','retention-over-acquisition'],
 'source_claim_boundaries':['Electric rides support mission; no lifecycle savings claim','Business-objective context does not prove Copenhagen results','Year-one model does not break even','Stage gates and repeat evidence constrain scale; not automatic expansion'],
 'whole_poster_or_print_verified':False,
}
(HERE/f'{PREFIX}-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for name,width in [(f'{PREFIX}.png',None),(f'{PREFIX}-small.png',950)]:
    cmd=['/opt/homebrew/bin/rsvg-convert']
    if width:cmd+=['-w',str(width)]
    cmd+=['-o',str(HERE/name),str(HERE/f'{PREFIX}.svg')]
    subprocess.run(cmd,check=True)
print(HERE/f'{PREFIX}.png')
