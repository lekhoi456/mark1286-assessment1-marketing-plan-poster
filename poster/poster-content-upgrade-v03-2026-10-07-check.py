"""Check content-upgrade proof v03 (D-160) against the v04 source SVG.

Runs the v02 checks with the v03 label expectations, then adds palette checks.
Usage: python3 -B poster/poster-content-upgrade-v03-2026-10-07-check.py SOURCE.svg OUT_DIR
"""
import contextlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('c2', HERE / 'poster-content-upgrade-v02-2026-10-07-check.py')
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
spec = importlib.util.spec_from_file_location('r3', HERE / 'poster-content-upgrade-v03-2026-10-07-render.py')
r3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r3)

STEM = 'poster-content-upgrade-v03-2026-10-07'
c2.STEM = STEM
c2.REMOVED |= {'*Test frequency + unit economics', 'Cost pilots separately', 'Proposed 12-month plan',
               'Local outcomes untested', 'Repeat: full 90-day follow-up',
               'Opt-in reminders + voucher pilots*', 'Tailored monthly paid bundle pilots*'}
c2.ADDED |= {'Opt-in reminders + voucher pilots', 'Tailored monthly paid bundle pilots'}

# national flags (Section 1), Vingroup emblem, VinFast wordmark/flag outlines: kept by design
PROTECTED = {'#000080', '#002868', '#0038a8', '#00afca', '#138808', '#143b4a', '#21468b', '#ae1c28',
             '#c8102e', '#ce1126', '#da251d', '#e32823', '#f8eb00', '#fcd116', '#fec50c', '#ff9933',
             '#fffdf4', '#ffff00'}
ALLOWED_CELL_COLOURS = {'#28bdbf', '#e3bb42', '#173a47', '#ffffff', '#eefafa'} | {
    new for new, _ in r3.COLOUR_MAP.values()}


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        c2.main()
    out_dir = Path(sys.argv[2])
    path = out_dir / f'{STEM}-checks.json'
    checks = json.loads(path.read_text())
    front = (out_dir / f'{STEM}.svg').read_text()
    body = re.sub(r'data:image/[^"]+', '', front)
    checks['old_off_palette_colours_remaining'] = sorted(
        c for c in r3.COLOUR_MAP if re.search(re.escape(c), body, re.I))
    cells = ''
    for gid in ['section-01-v07-candidate', 'section-02-v04-candidate', 'section-03-v07-candidate',
                'section-04-v03-candidate', 'section-05-v05-candidate', 'section-06-v04-candidate',
                'section-07-v04-candidate', 'section-08-v02-candidate', 'section-09-v02-candidate',
                'section-10-v02-candidate']:
        i = body.find(f'id="{gid}"')
        j = body.find('<g id="section-', i + 10)
        cells += body[i:j if j > 0 else None]
    for flagged in ('fit01-flag-', 'fit01-vinfast', 'fit01-background-vingroup', 'drawn-path'):
        cells = re.sub(rf'<(?:g|svg|path) id="{flagged}[^"]*".*?</(?:g|svg)>|<path id="{flagged}[^"]*"[^>]*/>', '', cells, flags=re.S)
    used = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}\b', cells)}
    checks['protected_flag_logo_colours'] = sorted(used & PROTECTED)
    checks['cell_colours_outside_palette_unprotected'] = sorted(used - ALLOWED_CELL_COLOURS - PROTECTED)
    checks['pass'] = bool(checks['pass'] and not checks['old_off_palette_colours_remaining']
                          and not checks['cell_colours_outside_palette_unprotected'])
    checks['palette'] = sorted(ALLOWED_CELL_COLOURS)
    path.write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in checks.items() if k not in ('arithmetic', 'not_checked_here')},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
