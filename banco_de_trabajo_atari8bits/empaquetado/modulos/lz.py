"""LZ para el Atari (ver src/carga.s):
   0 fin · $01-$7F literales · $80-$BF copia (c&$3F)+3, distancia 1 byte · $C0-$FF distancia 2 bytes"""
def pack(d):
    d = bytes(d); out = bytearray(); lit = bytearray(); i = 0; n = len(d); idx = {}
    def flush():
        nonlocal lit
        while lit:
            k = lit[:127]; out.append(len(k)); out.extend(k); lit = lit[127:]
    def add(k):
        if k + 3 <= n: idx.setdefault(d[k:k + 3], []).append(k)
    while i < n:
        best = 0; bo = 0
        if i + 3 <= n:
            for j in reversed(idx.get(d[i:i + 3], [])[-200:]):
                l = 0
                while i + l < n and l < 66 and d[j + l] == d[i + l]: l += 1
                o = i - j
                cost = 2 if o < 256 else 3
                if l > best or (l == best and o < 256 and bo >= 256):
                    best = l; bo = o
        need = 3 if bo < 256 else 4
        if best >= need:
            flush()
            if bo < 256: out += bytes([0x80 | (best - 3), bo])
            else: out += bytes([0xC0 | (best - 3), bo & 255, bo >> 8])
            for k in range(i, i + best): add(k)
            i += best
        else:
            add(i); lit.append(d[i]); i += 1
    flush(); out.append(0); return bytes(out)

def unpack(p):
    o = bytearray(); i = 0
    while True:
        c = p[i]; i += 1
        if c == 0: return bytes(o)
        if c < 0x80: o += p[i:i + c]; i += c
        else:
            l = (c & 0x3F) + 3; off = p[i]; i += 1
            if c & 0x40: off |= p[i] << 8; i += 1
            for _ in range(l): o.append(o[-off])
