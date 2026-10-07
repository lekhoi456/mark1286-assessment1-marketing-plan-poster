"""Section 5 trial reflow; preserve the A0 base byte-for-byte before insertion."""
from pathlib import Path
from html import escape
import json
import subprocess
import hashlib
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PREFIX = '05-cell-fit-v02-2026-10-04'
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

import base64
atlas = HERE / '05-v09-illustration-atlas-2026-10-04.png'
data = base64.b64encode(atlas.read_bytes()).decode('ascii')
assets=[]
parts.append(f'<defs><image id="atlas-v02" x="0" y="0" width="1536" height="1024" href="data:image/png;base64,{data}"/></defs>')
def art(name,source,dest,mask):
    x,y,w,h=dest
    identifier=f'asset-{len(assets)}'
    sx,sy,sw,sh=source
    parts.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{sx} {sy} {sw} {sh}" preserveAspectRatio="{"none" if name == "First-ride voucher" else "xMidYMid meet"}" overflow="hidden" aria-label="{name}"><defs><clipPath id="{identifier}">{mask}</clipPath></defs><use href="#atlas-v02" clip-path="url(#{identifier})"/></svg>')
    assets.append({'name':name,'source':source,'destination':dest,'native_mask':mask})

text('5. Digital Marketing',350,423,14,True,width=248)
stroke('M350 427 Q475 429 596 427',GOLD,1.7)
# Two source-specific micro-charts, separated from the named segment elsewhere.
text('40–50%',350,442,10,True)
text('one app',402,442,7,width=65)
text('57% lower price · 22% usual app',480,442,6.5,True,width=122)
text('DK · n=1,005',350,451,5.7)
text('Capital · n=79 · multi-select',480,451,5.7,width=123)
stroke('M350 455 L454 455','#d8e7e2',3)
stroke('M350 455 L392 455',CYAN,3)
parts.append(f'<path d="M392 455 L402 455" stroke="{CYAN}" stroke-width="3" stroke-dasharray="1 1"/>')
stroke('M480 455 L599 455','#d8e7e2',3)
stroke('M480 455 L548 455',CYAN,3)
stroke('M480 459 L506 459',GOLD,2)
text('Separate samples · not 25–44-specific',350,465,5.7,width=248)

# Applied mix is an illustrated left rail, not a paragraph column.
text('Marketing Mix',283,454,6.6,True,width=66)
text('4Ps*',283,463,7,True,width=66)
icon('car',282,465)
text('Product',298,473,7,True)
text('Electric + service',281,484,6.6,width=66)
icon('tag',277,490)
text('Price',293,498,7,True)
text('Clear fare + trial',277,508,6.6,width=67)
icon('browser',281,514)
text('Place',297,522,7,True)
text('Page → app',281,532,6.6,width=66)
icon('speaker',291,537)
text('Promotion',307,546,7,True,width=49)
text('Search / social',296,556,6.6,width=64)
text('/ reminders',305,565,6.6,width=64)
text('*Proposed',308,573,5.7,width=43)

# Main narrative uses the accepted asset language at a much larger scale.
text('Omni Channel · Search / SEO / Social',350,475,7.1,True,width=246)
art('Copenhagen page', [42,92,495,475], [351,480,74,53], '<rect x="53" y="105" width="473" height="452" rx="30"/>')
art('Mapped booking app', [630,65,280,485], [431,477,45,57], '<rect x="646" y="78" width="247" height="454" rx="49"/>')
art('Electric ride, driver and human help', [919,95,617,440], [488,476,112,59], '<path d="M942 411 Q931 377 960 337 L1088 277 Q1123 248 1163 250 L1174 216 Q1183 208 1228 216 L1243 250 Q1307 248 1367 300 L1436 335 Q1491 348 1506 404 Q1526 448 1479 483 Q1452 522 1399 500 Q1363 491 1361 474 H1094 Q1050 525 1002 493 Q970 476 967 447 L942 439Z"/><path d="M1330 126 Q1453 118 1488 138 Q1504 146 1503 221 Q1500 258 1453 257 L1421 289 L1417 260 Q1311 267 1308 226 L1308 165 Q1308 127 1330 126Z"/>')
arrow(426,508,430)
arrow(479,508,486)
text('Copenhagen page',352,543,7,True,width=78)
text('Green SM app',433,543,6.5,True,width=54)
text('Ride + help',510,543,7.5,True,width=91)
text('Same fares / offers / help',377,551,6.6,width=225)

