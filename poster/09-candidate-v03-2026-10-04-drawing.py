"""Hand-drawn marks used by the illustrated Section 9 candidate."""
INK, CYAN, GOLD, PAPER = '#173a47', '#26c6cf', '#ffd400', '#fffdf5'
PALE_CYAN, PALE_GOLD, RULE = '#f4ffff', '#fff9df', '#8cabad'
shapes = []

def path(d, colour=INK, width=2.8, fill='none', opacity=1):
    shapes.append(
        f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'
    )


def frame(x, y, width, height, fill='none', colour=RULE, thick=2.4):
    d = (
        f'M{x+7} {y+2} Q{x+width*.47} {y-3} {x+width-5} {y+3} '
        f'Q{x+width+2} {y+height*.46} {x+width-3} {y+height-5} '
        f'Q{x+width*.52} {y+height+3} {x+4} {y+height-2} '
        f'Q{x-3} {y+height*.52} {x+7} {y+2}Z'
    )
    path(d, colour, thick, fill)


def marker(x, y, width, height=14, colour=GOLD, opacity=.24):
    for i in range(3):
        yy = y + height * (i + .5) / 3
        path(
            f'M{x+i%2*2} {yy} Q{x+width*.5} {yy-2+i%3} {x+width-i%2*2} {yy+1}',
            colour, height/3*1.15, opacity=opacity,
        )


def arrow(x1, y1, x2, y2, colour=CYAN, width=3.4):
    midx, midy = (x1+x2)/2, (y1+y2)/2
    path(f'M{x1} {y1} Q{midx} {midy-2} {x2} {y2}', colour, width)
    if abs(x2-x1) >= abs(y2-y1):
        sign = 1 if x2 > x1 else -1
        path(f'M{x2-sign*12} {y2-7} L{x2} {y2} L{x2-sign*12} {y2+8}', colour, width)
    else:
        sign = 1 if y2 > y1 else -1
        path(f'M{x2-7} {y2-sign*12} L{x2} {y2} L{x2+8} {y2-sign*12}', colour, width)


def icon_phone(cx, cy, scale=1):
    s = scale
    path(f'M{cx-24*s} {cy-39*s} Q{cx} {cy-43*s} {cx+24*s} {cy-39*s} L{cx+22*s} {cy+39*s} Q{cx} {cy+42*s} {cx-23*s} {cy+38*s}Z', INK, 2.8*s, PALE_CYAN)
    path(f'M{cx-13*s} {cy-22*s} L{cx+13*s} {cy-22*s} M{cx-13*s} {cy-8*s} L{cx+8*s} {cy-8*s}', CYAN, 3*s)
    path(f'M{cx-12*s} {cy+19*s} Q{cx-8*s} {cy+15*s} {cx-8*s} {cy+8*s} Q{cx-8*s} {cy-1*s} {cx} {cy-2*s} Q{cx+8*s} {cy-1*s} {cx+8*s} {cy+8*s} Q{cx+8*s} {cy+15*s} {cx+12*s} {cy+19*s}Z', GOLD, 2.5*s, PALE_GOLD)
    path(f'M{cx-3*s} {cy+23*s} Q{cx} {cy+28*s} {cx+3*s} {cy+23*s} M{cx} {cy-6*s} L{cx} {cy-2*s}', GOLD, 2.3*s)


def icon_calendar(cx, cy, scale=1):
    s = scale
    path(f'M{cx-28*s} {cy-29*s} Q{cx} {cy-33*s} {cx+28*s} {cy-29*s} L{cx+26*s} {cy+29*s} Q{cx} {cy+32*s} {cx-28*s} {cy+28*s}Z', INK, 2.6*s, PALE_CYAN)
    path(f'M{cx-27*s} {cy-12*s} Q{cx} {cy-14*s} {cx+27*s} {cy-12*s}', CYAN, 3*s)
    path(f'M{cx-15*s} {cy-37*s} L{cx-15*s} {cy-22*s} M{cx+14*s} {cy-37*s} L{cx+14*s} {cy-22*s}', GOLD, 4*s)
    path(f'M{cx-13*s} {cy+1*s} L{cx-2*s} {cy+1*s} M{cx+7*s} {cy+1*s} L{cx+16*s} {cy+1*s}', INK, 2*s)


