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
PREFIX = '03-cell-fit-v06-2026-10-05'
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



# No Green SM graphic logo in this cell: the gained area belongs to positioning.
w=text('3. Why Green SM?',933,250,9.6,True,width=184)
path(f'M933 254Q{933+w/2} 255 {933+w} 254',colour=GOLD,width=1.25)
text('Positioning Strategy',1130,250,7.2,width=113)
text('Electric rides. One managed experience.',933,273,11.3,True,width=310)
text('Cleaner · Quieter · More reliable',933,285,7.6,width=206)
text('Company promise',1141,285,6.8,width=100)
path('M934 291Q1090 292 1244 290',colour=CYAN,width=.7)
# Operating structures are contrasted visually, without rating rival quality.
text('Green SM',933,305,9.5,True,width=142)
text('Competitors',1099,305,9.5,True,width=145)
text('Taxi partners operate rides',1099,317,7.1,width=146)
path('M1090 300Q1088 327 1090 349',colour=CYAN,width=.6)
# Owned app -> owned fleet -> employed driver, all within the operator's delivery chain.
path('M939 313Q936 313 936 316V336Q936 339 939 339H950Q953 339 953 336V316Q953 313 950 313Z',CYAN,width=.85)
path('M939 317H950V333H939Z',CREAM,width=.6)
path('M942 315H947 M942 336H947',width=.5)
path('M941 329L944 325L946 327L948 321',colour=CYAN,width=.8)
path('M946 320Q946 317 948 317Q950 317 950 320L948 323Z',GOLD,width=.5)
path('M958 327H967L963 323 M967 327L963 331',colour=CYAN,width=.9)
path('M975 325L982 316H997L1005 325L1012 328V336H974V329Z',CYAN,width=.8)
path('M981 323L985 318H990V324Z M993 318H997L1002 324H993Z',CREAM,width=.6)
path('M984 316L985 312H995L997 316Z',GOLD,width=.6)
circle(981,336,3.7,NAVY,.6);circle(981,336,1.6,CREAM,.4)
circle(1006,336,3.7,NAVY,.6);circle(1006,336,1.6,CREAM,.4)
path('M997 326L994 330H997L994 333',colour=CREAM,width=.8)
path('M1016 327H1025L1021 323 M1025 327L1021 331',colour=CYAN,width=.9)
circle(1040,319,4.3,CREAM,.8)
path('M1036 316Q1040 312 1044 316',NAVY,width=.55)
path('M1033 336V330Q1034 326 1040 326Q1046 326 1047 330V336Z',CYAN,width=.8)
path('M1038 327L1040 330L1042 327 M1040 330V334',width=.55)
text('Own app',933,349,6.9,width=37)
text('Owned fleet',974,349,6.9,width=53)
text('Employed drivers',1031,349,6.9,width=54)
# The actual taxi providers behind each rival app, rather than a vague partners label.
text('Uber',1100,330,8.2,True,width=28)
path('M1132 327H1140L1137 324 M1140 327L1137 330',colour=CYAN,width=.85)
text('Drivr · Dantaxi',1146,330,7.3,width=98)
text('Bolt',1100,348,8.2,True,width=28)
path('M1132 345H1140L1137 342 M1140 345L1137 348',colour=CYAN,width=.85)
text('Viggo/Bolt · Taxa 4x27',1146,348,7.3,width=98)
# Points of parity are explicit: app booking/electric access cannot by themselves establish a USP.
text('Shared: App booking · Electric options',933,363,7.7,width=311)
path('M934 369Q1086 370 1247 369',colour=CYAN,width=.65)
# Proposed reason to choose, supported by the operating structure above.
text('Proposed edge:',933,384,7.1,width=63)
text('Direct control → one service standard',1000,384,8.2,True,width=245)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-03-v06-candidate" clip-path="url(#cell-03-clip)">'+'\n'.join(parts)+'</g>'
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Removed from Section 3 as requested; text brand name retained for comparison','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
