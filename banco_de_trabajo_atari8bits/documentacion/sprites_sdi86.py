"""SDI '86 · dibuja los sprites y caracteres elegidos (desde gfx/) para el atlas y el folleto."""
import sys
sys.path.insert(0, '/home/claude/sdi86/juego/gfx')
from PIL import Image
from pal import atari_rgb
import mar, sdi2, estacion as E, agente as A, janus as J, compuzoides as CZ
import propuestas_f2 as P2, propuestas_f3 as P3, propuestas_f4 as P4, propuestas_f5 as P5

def draw(rows, cols, name, z=6):
    h = len(rows); w = max(len(r) for r in rows)
    im = Image.new('RGB', (w * 2 * z, h * z), (0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in cols:
                rgb = atari_rgb(cols[c])
                for yy in range(z):
                    for xx in range(2 * z): im.putpixel((x * 2 * z + xx, y * z + yy), rgb)
    im.save('img/spr_%s.png' % name)
    return name

def c3(t): return {'1': t[0], '2': t[1], '3': t[2]}
G = {'1': 0x0A}
S = []
S.append(draw(mar.SUBMARINO, {'1': 0x0C}, 'narval'))
S.append(draw(mar.PATRULLERA, {'1': 0x06, '2': 0x0A, '3': 0x0E}, 'patrullera'))
S.append(draw(mar.DESTRUCTOR, {'1': 0x06, '2': 0x0A, '3': 0x0E}, 'destructor'))
S.append(draw(mar.AVION, {'1': 0x34, '2': 0x38, '3': 0x0E}, 'avion'))
S.append(draw(mar.MINA, {'1': 0x24}, 'mina'))
S.append(draw(sdi2.CENTINELA, c3(P2.CENTINELA['A'][2]), 'centinela'))
S.append(draw(sdi2.CAZADOR[1], c3(P2.CAZADOR['B'][2]), 'cazador'))
S.append(draw(sdi2.ARTILLERO[1], c3(P2.ARTILLERO['B'][2]), 'artillero'))
S.append(draw(sdi2.ICBM[::-1], c3(P2.ICBM['B'][2]), 'icbm'))
S.append(draw(sdi2.MIRV[::-1], {'1': 0x0C, '2': 0x44, '3': 0x1E}, 'mirv'))
S.append(draw(E.CUERPO, c3(P3.ESTACION['A'][2]), 'estacion', 3))
S.append(draw(E.ESCOLTA[0], {'1': P3.ESCOLTA['C'][2][0]}, 'escolta'))
S.append(draw(E.CANON, c3(P3.CANON['C'][2]), 'canon'))
S.append(draw(A.AGENTE, {'1': 0x2A, '2': 0xC6, '3': 0xC6}, 'agente'))
S.append(draw(A.AGENTE_PASO, {'1': 0x2A, '2': 0xC6, '3': 0xC6}, 'agente_paso'))
S.append(draw(A.AGENTE_PASO_B, {'1': 0x2A, '2': 0xC6, '3': 0xC6}, 'agente_paso_b'))
S.append(draw(A.AGENTE_ARRIBA, {'1': 0x2A, '2': 0xC6, '3': 0xC6}, 'agente_arriba'))
S.append(draw(A.AGENTE_AGACHADO, {'1': 0x2A, '2': 0xC6, '3': 0xC6}, 'agente_agachado'))
S.append(draw(A.SOLDADO[0], c3((0xC4, 0x2A, 0xC8)), 'soldado'))
S.append(draw(A.TIRADOR[0], c3((0xC4, 0x2A, 0xC8)), 'tirador'))
S.append(draw(A.TIRADOR[1], c3((0xC4, 0x2A, 0xC8)), 'tirador_rodilla'))
S.append(draw(A.BLINDADO[:12], c3((0xC4, 0x2A, 0xC8)), 'blindado'))
S.append(draw(A.DRON, c3((0x06, 0x2A, 0x46)), 'dron'))
S.append(draw(J.PARED, c3((0x04, 0x46, 0x1C)), 'pared_janus', 3))
S.append(draw(J.BOLA, {'1': 0x1E}, 'bola'))
S.append(draw(J.EMISOR, c3((0x08, 0x84, 0x46)), 'emisor'))
S.append(draw([a + b for a, b in zip(J.CORAZA, J.CORAZA_ROTA)], c3((0x08, 0x84, 0x0E)), 'coraza'))
MT = {'1': 0x04, '2': 0x0A, '3': 0x46}
S.append(draw(CZ.ANDROIDE[0], MT, 'androide'))
S.append(draw(CZ.TORRETA[1], MT, 'torreta'))
S.append(draw(CZ.TORRETA[0], MT, 'torreta_escondida'))
S.append(draw(CZ.ARANA[:12], MT, 'arana'))
S.append(draw(CZ.OJO, MT, 'ojo'))
S.append(draw(CZ.CONSOLA, MT, 'consola'))
S.append(draw(CZ.MURO * 2, MT, 'muro_base'))
print(len(S), 'sprites')