def icon_person(cx, cy, colour=INK, scale=1):
    s = scale
    path(f'M{cx} {cy-31*s} C{cx+13*s} {cy-31*s} {cx+16*s} {cy-11*s} {cx} {cy-9*s} C{cx-16*s} {cy-11*s} {cx-13*s} {cy-31*s} {cx} {cy-31*s}Z', colour, 2.7*s, PALE_GOLD)
    path(f'M{cx-29*s} {cy+31*s} Q{cx-25*s} {cy-1*s} {cx} {cy-3*s} Q{cx+26*s} {cy-1*s} {cx+30*s} {cy+31*s}', colour, 2.7*s, PALE_CYAN)


def icon_trip_stack(cx, cy):
    for off in (13, 0, -13):
        path(f'M{cx-31} {cy+off-15} Q{cx} {cy+off-18} {cx+30} {cy+off-15} L{cx+29} {cy+off+14} Q{cx} {cy+off+17} {cx-31} {cy+off+14}Z', CYAN if off == 0 else RULE, 2.4, PALE_CYAN if off == 0 else PAPER)
        if off == 0:
            path(f'M{cx-20} {cy+off-3} L{cx-6} {cy+off-3} M{cx+1} {cy+off+5} L{cx+18} {cy+off-6}', INK, 2.2)


def icon_brain(cx, cy):
    # A small network cloud signals a proposed AI step without implying a system exists.
    path(f'M{cx-27} {cy+10} C{cx-40} {cy-5} {cx-31} {cy-23} {cx-16} {cy-24} C{cx-9} {cy-42} {cx+11} {cy-35} {cx+15} {cy-23} C{cx+36} {cy-22} {cx+38} {cy+5} {cx+22} {cy+12} C{cx+12} {cy+30} {cx-10} {cy+28} {cx-16} {cy+16}Z', GOLD, 3, PALE_GOLD)
    for dx, dy in [(-16, -12), (11, -16), (-8, 8), (16, 8)]:
        path(f'M{cx+dx-4} {cy+dy} Q{cx+dx} {cy+dy-4} {cx+dx+4} {cy+dy} Q{cx+dx} {cy+dy+4} {cx+dx-4} {cy+dy}Z', INK, 1.8, PALE_CYAN)
    path(f'M{cx-13} {cy-11} L{cx+7} {cy-15} L{cx-6} {cy+7} L{cx+14} {cy+8}', CYAN, 2.2)


def icon_shield(cx, cy):
    path(f'M{cx} {cy-34} Q{cx+24} {cy-32} {cx+31} {cy-25} L{cx+27} {cy+6} Q{cx+19} {cy+27} {cx} {cy+37} Q{cx-20} {cy+27} {cx-28} {cy+6} L{cx-31} {cy-25}Z', CYAN, 3, PALE_CYAN)
    path(f'M{cx-14} {cy} L{cx-3} {cy+11} L{cx+17} {cy-13}', GOLD, 4)


def icon_message(cx, cy):
    path(f'M{cx-39} {cy-24} Q{cx} {cy-28} {cx+39} {cy-24} L{cx+36} {cy+16} Q{cx+4} {cy+20} {cx-14} {cy+16} L{cx-33} {cy+29} L{cx-28} {cy+13}Z', INK, 2.8, PALE_CYAN)
    for dx in (-16, 0, 16):
        path(f'M{cx+dx-3} {cy-2} Q{cx+dx} {cy-5} {cx+dx+3} {cy-2} Q{cx+dx} {cy+1} {cx+dx-3} {cy-2}Z', GOLD, 1.4, GOLD)


