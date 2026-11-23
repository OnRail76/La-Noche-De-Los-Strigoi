#!/usr/bin/env python3
"""Partida automática con run8: título -> FIRE -> anda a la derecha, salta y lanza.
Uso: prueba.py juego.xex cuadros cada_n salida/ [semilla]
Saca capturas PNG cada n cuadros y una tabla de variables (Radu, cámara, enemigos)."""
import sys, os, re, random, subprocess
xex, n, step, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
random.seed(seed)
os.makedirs(out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
lbl = {}
for l in open(os.path.join(HERE, '..', 'build', 'game.lbl')):
    m = re.match(r'al ([0-9A-F]+) \.(\w+)', l)
    if m: lbl[m.group(2)] = int(m.group(1), 16)
L = ['in 100 104 0 1 0']
f = 200
while f < n:
    d = random.choice((20, 30, 40, 60))
    r = random.random()
    j = 8
    if r < 0.15: j = 9          # salto a la derecha
    elif r < 0.22: j = 2        # agachado
    elif r < 0.27: j = 0
    trig = 1 if random.random() < 0.5 else 0
    # FIRE a golpes: pulsado 1 de cada 8 cuadros
    for k in range(f, min(n, f + d)):
        t = trig if (k % 8) < 2 else 0
        jj = j if not (j == 9 and k > f + 3) else 8
        L.append('in %d %d %d %d 0' % (k, k, jj, t))
    f += d
for k in range(step, n, step):
    L.append('shot %d %s/f%05d.raw' % (k, out, k))
    L.append('mem %d 9800 256 %s/h%05d.bin' % (k, out, k))
L.append('end %d' % n)
open(out + '/guion.txt', 'w').write('\n'.join(L) + '\n')
subprocess.run([os.path.join(HERE, 'run8'), xex, out + '/guion.txt'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
names = ['camx', 'rxl', 'rxh', 'ry', 'rst', 'rarmor', 'rinv', 'lives', 'chk', 'spi', 'bact']
arr = ['etyp', 'est', 'exl', 'ey', 'et']
for k in range(step, n, step):
    p = '%s/h%05d.bin' % (out, k)
    if not os.path.exists(p): continue
    d = open(p, 'rb').read()
    g = lambda nm: d[lbl[nm] - 0x9800]
    camx = g('camx') + 256 * d[lbl['camx'] - 0x9800 + 1]
    print('%5d cam=%3d rx=%4d ry=%3d st=%d arm=%d inv=%3d vid=%d chk=%d spi=%2d ' % (
        k, camx, g('rxl') + 256 * g('rxh'), g('ry'), g('rst'), g('rarmor'), g('rinv'), g('lives'), g('chk'), g('spi')) +
        ' '.join('%s=%s' % (a, list(d[lbl[a] - 0x9800:lbl[a] - 0x9800 + 2])) for a in arr))
subprocess.run(['python3', os.path.join(HERE, 'shot.py')] + sorted(
    os.path.join(out, x) for x in os.listdir(out) if x.endswith('.raw')))
