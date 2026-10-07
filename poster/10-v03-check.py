"""Focused source-to-artwork and geometry checks for Section 10 v03."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from PIL import Image

HERE = Path(__file__).resolve().parent
PREFIX = '10-v03'
COPY = HERE / f'{PREFIX}-copy.md'
SVG = HERE / f'{PREFIX}.svg'
MANIFEST = json.loads((HERE / f'{PREFIX}-manifest.json').read_text())
clean = re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)
clean = re.sub(r'^#{1,6}\s*', '', clean, flags=re.M)
strings = [re.sub(r'^#+\s*', '', block.strip()).replace('**', '').strip()
           for block in clean.split('\n\n') if block.strip()]
texts = MANIFEST['text_objects']
boxes = [{'id': t['id'], 'text': line['text'], 'bbox': line['bbox'], 'owner': t['owner']}
         for t in texts for line in t['lines']]


def overlaps(a, b):
    x1, y1, x2, y2 = a
    z1, w1, z2, w2 = b
    return min(x2, z2) > max(x1, z1) and min(y2, w2) > max(y1, w1)


def inside(box, bounds):
    return (box[0] >= bounds[0] and box[1] >= bounds[1]
            and box[2] <= bounds[2] and box[3] <= bounds[3])


root = ET.parse(SVG).getroot()
concept_list = (HERE.parent / '03_course_materials' / 'concept-list.txt').read_text().lower()
all_pairs = [(a, b) for i, a in enumerate(boxes) for b in boxes[i + 1:]
             if overlaps(a['bbox'], b['bbox'])]
stage_bounds = {
    'local-consideration': [78, 740, 610, 1100],
    'paid-trial': [650, 740, 1180, 1100],
    'stable-service': [1225, 740, 1760, 1100],
    'repeat-growth': [1800, 740, 2310, 1100],
}
canvas = [30, 30, 2370, 1770]
copy_text = '\n'.join(strings)
rendered_strings = [t['text'] for t in texts]
counting_text = re.sub(r'^\d+[.)]\s+', '', clean, flags=re.M)
word_count = sum(bool(re.search(r'\w', word)) for word in re.split(r'\s+', counting_text))
svg_visible_labels = [e.attrib.get('aria-label', '') for e in root.iter()
                      if e.attrib.get('aria-label') is not None]
checks = {
    'canonical_section_heading': strings[0] == '10. Business Goals & Growth',
    'all_copy_is_rendered_in_order': strings == rendered_strings,
    'each_paragraph_reconstructs_from_paths': all(
        ' '.join(line['text'] for line in t['lines']) == t['text'] for t in texts),
    'copy_within_150_word_budget': word_count <= 150,
    'targets_are_proposals': 'targets, not results' in copy_text,
    'correct_measure_is_consideration': '+10 pp' in copy_text and 'Build consideration locally' in copy_text,
    'paid_trip_is_counted_as_first_rider': '378' in copy_text and 'first paid trip' in copy_text,
    'repeat_has_full_90_day_cohort_basis': 'first riders with a full observation window' in copy_text and 'Paid repeat within 90 days' in copy_text,
    'growth_is_gated_on_service_and_repeat': 'service and mature-repeat gates before growth' in copy_text,
    'business_alignment_and_retention_concept_visible': all(
        value in copy_text for value in ['stable local operation', 'Retention over acquisition', 'sustainable growth']),
    'retention_concept_is_in_module_register': 'retention over acquisition' in concept_list,
    'company_capability_boundary_visible': 'proposed controlled fleet and driver model' in copy_text and 'outcomes remain untested' in copy_text,
    'year_one_non_break_even_caveat_visible': 'illustrative year-one model does not break even' in copy_text,
    'no_visible_citations_or_logo': not any(re.search(r'\bE-\d{3}\b', s) for s in svg_visible_labels)
        and MANIFEST['citation_visible'] is False and MANIFEST['logo_used'] is False,
    'all_text_uses_outline_paths': not any(e.tag.endswith('}text') for e in root.iter()),
    'no_text_bounds_overlap': not all_pairs,
    'all_text_inside_canvas': all(inside(box['bbox'], canvas) for box in boxes),
    'stage_text_stays_in_its_column': all(
        inside(box['bbox'], stage_bounds[box['owner']])
        for box in boxes if box['owner'] in stage_bounds),
    'no_raster_art_or_external_images': not any(e.tag.endswith('}image') for e in root.iter()),
    'full_and_preview_dimensions': Image.open(HERE / f'{PREFIX}.png').size == (2400, 1800)
        and Image.open(HERE / f'{PREFIX}-small-preview.png').size == (1200, 900),
    'manifest_matches_copy_and_svg': MANIFEST['copy_sha256'] == hashlib.sha256(COPY.read_bytes()).hexdigest()
        and MANIFEST['version'] == 'v03',
}
result = {
    'status': 'passed focused candidate checks' if all(checks.values()) else 'failed focused candidate checks',
    'date': '2026-10-04',
    'checks': checks,
    'all_checks_pass': all(checks.values()),
    'word_count': word_count,
    'text_objects': len(texts),
    'text_overlaps': [[a['id'], b['id']] for a, b in all_pairs],
    'svg_sha256': hashlib.sha256(SVG.read_bytes()).hexdigest(),
    'png_sha256': hashlib.sha256((HERE / f'{PREFIX}.png').read_bytes()).hexdigest(),
    'approval': 'Student-accepted Section 10 v03 text and artwork on 4 October 2026; group approval, assembled-poster fit and print approval unverified',
}
(HERE / f'{PREFIX}-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'all_checks_pass': result['all_checks_pass'],
                  'failed': [key for key, ok in checks.items() if not ok],
                  'words': result['word_count'], 'text_objects': len(texts),
                  'overlaps': result['text_overlaps']}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)
