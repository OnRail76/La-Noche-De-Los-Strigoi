#!/usr/bin/env python3
"""Jefe 4: EL BALAUR · dragón de tres cabezas (azul arriba, roja en medio, verde abajo)
Cada cabeza vive en su franja de filas, con su paleta; los cuellos son del color del cuerpo."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T
import numpy as np

K = 0x00
B1, B2, B3 = 0x02, 0x04, 0x08          # cuerpo de escamas gris pizarra
BELLY = 0x24
HEADS = {'azul': (0x86, 0x8C), 'roja': (0x44, 0x48), 'verde': (0xC6, 0xCC)}
EYE = 0x1E
BKC = [0x80, 0x80, 0x82, 0x82, 0x82, 0x84, 0x84, 0x84, 0x84, 0x86, 0x86, 0x86, 0x86, 0x86, 0x86, 0x86]


def cabeza(L, u0, v0, mid, light, s=1.0):
    """cabeza de dragón de perfil mirando a la izquierda; (u0, v0) = nuca"""
    P = lambda pts: [(u0 + (u - 46) * s, v0 + (v - 8) * s) for (u, v) in pts]
    # cuernos hacia atrás
    L.curve(P([(38, 2)])[0], P([(48, -4)])[0], P([(60, -6)])[0], 3.0 * s, K, w1=1.0)
    L.curve(P([(42, 4)])[0], P([(54, 0)])[0], P([(64, 2)])[0], 2.6 * s, K, w1=1.0)
    # mandíbula inferior abierta
    L.poly(P([(6, 17), (16, 15), (32, 14), (46, 13), (44, 20), (26, 21), (10, 20)]), K)
    L.poly(P([(8, 17), (18, 16), (32, 15), (44, 14), (42, 18), (26, 19), (11, 19)]), mid)
    # cráneo y morro
    L.poly(P([(46, 2), (36, -1), (24, 1), (12, 3), (0, 5), (-1, 9), (2, 11), (16, 12), (32, 12), (46, 12)]), K)
    L.poly(P([(45, 3), (36, 0), (24, 2), (12, 4), (1, 6), (1, 9), (4, 10), (16, 11), (32, 11), (45, 11)]), mid)
    L.poly(P([(44, 3), (36, 1), (24, 3), (12, 5), (4, 6), (16, 6), (30, 5)]), light)     # luz en el morro
    L.ell(*P([(3, 7)])[0], 1.0 * s, 0.8 * s, K)                                            # orificio nasal
    # boca: interior negro y dientes
    L.poly(P([(4, 11), (18, 12), (32, 13), (40, 13), (30, 14), (16, 15), (8, 16)]), K)
    for u in (8, 14, 20, 26):
        L.line(P([(u, 11), (u, 13)]), 0.8, light)
    # cresta
    for u in (22, 30, 38):
        L.poly(P([(u - 3, 1), (u, -4), (u + 2, 1)]), K)
    return P([(30, 5)])[0]          # posición del ojo


def balaur():
    L = Lienzo(160, 136)
    # ---------- cola enroscada a la derecha ----------
    L.curve((292, 122), (320, 100), (304, 74), 12.0, K, w1=4.0)
    L.curve((292, 122), (318, 100), (304, 75), 9.0, B2, w1=2.4)
    L.poly([(300, 76), (308, 64), (310, 78)], K)
    # ---------- alas de murciélago plegadas hacia arriba ----------
    wing = [(204, 96), (214, 60), (232, 34), (240, 52), (254, 30), (262, 54), (280, 40), (284, 66), (300, 62), (290, 100)]
    L.poly(wing, K)
    L.poly([(210, 94), (218, 62), (232, 40), (240, 58), (254, 36), (262, 60), (280, 46), (282, 70), (296, 68), (286, 96)], B1)
    for (a, b) in ((232, 36), (254, 32), (280, 42)):
        L.curve((a, b), (a + 2, b + 30), (a - 4 if a < 270 else a, 96), 2.0, B2, w1=1.0)
    # ---------- cuerpo ----------
    L.ell(240, 110, 64, 25, K)
    L.ell(238, 108, 62, 23, B2)
    L.ell(226, 99, 40, 10, B3)
    L.ell(240, 126, 50, 8, K)
    L.ell(240, 125, 48, 6.5, BELLY)                                           # vientre curvo
    for u in range(200, 284, 12):
        L.curve((u, 119), (u - 2, 125), (u + 1, 131), 1.0, K)
    # escamas: arcos oscuros sobre el lomo
    for (u, v) in ((200, 104), (216, 96), (232, 102), (250, 96), (266, 104), (282, 110), (214, 114), (246, 112)):
        L.curve((u - 6, v), (u, v - 4), (u + 6, v), 1.0, B1)
    # patas con garras
    for u in (200, 266):
        L.curve((u, 116), (u - 10, 128), (u - 6, 136), 11.0, K, w1=8.0)
        L.curve((u, 116), (u - 10, 128), (u - 6, 135), 8.0, B2, w1=6.0)
        for d in (-10, -4, 2):
            L.poly([(u + d - 6, 136), (u + d - 1, 128), (u + d + 1, 136)], K)
    # ---------- cuellos ----------
    necks = [((210, 92), (178, 54), (158, 32)),     # azul (arriba)
             ((196, 100), (132, 84), (108, 62)),    # roja (en medio)
             ((190, 112), (150, 118), (128, 96))]   # verde (abajo)
    for (a, b, c) in necks:
        L.curve(a, b, c, 22.0, K, w1=14.0)
        L.curve(a, b, c, 18.0, B2, w1=11.0)
    eyes = []
    eyes.append(cabeza(L, 164, 26, *HEADS['azul'], s=1.4))
    eyes.append(cabeza(L, 112, 58, *HEADS['roja'], s=1.4))
    eyes.append(cabeza(L, 134, 92, *HEADS['verde'], s=1.4))
    return L, eyes


def gruta(E):
    L = Lienzo(160, 136)
    for (u, l, w) in ((8, 14, 6), (36, 22, 8), (70, 10, 5), (110, 18, 7), (150, 12, 5), (196, 20, 8), (240, 12, 6), (290, 18, 8)):
        L.poly([(u - w, 0), (u + w, 0), (u, l)], K)
        L.poly([(u - w + 2, 0), (u - 1, 0), (u - 1, l - 5)], 0x8C)
    E.paste(L.wide(), 0, 0)
    F = Lienzo(160, 40)
    F.rect(0, 0, 319, 39, 0x0A); F.rect(0, 0, 319, 1, 0x0E)
    for (u, v) in ((20, 6), (90, 10), (160, 4), (250, 8)):
        F.ell(u, v, 10, 2, 0x06)
    E.paste(F.wide(), 0, 136)


def bands():
    B = []
    for r in range(21):
        bk = BKC[r] if r < 16 else 0x0A
        if r < 2:
            B.append([bk, K, B1, 0x8C])                                      # carámbanos
        elif r < 5:
            B.append([bk, K, B2, HEADS['azul'][0], HEADS['azul'][1]])        # cabeza azul (luz en PF3)
        elif r < 9:
            B.append([bk, K, B2, HEADS['roja'][0], HEADS['roja'][1]])        # cabeza roja
        elif r < 13:
            B.append([bk, K, B2, HEADS['verde'][0], HEADS['verde'][1]])      # cabeza verde
        elif r < 17:
            B.append([bk, K, B2, B3, BELLY])                                 # cuerpo
        else:
            B.append([0x0A, 0x06, 0x0E, 0x08])                               # nieve
    return B


def escena():
    E = Escena(bands())
    gruta(E)
    L, eyes = balaur()
    for (u, v), name in zip(eyes, ('azul', 'roja', 'verde')):
        x, y = int(u // 2), int(v)
        for dx in (-1, 0):
            L.px(x + dx, y, HEADS[name][1]); L.px(x + dx, y - 1, K); L.px(x + dx, y + 1, K)
    E.paste(L.wide(), 0, 0)
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas del jefe:', E.cells(range(0, 17)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe4_borrador.png'))
