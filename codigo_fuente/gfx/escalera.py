#!/usr/bin/env python3
"""Fase 1, tramo 2: el interior de la Escalera Cubierta (Scara Acoperită).
Tramos de peldaños de 8 px (Radu los sube andando), rellanos, tablones rotos
y vigas de las que cuelgan murciélagos. Salida: ../src/tr_escalera.s"""
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
pix = C(W, H)
cls = [[0] * MCOLS for _ in range(MROWS)]

# --- perfil: fila de la superficie por columna (los peldaños se insertan solos)
SEQ = [(10, 18), (6, 16), (4, 12), (9, 8), (5, 16), (3, 10), (8, 8), (6, 12), (4, 12),
       (10, 10), (7, 12), (4, 12), (8, 8), (5, 14), (4, 999)]
prof = []
cur = None
for h, n in SEQ:
    if cur is not None and h < cur:
        for s in range(cur - 1, h - 1, -1):        # subida: un peldaño (2 columnas) por fila
            prof += [s, s]
    cur = h
    prof += [h] * n
prof = (prof + [4] * MCOLS)[:MCOLS]
END_COL = 238
# punto de control: el rellano a ras de suelo (fila 10) de la mitad del tramo
CHECK_COL = [c for c in range(100, 200) if prof[c] == 10 and prof[c - 4] == 10][0] + 6

