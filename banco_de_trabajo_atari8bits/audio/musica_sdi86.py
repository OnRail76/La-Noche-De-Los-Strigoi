#!/usr/bin/env python3
"""SDI '86 · música POKEY (compositor del banco): instrumentos, tablas de afinación medidas y temas.
Genera src/musdata.s.  Canales: 0 synth principal · 1 bajo (distorsión C) · 2 batería · 3 eco/pad
(el 3 lo pisan los efectos y la sirena; el 2 lo pisan explosiones y muerte)."""
import math

CLK = 63921.0                       # reloj base NTSC de 64 kHz
NOMBRE = 'C C# D D# E F F# G G# A A# B'.split()

def midi(t):
    t = t.replace('b', '#') if False else t
    n, o = (t[:-1], int(t[-1]))
    return NOMBRE.index(n) + 12 * (o + 1)

def hz(m): return 440 * 2 ** ((m - 69) / 12)

# --- afinación (comprobada en el emulador midiendo los 256 valores de AUDF)
#   tono puro ($A): f = CLK / (2 (N+1))
#   distorsión C ($C): f = CLK / (15 (N+1)) cuando N no es múltiplo de 3 ni de 5 (si no, otro timbre)
BASE = 24                            # índice 0 de la tabla = C1 (MIDI 24)
NT = 80
def best(fn, ok):
    out = []
    for i in range(NT):
        f = hz(BASE + i)
        c = min(((abs(1200 * math.log2(fn(n) / f)), n) for n in range(256) if ok(n)))
        out.append(c)
    return out
PURA = best(lambda n: CLK / (2 * (n + 1)), lambda n: True)
ZUMB = best(lambda n: CLK / (15 * (n + 1)), lambda n: n % 3 and n % 5)

# --- instrumentos: ctl, tabla (0 puro, 1 zumbido, 2 fijo), N fijo, desliz por cuadro, envolvente, arpegio, vaivén
INS = {}
def ins(nombre, ctl, tab, env, arp=(0,), fix=0, sld=0, wob=0):
    INS[nombre] = dict(ctl=ctl, tab=tab, env=list(env), arp=list(arp), fix=fix, sld=sld & 255, wob=wob)
ins('pulso',   0xA0, 0, [11, 10, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 0])
ins('sierra',  0xA0, 0, [7, 9, 10, 10, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6], wob=1)
ins('acmen',   0xA0, 0, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], arp=(0, 3, 7))
ins('acmay',   0xA0, 0, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], arp=(0, 4, 7))
ins('bajo',    0xC0, 1, [14, 13, 11, 10, 9, 8, 7, 6, 5, 4, 0])
ins('bajolar', 0xC0, 1, [13, 13, 12, 12, 11, 11, 11, 10, 10, 10, 10, 9])
ins('bombo',   0xC0, 2, [15, 14, 12, 10, 8, 6, 4, 2, 0], fix=26, sld=9)
ins('caja',    0x80, 2, [14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], fix=10)
ins('charles', 0x80, 2, [7, 4, 2, 0], fix=1)
ins('abierto', 0x80, 2, [7, 6, 5, 4, 3, 3, 2, 2, 1, 0], fix=1)
ins('ecopul',  0xA0, 0, [5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0])
ins('ecosie',  0xA0, 0, [3, 4, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2], wob=1)
ins('padmen',  0xA0, 0, [2, 3, 4, 5, 5, 5, 5, 5, 4, 4, 4, 4], arp=(0, 3, 7, 12))
ins('padmay',  0xA0, 0, [2, 3, 4, 5, 5, 5, 5, 5, 4, 4, 4, 4], arp=(0, 4, 7, 12))
ins('campana', 0xA0, 0, [13, 10, 8, 7, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0], arp=(0, 19, 12, 24))
ins('coro',    0xA0, 0, [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 5], arp=(0, 12, 7, 12), wob=1)
ins('piano',   0xA0, 0, [12, 10, 9, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0])
ins('tom',     0xA0, 2, [13, 11, 9, 7, 6, 5, 4, 3, 2, 1, 0], fix=90, sld=6)
INAMES = list(INS)

