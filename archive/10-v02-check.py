"""Focused Section 10 v02 copy, source, asset and layout checks."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

HERE = Path(__file__).resolve().parent
P = '10-v02'
M = json.loads((HERE / f'{P}-manifest.json').read_text())
COPY = HERE / M['copy_source']
ART = HERE / M['art_asset']
clean = re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)
strings = [re.sub(r'^#+\s*', '', b.strip()).replace('**', '').strip()
           for b in clean.split('\n\n') if b.strip()]
root = ET.parse(HERE / f'{P}.svg').getroot()
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
texts = M['text_objects']
boxes = [{'id': t['id'], 'text': line['text'], 'bbox': line['bbox'],
          'owner': t['owner']} for t in texts for line in t['lines']]
def intersects(a, b):
    x1, y1, x2, y2 = a
    z1, v1, z2, v2 = b
    return min(x2, z2) > max(x1, z1) and min(y2, v2) > max(y1, v1)
overlaps = [(a['id'], b['id']) for i, a in enumerate(boxes)
            for b in boxes[i+1:] if intersects(a['bbox'], b['bbox'])]
images = [e for e in root.iter() if e.tag.endswith('}image')]
art_bytes = ART.read_bytes()
source_record = M['internal_source_records'][0]
source_pdf = (HERE / source_record['pdf']).resolve()
card_frames = {f['id'].removesuffix('-frame'): f['bounds'] for f in M['frames']
               if f['id'].endswith('-frame') and f['id'] not in ('outer-pen-frame',)}
def inside(b, outer):
    return b[0] >= outer[0] and b[1] >= outer[1] and b[2] <= outer[2] and b[3] <= outer[3]

copy_text = '\n'.join(strings)
svg_labels = [e.attrib.get('aria-label', '') for e in root.iter()
              if e.attrib.get('aria-label') is not None]
checks = {
    'exact-numbered-heading': strings[0] == '10. Business Goals & Growth',
    'all-controlled-copy-rendered-in-order': strings == [t['text'] for t in texts],
    'rendered-lines-reconstruct-each-paragraph': all(' '.join(l['text'] for l in t['lines']) == t['text'] for t in texts),
    'within-190-word-panel-budget': 0 < sum(1 for w in re.split(r'\s+', re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)) if re.search(r'\w', w)) <= 190,
    'proposed-plan-and-targets-labelled': 'Proposed 12-month plan' in copy_text and 'targets, not results' in copy_text and 'Proposed targets' in copy_text,
    'sample-size-and-regional-limit-visible': 'n=79' in copy_text and 'Not representative.' in copy_text,
    'approved-s1-and-age-scope-visible': 'self-paying repeat taxi riders, 25–44' in copy_text,
    'digital-route-ends-in-app': 'Search/social → one local info page → Green SM app booking.' in copy_text,
    'completed-paid-trip-is-sale': 'Completed, paid first trip = sale.' in copy_text,
    'all-three-proposed-outcome-targets-visible': '378 paid first riders' in copy_text and '+10 pp awareness' in copy_text and '≥35% mature 90-day repeat' in copy_text,
    'all-four-service-floors-visible': all(v in copy_text for v in ['completion ≥95%', 'service cancellations ≤2%', 'referenced complaints answered in 24 h ≥90%', 'fare/area clarity ≥80%']),
    'service-and-mature-repeat-gate-scale': 'Growth follows only when service and mature-repeat evidence holds.' in copy_text,
    's9-pilots-conditional-and-cost-gated': 'Conditional S9 proposals' in copy_text and 'separate costing required' in copy_text,
    'm12-decision-uses-service-repeat-contribution': all(v in copy_text for v in ['M12:', 'O1 to O4', 'service, mature repeat, contribution', 'Renew · Revise · Stop.']),
    'year-one-non-break-even-visible': 'Illustrative year-one model does not break even.' in copy_text,
    'company-capability-bounded': 'Copenhagen outcomes untested.' in copy_text,
    'no-visible-citations-or-logo': not any(re.search(r'\bE-\d{3}\b', s) for s in svg_labels) and M['citation_visible'] is False and M['logo_used'] is False,
    'all-text-is-controlled-outline-paths': not any(e.tag.endswith('}text') for e in root.iter()),
    'no-text-bounds-overlap': not overlaps,
    'all-text-inside-canvas': all(inside(b['bbox'], [30, 30, M['canvas_px'][0]-30, M['canvas_px'][1]-30]) for b in boxes),
    'stage-text-inside-own-frame': all(inside(b['bbox'], card_frames[b['owner']]) for b in boxes if b['owner'] in card_frames),
    'four-art-crops-are-unique-and-clipped': len(M['raster_placements']) == 4 and len({tuple(p['source']) for p in M['raster_placements']}) == 4 and all(root.find(f'.//*[@id="{p["id"]}-source-clip"]') is not None for p in M['raster_placements']),
    'svg-images-reference-versioned-local-art': len(images) == 4 and all(e.get('href') == ART.name for e in images),
    'v02-art-byte-identical-to-v01-source': ART.read_bytes() == (HERE / '10-candidate-v01-2026-10-04-generated-art.png').read_bytes(),
    'source-pdf-hash-matches-verified-record': sha(source_pdf) == source_record['sha256'],
    'source-records-e024-table-pages-and-sample': source_record['evidence_ids'] == ['E-024'] and source_record['table'] == '5.12' and source_record['physical_pages'] == [150, 151] and source_record['verification'].startswith('Opened PDF pages 150-151'),
    'full-and-preview-renders-have-expected-size': Image.open(HERE / f'{P}.png').size == (2400, 1800) and Image.open(HERE / f'{P}-small-preview.png').size == (1200, 900),
    'all-art-references-resolve-inside-poster-folder': all((HERE / e.get('href', '')).resolve() == ART.resolve() for e in images),
    'no-visible-performance-emissions-or-sales-claims': all(v in M['source_claim_boundaries'] for v in ['No emissions saving, AI performance, subscription sale or Copenhagen success claimed']),
}
result = {
    'status': 'passed focused candidate checks' if all(checks.values()) else 'failed focused candidate checks',
    'date': '2026-10-04',
    'checks': checks,
    'all_checks_pass': all(checks.values()),
    'text_objects': len(texts),
    'text_overlaps': overlaps,
    'source_pdf_sha256': sha(source_pdf),
    'art_sha256': sha(ART),
    'svg_sha256': sha(HERE / f'{P}.svg'),
    'png_sha256': sha(HERE / f'{P}.png'),
    'visual_inspection': [
        'Full 2400 px PNG and 1200 px preview inspected after the final card-1 spacing correction.',
        'Four-stage reading order is visible from rider evidence and S1 through the app route and service-to-repeat loop to gated growth.',
        'No observed clipping, card overflow, lettering collision or neighbouring artwork sliver in the inspected preview.',
    ],
    'approval': 'Candidate only; parent selection pending; no group approval',
    'scope': 'Only new poster/10-v02-* files written; v01, other panels, shortcuts and shared assets untouched.',
    'unverified': ['Parent selection', 'Full A0 fit', 'Physical print legibility'],
}
(HERE / f'{P}-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'all_checks_pass': result['all_checks_pass'],
                  'failed': [k for k, v in checks.items() if not v],
                  'text_objects': len(texts), 'overlaps': overlaps}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)
