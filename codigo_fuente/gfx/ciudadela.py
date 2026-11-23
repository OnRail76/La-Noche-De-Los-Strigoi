#!/usr/bin/env python3
"""Fase 2: LAS CALLES DE LA CIUDADELA Y LAS TORRES DE LOS GREMIOS.
Calle empedrada, casas de entramado con tejados por los que se salta, pasarelas
de madera que se hunden (clase 3), torres de los gremios con gárgolas en lo alto.
Salida: ../src/tr_ciudadela.s"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import fase1 as F
from canvas import C, disc
import tramo

MCOLS, MROWS = 256, 13
W, H = MCOLS * 4, MROWS * 8
SURF = 10
pix = C(W, H)
cls = [[0] * MCOLS for _ in range(MROWS)]
random.seed(1847)

# --- calle empedrada (filas 10-12)
for x in range(W):
    for y in range(SURF * 8, H):
        yy = y - SURF * 8
        ch = '2'
        if yy == 0: ch = '3'
        elif (yy % 6 == 0) or ((x + (yy // 6) * 3) % 7 == 0): ch = '1'
        pix.set(x, y, ch)
for r in range(SURF, MROWS):
    for c in range(MCOLS): cls[r][c] = 1

def casa(c0, w, top, seed):
    """casa de entramado: fachada PF0, vigas PF2, ventanas encendidas PF1; tejado de tejas"""
    rnd = random.Random(seed)
    x0, x1 = c0 * 4, (c0 + w) * 4
    for y in range(top * 8, SURF * 8):
        for x in range(x0, x1):
            pix.set(x, y, '1')
    # tejado: alero de tejas (2 filas de píxel de borde + tejas)
    for x in range(x0 - 2, x1 + 2):
        for y in range(top * 8, top * 8 + 6):
            pix.set(x, y, '3' if (y - top * 8) < 2 or (x + y) % 4 else '2')
    # entramado
    for x in range(x0, x1, 12):
        for y in range(top * 8 + 6, SURF * 8):
            pix.set(x, y, '3')
    for y in range(top * 8 + 14, SURF * 8, 10):
        for x in range(x0, x1): pix.set(x, y, '3')
    # ventanas
    for wx in range(x0 + 4, x1 - 6, 12):
        wy = top * 8 + 8
        while wy + 7 < SURF * 8 - 4:
            lit = rnd.random() < 0.55
            for y in range(wy, wy + 6):
                for x in range(wx, wx + 4):
                    pix.set(x, y, '2' if lit else '.')
            for x in range(wx - 1, wx + 5): pix.set(x, wy + 6, '3')
            wy += 10
    # puerta
    dx = x0 + (w * 4) // 2 - 3
    for y in range(SURF * 8 - 12, SURF * 8):
        for x in range(dx, dx + 6):
            pix.set(x, y, '3' if x in (dx, dx + 5) or y == SURF * 8 - 12 else '.')
    for r in range(top, SURF):
        for c in range(c0, c0 + w): cls[r][c] = 1

def torre(c0, w, top, seed, door=False):
    """torre de gremio: piedra (PF0 con juntas), almenas y saetera; tejado en punta encima"""
    x0, x1 = c0 * 4, (c0 + w) * 4
    for y in range(top * 8, SURF * 8):
        for x in range(x0, x1):
            ch = '1'
            if y % 6 == 0 or (x + (y // 6) * 4) % 8 == 0: ch = '3'
            pix.set(x, y, ch)
    for x in range(x0 - 2, x1 + 2):                 # cornisa
        for y in range(top * 8, top * 8 + 3): pix.set(x, y, '3')
        pix.set(x, top * 8, '2')
    for y in range(top * 8 + 10, SURF * 8 - 10, 16):   # saeteras con luz
        cx = (x0 + x1) // 2
        for yy in range(y, y + 8):
            pix.set(cx - 1, yy, '2'); pix.set(cx, yy, '2')
    for r in range(top, SURF):
        for c in range(c0, c0 + w): cls[r][c] = 1
    if door:                                        # paso abierto en la calle: nunca quedas encerrado
        for y in range(SURF * 8 - 30, SURF * 8):
            for x in range(x0, x1):
                arch = y < SURF * 8 - 24 and abs(x - (x0 + x1) // 2) > (y - (SURF * 8 - 30)) * 2 + 8
                pix.set(x, y, '3' if arch or x in (x0, x1 - 1) else '.')
        for r in range(SURF - 3, SURF):
            for c in range(c0, c0 + w): cls[r][c] = 0

def pasarela(c0, c1, row):
    """pasarela de tablas entre tejados: se hunde si te quedas encima (clase 3)"""
    for c in range(c0, c1):
        cls[row][c] = 3
        for x in range(c * 4, c * 4 + 4):
            for y in range(row * 8, row * 8 + 5):
                pix.set(x, y, '2' if y == row * 8 else ('3' if (x % 6) and y < row * 8 + 4 else '.'))
        for y in range(row * 8 + 5, row * 8 + 8):          # cuerdas / soportes
            if c % 3 == 0: pix.set(c * 4 + 1, y, '3')

def farol(c, row):
    x = c * 4 + 1
    for y in range(row * 8, SURF * 8): pix.set(x, y, '3'); pix.set(x + 1, y, '3')
    for y in range(row * 8 - 6, row * 8):
        for xx in range(x - 1, x + 3): pix.set(xx, y, '2' if y > row * 8 - 5 else '3')

# --- recorrido (columna, ancho, fila del tejado): desde la calle solo se sube a tejados de la fila 6
def chimenea(c, top):
    for y in range(top * 8 - 7, top * 8):
        for x in range(c * 4, c * 4 + 4):
            pix.set(x, y, '3' if y > top * 8 - 6 else '2')
farol(10, 6)
casa(18, 10, 6, 1); chimenea(21, 6)
casa(28, 10, 4, 2); chimenea(34, 4)
pasarela(38, 48, 4)              # sobre un callejón
casa(48, 10, 6, 3)
casa(58, 8, 5, 13)
torre(66, 8, 2, 4)               # torre de los herreros (gárgola)
casa(74, 10, 5, 5); chimenea(80, 5)
farol(88, 6)
casa(92, 10, 6, 6)
casa(102, 8, 4, 14); chimenea(105, 4)
pasarela(110, 120, 4)
casa(120, 8, 6, 7)
# plaza del punto de control (calle libre)
farol(134, 6)
casa(146, 10, 6, 8); chimenea(150, 6)
casa(156, 8, 4, 9)
pasarela(164, 174, 4)
torre(174, 8, 2, 10, door=True)             # torre de los zapateros (gárgola)
pasarela(182, 192, 3)
casa(192, 10, 6, 11)
casa(202, 10, 4, 12); chimenea(207, 4)
farol(222, 6)
# Torre de los Sastres (final): puerta abierta en la calle
TS = 240
for y in range(0, SURF * 8):
    for x in range(TS * 4, W):
        ch = '1'
        if y % 6 == 0 or (x + (y // 6) * 4) % 8 == 0: ch = '3'
        pix.set(x, y, ch)
for y in range(SURF * 8 - 26, SURF * 8):
    for x in range(TS * 4 + 4, TS * 4 + 20):
        arch = y < SURF * 8 - 20 and abs(x - (TS * 4 + 12)) > (y - (SURF * 8 - 26)) + 2
        pix.set(x, y, '3' if arch else '.')
for y in range(8, 30):
    for x in range(TS * 4 + 30, TS * 4 + 34): pix.set(x, y, '2' if (y // 4) % 2 else '3')
END_COL = 238
CHECK_COL = 140

csB = F.Charset(1, 127)
MAP = [[csB.code(F.cut(pix, c, r), cls[r][c]) for c in range(MCOLS)] for r in range(MROWS)]
print('ciudadela: %d caracteres' % (csB.next - 1))

# --- cielo: el mismo de la fase 1 (luna y la Torre del Reloj a lo lejos)
csA = F.Charset(64, 64)
SKY = [[csA.code(F.cut(F.sky, c, r)) for c in range(40)] for r in range(4)]
# --- tejados lejanos (filas 4-6, media velocidad)
mtn = C(256, 24)
rnd = random.Random(5)
x = 0
while x < 256:
    w = rnd.randrange(14, 30)
    top = rnd.randrange(4, 12)
    peak = rnd.random() < 0.4
    for xx in range(x, min(256, x + w)):
        t = top
        if peak:
            t = top - 6 + abs(xx - (x + w // 2)) * 12 // w
        for y in range(max(0, t), 24):
            mtn.set(xx, y, '3')
    # ventanas encendidas
    for k in range(rnd.randrange(1, 4)):
        wx, wy = x + rnd.randrange(2, max(3, w - 3)), rnd.randrange(top + 3, 20)
        mtn.set(wx, wy, '2'); mtn.set(wx, wy + 1, '2')
    x += w
for x in range(0, 256, 64):                         # torres puntiagudas
    for y in range(24):
        hw = max(0, (y - 0) // 3)
        for xx in range(x + 30 - hw, x + 31 + hw):
            if y < 12 or abs(xx - x - 30) < 3: mtn.set(xx % 256, y, '1' if y < 12 else '3')
csC = F.Charset(1, 127)
MTN = [[csC.code(F.cut(mtn, c, r)) for c in range(64)] for r in range(3)]
print('cielo %d · tejados %d' % (csA.next - 64, csC.next - 1))

BK  = F.BK[:7] + [0x74] + [0x72] * 10 + [0x02, 0x02, 0x00, 0x00]
PF0 = F.PF0[:4] + [0x34, 0x34, 0x34, 0x00] + [0x2A] * 10 + [0x06, 0x06, 0x04, 0x00]
PF1 = F.PF1[:4] + [0x1C, 0x1C, 0x1C, 0x00] + [0x1E] * 10 + [0x0A, 0x0A, 0x08, 0x00]
PF2 = F.PF2[:4] + [0x50, 0x50, 0x50, 0x00] + [0x34] * 10 + [0x04, 0x04, 0x02, 0x00]
PF0[11] = PF0[12] = 0x08       # filas altas: piedra de las torres más clara contra el cielo

SPAWN = []
for gc, top in ((66, 2), (174, 2), (29, 4), (203, 4)):   # gárgolas en torres y tejados
    SPAWN.append((gc - 34, 10, gc + 3, 104 + top * 8))
for c in (60, 112, 170, 222):                       # Iele que llegan volando
    SPAWN.append((c - 30, 9, c + 8, 112))
for c in (14, 86, 128, 140, 216):                   # zombis de la calle
    SPAWN.append((c - 20, 1, c, 0))
SPAWN = [(max(4, a), b, c, d) for a, b, c, d in SPAWN]
SPAWN.sort(key=lambda e: e[0])
tramo.write_tramo(os.path.join(HERE, '..', 'src', 'tr_ciudadela.s'), 'TR2', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, [0x0C] * 22, SPAWN, END_COL, CHECK_COL, 0xFF, 1,
                  'LA CIUDADELA', 'TORRES DE GREMIOS')

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
sheet.save(os.path.join(HERE, '..', 'build', 'ciu_hoja.png'))
