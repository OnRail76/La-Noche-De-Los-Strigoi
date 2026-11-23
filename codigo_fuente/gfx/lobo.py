#!/usr/bin/env python3
"""Strigoi Mort, segunda forma: el lobo monstruoso (de perfil, embistiendo hacia la izquierda)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Lienzo, LienzoS
K, G1, G2, RD, WT = 0x00, 0x06, 0x0A, 0x44, 0x0E
WH, WW = 38, 46

def lobo(k=1.0):
    L = LienzoS(int(WW * k + 0.99), int(WH * k + 0.99), k) if k != 1.0 else Lienzo(WW, WH)
    # cola erizada hacia atrás y arriba
    L.curve((78, 14), (86, 6), (92, 4), 6.0, K, w1=2.0)
    L.curve((80, 12), (86, 7), (91, 5), 1.0, G1)
    # pata trasera lejana (empuja atrás) y cercana
    L.curve((72, 22), (80, 28), (90, 33), 5.0, K, w1=2.4)
    L.curve((66, 24), (70, 31), (78, 37), 7.0, K, w1=2.6)
    L.curve((64, 22), (68, 29), (75, 35), 1.2, G1)
    # patas delanteras estiradas
    L.curve((26, 26), (16, 30), (6, 33), 4.5, K, w1=2.2)
    L.curve((32, 28), (24, 33), (14, 37), 6.0, K, w1=2.6)
    L.curve((31, 27), (23, 31), (14, 35), 1.2, G1)
    # cuerpo: pecho alto y vientre recogido
    L.poly([(22, 10), (34, 6), (50, 8), (66, 10), (78, 12), (80, 22), (70, 26), (56, 24), (44, 27), (30, 30), (22, 24)], K)
    L.ell(30, 18, 12, 11, K)
    # lomo erizado
    L.poly([(28, 9), (31, 4), (35, 7), (39, 3), (43, 7), (47, 4), (51, 8), (55, 6), (59, 10), (64, 8), (66, 11), (40, 12)], K)
    # pelo iluminado (gris) en el lomo, la paletilla y la grupa
    L.poly([(30, 9), (32, 6), (35, 8), (39, 5), (43, 8), (47, 6), (51, 9), (55, 8), (58, 11), (64, 10), (76, 13), (60, 14), (40, 13)], G1)
    L.curve((33, 7), (40, 4), (48, 6), 1.0, G2)
    L.curve((22, 14), (24, 20), (28, 26), 2.0, G1)
    L.curve((70, 14), (77, 17), (78, 22), 2.4, G1)
    # cabeza alta con hocico abierto y orejas tiesas
    L.poly([(30, 8), (22, 4), (12, 7), (0, 12), (2, 14), (14, 14), (22, 18), (30, 18)], K)
    L.poly([(4, 17), (14, 16), (24, 20), (16, 23), (6, 21)], K)          # mandíbula abierta
    L.poly([(22, 5), (21, -2), (27, 4)], K)                              # oreja
    L.poly([(27, 6), (28, 0), (31, 6)], K)                               # oreja lejana
    L.curve((26, 6), (16, 5), (6, 9), 1.6, G1)                           # luz en la frente y el hocico
    L.curve((22, 5), (14, 5), (8, 8), 0.8, G2)
    L.poly([(4, 15), (14, 15), (22, 19), (13, 18)], RD)                  # fauces
    for u in (6, 10, 14):                                                # colmillos
        L.line([(u, 14), (u, 16)], 0.8, WT)
    L.line([(9, 21), (9, 19)], 0.8, WT)
    L.ell(19, 9, 2.0, 1.4, RD)                                           # ojo
    return L
