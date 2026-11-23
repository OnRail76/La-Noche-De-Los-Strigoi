#!/usr/bin/env python3
"""Jefe 2: ARIC, EL SASTRE DE LAS SOMBRAS · boceto con las reglas del Atari"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T

K = 0x00
T1, T2, T3, T4 = 0xA2, 0xA6, 0xAA, 0xAE     # espectro verde azulado (oscuro -> claro)
RC = 0x44                                  # tela bordada (roja)
NE = 0x0E                                  # aguja / botones
BK_ROOM = 0x20
W, H = 64, 100
X0, Y0 = 50, 6


def aric():
    L = Lienzo(W, H)
    c = 64
    # ---------- cola de fantasma que se curva hacia la derecha ----------
    L.poly([(48, 60), (82, 60), (86, 72), (92, 82), (104, 90), (118, 92), (110, 97), (94, 98), (80, 92),
            (68, 84), (58, 74)], T1)
    L.poly([(52, 60), (76, 60), (80, 70), (86, 80), (98, 88), (84, 88), (72, 80), (62, 70)], T2)
    L.poly([(54, 60), (64, 60), (66, 68), (72, 76), (64, 72), (58, 66)], T3)
    L.curve((44, 66), (36, 78), (40, 90), 3.0, T1, w1=0.8)              # jirón suelto
    L.curve((86, 64), (98, 70), (102, 64), 2.4, T1, w1=0.8)
    # ---------- brazo derecho levantado con la aguja ----------
    L.curve((84, 34), (104, 34), (114, 14), 5.0, K, w1=3.6)
    L.curve((84, 34), (103, 33), (113, 14), 3.0, T1, w1=1.8)
    L.ell(114, 13, 3.6, 3.2, T2)
    L.line([(114, 42), (114, 0)], 2.0, K)
    L.line([(114, 40), (114, 1)], 1.0, T3)
    # ---------- torso encorvado y estrecho ----------
    L.ell(48, 36, 13, 8, K); L.ell(80, 36, 13, 8, K)
    L.poly([(36, 36), (92, 36), (82, 62), (46, 62)], K)
    L.ell(48, 36, 11.5, 6.8, T2); L.ell(80, 36, 11.5, 6.8, T1)
    L.poly([(38, 37), (64, 40), (64, 61), (47, 61)], T2)
    L.poly([(90, 37), (64, 40), (64, 61), (81, 61)], T1)
    L.ell(45, 34, 6, 3.4, T3)                                           # luz en el hombro
    L.poly([(56, 30), (72, 30), (64, 44)], T3)                          # pechera
    L.poly([(60, 31), (68, 31), (64, 36)], RC)                          # corbatín
    for v in (46, 51, 56):
        L.ell(64, v, 1.4, 1.0, T3)
    # cinta métrica
    L.curve((55, 31), (49, 44), (52, 60), 2.4, T3)
    L.curve((73, 31), (79, 42), (77, 52), 2.4, T3)
    for v in range(34, 60, 3):
        L.line([(49.5, v), (51.5, v)], 0.6, K)
    # ---------- brazo izquierdo: dedos de aguja ----------
    L.curve((38, 38), (22, 46), (14, 64), 5.0, K, w1=3.6)
    L.curve((38, 38), (23, 45), (15, 63), 3.0, T2, w1=1.8)
    L.curve((37, 37), (23, 44), (15, 61), 1.0, T3)
    L.ell(14, 64, 3.6, 3.4, T3)
    for (dx, dy) in ((-8, 10), (-4, 13), (0, 14), (4, 12), (7, 8)):
        L.curve((14, 65), (14 + dx * 0.4, 65 + dy * 0.5), (14 + dx, 65 + dy), 1.4, T3, w1=0.6)
    # cuello
    L.rect(59, 24, 69, 31, T2)
    return L


PATCH = """
rrrrrr
rkrrkr
rrkkrr
rrkkrr
rkrrkr
rrrrrr
r.r.r.
"""
HEAD = """
.....kkkkkkkk.....
...kk33333222kk...
..k333333222222k..
.kkkkkkkkkkkkkkkk.
....k3333222222k..
...k33333222222k..
...k3kkk2kkk222k..
...kkWWWkkWWWk22k.
...kkWWWkkWWWk22k.
...kkWWWkkWWWk22k.
...kkWWWkkWWWk22k.
...k3kkk3kkk222k..
...k333k3k22222k..
...k33k33k2222k...
...k33k33kk222k...
...k333kkkk22k....
..kkkk3kk2kkkkk...
.kk..k3kk2k..kk...
k....k33k2k....k..
.....k33k22k......
......k3k2k.......
......k332k.......
.......kkk........
"""


def build():
    L = aric()
    L.ascii(W // 2 - 9, 3, HEAD, {'k': K, '2': T2, '3': T3, 'W': T3})
    for (x, y) in ((8, 0), (50, 1), (3, 12), (55, 12), (14, 20), (45, 20)):
        L.ascii(x, y, PATCH, {'k': K, 'r': RC})
    w = L.wide()
    return w


def bands():
    B = []
    for r in range(21):
        if r < 4:
            B.append([BK_ROOM, K, T2, T3, RC])                 # cabeza y retales del escudo (rojo en PF3)
        elif r < 6:
            B.append([BK_ROOM, K, T1, T2, T3])
        elif r < 9:
            B.append([BK_ROOM, K, T1, T2, T3])                 # torso
        elif r < 16:
            B.append([BK_ROOM, K, T1, T2, T3])                 # jirones
        elif r < 18:
            B.append([0x10, K, 0x22, 0x24, 0x26])              # suelo de madera
        else:
            B.append([0x10, 0x00, 0x22, 0x24])
    return B


def sala(E):
    """ventanal gótico, vigas y maniquí"""
    L = Lienzo(160, 128)
    # ventanal ojival a la izquierda
    L.poly([(16, 128), (16, 40), (26, 14), (38, 2), (50, 14), (60, 40), (60, 128)], K)
    L.poly([(20, 128), (20, 42), (29, 18), (38, 8), (47, 18), (56, 42), (56, 128)], T2)
    L.rect(37, 8, 39, 128, K); L.rect(20, 60, 56, 61, K); L.rect(20, 92, 56, 93, K)
    L.poly([(22, 128), (22, 46), (30, 24), (36, 14), (36, 128)], T4)
    # vigas del techo
    L.rect(0, 0, 319, 3, K); L.rect(236, 0, 242, 128, K)
    # maniquí de sastre a la derecha (silueta)
    L.ell(270, 70, 14, 8, K); L.poly([(258, 70), (282, 70), (278, 108), (262, 108)], K)
    L.rect(268, 108, 272, 124, K); L.poly([(258, 124), (282, 124), (276, 127), (264, 127)], K)
    w = L.wide()
    E.paste(w, 0, 0)
    # suelo de tablas
    F = Lienzo(160, 40)
    F.rect(0, 0, 319, 39, 0x22)
    for v in range(0, 40, 6):
        F.rect(0, v, 319, v, 0x24)
    for u in range(0, 320, 37):
        F.rect(u, 0, u + 1, 15, 0x00)
    F.rect(0, 0, 319, 1, 0x26)
    E.paste(F.wide(), 0, 128)


TIJERAS_P2 = """
..xxxx..
.x....x.
x......x
x......x
.x....x.
..xxxx..
...xx...
..xxxx..
.x....x.
x......x
x......x
.x....x.
..xxxx..
...xx...
...xx...
..xxxx..
..xxxx..
..x..x..
..x..x..
..x..x..
.xx..xx.
.x....x.
.x....x.
.x....x.
.x....x.
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
.x....x.
.x....x.
"""
TIJERAS_P3 = """
..xxxx..
.xx..xx.
xx....xx
xx....xx
.xx..xx.
..xxxx..
........
..xxxx..
.xx..xx.
xx....xx
xx....xx
.xx..xx.
..xxxx..
........
...xx...
..x..x..
..x..x..
...xx...
...xx...
...xx...
..x..x..
..x..x..
..x..x..
.x....x.
.x....x.
.x....x.
.x....x.
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
x......x
"""


def bits(txt):
    return [int(''.join('1' if ch == 'x' else '0' for ch in (r + '........')[:8]), 2) for r in txt.strip('\n').split('\n')]


def escena():
    E = Escena(bands())
    sala(E)
    E.paste(build(), X0, Y0)
    # tijeras oxidadas: P2 y P3 superpuestos en modo OR -> 3 tonos de óxido
    p2, p3 = bits(TIJERAS_P2), bits(TIJERAS_P3)
    for (x, y) in ((118, 66),):
        E.sprites.append((x, y, p2, 0x22))
        E.sprites.append((x, y, [b & ~a & 0xFF for a, b in zip(p2, p3)], 0x26))
        E.sprites.append((x, y, [a & b for a, b in zip(p2, p3)], 0x28))
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas del jefe:', E.cells(range(3, 16)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe2_borrador.png'))
