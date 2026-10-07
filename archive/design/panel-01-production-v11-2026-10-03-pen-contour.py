"""Create a separate light pen pass around supplied SVG paths.
The original source path is never changed. Parser covers this asset's commands.
"""
import math, random, re


def rough_contours(path, seed, amplitude=.065):
    commands = set(re.findall(r'[A-Za-z]', path))
    assert commands <= set('MmLlHhVvCcZz'), commands
    tokens = re.findall(r'[MmLlHhVvCcZz]|[-+]?(?:\d*\.\d+|\d+)', path)
    points, contours, cursor, start = [], [], (0.,0.), (0.,0.)
    i, command = 0, None
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]; i += 1
        relative, kind = command.islower(), command.upper()
        if kind == 'Z':
            cursor = start
            contours.append((points, True)); points = []
            command = None
            continue
        amount = {'M':2, 'L':2, 'H':1, 'V':1, 'C':6}[kind]
        values = list(map(float, tokens[i:i+amount])); i += amount
        x, y = cursor
        if kind == 'M':
            if points: contours.append((points, False))
            cursor = (values[0]+(x if relative else 0), values[1]+(y if relative else 0))
            start = cursor; points = [cursor]
            command = 'l' if relative else 'L'
        elif kind in ['L','H','V']:
            if kind == 'L': end = (values[0]+(x if relative else 0), values[1]+(y if relative else 0))
            elif kind == 'H': end = (values[0]+(x if relative else 0), y)
            else: end = (x, values[0]+(y if relative else 0))
            steps = max(1, math.ceil(math.dist(cursor,end)/.25))
            points.extend((x+(end[0]-x)*j/steps, y+(end[1]-y)*j/steps) for j in range(1,steps+1))
            cursor = end
        elif kind == 'C':
            controls = [(values[j]+(x if relative else 0), values[j+1]+(y if relative else 0)) for j in [0,2,4]]
            steps = max(4, math.ceil(sum(math.dist(a,b) for a,b in zip([cursor]+controls,controls))/.25))
            for j in range(1,steps+1):
                t, u = j/steps, 1-j/steps
                points.append((u*u*u*x+3*u*u*t*controls[0][0]+3*u*t*t*controls[1][0]+t*t*t*controls[2][0],
                               u*u*u*y+3*u*u*t*controls[0][1]+3*u*t*t*controls[1][1]+t*t*t*controls[2][1]))
            cursor = controls[-1]
    if points: contours.append((points, False))
    rng = random.Random(seed)
    result = []
    for points, closed in contours:
        altered = [(x+rng.uniform(-amplitude,amplitude), y+rng.uniform(-amplitude,amplitude)) for x,y in points]
        result.append('M '+' L '.join(f'{x:.4f} {y:.4f}' for x,y in altered)+(' Z' if closed else ''))
    return ' '.join(result)
