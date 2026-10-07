"""Improve only Section 7 within the accepted Section 5 full A0 assembly."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '07-cell-fit-v04-2026-10-05'
BASE = HERE / '05-cell-fit-v05-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M875 400 H1154 Q1177 400 1177 423 V575 Q1177 598 1154 598 H875 Q852 598 852 575 V423 Q852 400 875 400 Z'
parts, records = [], []
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '07-cell-fit-v02-2026-10-04-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def text(value, x, y, size=6.6, heading=False, width=None):
    font = 'MarkerFelt-Wide' if heading else 'ChalkboardSE-Regular'
    def glyph(size):
        proc.stdin.write(json.dumps({'text': value, 'font': font, 'size': size}, ensure_ascii=False) + '\n')
        proc.stdin.flush()
        result = json.loads(proc.stdout.readline())
        assert 'error' not in result, result
        assert all(f in (font, 'Native vector arrow', 'Native vector maths') for f in result['resolved_font_names']), result
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


def role_icon(kind, x, y):
    parts.append(f'<g transform="translate({x} {y})">')
    if kind == 'checks':
        circle(4,4,4,CYAN,.65)
        path('M7 7L12 12',width=1.25)
        path('M2 4L3.5 5.5L6 2.5',width=.65)
    elif kind == 'creative':
        path('M0 9L8 1L11 4L3 12H0Z',GOLD,width=.65)
        path('M7 2L10 5',width=.65)
    elif kind == 'campaigns':
        path('M0 4L10 0V11L0 7Z',CYAN,width=.65)
        path('M3 8L4 13H7L5 8',GOLD,width=.65)
        path('M12 3L15 1 M12 6H16 M12 9L15 11',colour=CYAN,width=.8)
    else:
        path('M0 0H13V9H7L2 13V9H0Z',GOLD,width=.65)
        path('M3 3H10 M3 6H8',width=.65)
    parts.append('</g>')


title_width = text('7. Budget & Resources',866,420,10.5,True,width=138)
path(f'M866 424Q{866+title_width/2} 425 {866+title_width} 424',colour=GOLD,width=1.5)
text('Proposed DKK600,000',1007,420,10.5,True,width=156)
text('12 months · excluding VAT',1021,434,6.8,width=142)
text('Local delivery first · Search/social drive trial',866,436,6.8,width=179)
allocations = [('Team',276000,46,CYAN),('Search',108000,18,GOLD),('Social',90000,15,CYAN),('Screens',43195,7.2,GOLD),('Tools',30000,5,CYAN),('Vouchers',12000,2,GOLD),('Contingency',40805,6.8,CYAN)]
for i,(label,amount,share,colour) in enumerate(allocations):
    y=451+i*13
    text(label,866,y,8.3,width=56)
    path(f'M925 {y-7.5}H990V{y+1.5}H925Z',CREAM,width=.65)
    length=65*amount/300000
    path(f'M925 {y-7.5}H{925+length}V{y+1.5}H925Z',colour,width=.65)
    text(f'{amount:,} / {share:g}%',996,y,8.1,width=53)
    if label=='Vouchers':
        text('400 riders',941,y-.1,7.1,width=43)
text('DKK / % · bars: 0–300,000',866,543,7.1,width=184)
path('M1052 444V550',colour=CYAN,width=.65)
text('460h × DKK600/h*',1059,452,7.7,width=104)
# Each resource gets an icon, short role label and its own hours in a 2×2 grid.
role_icon('checks',1075,460)
role_icon('creative',1133,460)
text('Checks',1063,485,7.2,width=46)
text('60h',1074,500,7.8,width=32)
text('Creative/',1121,480,6.8,width=44)
text('localisation',1116,489,6.5,width=48)
text('120h',1128,500,7.8,width=36)
role_icon('campaigns',1075,503)
role_icon('crm',1133,503)
text('Campaigns',1059,522,6.8,width=50)
text('160h',1071,533,7.8,width=36)
text('CRM/help',1117,522,6.8,width=48)
text('120h',1128,533,7.8,width=36)
text('*Planning allowance',1059,543,6.5,width=104)
text('Outside budget: cars, drivers,',1059,553,6.4,width=104)
text('charging / frontline support',1059,561,6.4,width=104)
# Only M4→M6 shares a spend timeline. The unreleased balance stays separate.
path('M866 557H1045',colour=CYAN,width=.8)
text('Budget reviews · cumulative commitments',866,566,6.8,width=179)
text('M4 review',874,577,8.1,True,width=86)
text('DKK177,000',874,587,8.2,width=86)
path('M961 580H972 M968 577L972 580L968 583',colour=CYAN,width=1)
text('M6 review',984,577,8.1,True,width=83)
text('DKK265,000',984,587,8.2,width=83)
text('Held at M6',1085,576,8.1,True,width=78)
text('Remaining DKK335,000',1080,586,6.6,width=86)
text('M6: 265,000 + 335,000 = 600,000',980,594,6.2,width=185)
proc.stdin.close()
proc.wait(timeout=15)
assert proc.returncode == 0, proc.stderr.read()
layer='<g id="section-07-v04-candidate" clip-path="url(#cell-07-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-07-v03-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end()
        break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1122" viewBox="846 394 337 210"><defs><clipPath id="cell-07-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>'
(HERE/f'{PREFIX}-panel.svg').write_text(standalone)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1122" viewBox="846 514.817073 337 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('panel',1800),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
copy=(HERE/f'{PREFIX}-copy.md').read_text()
copy_lines=[line.removeprefix('## ') for line in copy.splitlines() if line and not line.startswith('<!--')]
assert copy_lines==[r['text'] for r in records], {'draft':copy_lines,'surface':[r['text'] for r in records]}
def inside_cell(x,y):
    if not(852<=x<=1177 and 400<=y<=598): return False
    inset=23*(1-math.sqrt((y-400)/23))**2 if y<423 else (23*(1-math.sqrt((598-y)/23))**2 if y>575 else 0)
    return 852+inset<=x<=1177-inset
for i,record in enumerate(records):
    a=record['bbox']
    assert all(inside_cell(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]), record
    for other in records[i+1:]:
        b=other['bbox']
        assert not(min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])), (record,other)
assert sum(r[1] for r in allocations)==600000 and abs(sum(r[2] for r in allocations)-100)<.00001
assert 60+120+160+120==460 and 460*600==276000 and 30*400==12000 and 265000+335000==600000
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks={'status':'Section 7 improvement candidate. No artwork acceptance inferred.','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'cell_path':CELL,'a0_mm':[1189,841],'art_translation_y':120.817073,'visible_text':records,'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'glyph_bbox_corners_inside_native_cell':True,'pairwise_text_overlap_count':0,'allocations_sum_dkk':600000,'shares_sum_percent':100,'resource_hours':460,'voucher_reserve_ceiling_dkk':12000,'m6_committed_dkk':265000,'m6_held_dkk':335000,'m4_m6_cumulative_not_additive':True,'raster_images_added':0,'border_around_rider_cap':False,'framed_budget_review_boxes':0,'copy_matches_visible_surface':True,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'manual_visual_review':'Pending standalone, fitted close-up and full A0 inspection. Physical print proof remains unverified.'}
checks['resolved_fonts']=sorted(set(f for r in records for f in r['resolved_font_names']))
checks['heading_size_pt_a0']=records[0]['size_pt_a0']
with tempfile.TemporaryDirectory(prefix='mark1286-section7-') as temporary:
    headings=Path(temporary)/'headings.txt'
    headings.write_text('7. Budget & Resources\n')
    gate=subprocess.run(['python3','-B','/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py',str(HERE/f'{PREFIX}-copy.md'),'--mode','poster','--headings',str(headings),'--registry',str(HERE.parent/'04_references/references.json'),'--sources',str(HERE.parent/'04_references'),'--concepts',str(HERE.parent/'03_course_materials/concept-list.txt'),'--strict-scope','--json'],capture_output=True,text=True)
    report=json.loads(gate.stdout)
    (HERE/f'{PREFIX}-copy-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert gate.returncode==2 and report['hard_stops']==2 and all(v==0 for v in report['effective_base_hard_by_category'].values()), report
    checks['fragment_presentcheck']={'exit':gate.returncode,'genre_words':report['genre']['total_words'],'detector_status':report['base']['anti_slop']['status'],'detector_score':report['base']['anti_slop']['score'],'effective_base_hard_stops':0,'out_of_scope_whole_poster_tables':report['genre']['errors']}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
