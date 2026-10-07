"""Check the D-158 content-upgrade proof against the v04 source SVG.

Usage: python3 -B poster/poster-content-upgrade-v01-2026-10-07-check.py SOURCE.svg OUT_DIR
Writes poster-content-upgrade-v01-2026-10-07-checks.json into OUT_DIR.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

STEM = 'poster-content-upgrade-v01-2026-10-07'
LABEL = re.compile(r'<g aria-label="([^"]*)"[^>]*>\s*(?:<title>[^<]*</title>)?\s*<path d="([^"]+)"\s*transform="([^"]+)"')

REMOVED = {
    'Owned fleet · Employed drivers', 'Shared: App booking · Electric options', '10% vs 20%',
    'Max DKK30 · 400 cap · 1/rider', '*Proposed', '4Ps*', 'DATA*', 'Opt-in · proposed', '30-day paid*',
    'Sales strategy • proposed', '12 months · excluding VAT', 'Outside budget: cars, drivers,',
    'charging / frontline support', 'DKK / % · bars: 0–300,000', '*Paid campaign cohort only',
    'TRACKING PROPOSED', 'PROPOSED PILOTS · Local performance untested',
    'DKK600,000 excludes app/platform build + vehicle/driver/frontline operations',
}
ADDED = {
    'Owned fleet (590 registered) · Employed drivers', 'Later: visitors · business accounts',
    '(part to be sold)', 'Shared: App booking · Electric options · Similar fares (Dantaxi/Drivr)',
    '· ±11 pp', '/ Content', 'DKK15 vs DKK30', 'Post-launch · 400 riders · 1 each', '4Ps', 'DATA',
    'Opt-in', '30-day paid', 'bestil taxa', 'Elektrisk taxa', 'Tjek prisen.', 'Book i appen.',
    '· CTR, CPC', '· app installs', '· conversion', 'Nov 2026–Oct 2027 · excluding VAT',
    'Outside budget: app build, cars,', 'drivers, charging / frontline support',
    'Unit check: DKK165 CAC repaid in about 2.4 rides', 'at an assumed DKK68 contribution per ride',
    '*Paid-campaign riders only, not all Green SM trips', 'n=400 per wave', 'TRACKING',
    'PILOTS · Local performance untested',
    'Neuro cue test: calm-ride vs fare-first ads → attention (CTR) · recall (survey)',
    'Member contributions', 'Nguyen Phi Giao · 001545326', 'Le Quoc Khoi · 001545344',
    'Nguyen Ho Khanh Vy · 001545423', 'Contribution: to be confirmed by the group',
    'References: back of chart',
}
MOVED = {'Consideration'}  # same lettering, lifted 5 units to make room for n=400 per wave


def unesc(v):
    return v.replace('&amp;', '&').replace('&quot;', '"').replace('&#x27;', "'")


def labels(text):
    return [(unesc(m.group(1)), m.group(2), m.group(3)) for m in LABEL.finditer(text)]


def main():
    src = Path(sys.argv[1]).read_text()
    out_dir = Path(sys.argv[2])
    front = (out_dir / f'{STEM}.svg').read_text()
    back = (out_dir / f'{STEM}-back.svg').read_text()
    i = src.find('<g id="harvard-references-footer-v01"')
    footer_labels = {l for l, _, _ in labels(src[i:])}
    old = labels(src[:i])
    new_all = labels(front)
    old_c = Counter(l for l, _, _ in old)
    new_c = Counter(l for l, _, _ in new_all)
    checks = {}
    gone = {l for l in REMOVED if new_c[l] < old_c[l]}
    checks['removed_labels_gone'] = sorted(REMOVED - gone) == []
    checks['added_labels_present'] = sorted(l for l in ADDED if new_c[l] == 0)
    unexpected_removed = [l for l in old_c if new_c[l] < old_c[l] and l not in REMOVED]
    unexpected_added = [l for l in new_c if new_c[l] > old_c[l] and l not in ADDED | MOVED]
    checks['unexpected_removed'] = unexpected_removed
    checks['unexpected_added'] = unexpected_added
    old_paths = {(l, d, t) for l, d, t in old if l not in REMOVED | MOVED}
    new_paths = {(l, d, t) for l, d, t in new_all}
    checks['unchanged_lettering_byte_identical'] = len(old_paths - new_paths) == 0
    checks['unchanged_lettering_count'] = len(old_paths)
    checks['footer_reference_labels_removed_from_front'] = not any(
        l in new_c for l in footer_labels if l and l not in ('References',))
    for needle in ('href="poster-a0-layout-v02-2026-10-04-background.png"',
                   'href="poster-draft-car-background-v09-art-2026-10-04.png"',
                   'href="poster-draft-car-background-v06-art-2026-10-04.png"'):
        checks[f'external_link_kept {needle[6:-1]}'] = front.count(needle) == src.count(needle)
    images_old = re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]{64})', src)
    images_new = re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]{64})', front)
    checks['embedded_images_unchanged'] = images_old == images_new
    checks['cloud_lecturer_title'] = 'Lecturer: Dr Luu Tien Thuan' in front and 'PhD' not in front.split('Lecturer:')[1][:20]
    checks['cloud_global_statement'] = 'All targets and pilots are group proposals' in front
    back_labels = [l for l, _, _ in labels(back)]
    refs = (Path(__file__).resolve().parent / f'{STEM}-references.md').read_text().split('\n## Entries\n', 1)[1]
    entries = [e for e in refs.strip().split('\n\n') if e.strip()]
    checks['back_reference_entries'] = len(entries)
    starts = [e.split(' (')[0] for e in entries]
    checks['back_entries_alphabetical'] = starts == sorted(starts, key=str.lower)
    joined = ''.join(back_labels)
    checks['back_all_entry_starts_lettered'] = all(s.split()[0] in joined for s in starts)
    arithmetic = {
        'paid_cac': round((108000 + 90000) / 1200, 2) == 165,
        'contribution_per_ride': round(227 * 0.30, 2) == 68.1,
        'cac_payback_rides': round(165 / 68.1, 2),
        'full_recovery_rides': -(-600000 // 68.1),
        'voucher_ceiling_unchanged': 400 * 30 == 12000,
        'budget_total_unchanged': 276000 + 108000 + 90000 + 43195 + 30000 + 12000 + 40805 == 600000,
        'n79_margin_pp': round(196 * (0.25 / 79) ** 0.5, 1),
        'standard_trip_green_sm': 39 + 10 * 11 + 12 * 6.5,
        'standard_trip_dantaxi': round(39 + 10 * 11.30 + 12 * 6.67, 2),
        'standard_trip_drivr': 42 + 10 * 11 + 12 * 7.5,
    }
    checks['arithmetic'] = arithmetic
    ok = (checks['removed_labels_gone'] and not checks['added_labels_present']
          and not unexpected_removed and not unexpected_added
          and checks['unchanged_lettering_byte_identical'] and checks['embedded_images_unchanged']
          and checks['cloud_lecturer_title'] and checks['back_entries_alphabetical']
          and checks['back_reference_entries'] == 19)
    checks['pass'] = ok
    checks['not_checked_here'] = [
        'car/harbour background PNGs are external and absent from the cloud session; previews omit them',
        'Chalkboard SE rendering of the cloud text (macOS font) — verify locally',
        'mba-presentation-style presentcheck.py on changed copy — run locally',
        'native Danish check of Elektrisk taxa. Tjek prisen. Book i appen.',
        'actual-size print legibility',
    ]
    (out_dir / f'{STEM}-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps(checks, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
