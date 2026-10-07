"""Reconcile Section 3 layout without changing accepted displayed copy."""
from pathlib import Path
from html import escape
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = '03-cell-fit-v07-2026-10-05'
BASE = HERE / '02-cell-fit-v04-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
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
    records.append({'text': value, 'font': font, 'resolved_font_names': data['resolved_font_names'], 'size_px': size, 'size_pt_a0': round(size*1189/1672*72/25.4, 2), 'bbox': [x+a,y-d,x+c,y-b], 'advance_width': data['width'], 'maximum_width': width})
    parts.append(f'<g aria-label="{escape(value, quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{NAVY}"/></g>')
    return data['width']

def path(d, fill='none', colour=NAVY, width=.8):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')



# No Green SM graphic logo in this cell: the gained area belongs to positioning.
w=text('3. Why Green SM?',933,250,10.5,True,width=184)
path(f'M933 254Q{933+w/2} 255 {933+w} 254',colour=GOLD,width=1.25)
text('Positioning Strategy',1130,250,7.2,width=113)
text('Electric rides. One managed experience.',933,273,11.3,True,width=310)
text('Cleaner · Quieter · More reliable',933,285,7.6,width=206)
text('Company promise',1058,285,6.8,width=100)
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
text('Bolt',1100,349,8.2,True,width=28)
path('M1132 346H1140L1137 343 M1140 346L1137 349',colour=CYAN,width=.85)
text('Viggo/Bolt · Taxa 4x27',1146,349,7.3,width=98)
# Summarise only Green SM's managed chain; the connector terminates at the proposal qualifier.
path('M936 351.8V354.8H1084V351.8',colour=CYAN,width=.75)
path('M936 354.8H927.5V380.5H931.5 M928.8 378.5L931.5 380.5L928.8 382.5',colour=CYAN,width=.8)
# Points of parity are explicit: app booking/electric access cannot by themselves establish a USP.
shared='Shared: App booking · Electric options'
proc.stdin.write(json.dumps({'text':shared,'font':'ChalkboardSE-Regular','size':7.7})+'\n');proc.stdin.flush()
shared_width=json.loads(proc.stdout.readline())['width']
text(shared,1088-shared_width/2,366,7.7,width=311)
# Proposed reason to choose, supported by the operating structure above.
text('Proposed edge:',933,384,7.1,width=63)
text('Direct control → one service standard',1000,384,8.2,True,width=245)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-03-v07-candidate" clip-path="url(#cell-03-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-03-v06-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
(HERE/f'{PREFIX}-panel.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="960" viewBox="909 226 354 170"><defs><clipPath id="cell-03-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>')
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2000" height="960" viewBox="909 344.817073 354 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2000),('panel',2000)]:
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
checks={'status':'Section 3 v07 reconciliation candidate under D-134; exact accepted v06 copy retained; student review pending','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logo':'Removed from Section 3 as requested; text brand name retained for comparison','manual_visual_review':'Producer inspected panel, fitted close-up and full A0: claim qualifier attached, controlled-chain bracket leads to Proposed edge, Shared remains explicit; controller/student review still pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks['pdf_measured_mm']=[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]]
checks['pdf_page_count']=int(re.search(r'Pages:\s*(\d+)',pdf_info).group(1))
checks['heading_size_pt_a0']=records[0]['size_pt_a0']
checks['width_violations']=[r for r in records if r['maximum_width'] and r['advance_width']>r['maximum_width']+1e-6]
checks['ordinary_lettering_below_12_5_pt']=[r for r in records[1:] if r['size_pt_a0']<12.5]
checks['approved_copy_bytes_preserved']=(HERE/f'{PREFIX}-copy.md').read_bytes()==(HERE/'03-cell-fit-v06-2026-10-05-copy.md').read_bytes()
expected=[x for x in (HERE/f'{PREFIX}-copy.md').read_text().splitlines() if x and not x.startswith('<!--')]
expected[0]=expected[0].removeprefix('## ')
actual=[r['text'] for r in records]
checks['exact_displayed_string_multiset_preserved']=Counter(expected)==Counter(actual)
tokens=lambda value: Counter(re.findall(r'\w+|→|[%+]',value))
checks['displayed_token_multiset_preserved']=tokens(' '.join(expected))==tokens(' '.join(actual))
checks['replacement_layer_id']='section-03-v07-candidate'
checks['old_layer_occurrences_after_replacement']=assembled.count('id="section-03-v06-candidate"')
checks['new_layer_occurrences']=assembled.count('id="section-03-v07-candidate"')
checks['native_cell_unchanged']=CELL in base and CELL in assembled
checks['section_3_has_no_logos_or_raster_images']='<image' not in layer
checks['company_promise_gap_native']=records[4]['bbox'][0]-records[3]['bbox'][2]
checks['shared_parity_centre_native']=1088
checks['shared_parity_baseline_native']=366
checks['operating_rows_alignment']='Both headers baseline 305; controlled-chain arrows and Uber operator arrow 327; Green SM chain labels and Bolt operator branch baseline 349.'
checks['chain_to_proposed_edge']='Bracket spans controlled chain only, at y354.8; left-margin connector ends beside Proposed edge at y380.5; Shared remains separate, centred across both columns at baseline 366.'
copy_report=HERE/'03-cell-fit-v06-2026-10-05-copy-check.json'
(HERE/f'{PREFIX}-copy-check.json').write_bytes(copy_report.read_bytes())
copy_result=json.loads(copy_report.read_text())
checks['scoped_copycheck_reused']={'from':copy_report.name,'sha256':hashlib.sha256(copy_report.read_bytes()).hexdigest(),'reason':'Exact accepted v06 copy bytes retained; layout/palette only','scoped_words':copy_result['genre']['total_words'],'base_hard_stops':copy_result['base']['hard_stops'],'detector_score':copy_result['base']['anti_slop']['score'],'whole_poster_markers_outside_fragment':len(copy_result['genre']['errors'])}
checks['palette']={'navy':NAVY,'cyan':CYAN,'gold':GOLD,'cream':CREAM}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert not checks['width_violations'] and not checks['ordinary_lettering_below_12_5_pt']
assert checks['approved_copy_bytes_preserved'] and checks['exact_displayed_string_multiset_preserved'] and checks['displayed_token_multiset_preserved']
assert checks['other_nine_cells_and_background_byte_for_byte_preserved']
assert checks['pdf_page_count']==1
assert checks['old_layer_occurrences_after_replacement']==0 and checks['new_layer_occurrences']==1
assert 20<=checks['heading_size_pt_a0']<=22
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
