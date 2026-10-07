from pathlib import Path
import re,subprocess,json,hashlib
P=Path.cwd()/'poster';base=P/'poster-global-header-v02-2026-10-05.svg';stem='poster-white-sections-v01-2026-10-05'
s=base.read_text();matches=list(re.finditer(r'fill="#fdfbef"',s));assert len(matches)==112
out=s.replace('fill="#fdfbef"','fill="#ffffff"')
restored=out
for m in matches:restored=restored[:m.start()]+'fill="#fdfbef"'+restored[m.end():]
assert restored==s
(P/(stem+'.svg')).write_text(out)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'.png')),str(P/(stem+'.svg'))],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(P/(stem+'.pdf')),str(P/(stem+'.svg'))],check=True)
records=[]
for i in range(1,11):
 old=P/f'{i:02}-brief-heading-v01-2026-10-05-panel.svg';raw=old.read_text();new=raw.replace('fill="#fdfbef"','fill="#ffffff"')
 prefix=f'{i:02}-white-bg-v01-2026-10-05';dest=P/(prefix+'-panel.svg');dest.write_text(new)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2000','-o',str(P/(prefix+'-panel.png')),str(dest)],check=True)
 # An optional reusable overlay has no main-cell paper fill; icon whites are retained.
 exterior=re.search(r'</defs>(<path\b[^>]+>)',new);assert exterior
 path=exterior.group(1);assert 'fill="#ffffff"' in path
 transparent=new[:exterior.start(1)]+path.replace('fill="#ffffff"','fill="none"')+new[exterior.end(1):]
 layer=P/(prefix+'-transparent.svg');layer.write_text(transparent)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2000','-o',str(P/(prefix+'-transparent.png')),str(layer)],check=True)
 oldlabels=re.findall(r'aria-label="([^"]+)"',raw);assert oldlabels==re.findall(r'aria-label="([^"]+)"',new)
 oldimages=re.findall(r'(?:href|xlink:href)="data:[^"]+"',raw);assert oldimages==re.findall(r'(?:href|xlink:href)="data:[^"]+"',new)
 records.append({'section':i,'white_panel':dest.name,'transparent_layer':layer.name,'cream_fills_changed':raw.count('fill="#fdfbef"'),'display_labels_preserved':True,'embedded_images_preserved':True})
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'neutral_fills_changed':len(matches),'scope':'Ten main cell paper fills; 101 cream neutral diagram/icon fills; one group-cloud paper fill. No brand colour, heading, figure, geometry or image payload changed.','change_only_fill_attributes_restores_base_exactly':restored==s,'sections':records,'transparent_layer_rule':'Main cell fill none; existing icon whites retained; outside all native cells remains transparent. Full A0 uses white paper fills, not cyan-through transparent cells.','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout,'visual_review':'pending','student_review':'pending'}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,indent=2)+'\n')
(P/(stem+'-prompt.md')).write_text('# White and transparent section backgrounds — production brief\n\nStudent asks transparent/white backgrounds across all sections. Use pure white #ffffff for all ten marketing cell paper fills and neutral cream diagram/icon surfaces. Set group-information cloud paper to the same white. Preserve navy strokes, cyan/yellow brand colours, flags, all lettering/figures/diagrams, authentic embedded logos, car, skyline, header geometry and background raster. Generate standalone white panels with transparency outside the native cell. Also export optional transparent overlays: main cell fill none, icon whites retained. Full A0 assembly uses white main-cell fills to keep cyan car from showing through content. Preserve the original source/version and update only latest routes. Return full proof for human review.\n')
(P/(stem+'-render.py')).write_text(Path('/tmp/mark1286-white-sections.py').read_text())
print('White poster and all ten white/transparent standalone panels exported. Neutral fills changed:',len(matches))
