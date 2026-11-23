#!/usr/bin/env python3
"""Galería de jefes: cada uno en su arena, con Radu para la escala y el marcador con la barra de vida."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
from pal import atari_rgb
import font
import jefe1_mort, jefe2_aric, jefe3_muma, jefe5_rey, jefe6_cabeza, jefe7_capcaun, lobo

OUT = os.path.join(HERE, '..', 'capturas')
os.makedirs(OUT, exist_ok=True)
S = 3

RADU = """
..hhhh..
.hhhhhh.
.hhhhhh.
..ssss..
..sksk..
..ssss..
..kkks..
...ss...
.jjwwjj.
jjjwwjjj
jjjwwjjj
jjwwwwjj
sjjwwjjs
sjjwwjjs
.hhhhhh.
.jjwwjj.
..hh.hh.
..hh.hh.
..hh.hh.
..hh.hh.
..hh..hh
..hh..hh
.hhh..hhh
"""


def radu_sprites(x, feet):
    rows = [(r.strip() + '........')[:8] for r in RADU.strip('\n').split('\n')]
    y = feet - len(rows)
    a = [int(''.join('1' if c in 'hjk' else '0' for c in r), 2) for r in rows]
    b = [int(''.join('1' if c in 'ws' else '0' for c in r), 2) for r in rows]
    s = [int(''.join('1' if c == 's' else '0' for c in r), 2) for r in rows]
    return [(x, y, a, 0x24), (x, y, b, 0x0C), (x, y, s, 0x2C)]


def hud(name, vida=0.7):
    """línea de marcador en ANTIC 2 (fuente del juego) con la barra de vida del jefe"""
    fb = font.font_bytes()
    txt = (' ' + name).ljust(26)
    codes = font.text(txt, 26)
    img = Image.new('RGB', (320, 8), (0, 0, 0))
    px = img.load()
    for i, c in enumerate(codes):
        for y in range(8):
            bits = fb[c * 8 + y]
            for x in range(8):
                if (bits >> (7 - x)) & 1:
                    px[i * 8 + x, y] = atari_rgb(0x0C)
    d = ImageDraw.Draw(img)
    d.rectangle([212, 1, 312, 6], outline=atari_rgb(0x0C))
    d.rectangle([214, 3, 214 + int(96 * vida), 4], fill=atari_rgb(0x44))
    return img.resize((320 * S, 8 * S), Image.NEAREST)


def pantalla(E, name, radu_x, feet, vida):
    E.sprites = radu_sprites(radu_x, feet) + E.sprites
    E.quantize()
    body = E.render(scale=S)
    full = Image.new('RGB', (320 * S, (168 + 8 + 4) * S), (0, 0, 0))
    full.paste(hud(name, vida), (0, 2 * S))
    full.paste(body, (0, 12 * S))
    return full


def todas():
    out = []
    # 1 Strigoi Mort
    E = jefe1_mort.escena()
    out.append(('1_strigoi_mort', pantalla(E, 'STRIGOI MORT', 16, 144, 0.9)))
    # 1b el lobo (segunda forma)
    E = jefe1_mort.Escena(jefe1_mort.bands())
    for b in range(13, 18):
        E.bands[b] = [E.bands[b][0], 0x00, 0x06, 0x0A, 0x44]
    jefe1_mort.luna(E)
    for x0 in (8, 132):
        jefe1_mort.tumba(E, x0)
    E.paste(lobo.lobo().wide(), 66, 106)
    out.append(('1b_strigoi_mort_lobo', pantalla(E, 'STRIGOI MORT', 16, 144, 0.4)))
    # 2 Aric
    out.append(('2_aric', pantalla(jefe2_aric.escena(), 'ARIC, EL SASTRE', 16, 128, 0.8)))
    # 3 Muma
    out.append(('3_muma_padurii', pantalla(jefe3_muma.escena(), 'MUMA PADURII', 16, 136, 0.75)))
    # 4a Căpcăun, minijefe del paso de los Cárpatos
    out.append(('4a_capcaun', pantalla(jefe7_capcaun.escena(), 'EL CAPCAUN', 6, 144, 1.0)))
    # 4 Rey Strigoi (quimera alada)
    out.append(('4b_rey_strigoi', pantalla(jefe5_rey.escena(), 'EL REY STRIGOI', 4, 142, 1.0)))
    # 5 Rey Strigoi, segunda parte (cabeza gigante)
    out.append(('5_rey_strigoi_cabeza', pantalla(jefe6_cabeza.escena(), 'EL REY STRIGOI', 4, 166, 1.0)))
    return out


if __name__ == '__main__':
    shots = todas()
    for name, im in shots:
        im.save(os.path.join(OUT, 'jefe_%s.png' % name))
    w, h = shots[0][1].size
    tw, th = w * 2 // 3, h * 2 // 3
    G = Image.new('RGB', (tw * 2 + 12, th * 4 + 36), (24, 24, 24))
    for i, (name, im) in enumerate(shots):
        G.paste(im.resize((tw, th), Image.LANCZOS), ((i % 2) * (tw + 12), (i // 2) * (th + 12)))
    G.save(os.path.join(OUT, 'galeria_jefes.png'))
    print('ok', G.size)
