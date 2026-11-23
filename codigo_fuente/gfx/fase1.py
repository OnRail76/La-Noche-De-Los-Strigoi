#!/usr/bin/env python3
"""LA NOCHE DE LOS STRIGOI · Fase 1 (El Cementerio de la Colina)

Genera todos los datos de la fase a partir de dibujos en texto:
  - juego de caracteres A: fuente (0-63) + cielo, luna, ciudadela y montañas (64-127)
  - juego de caracteres B: cementerio (0-127)
  - mapa de 13 filas x 256 columnas (una página por fila) y clase de cada carácter
  - sprites de Radu (P0+P1 en modo OR), zombi, cuervo, nube de golpe y baltag (quinto player)
  - colores por fila (DLI) y lista de apariciones
Salida: ../src/data.s y vistas previas en ../build/
Píxeles: '.' fondo (COLBK) · '1' PF0 · '2' PF1 · '3' PF2
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from canvas import C, disc, stroke, bez
from pal import atari_rgb
import font

ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'src', 'data.s')
PREV = os.path.join(ROOT, 'build')
os.makedirs(PREV, exist_ok=True)

# ---------------------------------------------------------------
# Colores por fila del campo (0-20) + entrada 21 (debajo del campo)
#   filas 0-3 cielo fijo · 4-6 montañas (parallax 1/2) · 7 niebla del valle
#   filas 8-17 cementerio · 18 hierba · 19-20 tierra
# ---------------------------------------------------------------
ROWS = 21
BK  = [0x70, 0x70, 0x72, 0x72,  0x74, 0x74, 0x76,  0x76,
       0x72, 0x72, 0x72, 0x72, 0x72, 0x74, 0x74, 0x74, 0x74, 0x74,
       0x20, 0x10, 0x10,  0x00]
PF0 = [0x0A, 0x0A, 0x28, 0x28,  0x62, 0x62, 0x62,  0x00,
       0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
       0xC4, 0x22, 0x22,  0x00]
PF1 = [0x0E, 0x0E, 0x0E, 0x0C,  0x0C, 0x0A, 0x08,  0x00,
       0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A,
       0x0A, 0x0C, 0x0C,  0x00]
PF2 = [0x60, 0x60, 0x60, 0x60,  0x50, 0x50, 0x50,  0x00,
       0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
       0x24, 0x24, 0x34,  0x00]
COL_PF3 = 0x0C          # baltag (quinto player)
COL_P0 = 0x24           # Radu: chaqueta, gorro, pantalón
COL_P1 = 0x0C           # Radu: camisa (P0|P1 = $2C, la piel)
COL_ZOMBI = 0xC8
COL_CUERVO = 0x02
COL_PUFF = 0x3C

GROUND_ROW0 = 8          # primera fila del cementerio en pantalla
MROWS = 13               # filas del mapa (8-20)
MCOLS = 256
SURF = 10                # fila del mapa con la superficie del suelo (pantalla 18)

# ---------------------------------------------------------------
def to_bytes(cell):        # cell: lista de 8 cadenas de 4 píxeles '.123'
    out = []
    for row in cell:
        b = 0
        for ch in row:
            b = (b << 2) | ('.123'.index(ch))
        out.append(b)
    return bytes(out)


class Charset:
    def __init__(s, first, size):
        s.first, s.size = first, size
        s.cells = {}          # (bytes, clase) -> código
        s.data = bytearray(1024)
        s.cls = [0] * 128
        s.next = first

    def code(s, cell, cls=0):
        b = to_bytes(cell)
        if b == bytes(8) and cls == 0:
            return 0
        k = (b, cls)
        if k not in s.cells:
            assert s.next < s.first + s.size, 'juego de caracteres lleno (%d)' % s.size
            s.cells[k] = s.next
            s.data[s.next * 8:s.next * 8 + 8] = b
            s.cls[s.next] = cls
            s.next += 1
        return s.cells[k]


def cut(canvas, cx, cy):
    return [''.join(canvas.p[cy * 8 + y][cx * 4 + x] for x in range(4)) for y in range(8)]


def art(txt):
    return C.rows(txt)

# ===============================================================
# CIELO (filas 0-3, fijo) · LUNA, ESTRELLAS Y LA CIUDADELA
# ===============================================================
random.seed(1847)
sky = C(160, 32)
# estrellas (PF1 blanco; algunas PF0 en las filas 0-1)
for i in range(34):
    x, y = random.randrange(160), random.randrange(30)
    sky.set(x, y, '2' if y < 16 or random.random() < .5 else '2')
# luna llena con mares (filas 0-1)
for y in range(16):
    for x in range(40):
        pass
disc(sky, 30, 8.5, 7.2, '2')
for (mx, my, r) in ((28, 6, 2.2), (32, 10, 1.8), (27, 11, 1.3), (33, 6, 1.0)):
    disc(sky, mx, my, r, '1')
# borra estrellas sobre la luna
# ciudadela de Sighisoara a la derecha (silueta PF2, ventanas PF0)
cit = C(64, 24)
cit.rect(0, 18, 63, 23, '3')                       # colina
for x in range(64):                               # perfil de la colina
    h = int(4 + 3 * abs(((x - 30) / 34.0)) ** 1.5 * 2)
    for y in range(14 + min(h, 8), 18):
        cit.set(x, y, '3')
cit.rect(4, 13, 58, 18, '3')                       # muralla
for x in range(4, 59, 4):
    cit.set(x, 12, '3'); cit.set(x + 1, 12, '3')   # almenas
# Torre del Reloj
cit.rect(26, 2, 33, 18, '3')
for y in range(0, 6):                             # tejado piramidal
    w = 4 - (y * 4) // 6
    for x in range(30 - w, 30 + w):
        cit.set(x, y - 4 + 6 - 2, '3') if False else None
cit.line(26, 2, 29, -6, '3'); cit.line(33, 2, 30, -6, '3')
for yy in range(-6, 3):
    for x in range(26, 34):
        pass
# relleno del tejado (triángulo)
for y in range(0, 3):
    pass
roof = [(29, 30), (28, 31), (28, 31), (27, 32), (27, 32)]
# torretas de las esquinas
for tx in (25, 34):
    cit.set(tx, 1, '3'); cit.set(tx, 2, '3'); cit.set(tx, 0, '3')
# ventanas encendidas de la torre
cit.set(29, 7, '1'); cit.set(30, 7, '1'); cit.set(29, 11, '1')
# Iglesia de la Colina (izquierda, más alta en la colina)
cit.rect(6, 6, 15, 13, '3')
cit.line(6, 6, 10, 1, '3'); cit.line(15, 6, 11, 1, '3')
for y in range(1, 7):
    for x in range(6, 16):
        if abs(x - 10.5) <= (y - 1) * 0.9 + 0.5:
            cit.set(x, y, '3')
cit.rect(16, 4, 18, 13, '3'); cit.set(17, 2, '3'); cit.set(17, 3, '3')   # campanario
# torres de los gremios y casas
for (x0, w, top) in ((38, 4, 8), (44, 5, 10), (51, 4, 7), (20, 4, 10), (56, 5, 11)):
    cit.rect(x0, top, x0 + w - 1, 13, '3')
    for y in range(top - 3, top):
        for x in range(x0, x0 + w):
            if abs(x - (x0 + (w - 1) / 2)) <= (y - (top - 3)) * 0.8 + 0.3:
                cit.set(x, y, '3')
for (wx, wy) in ((40, 10), (46, 12), (52, 9), (22, 12), (57, 13), (9, 10), (12, 10), (36, 15), (48, 16), (14, 15)):
    cit.set(wx, wy, '1')
# tejado de la torre del reloj (triángulo sobre y=2)
for y in range(-6, 2):
    pass
sky_cit_y = 8                                       # fila del cielo donde empieza la silueta
for y in range(cit.h):
    for x in range(cit.w):
        if cit.p[y][x] != '.':
            sky.set(92 + x, sky_cit_y + y, cit.p[y][x])
# tejado de la Torre del Reloj, dibujado sobre el cielo
for y in range(0, 8):
    half = y * 0.55
    for x in range(118 - 1, 128 + 1):
        if abs(x - 121.5) <= half:
            sky.set(x, sky_cit_y - 8 + y + 2, '3')
for tx in (117, 126):                                # agujas de las esquinas
    for y in range(sky_cit_y + 1, sky_cit_y + 6):
        sky.set(tx, y, '3')
sky.set(121, sky_cit_y - 7, '3'); sky.set(122, sky_cit_y - 7, '3')

# ===============================================================
# MONTAÑAS (filas 4-6, anillo de 64 columnas = 256 píxeles, se repite)
# ===============================================================
mtn = C(256, 24)
random.seed(7)
def ridge(base, amp, freq, phase):
    import math
    return [base - amp * (0.6 * math.sin(x * freq + phase) + 0.4 * math.sin(x * freq * 2.7 + phase * 1.9))
            for x in range(256)]
import math
# Cárpatos lejanos: picos
peaks = [(18, 2), (52, 6), (84, 0), (120, 5), (150, 1), (186, 7), (214, 2), (240, 5)]
far = [24.0] * 256
for (px, ph) in peaks:
    for x in range(256):
        for k in (-256, 0, 256):
            d = abs(x - px - k)
            far[x] = min(far[x], ph + d * 0.75)
for x in range(256):
    top = int(far[x])
    for y in range(max(top, 0), 24):
        mtn.set(x, y, '1')
    # nieve en las cumbres
    for y in range(max(top, 0), min(top + 3, 24)):
        if y < 7 and y - max(top, 0) < 2 + (x % 3 == 0):
            mtn.set(x, y, '2')
# colinas boscosas cercanas (PF2), con abetos
near = [17 + 2.5 * math.sin(x * 2 * math.pi / 128) + 1.5 * math.sin(x * 2 * math.pi / 64 + 1) for x in range(256)]
for x in range(256):
    for y in range(int(near[x]), 24):
        mtn.set(x, y, '3')
random.seed(11)
for i in range(40):
    x = random.randrange(256)
    t = int(near[x]) - random.randrange(2, 5)
    for y in range(t, int(near[x]) + 1):
        w = (y - t) // 2
        for dx in range(-w, w + 1):
            mtn.set((x + dx) % 256, y, '3')

# ===============================================================
# CEMENTERIO: objetos en texto
# ===============================================================
LAPIDA = art("""
..2222..
.211112.
21111112
21133112
21133112
21333312
21133112
21133112
21133112
21111112
21111112
21111112
21111112
21111112
31111113
33333333
""")
LAPIDA2 = art("""
........
........
...22...
...22...
.222222.
.211112.
...21...
...21...
...21...
...21...
...21...
...21...
...21...
...21...
..2211..
.333333.
""")
CRUZ_ALTA = art("""
....22......
....21......
..222122....
..211111....
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
....21......
...2211.....
..222111....
.22221111...
333333333...
""")
# sarcófago de piedra: sólido, se puede subir encima
SARCOFAGO = art("""
2222222222222222
2111111111111112
3333333333333333
.21111111111112.
.21311131113112.
.21311131113112.
.21111111111112.
.21111111111112.
.21311131113112.
.21311131113112.
.21111111111112.
.21111111111112.
.21111111111112.
.21111111111112.
2111111111111112
3333333333333333
""")
# panteón (cripta): sólido, 6 columnas x 4 filas
CRIPTA = art("""
..........22............
.........2112...........
........211112..........
.......21111112.........
......2111111112........
.....211113311112.......
....21111133111112......
...2111111111111112.....
..222222222222222222....
..311111111111111113....
..322222222222222223....
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33.33.33.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33.33.33.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
...2112.33333333.2112...
..222222222222222222....
..211111111111111112....
.22222222222222222222...
.21111111111111111112...
.21111111111111111112...
3333333333333333333333..
""")
# murete de piedra (sólido), módulo de 8 px x 16
MURO = art("""
22222222
21112111
21112111
33333333
11211121
11211121
33333333
21112111
21112111
33333333
11211121
11211121
33333333
21112111
21112111
33333333
""")
# verja de hierro, módulo de 4 px x 16
VERJA = art("""
.3..
333.
.3..
.3..
3333
.3..
.3..
.3..
.3..
.3..
.3..
.3..
3333
.3..
.3..
.3..
""")
# escalera cubierta (final del tramo): madera (PF2) y tejado de tablas
def escalera(W=120):
    """Escalera Cubierta hasta el borde del mapa: tejado de tablas, postes,
    peldaños que suben hasta un rellano y barandilla (todo alineado a rejilla)"""
    c = C(W, 64)
    for y in range(0, 12):                      # tejado de tablas
        for x in range(W):
            c.set(x, y + 4, '3' if (y % 4) else '1')
    for x in range(0, W, 4):
        c.set(x, 4, '2')
    for px in range(0, W, 20):                  # postes cada 5 columnas
        for y in range(16, 64):
            for dx in range(4):
                c.set(px + dx, y, '3' if dx in (1, 2) else '.')
    def step(col, row):                         # bloque de peldaño de 2 columnas
        for k in range(2):
            x0 = (col * 2 + k) * 4
            if x0 >= W:
                continue
            for x in range(4):
                c.set(x0 + x, row * 8, '2')
                c.set(x0 + x, row * 8 + 1, '1')
                for y in range(row * 8 + 2, 64):
                    if (y % 8) == 7:
                        c.set(x0 + x, y, '3')
    for i in range(5):                          # tramo de subida
        step(1 + i, 7 - i)
    for col in range(6, W // 8 + 1):            # rellano hasta el final
        step(col, 3)
    return c
ESCALERA = escalera()

def arbol(seed, w=24, h=72):
    random.seed(seed)
    c = C(w, h)
    cx = w // 2
    trunk = [(cx - 1, h - 1), (cx + random.choice((-2, 2)), h * 0.7), (cx, h * 0.45), (cx + random.choice((-3, 3)), h * 0.25)]
    for (a, b) in zip(trunk, trunk[1:]):
        stroke(c, list(bez(a, ((a[0] + b[0]) / 2 + 1, (a[1] + b[1]) / 2), b, 6)), 1.5, '3')
    stroke(c, [(cx - 3, h - 1), (cx, h - 6)], 1.3, '3')
    stroke(c, [(cx + 3, h - 1), (cx + 1, h - 6)], 1.3, '3')
    # ramas retorcidas
    for i in range(5):
        y = h * (0.18 + 0.1 * i)
        side = -1 if i % 2 else 1
        x1 = cx + side * random.randint(7, w // 2 - 1)
        y1 = y - random.randint(6, 14)
        x2 = x1 + side * random.randint(-3, 3)
        y2 = y1 - random.randint(3, 8)
        stroke(c, list(bez((cx, y), ((cx + x1) / 2, y - 2), (x1, y1), 5)), 0.6, '3')
        stroke(c, [(x1, y1), (x2, y2)], 0.4, '3')
        stroke(c, [(x1, y1), (x1 + side * 3, y1 + 2)], 0.3, '3')
    # luz de luna en la corteza
    for y in range(h):
        for x in range(w):
            if c.p[y][x] == '3' and c.get(x - 1, y) == '.' and c.get(x + 1, y) == '3' and (y % 3) and y > h * 0.35:
                c.set(x, y, '1')
    return c

# ---------------------------------------------------------------
# Suelo: superficie (fila 10 del mapa) y tierra (11-12)
# ---------------------------------------------------------------
HIERBA = [art("""
1..1..1.
11.111.1
11111111
.1.11.11
........
...3....
........
.....3..
"""), art("""
.1....1.
.11.1.11
11111111
11.1.111
........
..3.....
......3.
........
"""), art("""
1...1...
11.111.1
11111111
1.1111.1
........
........
....3...
.3......
""")]
TIERRA = [art("""
........
..1.....
........
.....1..
........
.1......
......1.
........
"""), art("""
........
.....1..
.1......
........
...3....
........
.....1..
..1.....
"""), art("""
..3.....
........
.....1..
........
.1......
........
....1...
........
""")]
CALAVERA = art("""
..2222..
.222222.
.2..2..2
.222222.
..2.2.2.
........
.1......
........
""")
HUESOS = art("""
........
........
2.....2.
.22222..
2.....2.
........
...1....
........
""")
RAICES = art("""
...3....
....3...
....3...
...3.3..
..3...3.
.3......
........
........
""")

# ===============================================================
# MAPA
# ===============================================================
W = MCOLS * 4
H = MROWS * 8
pix = C(W, H)
cls = [[0] * MCOLS for _ in range(MROWS)]
SOLID, PLAT = 1, 2

def place(o, col, row_bottom, c=0, solid_rows=None):
    """coloca el objeto con su base en la fila row_bottom (incluida), alineado a columna"""
    rows = o.h // 8
    top = row_bottom - rows + 1
    for y in range(o.h):
        for x in range(o.w):
            ch = o.p[y][x]
            if ch != '.':
                pix.set(col * 4 + x, top * 8 + y, ch)
    if c:
        for r in range(top, row_bottom + 1):
            for cc in range(col, col + (o.w + 3) // 4):
                if solid_rows is None or (r - top) in solid_rows:
                    cls[r][cc] = c

# suelo
random.seed(3)
for col in range(MCOLS):
    g = HIERBA[random.randrange(3)]
    # dos columnas por baldosa de 8 píxeles
    for x in range(4):
        for y in range(8):
            pix.set(col * 4 + x, SURF * 8 + y, g.p[y][(col % 2) * 4 + x])
    for r in (SURF + 1, SURF + 2):
        t = random.choice(TIERRA)
        if random.random() < 0.05: t = CALAVERA
        elif random.random() < 0.05: t = HUESOS
        elif random.random() < 0.06: t = RAICES
        for x in range(4):
            for y in range(8):
                pix.set(col * 4 + x, r * 8 + y, t.p[y][(col % 2) * 4 + x])
    for r in (SURF, SURF + 1, SURF + 2):
        cls[r][col] = SOLID

B = SURF - 1      # fila del mapa justo encima del suelo
# --- tramo A: entrada al cementerio (columnas 0-40)
for c in range(0, 14):
    place(VERJA, c, B)
place(LAPIDA, 6, B)
ARBOL = arbol(5)
place(ARBOL, 16, B)
place(LAPIDA2, 26, B)
place(ARBOL, 40, B)
place(LAPIDA, 31, B)
place(CRUZ_ALTA, 36, B)
# --- tramo B: lápidas y primer sarcófago (40-90)
place(SARCOFAGO, 44, B, SOLID)
place(LAPIDA, 52, B)
place(LAPIDA2, 57, B)
place(ARBOL, 62, B)
place(LAPIDA, 72, B)
place(SARCOFAGO, 78, B, SOLID)
place(LAPIDA2, 86, B)
# --- tramo C: muretes y el panteón (90-140)
for c in range(94, 102, 2):
    place(MURO, c, B, SOLID)
place(LAPIDA, 96, B - 2)
place(CRIPTA, 104, B, SOLID)
place(LAPIDA2, 112, B)
place(CRUZ_ALTA, 116, B)
place(ARBOL, 124, B)
# punto de control (columna 136): una cruz alta
place(LAPIDA, 134, B)
# --- tramo D: subida por muretes y sarcófagos (140-200)
place(SARCOFAGO, 146, B, SOLID)
for c in range(154, 160, 2):
    place(MURO, c, B, SOLID)
place(SARCOFAGO, 156, B - 2, SOLID)
place(LAPIDA, 166, B)
place(ARBOL, 160, B)
place(ARBOL, 170, B)
place(LAPIDA2, 180, B)
place(CRUZ_ALTA, 184, B)
place(SARCOFAGO, 192, B, SOLID)
place(LAPIDA, 200, B)
place(ARBOL, 196, B)
# --- tramo E: verja y la Escalera Cubierta (200-256)
for c in range(206, 220):
    place(VERJA, c, B)
place(LAPIDA2, 210, B)
place(CRUZ_ALTA, 214, B)
place(ESCALERA, 226, B)

END_COL = 236          # al llegar aquí, fin del tramo
CHECK_COL = 136        # punto de control
# lápida de la columna 96 apoyada en el muro: ya está dibujada encima

# ---------------------------------------------------------------
# juego de caracteres B a partir del mapa
# ---------------------------------------------------------------
csB = Charset(1, 127)
MAP = [[0] * MCOLS for _ in range(MROWS)]
for r in range(MROWS):
    for c in range(MCOLS):
        MAP[r][c] = csB.code(cut(pix, c, r), cls[r][c])
print('cementerio: %d caracteres' % (csB.next - 1))

# juego A: fuente + cielo + montañas
csA = Charset(64, 64)
fb = font.font_bytes()
csA.data[0:512] = fb[0:512]
SKY = [[csA.code(cut(sky, c, r)) for c in range(40)] for r in range(4)]
csC = Charset(1, 127)
MTN = [[csC.code(cut(mtn, c, r)) for c in range(64)] for r in range(3)]
print('cielo: %d caracteres · montañas: %d' % (csA.next - 64, csC.next - 1))
for code in csA.cells.values():
    pass
# los códigos 64-127 del juego A en ANTIC 4 no deben chocar con la fuente: no la usan

# ===============================================================
# SPRITES
# ===============================================================
# Radu (8 px de ancho, 24 líneas). h = P0 (gorro, pelo, pantalón), j = chaqueta (P0; sin chaqueta, P1)
# w = camisa (P1), s = piel (P0+P1), k = bigote/ojo (P0)
RADU = {}
RADU['quieto'] = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
...ss...
.jjwwjj.
jjjwwjjj
jjjwwjjj
jjwwwwjj
sjjwwjjs
sjjwwjjs
.hhhhhh.
.jjwwjj.
..hh.hh.
..hh.hh.
..hh.hh.
..hh.hh.
..hh..hh
..hh..hh
.hhh..hhh
"""
RADU['paso1'] = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
...ss...
.jjwwjj.
jjjwwjjj
jjjwwjjj
jjwwwwjs
sjjwwjjs
.jjwwjj.
.hhhhhh.
.jjwwjj.
..hhhhh.
.hhh.hh.
.hh...hh
hh....hh
hh.....h
h......h
hh.....hh
"""
RADU['paso2'] = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
...ss...
.jjwwjj.
jjjwwjjj
jjjwwjjj
sjwwwwjj
sjjwwjjs
.jjwwjjs
.hhhhhh.
.jjwwjj.
..hhhh..
...hhh..
...hhh..
...hh...
...hh...
...hh...
...hhh..
"""
RADU['salto'] = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
s..ss..s
sjjwwjjs
jjjwwjjj
jjjwwjjj
jjwwwwjj
.jjwwjj.
.jjwwjj.
.hhhhhh.
.jjwwjj.
.hhhhhh.
hhh..hhh
hh....hh
.hh..hh.
..h..h..
..hh.hh.
........
"""
RADU['lanza'] = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
...ss...
.jjwwjj.
jjjwwjjj
jjjwwjsss
jjwwwjj.
sjjwwjj.
sjjwwjj.
.hhhhhh.
.jjwwjj.
..hh.hh.
..hh..hh
.hh...hh
.hh...hh
hh....hh
hh....hh
hhh...hhh
"""
RADU['agachado'] = """
........
........
........
........
........
........
........
........
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
.jjwwjj.
jjjwwjjj
sjwwwwjs
sjjwwjjs
.hhhhhh.
.hhhhhh.
hhh..hhh
hhh..hhh
"""
RADU['agachalanza'] = """
........
........
........
........
........
........
........
........
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
.jjwwjj.
jjjwwjsss
jjwwwjj.
sjjwwjj.
.hhhhhh.
.hhhhhh.
hhh..hhh
hhh..hhh
"""
RADU['golpe'] = """
........
.hhhh...
hhhhhh..
hhhhhh..
.ssss...
.ksks..s
.ssss.s.
.skkk.s.
..ssjjj.
.jjwwjjj
jjjwwjjj
jjwwwwjj
sjjwwjj.
s.jwwjj.
..hhhhhh
..jjwwjj
...hh.hh
..hh..hh
.hh....h
hh.....h
h......hh
........
........
"""
RADU_ORDER = ['quieto', 'paso1', 'quieto', 'paso2', 'salto', 'lanza', 'agachado', 'agachalanza', 'golpe']
RADU_ORDER = ['quieto', 'paso1', 'paso2', 'salto', 'lanza', 'agachado', 'agachalanza', 'golpe']
RH = 24

