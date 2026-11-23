#!/usr/bin/env python3
"""Fase 5: EL CASTILLO DEL TRONO DE SANGRE. Salones de piedra con vidrieras,
pilares, fosos de pinchos (clase 4), escalinatas, caballeros no muertos y
murciélagos. Al final, la puerta del Trono de Sangre. Salida: ../src/tr_castillo.s"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tramo_util as U
from canvas import C
import tramo

W, H = U.MCOLS * 4, U.MROWS * 8
pix = C(W, H); cls = [[0] * U.MCOLS for _ in range(U.MROWS)]
SEG = [(0, 10), (26, 'P'), (32, 10), (46, 8), (54, 6), (66, 8), (72, 10), (86, 'P'), (94, 10),
       (106, 7), (120, 10), (130, 'P'), (138, 10), (150, 8), (160, 10), (170, 'P'), (178, 10),
       (190, 7), (198, 5), (212, 7), (218, 10), (256, 0)]
prof = [None] * U.MCOLS
for (c0, h), (c1, _) in zip(SEG, SEG[1:]):
    for c in range(c0, c1): prof[c] = h

def piedra(c, r, top):
    for y in range(8):
        for x in range(4):
            X, Y = c * 4 + x, r * 8 + y
            ch = '1'
            if y == 7 or (X + (r % 2) * 4) % 8 == 0: ch = '.'
            if top and y == 0: ch = '2'
            pix.set(X, Y, ch)

for c in range(U.MCOLS):
    h = prof[c]
    if h == 'P':                       # foso de pinchos: hiere al pisarlo
        for r in range(10, U.MROWS):
            cls[r][c] = 4 if r == 10 else 1
            for y in range(8):
                for x in range(4):
                    X, Y = c * 4 + x, r * 8 + y
                    if r == 10:
                        k = X % 4
                        ch = '.'
                        if y < 2 and k in (1, 2): ch = '2'
                        elif 2 <= y < 5: ch = '2' if k != 3 or y == 4 else '.'
                        elif y >= 5: ch = '3'
                    else:
                        ch = '3' if y % 4 else '.'
                    pix.set(X, Y, ch)
        continue
    for r in range(h, U.MROWS):
        cls[r][c] = 1
        piedra(c, r, r == h)
# pilares góticos al fondo (decorado) y antorchas
for c in range(8, 230, 20):
    h = prof[c] if isinstance(prof[c], int) else 10
    for y in range(0, h * 8):
        for x in range(c * 4, c * 4 + 8):
            if pix.p[y][x] == '.':
                pix.set(x, y, '3' if x - c * 4 in (0, 7) else ('.' if (y // 8) % 2 and x - c * 4 == 3 else '3'))
    for y in range(h * 8 - 30, h * 8 - 22):
        pix.set(c * 4 + 10, y, '2' if y < h * 8 - 26 else '3'); pix.set(c * 4 + 11, y, '2' if y < h * 8 - 27 else '3')
# en los muros, entre pilar y pilar: esqueletos encadenados (hueso PF3) y cruces de hierro invertidas
ESQ = """
c.............c
c.............c
gg...........gg
.h...........h.
..h.........h..
...h.HHHHH.h...
....HH.H.HH....
....HHHHHHH....
.....H.H.H.....
......HHH......
.......H.......
....HHHHHHH....
...H.H.H.H.H...
....HHHHHHH....
...H.H.H.H.H...
....HHHHHHH....
.......H.......
......HHH......
.....HH.HH.....
.....H...H.....
.....H...H.....
.....H...H.....
.....H...H.....
....HH...HH....
"""
CRUZ = """
.....hHH.....
....hHHHH....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.h...hHH...h.
hhhhhhHHhhhhH
HHHHHHHHHHHHH
hhhhhhHHhhhhH
.h...hHH...h.
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
.....hHH.....
....hHHHH....
.....hHH.....
"""
k = 0
for c in range(8, 226, 20):
    h = prof[c + 10] if isinstance(prof[c + 10], int) else 10
    if c + 18 >= 230: break
    if k % 2 == 0:
        x0 = (c + 6) * 4 + 4
        for y in range(0, 10):                        # cadenas hasta las argollas
            if y % 3 != 2:
                pix.set(x0, y, '1'); pix.set(x0 + 14, y, '1')
        U.stamp(pix, x0, 10, ESQ, {'H': '4', 'h': '4', 'c': '1', 'g': '1'})
    else:
        U.stamp(pix, (c + 8) * 4 + 2, 4, CRUZ, {'h': '1', 'H': '4'})
    k += 1
# puerta del Trono de Sangre
for y in range(16, 80):
    for x in range(236 * 4, 248 * 4):
        dx = x - 242 * 4
        arch = y < 16 + 10 and abs(dx) > (y - 16) * 2
        pix.set(x, y, '.' if arch else ('3' if abs(dx) > 18 or y < 20 else ('2' if (x + y) % 6 == 0 else '.')))
END_COL, CHECK_COL = 236, 124

sky = C(160, 32)                        # bóvedas y cadenas de las lámparas
for y in range(32):
    for x in range(160):
        u = x % 40
        arc = abs(u - 20)
        ch = '1' if y < 2 + arc * arc // 40 else '.'
        if u == 20 and y < 26: ch = '2'
        if u in (18, 19, 21, 22) and 24 <= y < 28: ch = '2'
        sky.set(x, y, ch)
mtn = C(256, 24)                        # vidrieras de colores en el muro
for x in range(256):
    for y in range(24):
        mtn.set(x, y, '.')
for k in range(4):
    wx = k * 64 + 16
    for y in range(1, 24):
        for x in range(wx, wx + 22):
            dx = abs(x - (wx + 11))
            if y < 9 and dx > y + 2: continue
            col = '1' if ((x - wx) // 4 + y // 6) % 3 == 0 else ('2' if ((x - wx) // 4 + y // 6) % 3 == 1 else '3')
            if (x - wx) % 4 == 0 or y % 6 == 0: col = '.'
            mtn.set(x, y, col)
csA, csB, csC, SKY, MTN, MAP = U.build(pix, cls, sky, mtn)
BK  = [0x00, 0x00, 0x00, 0x00,  0x00, 0x00, 0x00,  0x02] + [0x00] * 10 + [0x00, 0x00, 0x00, 0x00]
PF0 = [0x04, 0x04, 0x04, 0x04,  0x44, 0x44, 0x44,  0x00] + [0x06] * 10 + [0x06, 0x04, 0x04, 0x00]
PF1 = [0x0A, 0x0A, 0x0A, 0x0A,  0x88, 0x88, 0x88,  0x00] + [0x2C] * 10 + [0x0C, 0x0A, 0x0A, 0x00]
PF2 = [0x02, 0x02, 0x02, 0x02,  0x1C, 0x1C, 0x1C,  0x00] + [0x04] * 10 + [0x34, 0x02, 0x02, 0x00]
SP = []
for c in (40, 80, 100, 144, 182, 224):                         # caballeros no muertos
    SP.append((c - 30, 21, c, prof[c] * 8 + 104 if isinstance(prof[c], int) else 184))
for c in (60, 112, 158, 204):                                  # murciélagos de las lámparas
    SP.append((c - 34, 6, c, 116))
SP = sorted([(max(4, a), b, c, d) for a, b, c, d in SP], key=lambda e: e[0])
tramo.write_tramo(os.path.join(HERE, '..', 'src', 'tr_castillo.s'), 'TR5', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, [0x0C] * 22, SP, END_COL, CHECK_COL, 0xFF, 0,
                  'EL CASTILLO DEL', 'TRONO DE SANGRE', mus=1)
U.preview('cas_hoja.png', csA, csB, csC, SKY, MTN, MAP, BK, PF0, PF1, PF2)
