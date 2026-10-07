"""Section 5 trial reflow; preserve the A0 base byte-for-byte before insertion."""
from pathlib import Path
from html import escape
import json
import subprocess
import hashlib
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PREFIX = '05-cell-fit-v01-2026-10-04'
INK, CYAN, GOLD = '#173a47', '#28bdbf', '#e3bb42'
BASE = HERE / 'poster-a0-layout-v02-2026-10-04.svg'
CELL = 'M309 400 H587 Q610 400 611 423 V575 Q611 598 587 598 H374 Q338 598 310 578 Q260 541 260 499 Q260 448 285 419 Q296 400 309 400 Z'
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '05-v09-glyphs-2026-10-04.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
parts, records = [], []

def glyph(value, size, heading=False):
    proc.stdin.write(json.dumps({'text': value, 'font': 'MarkerFelt-Wide' if heading else 'ChalkboardSE', 'size': size}, ensure_ascii=False)+'\n')
    proc.stdin.flush()
    result = json.loads(proc.stdout.readline())
    if 'error' in result:
        raise RuntimeError(result['error'])
    return result

def text(value, x, y, size=6.2, heading=False, width=None):
    data = glyph(value, size, heading)
    if width and data['width'] > width:
        raise ValueError(f'Text overflows {width}: {value} ({data["width"]:.2f})')
    a,b,c,d = data['bounds']
    records.append({'text':value, 'size_px':size, 'size_pt_a0':round(size*1189/1672*72/25.4,2), 'bbox':[x+a,y-d,x+c,y-b], 'advance_width':data['width']})
    parts.append(f'<g aria-label="{escape(value,quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{INK}"/></g>')

def lines(values, x, y, size=6.2, step=7.7, heading=False, width=None):
    for i,value in enumerate(values):
        text(value,x,y+i*step,size,heading,width)

