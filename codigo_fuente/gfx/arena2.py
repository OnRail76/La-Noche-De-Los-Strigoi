#!/usr/bin/env python3
"""Arena de ARIC, EL SASTRE DE LAS SOMBRAS (Fase 2) -> ../src/arena2.s
Taller de la Torre de los Sastres: ventanal, mesas de corte a los lados (plataformas),
suelo de tablas. Aric flota en el centro (bloque fijo de casillas); su cabeza la
protege un escudo de seis retales encantados que se arrancan de uno en uno."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from arte import Escena, Lienzo
import jefe2_aric as JA2
from arena1 import Juego, cell_of
import font

OUT = os.path.join(HERE, '..', 'src', 'arena2.s')
K = 0x00
BKR = 0x20
X0, Y0 = 48, 48                 # Aric (64 x 100) en píxeles de la escena
AC0, AR0 = X0 // 4, Y0 // 8     # columna y fila del bloque
AW, AH = 16, 13
ROWS_A, ROWS_P, ROWS_Q = range(0, 6), range(6, 12), range(12, 21)
TABLE_Y = 112                   # tablero de las mesas (fila 14)
FLOOR_Y = 144                   # suelo (fila 18)
TL = (4, 40)                    # mesa izquierda (x en píxeles)
TR = (120, 156)


def bands():
    T1, T2, T3, RC = JA2.T1, JA2.T2, JA2.T3, JA2.RC
    B = []
    for r in range(21):
        if r < 6:   B.append([BKR, K, 0x24, 0xAE, RC])        # vigas, ventanal (PF2 = cristal), retales
        elif r < 9: B.append([BKR, K, T2, T3, RC])            # cabeza, hombros: retales rojos en PF3
        elif r < 14: B.append([BKR, K, T1, T2, T3])           # torso
        elif r < 16: B.append([BKR, K, T1, T2, 0x26])         # jirones; mesas en PF3 (casillas invertidas)
        elif r < 18: B.append([BKR, K, T1, T2, 0x0C])         # patas; agujas clavadas (PF3)
        else:        B.append([0x10, K, 0x22, 0x26, 0x0C])    # suelo de tablas
    return B


def sala(E):
    L = Lienzo(160, 168)
    L.rect(0, 0, 319, 5, K)                                   # viga del techo
    for u in (40, 280):                                       # pilares
        L.rect(u - 6, 0, u + 6, 143, K)
    # ventanal ojival en el centro, por encima de Aric
    L.poly([(124, 46), (124, 22), (140, 8), (160, 2), (180, 8), (196, 22), (196, 46)], K)
    L.poly([(128, 46), (128, 24), (142, 11), (160, 6), (178, 11), (192, 24), (192, 46)], 0xAE)
    L.rect(158, 6, 162, 46, K); L.rect(128, 26, 192, 28, K)
    # mesas de corte
    for (a, b) in (TL, TR):
        L.rect(a * 2, TABLE_Y, b * 2 - 1, TABLE_Y + 3, 0x26)
        for lx in (a * 2 + 4, b * 2 - 8):
            L.rect(lx, TABLE_Y + 4, lx + 3, FLOOR_Y - 1, K)
    # rollo de tela sobre la mesa izquierda y maniquí sobre la derecha
    L.ell(30, TABLE_Y - 4, 10, 4, 0x26)
    L.ell(272, TABLE_Y - 22, 7, 5, K); L.poly([(262, TABLE_Y - 18), (282, TABLE_Y - 18), (278, TABLE_Y - 4), (266, TABLE_Y - 4)], K)
    L.rect(270, TABLE_Y - 4, 273, TABLE_Y - 1, K)
    E.paste(L.wide(), 0, 0)
    # suelo: tablas con un patrón que se repite cada casilla (4 píxeles)
    F = np.full((24, 160), 0x22, dtype=np.int16)
    for y in range(24):
        for x in range(160):
            if y % 6 == 0: F[y, x] = 0x26
            elif x % 4 == 0 and (y // 6) % 2 == 0: F[y, x] = K
    E.paste(F, 0, FLOOR_Y)


def main():
    fb = font.font_bytes()
    JA = Juego('ARA', 64, base=bytes(fb[:512]) + bytes(512))
    JP, JQ = Juego('ARP'), Juego('ARQ')
    JS = lambda r: JA if r in ROWS_A else (JP if r in ROWS_P else JQ)

    def codes(E, r0, c0, w, h):
        out = np.zeros((h, w), dtype=np.int32)
        for j in range(h):
            for i in range(w):
                cb, inv = cell_of(E.idx, r0 + j, c0 + i)
                code = JS(r0 + j).code(cb)
                out[j, i] = code | (0x80 if inv and code else 0)
        return out

    E = Escena(bands()); sala(E); E.quantize()
    BG = codes(E, 0, 0, 40, 21)
    # Aric con escudo (S) y sin escudo (N), sobre el fondo
    ES = Escena(bands()); sala(ES); ES.paste(JA2.build(), X0, Y0); ES.quantize()
    S = codes(ES, AR0, AC0, AW, AH)
    LN = JA2.aric()
    LN.ascii(JA2.W // 2 - 9, 3, JA2.HEAD, {'k': K, '2': JA2.T2, '3': JA2.T3, 'W': JA2.T3})
    EN = Escena(bands()); sala(EN); EN.paste(LN.wide(), X0, Y0); EN.quantize()
    N = codes(EN, AR0, AC0, AW, AH)
    print('ARA', JA.next - 64, 'ARP', JP.next - 1, 'ARQ', JQ.next - 1)
    # retales: rectángulos de casillas (en el bloque) que hay que redibujar sin el retal
    PP = [(8, 0), (50, 1), (3, 12), (55, 12), (14, 20), (45, 20)]
    PATCHES = []
    used = set()
    for (px, py) in PP:
        c0, c1 = (X0 + px) // 4 - AC0, (X0 + px + 5) // 4 - AC0
        r0, r1 = (Y0 + py) // 8 - AR0, (Y0 + py + 6) // 8 - AR0
        cells = {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)}
        assert not (cells & used), 'retales que comparten casillas'
        used |= cells
        PATCHES.append((r0, c0, c1 - c0 + 1, r1 - r0 + 1))
    # aguja clavada en el suelo (filas 16-17, PF1): ojo arriba, punta abajo
    nt = bytes([0b00000000, 0b00111100, 0b00110000, 0b00111100, 0b00111100, 0b00111100, 0b00111100, 0b00111100])
    nb = bytes([0b00111100, 0b00111100, 0b00111100, 0b00111100, 0b00111100, 0b00111100, 0b00110000, 0b00110000])
    NT, NB = JQ.code(nt) | 0x80, JQ.code(nb) | 0x80
    print('ARQ total', JQ.next - 1)

    AMAP = np.zeros((13, 256), dtype=np.int32)
    AMAP[10:13, 0:40] = 1
    for (a, b) in (TL, TR):
        AMAP[(TABLE_Y // 8) - 8, a // 4:(b + 3) // 4] = 1

    def bl(data, per=16):
        data = [int(x) & 255 for x in data]
        return '\n'.join('        .byte ' + ','.join('$%02X' % b for b in data[i:i + per]) for i in range(0, len(data), per))
    B = bands()
    L = ['; generado por gfx/arena2.py · no editar a mano', '        .segment "AR2"']
    L.append(bl(JA.data[512:]))
    L.append(bl(JP.data)); L.append(bl(JQ.data))
    for r in range(13): L.append(bl(AMAP[r]))
    L.append('ARENA_BG2:')
    for r in range(21): L.append(bl(BG[r], 40))
    for nm, i in (('AT_BK2', 0), ('AT_PF02', 1), ('AT_PF12', 2), ('AT_PF22', 3), ('AT_PF32', 4)):
        L.append(nm + ':'); L.append(bl([(B[r] + [0x0C])[i] for r in range(21)] + [0]))
    HUDS = ' PUNTOS 000000  RADU 3  ' + '■' * 16
    L += ['HUDA2:', bl(font.text(HUDS, 40), 20)]
    for name, t, col in (('T_V12', '¡FASE 2 SUPERADA!', 0), ('T_V22', 'ARIC, EL SASTRE', 1), ('T_V32', 'HA CAÍDO', 1),
                         ('T_V42', 'BONIFICACIÓN 5000', 2)):
        L += [name + ':', bl(font.text(t, 20, True, col), 20)]
    L += ['ARIC_S:'] + [bl(S[j], AW) for j in range(AH)]
    L += ['ARIC_N:'] + [bl(N[j], AW) for j in range(AH)]
    L.append('ARIC_C = %d' % AC0); L.append('ARIC_R = %d' % AR0)
    L.append('ARIC_W = %d' % AW); L.append('ARIC_H = %d' % AH)
    # retales: fila, columna, ancho, alto y códigos sin retal
    for k, (r0, c0, w, h) in enumerate(PATCHES):
        L.append('PATCH%d: .byte %d,%d,%d,%d' % (k, r0 + AR0, c0 + AC0, w, h))
        L.append(bl([N[r0 + j][c0 + i] for j in range(h) for i in range(w)]))
    L.append('PATCH_LO: .byte ' + ','.join('<PATCH%d' % k for k in range(6)))
    L.append('PATCH_HI: .byte ' + ','.join('>PATCH%d' % k for k in range(6)))
    L.append('NEEDLE_T = $%02X' % NT); L.append('NEEDLE_B = $%02X' % NB)
    L.append('ARIC_X0 = %d' % X0); L.append('ARIC_Y0 = %d' % Y0)
    L.append('        .assert ARENA_BG2 = ARENA_BG, error, "arena2: ARENA_BG"')
    L.append('        .assert AT_BK2 = AT_BK, error, "arena2: AT_BK"')
    L.append('        .assert HUDA2 = HUDA, error, "arena2: HUDA"')
    L.append('        .assert T_V12 = T_V1, error, "arena2: T_V1"')
    open(OUT, 'w').write('\n'.join(L) + '\n')

    # vista previa
    EP = Escena(bands()); sala(EP); EP.paste(JA2.build(), X0, Y0); EP.quantize()
    EP.render(scale=3).save(os.path.join(HERE, '..', 'build', 'arena2_prev.png'))
    print('ok')


if __name__ == '__main__':
    main()
