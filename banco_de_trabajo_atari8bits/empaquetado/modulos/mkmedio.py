#!/usr/bin/env python3
"""Disco (ATR doble densidad, 64 KB) o cartucho (AtariMax 8 Mbit, CAR tipo 42)
con el cargador de src/cargador_medio.s. Uso: mkmedio.py atr|car salida"""
import sys, struct, re, json, os, subprocess
kind, out = sys.argv[1], sys.argv[2]
CC65 = os.environ.get('CC65', '/home/claude/cc65/bin')
lbl = open('build/game.lbl').read()
def L(n): return int(re.search(r'al ([0-9A-F]+) \.%s\b' % n, lbl).group(1), 16)
def rec(a, d): return struct.pack('<HH', a, len(d)) + d
J = json.load(open('build/modulos.json'))
boot = rec(0x2000, open('build/font.bin', 'rb').read()) + rec(0x4000, open('build/main.bin', 'rb').read())
for f in J['fixed']:
    boot += rec(f['addr'], bytes.fromhex(f['data']))
boot += b'\0\0'
mods = [bytes.fromhex(m['img']) for m in J['mods']]
ldr = bytearray(open('build/ldr.bin', 'rb').read())
assert len(ldr) <= 0x300, 'cargador demasiado grande (%d)' % len(ldr)
def patch(name, val): ldr[L(name) - 0x9C00] = val
pad = lambda d, n: d + bytes(-len(d) % n)
if kind == 'atr':
    nld = (len(ldr) + 255) // 256
    sec = 4 + nld
    body = b''
    pos = []
    for d in [boot] + mods:
        pos.append(sec)
        d = pad(d, 256); body += d; sec += len(d) // 256
    patch('BOOT_A', pos[0] & 255); patch('BOOT_B', pos[0] >> 8)
    for i, p in enumerate(pos[1:]):
        patch('MOD_A', p & 255) if False else None
        ldr[L('MOD_A') - 0x9C00 + i] = p & 255; ldr[L('MOD_B') - 0x9C00 + i] = p >> 8
    subprocess.check_call([CC65 + '/ca65', '-g', '-o', 'build/arr_d.o', '-l', 'build/arr_d.lst', 'src/arranque_disco.s'])
    subprocess.check_call([CC65 + '/ld65', '-t', 'none', '-Ln', 'build/arr_d.lbl', '-o', 'build/arr_d.bin', 'build/arr_d.o'])
    bs = bytearray(open('build/arr_d.bin', 'rb').read()); assert len(bs) == 384
    al = open('build/arr_d.lbl').read()
    A = lambda n: int(re.search(r'al ([0-9A-F]+) \.%s\b' % n, al).group(1), 16) - 0x0700
    bs[A('nsec')] = nld
    bs[A('dbootv'):A('dbootv') + 2] = struct.pack('<H', L('dboot'))
    img = bytes(bs) + pad(bytes(ldr), 256) + body
    nsec = 3 + (len(img) - 384) // 256
    assert nsec <= 720, 'no cabe en el disco: %d sectores' % nsec
    img += bytes((720 - nsec) * 256)
    par = len(img) // 16
    hdr = struct.pack('<HHHB', 0x0296, par & 0xFFFF, 256, par >> 16) + bytes(9)
    open(out, 'wb').write(hdr + img)
    print('disco %s: %d de 720 sectores · cargador %d sectores · arranque en el %d' % (out, nsec, nld, pos[0]))
else:
    data = b''
    pos = []
    for d in [boot] + mods:
        pg = len(data) // 256
        pos.append((1 + pg // 32, 0xA0 + pg % 32))
        data += pad(d, 256)
    patch('BOOT_A', pos[0][0]); patch('BOOT_B', pos[0][1])
    for i, (b, p) in enumerate(pos[1:]):
        ldr[L('MOD_A') - 0x9C00 + i] = b; ldr[L('MOD_B') - 0x9C00 + i] = p
    open('build/ldr_cart.bin', 'wb').write(bytes(ldr))
    subprocess.check_call([CC65 + '/ca65', '-g', '-o', 'build/arr_c.o', 'src/arranque_cart.s'])
    subprocess.check_call([CC65 + '/ld65', '-t', 'none', '-Ln', 'build/arr_c.lbl', '-o', 'build/arr_c.bin', 'build/arr_c.o'])
    b0 = bytearray(open('build/arr_c.bin', 'rb').read()); assert len(b0) == 0x2000, len(b0)
    al = open('build/arr_c.lbl').read()
    cv = int(re.search(r'al ([0-9A-F]+) \.cbootv\b', al).group(1), 16) - 0xA000
    b0[cv:cv + 2] = struct.pack('<H', L('cboot'))
    nb = (len(data) + 0x1FFF) // 0x2000
    assert 1 + nb <= 127
    img = bytearray(b'\xff' * (128 * 0x2000))
    img[0:0x2000] = b0
    img[0x2000:0x2000 + len(data)] = data
    img[127 * 0x2000:] = b0
    chk = sum(img) & 0xFFFFFFFF
    open(out, 'wb').write(b'CART' + struct.pack('>II', 42, chk) + bytes(4) + img)
    print('cartucho %s: AtariMax 8 Mbit, %d bancos de datos + arranque' % (out, nb))
