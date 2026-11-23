#!/usr/bin/env python3
"""Arena de MUMA PĂDURII (Fase 3) -> ../src/arena3.s
Galería de sal bajo las criptas: estalactitas, cristales, dos repisas de roca a la
izquierda (desde la alta, saltando, se alcanza la cabeza) y Muma a la derecha."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from arte import Escena, Lienzo
import jefe3_muma as JM3
from arena1 import Juego, cell_of
import font

OUT = os.path.join(HERE, '..', 'src', 'arena3.s')
K = 0x00
MO, MO2, SK, SL, YE, SALT, BKC = JM3.MO, JM3.MO2, JM3.SK, JM3.SL, JM3.YE, JM3.SALT, JM3.BKC
ROCK, ROCK2 = 0x04, 0x08
X0, Y0 = 84, 16
AC0, AR0 = X0 // 4, Y0 // 8
AW, AH = 19, 16
FLOOR_Y = 144
LOW = (16, 40, 120)           # roca baja: x0, x1, y (fila 15)
HIGH = (44, 76, 96)           # repisa alta (fila 12)
SPLIT = None                  # filas de cambio de juego (se buscan solas)


def bands():
    B = []
    for r in range(21):
        if r < 2:    B.append([BKC, K, MO, ROCK, YE])         # estalactitas
        elif r < 4:  B.append([BKC, K, MO, SK, YE])           # cristal del bastón, pelo
        elif r < 8:  B.append([BKC, K, MO, SK, YE])           # ojo y dientes (PF3 amarillo)
        elif r < 16: B.append([BKC, K, MO, SK, SL])           # brazos, cuerpo y repisas de roca con musgo
        elif r < 18: B.append([BKC, K, MO, MO2, 0x0E])        # raíces (PF3 cristal)
        else:        B.append([0x10, K, MO, ROCK2, 0x0E])     # suelo de sal
    return B


def cueva(E):
    L = Lienzo(160, 168)
    for (u, l, w) in ((10, 14, 8), (40, 10, 6), (70, 14, 8), (100, 9, 6), (130, 15, 8), (170, 10, 6)):
        L.poly([(u - w, 0), (u + w, 0), (u, l)], K)
        L.poly([(u - w + 2, 0), (u - 1, 0), (u - 1, l - 4)], ROCK)
    L.rect(0, 0, 319, 1, K)
    # repisas de roca
    for (a, b, y) in (LOW, HIGH):
        bot = FLOOR_Y - 1 if a == LOW[0] else y + 9
        L.rect(a * 2, y, b * 2 - 1, bot, K)
        L.rect(a * 2, y, b * 2 - 1, y + 1, MO)
        L.rect(a * 2 + 2, y + 2, b * 2 - 3, bot - 2, SK)
        for x in range(a * 2 + 6, b * 2 - 4, 10):
            L.rect(x, y + 4, x + 1, bot - 3, K)
    L.poly([(HIGH[0] * 2 + 10, HIGH[2] + 9), (HIGH[1] * 2 - 10, HIGH[2] + 9), (HIGH[0] * 2 + 34, HIGH[2] + 20)], K)
    E.paste(L.wide(), 0, 0)
    # suelo de sal: patrón que se repite cada casilla
    F = np.full((24, 160), MO, dtype=np.int16)
    for y in range(24):
        for x in range(160):
            if y < 2: F[y, x] = ROCK2
            elif y < 8 and (x % 4 == 1) and y % 3 == 0: F[y, x] = 0x0E
            elif y >= 8: F[y, x] = K if (x + y) % 4 == 0 else MO
    E.paste(F, 0, FLOOR_Y)


def main():
    fb = font.font_bytes()
    best = None
    E = Escena(bands()); cueva(E); E.quantize()
    EM = Escena(bands()); cueva(EM); EM.paste(JM3.build(), X0, Y0); EM.quantize()
    for a in range(2, 9):
        for b in range(a + 3, 17):
            JA = Juego('ARA', 64, base=bytes(fb[:512]) + bytes(512)); JP, JQ = Juego('ARP'), Juego('ARQ')
            JS = lambda r: JA if r < a else (JP if r < b else JQ)
            try:
                for EE in (E, EM):
                    for r in range(21):
                        for cx in range(40):
                            cb, inv = cell_of(EE.idx, r, cx); JS(r).code(cb)
                JQ.code(bytes([0] * 8))
                for i in range(6): JQ.code(bytes([i + 1] * 8))   # hueco para raíces
                best = (a, b); break
            except AssertionError:
                pass
        if best: break
    assert best, 'Muma no cabe en tres juegos de caracteres'
    a, b = best
    JA = Juego('ARA', 64, base=bytes(fb[:512]) + bytes(512)); JP, JQ = Juego('ARP'), Juego('ARQ')
    JS = lambda r: JA if r < a else (JP if r < b else JQ)
    def codes(EE, r0, c0, w, h):
        out = np.zeros((h, w), dtype=np.int32)
        for j in range(h):
            for i in range(w):
                cb, inv = cell_of(EE.idx, r0 + j, c0 + i)
                code = JS(r0 + j).code(cb)
                out[j, i] = code | (0x80 if inv and code else 0)
        return out
    BG = codes(E, 0, 0, 40, 21)
    M = codes(EM, AR0, AC0, AW, AH)
    # raíces espinosas (filas 16-17, PF3 = cristal claro / PF2 musgo)
    rt = bytes([0b00110000, 0b00110011, 0b11111100, 0b00111100, 0b00110000, 0b11111111, 0b00111100, 0b00111100])
    rb = bytes([0b00111100, 0b11111111, 0b00111100, 0b00111100, 0b11111111, 0b00111100, 0b00111100, 0b00111100])
    RT, RB = JQ.code(rt), JQ.code(rb)
    print('juegos: ARA filas 0-%d, ARP %d-%d, ARQ %d-20 · ARA %d ARP %d ARQ %d' % (a - 1, a, b - 1, b, JA.next - 64, JP.next - 1, JQ.next - 1))

    AMAP = np.zeros((13, 256), dtype=np.int32)
    AMAP[10:13, 0:40] = 1
    for (x0, x1, y) in (LOW, HIGH):
        AMAP[(y // 8) - 8, x0 // 4:(x1 + 3) // 4] = 1
        if y // 8 - 8 + 1 < 10:
            AMAP[(y // 8) - 8 + 1:10, x0 // 4:(x1 + 3) // 4] = 1        # la roca es maciza
    def bl(data, per=16):
        data = [int(x) & 255 for x in data]
        return '\n'.join('        .byte ' + ','.join('$%02X' % v for v in data[i:i + per]) for i in range(0, len(data), per))
    B = bands()
    L = ['; generado por gfx/arena3.py · no editar a mano', '        .segment "AR3"']
    L.append(bl(JA.data[512:])); L.append(bl(JP.data)); L.append(bl(JQ.data))
    for r in range(13): L.append(bl(AMAP[r]))
    L.append('ARENA_BG3:')
    for r in range(21): L.append(bl(BG[r], 40))
    for nm, i in (('AT_BK3', 0), ('AT_PF03', 1), ('AT_PF13', 2), ('AT_PF23', 3), ('AT_PF33', 4)):
        L.append(nm + ':'); L.append(bl([B[r][i] for r in range(21)] + [0]))
    HUDS = ' PUNTOS 000000  RADU 3  ' + '■' * 16
    L += ['HUDA3:', bl(font.text(HUDS, 40), 20)]
    for name, t, col in (('T_V13', '¡FASE 3 SUPERADA!', 0), ('T_V23', 'MUMA PĂDURII'.replace('Ă', 'A'), 1),
                         ('T_V33', 'HA CAÍDO', 1), ('T_V43', 'BONIFICACIÓN 5000', 2)):
        L += [name + ':', bl(font.text(t, 20, True, col), 20)]
    L += ['MUMA_BLK:'] + [bl(M[j], AW) for j in range(AH)]
    L.append('MUMA_C = %d' % AC0); L.append('MUMA_R = %d' % AR0)
    L.append('MUMA_W = %d' % AW); L.append('MUMA_H = %d' % AH)
    L.append('MUMA_X0 = %d' % X0); L.append('MUMA_Y0 = %d' % Y0)
    L.append('ROOT_T = $%02X' % (RT | 0x80)); L.append('ROOT_B = $%02X' % (RB | 0x80))
    L.append('A3_SPLIT1 = %d' % a); L.append('A3_SPLIT2 = %d' % b)
    for n1, n2 in (('ARENA_BG3', 'ARENA_BG'), ('AT_BK3', 'AT_BK'), ('HUDA3', 'HUDA'), ('T_V13', 'T_V1')):
        L.append('        .assert %s = %s, error, "arena3: %s"' % (n1, n2, n2))
    open(OUT, 'w').write('\n'.join(L) + '\n')
    EP = Escena(bands()); cueva(EP); EP.paste(JM3.build(), X0, Y0); EP.quantize()
    EP.render(scale=3).save(os.path.join(HERE, '..', 'build', 'arena3_prev.png'))
    print('ok')


if __name__ == '__main__':
    main()
