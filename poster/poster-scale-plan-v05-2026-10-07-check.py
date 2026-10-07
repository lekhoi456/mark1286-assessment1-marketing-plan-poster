"""Check proof v05 (D-164): v04 without the connecting arrows.

Runs the v04 checks on the v04 build, then confirms that the v05 front equals
the v04 front with only the connected-cells group (and title/description) removed.
Usage: python3 -B poster/poster-scale-plan-v05-2026-10-07-check.py SOURCE.svg OUT_DIR
(OUT_DIR must hold the v04 build outputs and the v05 front.)
"""
import contextlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v05-2026-10-07'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out_dir = Path(sys.argv[2])
    c4 = load('c4', 'poster-scale-plan-v04-2026-10-07-check.py')
    r5 = load('r5', 'poster-scale-plan-v05-2026-10-07-render.py')
    with contextlib.redirect_stdout(io.StringIO()):
        c4.main()
    v04_checks = json.loads((out_dir / f'{c4.STEM}-checks.json').read_text())
    v04 = (out_dir / f'{c4.STEM}.svg').read_text()
    v05 = (out_dir / f'{STEM}.svg').read_text()
    checks = {
        'v04_checks_pass': v04_checks['pass'],
        'v05_equals_v04_without_connectors': v05 == r5.strip_connectors(v04),
        'connector_groups_left': len(re.findall(r'id="(?:connected-cells-v01|link-\d+-\d+)"', v05)),
        'dashed_cyan_paths_left': len(re.findall(r'stroke="#28bdbf"[^>]*stroke-dasharray="3\.2 2\.4"', v05)),
        'bytes_removed': len(v04) - len(v05),
        'back_of_chart': 'unchanged: poster-scale-plan-v04-2026-10-07-back.*',
    }
    checks['pass'] = bool(checks['v04_checks_pass'] and checks['v05_equals_v04_without_connectors']
                          and not checks['connector_groups_left'] and not checks['dashed_cyan_paths_left'])
    checks['not_checked_here'] = v04_checks['not_checked_here'][:-1] + ['actual-size print legibility']
    (out_dir / f'{STEM}-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps(checks, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
