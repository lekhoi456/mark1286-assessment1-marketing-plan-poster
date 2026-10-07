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
PREFIX = '10-cell-fit-v02-2026-10-05'
BASE = HERE / '04-cell-fit-v03-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M890 608 H1240 Q1269 608 1258 636 L1224 725 Q1217 747 1193 747 H890 Q867 747 867 724 V631 Q867 608 890 608 Z'
parts, records, artwork = [], [], []
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
    artwork.append({'kind':'path','d':d,'stroke_width':width})
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.8):
    artwork.append({'kind':'circle','bbox':[x-r-width/2,y-r-width/2,x+r+width/2,y+r+width/2]})
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')



def arrow(x1,y1,x2,y2,colour=CYAN):
    path(f'M{x1} {y1}L{x2} {y2}',colour=colour,width=.8)
    a=math.atan2(y2-y1,x2-x1)
    path(f'M{x2-3*math.cos(a-.55)} {y2-3*math.sin(a-.55)}L{x2} {y2}L{x2-3*math.cos(a+.55)} {y2-3*math.sin(a+.55)}',colour=colour,width=.8)

def phone(x,y):
    path(f'M{x+2} {y}Q{x} {y} {x} {y+2}V{y+19}Q{x} {y+21} {x+2} {y+21}H{x+12}Q{x+14} {y+21} {x+14} {y+19}V{y+2}Q{x+14} {y} {x+12} {y}Z',CREAM,width=.8)
    path(f'M{x+3} {y+5}H{x+11}M{x+3} {y+8}H{x+9}',colour=CYAN,width=.7)
    path(f'M{x+5} {y+14}Q{x+5} {y+10} {x+7} {y+10}Q{x+10} {y+10} {x+10} {y+14}L{x+11} {y+16}H{x+4}Z',GOLD,colour=NAVY,width=.6)

def taxi(x,y):
    path(f'M{x} {y+9}L{x+5} {y+2}H{x+16}L{x+22} {y+9}L{x+24} {y+11}V{y+17}H{x}Z',CYAN,width=.8)
    path(f'M{x+5} {y+8}L{x+8} {y+4}H{x+15}L{x+19} {y+8}Z',CREAM,width=.55)
    circle(x+5,y+17,2.5,CREAM,.8);circle(x+19,y+17,2.5,CREAM,.8)

# The unchanged core mission and one shared proposal/untested band qualify all four goals.
w=text('10. Business Goals & Growth',883,628,10.5,True,width=227)
path(f'M883 632Q{883+w/2} 633 {883+w} 632',colour=GOLD,width=1.2)
text('Green · smart · sustainable mobility',883,641,6.6,width=125)
path('M1014 631H1206V644H1014Z',CREAM,colour=GOLD,width=.8)
text('Proposed 12-month plan',1021,640,6.6,width=80)
path('M1102 634V641',colour=GOLD,width=.8)
text('Local outcomes untested',1110,640,6.6,width=88)

# Keep the four-goal board; each broad action icon leads visibly to its business outcome.
path('M1062 648V721',colour=CYAN,width=.8)
path('M884 686H1235',colour=CYAN,width=.8)

taxi(886,658)
circle(897,648,4,CREAM,.8)
path('M890 660Q891 653 897 653Q904 653 904 660',CREAM,width=.8)
arrow(914,660,923,650)
text('Stable local operation',927,654,8.1,True,width=128)
text('Owned fleet + employed drivers',927,666,6.6,width=126)
text('Service + 90-day repeat → scale',927,678,6.6,width=126)

phone(1072,654)
circle(1091,658,4,CREAM,.8)
path('M1094 661L1098 665',width=.8)
path('M1090 669H1101V676H1090ZM1095 676V679M1092 679H1098',CREAM,width=.8)
arrow(1099,657,1109,650)
text('Become known locally',1115,654,8.1,True,width=119)
text('Search / social → paid trial',1115,665,6.6,width=118)
text('Screens after service +',1115,674,6.6,width=111)
text('90-day repeat checks',1115,683,6.6,width=109)