def stroke(d, colour=CYAN, width=1):
    parts.append(f'<path d="{d}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

def arrow(x1,y,x2, colour=CYAN):
    stroke(f'M{x1} {y} L{x2} {y} M{x2-3} {y-2} L{x2} {y} L{x2-3} {y+2}',colour,.9)

def icon(kind,x,y):
    parts.append(f'<g transform="translate({x} {y})">')
    if kind == 'car':
        stroke('M0 5 L2 1 Q5 -1 9 1 L12 5 L11 8 L1 8Z',CYAN,.8)
        parts.append(f'<circle cx="3" cy="8" r="1.2" fill="{INK}"/><circle cx="9" cy="8" r="1.2" fill="{INK}"/>')
    elif kind == 'tag':
        stroke('M0 1 L8 1 L12 5 L8 9 L0 9Z',INK,.7)
        parts.append(f'<circle cx="3" cy="4" r="1" fill="{GOLD}"/>')
    elif kind == 'phone':
        stroke('M3 0 L8 0 Q10 0 10 2 L10 10 Q10 12 8 12 L3 12 Q1 12 1 10 L1 2 Q1 0 3 0Z M4 10 L7 10',INK,.7)
        stroke('M3 3 L8 3 M3 5 L8 5',CYAN,.55)
    elif kind == 'browser':
        stroke('M0 1 L12 1 L12 11 L0 11Z M0 4 L12 4 M3 7 L9 7',INK,.7)
        parts.append(f'<circle cx="2" cy="2.5" r=".5" fill="{GOLD}"/>')
    elif kind == 'speaker':
        stroke('M0 3 L9 0 L9 7 L0 5Z M2 5 L3 9 L5 9 L4 6 M11 1 L13 0 M11 4 L14 4 M11 7 L13 8',CYAN,.7)
    parts.append('</g>')

# Mirror is at x232–345, y377–448. The heading and scope start to its right.
text('5. Digital Marketing',350,423,13,True,width=248)
stroke('M350 427 Q475 429 596 427',GOLD,1.7)
text('Copenhagen · ages 25–44 · repeat self-paying taxi riders',350,437,6.2,width=250)

# Three top blocks: brief labels rather than miniature paragraphs.
text('CUSTOMER INSIGHT',282,451,7.7,True,width=103)
text('Denmark · taxi apps · n=1,005',282,461,5.7,width=103)
text('40–50%',282,478,12,True)
text('one installed app',330,478,5.7,width=55)
stroke('M282 483 L381 483', '#cbdedb',.6)
parts.append(f'<path d="M282 483 L322 483" stroke="{CYAN}" stroke-width="2.5"/>')
parts.append(f'<path d="M322 483 L332 483" stroke="{CYAN}" stroke-width="2.5" stroke-dasharray="1 1" opacity=".6"/>')
lines(['Capital Region · last-trip app','choice · n=79'],282,494,5.7,7,width=105)
text('57% lower price · 22% usual app',282,511,6.1,width=105)
lines(['Multi-select · separate samples ·','not 25–44-specific.'],282,519,5.5,7,width=106)

stroke('M389 450 Q387 487 389 523','#b2cecd',.6)
text('MARKETING MIX · 4Ps',395,451,7.6,True,width=94)
icon('car',395,457)
text('PRODUCT*',411,464,6.9,True,width=77)
text('Electric ride + controlled service',395,473,5.5,width=95)
icon('tag',395,478)
text('PRICE* · clear fare + trial',411,485,5.7,width=80)
text('PLACE · Copenhagen page',395,497,6.1,width=95)
text('→ Green SM app',395,505,6.2,width=95)
text('PROMOTION · search / social',395,516,5.7,width=95)
text('/ reminders',395,524,6.2,width=95)
text('*Proposed service / trial',395,532,5.5,width=95)

stroke('M491 450 Q493 504 491 526','#b2cecd',.6)
text('VOUCHER + PACKAGE',499,451,7.7,True,width=102)
text('Vietnam mechanics → CPH pilot',499,461,5.7,width=102)
text('FIRST PAID RIDE',499,471,6.3,True,width=102)
text('10% vs 20% OFF',499,484,9.5,True,width=102)
text('Max DKK30 · one per rider',499,493,6.1,width=101)
text('400-rider cap · DKK12,000',499,501,6.1,width=101)
text('reserve ceiling',499,509,5.7,width=101)
text('30-day paid package*',499,520,6.6,True,width=101)
text('Track redemption + paid repeats',499,528,5.5,width=101)
text('*Proposed',559,532,5.3,width=41)

# Actual connected nodes carry the channel route, followed by a return loop.
text('OMNI CHANNEL',302,534,7,True,width=106)
lines(['Paid search: “electric taxi Copenhagen”',
       'SEO: fare / area / booking FAQs',
       'Social: short electric-ride / booking demos'],
      302,542,5.2,6.2,width=109)
# The source nodes converge into the page, app and ride/help nodes.
stroke('M410 539 L414 539 L414 551 L410 551 M414 545 L419 545',CYAN,.8)
for x,w,label,kind in [(422,47,'CPH PAGE','browser'),(483,45,'APP','phone'),(543,57,'RIDE + HELP','car')]:
    parts.append(f'<rect x="{x}" y="534" width="{w}" height="16" rx="3" fill="#eefafa" stroke="{CYAN}" stroke-width=".8"/>')
    icon(kind,x+(1 if kind == "browser" else 3),537)
    text(label,x+15,544,5.2,True,width=w-17)
arrow(470,543,481)
arrow(530,543,541)
text('Consistent fares / offers / help',423,557,5.7,width=179)

# CDP, analytics and proposed AI each retain a distinct task.
text('CDP*: trip / app / consent',323,565,5.5,width=87)
text('Big Data*: repeat patterns at scale',410,565,5.5,width=100)
text('Marketing AI*: reminder timing/message',511,565,5.1,width=92)
text('Trip history → likely need → opt-in reminder → paid repeat',337,573,5.5,width=183)
text('consent / privacy / access',520,573,5.1,width=83)
stroke('M512 575 Q505 577 490 577 L349 577 Q343 577 343 574',CYAN,.65)
text('*Proposed after data/system checks · human review',345,581,5.3,width=254)

# The two-row timeline sits clear of the inward curve.
text('M1–2 verify service/data → M3–6 test content/offers · M4/M6 gates',376,587.5,5.5,width=225)
text('M7–12 refine · scale after gates',376,594.5,5.5,width=225)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode:
    raise RuntimeError(proc.stderr.read())

layer = '<g id="section-05-candidate" clip-path="url(#cell-05-clip)">'+'\n'.join(parts)+'</g>'
base = BASE.read_text()
assembled = base.replace('</g></svg>',layer+'</g></svg>')
assert assembled.count('section-05-candidate') == 1
assert assembled.replace(layer, '') == base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
layout = f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="250 395 365 210"><defs><clipPath id="cell-05-clip"><path d="{CELL}"/></clipPath></defs>{layer}</svg>'
(HERE/f'{PREFIX}-layout.svg').write_text(layout)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1672','-o',str(HERE/f'{PREFIX}-poster.png'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
# Crop actual A0 assembly rather than a re-created cell image.
tree = ET.fromstring(assembled)
tree.set('viewBox','250 515.817073 365 210')
tree.set('width','1600'); tree.set('height','920.547945')
crop = HERE/f'{PREFIX}-close-up.svg'
ET.ElementTree(tree).write(crop,encoding='unicode')
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1600','-o',str(HERE/f'{PREFIX}-close-up.png'),str(crop)],check=True)
manifest={'status':'HUMAN-REVIEW candidate; no copy or image acceptance','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'cell_path':CELL,'background_source_prefix_unchanged':assembled.split(layer)[0]==base.split('</g></svg>')[0],'visible_text':records,'min_pt':min(r['size_pt_a0'] for r in records)}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Rendered {PREFIX}; {len(records)} controlled strings; minimum {manifest["min_pt"]} pt')
