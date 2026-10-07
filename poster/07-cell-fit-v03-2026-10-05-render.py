"""Fit the approved budget content into native cell 07, preserving Sections 5–6."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '07-cell-fit-v03-2026-10-05'
BASE = HERE / '06-cell-fit-v02-2026-10-04-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
CELL = 'M875 400 H1154 Q1177 400 1177 423 V575 Q1177 598 1154 598 H875 Q852 598 852 575 V423 Q852 400 875 400 Z'
parts, records = [], []
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '07-cell-fit-v02-2026-10-04-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

title_width = text('7. Budget & Resources',866,420,12.2,True,width=130)
path(f'M866 424Q{866+title_width/2} 426 {866+title_width} 424',colour=GOLD,width=1.6)
text('Proposed DKK600,000',1007,420,10.8,True,width=156)
text('12 months · excluding VAT',1018,435,7.2,width=145)
text('Local delivery first · Search/social drive trial',866,437,7.1,width=175)
allocations = [
    ('Team',276000,46,CYAN), ('Search',108000,18,GOLD),
    ('Social',90000,15,CYAN), ('Screens',43195,7.2,GOLD),
    ('Tools',30000,5,CYAN), ('Vouchers',12000,2,GOLD),
    ('Contingency',40805,6.8,CYAN),
]
for i,(label,amount,share,colour) in enumerate(allocations):
    y=451+i*14
    text(label,866,y,8.3,width=56)
    # All seven amount bars retain their common DKK0–300,000 scale.
    path(f'M925 {y-7.5}H990V{y+1.5}H925Z',CREAM,width=.65)
    length=65*amount/300000
    path(f'M925 {y-7.5}H{925+length}V{y+1.5}H925Z',colour,width=.65)
    text(f'{amount:,} / {share:g}%',996,y,8.1,width=53)
    if label=='Vouchers':
        # Unbordered rider-cap lettering sits in the unused part of the bar.
        text('400 riders',941,y-.1,7.1,width=43)
text('DKK / % · bars: 0–300,000',866,547,7.1,width=184)
path('M1052 444V543',colour=CYAN,width=.65)
text('460h × DKK600/h*',1059,452,7.7,width=104)
roles=[('Checks',60),('Creative/localisation',120),('Campaigns',160),('CRM/help',120)]
for i,(label,hours) in enumerate(roles):
    y=468+i*16
    parts.append(f'<g transform="translate(1059 {y-6})">')
    if i==0:
        circle(3,2,3,CYAN,.65); path('M5 4L8 7',width=1.1)
    elif i==1:
        path('M0 6L5 0L8 3L3 9L0 9Z',GOLD,width=.65)
    elif i==2:
        path('M0 3L7 0V8L0 5Z',CYAN,width=.65); path('M2 6L3 9H5L4 5',GOLD,width=.5)
    else:
        path('M0 0H8V6H4L1 9V6H0Z',GOLD,width=.65)
    parts.append('</g>')
    text(f'{label} {hours}h',1071,y,7.5,width=92)
text('*Planning allowance',1059,528,6.5,width=104)
text('Outside budget: cars, drivers,',1059,540,6.6,width=104)
text('charging / frontline support',1059,549,6.6,width=104)
path('M866 555Q1014 553.5 1163 555',colour=CYAN,width=.8)
text('Budget reviews · cumulative commitments',866,565,7.1,width=300)
for x,w,fill in [(866,95,'#fff1a7'),(969,95,'#d9f4f2'),(1072,91,CREAM)]:
    path(f'M{x} 570H{x+w}V592H{x}Z',fill,width=.65)
text('M4 review',872,579,8.1,True,width=83)
text('DKK177,000',872,589,8.4,width=83)
text('M6 review',975,579,8.1,True,width=83)
text('DKK265,000',975,589,8.4,width=83)
text('Held at M6',1078,579,8.1,True,width=79)
text('DKK335,000',1078,589,8.4,width=79)
path('M962 581H967 M965 579L967 581L965 583',colour=CYAN,width=.8)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode: raise RuntimeError(proc.stderr.read())
layer='<g id="section-07-v03-candidate" clip-path="url(#cell-07-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
assert base.endswith('</g></svg>')
assert 'id="cell-07-clip"' in base
assembled=base[:-len('</g></svg>')]+layer+'</g></svg>'
assert assembled.replace(layer,'')==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
transparent=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="975" viewBox="852 400 325 198"><defs><clipPath id="cell-07-clip"><path d="{CELL}"/></clipPath></defs>{layer}</svg>'
(HERE/f'{PREFIX}-layout.svg').write_text(transparent)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1122" viewBox="846 514.817073 337 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
(HERE/f'{PREFIX}-copy.md').write_text('## 7. Budget & Resources\n<!-- budget: 120 -->\n\n'+'\n\n'.join(r['text'] for r in records[1:])+'\n')
def inside_cell(x,y):
    if not(852<=x<=1177 and 400<=y<=598): return False
    inset=0
    if y<423: inset=23*(1-math.sqrt((y-400)/23))**2
    elif y>575: inset=23*(1-math.sqrt((598-y)/23))**2
    return 852+inset<=x<=1177-inset
for i,record in enumerate(records):
    a=record['bbox']
    assert all(inside_cell(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]),record
    for other in records[i+1:]:
        b=other['bbox']
        assert not(min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])),(record,other)
assert sum(r[1] for r in allocations)==600000
assert abs(sum(r[2] for r in allocations)-100)<.00001
assert sum(hours for _,hours in roles)==460
assert 460*600==276000 and 30*400==12000
assert 600000-265000==335000
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks={'status':'Candidate for student review; no acceptance claimed','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'cell_path':CELL,'a0_mm':[1189,841],'art_translation_y':120.817073,'visible_text':records,'word_bearing_tokens':sum(bool(re.search(r'\w',w)) for w in displayed.split()),'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'raster_images_added':0,'glyph_bbox_corners_inside_native_cell':True,'pairwise_text_overlap_count':0,'allocations_sum_dkk':sum(r[1] for r in allocations),'shares_sum_percent':sum(r[2] for r in allocations),'resource_hours':460,'voucher_reserve_ceiling_dkk':12000,'unreleased_dkk':335000,'forecast_and_payback_figures_displayed':False,'border_around_rider_cap':False,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'manual_visual_review':'Pending controller visual inspection on 5 October 2026; physical A0 proof remains untested'}
with tempfile.TemporaryDirectory(prefix='mark1286-section7-') as temporary:
    headings=Path(temporary)/'headings.txt'
    headings.write_text('7. Budget & Resources\n')
    gate=subprocess.run(['python3','-B',str(Path.home()/'.codex/skills/mba-presentation-style/scripts/presentcheck.py'),str(HERE/f'{PREFIX}-copy.md'),'--mode','poster','--headings',str(headings),'--registry',str(HERE.parent/'04_references/references.json'),'--sources',str(HERE.parent/'04_references'),'--concepts',str(HERE.parent/'03_course_materials/concept-register.md'),'--strict-scope','--json'],capture_output=True,text=True)
    report=json.loads(gate.stdout)
    (HERE/f'{PREFIX}-copy-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert gate.returncode==2 and report['hard_stops']==2 and all(v==0 for v in report['effective_base_hard_by_category'].values()), report
    checks['fragment_presentcheck']={'exit':gate.returncode,'genre_words':report['genre']['total_words'],'detector_status':report['base']['anti_slop']['status'],'detector_score':report['base']['anti_slop']['score'],'effective_base_hard_stops':0,'out_of_scope_whole_poster_tables':report['genre']['errors']}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
