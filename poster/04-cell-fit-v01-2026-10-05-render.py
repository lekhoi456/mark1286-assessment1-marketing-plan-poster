"""Redesign positioning around verified Danish corporate promise and simple visual benefits."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '04-cell-fit-v01-2026-10-05'
BASE = HERE / '03-cell-fit-v06-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M1286 231 Q1354 234 1401 250 Q1436 261 1456 287 L1497 367 Q1512 389 1495 390 H1293 Q1272 390 1271 370 L1264 251 Q1263 231 1286 231 Z'
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



from xml.etree import ElementTree as ET
from copy import deepcopy
ET.register_namespace('', 'http://www.w3.org/2000/svg')
source=ET.parse(HERE.parent/'archive/04-candidate-v02-2026-10-04.svg').getroot()
logo=deepcopy(next(e for e in source if e.tag.endswith('image')))
# Reuse the exact approved-source hand-drawn logo pixels, placing them within the narrow roof portion.
logo.set('x','1278');logo.set('y','261');logo.set('width','100');logo.set('height','26')
parts.append(ET.tostring(logo,encoding='unicode'))

def centred(value,left,right,y,size=6.8,heading=False):
    w=text(value,left,y,size,heading,width=right-left)
    shift=(right-left-w)/2
    parts[-1]=parts[-1].replace(f'translate({left} {y})',f'translate({left+shift} {y})')
    records[-1]['bbox'][0]+=shift;records[-1]['bbox'][2]+=shift

w=text('4. Branding & Identity',1278,256,9.2,True,width=115)
path(f'M1278 260Q{1278+w/2} 261 {1278+w} 260',colour=GOLD,width=1.2)
text('Green SM =',1278,295,7.4,True,width=106)
text('Green and Smart Mobility',1278,307,7.4,width=114)
# Corporate slogan is the dominant message beneath the logo/name meaning.
text('Go Green For',1278,319,9.2,True,width=114)
text('a Green Future.',1278,331,9.2,True,width=114)
# Palette follows the expanding diagonal; swatches are broad solid colour shapes.
text('Primary',1394,275,6.6,width=45)
circle(1399,285,6,CYAN,.75)
text('New Cyan',1408,286,7.1,True,width=46)
text('#28bdbf',1394,298,6.6,width=62)
text('Pantone 319 C',1394,310,6.6,width=65)
text('Secondary',1394,322,6.6,width=65)
circle(1399,334,6,'#e3bb42',.75)
text('New Yellow',1408,335,7.1,True,width=68)
text('#e3bb42',1408,347,6.6,width=62)
# Typeface label and illustrative hand-drawn specimen; not an installed corporate-font demonstration.
text('Aa',1278,347,11,True,width=23)
text('Xanh Display 2.0',1306,346,7.5,width=82)
# Liquid Glass is represented as a simple layered-panel phone, without gradients/reflections.
path('M1283 351Q1280 351 1280 354V373Q1280 376 1283 376H1294Q1297 376 1297 373V354Q1297 351 1294 351Z',CREAM,width=.8)
path('M1283 355Q1288 354 1294 355V371Q1289 372 1283 371Z','#e9f7f5',colour=CYAN,width=.55)
path('M1284 358Q1288 357 1293 358V362Q1288 363 1284 362Z',CYAN,width=.45)
path('M1285 364Q1289 363 1294 364V368Q1289 369 1285 368Z','#e3bb42',width=.45)
path('M1286 353H1291',width=.5)
text('Modern Liquid Glass UI/UX',1304,360,7.1,True,width=157)
text('Layered · soft · clear',1304,372,6.8,width=170)
# Secondary tagline and language application remain distinct from the corporate slogan.
centred('Clear terms. Local care.',1304,1487,380,7.0)
centred('Danish first · English second',1304,1487,387.5,6.6)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-04-v01-candidate" clip-path="url(#cell-04-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();assert base.endswith('</g></svg>')
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2000" height="1344" viewBox="1258 344.817073 253 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2000)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
vertices=[(1286,231)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
curve((1354,234),(1401,250));curve((1436,261),(1456,287));line(1497,367);curve((1512,389),(1495,390));line(1293,390);curve((1272,390),(1271,370));line(1264,251);curve((1263,231),(1286,231))
def inside(x,y):
    hit=False
    for (ax,ay),(bx,by) in zip(vertices,vertices[1:]+vertices[:1]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:hit=not hit
    return hit
outside=[];overlaps=[]
for i,r in enumerate(records):
    a=r['bbox']
    if not all(inside(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]):outside.append(r)
    for other in records[i+1:]:
        b=other['bbox']
        if min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]):overlaps.append([r['text'],other['text']])
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Original embedded hand-drawn logo from archive/04-candidate-v02-2026-10-04.svg reused unchanged','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
