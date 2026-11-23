#!/usr/bin/env python3
"""Cartucho AtariMax 8 Mbit (CAR tipo 42, 1 MB) con el juego completo (del banco):
banco 0 (y 127) de arranque; programas 0 título · 1-5 operaciones en los bancos 1..n por páginas."""
import struct, re, sys, subprocess, os
progs = [('build/p%d.bin' % f, 'build/p%d.lbl' % f) for f in range(0, 6)]
ldr = bytearray(open('build/cartldr.bin', 'rb').read())
assert len(ldr) == 0x180
PTAB = 0x0840 - 0x0700
data = bytearray()
for i, (b, l) in enumerate(progs):
    d = open(b, 'rb').read()
    start = int(re.search(r'al ([0-9A-F]+) \.start\b', open(l).read()).group(1), 16)
    n = (len(d) + 255) // 256
    pg = len(data) // 256
    bank, ofs = 1 + pg // 32, pg % 32
    ldr[PTAB + 6 * i:PTAB + 6 * i + 6] = struct.pack('<BBHH', bank, ofs, n, start)
    data += d + bytes(n * 256 - len(d))
    print('programa %d: %-14s banco %2d página %2d, %3d páginas, arranque $%04X' % (i, b, bank, ofs, n, start))
open('build/cartldr.bin', 'wb').write(ldr)
CC65 = os.environ.get('CC65', '/home/claude/tools/cc65/bin')
subprocess.check_call([CC65 + '/ca65', '-o', 'build/cartboot.o', 'src/cartboot.s'])
subprocess.check_call([CC65 + '/ld65', '-t', 'none', '-o', 'build/cartboot.bin', 'build/cartboot.o'])
bank0 = open('build/cartboot.bin', 'rb').read()
assert len(bank0) == 0x2000, len(bank0)
nb = (len(data) + 0x1FFF) // 0x2000
assert 1 + nb <= 127
img = bytearray(b'\xff' * (128 * 0x2000))
img[0:0x2000] = bank0
img[0x2000:0x2000 + len(data)] = data
img[127 * 0x2000:] = bank0
chk = sum(img) & 0xFFFFFFFF
open(sys.argv[1], 'wb').write(b'CART' + struct.pack('>II', 42, chk) + bytes(4) + img)
print('cartucho %s: AtariMax 8 Mbit, %d bancos de datos + arranque' % (sys.argv[1], nb))
