"""Controlled lettering and a connected growth path for Section 10 v03."""
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('section10_v03_base', HERE / '10-v02-layout.py')
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

INK, CYAN, GOLD, PAPER = BASE.INK, BASE.CYAN, BASE.GOLD, BASE.PAPER


class Layout(BASE.Layout):
    def __init__(self, width, height, glyph_script):
        super().__init__(width, height, glyph_script)
        self.parts[1] = '<title>10. Business Goals &amp; Growth</title>'
        self.parts[2] = ('<desc>A visual strategy chain connects Green SM strengths to local consideration, '
                         'paid trial, stable service, repeat use and a gated M12 growth decision.</desc>')

    def line(self, d, colour=INK, width=5, fill='none', extra=''):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" '
                          f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')

    def station_icon(self, kind, cx, cy):
        if kind == 'consideration':
            self.line(f'M{cx-37} {cy} Q{cx} {cy-39} {cx+37} {cy} Q{cx} {cy+39} {cx-37} {cy}Z', width=4)
            self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{CYAN}" stroke="{INK}" stroke-width="4"/>')
            self.line(f'M{cx-52} {cy-42} l-12 -12 M{cx+52} {cy-42} l12 -12', colour=GOLD, width=7)
        elif kind == 'trial':
            self.line(f'M{cx-27} {cy-39} Q{cx-33} {cy-42} {cx-33} {cy-30} L{cx-33} {cy+30} '
                      f'Q{cx-32} {cy+41} {cx-20} {cy+38} L{cx+22} {cy+38} '
                      f'Q{cx+33} {cy+39} {cx+33} {cy+27} L{cx+33} {cy-31} '
                      f'Q{cx+32} {cy-40} {cx+21} {cy-38} Z', width=4, fill='#fffdf5')
            self.line(f'M{cx-12} {cy+1} l9 10 l19 -24', colour=CYAN, width=7)
            self.line(f'M{cx-9} {cy-24} L{cx+10} {cy-24}', colour=GOLD, width=5)
        elif kind == 'service':
            self.line(f'M{cx-40} {cy+17} L{cx-30} {cy-8} Q{cx-27} {cy-15} {cx-18} {cy-15} '
                      f'L{cx+21} {cy-15} Q{cx+29} {cy-13} {cx+34} {cy+2} L{cx+41} {cy+10} '
                      f'L{cx+41} {cy+24} L{cx-40} {cy+24} Z', width=4, fill='#dff7f4')
            self.parts.extend([f'<circle cx="{cx-22}" cy="{cy+26}" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>',
                               f'<circle cx="{cx+24}" cy="{cy+26}" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'])
            self.line(f'M{cx+7} {cy-48} l10 10 l20 -23', colour=CYAN, width=7)
        else:
            self.line(f'M{cx+36} {cy-10} A40 40 0 0 0 {cx-25} {cy-26}', colour=CYAN, width=7)
            self.line(f'M{cx-25} {cy-26} l2 -18 l17 8', colour=CYAN, width=7)
            self.line(f'M{cx-36} {cy+10} A40 40 0 0 0 {cx+25} {cy+26}', colour=GOLD, width=7)
            self.line(f'M{cx+25} {cy+26} l-2 18 l-17 -8', colour=GOLD, width=7)
