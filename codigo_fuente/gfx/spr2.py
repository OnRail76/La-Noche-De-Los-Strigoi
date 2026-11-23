#!/usr/bin/env python3
"""Sprites de los enemigos nuevos (8 px de ancho) -> ../src/spr2.s
  Vâvâma (espíritu del bosque con garras largas), Iele (espíritus del aire),
  gárgola de piedra. Cada tipo: 4 fotogramas de la misma altura."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

VAV = ["""
..XXX...
.XXXXX..
.X.X.X..
.XXXXX..
..XXX...
X.XXX..X
XXXXXXXX
.XXXXXX.
..XXXX..
..XXXX..
..XXXX..
.XXXXXX.
.XXXXXX.
XXX..XXX
XX....XX
X.X..X.X
X......X
.X....X.
""","""
..XXX...
.XXXXX..
.X.X.X..
.XXXXX..
..XXX...
..XXX...
.XXXXXXX
XXXXXX.X
X.XXXX.X
X.XXXX..
..XXXX..
.XXXXXX.
.XXXXXX.
XXX..XXX
XX....XX
.XX..XX.
..X..X..
........
""","""
...XXX..
..XXXXX.
..X.X.X.
..XXXXX.
...XXX..
X..XXX.X
XXXXXXXX
.XXXXXX.
..XXXX..
..XXXX..
..XXXX..
.XXXXXX.
.XXXXXX.
XXX..XXX
XX....XX
X.X..X.X
X......X
.X....X.
""","""
...XXX..
..XXXXX.
..X.X.X.
..XXXXX.
...XXX..
...XXX..
XXXXXXX.
X.XXXXXX
X.XXXX.X
..XXXX.X
..XXXX..
.XXXXXX.
.XXXXXX.
XXX..XXX
XX....XX
.XX..XX.
..X..X..
........
"""]

IELE = ["""
...XX...
..XXXX..
..X..X..
..XXXX..
.X.XX.X.
X.XXXX.X
..XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
X.XXXX.X
.X.XX.X.
X..XX..X
...X....
""","""
...XX...
..XXXX..
..X..X..
..XXXX..
X..XX..X
.XXXXXX.
..XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
.XXXXXX.
X.XXXX.X
.X.XX.X.
....X...
""","""
...XX...
..XXXX..
..X..X..
..XXXX..
.X.XX.X.
X.XXXX.X
..XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
X.XXXX.X
.X.XX.X.
X..XX..X
...X....
""","""
...XX...
..XXXX..
..X..X..
..XXXX..
X..XX..X
.XXXXXX.
..XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
.XXXXXX.
X.XXXX.X
.X.XX.X.
....X...
"""]

GARG = ["""
X......X
XX.XX.XX
.XXXXXX.
.X.XX.X.
.XXXXXX.
..X..X..
.XXXXXX.
XXXXXXXX
X.XXXX.X
X.XXXX.X
..XXXX..
.XX..XX.
XX....XX
XXX..XXX
""","""
X..XX..X
XXXXXXXX
.X.XX.X.
.XXXXXX.
X.X..X.X
XXXXXXXX
XXXXXXXX
XXXXXXXX
X.XXXX.X
..XXXX..
.XX..XX.
.X....X.
XX....XX
........
""","""
........
.X.XX.X.
XXXXXXXX
XXX..XXX
XX.XX.XX
X.XXXX.X
X.XXXX.X
..XXXX..
..XXXX..
.XX..XX.
.X....X.
XX....XX
........
........
""","""
X..XX..X
XXXXXXXX
.X.XX.X.
.XXXXXX.
X.X..X.X
XXXXXXXX
XXXXXXXX
XXXXXXXX
X.XXXX.X
..XXXX..
.XX..XX.
.X....X.
XX....XX
........
"""]

TIJ = ["""
X......X
XX....XX
.XX..XX.
.XX..XX.
..XXXX..
...XX...
...XX...
..XXXX..
.X.XX.X.
X..XX..X
X..XX..X
X..XX..X
.X.XX.X.
..XXXX..
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...X....
...X....
""","""
.X....X.
.XX..XX.
..XXXX..
..XXXX..
...XX...
...XX...
...XX...
..XXXX..
.X.XX.X.
X..XX..X
X..XX..X
X..XX..X
.X.XX.X.
..XXXX..
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...X....
...X....
"""]
TIJ = [TIJ[0], TIJ[1], TIJ[0], TIJ[1]]
AGU = ["""
...XX...
..X..X..
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...XX...
...X....
...X....
"""] * 4

PIE = ["""
.XXXX...
XXXXXX..
XXX.XX..
XXXXXX..
.XXXX...
"""] * 4

MOROI = ["""
...XX...
..XXXX..
.XXXXXX.
.X.XX.X.
.XXXXXX.
..X..X..
.XXXXXX.
XXXXXXXX
X.XXXX.X
X.XXXX.X
..XXXX..
.XXXXXX.
.XX..XX.
.X.XX.X.
X..X...X
...X.X..
""","""
...XX...
..XXXX..
.XXXXXX.
.X.XX.X.
.XXXXXX.
..X..X..
.XXXXXX.
XXXXXXXX
X.XXXX.X
X.XXXX.X
..XXXX..
.XXXXXX.
.XX..XX.
X.X..X.X
.X.X..X.
..X..X..
"""]
MOROI = MOROI * 2
VALVA = ["""
..XXX...
.XXXXX..
..XXXX..
..X.X...
..XXXX..
...XX..X
.XXXXXX.
X.XXXX..
X.XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
XXXXXXXX
.XX..XX.
.XX..XX.
.X....X.
XX....XX
........
""","""
..XXX...
.XXXXX..
..XXXX..
..X.X...
..XXXX..
...XX..X
.XXXXXX.
X.XXXX..
X.XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
XXXXXXXX
..XXXX..
..X..X..
..X..X..
.XX..XX.
........
""","""
X.XXX...
XXXXXX..
X.XXXX..
X.X.X...
X.XXXX..
X..XX...
XXXXXX..
.XXXXX..
..XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
XXXXXXXX
.XX..XX.
.XX..XX.
.X....X.
XX....XX
........
""","""
..XXX..X
.XXXXXXX
..XXXX.X
..X.X..X
..XXXX..
...XX...
.XXXXXX.
X.XXXX..
X.XXXX..
.XXXXXX.
.XXXXXX.
XXXXXXXX
XXXXXXXX
.XX..XX.
.XX..XX.
.X....X.
XX....XX
........
"""]
PICO = ["""
XXXXXX..
X..X....
...X....
...X....
...X....
...X....
""","""
.....X..
X...XX..
.X.X....
..X.....
.X.X....
X...X...
""","""
...X....
...X....
...X....
...X....
X..X....
XXXXXX..
""","""
X...X...
.X.X....
..X.....
.X.X....
XX...X..
X.......
"""]
ESTAL = ["""
XXXXXXXX
.XXXXXX.
.XXXXXX.
..XXXX..
..XXXX..
..XXXX..
...XX...
...XX...
...XX...
...X....
"""] * 4
INSECTO = ["""
X.X.....
.XXX.X..
XXXXXX..
.XXX.X..
X.X.....
........
""","""
.X......
XXXX....
XXXXXX..
XXXX....
.X......
........
"""] * 2

LUPARI = ["""
........
.X....X.
.XX..XX.
.XXXXXX.
.X.XX.X.
.XXXXXX.
..X..X..
.XXXXXXX
XXXXXXX.
X.XXXX..
..XXXX..
.XXXXX..
XX...XX.
X.....X.
X......X
""","""
........
.X....X.
.XX..XX.
.XXXXXX.
.X.XX.X.
.XXXXXX.
..X..X..
XXXXXXX.
.XXXXXXX
..XXXX.X
..XXXX..
..XXXXX.
..XX.XX.
.XX...X.
.X....X.
"""]
LUPARI = LUPARI * 2
FATUO = ["""
...X....
..XXX...
.XXXXX..
.XX.XX..
.XXXXX..
..XXX...
...X....
..X.....
""","""
....X...
...XXX..
..XXXXX.
..XX.XX.
..XXXXX.
...XXX..
....X...
.....X..
"""] * 2
CABALLERO = ["""
..XXX...
.XXXXX..
.X.X.X..
.XXXXX..
..XXX..X
XXXXXXXX
X.XXXX.X
X.XXXX.X
X.XXXX.X
..XXXX.X
.XXXXXX.
.XX..XX.
.XX..XX.
.XX..XX.
XXX..XXX
""","""
..XXX...
.XXXXX..
.X.X.X..
.XXXXX..
..XXX..X
XXXXXXXX
X.XXXX.X
X.XXXX.X
X.XXXX.X
..XXXX.X
.XXXXXX.
..XXXX..
..X..X..
.XX..XX.
.XX..XXX
"""] * 2
ONDA = ["""
...X....
..X.X...
.X...X..
X.X.X.X.
.X...X..
XXXXXXXX
""","""
....X...
...X.X..
..X...X.
.X.X.X.X
..X...X.
XXXXXXXX
"""] * 2

DECO = ["""
X......X
XX....XX
.XXXXXX.
..XXXX..
...XX...
........
""","""
........
........
.XXXXXX.
XXXXXXXX
X..XX..X
........
"""] * 2
_CAL = """
.....XXXXXX.....
...XXXXXXXXXX...
..XXXXXXXXXXXX..
.XXXXXXXXXXXXXX.
.XXXXXXXXXXXXXX.
XXXXXXXXXXXXXXXX
XX.....XX.....XX
X......XX......X
X......XX......X
XX.....XX.....XX
XXXXXXX..XXXXXXX
.XXXXX....XXXXX.
..XXXXXXXXXXXX..
...X.XX.XX.XX...
...XXXXXXXXXX...
....X.X.XX.X....
.....XXXXXX.....
"""
_rows = [r for r in _CAL.strip('\n').split('\n')]
CAL = ['\n'.join(r[:8] for r in _rows for _ in (0, 1, 2)), '\n'.join(r[8:] for r in _rows for _ in (0, 1, 2))] * 2

def bits(t):
    return [int(l.strip().replace('X', '1').replace('.', '0'), 2) for l in t.strip('\n').split('\n')]

L = ['; generado por gfx/spr2.py']
MODSPR = {'SLUP': (4, LUPARI), 'SFAT': (4, FATUO), 'SCAB': (5, CABALLERO)}
for nm, (m, fr) in MODSPR.items():
    pass
heights = []; HD = {}
for name, frames in (('SVAV', VAV), ('SIEL', IELE), ('SGAR', GARG), ('STIJ', TIJ), ('SAGU', AGU), ('SPIE', PIE), ('SMOR', MOROI), ('SVAL', VALVA), ('SPIC', PICO), ('SEST', ESTAL), ('SINS', INSECTO), ('SLUP', LUPARI), ('SFAT', FATUO), ('SCAB', CABALLERO), ('SOND', ONDA), ('SDEC', DECO), ('SCAL', CAL)):
    h = len(bits(frames[0]))
    heights.append(h); HD[name] = h
    L.append('%s:' % name)
    for f in frames:
        b = bits(f); assert len(b) == h, (name, len(b))
        L.append('        .byte ' + ','.join('$%02X' % x for x in b))
NM = ['SVAV','SIEL','SGAR','STIJ','SAGU','SPIE','SMOR','SVAL','SPIC','SEST','SINS','SLUP','SFAT','SCAB','SDEC','SOND','SCAL']
L.append('ESPR_LO: .byte ' + ','.join('<'+n for n in NM))
L.append('ESPR_HI: .byte ' + ','.join('>'+n for n in NM))
L.append('EHGT:    .byte %s' % ','.join(str(HD[n]) for n in NM))
open(os.path.join(HERE, '..', 'src', 'spr2.s'), 'w').write('\n'.join(L) + '\n')
print(heights)
