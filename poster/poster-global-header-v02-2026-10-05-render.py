from pathlib import Path
import json,re,subprocess,html,hashlib,base64
P=Path.cwd()/'poster';base=P/'poster-brief-headings-v01-2026-10-05.svg'
stem='poster-global-header-v02-2026-10-05';s=base.read_text();original=s
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
records=[]
def measure(t,z,font='MarkerFelt-Wide'):
 proc.stdin.write(json.dumps({'text':t,'font':font,'size':z})+'\n');proc.stdin.flush();d=json.loads(proc.stdout.readline());assert 'error' not in d;return d

def glyph(t,x,y,z,font='MarkerFelt-Wide'):
 d=measure(t,z,font);a,b,c,e=d['bounds'];records.append({'text':t,'font':font,'bbox':[x+a,y-e,x+c,y-b],'width':d['width'],'a0_pt':round(z*1189/1672*72/25.4,2)})
 return f'<g aria-label="{html.escape(t,quote=True)}"><path d="{d["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="#173a47"/></g>'

parts=[];cx=836;size=50;cw=measure('Copenhagen',size)['width'];mw=measure('meet',size)['width']
flagw=54;logow=290;gaps=[20,22,23];total=flagw+cw+mw+logow+sum(gaps);left=cx-total/2;fx=left
parts.append(f'<g id="title-denmark-flag" aria-label="Denmark flag"><path d="M{fx} 90L{fx+flagw} 91L{fx+flagw-1} 127L{fx} 126Z" fill="#c8102e" stroke="#173a47" stroke-width="1.2" stroke-linejoin="round"/><path d="M{fx+18} 91L{fx+18} 126M{fx} 108L{fx+flagw-1} 108" fill="none" stroke="#ffffff" stroke-width="5.5"/></g>')
x=fx+flagw+gaps[0];parts.append(glyph('Copenhagen',x,125,size));mx=x+cw+gaps[1];parts.append(glyph('meet',mx,125,size));lx=mx+mw+gaps[2]
start=s.index('id="fit01-authentic-green-sm-logo"');start=s.rfind('<svg',0,start);end=s.index('</svg>',start)+6
logo=s[start:end];original_logo=logo;first_end=logo.index('>')+1;tag=logo[:first_end]
for k,v in [('id','header-authentic-green-sm-logo'),('x',str(lx)),('y','49'),('width',str(logow)),('height',str(logow*572/2125))]:tag=re.sub(r'\b'+k+r'="[^"]*"',k+'="'+v+'"',tag)
logo=tag+logo[first_end:];logo=logo.replace('id="green-sm-shared-hand-drawn-png"','id="header-green-sm-shared-hand-drawn-png"');parts.append(logo)
t='A 12-month market-entry plan for local electric taxi rides';w=measure(t,28,'ChalkboardSE-Regular')['width'];parts.append(glyph(t,cx-w/2,177,28,'ChalkboardSE-Regular'))
proc.stdin.close();proc.wait()
# University asset is generated from the student-supplied master logo and embedded unchanged.
asset=P/'assets/greenwich-hand-drawn-v01-2026-10-05.png';assert asset.exists(),asset
payload=base64.b64encode(asset.read_bytes()).decode()
parts.append(f'<image id="greenwich-hand-drawn-logo" aria-label="University of Greenwich hand-drawn logo" x="45" y="58" width="310" height="124" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{payload}"/>')
header='<g id="global-header-v02-candidate" aria-label="Denmark flag, Copenhagen meet Green SM; University of Greenwich">'+''.join(parts)+'</g>'
out=s[:-6]+header+'</svg>';oldtitle=re.search(r'<title>.*?</title>',out).group();olddesc=re.search(r'<desc>.*?</desc>',out).group()
newtitle='<title>Copenhagen meet Green SM — University of Greenwich marketing plan</title>'
newdesc='<desc>A0 landscape hand-drawn marketing-plan poster. Centred title starts with the Denmark flag and ends with the Green SM logo; exact subtitle is centred underneath. Hand-drawn University of Greenwich logo sits left. The previous local tagline is removed by the student. Ten marketing cells, car, background and upper-right identity cloud are unchanged. Revised header awaits review.</desc>'
out=out.replace(oldtitle,newtitle,1).replace(olddesc,newdesc,1)
restored=out.replace(header,'').replace(newtitle,oldtitle,1).replace(newdesc,olddesc,1);assert restored==original
assert left>370 and lx+logow<1280
assert abs((left+lx+logow)/2-cx)<.001
assert abs(records[-1]['bbox'][0]+records[-1]['width']/2-cx)<2
assert 'Clear terms. Local care.' not in out
for r in records:assert r['bbox'][0]>370 and r['bbox'][2]<1250 and r['bbox'][1]>35 and r['bbox'][3]<190
(P/(stem+'.svg')).write_text(out)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'.png')),str(P/(stem+'.svg'))],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(P/(stem+'.pdf')),str(P/(stem+'.svg'))],check=True)
close=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2400" height="390" viewBox="15 25 1290 195"><rect x="15" y="25" width="1290" height="195" fill="#def6f5"/>{header}</svg>'
(P/(stem+'-close-up.svg')).write_text(close)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'-close-up.png')),str(P/(stem+'-close-up.svg'))],check=True)
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'base_artwork_restoration_exact':restored==original,'header_text':records,'title_bounds':[left,lx+logow],'title_centre':cx,'subtitle_centre':cx,'greenwich_logo_box':[45,58,355,182],'greenwich_asset':str(asset.relative_to(P)),'greenwich_asset_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'green_sm_logo_payload_preserved':re.search(r'href="([^"]+)"',logo).group(1)==re.search(r'href="([^"]+)"',original_logo).group(1),'previous_tagline_removed':True,'review':'pending','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout,'visual_review':'pending'}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,indent=2)+'\n')
(P/(stem+'-render.py')).write_text(Path('/tmp/mark1286-centred-header.py').read_text())
(P/(stem+'-prompt.md')).write_text('# Centred global header — production brief\n\nStudent revision: [Denmark flag] Copenhagen meet [Green SM logo]. Remove the comma; use the exact case Copenhagen meet. Centre this title at x=836 in the A0 native frame (width 1672). Centre the unchanged exact subtitle A 12-month market-entry plan for local electric taxi rides below it. Remove Clear terms. Local care. entirely. Keep the existing group cloud at the upper right; place a hand-drawn rendition of the student-supplied University of Greenwich master logo at the upper left. University asset is made with built-in imagegen and embedded unchanged; Green SM asset is reused unchanged. Keep all ten marketing cells, vehicle/background/flags/identities untouched. Native controlled header lettering and simple flat Danish flag. Return standalone header close-up and full A0 proof for review.\n')
print(json.dumps({'stem':stem,'title_left':left,'title_right':lx+logow,'centre':cx,'records':records,'existing_art_preserved':True},indent=2))
