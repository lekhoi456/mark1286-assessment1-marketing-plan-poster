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
PREFIX = '08-cell-fit-v01-2026-10-05'
BASE = HERE / '07-cell-fit-v03-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
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
        path('M-8 0Q0-8 8 0Q0 8-8 0Z',CREAM,width=.9)
        circle(0,0,2.5,CYAN)
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
        circle(0,0,7,GOLD)
        path('M2-4H-2Q-5-4-3-1L3 1Q5 4 1 4H-3 M0-6V6',width=1)
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

tw=text('8. Success Dashboard',1202,420,12.2,True,width=191)
path(f'M1202 424Q{1202+tw/2} 426 {1202+tw} 424',colour=GOLD,width=1.6)
text('12-month targets',1430,420,7.6,width=83)
text('COMMIT',1202,434,7.7,True)
text('Consideration survey:',1260,434,6.7,width=77)
text('M1–2 → M12',1340,434,6.7,width=54)
text('M12: Renew · Revise · Stop',1400,434,6.7,width=113)
metrics=[('consider','+10 pp','Consideration'),('riders','1,200','First paid riders*'),('rides','2,500','Paid rides*'),('repeat','≥50%','90-day repeat†'),('cost','≤DKK165','Paid acquisition*')]
for i,(kind,number,label) in enumerate(metrics):
    x=1202+i*62.6
    path(f'M{x} 440Q{x+27} 439 {x+59} 440V476Q{x+28} 477 {x} 476Z', '#d9f4f2' if i%2==0 else '#fff1a7',width=.6)
    icon(kind,x+29.5,449,.7)
    w=text(number,x+4,466,13.7,True,width=51)
    # Labels retain the cohort marks adjacent to the number-led graphic.
    text(label,x+3,474,6.6,width=53)
text('*Paid campaign cohort',1202,485,6.6,width=105)
text('†Full 90-day cohorts',1377,485,6.6,width=121)
text('SERVICE',1202,498,7.3,True,width=36)
icon('check',1247,495)
text('≥95% completed',1253,498,6.6,width=73)
icon('cancel',1335,495)
text('≤2% service cancellations',1342,498,6.6,width=103)
icon('help',1453,495)
text('≥90% help within 24h',1461,498,6.6,width=65)
path('M1202 501Q1343 502 1518 501',colour=CYAN,width=.6)
# Review targets follow the same two month markers as the adjacent budget cell.
text('M4 review',1202,512,8,True,width=88)
text('≥200 first paid riders',1202,522,6.8,width=100)
text('M1–2 data checks',1202,534,6.8,width=99)
text('M6 review',1316,512,8,True,width=94)
text('≥450 first paid riders',1316,521,6.8,width=97)
text('≤DKK175 paid acquisition',1316,530,6.8,width=97)
text('≥35% 90-day repeat†',1316,539,6.8,width=96)
path('M1306 507V543',colour=CYAN,width=.6)
icon('leaf',1433,514,.8)
text('BRAND UPSIDE',1443,512,7.4,True,width=76)
text('Organic · referrals ·',1428,522,6.8,width=87)
text('extra rides',1428,532,6.8,width=75)
text('Track separately',1428,542,6.8,width=75)
# Narrow the lower lane with the wheel arch; keep every approved tracking term.
path('M1202 538Q1260 537 1301 538',colour=GOLD,width=.8)
text('TRACKING PROPOSED',1202,550,7.3,True,width=107)
text('Ads + trips + dispatch/help',1202,561,6.8,width=91)
icon('data',1207,570,.55)
text('→ Big Data dashboard',1212,573,6.8,width=73)
text('Weekly actions ·',1202,581,6.6,width=70)
text('monthly cohorts',1202,590,6.6,width=64)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode: raise RuntimeError(proc.stderr.read())
layer='<g id="section-08-v01-candidate" clip-path="url(#cell-08-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
assert base.endswith('</g></svg>') and 'id="cell-08-clip"' in base
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
transparent=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1015" viewBox="1185 400 351 198"><defs><clipPath id="cell-08-clip"><path d="{CELL}"/></clipPath></defs>{layer}</svg>'
(HERE/f'{PREFIX}-layout.svg').write_text(transparent)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1027" viewBox="1179 514.817073 368 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
(HERE/f'{PREFIX}-copy.md').write_text('## 8. Success Dashboard\n<!-- budget: 150 -->\n\n'+'\n\n'.join(r['text'] for r in records[1:])+'\n')
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
checks={'status':'Approved compact content/layout D-108; fitted image pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'cell_path':CELL,'a0_mm':[1189,841],'visible_text':records,'word_bearing_tokens':sum(bool(re.search(r'\w',w)) for w in displayed.split()),'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'raster_images_added':0,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'manual_visual_review':'Pending controller inspection; physical A0 proof untested'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
