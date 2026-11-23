"""SDI '86 · utilidades comunes del generador de datos (un fichero src/dataN.s por programa).

Un solo juego de caracteres de 1 KB por programa:
  códigos 0-63   fuente propia (ANTIC 2 marcador, ANTIC 6/7 pantallas)
  códigos 64-127 caracteres multicolor del escenario (ANTIC 4)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'gfx'))
import font

OUT = []
def emit(s=''): OUT.append(s)
def bl(data, per=16):
    data = list(data)
    for i in range(0, len(data), per):
        emit('        .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))

# --------------------------------------------------------------- caracteres ANTIC 4
GLYPHS = {}
GLIST = []
def cell_bytes(rows, cx):
    out = []
    for r in rows:
        b = 0
        for k in range(4):
            ch = r[cx * 4 + k] if cx * 4 + k < len(r) else '.'
            b |= {'.': 0, '1': 1, '2': 2, '3': 3}[ch] << (6 - 2 * k)
        out.append(b)
    return tuple(out)

def code_of(cb, force=False):
    if not any(cb) and not force: return 0
    if cb not in GLYPHS:
        GLYPHS[cb] = 64 + len(GLIST)
        GLIST.append(cb)
    return GLYPHS[cb]

def norm(rows, w, name):
    out = []
    for r in rows:
        if len(r) != w: print('aviso: %s fila de %d px (se ajusta a %d)' % (name, len(r), w))
        out.append((r + '.' * w)[:w])
    return out

def cut(rows, wchars, name):
    """lista de filas de códigos (cada 8 líneas = una fila de caracteres)"""
    rows = norm(rows, wchars * 4, name)
    while len(rows) % 8: rows.append('.' * (wchars * 4))
    res = []
    for ry in range(0, len(rows), 8):
        band = rows[ry:ry + 8]
        res.append([code_of(cell_bytes(band, cx)) for cx in range(wchars)])
    return res

def tile(rows, name, n=40):
    w = len(rows[0]) // 4
    one = cut(rows, w, name)[0]
    return [one[i % w] for i in range(n)]

def recolor(rows, m):
    return [''.join(m.get(c, c) for c in r) for r in rows]

def emit_charset():
    if len(GLIST) > 64:
        sys.exit('ERROR: %d caracteres de escenario (máximo 64)' % len(GLIST))
    print('caracteres de escenario: %d de 64' % len(GLIST))
    cs = bytearray(font.font_bytes()[:512]) + bytearray(512)
    for i, g in enumerate(GLIST):
        cs[512 + i * 8:512 + i * 8 + 8] = bytes(g)
    emit('CHARSET:')
    bl(cs)
    emit('NCH_ESCENARIO = %d' % len(GLIST))

# --------------------------------------------------------------- sprites
def spr(rows, x0=0, w=8, only=None):
    """un player: 8 píxeles desde x0; only = colores que cuentan (por defecto, todo lo que no es '.')"""
    out = []
    for r in rows:
        b = 0
        for k in range(min(8, w)):
            x = x0 + k
            if 0 <= x < len(r) and r[x] != '.' and (only is None or r[x] in only): b |= 0x80 >> k
        out.append(b)
    return out

def pad16(rows):
    return [('..' + r + '..')[:16] if len(r) == 12 else r for r in rows]

def bitmap(px, w, h):
    out = bytearray()
    for y in range(h):
        for x in range(0, w, 4):
            out.append((px[y][x] << 6) | (px[y][x + 1] << 4) | (px[y][x + 2] << 2) | px[y][x + 3])
    return out

# --------------------------------------------------------------- textos
T = font.text
def center(t, w): return T(t, w, center=True)
def put(line, col, txt):
    return line[:col] + txt + line[col + len(txt):]

HUD_TOP_S = '1UP 000000        HI 000000     VIDAS 3 '

def textos_juego(msgs, status):
    """marcador de arriba (común), línea de estado de la fase, mensajes y pantalla de GAME OVER"""
    assert len(HUD_TOP_S) == 40 and len(status) == 40, status
    emit('HUD_TOP_T:'); bl(T(HUD_TOP_S), 20)
    emit('HUD_BOT_T:'); bl(T(status), 20)
    emit('HUD_SC = 4')
    emit('HUD_HI = %d' % (HUD_TOP_S.index('HI ') + 3))
    emit('HUD_LV = %d' % (HUD_TOP_S.index('VIDAS ') + 6))
    emit('HUD_VU = %d' % (status.index('VUELTA ') + 7))
    msgs = msgs + [('MSG_VUELTA', 'NUEVA AMENAZA DETECTADA'), ('MSG_VIDA', 'VIDA EXTRA'),
                   ('MSG_BONUS', 'SIN BAJAS: BONUS 1000')]
    for name, s in msgs:
        assert len(s) <= 40, s
        emit('%s:' % name); bl(center(s, 40), 20)
    emit('MSG_L: .byte ' + ','.join('<%s' % n for n, _ in msgs))
    emit('MSG_H: .byte ' + ','.join('>%s' % n for n, _ in msgs))
    for i, (n, _) in enumerate(msgs): emit('M_%s = %d' % (n[4:], i))
    for name, s, col in (('T_GO', 'GAME OVER', 2), ('T_GO2', 'JANUS HA VENCIDO', 1),
                         ('T_PTS', 'PUNTOS 000000', 0), ('T_REC', 'RÉCORD 000000', 3)):
        emit('%s:' % name); bl(T(s, 20, center=True, color=col), 20)
    emit('T_PTS_D = %d' % ('PUNTOS 000000'.center(20).index('0')))
    emit('T_REC_D = %d' % ('RÉCORD 000000'.center(20).index('0')))
    constantes()

def constantes():
    emit('DIG0 = %d' % font.CODE['0'])
    emit('DIG0C0 = %d' % (font.CODE['0'] | (0 << 6)))
    emit('DIG0C3 = %d' % (font.CODE['0'] | (3 << 6)))
    emit('CH_SPACE = 0')

def write(n):
    p = os.path.join(HERE, '..', 'src', 'data%d.s' % n)
    open(p, 'w').write('; GENERADO por tools/gen.py %d · no tocar a mano\n' % n + '\n'.join(OUT) + '\n')
    print('src/data%d.s escrito' % n)
