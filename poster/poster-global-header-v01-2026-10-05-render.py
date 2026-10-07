from pathlib import Path
import json,re,subprocess,html,hashlib
P=Path.cwd()/'poster'
base=P/'poster-brief-headings-v01-2026-10-05.svg'
stem='poster-global-header-v01-2026-10-05'
s=base.read_text();original=s
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
records=[]
def glyph(t,x,y,z,font='MarkerFelt-Wide',colour='#173a47'):
 proc.stdin.write(json.dumps({'text':t,'font':font,'size':z})+'\n');proc.stdin.flush();d=json.loads(proc.stdout.readline());assert 'error' not in d
 a,b,c,e=d['bounds'];records.append({'text':t,'font':font,'resolved_fonts':d['resolved_font_names'],'bbox':[x+a,y-e,x+c,y-b],'width':d['width'],'a0_pt':round(z*1189/1672*72/25.4,2)})
 return f'<g aria-label="{html.escape(t,quote=True)}"><path d="{d["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{colour}"/></g>',d['width']
parts=[]
a,w=glyph('COPENHAGEN,',85,135,60);parts.append(a)
fx=85+w+20
parts.append(f'<g id="title-denmark-flag" aria-label="Denmark flag"><path d="M{fx} 94L{fx+60} 95L{fx+59} 135L{fx} 134Z" fill="#c8102e" stroke="#173a47" stroke-width="1.2" stroke-linejoin="round"/><path d="M{fx+20} 95L{fx+20} 134M{fx} 115L{fx+59} 115" fill="none" stroke="#ffffff" stroke-width="6"/></g>')
mx=fx+60+24;a,w=glyph('MEET',mx,135,60);parts.append(a)
lx=mx+w+25
start=s.index('id="fit01-authentic-green-sm-logo"');start=s.rfind('<svg',0,start);end=s.index('</svg>',start)+6
logo=s[start:end];original_logo=logo
first_end=logo.index('>')+1;tag=logo[:first_end]
for k,v in [('id','header-authentic-green-sm-logo'),('x',str(lx)),('y','37'),('width','380'),('height',str(380*572/2125))]:tag=re.sub(r'\b'+k+r'="[^"]*"',k+'="'+v+'"',tag)
logo=tag+logo[first_end:];logo=logo.replace('id="green-sm-shared-hand-drawn-png"','id="header-green-sm-shared-hand-drawn-png"')
parts.append(logo)
right=lx+380;cx=(85+right)/2
# Centre subtitle and secondary tagline using measured native glyph widths.
for t,y,z in [('A 12-month market-entry plan for local electric taxi rides',187,30),('Clear terms. Local care.',226,25)]:
 a,w=glyph(t,0,y,z,'ChalkboardSE-Regular');records.pop();a,w=glyph(t,cx-w/2,y,z,'ChalkboardSE-Regular');parts.append(a)
 if y==226:
  x=cx-w/2;parts.append(f'<path d="M{x} 233Q{cx} 235 {x+w} 233" fill="none" stroke="#e3bb42" stroke-width="3" stroke-linecap="round"/>')
proc.stdin.close();proc.wait()
header='<g id="global-header-v01-candidate" aria-label="Copenhagen, meet Green SM; market-entry plan">'+''.join(parts)+'</g>'
out=s[:-6]+header+'</svg>'
# Replace stale background-only accessibility metadata; all actual existing artwork remains byte-identical.
oldtitle=re.search(r'<title>.*?</title>',out).group();olddesc=re.search(r'<desc>.*?</desc>',out).group()
newtitle='<title>Copenhagen, meet Green SM — 12-month market-entry plan</title>'
newdesc='<desc>A0 landscape hand-drawn marketing-plan poster. Ten populated marketing cells use assignment headings; group details appear in the upper-right cloud. Header adds the confirmed Denmark flag, Green SM logo, subtitle and secondary local tagline. Header candidate awaits student review.</desc>'
out=out.replace(oldtitle,newtitle,1).replace(olddesc,newdesc,1)
restored=out.replace(header,'').replace(newtitle,oldtitle,1).replace(newdesc,olddesc,1)
assert restored==original
assert right<1220,right
for r in records:assert r['bbox'][0]>25 and r['bbox'][2]<1220 and r['bbox'][1]>25 and r['bbox'][3]<240
for i,a in enumerate(records):
 for b in records[i+1:]:
  x=a['bbox'];y=b['bbox'];assert not(min(x[2],y[2])>max(x[0],y[0]) and min(x[3],y[3])>max(x[1],y[1]))
(P/(stem+'.svg')).write_text(out)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'.png')),str(P/(stem+'.svg'))],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(P/(stem+'.pdf')),str(P/(stem+'.svg'))],check=True)
close=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2400" height="500" viewBox="55 25 1130 235">{header}</svg>'
(P/(stem+'-close-up.svg')).write_text(close)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'-close-up.png')),str(P/(stem+'-close-up.svg'))],check=True)
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'base_artwork_restoration_exact':restored==original,'header_text':records,'header_right_edge':right,'logo_image_payload_preserved':re.search(r'href="([^"]+)"',logo).group(1)==re.search(r'href="([^"]+)"',original_logo).group(1),'header_review':'pending','existing_cells_cloud_vehicle_landmarks':'unchanged','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout,'visual_review':'pending'}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,indent=2)+'\n')
(P/(stem+'-prompt.md')).write_text('# Global header — production brief\n\nAdd the confirmed COPENHAGEN, MEET GREEN SM lock-up to the sky left of the existing identity cloud. Place a simple Denmark flag after Copenhagen; use the existing authentic hand-drawn Green SM image without recolouring or modifying its payload. Match controlled hand-drawn lettering used by the cells. Below, centre the exact subtitle: A 12-month market-entry plan for local electric taxi rides. Place the agreed secondary tagline Clear terms. Local care. beneath it; underline only its width. Preserve all ten cells, background, vehicle, landmarks, right-hand flag and group cloud. A0 landscape edge-to-edge. No visible citations. Return full proof and close-up for student review.\n')
(P/(stem+'-render.py')).write_text(Path('/tmp/mark1286-header.py').read_text())
print(json.dumps({'stem':stem,'header_right_edge':right,'text':records,'base_art_preserved':True},indent=2))