# --- pared del fondo: tablones verticales (PF0 = juntas azuladas)
random.seed(7)
for x in range(W):
    for y in range(H):
        if x % 16 == 0 or (x % 16 == 8 and (y // 8 + x // 16) % 3 == 0):
            pix.set(x, y, '1')
# vigas de atar en la fila 0-1 cada 24 columnas, con tornapuntas
BEAMS = list(range(6, MCOLS, 24))
for c in range(MCOLS * 4):
    pix.set(c, 0, '3'); pix.set(c, 1, '2'); pix.set(c, 2, '3')    # larguero bajo el tejado
for b in BEAMS:
    x0 = b * 4
    for y in range(0, 12):
        for x in range(x0, x0 + 8):
            pix.set(x, y, '3' if y < 10 else '2')
    for i in range(8):                                             # tornapuntas
        pix.set(x0 - 1 - i, 3 + i, '3'); pix.set(x0 - 2 - i, 3 + i, '3')
        pix.set(x0 + 8 + i, 3 + i, '3'); pix.set(x0 + 9 + i, 3 + i, '3')
# --- escalera: superficie (tablón) y estructura bajo ella
for c in range(MCOLS):
    h = prof[c]
    rotos = c > 0 and prof[c - 1] < h and prof[c - 1] <= 6     # borde de un rellano roto
    for r in range(h, MROWS):
        cls[r][c] = 1
        for y in range(8):
            for x in range(4):
                X, Y = c * 4 + x, r * 8 + y
                if r == h:
                    ch = '2' if y == 0 else '3' if y < 4 else ('1' if y == 4 else '.')
                    if y >= 5 and (X % 8 in (0, 1)):
                        ch = '3'
                else:
                    ch = '3'                     # costado de tablas bajo los peldaños
                    if y == 7 or X % 16 == 0:
                        ch = '1'
                    if y == 0 and X % 16 == 8:
                        ch = '2'
                    if r >= MROWS - 2:           # suelo de piedra al pie de la colina
                        ch = '1' if (X // 8 + Y // 4) % 2 == 0 and y % 4 == 0 else '.'
                        if y in (0,):
                            ch = '2'
                pix.set(X, Y, ch)
    # tablones astillados al final de un rellano que se corta
    if c + 1 < MCOLS and prof[c + 1] > h and h <= 6:
        for y in range(0, 4):
            for x in range(4):
                if (x + y) % 3 == 2: pix.set(c * 4 + x, h * 8 + y, '.')
# barandilla sobre los peldaños (pasamanos PF1 inclinado)
for c in range(1, MCOLS):
    h = prof[c]
    y = h * 8 - 14
    if y > 8:
        for x in range(4):
            pix.set(c * 4 + x, y - (x // 2 if prof[c - 1] > h else 0), '2')
        if c % 4 == 0:
            for yy in range(y, h * 8):
                pix.set(c * 4 + 1, yy, '3')
# puerta de salida a la Iglesia de la Colina (columna 240)
dx = 240 * 4
for y in range(1 * 8, 4 * 8):
    for x in range(dx, dx + 20):
        e = x - dx in (0, 1, 18, 19) or y < 8 + 3
        pix.set(x, y, '3' if e else ('2' if (x - dx) % 6 == 3 else '.'))

csB = F.Charset(1, 127)
MAP = [[csB.code(F.cut(pix, c, r), cls[r][c]) for c in range(MCOLS)] for r in range(MROWS)]
print('escalera: %d caracteres' % (csB.next - 1))

# --- techo (filas 0-3, fijo): tablas del tejado vistas desde dentro
sky = C(160, 32)
for y in range(32):
    for x in range(160):
        ch = '.'
        if y % 8 == 7: ch = '1'
        elif y % 8 == 0: ch = '2'
        if y >= 24 and (x % 40) < 6: ch = '3'          # cabios
        if y >= 24 and (x % 40) == 6: ch = '1'
        sky.set(x, y, ch)
csA = F.Charset(64, 64)
SKY = [[csA.code(F.cut(sky, c, r)) for c in range(40)] for r in range(4)]
# --- pared lejana (filas 4-6, media velocidad): ventanales con la luna y la ciudad
mtn = C(256, 24)
for y in range(24):
    for x in range(256):
        mtn.set(x, y, '3' if x % 8 == 0 else '.')
for k in range(4):
    wx = k * 64 + 18
    for y in range(3, 22):
        for x in range(wx, wx + 28):
            mtn.set(x, y, '1')
    for x in range(wx, wx + 28):
        mtn.set(x, 3, '3'); mtn.set(x, 21, '3'); mtn.set(x, 12, '3')
    for y in range(3, 22):
        mtn.set(wx, y, '3'); mtn.set(wx + 27, y, '3'); mtn.set(wx + 14, y, '3')
    # tejados de la ciudad tras el cristal
    for x in range(wx + 1, wx + 27):
        top = 16 - ((x * 7 + k * 3) % 5)
        for y in range(top, 21):
            mtn.set(x, y, '2')
    if k == 1:
        for y in range(5, 10):
            for x in range(wx + 4, wx + 9):
                mtn.set(x, y, '2')
csC = F.Charset(1, 127)
MTN = [[csC.code(F.cut(mtn, c, r)) for c in range(64)] for r in range(3)]
print('techo %d · pared %d' % (csA.next - 64, csC.next - 1))

# colores por fila (0-20) + 21
BK  = [0x00, 0x00, 0x00, 0x00,  0x02, 0x02, 0x02,  0x32] + [0x70] * 10 + [0x70, 0x02, 0x02, 0x00]
PF0 = [0x32, 0x32, 0x32, 0x32,  0x84, 0x84, 0x86,  0x00] + [0x72] * 10 + [0x72, 0x04, 0x04, 0x00]
PF1 = [0x34, 0x34, 0x34, 0x34,  0x08, 0x0A, 0x0A,  0x00] + [0x3C] * 10 + [0x3C, 0x08, 0x08, 0x00]
PF2 = [0x22, 0x22, 0x22, 0x22,  0x32, 0x32, 0x32,  0x00] + [0x34] * 10 + [0x34, 0x06, 0x06, 0x00]

# apariciones: murciélagos colgados de las vigas (tipo 6) y algún zombi en los rellanos bajos
SPAWN = []
for b in BEAMS[1:]:
    if b < END_COL - 4:
        SPAWN.append((max(4, b + 1 - 36), 6, b + 1, 104 + 12))
for c in range(30, 230):
    if prof[c] == 10 and prof[c - 1] != 10:
        SPAWN.append((max(4, c + 4 - 30), 1, c + 4, 0))
SPAWN.sort()
assert len(SPAWN) <= 32
tramo.write_tramo(os.path.join(HERE, '..', 'src', 'tr_escalera.s'), 'TR1', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, [0x0C] * 22, SPAWN, END_COL, CHECK_COL, 0xFF, 0,
                  'LA ESCALERA', 'CUBIERTA', mus=1)
print('control en', CHECK_COL, 'apariciones', len(SPAWN))

# vista previa
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
for cc in (0, 60, 130, 200):
    img = Image.new('RGB', (160, 168))
    for r in range(4): img.paste(row_img(SKY[r], csA, r), (0, r * 8))
    for r in range(3): img.paste(row_img([MTN[r][(cc // 2 + c) % 64] for c in range(40)], csC, 4 + r), (0, 32 + r * 8))
    img.paste(Image.new('RGB', (160, 8), atari_rgb(BK[7])), (0, 56))
    for r in range(13): img.paste(row_img(MAP[r][cc:cc + 40], csB, 8 + r), (0, 64 + r * 8))
    img.resize((640, 336), Image.NEAREST).save(os.path.join(HERE, '..', 'build', 'esc_%03d.png' % cc))
