"""Fit Section 2 with recognisable icons, preserving all wording and other sections."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '03-cell-fit-v02-2026-10-05'
BASE = HERE / '02-cell-fit-v03-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M938 230 H1227 Q1247 230 1250 250 L1257 370 Q1259 390 1237 390 H936 Q914 390 914 370 V250 Q914 230 938 230 Z'
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
source=ET.parse(HERE.parent/'archive/03-approved.svg').getroot()
# The approved artwork is reused unchanged; IDs/references are isolated for assembly.
def remap(element):
    element=deepcopy(element)
    for node in element.iter():
        if 'id' in node.attrib:node.set('id','fit03-approved-'+node.attrib['id'])
        for key,value in list(node.attrib.items()):
            if value.startswith('#'):node.set(key,'#fit03-approved-'+value[1:])
            elif 'url(#' in value:node.set(key,value.replace('url(#','url(#fit03-approved-'))
    return element
old_defs=source.find('{http://www.w3.org/2000/svg}defs')
keep=ET.Element('{http://www.w3.org/2000/svg}defs')
for node in old_defs:
    if node.tag.endswith('clipPath') or node.attrib.get('id')=='old-sheet':keep.append(remap(node))
parts.append(ET.tostring(keep,encoding='unicode'))
def asset(identifier,x,y,w,h):
    node=remap(source.find('.//*[@id="'+identifier+'"]'))
    node.set('x',str(x));node.set('y',str(y));node.set('width',str(w));node.set('height',str(h))
    parts.append(ET.tostring(node,encoding='unicode'))
w=text('3. Why Green SM?',933,251,12,True,width=310)
path(f'M933 256Q{933+w/2} 257 {933+w} 256',colour=GOLD,width=1.3)
text('Positioning Strategy',933,266,7.8,width=170)
text('Proposed position',1145,266,7.3,width=101)
asset('authentic-logo',1049,272,81,24)
# Restore the approved benefit groups on either side of the central offer.
path('M936 284Q984 281 1033 284L1036 335Q984 338 934 335Z',CREAM,width=.5)
path('M1144 284Q1193 281 1243 284L1248 335Q1193 338 1144 335Z',CREAM,width=.5)
text('Clear terms',938,295,9.2,True,width=94)
text('Local care',1149,295,9.2,True,width=95)
path('M938 298H1031 M1149 298H1241',colour=CYAN,width=.8)
# Large, recognisable map-pin, clock and receipt symbols.
path('M938 302L942 300L946 302L950 300V307L946 309L942 307L938 309Z',CREAM,width=.5)
path('M942 302Q942 299 944 299Q946 299 946 302Q946 303 944 305Q942 303 942 302Z',GOLD,width=.5)
text('Service area',955,307,7.2,width=76)
circle(944,315,3.8,CREAM,.6)
path('M944 312V315L947 317',width=.6)
text('Operating hours',955,319,7.2,width=76)
path('M940 323L941 322L942 323L943 322L944 323L945 322L946 323V331H940Z',CREAM,width=.5)
path('M941.5 325H944.5 M941.5 327H944.5 M941.5 329H944.5',colour=GOLD,width=.55)
text('Fare terms',955,331,7.2,width=76)
# Trip reference and a clear help route, preserving the approved benefit meaning.
path('M1149 302H1160V309H1149Q1151 307 1149 305Z',CREAM,width=.55)
path('M1156 302V309',colour=CYAN,width=.55)
text('Trip reference',1165,307,7.2,width=78)
path('M1149 319Q1149 312 1154 312Q1159 312 1159 319',width=.65)
path('M1148 317H1151V323H1148Z M1157 317H1160V323H1157Z',CYAN,width=.55)
path('M1159 323Q1159 326 1155 326 M1153 326H1155',width=.55)
text('A clear route',1165,320,7.2,width=78)
text('to local help',1165,331,7.2,width=78)
asset('green-sm-focal',1057,295,68,38)
path('M1036 316Q1047 310 1058 316 M1124 316Q1136 310 1144 316',colour=CYAN,width=.7)
text('App-booked electric rides',1047,341,7.3,width=94)
text('Generally quieter than combustion-engine vehicles',933,349,6.8,width=309)
text('Green SM: Owned fleet · Employed drivers',933,359,7.2,width=175)
text('Uber / Bolt: Taxi partners operate rides',1114,359,6.8,width=132)
text('Company service approach',933,368,7.3,width=170)
# Retain the corporate service approach with simple badge/clipboard/headset icons.
circle(939,375,2.2,CREAM,.5)
path('M935 381L936 378Q939 376 942 378L943 381Z',CYAN,width=.55)
text('Trained drivers',947,379.5,7.2,width=82)
path('M1040 373H1048V382H1040Z',CREAM,width=.55)
path('M1042 372H1046V374H1042Z',GOLD,width=.45)
path('M1042 377L1043 378L1045 375 M1042 380H1046',width=.5)
text('Operational standards',1053,379.5,7.2,width=87)
path('M1147 377Q1147 371 1151 371Q1155 371 1155 377',width=.6)
path('M1146 376H1149V380H1146Z M1153 376H1156V380H1153Z',CYAN,width=.45)
path('M1155 380Q1155 382 1152 382',width=.45)
text('Customer service procedures',1161,379.5,6.8,width=86)
text('Delivery plan: Use direct fleet and driver control to support clear terms and local help.',933,387,6.6,width=311)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-03-v02-candidate" clip-path="url(#cell-03-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();assert base.endswith('</g></svg>')
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2000" height="960" viewBox="909 344.817073 354 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2000)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
vertices=[(938,230)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
line(1227,230);curve((1247,230),(1250,250));line(1257,370);curve((1259,390),(1237,390));line(936,390);curve((914,390),(914,370));line(914,250);curve((914,230),(938,230))
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Approved shared hand-drawn Green SM asset reused unchanged; phone/taxi artwork reused from archive/03-approved.svg','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
