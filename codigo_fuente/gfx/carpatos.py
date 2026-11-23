#!/usr/bin/env python3
"""Fase 4: EL PASO DE LOS CÁRPATOS. Bosque alpino nevado, acantilados con viento
que empuja hacia atrás, ríos helados (mortales) con troncos que se hunden, Lupari y
fuegos fatuos. Al final, la cueva del Căpcăun. Salida: ../src/tr_carpatos.s"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tramo_util as U
from canvas import C
import tramo

W, H = U.MCOLS * 4, U.MROWS * 8
pix = C(W, H); cls = [[0] * U.MCOLS for _ in range(U.MROWS)]
SEG = [(0, 10), (24, None), (30, 10), (44, 8), (50, 6), (66, 8), (72, 10), (84, None), (96, 10),
       (110, 9), (116, 7), (122, 5), (140, 7), (146, 10), (160, None), (166, 10), (180, 8), (186, 6),
       (204, 8), (210, 10), (256, 0)]
prof = [None] * U.MCOLS
for (c0, h), (c1, _) in zip(SEG, SEG[1:]):
    for c in range(c0, c1): prof[c] = h
LOGS = [(84, 96, 10)]
WIND = (50, 66, 122, 140)        # dos acantilados con viento

for c in range(U.MCOLS):
    h = prof[c]
    if h is None:
        for r in (11, 12):
            for y in range(8):
                for x in range(4):
                    X = c * 4 + x
                    ch = '.' if (y + X // 4) % 5 else '2'          # río helado con espuma
                    if r == 11 and y < 2: ch = '2' if X % 8 < 4 else '.'
                    pix.set(X, r * 8 + y, ch)
        continue
    for r in range(h, U.MROWS):
        cls[r][c] = 1
        for y in range(8):
            for x in range(4):
                X, Y = c * 4 + x, r * 8 + y
                if r == h and y < 3: ch = '2'                      # nieve
                elif r == h and y == 3: ch = '2' if X % 8 in (1, 2, 5) else '1'
                else:
                    ch = '1'
                    xx, yy = X % 8, (Y + r * 3) % 8
                    if (xx, yy) in ((2, 1), (6, 5), (3, 6)): ch = '.'
                pix.set(X, Y, ch)
for (c0, c1, row) in LOGS:
    for c in range(c0, c1):
        cls[row][c] = 3
        for x in range(c * 4, c * 4 + 4):
            for y in range(row * 8, row * 8 + 6):
                pix.set(x, y, '1' if y in (row * 8, row * 8 + 5) else ('.' if (x + y) % 7 == 0 else '1'))
# abetos nevados (decorado), cada 14 columnas donde hay suelo
for c in range(4, 236, 14):
    h = prof[c]
    if h is None or prof[c + 3] != h: continue
    base = h * 8
    for k in range(5):
        y0 = base - 10 - k * 7
        w = 9 - k * 2
        for y in range(y0, y0 + 9):
            dy = y - y0
            ww = max(0, min(w, dy))
            for x in range(c * 4 + 6 - ww, c * 4 + 6 + ww + 1):
                pix.set(x, y, '2' if dy < 2 else '3')
    for y in range(base - 10, base):
        pix.set(c * 4 + 5, y, '1'); pix.set(c * 4 + 6, y, '1')
# empalados del voivoda junto al camino (decorado, PF3 granate): cuerpo atravesado, cabeza vencida
EMP0 = """
......s......
.....ss......
....BBB......
...BBBB......
....BB.......
..BBBBBB.....
.BBBsBBBB....
.BB.sBBB.B...
.B..sBBB..B..
B...sBB...B..
B...sBB....B.
....BsBB.....
...BB.s.B....
..BB..s..B...
..B...s..BB..
.BB...s...B..
......s......
"""
EMP = "".join(l + "\n" + l + "\n" for l in EMP0.strip().split("\n")) + "......s......\n" * 12 + ".....sss.....\n"
CUERVO = """
....BB..
.BBBBBB.
BB.BB..B
.......B
"""
EMP_H = len(EMP.strip().split('\n'))
pinos = [c for c in range(4, 236, 14) if prof[c] is not None and prof[c + 3] == prof[c]]
emps = []
for c in range(8, 226):
    if emps and c - emps[-1] < 13: continue
    h = prof[c]
    if h is None or any(prof[k] != h for k in range(c - 1, c + 5)) or h * 8 - EMP_H < 6: continue
    if any(p - 5 <= c <= p + 4 for p in pinos): continue
    emps.append(c)
    U.stamp(pix, c * 4, h * 8 - EMP_H, EMP, {'B': '4', 's': '1'})
    if len(emps) % 3 == 1:
        U.stamp(pix, c * 4 + 3, h * 8 - EMP_H - 4, CUERVO, {'B': '4'})
print('empalados en', emps)
# cueva del Căpcăun al final
for y in range(0, H - 24):
    for x in range(232 * 4, W):
        d = abs(x - 244 * 4) + max(0, 40 - y)
        pix.set(x, y, '1' if d > 26 else ('.' if y > 30 else '1'))
END_COL, CHECK_COL = 236, 104

sky = C(160, 32)
for y in range(32):
    for x in range(160):
        ch = '.'
        cx = (x % 80) - 40
        if y < 12 and cx * cx // 30 + (y - 5) * (y - 5) < 18 + (x // 80) * 6: ch = '1'   # nubes de tormenta
        if (x * 13 + y * 7) % 53 == 0: ch = '2'                      # copos
        sky.set(x, y, ch)
mtn = C(256, 24)
for x in range(256):
    k = x % 64
    top = 2 + int(abs(k - 32) * 0.55) + (3 if (x // 64) % 2 else 0)
    for y in range(top, 24):
        mtn.set(x, y, '2' if y < top + 3 else ('1' if (x + y) % 9 else '3'))
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
for x in (6, 40, 70, 101, 134, 168, 198, 230):                 # el bosque de estacas, a lo lejos
    U.stamp(mtn, x, 12 + (x * 7) % 3, EMPL, {'B': '4', 's': '4'})
U.clear3(mtn)
csA, csB, csC, SKY, MTN, MAP = U.build(pix, cls, sky, mtn)
BK  = [0x00, 0x00, 0x02, 0x02,  0x82, 0x82, 0x82,  0x84] + [0x80] * 10 + [0x80, 0x82, 0x82, 0x00]
PF3 = [0x0C] * 4 + [0x00] * 3 + [0x0C] + [0x32] * 10 + [0x32, 0x0C, 0x0C, 0x0C]
PF0 = [0x06, 0x06, 0x04, 0x04,  0x0A, 0x0A, 0x0A,  0x00] + [0x06] * 10 + [0x06, 0x06, 0x04, 0x00]
PF1 = [0x0E, 0x0E, 0x0E, 0x0E,  0x0E, 0x0E, 0x0C,  0x00] + [0x0E] * 10 + [0x0E, 0x0C, 0x0C, 0x00]
PF2 = [0x04, 0x04, 0x04, 0x04,  0x84, 0x84, 0x84,  0x00] + [0xC2] * 10 + [0xC2, 0x84, 0x84, 0x00]
SP = []
for c in (36, 76, 104, 130, 172, 196, 222):                     # Lupari
    SP.append((c - 30, 19, c, (prof[c] or 10) * 8 + 104))
for c in (58, 92, 132, 162, 200):                               # fuegos fatuos
    SP.append((c - 30, 20, c, 140))
for c in (20, 112, 190):                                        # cuervos de la tormenta
    SP.append((c - 30, 2, 0, 124))
SP = sorted([(max(4, a), b, c, d) for a, b, c, d in SP], key=lambda e: e[0])
tramo.write_tramo(os.path.join(HERE, '..', 'src', 'tr_carpatos.s'), 'TR4', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, PF3, SP, END_COL, CHECK_COL, 0xFF, 0,
                  'EL PASO DE', 'LOS CÁRPATOS', extra=WIND, mus=0)
U.preview('car_hoja.png', csA, csB, csC, SKY, MTN, MAP, BK, PF0, PF1, PF2, PF3=PF3)
