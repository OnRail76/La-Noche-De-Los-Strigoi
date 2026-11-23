#!/usr/bin/env python3
"""Fase 3: LAS MINAS DE SAL Y LAS CRIPTAS.
Galerías de sal con puntales de madera, pozos de agua salada negra (mortales),
puentes colgantes que se hunden (clase 3), repisas de roca y, al final, la cripta.
Salida: ../src/tr_minas.s"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import fase1 as F
from canvas import C
import tramo

MCOLS, MROWS = 256, 13
W, H = MCOLS * 4, MROWS * 8
SURF = 10
pix = C(W, H)
cls = [[0] * MCOLS for _ in range(MROWS)]
rnd = random.Random(1840)

# --- perfil del suelo: (columna inicial, fila de la superficie o None = pozo de agua)
SEG = [(0, 10), (22, None), (28, 10), (40, 8), (52, 10), (60, None), (72, 10), (84, 7), (92, 9),
       (100, None), (106, 10), (120, 8), (128, 10), (150, None), (162, 10), (172, 7), (180, 9),
       (188, None), (194, 10), (206, 8), (214, 10), (256, 0)]
prof = [None] * MCOLS
for (c0, h), (c1, _) in zip(SEG, SEG[1:]):
    for c in range(c0, c1): prof[c] = h
BRIDGES = [(60, 72, 10), (150, 162, 10)]          # puentes colgantes sobre los pozos anchos
CRYPT = 214                                        # desde aquí, la cripta

def rock(c, r, top):
    for y in range(8):
        for x in range(4):
            X, Y = c * 4 + x, r * 8 + y
            if top and y == 0: ch = '2'                                   # costra de sal
            elif top and y == 1: ch = '1' if (X % 8) not in (2, 5) else '2'
            else:
                ch = '1'
                xx, yy = X % 8, (Y + (r % 2) * 4) % 8
                if (xx, yy) in ((1, 2), (2, 3), (5, 6), (6, 5)): ch = '2'   # vetas de sal
                elif (xx, yy) in ((3, 0), (7, 4), (0, 7)): ch = '.'
            pix.set(X, Y, ch)

def cripta_wall(c, r, top):
    for y in range(8):
        for x in range(4):
            X, Y = c * 4 + x, r * 8 + y
            ch = '1'
            if Y % 8 == 7 or (X + (Y // 8) * 4) % 8 == 0: ch = '.'
            if top and y == 0: ch = '2'
            pix.set(X, Y, ch)

# --- suelo, pozos y repisas
for c in range(MCOLS):
    h = prof[c]
    if h is None:
        for r in (11, 12):                       # agua negra con brillos
            for y in range(8):
                for x in range(4):
                    X, Y = c * 4 + x, r * 8 + y
                    ch = '.'
                    if r == 11 and y == 2 and X % 8 < 3: ch = '3'
                    if r == 11 and y == 5 and (X + 4) % 8 < 2: ch = '3'
                    pix.set(X, Y, ch)
        continue
    for r in range(h, MROWS):
        cls[r][c] = 1
        (cripta_wall if c >= CRYPT else rock)(c, r, r == h)

# --- puentes colgantes (clase 3) con cuerdas
for (c0, c1, row) in BRIDGES:
    for c in range(c0, c1):
        cls[row][c] = 3
        for x in range(c * 4, c * 4 + 4):
            pix.set(x, row * 8, '3'); pix.set(x, row * 8 + 1, '3')
            if x % 4 == 0: pix.set(x, row * 8 + 2, '3')
        sag = abs(c - (c0 + c1) / 2.0)
        ry = row * 8 - 8 + int(sag * 0.6)
        for x in range(c * 4, c * 4 + 4): pix.set(x, ry, '2')            # cuerda
    for c in (c0, c1 - 1):
        for y in range(row * 8 - 10, row * 8 + 2): pix.set(c * 4 + 1, y, '3'); pix.set(c * 4 + 2, y, '3')

# --- columnas de sal al fondo (no estorban) y grupos de cristales sobre el suelo
for c in range(13, CRYPT - 4, 26):
    top = prof[c] if prof[c] is not None else 10
    for y in range(8, top * 8):
        for x in range(c * 4, c * 4 + 8):
            if pix.p[y][x] != '.': continue
            xx = x - c * 4
            ch = '1' if 1 <= xx <= 6 else '.'
            if xx in (2, 3) and y % 8 in (1, 2, 3): ch = '2'
            if xx == 6 and y % 8 == 5: ch = '.'
            pix.set(x, y, ch)
for c in range(3, CRYPT - 4, 11):
    h = prof[c]
    if h is None or prof[c + 1] != h: continue
    for (dx, l) in ((0, 3), (2, 6), (4, 4), (6, 2)):
        for y in range(h * 8 - l, h * 8):
            pix.set(c * 4 + dx, y, '2'); pix.set(c * 4 + dx + 1, y, '2' if y > h * 8 - l + 1 else '.')
# --- puntales de madera de la mina (decorado, no estorban)
for c in range(6, CRYPT - 6, 18):
    h = prof[c] if prof[c] is not None else 10
    if prof[c + 8] is None: continue
    hh = min(h, prof[c + 8] or 10)
    for y in range(8, hh * 8):
        for dx in (0, 1):
            pix.set(c * 4 + dx, y, '3'); pix.set((c + 8) * 4 + dx, y, '3')
    for x in range(c * 4, (c + 8) * 4 + 2):
        for y in range(8, 12): pix.set(x, y, '3')
# --- cristales de sal colgando del techo de la galería (fila 0)
for c in range(2, CRYPT, 7):
    l = (4, 6, 8)[c % 3]
    for y in range(l):
        w = max(0, 2 - y // 3)
        for x in range(c * 4 + 2 - w, c * 4 + 2 + w + 1): pix.set(x, y, '2')
# --- la cripta: nichos con calaveras y la verja final
for c in range(CRYPT + 2, 236, 6):
    for y in range(40, 64):
        for x in range(c * 4, c * 4 + 12):
            pix.set(x, y, '.' if y > 42 else '2')
    for (dx, dy) in ((4, 52), (5, 52), (7, 52), (8, 52), (5, 55), (6, 56), (7, 55)):
        pix.set(c * 4 + dx, dy, '2')
for y in range(16, 80):
    for x in range(238 * 4, 246 * 4):
        pix.set(x, y, '3' if (x % 4 == 0 or y % 16 == 0) else '.')
END_COL = 236
CHECK_COL = 138

csB = F.Charset(1, 127)
MAP = [[csB.code(F.cut(pix, c, r), cls[r][c]) for c in range(MCOLS)] for r in range(MROWS)]
print('minas: %d caracteres' % (csB.next - 1))

# --- techo de la cueva (filas 0-3, fijo)
sky = C(160, 32)
STAL = [6, 14, 9, 22, 11, 4, 17, 8, 12, 26, 7, 15, 10, 19, 5, 13]     # largo de cada estalactita (cada 10 px)
for x in range(160):
    k = x // 10; u = x % 10
    l = STAL[k % 16]
    w = 4 - abs(u - 5)
    for y in range(32):
        ch = '1' if y < 4 else '.'
        if y < 4 + l * max(0, w) // 4: ch = '1'
        if ch == '1' and u == 4 and y < 4 + l - 2: ch = '2'
        sky.set(x, y, ch)
csA = F.Charset(64, 64)
SKY = [[csA.code(F.cut(sky, c, r)) for c in range(40)] for r in range(4)]
# --- galería lejana (filas 4-6, media velocidad): paredes de sal y vagonetas
mtn = C(256, 24)
for x in range(256):
    top = 3 + int(3 * abs(((x % 64) - 32) / 32.0))
    for y in range(24):
        if y < top or y > 20: mtn.set(x, y, '1')
        elif (x * 3 + y * 5) % 17 == 0: mtn.set(x, y, '2')
for k in range(4):
    vx = k * 64 + 20
    for y in range(14, 19):
        for x in range(vx, vx + 14): mtn.set(x, y, '3')
    for x in (vx + 2, vx + 11): mtn.set(x, 19, '2'); mtn.set(x + 1, 19, '2')
for x in range(256): mtn.set(x, 20, '3')
csC = F.Charset(1, 127)
MTN = [[csC.code(F.cut(mtn, c, r)) for c in range(64)] for r in range(3)]
print('techo %d · galería %d' % (csA.next - 64, csC.next - 1))

BK  = [0x00, 0x00, 0x90, 0x90,  0x90, 0x90, 0x90,  0x92] + [0x90] * 10 + [0x90, 0x00, 0x00, 0x00]
PF0 = [0x94, 0x94, 0x94, 0x94,  0x96, 0x96, 0x96,  0x00] + [0x96] * 10 + [0x96, 0x96, 0x94, 0x00]
PF1 = [0x0E, 0x0E, 0x0E, 0x0C,  0x0C, 0x0C, 0x0C,  0x00] + [0x0E] * 10 + [0x0E, 0x0E, 0x0C, 0x00]
PF2 = [0x22, 0x22, 0x22, 0x22,  0x24, 0x24, 0x24,  0x00] + [0x26] * 10 + [0x26, 0x84, 0x82, 0x00]

SPAWN = []
for c in (34, 64, 112, 140, 178, 222):            # Moroi
    SPAWN.append((c - 30, 14, c + 6, 140))
for c in (44, 88, 124, 168, 208):                  # Vâlva Băii en el suelo
    SPAWN.append((c - 30, 15, c, (prof[c] or 10) * 8 + 104))
for c in (30, 76, 116, 156, 198):                  # estalactitas que caen
    SPAWN.append((c - 30, 17, c, 104))
SPAWN = [(max(4, a), b, c, d) for a, b, c, d in SPAWN]
SPAWN.sort(key=lambda e: e[0])
tramo.write_tramo(os.path.join(HERE, '..', 'src', 'tr_minas.s'), 'TR3', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, [0x0C] * 22, SPAWN, END_COL, CHECK_COL, 0xFF, 0,
                  'LAS MINAS DE SAL', 'Y LAS CRIPTAS', mus=1)

from PIL import Image
from pal import atari_rgb
def row_img(codes, cs, r):
    img = Image.new('RGB', (len(codes) * 4, 8)); px = img.load()
    pal = [atari_rgb(c) for c in (BK[r], PF0[r], PF1[r], PF2[r])]
    for c, code in enumerate(codes):
        for y in range(8):
            b = cs.data[code * 8 + y]
            for x in range(4): px[c * 4 + x, y] = pal[(b >> (6 - 2 * x)) & 3]
    return img
sheet = Image.new('RGB', (1280, 672))
for i, cc in enumerate((0, 50, 140, 200)):
    img = Image.new('RGB', (160, 168))
    for r in range(4): img.paste(row_img(SKY[r], csA, r), (0, r * 8))
    for r in range(3): img.paste(row_img([MTN[r][(cc // 2 + c) % 64] for c in range(40)], csC, 4 + r), (0, 32 + r * 8))
    img.paste(Image.new('RGB', (160, 8), atari_rgb(BK[7])), (0, 56))
    for r in range(13): img.paste(row_img(MAP[r][cc:cc + 40], csB, 8 + r), (0, 64 + r * 8))
    sheet.paste(img.resize((640, 336), Image.NEAREST), ((i % 2) * 640, (i // 2) * 336))
sheet.save(os.path.join(HERE, '..', 'build', 'min_hoja.png'))
