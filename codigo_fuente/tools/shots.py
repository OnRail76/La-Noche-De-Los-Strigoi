#!/usr/bin/env python3
"""shots.py dir salida.png cuadro1 cuadro2 ... : hoja de capturas (2 columnas)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gfx'))
from pal import atari_rgb
from PIL import Image
P = [atari_rgb(i) for i in range(256)]
d, out, fr = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
ims = []
for k in fr:
    b = open('%s/f%05d.raw' % (d, k), 'rb').read()
    im = Image.new('RGB', (384, 240)); im.putdata([P[x] for x in b])
    ims.append(im.crop((32, 16, 352, 216)).resize((480, 300), Image.NEAREST))
cols = 2 if len(ims) > 1 else 1
rows = (len(ims) + cols - 1) // cols
sh = Image.new('RGB', (480 * cols, 300 * rows))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 480, (i // cols) * 300))
sh.save(out)