# --- notación: compases de 16 semicorcheas; ficha = nota[:ranura] · '.' sigue · '-' calla
class Tema:
    def __init__(s, nombre, vel, ranuras):
        s.nombre, s.vel, s.ran = nombre, vel, ranuras     # ranuras: 4 canales x 4 instrumentos
        s.can = [[], [], [], []]
        s.bucle = 0
    def compas(s, c, txt):
        f = txt.split()
        assert len(f) == 16, (s.nombre, c, txt, len(f))
        s.can[c].append(f)
    def marca_bucle(s): s.bucle = len(s.can[0])

def cod(tema, c, tok):
    if tok == '.': return 0
    if tok == '-': return 1
    slot = 0
    if ':' in tok: tok, slot = tok.split(':'); slot = int(slot)
    if c == 2:                       # batería: letra = instrumento
        slot = 'KSHO'.index(tok); val = 2
    else:
        val = midi(tok) - BASE + 2
        assert 2 <= val < 64, tok
    return slot << 6 | val

# ---------------------------------------------------------------- utilidades de composición
def bajo_rueda(r, quinta, final=None):
    """bajo tecno rodando entre bombos: . r r r . r r r . r r r . r q r"""
    q = final or quinta
    return '. %s %s %s . %s %s %s . %s %s %s . %s %s %s' % (r, r, r, r, r, r, r, r, r, r, q, r)

def bateria(t):
    return {'main': 'K H O H S H O H K H O K S H O H',
            'fill': 'K H O H S H O H K S H S S S S S',
            'intro': 'K . H . K . H . K . H . K . H .',
            'hats': '. . H . . . O . . . H . . . O .',
            'medio': 'K . . . . . H . K . . . S . H .',
            'redob': 'S . S . S . S . S S S S S S S S',
            'duro': 'K H K H S H K H K H O K S H S S',
            'nada': '. . . . . . . . . . . . . . . .',
            'lento': 'K . . . . . H . S . . . . . H .',
            'lento2': 'K . . K . . H . S . . . K . H H',
            'rito': 'K . H . S . H . K K H . S . O .',
            'latido': 'K . K . . . H . K . K . . . H .',
            'latido2': 'K . K . S . H . K . K . S . H H',
            'carrera': 'K H K H S H K H K H K H S S S S'}[t]

def acordes(raiz, ran):
    return '%s:%d . %s:%d %s:%d . %s:%d . %s:%d %s:%d . %s:%d . %s:%d %s:%d . %s:%d' % ((raiz, ran) * 10)

def eco(tema, desde, hasta, retardo=3, mapa={0: 0, 1: 1}):
    """el canal 3 repite el canal 0 con 3 semicorcheas de retraso (eco de 'dotted eighth')"""
    plano = [t for comp in tema.can[0] for t in comp]
    for b in range(desde, hasta):
        fila = []
        for k in range(16):
            i = b * 16 + k - retardo
            t = plano[i] if i >= desde * 16 else '.'
            if t not in '.-':
                n, s = (t.split(':') + ['0'])[:2]
                t = '%s:%d' % (n, mapa.get(int(s), 0))
            fila.append(t)
        tema.can[3][b] = fila

# ================================================================ SDI '86 · Guerra Fría: marcha sintética
ins('metal',   0xA0, 0, [13, 12, 11, 11, 10, 10, 10, 10, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 7], wob=1)  # metal de banda, sostenido
ins('redo',    0x80, 2, [9, 6, 3, 1, 0], fix=9)                                                   # golpe de redoble (caja corta)
ins('cañon',   0xC0, 2, [15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], fix=40, sld=7)  # bombo de cañón
INAMES = list(INS)
V = '. . . . . . . . . . . . . . . .'
MARCHA = {'paso':  'K . H H S . H H K . H H S . S S',     # bombo en 1 y 3, caja en 2 y 4, redobles de relleno
          'paso2': 'K . H H S . H H K . K . S H S H',
          'redob': 'S H S H S H S H S S S S S S S S',
          'entra': 'K . . . . . . . K . . . K . K .',
          'golpe': 'K . . . S . . . K . . . S . . .'}

