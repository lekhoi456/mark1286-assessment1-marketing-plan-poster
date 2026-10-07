"""Build content-upgrade proof v03 (D-160): visual pass on proof v02.

1. Colour harmonisation: off-palette vector colours in the ten cells, cell
   outlines and identity cloud map to Cyan #28bdbf, Yellow #e3bb42, their
   white tints, white or the single ink #173a47. National flags, the Vingroup
   emblem, the VinFast wordmark, logos and raster artwork are not touched.
2. De-cluttering: lines that only repeat information shown elsewhere go.
3. Section 5 search example: the keyword moves into a full-size search box so
   it is no smaller than the poster's existing smallest lettering.

Usage: python3 -B poster/poster-content-upgrade-v03-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = load('glyphs', 'glyph-reuse-lettering.py')
v01 = load('v01', 'poster-content-upgrade-v01-2026-10-07-render.py')
v02 = load('v02', 'poster-content-upgrade-v02-2026-10-07-render.py')

STEM = 'poster-content-upgrade-v03-2026-10-07'
INK = '#173a47'
CYAN = (0x28, 0xbd, 0xbf)
YELLOW = (0xe3, 0xbb, 0x42)


def tint(rgb, t):
    return '#' + ''.join(f'{round(255 - (255 - c) * t):02x}' for c in rgb)


# old colour -> (new colour, role); every key occurs only in cells/cloud (audited)
COLOUR_MAP = {
    '#11354a': (INK, 'cell outlines -> single ink'),
    '#092b50': (INK, 'cloud outer outline -> single ink'),
    '#26c6cf': ('#28bdbf', 'cloud inner outline -> brand cyan'),
    '#dfeceb': (tint(CYAN, 0.15), 'Section 2 comparison bars -> cyan 15%'),
    '#fdfbef': ('#ffffff', 'Section 3 cream fill -> white'),
    '#e9f7f5': (tint(CYAN, 0.10), 'Section 4 panel -> cyan 10%'),
    '#d8e7e2': (tint(CYAN, 0.20), 'Section 5 bar tracks -> cyan 20%'),
    '#b8d9d6': (tint(CYAN, 0.40), 'Section 5 divider -> cyan 40%'),
    '#e9f8f5': (tint(CYAN, 0.10), 'Section 5 timeline boxes -> cyan 10%'),
    '#edf8f5': (tint(CYAN, 0.10), 'Section 5 DATA box -> cyan 10%'),
    '#8cc7c3': (tint(CYAN, 0.60), 'Section 5 DATA outline -> cyan 60%'),
    '#fff4b9': (tint(YELLOW, 0.30), 'Section 5 test-phase box -> yellow 30%'),
}

DELETE = [
    '*Test frequency + unit economics',   # Section 9 shows frequency/contribution tests
    'Cost pilots separately',             # Section 9: Unpriced ...: cost separately
    'Proposed 12-month plan',             # cloud: All targets and pilots are group proposals
    'Local outcomes untested',            # Section 9 header: Local performance untested
    'Repeat: full 90-day follow-up',      # Section 8 defines full 90-day cohorts
]
DROP_ASTERISK = ['Opt-in reminders + voucher pilots*', 'Tailored monthly paid bundle pilots*']
S10_BOX = ['<path d="M1014 631H1206V644H1014Z" fill="#ffffff" stroke="#e3bb42" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
           '<path d="M1102 634V641" fill="none" stroke="#e3bb42" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round"/>']


def group_span(svg, group_id):
    i = svg.find(f'<g id="{group_id}"')
    depth = 0
    for m in re.finditer(r'<g\b|</g>', svg[i:]):
        depth += 1 if m.group() != '</g>' else -1
        if depth == 0:
            return i, i + m.end()
    raise ValueError(group_id)


def build(src):
    front, _, _, _ = v01.build_front(src)
    front = v02.strip_group(front, 'member-contributions-strip-v01')
    S = G.load(front)
    body = G.Font(S, ['Cost pilots separately', 'Marketing AI reminders · human review'], any_skew=True)
    head = G.Font(S, ['5. Digital Marketing Tactics'])
    ed = v01.Editor(front)
    log = []
    for label in DELETE:
        s = G.find(S, label)
        ed.replace(s.match.start(), s.match.end(), '', f'delete {label!r}')
        log.append({'from': label, 'to': None})
    for label in DROP_ASTERISK:
        s = G.find(S, label)
        new = label[:-1]
        ed.replace(s.match.start(), s.match.end(),
                   G.group(new, G.subset(s, 0, len(s.glyphs) - 1), s.tx, s.ty, s.fill), f'{label!r} -> {new!r}')
        log.append({'from': label, 'to': new, 'method': 'original glyphs kept'})
    for el in S10_BOX:
        i = front.find(el)
        assert i >= 0, el
        ed.replace(i, i + len(el), '', 'delete Section 10 proposal/untested box')
    log.append({'from': 'Section 10 header box', 'to': None})

    # Section 5 search example at a legible size
    i, j = group_span(front, 'section-05-danish-example-ad-v01')
    ref_body = G.find(S, 'Same fares / offers / help')
    ref_head = G.find(S, 'Copenhagen page')
    bk = v01.size_in(body, ref_body)
    hk = v01.size_in(head, ref_head)
    parts = ['<g id="section-05-danish-example-ad-v02" stroke="none">',
             '<rect x="353.5" y="494.6" width="65" height="7.2" rx="3.2" fill="#ffffff" stroke="#28bdbf" stroke-width="0.7"/>',
             f'<circle cx="358.2" cy="497.9" r="1.6" fill="none" stroke="{INK}" stroke-width="0.5"/>',
             f'<path d="M359.35 499.05L360.6 500.3" stroke="{INK}" stroke-width="0.6" stroke-linecap="round"/>']
    d, w = body.compose('bestil taxa', bk * 0.92)
    parts.append(G.group('bestil taxa', d, 362.6, 500.4, INK))
    d, w = head.compose('Elektrisk taxa', hk * 0.9)
    parts.append(G.group('Elektrisk taxa', d, 386 - w / 2, 509.6, INK))
    for text, y in (('Tjek prisen.', 517.4), ('Book i appen.', 524.9)):
        d, w = body.compose(text, bk * 0.98)
        parts.append(G.group(text, d, 386 - w / 2, y, INK))
    parts.append('</g>')
    ed.replace(i, j, ''.join(parts), 'Section 5 search example v02')
    log.append({'from': 'search field in browser bar (1.5 mm x-height)',
                'to': 'full-width search box bestil taxa (about 2.1 mm x-height) above the Danish ad'})

    out = ed.apply()
    applied = {}
    for old, (new, role) in COLOUR_MAP.items():
        n = len(re.findall(re.escape(old), out, re.I))
        out = re.sub(re.escape(old), new, out, flags=re.I)
        applied[old] = {'to': new, 'role': role, 'occurrences': n}
    out = re.sub(r'<title>[^<]*</title>',
                 '<title>Copenhagen meet Green SM — content upgrade proof v03</title>', out, count=1)
    out = re.sub(r'<desc>[^<]*</desc>',
                 '<desc>A0 landscape marketing-plan poster, D-160 proof v03: proof v02 with vector colours harmonised to Cyan #28bdbf and Yellow #e3bb42 (tints, white and one ink), repeated lines removed and a legible Section 5 search example. Flags, logos and raster artwork unchanged. Awaits student review.</desc>',
                 out, count=1)
    return out, log, applied


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out, log, applied = build(source.read_text())
    (out_dir / f'{STEM}.svg').write_text(out)
    report = {'source': source.name, 'front': f'{STEM}.svg',
              'back': 'poster-content-upgrade-v01-2026-10-07-back.svg (unchanged)',
              'base': 'proof v02 (D-159)', 'visual_pass': log, 'colour_map': applied}
    (out_dir / f'{STEM}-changes.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps(applied, ensure_ascii=False, indent=1))
    print(len(log), 'visual-pass edits')


if __name__ == '__main__':
    main()
