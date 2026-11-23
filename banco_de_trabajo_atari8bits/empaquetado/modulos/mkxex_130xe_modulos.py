#!/usr/bin/env python3
"""XEX para 130XE: fuente, programa residente, cargador, comprobación de 128 KB y
los módulos en trozos que xcopy guarda en los bancos extendidos."""
import sys, struct, re, json
lbl = open('build/game.lbl').read()
def L(n): return int(re.search(r'al ([0-9A-F]+) \.%s\b' % n, lbl).group(1), 16)
def seg(a, d): return struct.pack('<HH', a, a + len(d) - 1) + d
x = b'\xff\xff' + seg(0x2000, open('build/font.bin', 'rb').read())
x += seg(0x9C00, open('build/ldr.bin', 'rb').read())
x += seg(0x02E2, struct.pack('<H', L('xcheck')))
J = json.load(open('build/modulos.json'))
for m in J['mods']:
    img = bytes.fromhex(m['img']); a = m['addr']
    for i in range(0, len(img), 0x1C00):
        part = img[i:i + 0x1C00]
        x += seg(0xA000, bytes([m['bank']]) + struct.pack('<HH', a + i, len(part)) + part)
        x += seg(0x02E2, struct.pack('<H', L('xcopy')))
main = open('build/main.bin', 'rb').read()
x += seg(0x4000, main)
for f in J['fixed']:                     # título y GAME OVER: bajo el OS durante la carga
    d = bytes.fromhex(f['data'])
    x += seg(0xA000, struct.pack('<HH', f['addr'], len(d)) + d)
    x += seg(0x02E2, struct.pack('<H', L('oscopy')))
x += seg(0x02E0, struct.pack('<H', L('start')))
open(sys.argv[1], 'wb').write(x)
print('xex 130XE: %d bytes · residente $4000-$%04X' % (len(x), 0x4000 + len(main) - 1))
