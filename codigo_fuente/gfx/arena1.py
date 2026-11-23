#!/usr/bin/env python3
"""Arena del Strigoi Mort (Fase 1) -> ../src/arena1.s

Pantalla fija de 21 filas ANTIC 4 (sin scroll) con tres juegos de caracteres:
  ARA  filas 0-4    fuente (0-63) + cielo y luna (64-127)   (también el marcador)
  ARP  filas 5-12   parte alta del Strigoi Mort
  ARQ  filas 13-20  tumbas, suelo, parte baja de Mort, lobo (izq./der.) y esquirlas de hielo
Mort se dibuja copiando un bloque de 13 x 11 códigos en una de tres tumbas.
El lobo es un bloque de 8 x 4 códigos que avanza de casilla en casilla.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from arte import Escena, Lienzo, T
import jefe1_mort as JM
import lobo as LB
import font

OUT = os.path.join(HERE, '..', 'src', 'arena1.s')
K = 0x00
MX = [8, 56, 100]                  # x (píxeles) de Mort en cada tumba
MY = 40                            # línea superior de Mort (fila 5)
TOMB_X = [x + 16 for x in MX]      # tumbas de 20 px bajo sus pies
WOLF_K = 0.68
SHARD_ROW = 15
ROWS_A, ROWS_P, ROWS_Q = range(0, 5), range(5, 13), range(13, 21)


# ---------------------------------------------------------------- paletas
def bands_mort():
    B = [list(b) for b in JM.bands()]
    for r in range(21):
        if len(B[r]) < 5:
            B[r] = B[r] + [0x0C]
    for r in range(13, 21):            # donde vuela el baltag: PF3 = gris del hacha
        B[r][4] = 0x0C
    return B


def bands_lobo():
    B = bands_mort()
    for r in range(13, 18):
        B[r] = [B[r][0], K, 0x06, 0x44, 0x0C]      # rojo del lobo en PF2; brillo (y tumbas, y hacha) en PF3
    return B


def tumba(E, x0):
    """tumba de la arena: el brillo en gris $0C (PF3), igual en las dos formas del jefe"""
    L = Lienzo(20, 16)
    L.poly([(0, 15), (0, 2), (4, 0), (36, 0), (40, 2), (40, 15)], 0x06)
    L.rect(2, 1, 36, 2, 0x0C); L.rect(1, 2, 2, 15, 0x0C)
    L.rect(6, 6, 34, 7, 0x00); L.rect(6, 10, 34, 11, 0x00)
    E.paste(L.wide(), x0, 128)


# ---------------------------------------------------------------- juegos de caracteres
class Juego:
    def __init__(s, name, first=1, base=None):
        s.name = name
        s.data = bytearray(1024) if base is None else bytearray(base)
        s.cells = {}
        s.next = first

    def code(s, cellbytes):
        if cellbytes == bytes(8):
            return 0
        if cellbytes not in s.cells:
            assert s.next < 128, 'juego %s lleno' % s.name
            s.cells[cellbytes] = s.next
            s.data[s.next * 8:s.next * 8 + 8] = cellbytes
            s.next += 1
        return s.cells[cellbytes]


def cell_of(idx, r, cx):
    c = idx[r * 8:r * 8 + 8, cx * 4:cx * 4 + 4]
    inv = bool((c == 4).any())
    v = np.where(c == 4, 3, c)
    out = bytes(int(v[y, 0]) << 6 | int(v[y, 1]) << 4 | int(v[y, 2]) << 2 | int(v[y, 3]) for y in range(8))
    return out, inv


def juego_de_fila(r):
    return 'A' if r in ROWS_A else ('P' if r in ROWS_P else 'Q')


def main():
    fb = font.font_bytes()
    JA = Juego('ARA', 64, base=bytes(fb[:512]) + bytes(512))
    JP = Juego('ARP')
    JQ = Juego('ARQ')
    JS = {'A': JA, 'P': JP, 'Q': JQ}

    # ---------- fondo: cielo, luna, tres tumbas, suelo
    E = Escena(bands_mort())
    JM.luna(E)
    for x in TOMB_X:
        tumba(E, x)
    G = Lienzo(160, 24)
    G.rect(0, 0, 319, 1, 0x24)                                   # borde de la hierba (fila 18)
    for u in range(0, 320, 6):
        G.line([(u, 0), (u + 2, 4)], 1.0, 0xC4)
    for (u, v) in ((20, 12), (70, 18), (130, 10), (190, 16), (250, 12), (300, 20), (100, 22)):
        G.ell(u, v, 2.0, 1.0, 0x22)
    E.paste(G.wide(), 0, 144)
    E.quantize()
    BG = np.zeros((21, 40), dtype=np.int32)
    for r in range(21):
        for cx in range(40):
            cb, inv = cell_of(E.idx, r, cx)
            code = JS[juego_de_fila(r)].code(cb)
            BG[r, cx] = code | (0x80 if inv and code else 0)

    # ---------- Mort (en la primera tumba; las casillas son las mismas en las otras)
    EM = Escena(bands_mort())
    EM.paste(JM.build(), MX[0], MY)
    EM.quantize()
    MB = np.zeros((11, 13), dtype=np.int32)
    for j in range(11):
        r = 5 + j
        for i in range(13):
            cb, inv = cell_of(EM.idx, r, MX[0] // 4 + i)
            code = JS[juego_de_fila(r)].code(cb)
            MB[j, i] = code | (0x80 if inv and code else 0)
    print('ARP tras Mort:', JP.next - 1, ' ARQ tras Mort:', JQ.next - 1)

    # ---------- lobo (32 x 26), apoyado en el suelo (línea 144): filas 14-17
    W = LB.lobo(WOLF_K).wide()                  # mira a la izquierda
    WOLF = {}
    for name, arr in (('L', W), ('R', W[:, ::-1])):
        EW = Escena(bands_lobo())
        EW.paste(arr, 40, 144 - arr.shape[0])
        EW.quantize()
        blk = np.zeros((4, 8), dtype=np.int32)
        for j in range(4):
            r = 14 + j
            for i in range(8):
                cb, inv = cell_of(EW.idx, r, 10 + i)
                code = JQ.code(cb)
                blk[j, i] = code | (0x80 if inv and code else 0)
        WOLF[name] = blk
    print('ARQ tras el lobo:', JQ.next - 1)

    # ---------- esquirla de hielo (fila 15, PF3 = blanco durante el viento)
    shard = bytes([0b00000000, 0b00000011, 0b00001111, 0b11111111, 0b11111111, 0b00001111, 0b00000011, 0b00000000])
    SH = JQ.code(shard) | 0x80
    print('ARQ total:', JQ.next - 1, ' ARA total:', JA.next - 64)

    # ---------- mapa de colisión (13 filas de página: pantalla 8-20), valor = clase
    AMAP = np.zeros((13, 256), dtype=np.int32)
    for r in (8, 9):                            # tumbas (pantalla 16-17)
        for x in TOMB_X:
            for cx in range(x // 4, (x + 20) // 4):
                AMAP[r, cx] = 1
    AMAP[10:13, 0:40] = 1                       # suelo

    # ---------- murciélago (8 x 8, dos aleteos)
    BAT = [[0b10000001, 0b11000011, 0b11100111, 0b01111110, 0b00111100, 0b00011000, 0, 0],
           [0, 0b00100100, 0b01100110, 0b11111111, 0b10111101, 0b00011000, 0, 0]]

    # ---------- salida
    def bl(data, per=16):
        data = [int(x) for x in data]
        return '\n'.join('        .byte ' + ','.join('$%02X' % (b & 0xFF) for b in data[i:i + per]) for i in range(0, len(data), per))
    BM, BL = bands_mort(), bands_lobo()
    assert bytes(JA.data[:512]) == bytes(fb[:512])
    L = ['; generado por gfx/arena1.py · no editar a mano', '        .segment "AR1"']
    L.append(bl(JA.data[512:]))
    for J in (JP, JQ):
        L.append(bl(J.data))
    for r in range(13):
        L.append(bl(AMAP[r]))
    L += ['ARENA_BG:']
    for r in range(21):
        L.append(bl(BG[r], 40))
    for nm, i in (('AT_BK', 0), ('AT_PF0', 1), ('AT_PF1', 2), ('AT_PF2', 3), ('AT_PF3', 4)):
        L.append(nm + ':'); L.append(bl([BM[r][i] for r in range(21)] + [0]))
    HUDS = ' PUNTOS 000000  RADU 3  ' + '■' * 16
    assert len(HUDS) == 40
    L += ['HUDA:', bl(font.text(HUDS, 40), 20)]
    L.append('HUDA_BAR = %d' % HUDS.index('■'))
    L.append('BAR_CODE = %d' % font.CODE['■'])
    # pantallas de victoria
    for name, t, col in (('T_V1', '¡FASE 1 SUPERADA!', 0), ('T_V2', 'EL STRIGOI MORT', 1), ('T_V3', 'HA CAÍDO', 1),
                         ('T_V4', 'BONIFICACIÓN 5000', 2)):
        L += [name + ':', bl(font.text(t, 20, True, col), 20)]
    L += ['MORT_BLK:'] + [bl(MB[j], 13) for j in range(11)]
    L += ['WOLF_L:'] + [bl(WOLF['L'][j], 8) for j in range(4)]
    L += ['WOLF_R:'] + [bl(WOLF['R'][j], 8) for j in range(4)]
    L.append('SHARD = $%02X' % SH)
    L.append('SHARD_ROW = %d' % SHARD_ROW)
    L.append('MORT_COL: .byte %s' % ','.join(str(x // 4) for x in MX))
    L.append('MORT_ROW = %d' % (MY // 8))
    for nm, i in (('WT_BK', 0), ('WT_PF0', 1), ('WT_PF1', 2), ('WT_PF2', 3), ('WT_PF3', 4)):
        L.append(nm + ':'); L.append(bl([BL[r][i] for r in range(13, 18)]))
    L.append('ARENA_FLOOR_COLS = 40')
    open(OUT, 'w').write('\n'.join(L) + '\n')

    # vista previa: fondo + Mort en la tumba central + lobo
    E2 = Escena(bands_mort())
    JM.luna(E2)
    for x in TOMB_X:
        tumba(E2, x)
    E2.paste(G.wide(), 0, 144)
    E2.paste(JM.build(), MX[1], MY)
    E2.quantize()
    E2.render(scale=3).save(os.path.join(HERE, '..', 'build', 'arena1_prev.png'))
    print('ok')


if __name__ == '__main__':
    main()