# Voucher + calendar images occupy the broad lower shoulder.
art('First-ride voucher', [24,643,550,289], [354,554,78,25], '<path d="M40 697 L67 672 L516 665 L539 690 L552 701 L550 742 Q512 783 550 819 L550 875 L524 908 L63 905 L45 880 L38 846 Q80 797 39 751Z"/>')
text('10% vs 20%',368,566,8.6,True,width=70)
text('First paid ride',364,575,6.3,True,width=78)
art('30-day paid package', [580,582,440,377], [433,551,30,27], '<path d="M618 636 L658 634 Q659 599 679 599 Q700 599 707 633 L822 633 Q828 599 849 599 Q871 599 876 635 L918 638 Q945 641 944 785 Q988 790 1000 840 Q1016 904 942 942 L651 946 Q624 946 624 923 L599 921 Q580 917 591 679 Q593 640 618 636Z"/>')
text('30-day paid*',467,577,6.3,True,width=76)
text('Max DKK30 · 400 cap · 1/rider',346,584,5.7,width=219)

# Data has explicit roles in a small connected footer, with proposal/opt-in gate.
text('CDP join → Big Data patterns → Marketing AI remind',467,560,5.7,True,width=136)
text('Opt-in · human review · proposed',467,568,5.7,width=136)
# Three coloured stages replace a prose timeline.
for x,w,month,activity,fill in [(375,70,'M1–2','Verify', '#e9f8f5'),(448,80,'M3–6','Test · M4/M6 gates','#fff4b9'),(531,70,'M7–12','Scale if gates','#e9f8f5')]:
    parts.append(f'<rect x="{x}" y="585" width="{w}" height="10" rx="2" fill="{fill}"/>')
    text(month,x+3,592,6.1,True)
    text(activity,x+26,592,5.7,width=w-27)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode:
    raise RuntimeError(proc.stderr.read())

layer = '<g id="section-05-v02-candidate" clip-path="url(#cell-05-clip)">'+'\n'.join(parts)+'</g>'
base = BASE.read_text()
assembled = base.replace('</g></svg>',layer+'</g></svg>')
assert assembled.count('section-05-v02-candidate') == 1
assert assembled.replace(layer, '') == base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
layout = f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="250 395 365 210"><defs><clipPath id="cell-05-clip"><path d="{CELL}"/></clipPath></defs>{layer}</svg>'
(HERE/f'{PREFIX}-layout.svg').write_text(layout)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1672','-o',str(HERE/f'{PREFIX}-poster.png'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
# Crop actual A0 assembly rather than a re-created cell image.
import re
cropped = re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"', 'width="1600" height="920.547945" viewBox="250 515.817073 365 210"', assembled, count=1)
crop = HERE/f'{PREFIX}-close-up.svg'
crop.write_text(cropped)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1600','-o',str(HERE/f'{PREFIX}-close-up.png'),str(crop)],check=True)
manifest={'status':'HUMAN-REVIEW candidate; no copy or image acceptance','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'cell_path':CELL,'background_source_prefix_unchanged':assembled.split(layer)[0]==base.split('</g></svg>')[0],'visible_text':records,'min_pt':min(r['size_pt_a0'] for r in records)}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Rendered {PREFIX}; {len(records)} controlled strings; minimum {manifest["min_pt"]} pt')
