from pathlib import Path
import re,json,subprocess,hashlib,copy
from lxml import etree as E
P=Path.cwd()/'poster';base=P/'poster-references-v03-2026-10-05.svg';stem='poster-references-v04-2026-10-07'
src=base.read_text();start=src.index('<g id="global-header-above-title-v01"');end=src.index('<g id="harvard-references-footer-v01"');old=src[start:end]
ns='http://www.w3.org/2000/svg';g=E.fromstring(('<svg xmlns="'+ns+'" xmlns:xlink="http://www.w3.org/1999/xlink">'+old+'</svg>').encode())[0]
logo=g[0];row=g[1]
subtitle=row.xpath('.//*[@aria-label="A 12-month market-entry plan for local electric taxi rides"]')[0];subtitle.getparent().remove(subtitle)
row.set('transform','translate(317.68 153.5) scale(0.62)');row.set('id','copenhagen-brand-subtitle-v04');row.set('aria-label','Copenhagen, meet Green SM')
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
text='12‑Month Marketing Plan for Electric Taxi Launch'
proc.stdin.write(json.dumps({'text':text,'font':'MarkerFelt-Wide','size':34})+'\n');proc.stdin.flush();glyph=json.loads(proc.stdout.readline());proc.stdin.close();proc.wait()
x=836-glyph['width']/2
heading=E.Element('{'+ns+'}g',{'id':'marketing-plan-primary-title-v04','aria-label':text})
path=E.SubElement(heading,'{'+ns+'}path',d=glyph['path'],transform=f'translate({x:.6f} 167) scale(1 -1)',fill='#173a47')
g.insert(1,heading);g.set('aria-label','Marketing plan title above Copenhagen brand subtitle; Greenwich upper left')
new=E.tostring(g,encoding='unicode')
new=re.sub(r' xmlns(?::xlink)?="[^"]+"','',new)+'\n'
out=src[:start]+new+src[end:];assert out.replace(new,old,1)==src
(P/(stem+'.svg')).write_text(out)
for fmt in ['png','pdf']:
 args=['/opt/homebrew/bin/rsvg-convert']+(['-w','2400'] if fmt=='png' else ['-f','pdf'])+['-o',str(P/(stem+'.'+fmt)),str(P/(stem+'.svg'))];subprocess.run(args,check=True)
close=E.fromstring(out.encode());close.set('width','3000');close.set('height',str(3000*270/1672));close.set('viewBox','0 0 1672 270')
(P/(stem+'-header-close-up.svg')).write_bytes(E.tostring(close,encoding='utf-8',xml_declaration=True));subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','3000','-o',str(P/(stem+'-header-close-up.png')),str(P/(stem+'-header-close-up.svg'))],check=True)
for suffix in ['-references.md','-reference-selection.json','-references-close-up.svg','-references-close-up.png']:
 (P/(stem+suffix)).write_bytes((P/('poster-references-v03-2026-10-05'+suffix)).read_bytes())
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'primary_title':text,'secondary_title':'Copenhagen, meet Green SM','main_font':'MarkerFelt-Wide','main_font_size':34,'main_advance_bounds':[x,x+glyph['width']],'main_baseline':167,'secondary_row_scale':0.62,'secondary_text_baseline':231,'both_centred_at':836,'restoration_to_base_exact':out.replace(new,old,1)==src,'ten_panels_cloud_footer_background_greenwich_unchanged':True,'pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout,'student_review':'pending'}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
(P/(stem+'-prompt.md')).write_text('''# Swap the primary and secondary title

Request, 7 October 2026: replace A 12-month market-entry plan for local electric taxi rides with 12‑Month Marketing Plan for Electric Taxi Launch, and swap positions with Copenhagen, meet Green SM.

Use the comma-corrected v03 native assembly (all non-header artwork identical to the attached v02). Top/main line: exact user wording, including U+2011 non-breaking hyphen, in controlled hand-drawn Marker Felt. Lower/supporting line: the original Denmark flag / Copenhagen, meet / exact Green SM logo payload, scaled together and centred. Both lines centre on native x=836. Main font size 34 fits clear of the right identity cloud. Secondary text baseline 231 allows clearance for the tall authentic logo. University logo remains in its previous upper-left position.

Only the header changes. Preserve all ten section wording/numbers/artwork, cloud identities, harbour/car background and Harvard References. Preserve v02/v03 and the illustrations-only export. Native SVG editing and deterministic PNG/PDF export; no image regeneration. Return the new proof for student review.
''')
print(json.dumps(checks,ensure_ascii=False))
