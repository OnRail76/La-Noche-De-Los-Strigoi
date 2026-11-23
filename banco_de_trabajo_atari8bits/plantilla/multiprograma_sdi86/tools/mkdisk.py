#!/usr/bin/env python3
"""Disco de doble densidad (ATR, 720 sectores de 256 bytes) con arranque propio (src/boot.s, del banco)
y los 6 programas: 0 título · 1-5 operaciones. Cada uno se carga desde $2000 y salta a su etiqueta start.
Uso: mkdisk.py salida.atr [sufijo]   (sufijo: p para la versión de prueba)"""
import struct, re, sys
suf = sys.argv[2] if len(sys.argv) > 2 else ''
progs = [('build/p0.bin', 'build/p0.lbl')] + [('build/p%d%s.bin' % (f, suf), 'build/p%d%s.lbl' % (f, suf)) for f in range(1, 6)]
boot = bytearray(open('build/boot.bin', 'rb').read())
assert len(boot) == 384
ptab = int(re.search(r'al ([0-9A-F]+) \.PTAB\b', open('build/boot.lbl').read()).group(1), 16) - 0x0700
sectors = {}
nxt = 4
for i, (b, l) in enumerate(progs):
    data = open(b, 'rb').read()
    start = int(re.search(r'al ([0-9A-F]+) \.start\b', open(l).read()).group(1), 16)
    n = (len(data) + 255) // 256
    data += bytes(n * 256 - len(data))
    for k in range(n): sectors[nxt + k] = data[k * 256:(k + 1) * 256]
    boot[ptab + 6 * i:ptab + 6 * i + 6] = struct.pack('<HHH', nxt, n, start)
    print('programa %d: %-14s sectores %3d-%3d (%d) arranque $%04X' % (i, b, nxt, nxt + n - 1, n, start))
    nxt += n
assert nxt <= 721, 'no cabe: %d sectores' % nxt
img = bytes(boot)
for s in range(4, 721): img += sectors.get(s, bytes(256))
par = len(img) // 16
hdr = struct.pack('<HHHB', 0x0296, par & 0xFFFF, 256, par >> 16) + bytes(9)
open(sys.argv[1], 'wb').write(hdr + img)
print('disco %s: %d de 717 sectores de datos usados' % (sys.argv[1], nxt - 4))
