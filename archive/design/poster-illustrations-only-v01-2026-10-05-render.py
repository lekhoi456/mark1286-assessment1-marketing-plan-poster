from pathlib import Path
from lxml import etree as E
import json,subprocess,hashlib
P=Path.cwd()/'poster';base=P/'poster-references-v03-2026-10-05.svg';stem='poster-illustrations-only-v01-2026-10-05'
ns='http://www.w3.org/2000/svg';tag=lambda t:'{'+ns+'}'+t
r=E.parse(str(base));removed=[]
# Controlled letter outlines each live in an isolated labelled group.
for x in list(r.xpath('//*[local-name()="g" and @aria-label]')):
 if x.get('id')=='fit01-vinfast-full-wordmark' or (len(x)==1 and x[0].tag==tag('path')):
  removed.append(x.get('aria-label'));x.getparent().remove(x)
for x in list(r.xpath('//*[local-name()="text"]')):
 removed.append(''.join(x.itertext()));x.getparent().remove(x)
# Bibliography is lettering only; retain its original white paper rect.
footer=r.xpath('//*[@id="harvard-references-footer-v01"]')[0]
for x in list(footer):
 if x.tag!=tag('rect'):footer.remove(x)
# Preserve the university compass graphic; clip its wordmark out in native SVG.
greenwich=r.xpath('//*[@id="greenwich-hand-drawn-logo"]')[0]
wrapper=E.Element(tag('svg'),x=greenwich.get('x'),y=greenwich.get('y'),width=str(310*680/2078),height=greenwich.get('height'),viewBox='0 0 680 757',overflow='hidden',id='greenwich-compass-only')
parent=greenwich.getparent();parent.replace(greenwich,wrapper)
for k,v in {'x':'0','y':'0','width':'2078','height':'757'}.items():greenwich.set(k,v)
wrapper.append(greenwich)
# Wordmark assets temporarily removed; final run inserts the imagegen bird symbol.
asset=P/'assets/green-sm-symbol-only-v01-2026-10-05.png'
for ident,width,height in [('fit01-authentic-green-sm-logo',15,14),('header-authentic-green-sm-logo',116,78.06117647058824)]:
 old=r.xpath('//*[@id="'+ident+'"]')[0];parent=old.getparent()
 if asset.exists():
  new=E.Element(tag('image'),id=ident+'-symbol-only',x=old.get('x'),y=old.get('y'),width=str(width),height=str(height),href='assets/'+asset.name,preserveAspectRatio='xMidYMid meet');parent.replace(old,new)
 else:parent.remove(old)
section4=r.xpath('//*[@id="section-04-v03-candidate"]')[0]
for old in list(section4):
 if old.tag==tag('image'):
  if asset.exists():
   new=E.Element(tag('image'),id='brand-symbol-only',x=old.get('x'),y=old.get('y'),width='41',height=old.get('height'),href='assets/'+asset.name,preserveAspectRatio='xMidYMid meet');section4.replace(old,new)
  else:section4.remove(old)
# Title underlines are writing guides and remain. Icons, bars, flags, arrows and geometry are untouched.
assert not r.xpath('//*[local-name()="text"]')
assert not r.xpath('//*[local-name()="g" and @aria-label and count(*)=1 and local-name(*)="path"]')
for x in r.xpath('//*[local-name()="title" or local-name()="desc"]'):
 x.text='Illustrations-only drawing reference' if x.getparent() is r.getroot() else 'Graphic'
out=P/(stem+'.svg');out.write_bytes(E.tostring(r,encoding='utf-8',xml_declaration=True))
for fmt in ['png','pdf']:
 cmd=['/opt/homebrew/bin/rsvg-convert']+(['-w','2400'] if fmt=='png' else ['-f','pdf'])+['-o',str(P/(stem+'.'+fmt)),str(out)];subprocess.run(cmd,check=True)
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout
check={'source':base.name,'source_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'removed_visible_lettering_groups':len(removed),'text_elements_remaining':len(r.xpath('//*[local-name()="text"]')),'wordmarks_removed':True,'ten_cells_retained':len(r.xpath('//*[starts-with(@id,"cell-") and local-name()="g"]')),'textful_master_unchanged':True,'symbol_asset_ready':asset.exists(),'pdfinfo':info,'visual_review':'pending'}
(P/(stem+'-checks.json')).write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check))
