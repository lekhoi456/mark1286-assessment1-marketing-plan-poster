"""Fit the selected four-step Ride Innovation board into the lower-left car cell."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '09-cell-fit-v01-2026-10-05'
BASE = HERE / '04-cell-fit-v01-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M400 608 H836 Q859 608 859 631 V724 Q859 747 835 747 H430 Q409 747 401 728 L379 637 Q373 608 400 608 Z'
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



def arrow(x1,y1,x2,y2,colour=CYAN):
    path(f'M{x1} {y1}L{x2} {y2}',colour=colour,width=.8)
    a=math.atan2(y2-y1,x2-x1)
    path(f'M{x2-3*math.cos(a-.55)} {y2-3*math.sin(a-.55)}L{x2} {y2}L{x2-3*math.cos(a+.55)} {y2-3*math.sin(a+.55)}',colour=colour,width=.8)

def phone(x,y):
    path(f'M{x+2} {y}Q{x} {y} {x} {y+2}V{y+19}Q{x} {y+21} {x+2} {y+21}H{x+12}Q{x+14} {y+21} {x+14} {y+19}V{y+2}Q{x+14} {y} {x+12} {y}Z',CREAM,width=.8)
    path(f'M{x+3} {y+5}H{x+11}M{x+3} {y+8}H{x+9}',colour=CYAN,width=.7)
    path(f'M{x+5} {y+14}Q{x+5} {y+10} {x+7} {y+10}Q{x+10} {y+10} {x+10} {y+14}L{x+11} {y+16}H{x+4}Z',GOLD,colour=NAVY,width=.6)

def data(x,y):
    path(f'M{x} {y+3}Q{x+8} {y-1} {x+16} {y+3}V{y+18}Q{x+8} {y+22} {x} {y+18}Z','#e9f7f5',width=.8)
    path(f'M{x} {y+3}Q{x+8} {y+7} {x+16} {y+3}M{x} {y+10}Q{x+8} {y+14} {x+16} {y+10}',colour=CYAN,width=.7)

def ai(x,y):
    circle(x,y,10,'#fff5c9',.8)
    pts=[(x-5,y-4),(x+5,y-4),(x-4,y+5),(x+5,y+4)]
    path(f'M{pts[0][0]} {pts[0][1]}L{pts[1][0]} {pts[1][1]}L{pts[2][0]} {pts[2][1]}L{pts[3][0]} {pts[3][1]}',colour=CYAN,width=1.1)
    for a,b in pts:circle(a,b,1.3,CREAM,.5)

def taxi(x,y):
    path(f'M{x} {y+9}L{x+5} {y+2}H{x+16}L{x+22} {y+9}L{x+24} {y+11}V{y+17}H{x}Z',CYAN,width=.8)
    path(f'M{x+5} {y+8}L{x+8} {y+4}H{x+15}L{x+19} {y+8}Z',CREAM,width=.55)
    circle(x+5,y+17,2.5,CREAM,.8);circle(x+19,y+17,2.5,CREAM,.8)

def support(x,y):
    circle(x+7,y+5,4,CREAM,.7)
    path(f'M{x} {y+19}Q{x+1} {y+10} {x+7} {y+10}Q{x+14} {y+10} {x+14} {y+19}',colour=NAVY,width=.8)
    path(f'M{x+2} {y+6}Q{x+1} {y-1} {x+7} {y-1}Q{x+14} {y-1} {x+13} {y+7}L{x+10} {y+8}',colour=CYAN,width=.9)

def calendar(x,y):
    path(f'M{x} {y+3}H{x+16}V{y+20}H{x}Z','#fff5c9',width=.8)
    path(f'M{x} {y+8}H{x+16}',colour=CYAN,width=.7)
    path(f'M{x+4} {y}V{y+5}M{x+12} {y}V{y+5}',colour=GOLD,width=1.2)
    path(f'M{x+4} {y+13}H{x+7}M{x+10} {y+13}H{x+13}',colour=NAVY,width=.6)

w=text('9. Ride Innovation',405,628,11,True,width=127)
path(f'M405 632Q{405+w/2} 633 {405+w} 632',colour=GOLD,width=1.2)
text('PROPOSED PILOTS',542,627,7.8,True,width=95)
text('ADVERTISED: COPENHAGEN',663,620,6.4,True,width=179)
text('App booking · Pre-book: max 30 days',663,629,6.4,width=179)
text('Performance untested',663,637,6.4,width=179)

for x in [519,627,737]:path(f'M{x} 646Q{x-1} 679 {x} 714',colour='#9cc9c7',width=.5)
# Each lane retains one proposed mechanism and its indispensable testing limit.
text('01 Target S1',410,647,7.8,True,width=99)
data(414,654);arrow(432,665,445,665);ai(459,664);arrow(472,665,484,665);phone(489,653)
text('Consented first-party data',410,684,6.6,width=103)
text('Big Data + AI → reminders',410,694,6.6,width=103)
text('Purpose/quality/access',410,704,6.6,width=103)
text('No bought/sensitive profiles',410,714,6.6,width=103)

text('02 Dispatch AI',528,647,7.8,True,width=99)
phone(531,653);arrow(549,665,560,665);ai(573,664);arrow(586,665,594,665);taxi(597,655)
text('Booking → AI match',528,686,6.6,width=103)
text('Local baseline comparison',528,694,6.6,width=103)
text('Match time · Fulfilment',528,704,6.6,width=103)
text('Cancellations · Fairness',528,714,6.6,width=103)
text('Gain unproven',557,678,6.4,width=65)

text('03 Connect care',638,647,7.8,True,width=94)
text('ONE TRIP ID',656,655,6.4,True,width=60)
path('M665 657Q651 657 647 660M680 657V661M695 657Q710 657 716 661',colour=CYAN,width=.7)
phone(642,661);taxi(671,663);support(711,661)
text('Support · Ratings',638,694,6.6,width=96)
text('Test FAQ bot',638,704,6.6,width=96)
text('→ Human hand-off',638,714,6.6,width=96)

text('04 Test retention',747,647,7.8,True,width=98)
text('First: frequency + contribution',747,655,6.4,width=99)
taxi(754,657);path('M790 662V675M784 665H796M787 665L783 671H791ZM793 665L789 671H797Z',colour=CYAN,width=.55);calendar(806,658)
text('Pay-per-trip',747,684,6.6,width=98)
text('Prepaid/monthly · Needs-matched',747,694,6.6,width=98)
text('Retention + margin',747,704,6.6,width=98)
text('Stop if either falls',747,714,6.6,width=98)

arrow(505,665,526,665);arrow(622,665,639,665);arrow(726,665,744,665)
# Learning loop returns through all lanes. Text sits above the return path.
path('M843 718V724H423V718',colour=CYAN,width=.8)
path('M420 721L423 718L426 721',colour=CYAN,width=.8)
path('M597 720H674V727H597Z',CREAM,colour=CREAM,width=.2)
text('MEASURE / REFINE',602,725,6.4,True,width=69)

text('BEFORE PILOTS',422,735,6.4,True,width=55)
text('Privacy/tech/operations + group approval',481,735,6.4,width=164)
text('Unpriced dispatch/chatbot/subscription:',422,743,6.4,width=154)
text('cost separately',579,743,6.4,width=64)
text('DKK600,000 excludes app/platform build +',655,734,6.4,width=187)
text('vehicle/driver/frontline operations',655,743,6.4,width=187)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-09-v01-candidate" clip-path="url(#cell-09-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();assert base.endswith('</g></svg>')
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2400" height="740" viewBox="372 725.817073 494 152"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2400)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
vertices=[(400,608)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
line(836,608);curve((859,608),(859,631));line(859,724);curve((859,747),(835,747));line(430,747);curve((409,747),(401,728));line(379,637);curve((373,608),(400,608))
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'None in Section 9; source-inspired simple original vector diagrams','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
