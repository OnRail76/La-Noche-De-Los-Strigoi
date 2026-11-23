#!/usr/bin/env python3
"""SDI '86 en un solo XEX para Atari 130XE (128 KB).
Los 6 programas se guardan al cargar en la memoria extendida (4 bancos de 16 KB) y en la RAM bajo
el SO; el cargador residente ($0700) los trae a $2000 igual que el disco o el cartucho.
Uso: mkxe130.py salida.xex [sufijo]   (sufijo: p = operaciones invencibles, para pruebas)"""
import struct, re, sys, subprocess
CC = '/home/claude/tools/cc65/bin'
def asm(name):
    subprocess.run([CC + '/ca65', '-g', '-o', 'build/%s.o' % name, 'src/%s.s' % name], check=True)
    subprocess.run([CC + '/ld65', '-t', 'none', '-Ln', 'build/%s.lbl' % name, '-o', 'build/%s.bin' % name, 'build/%s.o' % name], check=True)
    return bytearray(open('build/%s.bin' % name, 'rb').read())
store, ldr, move = asm('xestore'), asm('xeldr'), asm('xemove')
assert len(store) <= 0x100 and len(ldr) == 0x180
ptab = int(re.search(r'al ([0-9A-F]+) \.PTAB\b', open('build/xeldr.lbl').read()).group(1), 16) - 0x0700
def seg(addr, data): return struct.pack('<HH', addr, addr + len(data) - 1) + bytes(data)
def init(addr): return seg(0x02E2, struct.pack('<H', addr))
out = b'\xff\xff' + seg(0x0600, store) + init(0x0603)        # rutina de guardado y comprobación de 128 KB
v = 0
for i in range(6):
    suf = sys.argv[2] if len(sys.argv) > 2 and i > 0 else ''
    b, l = 'build/p%d%s.bin' % (i, suf), 'build/p%d%s.lbl' % (i, suf)
    data = open(b, 'rb').read()
    start = int(re.search(r'al ([0-9A-F]+) \.start\b', open(l).read()).group(1), 16)
    n = (len(data) + 255) // 256
    data += bytes(n * 256 - len(data))
    ldr[ptab + 6 * i:ptab + 6 * i + 6] = struct.pack('<HHH', v, n, start)
    print('programa %d: %-12s páginas virtuales %3d-%3d (%d) arranque $%04X' % (i, b, v, v + n - 1, n, start))
    for k in range(0, n, 32):                                 # trozos de hasta 8 KB en $2000
        m = min(32, n - k)
        out += seg(0x2000, data[k * 256:(k + m) * 256]) + seg(0x06F0, struct.pack('<HB', v + k, m)) + init(0x0600)
    v += n
assert v <= 256 + 56, 'no cabe: %d páginas' % v
out += seg(0x2000, move) + seg(0x2100, ldr) + seg(0x02E0, struct.pack('<H', 0x2000))
open(sys.argv[1], 'wb').write(out)
print('%s: %d bytes · %d páginas (%d en bancos, %d bajo el SO)' % (sys.argv[1], len(out), v, min(v, 256), max(0, v - 256)))
