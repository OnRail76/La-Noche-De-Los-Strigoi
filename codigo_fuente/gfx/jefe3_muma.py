#!/usr/bin/env python3
"""Jefe 3: MUMA PĂDURII · boceto con las reglas del Atari (ocupa un tercio de la pantalla)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T
import numpy as np

K = 0x00
MO, MO2 = 0xC2, 0xC6       # musgo oscuro y claro (pelo)
SK, SL = 0xF6, 0xFA        # piel de corteza media y clara
YE = 0x1E                  # ojo, dientes, cristal (PF3)
SALT = 0x0E                # cristales de sal
BKC = 0x90                 # cueva
W, H = 76, 128
X0, Y0 = 80, 16


def mir(pts, c):
    return [(2 * c - u, v) for (u, v) in pts]


def muma():
    L = Lienzo(W, H)
    # ---------- bastón de raíz retorcida (detrás) ----------
    L.curve((40, 127), (28, 70), (38, 14), 7.0, K, w1=5.0)
    L.curve((40, 127), (28, 70), (38, 14), 4.4, MO, w1=3.2)
    L.curve((38, 124), (27, 70), (36, 16), 1.2, MO2)
    L.curve((38, 14), (28, 8), (22, 12), 3.0, K, w1=1.2)            # raíces que abrazan el cristal
    L.curve((38, 14), (48, 8), (54, 12), 3.0, K, w1=1.2)
    L.poly([(30, 10), (34, 0), (38, 8), (42, -2), (46, 10), (38, 14)], YE)   # cristal de sal
    # ---------- melena de musgo: cae por la espalda hasta el suelo ----------
    hair = [(70, 6), (96, 2), (122, 10), (138, 30), (146, 60), (150, 92), (148, 127), (130, 127), (126, 110),
            (118, 127), (104, 127), (100, 108), (92, 127), (80, 127), (78, 96), (70, 70), (64, 40)]
    L.poly(hair, MO)
    for (u0, u1) in ((96, 92), (108, 112), (120, 128), (132, 140), (140, 146)):
        L.curve((u0, 12), (u0 + 10, 60), (u1, 124), 1.4, K)         # mechones oscuros
    for (u0, u1) in ((102, 100), (114, 120), (126, 136)):
        L.curve((u0, 14), (u0 + 8, 60), (u1, 120), 1.4, MO2)        # mechones a la luz
    # ---------- cuerpo encorvado bajo un harapo ----------
    L.poly([(66, 52), (100, 44), (112, 70), (110, 127), (60, 127), (56, 96)], K)
    L.poly([(70, 56), (98, 50), (104, 72), (100, 127), (66, 127), (62, 96)], MO)
    L.curve((76, 60), (70, 92), (74, 127), 1.6, K)
    L.curve((88, 56), (86, 92), (90, 127), 1.6, K)
    # ---------- brazo huesudo que agarra el bastón ----------
    L.curve((76, 60), (56, 66), (38, 58), 6.0, K, w1=5.0)
    L.curve((76, 60), (56, 65), (39, 57), 4.0, SK, w1=3.4)
    L.curve((74, 58), (56, 62), (40, 55), 1.2, SL)
    L.ell(37, 57, 5.0, 4.6, K); L.ell(36, 56, 4.0, 3.6, SK)
    for (dx, dy) in ((-6, -3), (-6, 1), (-5, 5)):
        L.curve((34, 56), (31, 56 + dy), (34 + dx - 2, 56 + dy + 2), 1.6, SK, w1=0.8)
    # ---------- brazo con garras que se tiende hacia Radu ----------
    L.curve((70, 80), (40, 90), (16, 82), 6.0, K, w1=4.6)
    L.curve((70, 80), (40, 89), (17, 81), 4.0, SK, w1=3.0)
    L.curve((68, 78), (40, 86), (18, 79), 1.2, SL)
    L.ell(14, 82, 5.0, 4.4, K); L.ell(14, 81, 4.0, 3.4, SK)
    for (dx, dy) in ((-10, -6), (-12, -1), (-11, 4), (-7, 8)):
        L.curve((12, 81), (12 + dx * 0.5, 81 + dy * 0.7), (12 + dx, 81 + dy), 1.8, SK, w1=0.6)
        L.ell(12 + dx, 81 + dy, 0.9, 1.0, K)
    # ---------- cabeza de perfil (mira a la izquierda) ----------
    L.ell(94, 30, 23, 26, K)
    L.ell(93, 30, 21.5, 25, SK)
    L.ell(86, 20, 11, 12, SL)
    # nariz ganchuda, fina, que cae hacia la izquierda
    L.poly([(74, 22), (62, 28), (54, 36), (52, 42), (58, 38), (66, 35), (76, 34)], K)
    L.poly([(74, 23), (63, 29), (56, 36), (55, 39), (60, 36), (67, 33), (76, 33)], SK)
    L.poly([(73, 24), (64, 29), (60, 32), (72, 28)], SL)
    L.ell(64, 31, 1.4, 1.2, K)                                       # verruga
    # barbilla puntiaguda hacia arriba
    L.poly([(80, 48), (68, 50), (62, 46), (64, 54), (78, 60), (92, 54)], K)
    L.poly([(80, 49), (69, 50), (65, 48), (66, 53), (78, 58), (90, 53)], SK)
    # boca abierta (de aquí salen los insectos)
    L.poly([(78, 40), (68, 40), (66, 44), (72, 48), (82, 47)], K)
    # pelo por encima de la frente
    L.poly([(70, 12), (84, 2), (106, 0), (120, 8), (112, 14), (100, 10), (88, 12), (78, 18)], MO)
    L.curve((76, 14), (90, 6), (110, 6), 1.2, MO2)
    return L


EYE = """
.kkkk.
kyyyyk
kyykyk
kyyyyk
.kkkk.
"""
TEETH = """
.y.y.y
.y.y..
"""


def build():
    L = muma()
    L.ascii(36, 20, EYE, {'k': K, 'y': YE})
    L.ascii(34, 40, TEETH, {'y': YE})
    return L.wide()


def cueva(E):
    """galería de sal: estalactitas arriba, vetas y cristales, suelo de sal"""
    L = Lienzo(160, 168)
    for (u, l, w) in ((10, 26, 8), (40, 16, 6), (64, 34, 10), (100, 20, 7), (140, 28, 9), (190, 14, 6)):
        L.poly([(u - w, 0), (u + w, 0), (u, l)], K)
        L.poly([(u - w + 2, 0), (u - 1, 0), (u - 1, l - 6)], MO)
    for (u, v) in ((30, 40), (120, 30), (170, 52), (20, 90)):
        L.poly([(u, v), (u + 4, v - 8), (u + 8, v), (u + 4, v + 4)], YE)   # cristales de sal
    L.rect(0, 136, 319, 167, K)
    L.poly([(0, 136), (40, 130), (90, 134), (160, 128), (240, 132), (319, 128), (319, 140), (0, 140)], MO)
    for (u, h) in ((8, 6), (34, 10), (52, 4), (130, 8), (150, 5), (200, 12), (230, 6), (288, 9), (306, 4)):
        L.poly([(u, 136), (u + 3, 136 - h), (u + 7, 136)], YE)
    E.paste(L.wide(), 0, 0)


def bands():
    B = []
    for r in range(21):
        if r < 3:
            B.append([BKC, K, MO, SK, YE])        # estalactitas, cristal del bastón
        elif r < 16:
            B.append([BKC, K, MO, SK, SL])        # cuerpo (PF3 = piel clara)
        elif r < 18:
            B.append([BKC, K, MO, MO2, YE])       # suelo de sal
        else:
            B.append([0x10, K, MO, MO2, YE])
    B[4] = [BKC, K, MO, SK, YE]                   # fila del ojo: amarillo en PF3
    B[5] = [BKC, K, MO, SK, YE]
    B[7] = [BKC, K, MO, SK, YE]                   # dientes
    return B


def escena():
    E = Escena(bands())
    cueva(E)
    E.paste(build(), X0, Y0)
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas del jefe:', E.cells(range(2, 18)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe3_borrador.png'))
