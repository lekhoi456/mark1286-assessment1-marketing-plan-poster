"""Fit the approved Success Dashboard into cell 08, preserving Sections 5–7."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '08-cell-fit-v02-2026-10-05'
BASE = HERE / '07-cell-fit-v04-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M1211 400 H1497 Q1518 400 1532 426 Q1549 452 1536 482 L1500 544 Q1491 559 1476 558 Q1397 532 1330 552 Q1293 562 1264 592 Q1256 598 1243 598 H1209 Q1185 598 1185 575 V423 Q1185 400 1211 400 Z'
parts, records = [], []
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '08-cell-fit-v01-2026-10-05-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def text(value, x, y, size=6.6, heading=False, width=None):
    font = 'MarkerFelt-Wide' if heading else 'ChalkboardSE-Regular'
    def glyph(size):
        proc.stdin.write(json.dumps({'text': value, 'font': font, 'size': size}, ensure_ascii=False) + '\n')
        proc.stdin.flush()
        result = json.loads(proc.stdout.readline())
        if 'error' in result:
            raise RuntimeError(result['error'])
        assert all(f in (font, 'Native vector arrow', 'Native vector maths') for f in result['resolved_font_names']), {'text':value, 'resolved':result['resolved_font_names']}
        return result
    data = glyph(size)
    if width and data['width'] > width:
        size *= width / data['width']
        data = glyph(size)
    a, b, c, d = data['bounds']
    records.append({'text': value, 'font': font, 'resolved_font_names': data['resolved_font_names'], 'size_px': size, 'size_pt_a0': round(size*1189/1672*72/25.4, 2), 'bbox': [x+a,y-d,x+c,y-b], 'advance_width': data['width']})
    parts.append(f'<g aria-label="{escape(value, quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{NAVY}"/></g>')
    return data['width']

def path(d, fill='none', colour=NAVY, width=.8):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')


def icon(kind, x, y, scale=1):
    parts.append(f'<g transform="translate({x} {y}) scale({scale})">')
    if kind=='consider':
        path('M-7-7H6V5H1L-3 8V5H-7Z',CREAM,width=.8)
        path('M-4-3L-2-1L1-4 M2-3H4 M-4 1L-2 3L1 0 M2 1H4',width=.8)
    elif kind=='riders':
        circle(0,-3,3,GOLD)
        path('M-6 7Q-6 1 0 1Q6 1 6 7Z',CYAN)
    elif kind=='rides':
        path('M-8 2L-5-4H4L7 2V7H-8Z',CYAN)
        path('M-4-3H3L5 1H-6Z',CREAM,width=.6)
        circle(-5,7,2,NAVY);circle(4,7,2,NAVY)
    elif kind=='repeat':
        path('M-6 3Q-10-6 0-7Q6-7 7-2 M7-2L7-7 M7-2L2-3',colour=CYAN,width=1.5)
        path('M6 4Q3 10-4 6 M-4 6L-1 6 M-4 6L-3 9',colour=NAVY,width=1.1)
    elif kind=='cost':
        circle(-9,0,7,GOLD)
        circle(-6,-2,7,GOLD)
        # Currency letters are native Chalkboard outlines, at the same 12.5 pt floor.
        proc.stdin.write(json.dumps({'text':'DKK','font':'ChalkboardSE-Regular','size':6.2/scale})+'\n')
        proc.stdin.flush()
        data=json.loads(proc.stdout.readline())
        assert data['resolved_font_names']==['ChalkboardSE-Regular'], data
        a,b,c,d=data['bounds']
        records.append({'text':'DKK','font':'ChalkboardSE-Regular','resolved_font_names':data['resolved_font_names'],'size_px':6.2,'size_pt_a0':round(6.2*1189/1672*72/25.4,2),'bbox':[x+scale*(4+a),y+scale*(4-d),x+scale*(4+c),y+scale*(4-b)],'advance_width':data['width']*scale})
        parts.append(f'<g aria-label="DKK"><path d="{data["path"]}" transform="translate(4 4) scale(1 -1)" fill="{NAVY}"/></g>')
    elif kind=='check':
        circle(0,0,3.2,CYAN,.6);path('M-2 0L-.5 1.5L2-1.5',width=.7)
    elif kind=='cancel':
        circle(0,0,3.2,GOLD,.6);path('M-1.4-1.4L1.4 1.4 M1.4-1.4L-1.4 1.4',width=.7)
    elif kind=='help':
        path('M-3 1V-1Q-3-5 0-5Q3-5 3-1V1 M-3 0V3 M3 0V3L0 4',width=.8)
    elif kind=='data':
        path('M-5-3Q0-6 5-3V5Q0 8-5 5Z',CYAN)
        path('M-5-3Q0 0 5-3 M-5 1Q0 4 5 1',width=.6)
    elif kind=='leaf':
        path('M-5 5Q-8-5 5-5Q8 5-5 5Z',CYAN);path('M-6 7L3-3',width=.7)
    parts.append('</g>')

title_width=text('8. Success Dashboard',1202,420,10.5,True,width=191)
path(f'M1202 424Q{1202+title_width/2} 425 {1202+title_width} 424',colour=GOLD,width=1.5)
text('12-month targets',1430,420,7.6,width=83)
text('COMMIT',1202,434,7.7,True)
text('Consideration survey:',1260,434,6.7,width=77)
text('M1–2 → M12',1340,434,6.7,width=54)
text('M12: Renew · Revise · Stop',1400,434,6.7,width=113)
metrics=[('consider','+10 pp',['Consideration']),('riders','1,200',['Distinct first paid','riders*']),('rides','2,500',['Paid rides*']),('repeat','≥50%',['90-day repeat†']),('cost','≤DKK165',['Cost / first','paid rider*'])]
for i,(kind,number,labels) in enumerate(metrics):
    x=1202+i*62.6
    path(f'M{x} 439Q{x+27} 438 {x+59} 439V486Q{x+28} 487 {x} 486Z',CREAM if i%2==0 else GOLD,width=.8)
    icon(kind,x+29.5,445,.59)
    text(number,x+4,463,12.9,True,width=51)
    baselines=[479] if len(labels)==1 else ([474,484] if len(labels)==2 else [472,479,486])
    for label,y in zip(labels,baselines): text(label,x+3,y,6.2,width=55)
text('*Paid campaign cohort only',1202,494,6.2,width=140)
text('†Full 90-day cohorts',1377,494,6.2,width=121)
# One service strip applies to both budget-release reviews.
text('SERVICE',1202,503,7.3,True,width=36)
icon('check',1247,500)
text('≥95% completed',1253,503,6.6,width=73)
icon('cancel',1335,500)
text('≤2% service cancellations',1342,503,6.6,width=103)
icon('help',1440,500)
text('≥90% help within 24h',1448,503,6.6,width=65)
path('M1202 507Q1343 508 1511 507',colour=CYAN,width=.7)
text('M4 review',1202,518,7.5,True,width=86)
text('≥200 first paid riders',1202,528,6.2,width=104)
text('Both counts cumulative',1202,537,6.2,width=101)
path('M1283 515H1304 M1300 512L1304 515L1300 518',colour=CYAN,width=1)
text('M6 review',1316,518,7.5,True,width=94)
text('≥450 first paid riders',1316,526,6.2,width=97)
text('≤DKK175 paid acquisition',1316,534,6.2,width=97)
text('≥35% 90-day repeat†',1316,541,6.2,width=96)
icon('leaf',1433,514,.7)
text('BRAND UPSIDE',1443,516,7.2,True,width=76)
text('Organic · referrals ·',1428,526,6.2,width=87)
text('extra rides',1428,534,6.2,width=75)
text('Track separately',1428,542,6.2,width=75)
# The inputs, proposed dashboard and weekly action follow one vertical route.
text('TRACKING PROPOSED',1202,549,7.1,True,width=107)
text('M1–2 data checks',1202,557,6.2,width=99)
text('Ads + trips + dispatch/help',1202,565,6.2,width=94)
path('M1195 565V572 M1192.5 569.5L1195 572L1197.5 569.5',colour=CYAN,width=.8)
icon('data',1205,572,.55)
text('Big Data dashboard',1214,574,6.2,width=73)
path('M1195 575V580 M1192.5 577.5L1195 580L1197.5 577.5',colour=CYAN,width=.8)
icon('check',1205,580,.8)
text('Weekly actions',1214,582,6.2,width=70)
text('Monthly cohort review',1199,589,6.2,width=73)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode: raise RuntimeError(proc.stderr.read())
layer='<g id="section-08-v02-candidate" clip-path="url(#cell-08-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
assert base.count('id="section-08-v01-candidate"')==1
start=base.index('<g id="section-08-v01-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
assert assembled.count('id="section-08-v02-candidate"')==1 and 'id="section-08-v01-candidate"' not in assembled
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1027" viewBox="1179 394 368 210"><defs><clipPath id="cell-08-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>'
(HERE/f'{PREFIX}-panel.svg').write_text(standalone)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1027" viewBox="1179 514.817073 368 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('panel',1800),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
copy=(HERE/f'{PREFIX}-copy.md').read_text()
copy_lines=[line.removeprefix('## ') for line in copy.splitlines() if line and not line.startswith('<!--')]
assert copy_lines==[r['text'] for r in records], {'draft':copy_lines,'surface':[r['text'] for r in records]}
# Sample the exact quadratic path and test glyph corners against its polygon.
vertices=[(1211,400)]
def line(x,y): vertices.append((x,y))
def quad(cx,cy,x,y):
    ax,ay=vertices[-1]
    for i in range(1,101):
        t=i/100
        vertices.append(((1-t)**2*ax+2*(1-t)*t*cx+t*t*x,(1-t)**2*ay+2*(1-t)*t*cy+t*t*y))
line(1497,400);quad(1518,400,1532,426);quad(1549,452,1536,482);line(1500,544);quad(1491,559,1476,558);quad(1397,532,1330,552);quad(1293,562,1264,592);quad(1256,598,1243,598);line(1209,598);quad(1185,598,1185,575);line(1185,423);quad(1185,400,1211,400)
def inside(x,y):
    hit=False
    for (ax,ay),(bx,by) in zip(vertices,vertices[1:]+vertices[:1]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: hit=not hit
    return hit
outside=[]; overlaps=[]
for i,r in enumerate(records):
    a=r['bbox']
    if not all(inside(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]): outside.append(r)
    for s in records[i+1:]:
        b=s['bbox']
        if min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]):overlaps.append([r['text'],s['text']])
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks={'status':'Section 8 v02 improvement candidate; fitted image pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'cell_path':CELL,'a0_mm':[1189,841],'visible_text':records,'word_bearing_tokens':sum(bool(re.search(r'\w',w)) for w in displayed.split()),'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'raster_images_added':0,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'copy_matches_visible_surface':True,'heading_size_pt_a0':records[0]['size_pt_a0'],'m4_m6_cumulative_first_paid_riders':True,'paid_acquisition_basis':'Paid search/social spend per distinct paid-attributed first paid rider; not full marketing-budget CAC','manual_visual_review':'Producing agent inspected standalone, fitted close-up and full A0 PNGs: no observed text/icon overlap or arch clipping. Physical A0 proof untested.'}
with tempfile.TemporaryDirectory(prefix='mark1286-section8-') as temporary:
    headings=Path(temporary)/'headings.txt'
    headings.write_text('8. Success Dashboard\n')
    gate=subprocess.run(['python3','-B','/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py',str(HERE/f'{PREFIX}-copy.md'),'--mode','poster','--headings',str(headings),'--registry',str(HERE.parent/'04_references/references.json'),'--sources',str(HERE.parent/'04_references'),'--concepts',str(HERE.parent/'03_course_materials/concept-list.txt'),'--strict-scope','--json'],capture_output=True,text=True)
    report=json.loads(gate.stdout)
    (HERE/f'{PREFIX}-copycheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    checks['fragment_presentcheck']={'exit':gate.returncode,'genre_words':report['genre']['total_words'],'detector_status':report['base']['anti_slop']['status'],'detector_score':report['base']['anti_slop']['score'],'effective_base_hard_by_category':report['effective_base_hard_by_category'],'out_of_scope_whole_poster_tables':report['genre']['errors']}
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert checks['minimum_size_pt_a0']>=12.5
assert gate.returncode==2 and report['hard_stops']==2 and all(v==0 for v in report['effective_base_hard_by_category'].values()), report
assert 198000/1200==165 and 265000+335000==600000
checks['cross_panel_section7']={'budget_dkk':600000,'paid_search_social_dkk':198000,'year_end_cost_at_1200_paid_first_riders_dkk':165,'m4_cumulative_commitment_dkk':177000,'m6_cumulative_commitment_dkk':265000,'m6_held_dkk':335000,'cost_denominator_is_riders_not_total_budget':True}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
