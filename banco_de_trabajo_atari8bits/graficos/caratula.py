#!/usr/bin/env python3
"""Convierte gfx/caratula.png en gfx/caratula.bin: ANTIC E 160x192 (JANUS y el misil, de la carátula),
negro fijo + 3 colores por franja de 4 líneas. Se ejecuta una vez (tarda); gen.py solo lee el .bin."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import atpic
src = Image.open(os.path.join(HERE, '..', 'gfx', 'caratula.png')).convert('RGB')
W, H = src.size
# 160 píxeles x 1,6 = 256 unidades por 192: recorte de aspecto 1,33 centrado en JANUS y el misil que despega
crop = src.crop((250, 215, 850, 665))
crop = ImageEnhance.Color(crop).enhance(1.2)
crop = ImageEnhance.Contrast(crop).enhance(1.1)
canvas = crop.resize((160, 192), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 80, 2))
CAND = [0x04, 0x08, 0x0C, 0x0E, 0x82, 0x84, 0x86, 0x88, 0x96, 0x9A, 0x9C, 0x32, 0x34, 0x36, 0x38,
        0x24, 0x26, 0x28, 0x2A, 0x2C, 0x1C, 0x3A, 0x3C, 0x54, 0x56, 0x22, 0x42, 0x44, 0x46]
idx, pals = atpic.convert2(canvas, CAND, band=4, err=0.75)
idx = atpic.clean(idx)
out = bytearray(atpic.tobytes(idx))
for k in range(3):
    out += bytes(p[k] for p in pals)
open(os.path.join(HERE, '..', 'gfx', 'caratula.bin'), 'wb').write(out)
atpic.preview(idx, pals, 4, 2).save(os.path.join(HERE, '..', 'gfx', 'caratula_atari.png'))
print('caratula.bin: %d bytes' % len(out))
