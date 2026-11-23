#!/usr/bin/env python3
"""Jefe 1: EL STRIGOI MORT · boceto con las reglas del Atari (ANTIC 4)
Sombreado por planos (cel), luz de luna desde arriba a la izquierda."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T
import numpy as np

K = 0x00            # negro
SM, SL = 0x08, 0x0C  # piel media y clara
RD, RL = 0x42, 0x44  # forro rojo oscuro y claro
VR = 0x54           # luz violeta en el borde de la capa
EY = 0x46           # ojos
WT = 0x0E           # colmillos
W, H = 52, 88
X0, Y0 = 54, 40


def mirror(pts, c=52):
    return [(2 * c - u, v) for (u, v) in pts]


def mort():
    L = Lienzo(W, H)
    c = 52
    # ---------------- capa (alas de murciélago con festones) ----------------
    wingL = [(12, 8), (20, 20), (32, 30), (40, 33), (40, 87), (2, 87), (5, 76), (0, 64), (5, 52), (1, 40), (5, 28), (8, 16)]
    L.poly(wingL, K)
    L.poly(mirror(wingL), K)
    # forro rojo (interior), dejando un ribete negro en el borde exterior
    linL = [(14, 15), (21, 24), (33, 32), (41, 35), (41, 86), (8, 86), (10, 76), (5, 64), (10, 52), (6, 40), (10, 28)]
    L.poly(linL, RD)
    L.poly(mirror(linL), RD)
    # pliegues iluminados (rojo claro) bajando desde la mano: tres en el ala izquierda, uno a la derecha
    L.poly([(14, 18), (19, 26), (16, 50), (12, 74), (10, 75), (12, 50), (11, 28)], RL)
    L.poly([(22, 26), (27, 31), (27, 58), (24, 84), (21, 84), (23, 58), (21, 32)], RL)
    L.poly([(33, 33), (36, 34), (35, 62), (34, 85), (31, 85), (32, 62)], RL)
    L.poly(mirror([(22, 26), (25, 29), (24, 58), (23, 84), (21, 84), (22, 58), (20, 32)]), RL)
    # sombra del forro junto al cuerpo
    L.poly([(37, 34), (42, 36), (42, 86), (38, 86)], K)
    L.poly(mirror([(37, 34), (42, 36), (42, 86), (38, 86)]), K)
    # luz de luna en el ribete exterior izquierdo (festones)
    L.line([(5, 28), (1, 40), (5, 52), (0, 64), (5, 76), (2, 87)], 1.2, VR)
    L.line([(8, 16), (5, 28)], 1.0, VR)
    # ---------------- cuerpo enjuto (traje negro) ----------------
    body = [(40, 31), (64, 31), (61, 52), (58, 60), (59, 87), (45, 87), (46, 60), (43, 52)]
    L.poly(body, K)
    L.line([(41, 33), (44, 52), (47, 60), (46, 86)], 1.0, VR)        # luz en el costado izquierdo
    L.line([(52, 36), (52, 58)], 0.8, 0x52 if False else VR)        # costura
    # ---------------- brazos (mangas) hacia las garras ----------------
    L.curve((40, 34), (24, 30), (14, 14), 6.0, K, w1=4.0)
    L.curve((64, 34), (80, 30), (90, 14), 6.0, K, w1=4.0)
    L.curve((39, 32), (25, 28), (15, 15), 1.2, VR, w1=0.8)          # luz en el brazo izquierdo
    # ---------------- cuello alto rojo detrás de la cabeza ----------------
    colL = [(41, 32), (36, 20), (32, 8), (40, 14), (45, 24), (46, 31)]
    L.poly(colL, K)
    L.poly([(42, 31), (38, 20), (35, 11), (41, 16), (45, 25)], RL)
    L.poly(mirror(colL), K)
    L.poly(mirror([(42, 31), (38, 20), (35, 11), (41, 16), (45, 25)]), RD)
    # cuernos que salen de las sienes de la calavera, curvados hacia arriba y afuera
    L.curve((40, 16), (26, 12), (28, -2), 6.0, K, w1=1.6)
    L.curve((64, 16), (78, 12), (76, -2), 6.0, K, w1=1.6)
    L.curve((40, 14), (28, 11), (29, 0), 2.0, SM, w1=0.8)
    L.curve((63, 14), (75, 11), (75, 1), 1.2, SM, w1=0.6)
    return L


# cabeza y manos dibujadas a mano (píxeles del Atari)
# calavera (16 px de ancho); en las columnas de los ojos solo hay tonos medios para que el rojo quepa
HEAD = """
....kkkkkkkk....
..kkllllmmmmkk..
.kllllmmmmmmmmk.
kllllmmmmmmmmmmk
kllllmmmmmmmmmmk
kllkmmmmmmmmkmmk
klkkkkkmmkkkkkmk
kkkkrrkmmkrrkkkk
kkkkrrkmmkrrkkkk
klkkkkkmmkkkkkmk
kllmmmmkkmmmmmmk
.kllmmkkkkmmmmk.
.kllmmmmmmmmmmk.
..kllmmmmmmmmk..
..klkmkmkmkmkk..
..kmmmmmmmmmmk..
..klkmkmkmkmkk..
...kllmmmmmmk...
....kkkkkkkk....
"""
HAND = """
k.......k.
k..k..k.k.
m..k..k.m.
m..m..m.m.
m.lm.lm.m.
mllmllmlm.
.lllllllm.
.lllllmmm.
..llllmm..
..lmmmmk..
...mmmk...
...kmmk...
"""
CM = {'k': K, 'm': SM, 'l': SL, 'r': 0x44}


def build():
    L = mort()
    L.ascii(W // 2 - 8, 13, HEAD, CM)
    L.ascii(2, 1, HAND, CM)
    L.ascii(W - 12, 1, '\n'.join(r[::-1] for r in HAND.strip('\n').split('\n')), CM)
    return L.wide()


def bands():
    sky = [0x80, 0x80, 0x80, 0x82, 0x82, 0x82, 0x84, 0x84, 0x84, 0x84, 0x86, 0x86, 0x86, 0x86, 0x86, 0x86, 0x86]
    B = []
    for r in range(21):
        bk = sky[r] if r < 17 else 0x10
        if r < 5:
            B.append([bk, 0x08, 0x0C, 0x0E])                    # luna
        elif r in (5, 6, 7, 8):
            B.append([bk, K, SM, SL, 0x44])                     # cabeza y manos (rojo en PF3: ojos y cuello)
        elif r == 9:
            B.append([bk, K, SM, RD, RL])
        elif r < 16:
            B.append([bk, K, RD, RL, VR])                       # capa
        elif r < 18:
            B.append([bk, K, 0x06, 0x0A])                       # tumbas
        else:
            B.append([[0x20, 0xC4, 0x0A, 0x24], [0x10, 0x22, 0x0C, 0x24], [0x10, 0x22, 0x0C, 0x34]][r - 18])
    B[7] = [B[7][0], K, SM, SL, 0x46]                    # fila de los ojos: rojo más vivo
    return B


def tumba(E, x0):
    L = Lienzo(20, 16)
    L.poly([(0, 15), (0, 2), (4, 0), (36, 0), (40, 2), (40, 15)], 0x06)
    L.rect(2, 1, 36, 2, 0x0A); L.rect(1, 2, 2, 15, 0x0A)
    L.rect(6, 6, 34, 7, 0x00); L.rect(6, 10, 34, 11, 0x00)
    E.paste(L.wide(), x0, 128)


def luna(E):
    L = Lienzo(26, 30)
    L.ell(26, 15, 25, 14.5, 0x0C)
    L.ell(23, 13, 21, 12, 0x0E)
    for (a, b, r) in ((18, 10, 5), (32, 18, 6), (22, 21, 3.5), (34, 8, 3)):
        L.ell(a, b, r, r * 0.7, 0x0C)
    E.paste(L.wide(), 122, 4)


def escena():
    E = Escena(bands())
    luna(E)
    for x0 in (8, 70, 132):
        tumba(E, x0)
    E.paste(build(), X0, Y0)
    return E


if __name__ == '__main__':
    E = escena()
    rep = E.quantize()
    print(rep, 'casillas del jefe:', E.cells(range(5, 16)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe1_borrador.png'))
