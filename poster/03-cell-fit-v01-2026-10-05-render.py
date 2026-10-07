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
PREFIX = '03-cell-fit-v01-2026-10-05'
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
source=ET.parse(HERE/'03-logo-candidate.svg').getroot()
logo=deepcopy(source.find('.//*[@id="authentic-logo"]'))
assert logo is not None
for node in logo.iter():
    if 'id' in node.attrib:node.set('id','fit03-'+node.attrib['id'])
    for key,value in list(node.attrib.items()):
        if 'url(#authentic-' in value:node.set(key,value.replace('url(#authentic-','url(#fit03-authentic-'))
logo.set('x','1160');logo.set('y','240');logo.set('width','77');logo.set('height','23')
parts.append(ET.tostring(logo,encoding='unicode'))
w=text('3. Why Green SM?',933,251,12,True,width=216)
path(f'M933 256Q{933+w/2} 257 {933+w} 256',colour=GOLD,width=1.3)
text('Positioning Strategy',933,265,7.8,width=160)
text('Proposed position',933,277,7.2,width=150)
text('Self-paying Copenhagen residents aged 25–44',933,291,7.4,width=176)
text('Recurring local taxi trips · within the service area',933,303,7.4,width=176)
path('M1114 295H1135 M1131 292L1135 295L1131 298',colour=CYAN,width=1.1)
text('App-booked electric',1144,291,8,width=102)
text('taxi rides',1144,303,8,width=102)
# Three equal visual pillars: EV, app, and direct service control.
# Draw the EV and plug in broad flat regions, using no decorative street detail.
path('M941 339L945 334L950 330H964L972 335L978 338V343H940V339Z',CYAN,width=.75)
path('M949 334L952 331H962L967 335H949Z',CREAM,width=.55)
circle(948,343,3,NAVY,.4);circle(948,343,1.4,CREAM,.3)
circle(969,343,3,NAVY,.4);circle(969,343,1.4,CREAM,.3)
path('M973 330Q977 328 977 324H981V329H977 M978 322V324 M980 322V324',colour=CYAN,width=.7)
text('Electric',937,355,9.2,True,width=94)
text('Generally quieter',937,365,7,width=91)
text('than combustion-',937,375,7,width=91)
text('engine vehicles',937,385,7,width=91)
# A phone screen communicates booking: location pin, route and one clear button.
path('M1070 327Q1070 324 1073 324H1084Q1087 324 1087 327V343Q1087 346 1084 346H1073Q1070 346 1070 343Z',CYAN,width=.75)
path('M1072 328H1085V341H1072Z',CREAM,width=.5)
path('M1076 326H1081',width=.5)
path('M1075 338Q1082 338 1078 335Q1075 332 1081 332',colour=CYAN,width=.7)
circle(1075,338,.9,CREAM,.4)
path('M1079.5 330Q1079.5 328.5 1081 328.5Q1082.5 328.5 1082.5 330Q1082.5 331 1081 332.5Q1079.5 331 1079.5 330Z',GOLD,width=.4)
path('M1075 343H1082',colour=GOLD,width=1.3)
text('Smart',1040,355,9.2,True,width=88)
text('App booking',1040,365,7,width=90)
text('Clear terms: area · hours · fares',1040,375,7,width=96)
text('Trip reference · local help',1040,385,7,width=90)
parts.append('<g transform="translate(0 3)">')
# Driver, standards clipboard and headset show how the company controls delivery.
circle(1159,330,3,CREAM,.55)
path('M1156 329Q1156 326 1159 326Q1162 326 1162 329Z',NAVY,width=.4)
path('M1151 343L1153 336Q1159 332 1165 336L1167 343Z',CYAN,width=.65)
circle(1159,340,3.3,CREAM,.5)
path('M1156 340H1162 M1159 340V343',width=.5)
path('M1173 327H1186V344H1173Z',CREAM,width=.6)
path('M1177 325H1182V329H1177Z',GOLD,width=.5)
path('M1176 333L1177 334L1179 331 M1181 333H1184 M1176 339L1177 340L1179 337 M1181 339H1184',width=.55)
path('M1194 337Q1194 329 1200 329Q1206 329 1206 337',width=.7)
path('M1193 336H1196V342H1193Z M1204 336H1207V342H1204Z',CYAN,width=.55)
path('M1206 342Q1206 345 1202 345 M1200 345H1202',width=.6)
parts.append('</g>')
text('Controlled service',1142,355,8.7,True,width=104)
text('Owned fleet · Employed drivers',1142,365,6.9,width=106)
text('Trained drivers · Standards',1142,375,6.9,width=106)
text('Customer service procedures',1142,385,6.9,width=106)
# Keep the neutral partner-model comparison explicit, without rival quality scores.
# The comparison fits in the available upper-right band rather than tiny bottom lettering.
text('Uber / Bolt:',1142,313,6.8,width=104)
text('Taxi partners operate rides',1142,323,6.8,width=104)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-03-v01-candidate" clip-path="url(#cell-03-clip)">'+'\n'.join(parts)+'</g>'
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Shared hand-drawn Green SM asset reused unchanged with unique nested ids','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
