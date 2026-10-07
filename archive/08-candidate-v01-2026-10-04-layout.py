"""Controlled native handwriting and slightly uneven pen frames for Section 8."""
from html import escape
from pathlib import Path
import json
import subprocess

INK, CYAN, GOLD, PAPER = '#173a47', '#26c6cf', '#ffd400', '#fffdf5'

class Layout:
    def __init__(self, width, height, glyph_script):
        self.width, self.height = width, height
        self.process = subprocess.Popen(['/usr/bin/swift', str(glyph_script)], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.cache, self.texts, self.frames = {}, [], []
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<title>8. Success Dashboard</title>',
            '<desc>Proposed targets and controls, with tracking tools, review rhythms and separate scale gates. Not achieved results.</desc>',
            f'<rect width="{width}" height="{height}" fill="{PAPER}"/>']

    def glyph(self, value, size, font):
        key = value, size, font
        if key not in self.cache:
            self.process.stdin.write(json.dumps({'text': value, 'font': font, 'size': size}) + '\n')
            self.process.stdin.flush()
            response = json.loads(self.process.stdout.readline())
            assert 'error' not in response, response
            assert response['resolved_font'] == font
            assert all(f in [font, 'controlled-arrow-vector'] for f in response['run_fonts']), response['run_fonts']
            self.cache[key] = response
        return self.cache[key]

    def wrap(self, value, size, font, width):
        lines, line = [], ''
        for word in value.split():
            candidate = (line + ' ' + word).strip()
            if line and self.glyph(candidate, size, font)['width'] > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        return lines + ([line] if line else [])

    def text(self, value, x, baseline, size=34, font='Noteworthy-Light', width=None, role='display', owner=None):
        lines = self.wrap(value, size, font, width) if width else [value]
        identifier, boxes = f'text-{len(self.texts):03d}', []
        self.parts.append(f'<g id="{identifier}" aria-label="{escape(value, quote=True)}" data-role="{role}">')
        for i, line in enumerate(lines):
            y = baseline + i * size * 1.28
            g = self.glyph(line, size, font)
            self.parts.append(f'<path d="{g["path"]}" transform="translate({x:.3f} {y:.3f}) scale(1 -1)" fill="{INK}"/>')
            left, bottom, right, top = g['bounds']
            boxes.append({'text': line, 'bbox': [x + left, y - top, x + right, y - bottom]})
        self.parts.append('</g>')
        self.texts.append({'id': identifier, 'text': value, 'font': font, 'font_size': size,
            'font_file': self.glyph(value, size, font)['font_file'], 'role': role, 'owner': owner, 'lines': boxes})
        return baseline + (len(lines) - 1) * size * 1.28

    def frame(self, key, x, y, w, h, fill='none', stroke='#80a5a8', thick=2.5):
        # Each side has a small distinct bend; no precision rounded-card silhouette.
        d = f'M{x+8} {y+2} Q{x+w*.47} {y-4} {x+w-6} {y+3} Q{x+w+2} {y+h*.46} {x+w-3} {y+h-6} Q{x+w*.48} {y+h+3} {x+4} {y+h-2} Q{x-3} {y+h*.48} {x+8} {y+2}Z'
        self.parts.append(f'<path id="{key}" d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{thick}" stroke-linejoin="round"/>')
        self.frames.append({'id': key, 'bounds': [x, y, x+w, y+h]})

    def rule(self, x, y, w, colour=CYAN, thick=3):
        self.parts.append(f'<path d="M{x} {y} Q{x+w*.48} {y-3} {x+w} {y+1}" fill="none" stroke="{colour}" stroke-width="{thick}" stroke-linecap="round"/>')

    def close(self):
        self.parts.append('</svg>')
        self.process.stdin.close()
        self.process.wait(timeout=10)
        return '\n'.join(self.parts)
