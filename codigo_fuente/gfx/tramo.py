"""Escritura de un tramo (superpuesto en $2200-$3FFF) para ca65.
Disposición fija: cielo (códigos 64-127 del juego A, 512 bytes) · juego B · juego C ·
mapa (13 páginas) · tabla TRT (768 bytes, ver strigoi.s)"""
import font

def bl(data, per=16):
    data = [int(x) & 255 for x in data]
    return '\n'.join('        .byte ' + ','.join('$%02X' % b for b in data[i:i + per]) for i in range(0, len(data), per))

def write_tramo(path, seg, sky512, csB, csC, MAP, SKY, MTN, BK, PF0, PF1, PF2, PF3,
                SPAWN, end, chk, nxt, flags, t1, t2, extra=(), mus=0):
    assert len(sky512) == 512 and len(MAP) == 13
    assert len(SPAWN) <= 32
    L = ['; generado · no editar a mano', '        .segment "%s"' % seg]
    L.append(bl(sky512)); L.append(bl(csB.data)); L.append(bl(csC.data))
    for r in range(13):
        assert len(MAP[r]) == 256
        L.append(bl(MAP[r]))
    T = []
    T += list(csB.cls)[:128]
    for r in range(4): T += list(SKY[r])[:40]
    for r in range(3): T += list(MTN[r])[:64]
    for tab in (BK, PF0, PF1, PF2, PF3):
        t = list(tab) + [0] * 22
        T += t[:22]
    sp = list(SPAWN)
    for k in range(4):
        col = [s[k] for s in sp] + [255 if k == 0 else 0] * (32 - len(sp))
        T += col
    T += [len(sp), end, chk, nxt, flags, mus]
    assert len(T) == 724, len(T)
    T += font.text(t1, 20, True, 0) + font.text(t2, 20, True, 2)
    T += list(extra)
    assert len(T) <= 768, len(T)
    T += [0] * (768 - len(T))
    L.append(bl(T))
    open(path, 'w').write('\n'.join(L) + '\n')
