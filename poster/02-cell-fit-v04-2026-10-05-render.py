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
PREFIX = '02-cell-fit-v04-2026-10-05'
BASE = HERE / '01-cell-fit-v07-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
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
    records.append({'text': value, 'font': font, 'resolved_font_names': data['resolved_font_names'], 'size_px': size, 'size_pt_a0': round(size*1189/1672*72/25.4, 2), 'bbox': [x+a,y-d,x+c,y-b], 'advance_width': data['width'], 'maximum_width': width})
    parts.append(f'<g aria-label="{escape(value, quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{NAVY}"/></g>')
    return data['width']

def path(d, fill='none', colour=NAVY, width=.8):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')



# Keep the chart small and allocate the right-hand space to audience conditions.
w=text('2. Target Market',629,250,10.5,True,width=270)
path(f'M629 255Q{629+w/2} 256 {629+w} 255',colour=GOLD,width=1.3)
text('Copenhagen residents aged 25–44',629,267,8.2,width=269)
# Date and adult chart scope sit together with the all-age percentage denominator below the bars.
path('M640 281V309H787',width=.65)
text('0',631,311,6.2,width=8)
# All four heights use one exact population scale; age selection does not distort bars.
bars=[]
for i,(age,count) in enumerate([('18–24',72396),('25–44',269277),('45–64',143668),('65+',74728)]):
    cx=658+i*36;top=309-count/300000*30
    fill=CYAN if age=='25–44' else '#dfeceb'
    path(f'M{cx-12} 309V{top}H{cx+12}V309Z',fill,width=.65)
    value=f'{count:,}'
    # Centre the glyph advance above each column.
    proc.stdin.write(json.dumps({'text':value,'font':'ChalkboardSE-Regular','size':9 if age=='25–44' else 6.5})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(value,cx-measured/2,top-3,9 if age=='25–44' else 6.5,width=34)
    proc.stdin.write(json.dumps({'text':age,'font':'ChalkboardSE-Regular','size':9 if age=='25–44' else 7.1})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    text(age,cx-measured/2,320,9 if age=='25–44' else 7.1,width=34)
    if age=='25–44':
        text('40.2%',cx-11,296,7.6,width=23)
        text('of city',cx-9,306,6.2,width=22)
    bars.append({'age':age,'count':count,'top':top,'baseline':309,'height':309-top})
# A single arrow selects the intersection of the three audience conditions.
path('M706 289L714 282H780Q783 282 783 286V298H788 M785 296L788 298L785 300',colour=CYAN,width=1)
path('M795 275Q791 275 791 279V291Q791 295 787.5 298Q791 301 791 305V323Q791 327 795 327',colour=CYAN,width=1)
parts.append('<g transform="translate(0 -6)">')
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
parts.append('</g>')
for record in records[-3:]:
    record['bbox'][1]-=6;record['bbox'][3]-=6
text('Copenhagen · 1 Jul 2026 · 18+',630,328,6.3,width=158)
text('City population (all ages): 670,389',630,336,6.3,width=269)
path('M630 342H893',colour=CYAN,width=.65)
# Proposed profile remains distinct from the measured age pool.
proc.stdin.write(json.dumps({'text':'Proposed rider profile','font':'ChalkboardSE-Regular','size':7.8})+'\n');proc.stdin.flush()
profile_width=json.loads(proc.stdout.readline())['width']
text('Proposed rider profile',751-profile_width/2,351,7.8,width=96)
path('M630 367Q630 364 633 364Q636 364 636 367Q636 370 633 373Q630 370 630 367Z',GOLD,width=.55)
circle(633,367,.8,CREAM,.3)
text('Within the service area',640,372,7.2,width=89)
parts.append('<g transform="translate(7 4)">')
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
thought_cloud(355);thought_cloud(365);thought_cloud(375)
circle(766,367,.7,CREAM,.35);circle(769,367.5,1,CREAM,.35)
for bx,by,br in [(771.5,364,.8),(775.5,362.5,1.1),(772,371,.8),(776,372.5,1.1),(771.5,377,.8),(775.5,381,1.1)]:circle(bx,by,br,CREAM,.35)
# Preserve the recognisable icons, offset to their cloud rows.
parts.append('<g transform="translate(18 1.2)">')
path('M764.5 354L769.5 354L773 358L769 361.5L764.5 357Z',GOLD,width=.65)
circle(766.5,355.6,.65,CREAM,.25)
parts.append('</g>')
text('Price-conscious',797,361.5,7.2,width=91)
parts.append('<g transform="translate(171.2 74.1) scale(.8)">')
path('M764.5 364.5Q764.5 363.5 765.5 363.5H772Q773 363.5 773 364.5V372.5Q773 373.5 772 373.5H765.5Q764.5 373.5 764.5 372.5Z',CREAM,width=.65)
# A curved route runs from the start circle to a pointed location pin; no tick glyph.
path('M767 371Q770 371 768 369Q766.5 367.5 770.5 367.5',colour=CYAN,width=.65)
circle(766.5,371,.8,CREAM,.4)
path('M769 365.5Q769 364 770.5 364Q772 364 772 365.5Q772 366.5 770.5 368Q769 366.5 769 365.5Z',GOLD,width=.4)
parts.append('</g>')
text('Values trip control',797,371.5,7.2,width=91)
parts.append('<g transform="translate(209.5 94.2) scale(.75)">')
path('M764 379Q764 374.5 768.5 374.5Q773 374.5 773 379',width=.7)
path('M763.5 378H766V382H763.5Z M771 378H773.5V382H771Z',CYAN,width=.55)
path('M772.5 382Q772.5 384 769.5 384',width=.6)
path('M768 383.3H770V384.5H768Z',GOLD,width=.45)
parts.append('</g>')
text('Expects fair treatment',797,381.5,7.2,width=91)
text('Recurring trips → repeat rides',630,385,6.5,width=100)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-02-v04-candidate" clip-path="url(#cell-02-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-02-v03-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
(HERE/f'{PREFIX}-panel.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1008" viewBox="607 226 303 170"><defs><clipPath id="cell-02-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>')
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1008" viewBox="607 344.817073 303 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1800),('panel',1800)]:
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
checks={'status':'Section 2 v04 reconciliation candidate; exact accepted v03 wording preserved, pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'bars':bars,'scale':{'minimum':0,'maximum':300000,'height':30},'denominator':670389,'selected_share_actual':269277/670389*100,'selected_share_rounded':'40.2%','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','bars']},ensure_ascii=False,indent=2))

pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks['pdf_measured_mm']=[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]]
checks['heading_size_pt_a0']=records[0]['size_pt_a0']
checks['width_violations']=[r for r in records if r['maximum_width'] and r['advance_width']>r['maximum_width']+1e-6]
checks['ordinary_lettering_below_12_5_pt']=[r for r in records[1:] if r['size_pt_a0']<12.5]
checks['approved_copy_bytes_preserved']=(HERE/f'{PREFIX}-copy.md').read_bytes()==(HERE/'02-cell-fit-v03-2026-10-05-copy.md').read_bytes()
expected=[x for x in (HERE/f'{PREFIX}-copy.md').read_text().splitlines() if x and not x.startswith('<!--')]
expected[0]=expected[0].removeprefix('## ')
from collections import Counter
tokens=lambda value: Counter(re.findall(r'\w+|→|[%+]',value))
checks['displayed_token_multiset_preserved']=tokens(' '.join(expected))==tokens(' '.join(r['text'] for r in records if r['text']!='0'))
checks['bar_height_scale_verified']=all(abs(b['height']-b['count']/300000*30)<1e-8 for b in bars)
checks['pdf_page_count']=int(re.search(r'Pages:\s*(\d+)',pdf_info).group(1))
checks['replacement_layer_id']='section-02-v04-candidate'
checks['old_layer_occurrences_after_replacement']=assembled.count('id="section-02-v03-candidate"')
checks['new_layer_occurrences']=assembled.count('id="section-02-v04-candidate"')
checks['section_2_has_no_logos_or_raster_images']='<image' not in layer
checks['proposed_profile_title_centre_native']=751
checks['person_head_centre_native']=744+7
checks['thought_cloud_conservative_bottom_clearance_native']=390-(375+9+.225)
copy_report=HERE/'02-cell-fit-v03-2026-10-05-copy-check.json'
(HERE/f'{PREFIX}-copy-check.json').write_bytes(copy_report.read_bytes())
checks['scoped_copycheck_reused']={'from':copy_report.name,'sha256':hashlib.sha256(copy_report.read_bytes()).hexdigest(),'reason':'Exact v03 copy bytes retained; only positioning/style changed','base_hard_stops':0,'whole_poster_markers_outside_fragment':2}
checks['selection_logic']='AND: three simultaneous conditions grouped by brace and reached by an arrow from 25–44; service-area restriction retained.'
checks['palette']={'navy':NAVY,'cyan':CYAN,'gold':GOLD,'cream':CREAM,'comparison_bar':'#dfeceb'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert not checks['width_violations'] and not checks['ordinary_lettering_below_12_5_pt']
assert checks['approved_copy_bytes_preserved'] and checks['displayed_token_multiset_preserved']
assert checks['bar_height_scale_verified']
assert checks['pdf_page_count']==1
assert checks['old_layer_occurrences_after_replacement']==0 and checks['new_layer_occurrences']==1
assert 21<=checks['heading_size_pt_a0']<=21.2
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','bars']},ensure_ascii=False,indent=2))
