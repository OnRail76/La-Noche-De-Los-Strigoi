#!/usr/bin/env python3
"""XEX de un programa suelto: build/init.bin ($0600, INITAD) + main ($2000, RUNAD = etiqueta start).
Uso: mkxex.py main.bin programa.lbl salida.xex"""
import sys, struct, re
main, lblf, out = sys.argv[1:4]
init = open('build/init.bin', 'rb').read(); main = open(main, 'rb').read()
start = int(re.search(r'al ([0-9A-F]+) \.start\b', open(lblf).read()).group(1), 16)
def seg(addr, data): return struct.pack('<HH', addr, addr + len(data) - 1) + data
x = b'\xff\xff' + seg(0x0600, init) + seg(0x02E2, struct.pack('<H', 0x0600)) + seg(0x2000, main) + seg(0x02E0, struct.pack('<H', start))
open(out, 'wb').write(x)
print('xex %s: %d bytes, $2000-$%04X, arranque $%04X' % (out, len(x), 0x2000 + len(main) - 1, start))