phone(884,692)
taxi(900,696)
path('M914 690L910 696H914L911 702',colour=GOLD,width=.8)
arrow(919,690,924,690)
text('Green & smart mobility',929,694,8.1,True,width=125)
text('App-booked electric rides',929,705,6.6,width=125)
text('Easy to understand + use',929,716,6.6,width=125)

# The full observation window belongs explicitly to sustainable growth.
circle(1087,706,9,CREAM,.8)
path('M1081 707Q1080 701 1086 700Q1091 700 1093 704M1090 701L1093 704L1094 700',colour=CYAN,width=.8)
path('M1093 707Q1093 713 1087 714Q1083 714 1081 710M1080 714L1081 710L1085 712',colour=CYAN,width=.8)
arrow(1098,699,1109,691)
text('Sustainable growth',1115,694,8.1,True,width=109)
text('Retention + contribution',1115,703,6.6,width=106)
text('Repeat before expansion',1115,711,6.6,width=101)
text('Repeat: full 90-day follow-up',1115,720,6.4,width=97)

# Shared review and investment limit remain separate from the four causal links.
path('M882 724H1223L1219 742H883Z',CREAM,colour=GOLD,width=.8)
text('M12 review:',889,731,6.6,True,width=43)
text('Consideration · paid trial · service · 90-day repeat · contribution',936,731,6.4,width=278)
text('Renew · Revise · Stop',889,740,7.2,True,width=105)
text('Entry investment · first-year break-even not required',1000,740,6.4,width=209)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-10-v02-candidate" clip-path="url(#cell-10-clip)">'+ '\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-10-v01-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
restored=assembled.replace(layer,old_layer,1)
assert restored==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
(HERE/f'{PREFIX}-panel.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="900" viewBox="860 603 408 153"><defs><clipPath id="cell-10-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>')
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2400" height="900" viewBox="860 721.817073 408 153"',assembled,count=1)
(HERE/f'{PREFIX}-closeup.svg').write_text(crop)
for suffix,width in [('poster',2400),('closeup',2400),('panel',2400)]:
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
# Art containment tests every path control point and extremal box, including stroke.
def art_box(item):
    if item['kind']=='circle':return item['bbox']
    tokens=re.findall(r'[MLHVQZ]|-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',item['d'],re.I)
    points=[]; x=y=0; i=0; command=None
    while i<len(tokens):
        if tokens[i].isalpha():command=tokens[i];i+=1
        if command=='Z':command=None;continue
        if command in ('M','L'):
            x,y=map(float,tokens[i:i+2]);i+=2;points.append((x,y))
        elif command=='H':x=float(tokens[i]);i+=1;points.append((x,y))
        elif command=='V':y=float(tokens[i]);i+=1;points.append((x,y))
        elif command=='Q':
            cx,cy,x,y=map(float,tokens[i:i+4]);i+=4;points.extend([(cx,cy),(x,y)])
        elif command is None:continue
        else:raise ValueError(command)
    pad=item['stroke_width']/2
    return [min(x for x,y in points)-pad,min(y for x,y in points)-pad,max(x for x,y in points)+pad,max(y for x,y in points)+pad]
art_outside=[]
for item in artwork:
    b=art_box(item)
    if not all(inside(x,y) for x in [b[0],b[2]] for y in [b[1],b[3]]):art_outside.append({'art':item,'bbox':b})
from collections import Counter
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
expected=[x.removeprefix('## ') for x in (HERE/f'{PREFIX}-copy.md').read_text().splitlines() if x and not x.startswith('<!--')]
previous=json.loads((HERE/'10-cell-fit-v01-2026-10-05-checks.json').read_text())['visible_text']
previous_strings=[r['text'] for r in previous]
actual=[r['text'] for r in records]
tokens=lambda value:Counter(re.findall(r'\w+|→|[%+]',value))
token_signature=lambda value:hashlib.sha256(json.dumps(sorted(tokens(value).items()),ensure_ascii=False).encode()).hexdigest()
copy_report=json.loads((HERE/f'{PREFIX}-copy-check.json').read_text())
checks={
 'status':'Section 10 v02 reconciliation candidate under D-134; student/controller review pending',
 'base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),
 'other_nine_cells_and_background_byte_for_byte_preserved':restored==base,
 'restored_base_sha256':hashlib.sha256(restored.encode()).hexdigest(),
 'replacement_layer_id':'section-10-v02-candidate',
 'old_layer_occurrences_after_replacement':assembled.count('id="section-10-v01-candidate"'),
 'new_layer_occurrences':assembled.count('id="section-10-v02-candidate"'),
 'native_cell_unchanged':CELL in base and CELL in assembled,'cell_path':CELL,
 'a0_mm':[1189,841],
 'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],
 'pdf_page_count':int(re.search(r'Pages:\s*(\d+)',pdf_info).group(1)),
 'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,
 'artwork_geometry_boxes_outside_native_cell':art_outside,'native_art_containment_pass':not art_outside,
 'width_violations':[r for r in records if r['maximum_width'] and r['advance_width']>r['maximum_width']+1e-6],
 'heading_size_pt_a0':records[0]['size_pt_a0'],
 'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records[1:]),
 'exact_displayed_copy_matches_markdown':Counter(expected)==Counter(actual),
 'exact_v01_displayed_strings_preserved':Counter(previous_strings)==Counter(actual),
 'v01_displayed_token_signature':token_signature(' '.join(previous_strings)),
 'v02_displayed_token_signature':token_signature(' '.join(actual)),
 'previous_copy_sha256':hashlib.sha256((HERE/'10-cell-fit-v01-2026-10-05-copy.md').read_bytes()).hexdigest(),
 'current_copy_sha256':hashlib.sha256((HERE/f'{PREFIX}-copy.md').read_bytes()).hexdigest(),
 'copy_change':'Remove redundant non-displayed Markdown title/plain duplicate heading; all visible strings remain exact',
 'qualifier_location':'Repeat: full 90-day follow-up belongs to the lower-right Sustainable growth tile, baseline 720; footer band starts at 724',
 'followup_to_footer_clearance_native':724-next(r['bbox'][3] for r in records if r['text']=='Repeat: full 90-day follow-up'),
 'footer_bottom_clearance_native':747-max(r['bbox'][3] for r in records[-4:]),
 'local_action_to_outcome_arrows':4,
 'proposal_qualification':'Both exact labels share one header support band; neither reads as a proved result',
 'logo':'No graphic logo or raster in Section 10','section_10_has_no_raster':'<image' not in layer,
 'palette':{'navy':NAVY,'cyan':CYAN,'gold':GOLD,'cream':CREAM},
 'fragment_presentcheck':{'exit':2,'genre_words':copy_report['genre']['total_words'],'detector_status':copy_report['base']['anti_slop']['status'],'detector_score':copy_report['base']['anti_slop']['score'],'effective_base_hard_by_category':copy_report['effective_base_hard_by_category'],'whole_poster_tables_outside_fragment':copy_report['genre']['errors']},
 'manual_visual_review':'Pending producer inspection'
}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not outside and not overlaps and not art_outside, {'text_outside':outside,'overlaps':overlaps,'art_outside':art_outside}
assert not checks['width_violations'] and checks['minimum_ordinary_lettering_pt_a0']>=12.5
assert checks['other_nine_cells_and_background_byte_for_byte_preserved'] and checks['restored_base_sha256']==checks['base_sha256']
assert checks['old_layer_occurrences_after_replacement']==0 and checks['new_layer_occurrences']==1
assert checks['exact_displayed_copy_matches_markdown'] and checks['exact_v01_displayed_strings_preserved']
assert checks['v01_displayed_token_signature']==checks['v02_displayed_token_signature']
assert checks['section_10_has_no_raster'] and checks['footer_bottom_clearance_native']>=4
assert 20<=checks['heading_size_pt_a0']<=22 and checks['pdf_page_count']==1
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
assert copy_report['hard_stops']==2 and all(v==0 for v in copy_report['effective_base_hard_by_category'].values())
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
