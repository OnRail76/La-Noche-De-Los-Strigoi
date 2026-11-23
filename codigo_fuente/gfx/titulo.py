#!/usr/bin/env python3
"""Bocetos: logo A (letras góticas que gotean), título 1 (Sighișoara de noche)
y GAME OVER (la calavera de Radu + «HA GANADO LA NOCHE...»). -> build/*.png"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
from arte import Escena, Lienzo, T
from pal import atari_rgb
import font

# --- letras góticas (9 x 12, se dibujan al doble de alto: 9 x 24 píxeles anchos)
G = {
'S': """
.XXXXXXX.
XXX...XXX
XXX....X.
XXXX.....
.XXXXX...
..XXXXXX.
....XXXXX
......XXX
X.....XXX
XXX..XXXX
.XXXXXXX.
..X...X..""",
'T': """
XXXXXXXXX
XX.XXX.XX
X..XXX..X
...XXX...
...XXX...
...XXX...
...XXX...
...XXX...
...XXX...
...XXX...
..XXXXX..
...X.....""",
'R': """
XXXXXXX..
.XXX.XXX.
.XXX..XXX
.XXX..XXX
.XXX.XXX.
.XXXXXX..
.XXX.XXX.
.XXX..XX.
.XXX..XXX
.XXX..XXX
XXXXX..XX
..X.....X""",
'I': """
XXXXX
.XXX.
.XXX.
.XXX.
.XXX.
.XXX.
.XXX.
.XXX.
.XXX.
.XXX.
XXXXX
..X..""",
'G': """
..XXXXXX.
.XXX..XXX
XXX....XX
XXX......
XXX......
XXX..XXXX
XXX...XXX
XXX...XXX
XXX...XXX
.XXX..XXX
..XXXXXX.
....X....""",
'O': """
..XXXXX..
.XXX.XXX.
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
.XXX.XXX.
..XXXXX..
....X....""",
'A': """
...XXX...
..XXXXX..
.XXX.XXX.
.XXX.XXX.
XXX...XXX
XXX...XXX
XXXXXXXXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
.X.....X.""",
'M': """
XX.....XX
XXX...XXX
XXXX.XXXX
XXXXXXXXX
XXX.X.XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
.X.....X.""",
'E': """
XXXXXXXXX
.XXX...XX
.XXX....X
.XXX.....
.XXX..X..
.XXXXXX..
.XXX..X..
.XXX.....
.XXX....X
.XXX...XX
XXXXXXXXX
...X.....""",
'V': """
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
XXX...XXX
.XXX.XXX.
.XXX.XXX.
..XXXXX..
..XXXXX..
...XXX...
....X....""",
' ': '\n' + '\n'.join(['.....'] * 12),
}

def palabra(txt, hue_top=0x46, hue_bot=0x42, edge=0x20, glint=0x4C, gap=3, drip=True, sx=2, sy=3):
    """devuelve una matriz de colores (alto 30) con la palabra gótica, sombreado y gotas"""
    cols = []
    for ch in txt:
        rows = [r for r in G[ch].strip('\n').split('\n')]
        cols.append(rows)
    w = (sum(len(r[0]) for r in cols) + gap * (len(cols) - 1)) * sx
    H = 12 * sy + 8
    A = np.full((H, w + 2), T, dtype=np.int16)
    x = 1
    for rows in cols:
        cw = len(rows[0])
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                if c != 'X': continue
                for k in range(sy):
                    y = j * sy + k
                    for q in range(sx):
                        xx = x + i * sx + q
                        if j == 11:                       # rabito de la gota
                            A[y, xx] = hue_bot; continue
                        t = y / (11.0 * sy)
                        col = hue_top + 2 if t < 0.25 else (hue_top if t < 0.6 else hue_bot)
                        if q == 0 and (i == 0 or row[i - 1] != 'X'):
                            col = glint if t < 0.5 else hue_top + 2     # brillo en el borde izquierdo
                        A[y, xx] = col
        x += (cw + gap) * sx
    # gotas que cuelgan
    if drip:
        yb = 12 * sy - 1
        for xx in range(1, w + 1):
            if A[yb - 1, xx] == hue_bot and (xx * 7) % 5 == 0:
                for y in range(yb, yb + 3 + (xx * 5) % 5):
                    A[y, xx] = hue_bot
    # perfil oscuro alrededor
    B = A.copy()
    for y in range(H):
        for xx in range(w + 2):
            if A[y, xx] == T:
                nb = [A[yy, x2] for yy, x2 in ((y - 1, xx), (y + 1, xx), (y, xx - 1), (y, xx + 1)) if 0 <= yy < H and 0 <= x2 < w + 2]
                if any(v != T for v in nb):
                    B[y, xx] = edge
    return B

def texto(lines, w=320, scale=3):
    """renglones de texto (modo 6: 20 caracteres de 8x8 ancho doble) -> imagen RGB"""
    fb = font.font_bytes()
    img = Image.new('RGB', (w, 16 * len(lines)), (0, 0, 0)); px = img.load()
    for n, (t, col, bk) in enumerate(lines):
        for y in range(16):
            for x in range(w): px[x, n * 16 + y] = atari_rgb(bk)
        t = t.center(20)
        for i, ch in enumerate(t):
            code = font.text(ch, 1)[0] & 0x3F
            for y in range(8):
                b = fb[code * 8 + y]
                for k in range(8):
                    if (b >> (7 - k)) & 1:
                        for dx in range(2):
                            for dy in range(2):
                                px[i * 16 + k * 2 + dx, n * 16 + y * 2 + dy] = atari_rgb(col)
    return img.resize((w * scale, 16 * len(lines) * scale), Image.NEAREST)

def montar(partes, nombre):
    W = max(p.size[0] for p in partes); H = sum(p.size[1] for p in partes)
    out = Image.new('RGB', (W, H)); y = 0
    for p in partes:
        out.paste(p, (0, y)); y += p.size[1]
    out.save(os.path.join(HERE, '..', 'build', nombre))

# ================================================================ TÍTULO
def titulo():
    SKY = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x60, 0x62, 0x62, 0x52, 0x54, 0x54, 0x52, 0x50, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00]
    B = []
    for r in range(21):
        if r < 6:   B.append([SKY[r], 0x20, [0x48, 0x48, 0x46, 0x44, 0x42, 0x42][r], 0x4C, 0x42])   # logo
        elif r < 15: B.append([SKY[r], 0x00, 0x0C, 0x0A, 0x1C])         # cielo, luna, silueta, ventanas
        else:       B.append([SKY[r], 0x00, 0x08, 0x06, 0x1C])          # niebla y roca
    E = Escena(B)
    logo = palabra('STRIGOI')
    E.paste(logo, (160 - logo.shape[1]) // 2, 2)
    L = Lienzo(160, 168)
    L.ell(212, 92, 44, 24, 0x0C)                                   # la luna (u = 2 x píxel)
    L.ell(198, 86, 8, 5, 0x0A); L.ell(226, 100, 6, 4, 0x0A); L.ell(220, 80, 4, 3, 0x0A)
    # ciudadela: murallas, tejados y la Torre del Reloj
    sil = [(0, 168), (0, 128), (20, 124), (24, 116), (32, 116), (36, 124), (56, 122), (60, 110), (66, 104), (72, 110),
           (76, 120), (96, 118), (100, 100), (104, 96), (104, 70), (108, 64), (112, 52), (116, 64), (120, 70), (120, 96),
           (124, 100), (128, 116), (150, 114), (156, 106), (162, 114), (182, 116), (186, 108), (194, 108), (198, 118),
           (232, 120), (238, 112), (244, 112), (250, 122), (276, 124), (282, 116), (290, 116), (296, 126), (319, 126), (319, 168)]
    L.poly(sil, 0x00)
    for (x, y) in ((108, 80), (114, 80), (110, 90), (62, 114), (160, 120), (240, 118), (30, 126), (190, 114), (286, 122)):
        L.rect(x, y, x + 1, y + 2, 0x1C)                           # ventanas encendidas
    # niebla al pie de la colina
    for x in range(0, 320, 2):
        yy = 128 + int(3 * math.sin(x / 17.0)) + int(2 * math.sin(x / 7.0))
        L.rect(x, yy, x + 1, yy + 5 + (x // 2) % 3, 0x06)
    # colina y la roca de Radu
    L.poly([(0, 168), (0, 150), (60, 140), (120, 146), (180, 144), (240, 150), (319, 146), (319, 168)], 0x00)
    L.poly([(40, 168), (50, 150), (70, 140), (104, 142), (118, 156), (124, 168)], 0x00)
    E.paste(L.wide(), 0, 0)
    E.quantize()
    # Radu de pie en la roca, baltag al hombro, capa al viento (sprites)
    radu = ["00011000", "00111100", "00111100", "00011000", "00111100", "01111110", "11111111", "10111101", "10111101",
            "10111101", "00111100", "00111100", "00100100", "00100100", "00100100", "00100100", "01100110", "11100111"]
    E.sprites.append((40, 120, [int(r, 2) for r in radu], 0x26))
    capa = ["00000000"] * 4 + ["00000011", "00000111", "00001111", "00011110", "00111100", "01111000", "01110000", "01100000"]
    E.sprites.append((46, 120, [int(r, 2) for r in capa], 0x44))
    hacha = ["00011100", "00111110", "00111100", "00011000", "00100000", "01000000", "10000000"]
    E.sprites.append((34, 113, [int(r, 2) for r in hacha], 0x0C))
    murc = ["10000001", "11000011", "11100111", "01111110", "00111100", "00011000"]
    for (x, y) in ((92, 68), (120, 84), (70, 58)):
        E.sprites.append((x, y, [int(r, 2) for r in murc], 0x00))
    escena = E.render(scale=3)
    arriba = texto([('LA NOCHE DE LOS', 0x0C, 0x00)], w=320)
    abajo = texto([('PULSA FIRE', 0x0E, 0x00), ('NORMAL  HARDCORE', 0x36, 0x00), ('2026 - TONY C. WARE', 0x08, 0x00)], w=320)
    montar([arriba, escena, abajo], 'boceto_titulo.png')

# ================================================================ GAME OVER
CALAVERA = """
.....XXXXXXXXXX.....
...XXXXXXXXXXXXXX...
..XXXXXXXXXXXXXXXX..
.XXXXXXXXXXXXXXXXXX.
.XXXXXXXXXXXXXXXXXX.
XXXXXXXXXXXXXXXXXXXX
XXX.....XXXX.....XXX
XX.......XX.......XX
XX.......XX.......XX
XXX.....XXXX.....XXX
XXXXXXXXX..XXXXXXXXX
.XXXXXXX....XXXXXXX.
..XXXXXXXXXXXXXXXX..
...XX.XX.XX.XX.XX...
...XXXXXXXXXXXXXX...
....X.XX.XX.XX.X....
.....XXXXXXXXXX.....
"""
def gameover():
    REDS = [0x48, 0x46, 0x44, 0x42, 0x42, 0x48, 0x46, 0x44, 0x42, 0x42, 0x42]
    B = [[0x00, 0x20, REDS[r - 8], 0x4C, 0x42] if 8 <= r < 19 else [0x00, 0x04, 0x0E, 0x0A, 0x06] for r in range(21)]
    E = Escena(B)
    rows = CALAVERA.strip('\n').split('\n')
    A = np.full((len(rows) * 3, len(rows[0]) * 2), T, dtype=np.int16)
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c == 'X':
                for k in (0, 1, 2):
                    y = j * 3 + k
                    for q in (0, 1):
                        A[y, i * 2 + q] = 0x0E if (i < 6 and y < 21) else (0x0A if y < 36 else 0x06)
    E.paste(A, 60, 4)
    # el polvo del bote y el suelo
    L = Lienzo(160, 168)
    L.rect(100, 57, 220, 58, 0x04)
    for (x, y) in ((106, 53), (114, 51), (206, 52), (214, 54), (100, 55), (220, 55)):
        L.rect(x, y, x + 1, y, 0x06)
    E.paste(L.wide(), 0, 0)
    w1 = palabra('GAME', gap=2, sx=2, sy=3)
    E.paste(w1, (160 - w1.shape[1]) // 2, 66)
    w2 = palabra('OVER', gap=2, sx=2, sy=3)
    E.paste(w2, (160 - w2.shape[1]) // 2, 106)
    E.quantize()
    escena = E.render(scale=3)
    abajo = texto([('HA GANADO', 0x0C, 0x00), ('LA NOCHE...', 0x0C, 0x00), ('', 0x00, 0x00), ('PUNTOS   012400', 0x0E, 0x00), ('RECORD   048300', 0x36, 0x00)], w=320)
    montar([escena.crop((0, 0, escena.size[0], 150 * 3)), abajo], 'boceto_gameover.png')

titulo(); gameover()
print('ok')
