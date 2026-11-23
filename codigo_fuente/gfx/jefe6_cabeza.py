#!/usr/bin/env python3
"""Jefe final: EL REY STRIGOI, SEGUNDA PARTE · cabeza de vampiro gigante; la boca es el punto débil"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T

K = 0x00
S1, S2, S3 = 0x62, 0x66, 0x6A      # piel lívida violácea: sombra, media, luz
RE = 0x2E                          # ojos de fuego (como los del Rey Strigoi)
MO1, MO2 = 0x42, 0x44              # boca (garganta incandescente)
FA = 0x0E                          # colmillos
BKR = 0x80


def mir(pts, c=160):
    return [(2 * c - u, v) for (u, v) in pts]


def cabeza():
    L = Lienzo(160, 168)
    c = 160
    # ---------- orejas de murciélago ----------
    earL = [(98, 70), (64, 24), (70, 56), (60, 60), (84, 96), (100, 98)]
    L.poly(earL, K); L.poly(mir(earL), K)
    L.poly([(97, 72), (68, 32), (73, 58), (66, 61), (86, 93), (98, 94)], S2)
    L.poly([(94, 74), (74, 44), (78, 62), (90, 88)], S1)
    L.poly(mir([(97, 72), (68, 32), (73, 58), (66, 61), (86, 93), (98, 94)]), S1)
    # ---------- cráneo y mandíbula ----------
    L.ell(c, 70, 64, 62, K)
    L.poly([(98, 80), (222, 80), (210, 132), (186, 158), (160, 166), (134, 158), (110, 132)], K)
    L.ell(c - 1, 70, 62, 60, S2)
    L.poly([(100, 80), (220, 80), (208, 131), (185, 156), (160, 164), (135, 156), (112, 131)], S2)
    # sombra en el lado derecho (luz desde la izquierda)
    L.poly([(186, 20), (222, 60), (220, 82), (208, 130), (186, 156), (172, 162), (190, 120), (200, 80), (196, 40)], S1)
    # luz en la frente y la mejilla izquierdas
    L.ell(136, 50, 24, 20, S3)
    L.poly([(108, 96), (126, 92), (130, 120), (118, 128)], S3)
    # ---------- pelo negro con pico de viuda ----------
    L.poly([(96, 52), (104, 20), (130, 6), (160, 2), (190, 6), (216, 20), (224, 52), (206, 34), (184, 28),
            (160, 52), (136, 28), (114, 34)], K)
    L.curve((112, 22), (136, 10), (156, 14), 2.0, S1)                   # brillo del pelo
    # ---------- cejas en V, cuencas y ojos ----------
    L.poly([(108, 58), (128, 52), (156, 66), (152, 72), (128, 62), (110, 64)], K)
    L.poly(mir([(108, 58), (128, 52), (156, 66), (152, 72), (128, 62), (110, 64)]), K)
    L.ell(132, 76, 18, 9, S1); L.ell(188, 76, 18, 9, S1)                # cuencas
    L.ell(132, 77, 14, 6.5, K); L.ell(188, 77, 14, 6.5, K)
    L.ell(132, 77, 12, 5.0, RE); L.ell(188, 77, 12, 5.0, RE)
    L.rect(130, 72, 134, 82, K); L.rect(186, 72, 190, 82, K)            # pupilas en rendija
    # ---------- nariz aguileña ----------
    L.poly([(156, 74), (164, 74), (168, 104), (172, 110), (160, 114), (148, 110), (152, 104)], S2)
    L.poly([(156, 74), (160, 74), (158, 104), (150, 110), (152, 104)], S3)
    L.poly([(164, 76), (168, 104), (172, 110), (166, 108)], S1)
    L.ell(152, 109, 3, 1.8, K); L.ell(168, 109, 3, 1.8, K)              # orificios
    # pómulos marcados
    L.curve((112, 100), (122, 112), (134, 118), 2.4, S1)
    L.curve((208, 100), (198, 112), (186, 118), 2.4, K)
    # ---------- boca abierta: el punto débil ----------
    L.poly([(122, 122), (140, 118), (160, 120), (180, 118), (198, 122), (192, 140), (176, 152), (160, 155),
            (144, 152), (128, 140)], K)
    L.poly([(128, 124), (142, 121), (160, 123), (178, 121), (192, 124), (187, 138), (174, 148), (160, 151),
            (146, 148), (133, 138)], MO1)
    L.ell(160, 139, 9, 5, K)                                             # garganta
    # colmillos superiores largos y dientes
    for (u, ln, w) in ((138, 20, 4), (182, 20, 4)):
        L.poly([(u - w, 121), (u + w, 121), (u, 121 + ln)], FA)
    for u in range(146, 176, 6):
        L.poly([(u - 2, 122), (u + 2, 122), (u, 128)], FA)
    for u in range(140, 182, 7):
        L.poly([(u - 2, 147), (u + 2, 147), (u, 141)], FA)
    # labio inferior y barbilla
    L.curve((132, 142), (160, 160), (188, 142), 2.0, S1)
    return L


def sala(E):
    L = Lienzo(160, 168)
    for u0 in (8, 278):                                  # columnas
        L.rect(u0, 0, u0 + 26, 167, K)
        L.rect(u0 + 4, 0, u0 + 8, 167, 0x82)
    E.paste(L.wide(), 0, 0)


def bands():
    B = []
    for r in range(21):
        if r < 8:
            B.append([BKR, K, S1, S2, S3])             # pelo, orejas, frente
        elif r < 11:
            B.append([BKR, K, S1, S2, RE])             # ojos (rojo en PF3)
        elif r < 14:
            B.append([BKR, K, S1, S2, S3])             # nariz y pómulos
        elif r < 20:
            B.append([BKR, K, S2, MO1, FA])            # boca (colmillos en PF3)
        else:
            B.append([BKR, K, S1, MO2])
    return B


def escena():
    E = Escena(bands())
    sala(E)
    E.paste(cabeza().wide(), 0, 0)
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas:', E.cells(range(21)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe6_borrador.png'))
