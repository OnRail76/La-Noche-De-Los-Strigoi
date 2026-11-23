#!/usr/bin/env python3
"""Boceto 2 de empalados (fase 4): anatomía nueva y tres coloridos posibles.
Cuerpo = PF3 (caracteres inversos, color libre en las filas del juego),
estaca = PF0 (gris roca), nieve = PF1. Salida: carpeta dada."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pal import atari_rgb
from PIL import Image, ImageDraw
P = [atari_rgb(i) for i in range(256)]

# B cuerpo · s estaca · n nieve
EMP = """
.......s.....
......ss.....
....BBBB.....
...BBBB......
...BBB.......
....BB.......
..BBBBBBB....
..BBBsBBBB...
..BB.sBBBB...
.BB..sBBB.B..
.B...sBBB..B.
.B...sBBB..B.
B....sBB...B.
B....sBB....B
.....sBB.....
....BBsBB....
....B.s.BB...
...BB.s..B...
...B..s..BB..
..BB..s...B..
..B...s...B..
.BB...s...BB.
......ss.....
"""
EMP = EMP + "......ss.....\n" * 20 + ".....ssss....\n"
CUERVO = """
....BB..
.BBBBBB.
BB.BB..B
.......B
"""
F4 = '/tmp/v4/f00900.raw'
def put(d, x, y, c):
    if 0 <= x < 192 and 0 <= y < 240:
        d[y * 384 + 2 * x] = c; d[y * 384 + 2 * x + 1] = c
def spr(d, x0, y0, art, cols, flip=False):
    rows = art.strip('\n').split('\n')
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch in cols: put(d, x0 + ((len(r) - 1 - i) if flip else i), y0 + j, cols[ch])
EMPL = """
.B..
BBB.
BBB.
.BB.
B.B.
.s..
.s..
.s..
.s..
.s..
.s..
.s..
"""
VAR = [('1 - GRANATE OSCURO (sangre seca a la luz de la luna)', 0x32),
       ('2 - PARDO MORTECINO', 0x22),
       ('3 - NEGRO (silueta de grabado)', 0x00)]
out = Image.new('RGB', (640, 280 * 3))
for k, (txt, col) in enumerate(VAR):
    d = bytearray(open(F4, 'rb').read())
    for x in range(16, 180, 6):                       # capa lejana: siluetas negras
        spr(d, x, 76 + ((x * 7) % 3), EMPL, {'B': 0x00, 's': 0x00})
    cols = {'B': col, 's': 0x06, 'n': 0x0E}
    spr(d, 58, 116, EMP, cols)
    spr(d, 126, 84, EMP, cols, True)
    spr(d, 61, 107, CUERVO, {'B': 0x00})
    im = Image.new('RGB', (384, 240)); im.putdata([P[b] for b in d])
    im = im.crop((32, 56, 352, 196)).resize((640, 280), Image.NEAREST)
    dr = ImageDraw.Draw(im); dr.rectangle((0, 0, 640, 16), fill=(0, 0, 0)); dr.text((6, 2), txt, fill=(255, 220, 120))
    out.paste(im, (0, 280 * k))
out.save(sys.argv[1] + '/boceto_empalados_v2.png')
# detalle ampliado
big = Image.new('RGB', (3 * 160, 240), (0, 0, 0x30))
for k, (txt, col) in enumerate(VAR):
    d = bytearray([0x80] * 384 * 240)
    spr(d, 10, 2, EMP, {'B': col, 's': 0x06, 'n': 0x0E})
    im = Image.new('RGB', (384, 240)); im.putdata([P[b] for b in d])
    big.paste(im.crop((0, 0, 60, 60)).resize((150, 240), Image.NEAREST), (k * 160 + 5, 0))
big.save(sys.argv[1] + '/boceto_empalados_v2_detalle.png')