def radu_bytes(name, mirror, shirt):
    rows = [l.strip() for l in RADU[name].strip('\n').split('\n')]
    rows = rows + ['........'] * (RH - len(rows))
    assert len(rows) == RH, (name, len(rows))
    p0, p1 = [], []
    for r in rows:
        r = (r + '........')[:8]
        if mirror: r = r[::-1]
        b0 = b1 = 0
        for ch in r:
            a = ch in 'hks' or (ch == 'j' and not shirt)
            b = ch in 'ws' or (ch == 'j' and shirt)
            b0 = (b0 << 1) | a
            b1 = (b1 << 1) | b
        p0.append(b0); p1.append(b1)
    return p0, p1

# arreglo: algunas filas se dibujaron con 9 caracteres (pie adelantado): se recortan a 8
ZOMBI = ["""
..xxx...
.xxxxx..
.x.x.x..
.xxxxx..
..x.xx..
..xxx...
...xx...
.xxxxxx.
xxxxxxxxx
x.xxxx.xx
x.xxxx..x
..xxxx...
..xxxx..
..xxxx..
..xx.xx.
..xx..x.
..x...x.
..x...x.
.xx..xx.
""", """
..xxx...
.xxxxx..
.x.x.x..
.xxxxx..
..x.xx..
..xxx...
...xx...
.xxxxxxx
xxxxxxx.
x.xxxx..
x.xxxx..
..xxxx..
..xxxx..
..xxxx..
...xxx..
...xx...
...xx...
...xx...
..xxx...
"""]
ZH = 19
CUERVO = ["""
x......x
xx....xx
.xx..xx.
..xxxx..
...xxxx.
..xxx.x.
....x...
........
""", """
........
........
...xx...
..xxxxx.
.xxxxxxx
xx.xx.x.
x..xx...
........
"""]
CH_ = 8
PUFF = ["""
........
...x....
..xxx...
.xx.xx..
..xxx...
...x....
........
........
""", """
.x...x..
..x.x...
x..x..x.
.xx.xx..
x..x..x.
..x.x...
.x...x..
........
""", """
x.....x.
........
..x.x...
........
..x.x...
........
x.....x.
........
"""]
BALTAG = """
.xxx....
xxxxx...
xxxxxx..
.xxxxxx.
...xx.xx
....x..x
.....x..
......x.
"""

