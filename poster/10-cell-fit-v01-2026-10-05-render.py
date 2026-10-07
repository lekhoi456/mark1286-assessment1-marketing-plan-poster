"""Fit the selected four-business-goal board into the lower-right car cell."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '10-cell-fit-v01-2026-10-05'
BASE = HERE / '09-cell-fit-v01-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M890 608 H1240 Q1269 608 1258 636 L1224 725 Q1217 747 1193 747 H890 Q867 747 867 724 V631 Q867 608 890 608 Z'
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

w=text('10. Business Goals & Growth',883,628,10.5,True,width=227)
path(f'M883 632Q{883+w/2} 633 {883+w} 632',colour=GOLD,width=1.2)
text('Green · smart · sustainable mobility',883,640,6.6,width=209)
text('Proposed 12-month plan',1115,624,6.6,width=132)
text('Local outcomes untested',1115,635,6.6,width=132)
text('Repeat: full 90-day follow-up',1115,644,6.4,width=130)

# Four business goals; short mechanism labels replace the original long O-code rows.
path('M1062 648V719',colour='#9cc9c7',width=.5)
path('M884 688H1228',colour='#9cc9c7',width=.5)

# Stable service: controlled fleet/driver cue and an explicit scaling condition.
taxi(886,658);circle(897,648,4,CREAM,.7);path('M890 660Q891 653 897 653Q904 653 904 660',colour=NAVY,width=.8)
text('Stable local operation',920,654,8.1,True,width=134)
text('Owned fleet + employed drivers',920,666,6.6,width=133)
text('Service + 90-day repeat → scale',920,678,6.6,width=133)

# Local recognition: search/social phone and a small screen, without branding logos.
phone(1071,651)
path('M1090 658H1103V669H1090ZM1096 669V673M1092 673H1100',fill='#e9f7f5',width=.7)
circle(1089,652,3.7,CREAM,.7);path('M1092 655L1095 658',width=.8)
text('Become known locally',1110,654,8.1,True,width=128)
text('Search / social → paid trial',1110,666,6.6,width=126)
text('Screens after service +',1110,676,6.6,width=121)
text('90-day repeat checks',1110,685,6.6,width=118)

# Core mission: electric car plus app, using broad flat fill regions.
phone(884,695);taxi(900,699)
path('M914 693L910 699H914L911 705',colour=GOLD,width=1.5)
text('Green & smart mobility',928,699,8.1,True,width=134)
text('App-booked electric rides',928,710,6.6,width=134)
text('Easy to understand + use',928,719,6.6,width=134)

# Repeat use supports sustainable growth; circular arrows show the proposed retention logic.
circle(1087,707,9,'#fff5c9',.65)
path('M1081 708Q1080 702 1086 701Q1091 701 1093 705M1090 702L1093 705L1094 701',colour=CYAN,width=.9)
path('M1093 708Q1093 714 1087 715Q1083 715 1081 711M1080 715L1081 711L1085 713',colour=CYAN,width=.9)
text('Sustainable growth',1110,699,8.1,True,width=113)
text('Retention + contribution',1110,710,6.6,width=110)
text('Repeat before expansion',1110,719,6.6,width=105)

# Year-two decision is shared across the four goals; year one remains an entry investment.
path('M882 724H1224L1219 742H883Z','#fff5c9',colour='#e3bb42',width=.45)
text('M12 review:',889,732,6.6,True,width=43)
text('Consideration · paid trial · service · 90-day repeat · contribution',936,732,6.4,width=282)
text('Renew · Revise · Stop',889,741,7.2,True,width=105)
text('Entry investment · first-year break-even not required',1000,741,6.4,width=214)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-10-v01-candidate" clip-path="url(#cell-10-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();assert base.endswith('</g></svg>')
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2400" height="936" viewBox="860 725.817073 405 158"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2400)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
vertices=[(890,608)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
line(1240,608);curve((1269,608),(1258,636));line(1224,725);curve((1217,747),(1193,747));line(890,747);curve((867,747),(867,724));line(867,631);curve((867,608),(890,608))
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
checks={'status':'Fitting authorised; reduced copy/art pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'None in Section 10; source-inspired simple original vector diagrams','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
