#!/usr/bin/env python3
"""Pantallas fijas: TÍTULO (logo A + Sighișoara de noche, también sirve para el
amanecer del final) y GAME OVER (letras góticas; la calavera es un sprite).
Misma disposición que las arenas 4-6: cielo de A · P · Q · R · libre desde $3000 ·
tablas en $3900. Salida: ../src/pantallas.s"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from arte import Escena, Lienzo, T
from arena1 import Juego, cell_of
import font
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import titulo as TT

ROWS = 14

def bl(data, per=16):
    data = [int(x) & 255 for x in data]
    return '\n'.join('        .byte ' + ','.join('$%02X' % v for v in data[i:i + per]) for i in range(0, len(data), per))

def charsets(E, ROWS=14):
    fb = font.font_bytes()
    for a in range(1, 8):
        for b in range(a + 1, 13):
            for c in range(b + 1, 15):
                JA = Juego('A', 64, base=bytes(fb[:512]) + bytes(512)); JP, JQ, JR = Juego('P'), Juego('Q'), Juego('R')
                JS = lambda r: JA if r < a else (JP if r < b else (JQ if r < c else JR))
                try:
                    out = np.zeros((21, 40), dtype=np.int32)
                    for r in range(ROWS):
                        for cx in range(40):
                            cb, inv = cell_of(E.idx, r, cx)
                            code = JS(r).code(cb)
                            out[r, cx] = code | (0x80 if inv and code else 0)
                    return (a, b, c), (JA, JP, JQ, JR), out
                except AssertionError:
                    pass
    raise SystemExit('pantalla: no cabe')

def escribir(seg, pre, E, extra_lines, consts, rows=14):
    (a, b, c), (JA, JP, JQ, JR), BG = charsets(E, rows)
    print('%s: A 0-%d P %d-%d Q %d-%d R %d-13 · %d %d %d %d' % (seg, a - 1, a, b - 1, b, c - 1, c, JA.next - 64, JP.next - 1, JQ.next - 1, JR.next - 1))
    L = ['; generado por gfx/pantallas.py · no editar a mano', '        .segment "%s"' % seg]
    L.append(bl(JA.data[512:])); L.append(bl(JP.data)); L.append(bl(JQ.data)); L.append(bl(JR.data))
    used = 0
    for name, t, col in extra_lines:                 # textos (modo 6, 20 caracteres)
        if isinstance(t, list):                      # trozos con colores distintos
            row = []
            for tt, cc in t: row += font.text(tt, len(tt), False, cc)
            pad = (20 - len(row)) // 2
            row = [0] * pad + row + [0] * (20 - pad - len(row))
            L += ['%s:' % name, bl(row, 20)]; used += 20; continue
        L += ['%s:' % name, bl(font.text(t, 20, True, col), 20)]; used += 20
    assert used <= 0x900
    L.append('        .res %d' % (0x900 - used))
    L.append(pre + 'BG:')
    for r in range(21): L.append(bl(BG[r], 40))
    B = E.bands
    for nm, i in (('BK', 0), ('PF0', 1), ('PF1', 2), ('PF2', 3), ('PF3', 4)):
        L.append(pre + nm + ':'); L.append(bl([(list(B[r]) + [0x0C] * 5)[i] for r in range(21)] + [0]))
    for k, v in list(consts.items()) + [('S1', a), ('S2', b), ('S3', c)]:
        L.append('%s%s = %d' % (pre, k, v))
    L.append('        .assert %sBG = ARENA_BG, error, "%s"' % (pre, seg))
    L.append('        .assert %sBK = AT_BK, error, "%s"' % (pre, seg))
    return L

# ---------------------------------------------------------------- TÍTULO
def titulo():
    SKY = [0x00] * 6 + [0x60, 0x62, 0x52, 0x54, 0x52, 0x50, 0x00, 0x00] + [0x00] * 7
    B = []
    for r in range(21):
        if r < 6: B.append([0x00, 0x20, [0x48, 0x48, 0x46, 0x44, 0x42, 0x42][r], 0x4C, 0x42])
        elif r < 12: B.append([SKY[r], 0x00, 0x0C, 0x0A, 0x1C])
        else: B.append([SKY[r], 0x00, 0x08, 0x06, 0x1C])
    E = Escena(B)
    logo = TT.palabra('STRIGOI')
    E.paste(logo, (160 - logo.shape[1]) // 2, 1)
    L = Lienzo(160, 168)
    L.ell(212, 70, 34, 16, 0x0C)                                          # luna
    L.ell(200, 66, 6, 3, 0x0A); L.ell(222, 76, 5, 3, 0x0A); L.ell(218, 62, 3, 2, 0x0A)
    sil = [(0, 112), (0, 96), (20, 94), (24, 88), (32, 88), (36, 94), (56, 92), (60, 84), (66, 80), (72, 84),
           (76, 92), (96, 90), (100, 78), (104, 74), (104, 58), (108, 54), (112, 46), (116, 54), (120, 58), (120, 74),
           (124, 78), (128, 90), (150, 88), (156, 82), (162, 88), (182, 90), (186, 84), (194, 84), (198, 92),
           (232, 92), (238, 86), (244, 86), (250, 94), (276, 96), (282, 90), (290, 90), (296, 98), (319, 98), (319, 112)]
    L.poly(sil, 0x00)
    for (x, y) in ((108, 62), (114, 62), (110, 68), (62, 86), (160, 92), (240, 90), (30, 96), (190, 88), (286, 94)):
        L.rect(x, y, x + 1, y + 1, 0x1C)
    for x in range(0, 320, 2):
        yy = 98 + int(2 * math.sin(x / 17.0)) + int(1.5 * math.sin(x / 7.0))
        L.rect(x, yy, x + 1, yy + 3 + (x // 2) % 2, 0x06)
    L.poly([(0, 112), (0, 106), (60, 102), (120, 105), (180, 104), (240, 107), (319, 104), (319, 112)], 0x00)
    L.poly([(30, 112), (40, 100), (60, 94), (96, 96), (110, 104), (116, 112)], 0x00)       # la roca de Radu
    E.paste(L.wide(), 0, 0)
    E.quantize()
    lines = [('TT_TOP', 'LA NOCHE DE LOS', 0), ('TT_FIRE', 'PULSA FIRE', 0), ('TT_D0', [('NORMAL', 1), ('  ', 0), ('HARDCORE', 3)], 0), ('TT_D1', [('NORMAL', 3), ('  ', 0), ('HARDCORE', 1)], 0),
             ('TT_AUT', '2026 - TONY C. WARE', 2), ('TT_BLK', '', 0), ('TT_REC', 'RÉCORD 000000', 2), ('TT_INV', 'INVENCIBLE', 1),
             ('TT_FIN1', 'LA NOCHE', 0), ('TT_FIN2', 'HA TERMINADO', 1),
             ('CR_1', 'STRIGOI MORT', 0), ('CR_2', 'ARIC, EL SASTRE', 0), ('CR_2B', 'DE LAS SOMBRAS', 0),
             ('CR_3', 'MUMA PADURII', 0), ('CR_4', 'EL CAPCAUN', 0), ('CR_5', 'EL REY STRIGOI', 0),
             ('CR_E1', 'ZOMBIS  CUERVOS', 2), ('CR_E2', 'VAVAMA  MURCIELAGOS', 2), ('CR_E3', 'IELE  GARGOLAS', 2),
             ('CR_E4', 'MOROI  VALVA BAII', 2), ('CR_E5', 'LUPARI  FATUOS', 2), ('CR_E6', 'CABALLEROS', 2),
             ('CR_T1', 'LOS JEFES', 1), ('CR_T2', 'LAS CRIATURAS', 1), ('CR_G', 'GRACIAS POR JUGAR', 1),
             ('CR_A1', 'UN JUEGO DE', 2), ('CR_A2', 'TONY C. WARE', 0), ('CR_A3', 'ATARI 8 BITS', 2), ('CR_A4', '2026', 1)]
    L = escribir('TIT', 'TI_', E, lines, {'RX': 30, 'RY': 94 + 40})
    open(os.path.join(HERE, '..', 'src', 'pantallas_ti.s'), 'w').write('\n'.join(L) + '\n')
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'pant_titulo.png'))

# ---------------------------------------------------------------- GAME OVER
def gameover():
    REDS = [0x48, 0x46, 0x44, 0x42, 0x42]
    B = []
    for r in range(21):
        if 8 <= r < 12: B.append([0x00, 0x20, REDS[r - 8], 0x4C, 0x42])
        elif 12 <= r < 16: B.append([0x00, 0x20, REDS[r - 12], 0x4C, 0x42])
        else: B.append([0x00, 0x04, 0x06, 0x08, 0x0C])
    E = Escena(B)
    L = Lienzo(160, 168)
    L.rect(96, 61, 224, 62, 0x04)                                       # el suelo donde bota
    for (x, y) in ((100, 58), (108, 56), (212, 57), (220, 59)):
        L.rect(x, y, x + 1, y, 0x06)
    E.paste(L.wide(), 0, 0)
    w1 = TT.palabra('GAME', gap=2, sx=2, sy=2); E.paste(w1, (160 - w1.shape[1]) // 2, 66)
    w2 = TT.palabra('OVER', gap=2, sx=2, sy=2); E.paste(w2, (160 - w2.shape[1]) // 2, 97)
    E.quantize()
    lines = [('GO_T1', 'HA GANADO', 0), ('GO_T2', 'LA NOCHE...', 0)]
    L = escribir('GOV', 'GO_', E, lines, {'FLOOR': 62}, rows=16)
    open(os.path.join(HERE, '..', 'src', 'pantallas_go.s'), 'w').write('\n'.join(L) + '\n')
    E.render(scale=3).save(os.path.join(HERE, '..', 'build', 'pant_go.png'))

titulo(); gameover(); print('ok')
