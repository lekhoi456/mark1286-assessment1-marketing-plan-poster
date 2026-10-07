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
PREFIX = '02-cell-fit-v03-2026-10-05'
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
path('M640 286V319H787',width=.65)
text('0',631,321,6.2,width=8)
# Every height is count / 300,000 * 38; baseline never moves.
bars=[]
for i,(age,count) in enumerate([('18–24',72396),('25–44',269277),('45–64',143668),('65+',74728)]):
    cx=658+i*36;top=319-count/300000*33
    fill=CYAN if age=='25–44' else '#dfeceb'
    path(f'M{cx-12} 319V{top}H{cx+12}V319Z',fill,width=.65)
    value=f'{count:,}'
    # Centre the glyph advance above each column.
    proc.stdin.write(json.dumps({'text':value,'font':'ChalkboardSE-Regular','size':6.5})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(value,cx-measured/2,top-3,6.5,width=34)
    proc.stdin.write(json.dumps({'text':age,'font':'ChalkboardSE-Regular','size':7.1})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(age,cx-measured/2,330,7.1,width=34)
    if age=='25–44':
        text('40.2%',cx-11,304,7,width=22)
        text('of city',cx-9,315,6.2,width=22)
    bars.append({'age':age,'count':count,'top':top,'baseline':319,'height':319-top})
# A single arrow selects the intersection of the three audience conditions.
path('M706 293L714 287H780Q783 287 783 291V304H788 M785 302L788 304L785 306',colour=CYAN,width=1)
path('M795 281Q791 281 791 285V297Q791 301 787.5 304Q791 307 791 311V329Q791 333 795 333',colour=CYAN,width=1)
# Wallet with a fold and clasp, a taxi with a roof sign, and a repeat calendar.
path('M798 285Q798 284 799 284H809V294H799Q798 294 798 293Z',CYAN,width=.7)
path('M800 284V282H809V285 M798 286H809',width=.65)
path('M807 287H812V291H807Z',CREAM,width=.65)
circle(809.5,289,.65,GOLD,.25)
text('Self-paying',818,293,8.1,width=82)
path('M797 309L800 305L803 303H807L810 306L812 308V312H797Z',GOLD,width=.7)
path('M801 307L803 304H806L809 307Z',CREAM,width=.55)
path('M803 302H806V303H803Z',GOLD,width=.5)
circle(800,312,1.7,NAVY,.35);circle(809,312,1.7,NAVY,.35)
text('Existing taxi users',818,311,7.8,width=83)
path('M800 321Q800 320 801 320H808Q809 320 809 321V329H800Z',CREAM,width=.65)
path('M800 323H809 M802 318.5V321.5 M807 318.5V321.5',colour=CYAN,width=.7)
# Two separated circular arrow segments make recurring trips recognisable.
path('M797 325Q797 316.5 805 316.5Q811 316.5 813 321 M810.5 319.5L813 321L813 318',colour=CYAN,width=.7)
path('M813 326Q813 333 805 333Q799 333 797 329 M797 332L797 329L799.5 330.5',colour=CYAN,width=.7)
text('Recurring local trips',818,329,7.7,width=83)
text('City population (all ages): 670,389',630,340,7.4,width=269)
path('M630 345H893',colour=CYAN,width=.65)
# Proposed profile remains distinct from the measured age pool.
proc.stdin.write(json.dumps({'text':'Proposed rider profile','font':'ChalkboardSE-Regular','size':7.8})+'\n');proc.stdin.flush()
profile_width=json.loads(proc.stdout.readline())['width']
text('Proposed rider profile',756-profile_width/2,356,7.8,width=96)
path('M630 367Q630 364 633 364Q636 364 636 367Q636 370 633 373Q630 370 630 367Z',GOLD,width=.55)
circle(633,367,.8,CREAM,.3)
text('Within the service area',640,372,7.2,width=89)
parts.append('<g transform="translate(12 8)">')
# A recognisable person holding a separate phone: head, hair, neck and bent arm.
path('M740 359Q740 355 744 354.5Q748 355 748 359V361Q747 365 744 365Q741 364 740 361Z',CREAM,width=.65)
path('M740 359Q738.8 355.5 742 354Q747.5 352.5 748 358L746 357L742 358Z',NAVY,width=.5)
path('M742 364V367H746V364',CREAM,width=.5)
path('M734 377L736 369Q737 366 741 366Q744 369 747 366Q751 367 752 370L754 377Z',CYAN,width=.7)
path('M739 370L742 375Q743 376 746 375L751 372',CREAM,width=.65)
path('M749 367Q749 366 750 366H754Q755 366 755 367V374H749Z',CYAN,width=.65)
path('M750 368H754V372H750Z',CREAM,width=.45)
circle(742.5,360.5,.35,NAVY,.15);circle(745.5,360.5,.35,NAVY,.15)
path('M743 362.5Q744 363.5 745 362.5',width=.35)
parts.append('</g>')
# Thought clouds share a short dotted path from the rider's head.
def thought_cloud(y):
    path(f'M782 {y+1}Q780 {y-1} 786 {y}Q790 {y-1} 794 {y}H877Q882 {y-1} 885 {y+1}Q891 {y} 890 {y+4}Q893 {y+6} 887 {y+8}H792Q787 {y+9} 784 {y+8}Q778 {y+9} 780 {y+5}Q776 {y+3} 782 {y+1}Z',CREAM,colour=NAVY,width=.45)
thought_cloud(358);thought_cloud(368.5);thought_cloud(379)
circle(766,367,.7,CREAM,.35);circle(769,367.5,1,CREAM,.35)
for bx,by,br in [(771.5,364,.8),(775.5,362.5,1.1),(772,371,.8),(776,372.5,1.1),(771.5,377,.8),(775.5,381,1.1)]:circle(bx,by,br,CREAM,.35)
# Preserve the recognisable icons, offset to their cloud rows.
parts.append('<g transform="translate(18 4.2)">')
path('M764.5 354L769.5 354L773 358L769 361.5L764.5 357Z',GOLD,width=.65)
circle(766.5,355.6,.65,CREAM,.25)
parts.append('</g>')
text('Price-conscious',797,364.5,7.2,width=91)
parts.append('<g transform="translate(171.2 77.6) scale(.8)">')
path('M764.5 364.5Q764.5 363.5 765.5 363.5H772Q773 363.5 773 364.5V372.5Q773 373.5 772 373.5H765.5Q764.5 373.5 764.5 372.5Z',CREAM,width=.65)
# A curved route runs from the start circle to a pointed location pin; no tick glyph.
path('M767 371Q770 371 768 369Q766.5 367.5 770.5 367.5',colour=CYAN,width=.65)
circle(766.5,371,.8,CREAM,.4)
path('M769 365.5Q769 364 770.5 364Q772 364 772 365.5Q772 366.5 770.5 368Q769 366.5 769 365.5Z',GOLD,width=.4)
parts.append('</g>')
text('Values trip control',797,375,7.2,width=91)
parts.append('<g transform="translate(209.5 98.2) scale(.75)">')
path('M764 379Q764 374.5 768.5 374.5Q773 374.5 773 379',width=.7)
path('M763.5 378H766V382H763.5Z M771 378H773.5V382H771Z',CYAN,width=.55)
path('M772.5 382Q772.5 384 769.5 384',width=.6)
path('M768 383.3H770V384.5H768Z',GOLD,width=.45)
parts.append('</g>')
text('Expects fair treatment',797,385.5,7.2,width=91)
text('Recurring trips → repeat rides',630,385,6.5,width=100)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-02-v03-candidate" clip-path="url(#cell-02-clip)">'+'\n'.join(parts)+'</g>'
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
checks={'status':'Fitting authorised; artwork/reduced copy pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'bars':bars,'scale':{'minimum':0,'maximum':300000,'height':33},'denominator':670389,'selected_share_actual':269277/670389*100,'selected_share_rounded':'40.2%','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','bars']},ensure_ascii=False,indent=2))
