#!/usr/bin/env python3
"""comprime los superpuestos, los coloca bajo el OS y escribe src/packs.inc + build/packs.bin.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from lz import pack, unpack
NAMES = ['ov_t0', 'ov_t1', 'ov_t2', 'ov_a1', 'ov_a2', 'ov_t3', 'ov_a3']
REG = [[0xC000, 0xD000], [0xD800, 0xFFFA]]
out = []; inc = []
for nm in NAMES:
    raw = open('build/%s.bin' % nm, 'rb').read()
    p = pack(raw); assert unpack(p) == raw
    for r in REG:
        if r[1] - r[0] >= len(p):
            a = r[0]; r[0] += len(p); break
    else:
        sys.exit('no cabe %s (%d bytes) bajo el OS' % (nm, len(p)))
    out.append({'name': nm, 'addr': a, 'raw': len(raw), 'size': len(p)})
    open('build/%s.lz' % nm, 'wb').write(p)
    print('%-6s %5d -> %5d  en $%04X' % (nm, len(raw), len(p), a))
print('libre bajo el OS: %d + %d bytes' % (REG[0][1] - REG[0][0], REG[1][1] - REG[1][0]))
json.dump(out, open('build/packs.json', 'w'))
open('src/packs.inc', 'w').write('PK_LO:  .byte %s\nPK_HI:  .byte %s\n' % (
    ','.join('$%02X' % (o['addr'] & 255) for o in out), ','.join('$%02X' % (o['addr'] >> 8) for o in out)))
