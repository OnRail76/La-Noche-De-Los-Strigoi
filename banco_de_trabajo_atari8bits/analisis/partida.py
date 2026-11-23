#!/usr/bin/env python3
"""Partida automática: FIRE en el título, luego zigzag con fuego continuo.
Uso: partida.py juego.xex cuadros cada_n salida/  -> capturas f#####.raw/png y volcados z#####.bin (ZP) h#####.bin ($8000-$8FFF)"""
import sys, subprocess, os
xex, n, step, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
L = ['in 130 134 0 1 0', 'in 200 204 0 1 0']   # FIRE: fuera la carátula; FIRE: ARCADE
f = 260
seq = [(8, 90), (8 + 1, 30), (4, 120), (4 + 2, 30), (8, 60), (0, 20), (4, 60), (1, 25), (2, 25)]
i = 0
while f < n:
    j, d = seq[i % len(seq)]; i += 1
    L.append('in %d %d %d 1 0' % (f, min(n, f + d - 1), j)); f += d
for k in range(step, n, step):
    L.append('shot %d %s/f%05d.raw' % (k, out, k))
    L.append('mem %d 0080 128 %s/z%05d.bin' % (k, out, k))
    L.append('mem %d 8000 4096 %s/h%05d.bin' % (k, out, k))   # variables de HIBSS (base $8000)
L.append('end %d' % n)
open(out + '/guion.txt', 'w').write('\n'.join(L) + '\n')
subprocess.run(['/home/claude/tools/run8', xex, out + '/guion.txt'], stderr=subprocess.DEVNULL)