def bits(txt, h, mirror=False):
    rows = [l.strip() for l in txt.strip('\n').split('\n')]
    rows = [(r + '........')[:8] for r in rows] + ['........'] * (h - len(rows))
    out = []
    for r in rows[:h]:
        if mirror: r = r[::-1]
        out.append(int(''.join('1' if ch == 'x' else '0' for ch in r), 2))
    return out

def rot(rows):  # 90 grados a la derecha
    g = [[(rows[y] >> (7 - x)) & 1 for x in range(8)] for y in range(8)]
    r = [[g[7 - x][y] for x in range(8)] for y in range(8)]
    return [int(''.join(map(str, row)), 2) for row in r]

b0 = bits(BALTAG, 8)
BALT = [b0]
for i in range(3):
    BALT.append(rot(BALT[-1]))


# ---------------------------------------------------------------
# HOMENAJE: bruja, hechizo y Radu convertido en pollo
#   pollo: y = P0 (amarillo) · o = P1 (naranja: pico y patas)
# ---------------------------------------------------------------
POLLO = {
'quieto': """
...yyy..
..yyyyy.
..yy.yyo
..yyyyoo
.yyyyy..
yyyyyyy.
yyyyyyy.
yyyyyyy.
.yyyyy..
..o..o..
..o..o..
.oo.oo..
""",
'paso': """
...yyy..
..yyyyy.
..yy.yyo
..yyyyoo
.yyyyy..
yyyyyyy.
yyyyyyy.
yyyyyyy.
.yyyyy..
..o.o...
.o...o..
oo...oo.
""",
'salto': """
...yyy..
y.yyyyy.
yyyy.yyo
yyyyyyoo
.yyyyy..
.yyyyyy.
..yyyyy.
..yyyy..
...yy...
...o.o..
..o...o.
........
"""}
POLLO_ORDER = ['quieto', 'paso', 'salto']
COL_POLLO0 = 0xFE
COL_POLLO1 = 0x38