def icon_car(cx, cy, scale=1):
    s = scale
    path(f'M{cx-38*s} {cy+12*s} Q{cx-28*s} {cy-12*s} {cx-8*s} {cy-15*s} L{cx+20*s} {cy-15*s} Q{cx+34*s} {cy-7*s} {cx+40*s} {cy+12*s} L{cx+36*s} {cy+23*s} L{cx-38*s} {cy+23*s}Z', GOLD, 2.8*s, PALE_GOLD)
    path(f'M{cx-18*s} {cy-13*s} L{cx-7*s} {cy-28*s} L{cx+17*s} {cy-27*s} L{cx+28*s} {cy-12*s}', INK, 2.5*s)
    for wx in (cx-22*s, cx+25*s):
        path(f'M{wx-7*s} {cy+23*s} Q{wx} {cy+14*s} {wx+7*s} {cy+23*s} Q{wx+6*s} {cy+33*s} {wx-1*s} {cy+32*s} Q{wx-8*s} {cy+31*s} {wx-7*s} {cy+23*s}Z', INK, 2*s, PAPER)


def icon_clock(cx, cy):
    path(f'M{cx} {cy-29} C{cx+18} {cy-29} {cx+30} {cy-16} {cx+30} {cy} C{cx+30} {cy+18} {cx+17} {cy+30} {cx} {cy+30} C{cx-18} {cy+30} {cx-30} {cy+17} {cx-30} {cy} C{cx-30} {cy-18} {cx-17} {cy-29} {cx} {cy-29}Z', CYAN, 2.8, PALE_CYAN)
    path(f'M{cx} {cy-16} L{cx} {cy+1} L{cx+15} {cy+10}', GOLD, 3.4)


def icon_star(cx, cy, radius=21):
    pts = []
    for i in range(10):
        angle = -90 + i*36
        r = radius if i % 2 == 0 else radius*.43
        import math
        pts.append((cx+math.cos(math.radians(angle))*r, cy+math.sin(math.radians(angle))*r))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    path(d, GOLD, 2.4, PALE_GOLD)


def icon_gauge(cx, cy, colour=CYAN):
    path(f'M{cx-29} {cy+19} A30 30 0 0 1 {cx+29} {cy+19}', colour, 3)
    path(f'M{cx} {cy+18} L{cx+14} {cy-4}', GOLD, 3.5)
    path(f'M{cx-25} {cy+11} l7 -2 M{cx-15} {cy-5} l5 6 M{cx+15} {cy-5} l-5 6 M{cx+25} {cy+11} l-7 -2', INK, 2)


def icon_scale(cx, cy):
    path(f'M{cx} {cy-29} L{cx} {cy+23} M{cx-28} {cy-18} L{cx+28} {cy-18} M{cx-22} {cy-18} L{cx-33} {cy+4} M{cx-34} {cy+4} Q{cx-22} {cy+17} {cx-10} {cy+4} M{cx+22} {cy-18} L{cx+33} {cy+4} M{cx+10} {cy+4} Q{cx+22} {cy+17} {cx+34} {cy+4} M{cx-18} {cy+24} L{cx+18} {cy+24}', CYAN, 2.5)


def icon_stop(cx, cy, scale=1):
    s = scale
    path(f'M{cx-22*s} {cy-17*s} L{cx-10*s} {cy-29*s} L{cx+10*s} {cy-29*s} L{cx+22*s} {cy-17*s} L{cx+22*s} {cy+13*s} L{cx+10*s} {cy+25*s} L{cx-10*s} {cy+25*s} L{cx-22*s} {cy+13*s}Z', GOLD, 2.8*s, PALE_GOLD)
    path(f'M{cx-11*s} {cy-2*s} L{cx+11*s} {cy-2*s}', INK, 3*s)

