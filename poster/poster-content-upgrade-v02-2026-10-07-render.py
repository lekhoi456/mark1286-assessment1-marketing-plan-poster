"""Build content-upgrade proof v02 (D-159) from poster-references-v04-2026-10-07.svg.

v02 = v01 front without the member-contributions strip and its white band:
the lecturer says no contribution statement is needed, so the area below the
car returns to the approved background art. Every other v01 edit is kept.
The back of chart is unchanged: use poster-content-upgrade-v01-2026-10-07-back.*

Usage: python3 -B poster/poster-content-upgrade-v02-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('v01', HERE / 'poster-content-upgrade-v01-2026-10-07-render.py')
v01 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v01)

STEM = 'poster-content-upgrade-v02-2026-10-07'


def strip_group(svg, group_id):
    i = svg.find(f'<g id="{group_id}"')
    if i < 0:
        raise ValueError(f'{group_id} not found')
    depth = 0
    for m in re.finditer(r'<g\b|</g>', svg[i:]):
        depth += 1 if m.group() != '</g>' else -1
        if depth == 0:
            return svg[:i] + svg[i + m.end():]
    raise ValueError(f'{group_id} not closed')


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    front, changes, _, _ = v01.build_front(source.read_text())
    front = strip_group(front, 'member-contributions-strip-v01')
    front = re.sub(r'<title>[^<]*</title>',
                   '<title>Copenhagen meet Green SM — content upgrade proof v02</title>', front, count=1)
    front = re.sub(r'<desc>[^<]*</desc>',
                   '<desc>A0 landscape marketing-plan poster, D-159 content-upgrade proof v02. Label-level edits inside the ten existing cells; identity cloud uses Dr and one global proposal statement; References are on the back of the chart; no member-contribution strip (lecturer guidance LG-005), so the approved background shows below the car. Lettering reuses the approved glyph outlines. Awaits student review.</desc>',
                   front, count=1)
    (out_dir / f'{STEM}.svg').write_text(front)
    changes = [c for c in changes if 'Member contributions' not in str(c.get('to'))]
    changes.append({'from': 'Harvard References footer (17 sources)',
                    'to': 'removed from the front; References on the back (v01 back unchanged); approved background shows below the car'})
    report = {'source': source.name, 'front': f'{STEM}.svg',
              'back': 'poster-content-upgrade-v01-2026-10-07-back.svg (unchanged)',
              'difference_from_v01': 'member-contributions strip and its white band removed (D-159, LG-005)',
              'changes': changes}
    (out_dir / f'{STEM}-changes.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(len(changes), 'changes;', report['difference_from_v01'])


if __name__ == '__main__':
    main()
