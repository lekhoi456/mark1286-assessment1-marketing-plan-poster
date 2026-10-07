from pathlib import Path
import re,json,subprocess,hashlib
P=Path.cwd()/'poster';asset=P/'assets/copenhagen-left-cloud-removed-v01-2026-10-05.png';assert asset.exists()
# Feather a bounded sky-only patch from the edited raster. No other generated region is used.
patch='''<g id="left-cloud-removal-v01"><defs>
<linearGradient id="left-cloud-x-fade" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="330" y2="0"><stop offset="0" stop-color="white"/><stop offset="0.89" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient>
<linearGradient id="left-cloud-y-fade" gradientUnits="userSpaceOnUse" x1="0" y1="90" x2="0" y2="255"><stop offset="0" stop-color="black"/><stop offset="0.12" stop-color="white"/><stop offset="0.88" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient>
<mask id="left-cloud-vertical-fade" maskUnits="userSpaceOnUse" x="0" y="90" width="330" height="165"><rect x="0" y="90" width="330" height="165" fill="url(#left-cloud-y-fade)"/></mask>
<mask id="left-cloud-bounded-mask" maskUnits="userSpaceOnUse" x="0" y="90" width="330" height="165"><rect x="0" y="90" width="330" height="165" fill="url(#left-cloud-x-fade)" mask="url(#left-cloud-vertical-fade)"/></mask>
</defs><image id="left-cloud-sky-patch" x="0" y="0" width="1672" height="1182.634146" preserveAspectRatio="none" href="assets/copenhagen-left-cloud-removed-v01-2026-10-05.png" mask="url(#left-cloud-bounded-mask)"/></g>'''
records=[]
for filename,stem in [('poster-white-sections-v01-2026-10-05.svg','poster-no-left-cloud-v01-2026-10-05'),('poster-a0-layout-v02-2026-10-04.svg','poster-background-no-left-cloud-v01-2026-10-05')]:
 base=P/filename;original=base.read_text();s=original
 # The layout-only view adopts current white section/cloud paper for consistency.
 if 'background-' in stem:s=s.replace('fill="#fdfbef"','fill="#ffffff"')
 m=re.search(r'<image\b[^>]*id="full-page-copenhagen-background"[^>]*/>',s);assert m
 out=s[:m.end()]+patch+s[m.end():];assert out.replace(patch,'',1)==s
 target=P/(stem+'.svg');target.write_text(out)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(stem+'.png')),str(target)],check=True)
 if stem=='poster-no-left-cloud-v01-2026-10-05':subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(P/(stem+'.pdf')),str(target)],check=True)
 records.append({'base':filename,'output':stem,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'patch_removal_restores_base_art_exactly':out.replace(patch,'',1)==s,'other_changes':'Layout-only view adopts eleven already-requested white cell/cloud fills' if 'background-' in stem else 'none'})
(P/'poster-no-left-cloud-v01-2026-10-05-checks.json').write_text(json.dumps({'scope':'Remove decorative upper-left cloud only','asset':str(asset.relative_to(P)),'patch_bounds_native':[0,90,330,255],'native_viewbox':[0,0,1672,1182.634146],'method':'Built-in imagegen removal; use only feathered bounded sky patch, retain original image everywhere else','versions':records,'visual_review':'pending','student_review':'pending','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/'poster-no-left-cloud-v01-2026-10-05.pdf')],capture_output=True,text=True,check=True).stdout},indent=2)+'\n')
(P/'poster-no-left-cloud-v01-2026-10-05-render.py').write_text(Path('/tmp/mark1286-remove-left-cloud.py').read_text())
(P/'poster-no-left-cloud-v01-2026-10-05-prompt.md').write_text('''# Remove decorative left cloud\n\nStudent request: remove the left background cloud. Preserve University of Greenwich logo, header, all ten white sections, group information cloud at right, car, harbour, flags and page framing. Built-in imagegen edits the original empty-cell background: remove only the decorative white-outline upper-left cloud and its horizontal white strokes, continuing the surrounding cyan sky. Keep all other elements unchanged. The assembly uses only a feathered bounded patch x=0–330, y=90–255 in the original 1672-wide frame; generated pixels elsewhere are not used. Native content/header artwork and original raster remain unchanged outside this patch. Return full A0 proof and reusable blank-cell background.\n''')
print('Cloud-free poster and reusable background exported; existing SVG layers unchanged.')
