"""Fit the selected four independent Ride Innovation pilot lanes into the lower-left car cell."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '09-cell-fit-v02-2026-10-05'
BASE = HERE / '08-cell-fit-v02-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
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
    path(f'M{x} {y+3}Q{x+8} {y-1} {x+16} {y+3}V{y+18}Q{x+8} {y+22} {x} {y+18}Z',CYAN,width=.8)
    path(f'M{x} {y+3}Q{x+8} {y+7} {x+16} {y+3}M{x} {y+10}Q{x+8} {y+14} {x+16} {y+10}',colour=CYAN,width=.7)

def ai(x,y):
    circle(x,y,10,GOLD,.8)
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
    path(f'M{x} {y+3}H{x+16}V{y+20}H{x}Z',GOLD,width=.8)
    path(f'M{x} {y+8}H{x+16}',colour=CYAN,width=.7)
    path(f'M{x+4} {y}V{y+5}M{x+12} {y}V{y+5}',colour=GOLD,width=1.2)
    path(f'M{x+4} {y+13}H{x+7}M{x+10} {y+13}H{x+13}',colour=NAVY,width=.6)

title_width=text('9. Ride Innovation',401,626,10.5,True)
path(f'M401 630Q{401+title_width/2} 631 {401+title_width} 630',colour=GOLD,width=1.5)
text('PROPOSED PILOTS · Local performance untested',561,626,7.5,width=280)
# Separate cards are alternative proposed pilots, not one processing pipeline.
for x,w in [(400,108),(515,107),(629,107),(743,104)]:
    path(f'M{x+3} 638H{x+w-3}Q{x+w} 638 {x+w} 641V719Q{x+w} 722 {x+w-3} 722H{x+3}Q{x} 722 {x} 719V641Q{x} 638 {x+3} 638Z',CREAM,colour=CYAN,width=.5)

text('AI targeting',407,651,8,True,width=94)
data(408,660);arrow(427,673,435,673);ai(448,672);arrow(461,673,471,673);phone(478,660)
text('Consented first-party data',407,695,6.5,width=94)
text('Big Data + AI',407,706,7.2,width=94)
text('Relevant reminders',407,717,7.2,width=94)

text('AI dispatch',522,651,8,True,width=93)
phone(523,660);arrow(540,673,549,673);ai(562,672);arrow(575,673,583,673);taxi(588,663)
text('Booking → AI match → taxi',522,693,6.5,width=94)
text('Test vs local baseline',522,701,6.5,width=94)
text('Match time · Fulfilment',522,709,6.5,width=94)
text('Cancellations · Fairness',522,717,6.5,width=94)

text('Connected care',636,651,8,True,width=93)
text('One trip ID',660,660,6.5,True,width=56)
path('M670 663Q651 663 649 668M681 663V671M691 663Q714 663 718 668',colour=CYAN,width=.8)
phone(638,666);taxi(666,669);support(710,668)
text('App · Driver/car · Support',636,695,6.5,width=93)
text('Ratings',636,703,6.5,width=93)
text('Test FAQ bot',636,710,6.5,width=93)
text('→ Human hand-off',636,717,6.5,width=93)

text('Personalised packages',750,651,7.7,True,width=90)
text('First: frequency + contribution',750,660,6.3,width=90)
taxi(753,666);calendar(815,666)
# A balance cue compares payment options; it does not imply automatic migration.
path('M797 670V684M788 674H806M791 674L787 680H795ZM803 674L799 680H807Z',colour=CYAN,width=.8)
text('Pay-per-trip vs',750,693,6.5,width=90)
text('Needs-matched prepaid/monthly',750,701,6.3,width=92)
text('Retention + margin',750,709,6.5,width=90)
text('Stop if either falls',750,717,6.5,width=90)

text('Feedback: Measure / refine',419,731,6.5,True,width=127)
text('Unpriced dispatch/chatbot/subscription: cost separately',554,731,6.3,width=288)
text('DKK600,000 excludes app/platform build + vehicle/driver/frontline operations',419,741,6.3,width=423)

proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-09-v02-candidate" clip-path="url(#cell-09-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
assert base.count('id="section-09-v01-candidate"')==1
start=base.index('<g id="section-09-v01-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
assert assembled.count('id="section-09-v02-candidate"')==1 and 'id="section-09-v01-candidate"' not in assembled
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="740" viewBox="372 602 494 152"><defs><clipPath id="cell-09-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>'
(HERE/f'{PREFIX}-panel.svg').write_text(standalone)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2400" height="740" viewBox="372 725.817073 494 152"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('panel',2400),('close-up',2400)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
copy=(HERE/f'{PREFIX}-copy.md').read_text()
copy_lines=[line.removeprefix('## ') for line in copy.splitlines() if line and not line.startswith('<!--')]
assert copy_lines==[r['text'] for r in records], {'draft':copy_lines,'surface':[r['text'] for r in records]}
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
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks={'status':'Section 9 v02 improvement candidate; copy and image pending student review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'cell_path':CELL,'a0_mm':[1189,841],'visible_text':records,'word_bearing_tokens':sum(bool(re.search(r'\w',w)) for w in displayed.split()),'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'heading_size_pt_a0':records[0]['size_pt_a0'],'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'raster_images_added':0,'cross_lane_pipeline_arrows':0,'local_mechanism_arrows_only':True,'feedback_explicitly_labelled':True,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'copy_matches_visible_surface':True,'manual_visual_review':'Pending'}
with tempfile.TemporaryDirectory(prefix='mark1286-section9-') as temporary:
    headings=Path(temporary)/'headings.txt';headings.write_text('9. Ride Innovation\n')
    gate=subprocess.run(['python3','-B','/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py',str(HERE/f'{PREFIX}-copy.md'),'--mode','poster','--headings',str(headings),'--registry',str(HERE.parent/'04_references/references.json'),'--sources',str(HERE.parent/'04_references'),'--concepts',str(HERE.parent/'03_course_materials/concept-list.txt'),'--strict-scope','--json'],capture_output=True,text=True)
    report=json.loads(gate.stdout)
    (HERE/f'{PREFIX}-copycheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    checks['fragment_presentcheck']={'exit':gate.returncode,'genre_words':report['genre']['total_words'],'detector_status':report['base']['anti_slop']['status'],'detector_score':report['base']['anti_slop']['score'],'effective_base_hard_by_category':report['effective_base_hard_by_category'],'out_of_scope_whole_poster_tables':report['genre']['errors']}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert checks['minimum_size_pt_a0']>=12.5, [(r['text'],r['size_pt_a0']) for r in records if r['size_pt_a0']<12.5]
assert gate.returncode==2 and report['hard_stops']==2 and all(v==0 for v in report['effective_base_hard_by_category'].values()), report
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
