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
PREFIX = '03-cell-fit-v03-2026-10-05'
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
w=text('3. Why Green SM?',933,251,12,True,width=205)
path(f'M933 256Q{933+w/2} 257 {933+w} 256',colour=GOLD,width=1.3)
asset('authentic-logo',1162,236,81,23)
text('Positioning Strategy',933,268,7.8,width=135)
text('Company promise',1135,268,7.1,width=108)
# One corporate positioning sentence, separated from implementation evidence.
text('Cleaner · Quieter · More reliable rides',933,286,11.3,True,width=310)
path('M935 292Q1088 293 1242 291',colour=CYAN,width=.7)
# Three broad visual zones, with direct benefit-to-capability relationships.
text('100% electric',933,304,9,True,width=95)
text('Smart app booking',1039,304,8.6,True,width=102)
text('Professional care',1147,304,8.6,True,width=98)
# A large simple leaf, without texture or tiny components.
path('M938 330Q934 313 952 313Q957 332 938 330Z',CYAN,width=.9)
path('M938 334Q942 325 951 317',width=.85)
text('Zero tailpipe',960,321,7.2,width=70)
text('emissions',960,333,7.2,width=70)
text('Quieter EV rides',933,350,7.8,width=98)
# Minimal phone -> electric taxi diagram, deliberately easy to colour by hand.
path('M1040 312Q1036 312 1036 316V344Q1036 348 1040 348H1055Q1059 348 1059 344V316Q1059 312 1055 312Z',CYAN,width=.9)
path('M1040 317H1055V341H1040Z',CREAM,width=.6)
path('M1045 314H1050 M1045 345H1050',width=.65)
path('M1043 336L1047 332L1050 333L1052 326',colour=CYAN,width=1.1)
path('M1048 324Q1048 320 1051 320Q1055 320 1055 324Q1055 326 1051 329Q1048 326 1048 324Z',GOLD,width=.65)
circle(1051.5,323.5,.85,CREAM,.45)
path('M1063 331H1071L1068 328 M1071 331L1068 334',colour=CYAN,width=1)
# Broad car silhouette and just two wheels/windows; no street map, grille texture or facial detail.
path('M1078 332L1086 320Q1090 317 1101 317H1113L1123 330L1133 334V345H1075V336Z',CYAN,width=.95)
path('M1086 329L1091 322H1102V330Z M1106 322H1112L1118 330H1106Z',CREAM,width=.7)
path('M1105 332V342 M1110 334H1114',width=.65)
path('M1098 319L1099 315H1108L1109 319Z',GOLD,width=.65)
path('M1077 335H1081V339H1076 M1127 336H1132V339H1127Z',GOLD,width=.55)
circle(1086,345,4.5,NAVY,.7);circle(1086,345,2.1,CREAM,.55)
circle(1124,345,4.5,NAVY,.7);circle(1124,345,2.1,CREAM,.55)
path('M1113 332L1109 337H1113L1110 342',colour=CREAM,width=1.1)
text('App → electric taxi',1040,359,7.1,width=99)
# Professional service: one friendly driver badge, rather than a complex portrait.
circle(1155,319,4.4,CREAM,.8)
path('M1151 316Q1155 311 1159 316',NAVY,width=.6)
path('M1148 335V330Q1149 326 1155 326Q1161 326 1162 330V335Z',CYAN,width=.8)
path('M1153 327L1155 330L1157 327 M1155 330V334',width=.55)
text('Trained drivers',1168,322,7.1,width=78)
text('Service standards',1168,334,7.1,width=78)
text('Customer support',1147,350,7.8,width=100)
# A proposed operating mechanism supplies the reason to believe; rivals are compared only by model.
path('M934 363Q1088 364 1247 363',colour=CYAN,width=.7)
text('Plan: Owned fleet · Employed drivers → Service control',933,376,8.1,width=313)
text('Uber / Bolt: Taxi partners operate rides',933,387,7.2,width=307)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-03-v03-candidate" clip-path="url(#cell-03-clip)">'+'\n'.join(parts)+'</g>'
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Approved shared hand-drawn Green SM logo reused unchanged; new simple native phone/taxi and service icons','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
