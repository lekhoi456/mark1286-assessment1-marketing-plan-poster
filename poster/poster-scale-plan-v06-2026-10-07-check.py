"""Check proof v06 (D-165): v05 without the cloud line on group proposals.

Runs the v05 checks, then confirms that v06 equals the v05 front with only that
cloud line removed, the seven remaining cloud lines moved down 2 units, and the
SVG title/description updated.
Usage: python3 -B poster/poster-scale-plan-v06-2026-10-07-check.py SOURCE.svg OUT_DIR
(OUT_DIR must hold the v04 build outputs and the v05 and v06 fronts.)
"""
import contextlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v06-2026-10-07'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out_dir = Path(sys.argv[2])
    c5 = load('c5', 'poster-scale-plan-v05-2026-10-07-check.py')
    r6 = load('r6', 'poster-scale-plan-v06-2026-10-07-render.py')
    with contextlib.redirect_stdout(io.StringIO()):
        c5.main()
    v05_checks = json.loads((out_dir / f'{c5.STEM}-checks.json').read_text())
    v05 = (out_dir / f'{c5.STEM}.svg').read_text()
    v06 = (out_dir / f'{STEM}.svg').read_text()
    cloud = re.findall(r'<text x="1387" y="([\d.]+)"[^>]*>([^<]*)</text>', v06)
    checks = {
        'v05_checks_pass': v05_checks['pass'],
        'v06_equals_v05_with_line_dropped': v06 == r6.drop_cloud_line(v05),
        'group_proposals_line_absent': 'All targets and pilots are group proposals' not in v06,
        'cloud_lines': [t for _, t in cloud],
        'cloud_baselines': [float(y) for y, _ in cloud],
    }
    checks['pass'] = bool(checks['v05_checks_pass'] and checks['v06_equals_v05_with_line_dropped']
                          and checks['group_proposals_line_absent'] and len(cloud) == 7)
    checks['not_checked_here'] = v05_checks['not_checked_here']
    (out_dir / f'{STEM}-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps(checks, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
