#!/usr/bin/env python3
"""Minijefe: EL CĂPCĂUN · ogro caníbal gigante con un fémur por garrote, empalados al fondo"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from arte import Escena, Lienzo, T

K = 0x00
O1, O2, O3 = 0xE2, 0xE6, 0xE6      # piel verde oliva de cadáver: sombra, media (sin luz aparte)
BO = 0x0C                          # hueso
SKY = [0x40, 0x40, 0x40, 0x40, 0x42, 0x42, 0x42, 0x42, 0x42, 0x44, 0x44, 0x44, 0x44, 0x46, 0x46, 0x46, 0x46, 0x46]


def calavera(L, u, v, s=1.0):
    L.ell(u, v, 4.5 * s, 4.0 * s, BO)
    L.rect(u - 2.5 * s, v + 2, u + 2.5 * s, v + 5 * s, BO)
    L.ell(u - 1.8 * s, v, 1.2 * s, 1.2 * s, K); L.ell(u + 1.8 * s, v, 1.2 * s, 1.2 * s, K)


def empalado(L, u, top, side=1):
    """estaca con un esqueleto ensartado"""
    L.line([(u, 144), (u, top)], 2.4, K)
    L.poly([(u - 1.5, top), (u, top - 8), (u + 1.5, top)], K)
    v = top + 6
    calavera(L, u + side * 2, v, 0.9)                            # cráneo caído hacia un lado
    for i in range(4):                                            # costillas
        L.curve((u - 5, v + 9 + i * 3), (u, v + 7 + i * 3), (u + 5, v + 9 + i * 3), 1.0, BO)
    L.line([(u, v + 6), (u, v + 22)], 1.0, BO)                    # columna
    L.curve((u - 4, v + 8), (u - 9, v + 16), (u - 8, v + 26), 1.0, BO)   # brazos colgando
    L.curve((u + 4, v + 8), (u + 9, v + 16), (u + 8, v + 26), 1.0, BO)
    L.curve((u - 2, v + 22), (u - 5, v + 32), (u - 4, v + 42), 1.0, BO)  # piernas
    L.curve((u + 2, v + 22), (u + 4, v + 32), (u + 6, v + 41), 1.0, BO)


def fondo(E):
    L = Lienzo(160, 168)
    # montes lejanos en silueta
    L.poly([(0, 110), (40, 92), (80, 104), (130, 84), (190, 100), (240, 80), (290, 96), (320, 88), (320, 144), (0, 144)], K)
    # campo de empalados
    for (u, top, sd) in ((14, 58, 1), (46, 74, -1), (78, 50, 1), (110, 80, -1), (300, 64, 1)):
        empalado(L, u, top, sd)
    # suelo
    L.rect(0, 144, 319, 167, K)
    L.poly([(0, 144), (60, 141), (130, 145), (200, 140), (320, 143), (320, 150), (0, 150)], 0x22)
    for (u, v) in ((30, 152), (150, 156), (250, 154)):
        calavera(L, u, v, 0.8)
    E.paste(L.wide(), 0, 0)


def ogro():
    L = Lienzo(160, 150)
    # ---------- brazo derecho caído, con una pierna humana a medio roer ----------
    L.curve((268, 70), (292, 96), (296, 122), 16.0, K, w1=12.0)
    L.curve((268, 70), (291, 96), (295, 121), 13.0, O1, w1=9.0)
    L.ell(296, 124, 8, 7, K); L.ell(295, 123, 6.5, 5.5, O2)
    L.curve((300, 118), (312, 128), (316, 140), 3.0, BO)           # hueso que asoma de la mano
    L.ell(316, 141, 2.4, 2.0, BO)
    # ---------- piernas cortas y gruesas ----------
    for (a, b, c, w) in (((200, 118), (190, 132), (188, 146), 22.0), ((250, 118), (258, 132), (258, 146), 24.0)):
        L.curve(a, b, c, w, K, w1=w * 0.8)
        L.curve(a, b, (c[0], c[1] - 1), w - 3, O1, w1=w * 0.8 - 3)
        L.ell(c[0] - 4, 146, 14, 4, K)

    # ---------- barriga enorme ----------
    L.ell(226, 98, 54, 38, K)
    L.ell(224, 97, 52, 36, O2)
    L.ell(254, 104, 26, 28, O1)                                    # lado en sombra

    L.ell(226, 112, 2.0, 1.6, K)                                   # ombligo
    for (u, v) in ((196, 104), (240, 84), (212, 124), (258, 116), (186, 90)):
        L.ell(u, v, 1.6, 1.4, K)                                   # verrugas
    L.curve((200, 96), (214, 104), (230, 100), 1.0, K)             # cicatriz
    # taparrabos de piel
    L.poly([(174, 116), (278, 116), (272, 128), (262, 124), (254, 134), (242, 124), (228, 136), (216, 124),
            (202, 134), (192, 124), (180, 130)], K)
    L.rect(176, 114, 276, 118, 0x22)
    calavera(L, 226, 118, 1.0)                                     # hebilla
    # ---------- hombros y pecho encorvados ----------
    L.ell(222, 56, 58, 26, K)
    L.ell(220, 55, 56, 24, O2)
    L.ell(250, 60, 30, 18, O1)

    # collar de calaveras
    for i, u in enumerate((178, 196, 214, 232, 250, 266)):
        v = 64 + (6 if 1 <= i <= 4 else 0) + (3 if i in (2, 3) else 0)
        L.line([(u, v - 4), (u + 18, v - 4)], 0.8, K)
        calavera(L, u, v, 1.0)
    # ---------- brazo izquierdo en alto con el fémur ----------
    L.curve((182, 50), (150, 50), (132, 26), 18.0, K, w1=13.0)
    L.curve((182, 50), (151, 49), (133, 27), 15.0, O2, w1=10.0)

    # fémur gigante (diagonal) con sus cabezas articulares
    L.line([(98, 4), (152, 58)], 11.0, K)
    L.line([(98, 4), (152, 58)], 8.0, BO)
    for (u, v) in ((96, 2), (154, 60)):
        L.ell(u - 3, v + 2, 7, 6, K); L.ell(u + 3, v - 2, 7, 6, K)
        L.ell(u - 3, v + 2, 5.5, 4.5, BO); L.ell(u + 3, v - 2, 5.5, 4.5, BO)
    L.ell(132, 26, 10, 9, K); L.ell(131, 25, 8.5, 7.5, O2)         # puño sobre el hueso
    # ---------- cabeza enorme hundida entre los hombros ----------
    L.ell(172, 44, 32, 28, K)
    L.ell(171, 43, 30, 26, O2)
    L.ell(190, 50, 14, 18, O1)                                     # lado en sombra
    # orejas caídas
    L.poly([(198, 34), (218, 42), (214, 64), (200, 58)], K); L.poly([(200, 37), (215, 44), (211, 60), (201, 55)], O1)
    # bocaza abierta de oreja a oreja con dientes desiguales
    L.poly([(146, 50), (200, 48), (198, 62), (174, 72), (148, 62)], K)
    for (u, h) in ((152, 6), (159, 4), (165, 7), (172, 3), (179, 6), (186, 4), (193, 6)):
        L.poly([(u - 2.5, 50), (u + 2.5, 50), (u, 50 + h)], BO)
    for (u, h) in ((156, 4), (166, 6), (178, 5), (190, 4)):
        L.poly([(u - 2.5, 64), (u + 2.5, 64), (u, 64 - h)], BO)
    L.poly([(148, 62), (150, 48), (154, 60)], BO)                  # colmillos que suben
    L.poly([(194, 60), (198, 46), (200, 58)], BO)
    L.curve((160, 70), (162, 80), (160, 90), 2.0, O2)              # baba colgando
    # nariz de cerdo
    L.ell(168, 40, 8, 5.5, K); L.ell(168, 39, 6.5, 4.5, O1)
    L.ell(165, 40, 1.6, 1.6, K); L.ell(171, 40, 1.6, 1.6, K)
    # ceja única
    L.poly([(148, 26), (194, 22), (192, 28), (150, 32)], K)
    for u in (160, 172, 184):
        L.curve((u, 20), (u + 2, 13), (u - 1, 9), 1.2, K)
    return L


# ojos desparejos (uno pequeño, otro saltón), a mano
# ojos desparejos: cuencas negras que ocupan casillas enteras (4 x 8) para que el blanco quepa
EYES = """
kkkk....kkkkkkkk
kkkk....kkbbbbkk
kbbk....kbbbbbbk
kbkk....kbbkkbbk
kkkk....kbbkkbbk
kkkk....kbbbbbbk
kkkk....kkbbbbkk
kkkk....kkkkkkkk
"""


def bands():
    B = []
    for r in range(21):
        bk = SKY[r] if r < 18 else 0x10
        if r < 18:
            B.append([bk, K, O1, O2, BO])           # cielo de sangre; ogro (hueso en PF3)
        else:
            B.append([0x10, K, 0x22, BO])
    return B


def escena():
    E = Escena(bands())
    fondo(E)
    L = ogro()
    L.ascii(76, 32, EYES, {'k': K, 'b': BO})
    E.paste(L.wide(), 0, 0)
    return E


if __name__ == '__main__':
    E = escena()
    print(E.quantize(), 'casillas:', E.cells(range(21)))
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'jefe7_borrador.png'))