def con_slot(m, s):
    return ' '.join(t if t in '.-' else '%s:%d' % (t, s) for t in m.split())

# ---------------------------------------------------------------- TÍTULO · Do menor · 120 BPM
def titulo():
    T = Tema('TITULO', (7, 8), [['metal', 'pulso', 'acmen', 'acmay'],
                                ['bajo', 'bajolar', 'bajo', 'bajo'],
                                ['cañon', 'caja', 'redo', 'tom'],
                                ['padmen', 'padmay', 'ecopul', 'campana']])
    def c(lead, bajo, bat, pad=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, MARCHA.get(bat, bat)); T.compas(3, pad)
    # entrada: redoble y cañonazos sobre el pedal de Do
    c(V, 'C1 . . . . . . . C1 . . . C1 . C1 .', 'redob')
    c(V, 'C1 . . . . . . . G1 . . . G1 . G1 .', 'redob', 'C4:0 . . . . . . . . . . . . . . .')
    T.marca_bucle()
    A = [('G4 . . G4 C5 . . . . . . . D#5 . D5 .', 'C', 'm'),
         ('C5 . . . G4 . . . - . . . G4 . G4 .',   'C', 'm'),
         ('G#4 . . G#4 C5 . . . D#5 . . . G#5 . . .', 'G#', 'M'),
         ('G5 . . . . . . . F5 . D#5 . D5 . . .',  'G', 'M'),
         ('F4 . . F4 G#4 . . . C5 . . . F5 . . .', 'F', 'm'),
         ('D#5 . . . D5 . . . C5 . . . G4 . . .',  'C', 'm'),
         ('G#4 . . G#4 C5 . . . B4 . . . D5 . . .', 'G', 'M'),
         ('C5 . . . . . . . - . G4 . C5 . D5 .',   'C', 'm')]
    B = [('D#5 . . . D#5 . F5 . G5 . . . . . . .', 'D#', 'M'),
         ('F5 . . . D5 . . . A#4 . . . D5 . F5 .', 'A#', 'M'),
         ('G5 . . . G5 . G#5 . G5 . F5 . D#5 . . .', 'C', 'm'),
         ('D5 . . . . . . . B4 . . . G4 . . .',    'G', 'M'),
         ('C5 . . . C5 . D#5 . G#5 . . . . . . .', 'G#', 'M'),
         ('G5 . . . F5 . . . D#5 . . . C5 . . .',  'F', 'm'),
         ('B4 . . . D5 . . . F5 . . . G5 . . .',   'G', 'M'),
         ('C5 . . . . . . . - . . . . . . .',      'C', 'm')]
    def bajo(r):          # marcha: tónica en 1 y 3, quinta abajo en 2 y 4 (con octava)
        q = {'C': 'G1', 'G#': 'D#1', 'G': 'D2', 'F': 'C2', 'D#': 'A#1', 'A#': 'F1'}[r]
        r1 = r + ('2' if r in ('C', 'D#') else '1')
        return '%s . . . %s . . . %s . . . %s . %s .' % (r1, q, r1, q, q)
    def pad(r, k):
        n = r + ('4' if r in ('C', 'D#', 'D') else '3')
        return '%s:%d . . . . . . . . . . . . . . .' % (n, 0 if k == 'm' else 1)
    for frase, pie in ((A, 'paso'), (B, 'paso2'), (A, 'paso')):
        for i, (m, r, k) in enumerate(frase):
            bat = 'redob' if i == 7 else pie
            c(m, bajo(r), bat, pad(r, k))
    return T

