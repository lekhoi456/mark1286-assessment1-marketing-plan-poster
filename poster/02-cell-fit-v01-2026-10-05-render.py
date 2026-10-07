"""Fit Section 1 into the current A0, preserving the background and Sections 5–8."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '02-cell-fit-v01-2026-10-05'
BASE = HERE / '01-cell-fit-v06-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M636 230 H884 Q904 230 906 250 V370 Q906 390 884 390 H633 Q611 390 611 370 L615 250 Q615 230 636 230 Z'
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



# Keep the chart small and allocate the right-hand space to audience conditions.
w=text('2. Target Market',629,251,12,True,width=270)
path(f'M629 256Q{629+w/2} 257 {629+w} 256',colour=GOLD,width=1.3)
text('Copenhagen residents aged 25–44',629,267,8.2,width=269)
text('Copenhagen · 1 Jul 2026 · 18+',630,279,6.8,width=158)
path('M640 286V324H787',width=.65)
text('0',631,326,6.2,width=8)
# Every height is count / 300,000 * 38; baseline never moves.
bars=[]
for i,(age,count) in enumerate([('18–24',72396),('25–44',269277),('45–64',143668),('65+',74728)]):
    cx=658+i*36;top=324-count/300000*38
    fill=CYAN if age=='25–44' else '#dfeceb'
    path(f'M{cx-12} 324V{top}H{cx+12}V324Z',fill,width=.65)
    value=f'{count:,}'
    # Centre the glyph advance above each column.
    proc.stdin.write(json.dumps({'text':value,'font':'ChalkboardSE-Regular','size':6.5})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(value,cx-measured/2,top-3,6.5,width=34)
    proc.stdin.write(json.dumps({'text':age,'font':'ChalkboardSE-Regular','size':7.1})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(age,cx-measured/2,335,7.1,width=34)
    if age=='25–44':
        text('40.2%',cx-11,308,7,width=22)
        text('of city',cx-9,319,6.2,width=22)
    bars.append({'age':age,'count':count,'top':top,'baseline':324,'height':324-top})
# Three simple, unboxed icons replace repeated audience labels.
path('M800 284H810V293H798V285H808 M807 287H812V291H807Z',CYAN,width=.65)
circle(809.5,289,.45,GOLD,.2)
text('Self-paying',818,293,8.1,width=82)
path('M798 308L801 304H807L811 308V312H797V308Z',GOLD,width=.65)
path('M801 308L802 306H806L808 308Z',CREAM,width=.5)
circle(800,312,1.6,NAVY,.3);circle(808,312,1.6,NAVY,.3)
text('Existing taxi users',818,311,7.8,width=83)
path('M798 319H810V330H798Z',CREAM,width=.65)
path('M798 322H810 M801 317V321 M807 317V321',colour=CYAN,width=.8)
path('M801 327Q804 324 807 327 M805 326L807 327L806 329',colour=CYAN,width=.65)
text('Recurring local trips',818,329,7.7,width=83)
text('City population (all ages): 670,389',630,346,7.4,width=269)
path('M630 351H893',colour=CYAN,width=.65)
# Proposed profile remains distinct from the measured age pool.
text('Proposed rider profile',630,363,7.8,width=96)
path('M630 370Q630 367 633 367Q636 367 636 370Q636 373 633 376Q630 373 630 370Z',GOLD,width=.55)
circle(633,370,.8,CREAM,.3)
text('Within the service area',640,376,7.2,width=89)
# A broad-colour rider silhouette with a phone; no facial or fabric detail.
circle(744,359,4.2,CREAM,.65)
path('M740 359Q739 353 745 354Q748 354 748 358',NAVY,width=.5)
path('M734 377L736 368Q737 365 742 365H747Q752 365 754 377Z',CYAN,width=.7)
path('M749 367H755V375H749Z',CREAM,width=.65)
path('M741 372L749 373 M752 369H753',width=.55)
# Preference icons are large single shapes, suitable for manual colouring.
path('M765 353L770 354L772 359L769 361L764 357Z',GOLD,width=.55)
circle(768,355.5,.55,CREAM,.25)
text('Price-conscious',778,360,7.5,width=114)
path('M765 364H771V372H765Z',CREAM,width=.55)
path('M766 369L769 367L770 368',colour=CYAN,width=.65)
text('Values trip control',778,371,7.5,width=114)
path('M764 382V378Q768 373 772 378V382 M764 379H766V382H764 M770 379H772V382H770',colour=CYAN,width=.65)
text('Expects fair treatment',778,382,7.5,width=114)
text('Recurring trips → repeat rides',630,385,6.5,width=125)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-02-v01-candidate" clip-path="url(#cell-02-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();assert base.endswith('</g></svg>')
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1008" viewBox="607 344.817073 303 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
# Test against the native rounded-cell outline rather than its enclosing rectangle.
vertices=[(636,230)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
line(884,230);curve((904,230),(906,250));line(906,370);curve((906,390),(884,390));line(633,390);curve((611,390),(611,370));line(615,250);curve((615,230),(636,230))
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
checks={'status':'Fitting authorised; artwork/reduced copy pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'bars':bars,'scale':{'minimum':0,'maximum':300000,'height':38},'denominator':670389,'selected_share_actual':269277/670389*100,'selected_share_rounded':'40.2%','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','bars']},ensure_ascii=False,indent=2))
