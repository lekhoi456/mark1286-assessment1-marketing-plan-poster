"""Build proof v04 (D-163): scaled DKK30M plan with connected cells.

Starts from the proof v03 build and applies the display copy in
10-sections-scale-copy-v46-2026-10-07.md. All figures come from
scale-plan-v01-2026-10-07-model.py. Lettering reuses the approved glyph
outlines; new shapes use the brand palette only.

Usage: python3 -B poster/poster-scale-plan-v04-2026-10-07-render.py SOURCE.svg OUT_DIR
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
r3 = load('r3', 'poster-content-upgrade-v03-2026-10-07-render.py')
MODEL = load('model', 'scale-plan-v01-2026-10-07-model.py')

STEM = 'poster-scale-plan-v04-2026-10-07'
INK, CYAN, YELLOW, WHITE = '#173a47', '#28bdbf', '#e3bb42', '#ffffff'
YELLOW30 = '#f7ebc6'


class Builder:
    def __init__(self, svg, glyph_source):
        self.svg = svg
        self.S = G.load(svg)
        supply = G.load(glyph_source)  # original v04 SVG keeps the footer glyphs (ø, &)
        self.body = G.Font(supply, ['Marketing AI reminders · human review'], any_skew=True)
        self.head = G.Font(supply, ['5. Digital Marketing Tactics'])
        # short strings the ratio filter skips but whose glyphs are needed
        for font, extras in ((self.body, ('460h × DKK600/h*',)),
                             (self.head, ('≤DKK165', '≥50%', '1,200', '2,500', '10% vs 20%', '+10 pp'))):
            for extra in extras:
                s = G.find(supply, extra)
                k, spread = font.measure(s)
                assert spread < 0.05, (extra, spread)
                font._add(s, k)
            font._fit()
        self.ed = v01.Editor(svg)
        self.log = []
        self.used = set()

    def sample(self, label, index=0):
        s = G.find(self.S, label, index)
        key = (label, index)
        assert key not in self.used, f'{label!r} edited twice'
        self.used.add(key)
        return s

    def font_of(self, s):
        if not s.glyphs:  # unclustered string: size from width ratio, heading font
            w1 = self.head.width(s.label, 1.0)
            return self.head, (s.x1 - s.x0) / w1
        for f in (self.body, self.head):
            try:
                k, spread = f.measure(s)
            except KeyError:
                continue
            if spread < 0.03:
                return f, k
        raise KeyError(f'no font for {s.label!r}')

    def compose(self, text, font, size, x, y, anchor='left', fill=INK):
        d, w = font.compose(text, size)
        left = x if anchor == 'left' else (x - w / 2 if anchor == 'centre' else x - w)
        return G.group(text, d, left, y, fill), w

    def rep(self, label, text, scale=1.0, x=None, y=None, anchor='left', font=None, index=0, fill=None, size=None):
        s = self.sample(label, index)
        f, k = self.font_of(s)
        f = font or f
        k = size if size is not None else k
        if x is None:
            x = {'left': s.left, 'centre': (s.left + s.right) / 2, 'right': s.right}[anchor]
        g, w = self.compose(text, f, k * scale, x, s.ty if y is None else y, anchor, fill or s.fill)
        self.ed.replace(s.match.start(), s.match.end(), g, f'{label!r} -> {text!r}')
        self.log.append({'from': label, 'to': text, 'width': round(w, 1)})
        return w

    def delete(self, label, index=0):
        s = self.sample(label, index)
        self.ed.replace(s.match.start(), s.match.end(), '', f'delete {label!r}')
        self.log.append({'from': label, 'to': None})

    def add_after(self, anchor_label, text, font, size, x, y, anchor='left', fill=INK, index=0):
        s = G.find(self.S, anchor_label, index)
        g, w = self.compose(text, font, size, x, y, anchor, fill)
        self.ed.replace(s.match.end(), s.match.end(), g, f'add {text!r}')
        self.log.append({'from': None, 'to': text, 'x': round(x, 1), 'y': y, 'width': round(w, 1)})
        return w

    def size(self, label, font=None):
        s = G.find(self.S, label)
        f, k = self.font_of(s)
        return k if font is None or font is f else font.measure(s)[0]

    def raw(self, old, new, note, count=1):
        i = self.svg.find(old)
        assert i >= 0, f'raw target not found: {note}'
        if count == 1:
            assert self.svg.find(old, i + 1) < 0, f'raw target not unique: {note}'
        self.ed.replace(i, i + len(old), new, note)
        self.log.append({'shape': note})

    def raw_re(self, pattern, new, note):
        m = re.search(pattern, self.svg, re.S)
        assert m, f'pattern not found: {note}'
        self.ed.replace(m.start(), m.end(), new, note)
        self.log.append({'shape': note})

    def insert_after_label(self, anchor_label, svg_fragment, note):
        s = G.find(self.S, anchor_label)
        self.ed.replace(s.match.end(), s.match.end(), svg_fragment, note)
        self.log.append({'shape': note})


def arrow(x1, y1, x2, y2, both=False):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)

    def head(x, y, a):
        l, w = 4.2, 2.6
        bx, by = x - l * math.cos(a), y - l * math.sin(a)
        px, py = -math.sin(a) * w, math.cos(a) * w
        return (f'<path d="M{x:.1f} {y:.1f}L{bx + px:.1f} {by + py:.1f}L{bx - px:.1f} {by - py:.1f}Z" '
                f'fill="{CYAN}"/>')
    sx, sy, ex, ey = x1, y1, x2, y2
    trim = 3.6
    ex2, ey2 = ex - trim * math.cos(ang), ey - trim * math.sin(ang)
    sx2, sy2 = (sx + trim * math.cos(ang), sy + trim * math.sin(ang)) if both else (sx, sy)
    out = (f'<path d="M{sx2:.1f} {sy2:.1f}L{ex2:.1f} {ey2:.1f}" fill="none" stroke="{CYAN}" '
           f'stroke-width="1.7" stroke-dasharray="3.2 2.4" stroke-linecap="round"/>' + head(ex, ey, ang))
    if both:
        out += head(sx, sy, ang + math.pi)
    return out


CONNECTORS = [  # (from, to, x1, y1, x2, y2, both)
    ('1', '2', 596, 286, 626, 286, False),
    ('2', '3', 896, 263, 927, 263, False),
    ('3', '4', 1246, 345, 1275, 345, False),
    ('1', '5', 572, 382, 572, 412, False),
    ('2', '6', 782, 384, 782, 412, False),
    ('5', '6', 600, 548, 630, 548, False),
    ('7', '8', 1163, 528, 1197, 528, True),
    ('6', '9', 826, 588, 826, 640, False),
    ('8', '10', 1322, 557, 1250, 618, False),
    ('9', '10', 846, 737, 884, 737, False),
]


def build(src):
    base, _, _ = r3.build(src)
    b = Builder(base, src)
    body, head = b.body, b.head
    M = MODEL.BUDGET

    # ---------- Section 1
    b.rep('Green SM Taxi: app-booked electric taxi rides in Copenhagen',
          'App-booked electric taxi rides · Denmark = 1st EU market', anchor='centre')

    # ---------- Section 2: focus title, segment ladder, evidenced profile
    b.rep('Copenhagen residents aged 25–44', 'Focus: Copenhagen residents aged 25–44')
    b.delete('Later: visitors · business accounts')
    b.delete('Within the service area')
    b.delete('Recurring trips → repeat rides')
    b.raw('<path d="M630 367Q630 364 633 364Q636 364 636 367Q636 370 633 373Q630 370 630 367Z" fill="#e3bb42" stroke="#173a47" stroke-width="0.55" stroke-linecap="round" stroke-linejoin="round"/>',
          '', 'Section 2 pin icon removed (service area folded into the focus line)')
    k_lad = b.size('Marketing AI reminders · human review')
    b.rep('Proposed rider profile', 'Rider profile', x=838, anchor='centre')
    rows = [('1  Focus: 25–44 · M1+', True), ('2  All adults · M1+', False),
            ('3  Business accounts · M4+', False), ('4  Visitors + airport · M6+', False)]
    lad = [f'<g id="section-02-segment-ladder-v01">']
    g, w = b.compose('4 segments', head, b.size('Copenhagen page', head) * 0.78, 632, 350.6)
    lad.append(g)
    for i, (t, focus) in enumerate(rows):
        y = 358.6 + i * 8.5
        if focus:
            gw = body.width(t, k_lad)
            lad.append(f'<rect x="629.8" y="{y - 5.9:.1f}" width="{gw + 5.5:.1f}" height="7.6" rx="2.8" fill="{YELLOW30}" stroke="{YELLOW}" stroke-width="0.6"/>')
        g, w = b.compose(t, body, k_lad, 632.5, y)
        lad.append(g)
    lad.append('</g>')
    b.insert_after_label('Rider profile' if False else 'Values trip control', ''.join(lad), 'Section 2 four-segment ladder')
    b.rep('Price-conscious', 'Price-conscious · 57%')
    b.rep('Expects fair treatment', 'Green by habit · 41%')

    # ---------- Section 3: positioning statement
    b.rep('Cleaner · Quieter · More reliable',
          'For green, fair-fare riders: 100% electric · one company runs app, car + driver')
    b.delete('Company promise')
    b.rep('Taxi partners operate rides', 'Partner operators · Uber + Dantaxi 40–50%')
    b.rep('Shared: App booking · Electric options · Similar fares (Dantaxi/Drivr)',
          'Parity: app booking · electric options · Dantaxi/Drivr fares', anchor='centre')
    b.rep('Proposed edge:', 'Edge:')

    # ---------- Section 4: campaign lockup
    b.rep('Danish first · English second', 'Campaign: Copenhagen, meet Green SM', y=375.5, anchor='centre',
          font=head, size=b.size('Modern Liquid Glass UI/UX'))
    k4 = b.size('Layered · soft · clear')
    b.add_after('Layered · soft · clear', 'Danish first: København, mød Green SM', body, k4, 1402, 385.0, anchor='centre')

    # ---------- Section 5
    b.rep('40–50%', '70–90%')
    b.rep('one app', '0–1 taxi apps')
    b.raw('<path d="M350 456H388.8" stroke="#28bdbf" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
          '<path d="M350 456H417.9" stroke="#28bdbf" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
          'Section 5 bar to 70%')
    b.raw('<path d="M388.8 456H398.5" stroke="#28bdbf" stroke-width="3" stroke-dasharray="1 1"/>',
          '<path d="M417.9 456H437.3" stroke="#28bdbf" stroke-width="3" stroke-dasharray="1 1"/>', 'Section 5 range to 90%')
    b.rep('Search / social', 'Channel plan →')
    b.delete('/ reminders')
    b.rep('Omni Channel · Search / SEO / Social', 'Omnichannel: page → app → ride')
    b.delete('/ Content')
    b.delete('Ride + help')
    b.raw_re(r'<g id="section-05-electric-taxi-picture">.*?</g>', '', 'Section 5 taxi illustration removed (continues into Section 6)')
    b.raw('<path d="M481 508 L492 508 M489 506 L492 508 L489 510" stroke="#28bdbf" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
          '', 'Section 5 phone-to-taxi arrow removed')
    kt = b.size('Marketing AI reminders · human review')
    tab = ['<g id="section-05-channel-plan-v01">',
           f'<rect x="481" y="481.5" width="124" height="61" rx="3" fill="#eaf8f9" stroke="#7ed7d9" stroke-width="0.7"/>']
    g, _ = b.compose('Channel → KPI', head, b.size('Copenhagen page', head) * 0.78, 485, 490.0)
    tab.append(g)
    for i, t in enumerate(['Search: bestil taxa → installs', 'Social: Instagram · Facebook → CTR',
                           'City screens + video → awareness', 'Content: Copenhagen page → visits',
                           'CRM: reminders · referral → repeat']):
        g, w = b.compose(t, body, kt * 1.02, 485, 499.6 + i * 9.6)
        tab.append(g)
    tab.append('</g>')
    b.insert_after_label('Same fares / offers / help', ''.join(tab), 'Section 5 channel → KPI table')
    b.rep('Post-launch · 400 riders · 1 each', '1 per rider · ≤DKK30')
    b.delete('30-day paid')
    b.delete('30')
    b.raw('<path d="M440 553H463V572H440Z M440 558H463 M445 551V556 M458 551V556" stroke="#173a47" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
          '', 'Section 5 pass calendar removed')
    b.raw('<rect x="474" y="554" width="130" height="29" rx="3" fill="#eaf8f9" stroke="#7ed7d9" stroke-width=".75"/>',
          f'<rect x="440" y="553" width="164" height="30" rx="3" fill="{YELLOW30}" stroke="{YELLOW}" stroke-width=".75"/>',
          'Section 5 launch-campaign box')
    b.rep('DATA', 'LAUNCH CAMPAIGN', x=445)
    b.delete('Opt-in')
    b.rep('CDP join → Big Data patterns', 'Copenhagen, meet Green SM', x=445)
    b.rep('Marketing AI reminders · human review', 'city screens · video · social · search', x=445)
    b.rep('M1–2 Verify', 'M1–3 Test', anchor='centre')
    b.rep('M3–6 Test · M4/M6 checks', 'M4 / M6 gates', anchor='centre')

    # ---------- Section 6
    b.rep('Search/social → leads', 'Campaign · search · social → lead')
    b.delete('· CTR, CPC')
    b.rep('Fare check → prospect', 'Fare check → app install')
    b.delete('· app installs')
    b.rep('App booking → completed trip', 'Book now or pre-book 30 days')
    b.delete('· conversion')
    b.rep('First-ride voucher', 'First-ride offer DKK15/30')
    b.rep('Check app · driver · car · care', 'One standard: app · driver · car · care')
    b.rep('Post-ride feedback + rating', 'Rating → fix issues')
    b.rep('Unpaid review: well-rated/resolved', 'Invite unpaid reviews')
    b.rep('Opt-in reminders + voucher pilots', 'Reminders · referral credit')
    b.rep('Tailored monthly paid bundle pilots', 'Commuter pass test')
    k6 = b.size('Marketing AI reminders · human review')
    b.add_after('Tailored monthly paid bundle pilots', 'Channels: app · B2B via LinkedIn (M4+) · partners (M6+)', body, k6, 638, 590.5)

    # ---------- Section 7
    b.rep('Proposed DKK600,000', 'Proposed DKK30.0M')
    b.rep('Local delivery first · Search/social drive trial', 'Objective-and-task · about 6% of base revenue*')
    labels = ['Team', 'Search', 'Social', 'Screens', 'Tools', 'Vouchers', 'Contingency']
    values = ['276,000 / 46%', '108,000 / 18%', '90,000 / 15%', '43,195 / 7.2%', '30,000 / 5%', '12,000 / 2%', '40,805 / 6.8%']
    new_labels = ['Search + app', 'Social', 'Screens/video', 'Incentives', 'Team/creative', 'B2B sales', 'CRM/research', 'Contingency']
    shares = MODEL.main.__globals__['BUDGET']
    pct = {k: round(v / 30.0 * 100) for k, v in shares}
    new_values = [f'{v:.1f}M / {pct[k]}%' for k, v in shares]
    for old, new in zip(labels, new_labels[:7]):
        b.rep(old, new)
    k_lab = b.size('Social')
    k_val = b.size('90,000 / 15%')
    for old, new in zip(values, new_values[:7]):
        b.rep(old, new, font=body, size=k_val)
    b.add_after('Contingency', new_labels[7], body, k_lab, 866, 542)
    b.add_after('Contingency', new_values[7], body, k_val, 996, 542)
    b.delete('400 riders')
    # bars: replace the seven fill paths and add an eighth row; scale 0-8M over 65 units
    old_fill = re.findall(r'<path d="M925 (\d+\.5)H([\d.]+)V(\d+\.5)H925Z" fill="(#28bdbf|#e3bb42)" stroke="#173a47" stroke-width="0.65" stroke-linecap="round" stroke-linejoin="round"/>', base)
    assert len(old_fill) == 7, old_fill
    for (y0, x1, y1, col), (_, v) in zip(old_fill, shares[:7]):
        old = f'<path d="M925 {y0}H{x1}V{y1}H925Z" fill="{col}" stroke="#173a47" stroke-width="0.65" stroke-linecap="round" stroke-linejoin="round"/>'
        b.raw(old, f'<path d="M925 {y0}H{925 + v / 8 * 65:.2f}V{y1}H925Z" fill="{col}" stroke="#173a47" stroke-width="0.65" stroke-linecap="round" stroke-linejoin="round"/>',
              f'bar {y0}')
    v8 = shares[7][1]
    row8 = (f'<path d="M925 534.5H990V543.5H925Z" fill="#ffffff" stroke="#173a47" stroke-width="0.65" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M925 534.5H{925 + v8 / 8 * 65:.2f}V543.5H925Z" fill="#e3bb42" stroke="#173a47" stroke-width="0.65" stroke-linecap="round" stroke-linejoin="round"/>')
    b.insert_after_label('Contingency', row8, 'bar row 8')
    b.delete('Unit check: DKK165 CAC repaid in about 2.4 rides')
    b.rep('at an assumed DKK68 contribution per ride', '*Base case, assumed: 450 cars × 15 trips/day × DKK200', y=553.0)
    b.rep('460h × DKK600/h*', 'People')
    b.rep('Checks', 'Analytics')
    b.rep('60h', 'CRM tools', anchor='centre')
    b.rep('Creative/', 'Creative', anchor='centre')
    b.rep('localisation', '+ agency', anchor='centre')
    b.delete('120h', 0)
    b.rep('160h', '3 FTE', anchor='centre')
    b.rep('CRM/help', 'B2B sales', anchor='centre')
    b.rep('120h', '2 FTE', anchor='centre', index=1)
    b.delete('*Planning allowance')
    b.rep('Budget reviews · cumulative commitments', 'Budget reviews · cumulative caps')
    b.rep('DKK177,000', 'DKK7.5M')
    b.rep('DKK265,000', 'DKK13.5M')
    b.rep('Remaining DKK335,000', 'DKK16.5M', anchor='right')
    b.delete('M6: 265,000 + 335,000 = 600,000')

    # ---------- Section 8
    b.rep('Consideration survey:', 'Awareness survey:')
    b.rep('+10 pp', '≥50%')
    b.rep('Consideration', 'Aided awareness')
    b.rep('1,200', '150,000', anchor='centre', scale=0.84)
    b.rep('Distinct first paid', 'First paid')
    b.rep('riders*', 'riders')
    b.rep('2,500', '2.5M', anchor='centre')
    b.rep('Paid rides*', 'Paid trips', y=474.0)
    b.add_after('Paid trips' if False else '90-day repeat†', '15/car/day average', body, b.size('Cost / first'), 1330.2, 484.0)
    b.rep('≤DKK165', '≤DKK100', anchor='centre')
    b.rep('Cost / first', 'Media CAC per')
    b.rep('paid rider*', 'first rider')
    b.rep('*Paid-campaign riders only, not all Green SM trips', 'Media CAC = (search + social) / first paid riders')
    b.rep('≥200 first paid riders', '≥25,000 first paid riders')
    b.rep('Both counts cumulative', 'Media CAC ≤DKK120')
    b.rep('≥450 first paid riders', '≥55,000 first paid riders')
    b.rep('≤DKK175 paid acquisition', '≥10 trips per car per day')
    b.rep('BRAND UPSIDE', 'B2B')
    b.raw_re(r'(<g transform="translate\(1433 514\) scale\(0\.7\)">)\s*<path d="M-5 5Q-8-5 5-5Q8 5-5 5Z"[^>]*/>\s*<path d="M-6 7L3-3"[^>]*/>',
             '<g transform="translate(1433 514) scale(0.7)"><path d="M-6-2H6V6H-6Z" fill="#28bdbf" stroke="#173a47" stroke-width="0.8" stroke-linejoin="round"/>'
             '<path d="M-2.5-2V-4.5H2.5V-2 M-6 1.5H6" fill="none" stroke="#173a47" stroke-width="0.7" stroke-linecap="round" stroke-linejoin="round"/>',
             'Section 8 B2B briefcase icon replaces the brand-upside leaf')
    b.rep('Organic · referrals ·', '≥100 business')
    b.rep('extra rides', 'accounts by M12')
    b.delete('Track separately')
    b.rep('Ads + trips + dispatch/help', 'Ads → app → trips → help')

    # ---------- Section 9
    b.rep('Consented first-party data', 'Weather + night triggers')
    b.rep('Big Data + AI', 'Consented app data')
    b.rep('Relevant reminders', 'Timed offers')
    b.rep('Match time · Fulfilment', 'Wait time · fulfilment')
    b.rep('Needs-matched prepaid/monthly', 'commuter monthly pass')
    b.rep('Unpriced dispatch/chatbot/subscription: cost separately', 'Unpriced pilots: cost separately')
    b.rep('Neuro cue test: calm-ride vs fare-first ads → attention (CTR) · recall (survey)',
          'Neuro test: calm-ride vs fare-first ads → attention · recall')

    # ---------- Section 10
    b.rep('Service + 90-day repeat → scale', 'Service gates before scale')
    b.rep('Search / social → paid trial', 'Copenhagen, meet Green SM')
    b.rep('Screens after service +', '≥50% aided awareness')
    b.delete('90-day repeat checks')
    b.rep('App-booked electric rides', '100% electric app-booked rides')
    b.rep('Retention + contribution', 'Repeat + trips per car')
    b.rep('Repeat before expansion', 'Scale only through M4/M6 gates')
    b.rep('Consideration · paid trial · service · 90-day repeat · contribution',
          'awareness · riders · trips/car · repeat · CAC')
    b.rep('Entry investment · first-year break-even not required', 'Entry investment: about 6% of base revenue')

    # ---------- connectors (inside the car group, after the last cell)
    conn = ['<g id="connected-cells-v01" aria-label="Cyan dashed arrows linking related cells">']
    for f, t, x1, y1, x2, y2, both in CONNECTORS:
        conn.append(f'<g id="link-{f}-{t}">' + arrow(x1, y1, x2, y2, both) + '</g>')
    conn.append('</g>')
    i_car, j_car = r3.group_span(base, 'proportional-car-placement')
    b.ed.replace(j_car - 4, j_car - 4, ''.join(conn), 'connectors before the car layer closes')
    b.log.append({'shape': 'connectors'})

    out = b.ed.apply()
    out = re.sub(r'<title>[^<]*</title>', '<title>Copenhagen meet Green SM — scaled plan proof v04</title>', out, count=1)
    out = re.sub(r'<desc>[^<]*</desc>', '<desc>A0 landscape marketing-plan poster, D-163 proof v04: scaled DKK30M gated market-entry plan, four segments with 25–44 as focus, campaign Copenhagen, meet Green SM with Go Green / For a Green Future., and cyan dashed arrows linking related cells. Lettering reuses the approved glyph outlines. Awaits student review.</desc>', out, count=1)
    return out, b.log


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out, log = build(source.read_text())
    (out_dir / f'{STEM}.svg').write_text(out)
    # back of chart: 21 references in the approved lettering
    src = source.read_text()
    supply = G.load(src)
    body = G.Font(supply, ['*Paid campaign cohort only', 'Max DKK30 · 400 cap · 1/rider', 'Cost pilots separately'],
                  any_skew=True)
    head = G.Font(supply, ['5. Digital Marketing Tactics'])
    a, ka = body.best('a')
    body.synth('æ', [('a', 0, 0, 1, 1), ('e', a.w / ka * 0.62, 0, 1, 1)], spacing_like=('a', 'e'))
    v01.wrap.font = body
    refs = (HERE / f'{STEM}-references.md').read_text().split('\n## Entries\n', 1)[1]
    entries = [e.strip() for e in refs.strip().split('\n\n') if e.strip()]
    back, sz = v01.build_back(src, body, head, entries)
    (out_dir / f'{STEM}-back.svg').write_text(back)
    print('back entries', len(entries), 'lettering size', round(sz, 2))
    (out_dir / f'{STEM}-changes.json').write_text(json.dumps({'source': source.name, 'base': 'proof v03 build',
                                                              'copy': '10-sections-scale-copy-v46-2026-10-07.md',
                                                              'changes': log}, ensure_ascii=False, indent=1))
    print(len(log), 'changes')


if __name__ == '__main__':
    main()
