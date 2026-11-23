#!/usr/bin/env python3
"""Jefe 5: EL REY STRIGOI · quimera alada de sombra y sangre (frontal, alas abiertas)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T

K = 0x00
M1, M2 = 0x42, 0x46        # membrana (sangre) oscura y clara
SH = 0x54                  # brillo de sombra (violeta)
HEART = 0x2E               # corazón incandescente / ojos
BONE = 0x0A
BKR = 0x90


def mir(pts, c=160):
    return [(2 * c - u, v) for (u, v) in pts]


def rey():
    L = Lienzo(160, 140)
    # ---------- alas (izquierda y su espejo) ----------
    for side in (0, 1):
        f = (lambda p: p) if side == 0 else (lambda p: mir(p))
        memb = [(134, 46), (96, 22), (60, 8), (30, 4), (8, 14), (2, 34), (14, 40), (12, 60), (28, 62), (34, 82),
                (52, 80), (66, 96), (86, 86), (104, 98), (118, 80), (136, 72)]
        L.poly(f(memb), K)
        L.poly(f([(132, 48), (96, 25), (60, 11), (30, 7), (10, 16), (6, 32), (18, 38), (16, 56), (30, 58), (37, 77),
                  (52, 76), (66, 91), (86, 82), (103, 93), (116, 78), (134, 70)]), M1)
        # zona iluminada cerca del brazo del ala
        # varillas (dedos del ala) desde la muñeca
        wrist = (60, 10)
        L.curve(f([(134, 46)])[0], f([(100, 24)])[0], f([wrist])[0], 5.0, K, w1=3.0)
        for tip in ((4, 16), (8, 38), (26, 62), (52, 80), (86, 86), (118, 80)):
            mid = ((wrist[0] + tip[0]) / 2 + 4, (wrist[1] + tip[1]) / 2 - 4)
            L.curve(f([wrist])[0], f([mid])[0], f([tip])[0], 3.2, K, w1=2.0)
        L.poly(f([(56, 4), (62, -2), (66, 8)]), BONE)          # garra del ala
    # ---------- cola con aguijón ----------
    L.curve((170, 110), (220, 134), (252, 112), 7.0, K, w1=3.0)
    L.curve((170, 110), (220, 132), (251, 112), 4.6, M1, w1=1.6)
    L.poly([(248, 104), (262, 104), (254, 120)], BONE)
    # ---------- patas con garras ----------
    for sgn in (-1, 1):
        hx = 160 + sgn * 16
        L.curve((hx, 92), (hx + sgn * 14, 108), (hx + sgn * 6, 126), 13.0, K, w1=7.0)
        L.curve((hx, 92), (hx + sgn * 13, 108), (hx + sgn * 6, 125), 9.0, M1, w1=5.0)
        for d in (-6, 0, 6):
            L.curve((hx + sgn * 6 + d, 126), (hx + sgn * 6 + d * 1.6, 132), (hx + sgn * 6 + d * 2.2, 137), 2.4, BONE, w1=0.8)
    # ---------- torso de sombra: hombros, pectorales, abdomen y cintura ----------
    L.ell(140, 50, 12, 9, K); L.ell(180, 50, 12, 9, K)                      # hombros
    L.poly([(130, 50), (190, 50), (182, 70), (172, 92), (148, 92), (138, 70)], K)
    L.ell(150, 60, 12, 10, K); L.ell(170, 60, 12, 10, K)                    # pectorales
    # luz violeta: media luna en el hombro y el pectoral izquierdos, costillas
    L.ell(138, 48, 7, 4.5, SH); L.ell(140, 50, 6, 3.5, K)
    L.ell(147, 58, 8, 6.5, SH); L.ell(150, 60, 7, 6, K)
    for v in (74, 80, 86):
        L.curve((150, v - 2), (154, v + 1), (159, v), 1.6, SH)
        L.curve((170, v - 2), (166, v + 1), (161, v), 1.0, SH)
    L.line([(160, 70), (160, 90)], 1.0, SH)
    # corazón incandescente (punto débil)
    L.ell(160, 58, 10, 8.5, M1)
    L.ell(160, 58, 7.5, 6.5, K)
    L.ell(160, 58, 6, 5.2, HEART)
    L.curve((157, 54), (160, 58), (158, 63), 0.9, K)
    L.curve((163, 55), (161, 59), (164, 62), 0.9, K)
    # ---------- cabeza: cráneo demoníaco con cuernos y corona ----------
    L.curve((148, 20), (118, 18), (114, -4), 8.0, K, w1=2.4)
    L.curve((172, 20), (202, 18), (206, -4), 8.0, K, w1=2.4)
    L.curve((147, 19), (121, 17), (116, -2), 2.4, BONE, w1=1.0)
    L.ell(160, 26, 16, 18, K)
    L.curve((146, 22), (154, 17), (159, 22), 2.4, BONE)                    # arco de la ceja
    L.curve((174, 22), (166, 17), (161, 22), 2.0, BONE)
    L.curve((146, 36), (150, 40), (154, 42), 2.0, BONE)                    # pómulos (fuera de las casillas de los ojos)
    L.curve((174, 36), (170, 40), (166, 42), 1.6, BONE)
    for (u, h) in ((150, 6), (155, 9), (160, 11), (165, 9), (170, 6)):     # corona de púas
        L.poly([(u - 2, 14), (u, 14 - h), (u + 2, 14)], BONE)
    L.rect(148, 12, 172, 14, BONE)
    return L


EYES = """
kyyykyyyk
.yyk.kyy.
"""
FANGS = """
w.w.w
w...w
"""


def sala(E):
    L = Lienzo(160, 168)
    for u0 in (6, 290):
        L.rect(u0, 0, u0 + 22, 135, K)
        L.rect(u0 + 3, 0, u0 + 6, 135, 0x92)
    # trono de sangre detrás
    L.poly([(130, 136), (130, 96), (140, 80), (180, 80), (190, 96), (190, 136)], K)
    # suelo ajedrezado
    for v in range(136, 168, 8):
        for u in range(0, 320, 16):
            if ((u // 16) + (v // 8)) % 2:
                L.rect(u, v, u + 15, v + 7, 0x92)
            else:
                L.rect(u, v, u + 15, v + 7, 0x90)
    E.paste(L.wide(), 0, 0)


def bands():
    B = []
    for r in range(21):
        if r < 6:
            B.append([BKR, K, M1, BONE, HEART])        # alas, corona de hueso, ojos (PF3 incandescente)
        elif r < 13:
            B.append([BKR, K, M1, SH, HEART])          # torso y corazón
        elif r < 17:
            B.append([BKR, K, M1, BONE, HEART])        # patas, garras, cola
        else:
            B.append([0x90, 0x92, 0x00, 0x42])          # suelo
    return B


def escena():
    E = Escena(bands())
    sala(E)
    L = rey()
    L.ascii(76, 27, EYES, {'y': HEART, 'k': K})
    L.ascii(78, 40, FANGS, {'w': BONE})
    E.paste(L.wide(), 0, 6)
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas del jefe:', E.cells(range(0, 17)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe5_borrador.png'))
