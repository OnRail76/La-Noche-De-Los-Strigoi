#!/usr/bin/env python3
"""Arenas de los jefes de las fases 4 y 5 (a partir de los bocetos aprobados):
  AR4 el Căpcăun · AR5 el Rey Strigoi · AR6 la cabeza del Rey Strigoi
Cada una: fondo + jefe como bloque fijo de casillas, suelo de juego en las filas 18-20,
cajas de golpe (punto débil) y de cuerpo para jefe_gen.s. Salida: ../src/arenaN.s"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from arte import Escena, Lienzo
from arena1 import Juego, cell_of
import font
import jefe7_capcaun as J7, jefe5_rey as J5, jefe6_cabeza as J6

def bl(data, per=16):
    data = [int(x) & 255 for x in data]
    return '\n'.join('        .byte ' + ','.join('$%02X' % v for v in data[i:i + per]) for i in range(0, len(data), per))

def suelo(E, c0, c1, c2):
    F = np.full((24, 160), c1, dtype=np.int16)
    for y in range(24):
        for x in range(160):
            if y < 2: F[y, x] = c2
            elif (x % 4 == 0 and (y // 6) % 2 == 0) or y % 6 == 0: F[y, x] = c0
    E.base[144:168, :] = F

def hacer(n, seg, bands, fondo, jefe, alt, X0, Y0, blk, head, body, ax, ay, rx, textos, floor):
    """blk = (fila, col, ancho, alto) del bloque; head/body = (x0, x1, y0, y1) en píxeles/líneas de escena"""
    fb = font.font_bytes()
    def escena(con_jefe, version):
        E = Escena(bands()); fondo(E)
        if con_jefe: E.paste(version, X0, Y0)
        suelo(E, *floor); E.quantize(); return E
    EB = escena(False, None)
    EJ = escena(True, jefe)
    EA = escena(True, alt) if alt is not None else None
    R0, C0, W, H = blk
    sel = None
    for a in range(1, 8):
        for b in range(a + 2, 14):
            for c in range(b + 2, 20):
                JA = Juego('A', 64, base=bytes(fb[:512]) + bytes(512)); JP, JQ, JR = Juego('P'), Juego('Q'), Juego('R')
                JS = lambda r: JA if r < a else (JP if r < b else (JQ if r < c else JR))
                try:
                    for EE in [x for x in (EB, EJ, EA) if x is not None]:
                        for r in range(21):
                            for cx in range(40):
                                cb, inv = cell_of(EE.idx, r, cx); JS(r).code(cb)
                    sel = (a, b, c); break
                except AssertionError:
                    pass
            if sel: break
        if sel: break
    assert sel, 'arena %d: no cabe en cuatro juegos de caracteres' % n
    a, b, c = sel
    JA = Juego('A', 64, base=bytes(fb[:512]) + bytes(512)); JP, JQ, JR = Juego('P'), Juego('Q'), Juego('R')
    JS = lambda r: JA if r < a else (JP if r < b else (JQ if r < c else JR))
    def codes(EE, r0, c0, w, h):
        out = np.zeros((h, w), dtype=np.int32)
        for j in range(h):
            for i in range(w):
                cb, inv = cell_of(EE.idx, r0 + j, c0 + i)
                code = JS(r0 + j).code(cb)
                out[j, i] = code | (0x80 if inv and code else 0)
        return out
    BG = codes(EB, 0, 0, 40, 21)
    BJ = codes(EJ, R0, C0, W, H)
    BA = codes(EA, R0, C0, W, H) if EA is not None else None
    print('arena %d: juegos A 0-%d · P %d-%d · Q %d-%d · R %d-20 · A %d P %d Q %d R %d' % (
        n, a - 1, a, b - 1, b, c - 1, c, JA.next - 64, JP.next - 1, JQ.next - 1, JR.next - 1))
    B = bands()
    p = 'G%d_' % n
    # disposición: cielo de A ($2200) · P $2400 · Q $2800 · R $2C00 · bloques desde $3000 · tablas en $3900
    L = ['; generado por gfx/arena_gen.py · no editar a mano', '        .segment "%s"' % seg]
    L.append(bl(JA.data[512:])); L.append(bl(JP.data)); L.append(bl(JQ.data)); L.append(bl(JR.data))
    L += [p + 'BLK:'] + [bl(BJ[j], W) for j in range(H)]
    if BA is not None:
        L += [p + 'ALT:'] + [bl(BA[j], W) for j in range(H)]
    used = W * H * (2 if BA is not None else 1)
    assert used <= 0x900, 'arena %d: bloques demasiado grandes' % n
    L.append('        .res %d' % (0x900 - used))
    L.append(p + 'BG:')
    for r in range(21): L.append(bl(BG[r], 40))
    for nm, i in (('BK', 0), ('PF0', 1), ('PF1', 2), ('PF2', 3), ('PF3', 4)):
        L.append(p + nm + ':'); L.append(bl([(list(B[r]) + [0x0C] * 5)[i] for r in range(21)] + [0]))
    HUDS = ' PUNTOS 000000  RADU 3  ' + '■' * 16
    L += [p + 'HUDA:', bl(font.text(HUDS, 40), 20)]
    for k, (t, col) in enumerate(textos):
        L += [p + 'TV%d:' % (k + 1), bl(font.text(t, 20, True, col), 20)]
    for k, v in (('R', R0), ('C', C0), ('W', W), ('H', H), ('S1', a), ('S2', b), ('S3', c),
                 ('HL', head[0]), ('HR', head[1]), ('HT', head[2] + 40), ('HB', head[3] + 40),
                 ('BL', body[0]), ('BR', body[1]), ('BT', body[2] + 40), ('BB', body[3] + 40),
                 ('AX', ax), ('AY', ay + 40), ('RX', rx)):
        L.append('%s%s = %d' % (p, k, v))
    for n1, n2 in (('BG', 'ARENA_BG'), ('BK', 'AT_BK'), ('HUDA', 'HUDA'), ('TV1', 'T_V1')):
        L.append('        .assert %s%s = %s, error, "arena %d: %s"' % (p, n1, n2, n, n2))
    open(os.path.join(HERE, '..', 'src', 'arena%d.s' % n), 'w').write('\n'.join(L) + '\n')
    EP = escena(True, jefe)
    EP.render(scale=3).save(os.path.join(HERE, '..', 'build', 'arena%d_prev.png' % n))

def main():
    # --- el Căpcăun: ogro a la derecha, empalados al fondo; punto débil, la panza
    og = J7.ogro(); og.ascii(76, 32, J7.EYES, {'k': J7.K, 'b': J7.BO})
    hacer(4, 'AR4', J7.bands, J7.fondo, og.wide(), None, 0, 0, (0, 18, 22, 18),
          head=(88, 136, 84, 134), body=(100, 150, 20, 144), ax=104, ay=60, rx=8,
          textos=[('¡EL CĂPCĂUN'.replace('Ă', 'A'), 0), ('HA CAÍDO!', 1), ('Y AHORA...', 1), ('EL REY STRIGOI', 2)],
          floor=(0x00, 0x22, 0x24))
    # --- el Rey Strigoi alado: punto débil, el corazón incandescente
    ry = J5.rey(); ry.ascii(76, 27, J5.EYES, {'y': J5.HEART, 'k': J5.K}); ry.ascii(78, 40, J5.FANGS, {'w': J5.BONE})
    Y5 = 36
    def bands5():
        B0 = J5.bands(); k = (Y5 - 6) // 8
        return [B0[max(0, r - k)] if r < 17 else B0[r] for r in range(21)]
    hacer(5, 'AR5', bands5, J5.sala, ry.wide(), None, 0, Y5, (Y5 // 8, 4, 32, 18 - Y5 // 8),
          head=(68, 94, Y5 + 44, Y5 + 74), body=(70, 92, Y5 + 20, Y5 + 108), ax=80, ay=Y5 + 30, rx=8,
          textos=[('¡FASE 4 SUPERADA!', 0), ('EL REY STRIGOI', 1), ('HUYE AL CASTILLO', 1), ('BONIFICACIÓN 5000', 2)],
          floor=(0x90, 0x92, 0x94))
    # --- la cabeza gigante: punto débil, la boca (abierta solo a ratos)
    cab = J6.cabeza().wide()
    cerr = J6.cabeza()
    cerr.poly([(118, 116), (202, 116), (198, 150), (122, 150)], J6.S2)          # boca cerrada: labios
    cerr.line([(124, 132), (196, 132)], 2.0, J6.K)
    cerr = cerr.wide()
    hacer(6, 'AR6', J6.bands, J6.sala, cerr, cab, 0, 0, (0, 8, 24, 18),
          head=(58, 102, 112, 150), body=(40, 120, 0, 100), ax=80, ay=126, rx=8,
          textos=[('¡EL REY STRIGOI', 0), ('HA SIDO DESTRUIDO!', 1), ('SIGHIȘOARA'.replace('Ș', 'S'), 1), ('VUELVE A AMANECER', 2)],
          floor=(0x00, 0x52, 0x54))
    print('ok')

if __name__ == '__main__':
    main()