# ---------------------------------------------------------------- FASE SUPERADA · fanfarria corta (no se repite)
def superada():
    T = Tema('SUPERADA', (5, 5), [['metal', 'pulso', 'acmen', 'acmay'],
                                  ['bajo', 'bajolar', 'bajo', 'bajo'],
                                  ['cañon', 'caja', 'redo', 'tom'],
                                  ['padmen', 'padmay', 'ecopul', 'campana']])
    def c(lead, bajo, bat, pad=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, MARCHA.get(bat, bat)); T.compas(3, pad)
    c('G4 . G4 G4 C5 . . . G4 . . . C5 . D#5 .', 'C2 . . . C2 . . . G1 . . . C2 . . .', 'S H S H K . . . S . . . K . S S',
      'C4:0 . . . . . . . . . . . . . . .')
    c('G5 . . . . . F5 D#5 F5 . . . . . G5 .', 'G#1 . . . . . . . A#1 . . . . . . .', 'K . . . S . . . K . . . S S S S',
      'G#3:1 . . . . . . . A#3:1 . . . . . . .')
    c('C6 . . . . . . . . . . . . . . -', 'C2 . . . C1 . . . . . . . . . . -', 'K . . . . . . . . . . . . . . .',
      'C4:1 . . . . . . . . . . . . . . -')
    T.bucle = None
    return T

# ---------------------------------------------------------------- GAME OVER · marcha fúnebre (no se repite)
def gameover():
    T = Tema('GAMEOVER', (9, 9), [['metal', 'pulso', 'acmen', 'acmay'],
                                  ['bajolar', 'bajo', 'bajo', 'bajo'],
                                  ['cañon', 'caja', 'redo', 'tom'],
                                  ['padmen', 'padmay', 'ecopul', 'campana']])
    def c(lead, bajo, bat, pad=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bat); T.compas(3, pad)
    c('C5 . . . . . . . B4 . . . . . . .', 'C1 . . . . . . . . . . . . . . .', 'K . . . S . H H K . . . S . H H',
      'C4:0 . . . . . . . . . . . . . . .')
    c('G#4 . . . . . . . G4 . . . F#4 . . .', 'G#1 . . . . . . . G1 . . . . . . .', 'K . . . S . H H K . . . S H S H',
      'G#3:1 . . . . . . . G3:1 . . . . . . .')
    c('G4 . . . . . . . C4 . . . . . . -', 'C1 . . . . . . . . . . . . . . -', 'K . . . . . . . K . . . . . . .',
      'C4:0 . . . . . . . . . . . . . . -')
    T.bucle = None
    return T

