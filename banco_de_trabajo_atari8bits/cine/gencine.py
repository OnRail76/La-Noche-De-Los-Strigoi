#!/usr/bin/env python3
"""Datos de los programas de INTRO (V6CINE=1) y FINAL (V6CINE=2): imagen ANTIC E con colores por franja,
frases (modo 7, fuente del juego), créditos (modo 2) y lista de visualización. Escribe build/cine/cinedata.s"""
import sys, os, pickle
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
import font, atpic
CINE = int(os.environ.get('V6CINE', '1'))
OUT = os.path.join(ROOT, 'build', 'cine'); os.makedirs(OUT, exist_ok=True)
L = []
def emit(s): L.append(s)
def bl(data, lab=None, per=16):
    if lab: emit('%s:' % lab)
    for i in range(0, len(data), per): emit('    .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))

idx, pals = pickle.load(open(os.path.join(ROOT, 'pic', 'nave.pkl' if CINE == 1 else 'elara.pkl'), 'rb'))
BAND = 4
NB = 192 // BAND
pic = atpic.tobytes(idx)
open(os.path.join(OUT, 'pic.bin'), 'wb').write(pic)
pals = [list(p) + [0] * (4 - len(p)) for p in pals]
emit('NBANDS = %d' % NB)
# por franja: color del fondo (índice 0) y PF0..PF2 (índices 1..3)
bl([p[0] for p in pals], 'PALBK'); bl([p[1] for p in pals], 'PAL0'); bl([p[2] for p in pals], 'PAL1'); bl([p[3] for p in pals], 'PAL2')

def big(t):                     # modo 7: 20 columnas, colores por los 2 bits altos (PF0)
    return font.text(t, 20, center=True, color=0)
FR = {1: ['CUANDO CAYÓ EL CORAZÓN DE ACERO...', 'EL VACÍO TOMÓ SU LUGAR...', 'EL ALMA DEL UNIVERSO PIDE TU AYUDA...'],
      2: ['EL VACÍO DA PASO AL SILENCIO.', 'EL SILENCIO ES LA PAZ.', 'LA GALAXIA RECUPERA LA ESPERANZA.', 'FIN']}[CINE]
emit('NFRASES = %d' % len(FR))
for i, f in enumerate(FR):
    ls = font.split_lines(f, 20)
    assert len(ls) <= 2, f
    ls = ([''] + ls) if len(ls) == 1 else ls
    bl(list(big(ls[0])) + list(big(ls[1])), 'FRASE%d' % i)
emit('FRASES: .word ' + ','.join('FRASE%d' % i for i in range(len(FR))))
# créditos (solo el final)
CRED = [''] * 24 + ['VÓRTICE 6', 'CORAZÓN DEL VACÍO', '', 'UN EUROSHOOTER EN 8 BITS', 'DE', 'TONY C. WARE', '', '',
        'DIRIGIDO Y DISEÑADO POR', 'TONY C. WARE', '', 'GRÁFICOS · FASES · MÚSICA', 'TONY C. WARE', '',
        '',
        'PROTAGONISTA', 'LA COMANDANTE ELARA VOSS', 'A BORDO DEL VÓRTICE 6', '', '',
        'LOS GUARDIANES DEL VACÍO', '', 'FERRUM-9', 'EL COMPACTADOR SOBERANO', '', 'THALASSA',
        'LA MADRE DE LAS MAREAS', '', 'EL TRÍPTICO DE HADES', '', 'SATURNUS', 'EL OFICIANTE VACÍO', '',
        'EL CORAZÓN NULO', 'LEVIATÁN V RESUCITADO', '', '',
        'LA FEDERACIÓN EUROPEA GALÁCTICA', 'TE DA LAS GRACIAS', '', '', 'GRACIAS POR JUGAR', '', '',
        '2026 - TONY C. WARE', '', '', 'ASISTIDO POR GPT Y CLAUDE', '', '', '', '', '', '', '', '', '', '', '']
CRED = [c.replace('·', '-') for c in CRED]
emit('NCRED = %d' % len(CRED))
emit('    .align 64')
emit('CRED:')
for c in CRED: bl(list(font.text(c, 40, center=True)), per=20)
emit('CH_SPACE = %d' % font.CODE[' '])
emit('DIG0 = %d' % font.CODE['0'])
bl(list(font.text('PUNTUACIÓN FINAL', 40, center=True)), 'TXSCORE', per=20)
bl(list(font.text('PULSA FIRE', 40, center=True)), 'TXFIRE', per=20)
# fuente del juego (1 KB, alineada)
emit('    .align 1024')
bl(list(font.font_bytes()), 'FONT')
open(os.path.join(OUT, 'cinedata.s'), 'w').write('\n'.join(L) + '\n')
print('cine %d: %d franjas, %d frases, %d líneas de créditos' % (CINE, NB, len(FR), len(CRED)))