def pollo_bytes(name, mirror):
    rows = [l.strip() for l in POLLO[name].strip('\n').split('\n')]
    rows = ['........'] * (RH - len(rows)) + rows          # el pollo está abajo, sobre los pies
    p0, p1 = [], []
    for r in rows:
        r = (r + '........')[:8]
        if mirror: r = r[::-1]
        p0.append(int(''.join('1' if ch == 'y' else '0' for ch in r), 2))
        p1.append(int(''.join('1' if ch == 'o' else '0' for ch in r), 2))
    return p0, p1

BRUJA = ["""
....x...
...xx...
..xxx...
.xxxxx..
xxxxxxxx
..x.x...
..xxx..x
...xx..x
..xxxxxx
.xxxxx.x
.xxxx..x
.xxxx..x
xxxxx..x
xxxxxx.x
xxxxxx.x
xxxxxx..
xxxxxxx.
.x...x..
""", """
....x...
...xx...
..xxx..x
.xxxxx.x
xxxxxxxx
..x.x..x
..xxx.xx
...xx.x.
..xxxxx.
.xxxxx..
.xxxx...
.xxxx...
xxxxx...
xxxxxx..
xxxxxx..
xxxxxx..
xxxxxxx.
.x...x..
"""]
BH = 18
COL_BRUJA = 0x5A
HECHIZO = ["""
...x....
.x.x.x..
..xxx...
xxxxxxx.
..xxx...
.x.x.x..
...x....
........
""", """
x.....x.
.x...x..
..x.x...
...x....
..x.x...
.x...x..
x.....x.
........
"""]