TEMAS = [titulo(), superada(), gameover()]       # números de tema: 0 título, 1 fase superada, 2 GAME OVER
# solo los instrumentos que se usan (las tablas de envolventes tienen que caber en 256 bytes)
INAMES = [k for k in INAMES if any(k in c for T in TEMAS for c in T.ran)]
# ---------------------------------------------------------------- salida
def main():
    L = ['; generado por tools/musica.py · no editar', '']
    pats, pid = [], {}
    temas = []
    for T in TEMAS:
        n = len(T.can[0])
        assert all(len(c) == n for c in T.can), T.nombre
        compases = []
        for b in range(n):
            fila = []
            for c in range(4):
                p = tuple(cod(T, c, t) for t in T.can[c][b])
                if p not in pid: pid[p] = len(pats); pats.append(p)
                fila.append(pid[p])
            compases.append(fila)
        temas.append((T, compases))
    assert len(pats) < 256
    # tablas de afinación (con hueco para arpegios)
    L.append('MUS_PURA: .byte ' + ','.join('$%02X' % n for c, n in PURA))
    L.append('MUS_ZUMB: .byte ' + ','.join('$%02X' % n for c, n in ZUMB))
    # instrumentos
    env, arp, eo, ao = [], [], [], []
    for k in INAMES:
        i = INS[k]; eo.append(len(env)); env += i['env']; ao.append(len(arp)); arp += i['arp']
    assert len(env) < 256 and len(arp) < 256
    def row(nm, vals): L.append('%s: .byte %s' % (nm, ','.join('$%02X' % v for v in vals)))
    row('MI_CTL', [INS[k]['ctl'] for k in INAMES])
    row('MI_TAB', [INS[k]['tab'] for k in INAMES])
    row('MI_FIX', [INS[k]['fix'] for k in INAMES])
    row('MI_SLD', [INS[k]['sld'] for k in INAMES])
    row('MI_ENV', eo)
    row('MI_ENVL', [len(INS[k]['env']) - 1 for k in INAMES])
    row('MI_ARP', ao)
    row('MI_ARPL', [len(INS[k]['arp']) for k in INAMES])
    row('MI_WOB', [INS[k]['wob'] for k in INAMES])
    row('MUS_ENVT', env)
    row('MUS_ARPT', arp)
    # patrones
    L.append('MUS_PATLO: .byte ' + ','.join('<MP%d' % i for i in range(len(pats))))
    L.append('MUS_PATHI: .byte ' + ','.join('>MP%d' % i for i in range(len(pats))))
    for i, p in enumerate(pats): L.append('MP%d: .byte %s' % (i, ','.join('$%02X' % v for v in p)))
    # temas
    for k, (T, comp) in enumerate(temas):
        L.append('MUS_T%d: .byte %s' % (k, ','.join('%d' % v for f in comp for v in f)))
        L.append('MUS_T%d_INS: .byte %s' % (k, ','.join('%d' % INAMES.index(x) for c in T.ran for x in c)))
    row('MUS_LEN', [len(c) for T, c in temas])
    row('MUS_LOOP', [255 if T.bucle is None else T.bucle for T, c in temas])     # 255 = una sola vez
    row('MUS_SPD0', [T.vel[0] - 1 for T, c in temas])
    row('MUS_SPD1', [T.vel[1] - 1 for T, c in temas])
    L.append('MUS_TLO: .byte ' + ','.join('<MUS_T%d' % k for k in range(len(temas))))
    L.append('MUS_THI: .byte ' + ','.join('>MUS_T%d' % k for k in range(len(temas))))
    L.append('MUS_ILO: .byte ' + ','.join('<MUS_T%d_INS' % k for k in range(len(temas))))
    L.append('MUS_IHI: .byte ' + ','.join('>MUS_T%d_INS' % k for k in range(len(temas))))
    L.append('MUS_BASE = %d' % BASE)
    open('src/musdata.s', 'w').write('\n'.join(L) + '\n')
    tam = len(pats) * 16 + sum(len(c) * 4 for T, c in temas) + 2 * NT + len(env) + len(arp)
    for T, c in temas:
        bpm = 3600 / (sum(T.vel) / 2 * 4) * 59.94 / 60
        print('%s: %d compases (bucle desde %s) · %.0f BPM · %.0f s' % (T.nombre, len(c), T.bucle, bpm, len(c) * 16 * sum(T.vel) / 2 / 59.94))
    print('patrones %d · datos de música ~%d bytes' % (len(pats), tam))
    # notas usadas y su desafinación
    usadas = {}
    for T in TEMAS:
        for c in (0, 1, 3):
            for comp in T.can[c]:
                for t in comp:
                    if t in '.-': continue
                    n = t.split(':')[0]; m = midi(n)
                    tab = ZUMB if c == 1 else PURA
                    usadas[(c == 1, n)] = round(tab[m - BASE][0])
    peor = sorted(((v, k) for k, v in usadas.items()), reverse=True)[:6]
    print('mayor desafinación (cents):', ', '.join('%s %s %d' % ('bajo' if b else 'synth', n, v) for v, (b, n) in peor))

if __name__ == '__main__':
    main()
