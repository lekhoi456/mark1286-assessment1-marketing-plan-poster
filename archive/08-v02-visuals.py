"""Controlled hand-drawn charts and icon viewports; all marks represent targets."""
import base64
import math

INK, CYAN, GOLD = '#173a47', '#26c6cf', '#ffd400'

def install_art(layout, path):
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    layout.parts.append(f'<defs><image id="objective-icons" href="data:image/png;base64,{data}" width="2172" height="724"/></defs>')

def icon(layout, quarter, x, y, w, h):
    crops=[(38,145,518,420),(608,145,470,420),(1080,132,466,425),(1550,145,604,420)]
    cx,cy,cw,ch=crops[quarter]
    layout.parts.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" overflow="hidden"><use href="#objective-icons"/></svg>')

def arrow(layout, x1, y1, x2, y2, colour=CYAN, width=11):
    layout.parts.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2} {(y1+y2)/2-3} {x2} {y2}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>')
    angle = math.atan2(y2-y1,x2-x1)
    a = (x2-22*math.cos(angle-.5), y2-22*math.sin(angle-.5))
    b = (x2-22*math.cos(angle+.5), y2-22*math.sin(angle+.5))
    layout.parts.append(f'<path d="M{a[0]} {a[1]} L{x2} {y2} L{b[0]} {b[1]}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')

def target_bar(layout, key, x, y, value, maximum=3, width=330, colour=CYAN):
    end = x + width * value / maximum
    layout.parts.append(f'<path id="{key}" data-value="{value}" data-baseline="0" data-scale-max="{maximum}" d="M{x} {y} Q{(x+end)/2} {y-2} {end} {y+1}" fill="none" stroke="{colour}" stroke-width="25" stroke-linecap="butt"/>')
    layout.parts.append(f'<path d="M{x} {y-14} L{x} {y+16}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    layout.parts.append(f'<path d="M{x+1} {y-5} L{end-2} {y-3}" fill="none" stroke="#fffdf5" stroke-width="2.5" opacity=".45"/>')
    return {'id':key,'value':value,'zero_baseline':0,'scale_max':maximum,'width':end-x,'kind':'proposed-target bar'}

def gauge(layout, key, cx, cy, value, direction, radius=82):
    # Full unfilled arc is a percentage scale. Only the small marker encodes the target.
    layout.parts.append(f'<path id="{key}-scale" d="M{cx-radius} {cy} A{radius} {radius} 0 0 1 {cx+radius} {cy}" fill="none" stroke="#74c8cc" stroke-width="12" opacity=".5"/>')
    layout.parts.append(f'<path d="M{cx-radius} {cy+1} A{radius+1} {radius+1} 0 0 1 {cx+radius} {cy-1}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    for fraction in [0,.25,.5,.75,1]:
        theta = math.pi*(1-fraction)
        a=(cx+(radius-7)*math.cos(theta),cy-(radius-7)*math.sin(theta))
        b=(cx+(radius+8)*math.cos(theta),cy-(radius+8)*math.sin(theta))
        layout.parts.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{INK}" stroke-width="2.2"/>')
    theta=math.pi*(1-value/100)
    a=(cx+(radius-12)*math.cos(theta),cy-(radius-12)*math.sin(theta))
    b=(cx+(radius+13)*math.cos(theta),cy-(radius+13)*math.sin(theta))
    layout.parts.append(f'<path id="{key}-target" data-target="{value}" data-direction="{direction}" d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>')
    layout.parts.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{INK}" stroke-width="2.3"/>')
    return {'id':key,'target':value,'direction':direction,'scale':[0,100],
        'actual_result':None,'progress_fill':False,'marker_only_target':True}