# ===============================================================
# APARICIONES (columna de la cámara, tipo, columna del mundo, y)
#   tipo 1 zombi (sale del suelo) · 2 cuervo (entra por la derecha)
# ===============================================================
SPAWN = [
    (8, 1, 30, 0), (20, 2, 0, 128), (34, 1, 58, 0), (46, 1, 66, 0), (58, 2, 0, 120),
    (70, 1, 92, 0), (84, 2, 0, 136), (92, 1, 118, 0), (108, 2, 0, 124), (118, 1, 140, 0),
    (130, 1, 150, 0), (142, 2, 0, 128), (150, 1, 176, 0), (162, 2, 0, 120), (170, 1, 188, 0),
    (176, 2, 0, 140), (186, 1, 206, 0), (196, 2, 0, 128), (204, 1, 222, 0), (212, 2, 0, 124),
]
# Vâvâma: espíritus que acechan en los árboles (tipo 8, en el tronco)
for tc in (40, 62, 124, 170, 196):
    SPAWN.append((tc + 2 - 30, 8, tc + 2, 184))
SPAWN.sort(key=lambda e: e[0])

# ===============================================================
# SALIDA ca65
# ===============================================================
def bline(data, per=16):
    out = []
    data = list(data)
    for i in range(0, len(data), per):
        out.append('        .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))
    return '\n'.join(out)

L = []
L.append('; generado por gfx/fase1.py · no editar a mano')
L.append('        .segment "FONT"')
L.append(bline(csA.data[:512]))
L.append('        .segment "CODE"')
import tramo
tramo.write_tramo(os.path.join(ROOT, 'src', 'tr_cementerio.s'), 'TR0', csA.data[512:1024], csB, csC, MAP,
                  SKY, MTN, BK, PF0, PF1, PF2, [COL_PF3] * 22, SPAWN, END_COL, CHECK_COL, 1, 1,
                  'EL CEMENTERIO', 'DE LA COLINA')
L.append('RADU_N = %d' % len(RADU_ORDER))
L.append('RH = %d' % RH)
for i, n in enumerate(RADU_ORDER):
    L.append('RF_%s = %d' % (n.upper(), i))
# tabla: [espejo][camisa][frame] -> P0, P1
idx = 0
lo0, hi0 = [], []
for shirt in (0, 1):
    for mirror in (0, 1):
        for n in RADU_ORDER:
            p0, p1 = radu_bytes(n, mirror, shirt)
            L.append('RSPR%d:' % idx)
            L.append(bline(p0 + p1, 24))
            idx += 1
L.append('RSPR_LO:')
L.append('        .byte ' + ','.join('<RSPR%d' % i for i in range(idx)))
L.append('RSPR_HI:')
L.append('        .byte ' + ','.join('>RSPR%d' % i for i in range(idx)))
L.append('ZH = %d' % ZH)
zi = 0
for mirror in (0, 1):
    for z in ZOMBI:
        L.append('ZSPR%d:' % zi); L.append(bline(bits(z, ZH, mirror), ZH)); zi += 1
L.append('ZSPR_LO:\n        .byte ' + ','.join('<ZSPR%d' % i for i in range(zi)))
L.append('ZSPR_HI:\n        .byte ' + ','.join('>ZSPR%d' % i for i in range(zi)))
ci = 0
for mirror in (0, 1):
    for z in CUERVO:
        L.append('CSPR%d:' % ci); L.append(bline(bits(z, 8, mirror), 8)); ci += 1
L.append('CSPR_LO:\n        .byte ' + ','.join('<CSPR%d' % i for i in range(ci)))
L.append('CSPR_HI:\n        .byte ' + ','.join('>CSPR%d' % i for i in range(ci)))
for i, p in enumerate(PUFF):
    L.append('PSPR%d:' % i); L.append(bline(bits(p, 8), 8))
L.append('PSPR_LO:\n        .byte ' + ','.join('<PSPR%d' % i for i in range(len(PUFF))))
L.append('PSPR_HI:\n        .byte ' + ','.join('>PSPR%d' % i for i in range(len(PUFF))))
L.append('BSPR:')
for b in BALT: L.append(bline(b, 8))

pi = 0
for mirror in (0, 1):
    for n in POLLO_ORDER:
        p0, p1 = pollo_bytes(n, mirror)
        L.append('POL%d:' % pi); L.append(bline(p0 + p1, 24)); pi += 1
L.append('POL_LO:\n        .byte ' + ','.join('<POL%d' % i for i in range(pi)))
L.append('POL_HI:\n        .byte ' + ','.join('>POL%d' % i for i in range(pi)))
L.append('BH = %d' % BH)
bi = 0
for mirror in (0, 1):
    for b in BRUJA:
        L.append('BRU%d:' % bi); L.append(bline(bits(b, BH, mirror), BH)); bi += 1
L.append('BRU_LO:\n        .byte ' + ','.join('<BRU%d' % i for i in range(bi)))
L.append('BRU_HI:\n        .byte ' + ','.join('>BRU%d' % i for i in range(bi)))
for i, h in enumerate(HECHIZO):
    L.append('HEC%d:' % i); L.append(bline(bits(h, 8), 8))
L.append('HEC_LO:\n        .byte <HEC0,<HEC1')
L.append('HEC_HI:\n        .byte >HEC0,>HEC1')
L.append('COL_POLLO0 = $%02X' % COL_POLLO0)
L.append('COL_POLLO1 = $%02X' % COL_POLLO1)
L.append('COL_BRUJA = $%02X' % COL_BRUJA)

L.append('SURF = %d' % SURF)
L.append('COL_P0 = $%02X' % COL_P0)
L.append('COL_P1 = $%02X' % COL_P1)
L.append('COL_PF3 = $%02X' % COL_PF3)
L.append('COL_ZOMBI = $%02X' % COL_ZOMBI)
L.append('COL_CUERVO = $%02X' % COL_CUERVO)
L.append('COL_PUFF = $%02X' % COL_PUFF)

# ---------------------------------------------------------------
# textos (fuente propia: códigos 0-63)
# ---------------------------------------------------------------
HUDS = ' PUNTOS 000000   RÉCORD 000000   RADU 3 '
assert len(HUDS) == 40
TEXTS = [
    ('HUDT', font.text(HUDS, 40)),
    ('T_LA', font.text('LA NOCHE DE LOS', 20, True, 0)),
    ('T_STR', font.text('STRIGOI', 20, True, 1)),
    ('T_FASE', font.text('FASE 1', 20, True, 2)),
    ('T_CEM', font.text('EL CEMENTERIO', 20, True, 0)),
    ('T_FIRE', font.text('PULSA FIRE', 20, True, 2)),
    ('T_INV', font.text('INVENCIBLE', 20, True, 1)),
    ('T_AUT', font.text('2026 - TONY C. WARE', 20, True, 0)),
    ('T_REC', font.text('RÉCORD 000000', 20, True, 1)),
    ('T_GO', font.text('GAME OVER', 20, True, 1)),
    ('T_PTS', font.text('PUNTOS 000000', 20, True, 0)),
    ('T_E1', font.text('¡CEMENTERIO', 20, True, 0)),
    ('T_E2', font.text('SUPERADO!', 20, True, 0)),
    ('T_E3', font.text('LA ESCALERA CUBIERTA', 20, True, 2)),
    ('T_E4', font.text('TE ESPERA...', 20, True, 2)),
    ('T_BLK', font.text('', 20)),
    ('T_F1', font.text('LA NOCHE', 20, True, 0)),
    ('T_F2', font.text('HA TERMINADO', 20, True, 1)),
    ('T_F3', font.text('RADU HA SALVADO', 20, True, 2)),
    ('T_F4', font.text('TRANSILVANIA', 20, True, 2)),
    ('T_F5', font.text('2026 - TONY C. WARE', 20, True, 0)),
]
for name, codes in TEXTS:
    L.append(name + ':')
    L.append(bline(codes, 20))
L.append('HUD_SC = %d' % (HUDS.index('000000')))
L.append('HUD_HI = %d' % (HUDS.index('000000', HUDS.index('000000') + 1)))
L.append('HUD_LV = %d' % (HUDS.index('3')))
L.append('DIG0 = %d' % font.CODE['0'])
L.append('TXT_DIG = %d' % (font.text('PUNTOS 000000', 20, True)[0:20].index(font.CODE['0'])))
L.append('REC_DIG = %d' % (font.text('RÉCORD 000000', 20, True)[0:20].index(font.CODE['0'])))

open(OUT, 'w').write('\n'.join(L) + '\n')

# textos en la fuente (para title/HUD)
def txt_codes(t, w):
    return font.text(t, w)

# ===============================================================
# VISTA PREVIA (proporción de píxel NTSC aproximada: 2 x 1 -> se escala 3x2)
# ===============================================================
from PIL import Image
def render_row_cells(rowcodes, cs, r_screen, w):
    img = Image.new('RGB', (w * 4, 8))
    cols = [BK[r_screen], PF0[r_screen], PF1[r_screen], PF2[r_screen]]
    pal = [atari_rgb(c) for c in cols]
    px = img.load()
    for c, code in enumerate(rowcodes):
        for y in range(8):
            b = cs.data[code * 8 + y]
            for x in range(4):
                v = (b >> (6 - 2 * x)) & 3
                px[c * 4 + x, y] = pal[v]
    return img

def preview(camcol, name):
    img = Image.new('RGB', (160, 8 * 22))
    for r in range(4):
        img.paste(render_row_cells(SKY[r], csA, r, 40), (0, 8 + r * 8))
    off = camcol // 2
    for r in range(3):
        rc = [MTN[r][(off + c) % 64] for c in range(40)]
        img.paste(render_row_cells(rc, csC, 4 + r, 40), (0, 8 + (4 + r) * 8))
    img.paste(Image.new('RGB', (160, 8), atari_rgb(BK[7])), (0, 8 + 7 * 8))
    for r in range(MROWS):
        rc = [MAP[r][camcol + c] for c in range(40)]
        img.paste(render_row_cells(rc, csB, 8 + r, 40), (0, 8 + (8 + r) * 8))
    img = img.resize((160 * 4, 176 * 2 + 0), Image.NEAREST)
    img.save(os.path.join(PREV, name))

for cc in (0, 40, 90, 140, 196, 216):
    preview(cc, 'prev_%03d.png' % cc)
# tira completa
strip = Image.new('RGB', (MCOLS * 4, MROWS * 8))
for r in range(MROWS):
    strip.paste(render_row_cells(MAP[r], csB, 8 + r, MCOLS), (0, r * 8))
strip.resize((MCOLS * 8, MROWS * 16), Image.NEAREST).save(os.path.join(PREV, 'mapa_fase1.png'))
# hoja de sprites
sheet = Image.new("RGB", (400, 290), atari_rgb(0x72))
spx = sheet.load()
c0, c1 = atari_rgb(COL_P0), atari_rgb(COL_P1)
cboth = atari_rgb(COL_P0 | COL_P1)
for shirt in (0, 1):
    for i, n in enumerate(RADU_ORDER):
        p0, p1 = radu_bytes(n, 0, shirt)
        for y in range(RH):
            for x in range(8):
                a = (p0[y] >> (7 - x)) & 1; b = (p1[y] >> (7 - x)) & 1
                col = cboth if a and b else c0 if a else c1 if b else None
                if col:
                    for dx in range(4):
                        for dy in range(3):
                            spx[i * 40 + x * 4 + dx, shirt * 80 + y * 3 + dy] = col
for i, z in enumerate(ZOMBI + CUERVO + PUFF):
    rows = bits(z, 19)
    col = atari_rgb(COL_ZOMBI if i < 2 else COL_CUERVO if i < 4 else COL_PUFF)
    for y in range(19):
        for x in range(8):
            if (rows[y] >> (7 - x)) & 1:
                for dx in range(4):
                    for dy in range(3):
                        spx[i * 40 + x * 4 + dx, 170 + y * 3 + dy] = col
for i, b in enumerate(BALT):
    for y in range(8):
        for x in range(8):
            if (b[y] >> (7 - x)) & 1:
                for dx in range(4):
                    for dy in range(3):
                        spx[240 + i * 40 + x * 4 + dx, 250 + y * 3 + dy] = atari_rgb(COL_PF3)
from PIL import Image as _I
hs = _I.new('RGB', (400, 110), atari_rgb(0x72)); hp = hs.load()
for i, n in enumerate(POLLO_ORDER):
    p0, p1 = pollo_bytes(n, 0)
    for y in range(RH):
        for x in range(8):
            a = (p0[y] >> (7 - x)) & 1; b = (p1[y] >> (7 - x)) & 1
            if a or b:
                col = atari_rgb(COL_POLLO0 if a else COL_POLLO1)
                for dx in range(4):
                    for dy in range(4): hp[i * 40 + x * 4 + dx, y * 4 + dy] = col
for i, b in enumerate(BRUJA + HECHIZO):
    rows = bits(b, BH)
    for y in range(BH):
        for x in range(8):
            if (rows[y] >> (7 - x)) & 1:
                for dx in range(4):
                    for dy in range(4): hp[140 + i * 40 + x * 4 + dx, 20 + y * 4 + dy] = atari_rgb(COL_BRUJA if i < 2 else 0x0E)
hs.save(os.path.join(PREV, 'homenaje.png'))
sheet.save(os.path.join(PREV, 'sprites_fase1.png'))
print('ok')
