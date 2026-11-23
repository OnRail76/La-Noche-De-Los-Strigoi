#!/usr/bin/env python3
"""Módulos de fase para el XEX de 130XE.
Comprime los superpuestos (tramos y arenas), los reparte por módulos, les da sitio
bajo el OS (cada módulo empieza de cero) y coloca cada módulo en un banco extendido.
Escribe src/packs.inc, src/modtab.inc y build/modulos.json."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from lz import pack, unpack
PACKS = ['ov_t0', 'ov_t1', 'ov_t2', 'ov_a1', 'ov_a2', 'ov_t3', 'ov_a3', 'ov_t4', 'ov_a4', 'ov_a5', 'ov_t5', 'ov_a6', 'ov_ti', 'ov_go']
FIXED = ['ov_ti', 'ov_go']      # siempre bajo el OS (título y GAME OVER), desde FIXBASE
MODS = {1: ['ov_t0', 'ov_t1', 'ov_a1'], 2: ['ov_t2', 'ov_a2'], 3: ['ov_t3', 'ov_a3'],
        4: ['ov_t4', 'ov_a4', 'ov_a5'], 5: ['ov_t5', 'ov_a6']}
addr = {p: 0 for p in PACKS}
# paquetes fijos: al final de la RAM bajo el OS
fixed = []
FIXBASE = 0xFFFA
for p in reversed(FIXED):
    f = 'build/%s.bin' % p
    if os.path.exists(f) and os.path.getsize(f) >= 16:
        z = pack(open(f, 'rb').read())
        FIXBASE -= len(z); addr[p] = FIXBASE
        fixed.append({'addr': FIXBASE, 'data': z.hex(), 'name': p})
print('paquetes fijos desde $%04X' % FIXBASE)
data = {}
out = []
bank, off = 0, 0x4000
info = []
for m in sorted(MODS):
    code = open('build/mod%d.bin' % m, 'rb').read() if os.path.exists('build/mod%d.bin' % m) else b''
    assert len(code) <= 0xC00, 'módulo %d: código demasiado grande (%d)' % (m, len(code))
    recs = [(0x8C00, code)] if code else []
    reg = [[0xC000, 0xD000], [0xD800, FIXBASE]]
    for p in MODS[m]:
        f = 'build/%s.bin' % p
        if not os.path.exists(f) or os.path.getsize(f) < 16:
            continue
        raw = open(f, 'rb').read()
        z = pack(raw); assert unpack(z) == raw
        for r in reg:
            if r[1] - r[0] >= len(z):
                addr[p] = r[0]; r[0] += len(z); break
        else:
            sys.exit('módulo %d: %s no cabe bajo el OS' % (m, p))
        recs.append((addr[p], z))
        info.append('  %-6s %5d -> %5d  en $%04X' % (p, len(raw), len(z), addr[p]))
    img = b''.join(bytes([d & 255, d >> 8, len(x) & 255, len(x) >> 8]) + x for d, x in recs) + b'\0\0'
    if off + len(img) > 0x7FFF:
        bank, off = bank + 1, 0x4000
    assert bank < 4 and off + len(img) <= 0x7FFF, 'no caben los módulos en 64 KB extendidos'
    out.append({'mod': m, 'bank': bank, 'addr': off, 'img': img.hex()})
    print('módulo %d: código %5d · imagen %5d en banco %d $%04X · libre bajo el OS %d' % (
        m, len(code), len(img), bank, off, sum(r[1] - r[0] for r in reg)))
    off += len(img)
print('\n'.join(info))
json.dump({'mods': out, 'fixed': fixed}, open('build/modulos.json', 'w'))
open('src/packs.inc', 'w').write('PK_LO:  .byte %s\nPK_HI:  .byte %s\n' % (
    ','.join('$%02X' % (addr[p] & 255) for p in PACKS), ','.join('$%02X' % (addr[p] >> 8) for p in PACKS)))
open('src/modtab.inc', 'w').write('MOD_BANK: .byte %s\nMOD_LO:   .byte %s\nMOD_HI:   .byte %s\n' % (
    ','.join(str(o['bank']) for o in out), ','.join('$%02X' % (o['addr'] & 255) for o in out),
    ','.join('$%02X' % (o['addr'] >> 8) for o in out)))
