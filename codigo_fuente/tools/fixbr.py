#!/usr/bin/env python3
"""Convierte saltos condicionales fuera de alcance (errores de ca65) en salto invertido + jmp.
Uso: fixbr.py fuente_principal.s ruta_cc65/bin   (arregla también los ficheros incluidos que den el error)"""
import re, subprocess, sys, collections
INV = {'beq': 'bne', 'bne': 'beq', 'bcc': 'bcs', 'bcs': 'bcc', 'bpl': 'bmi', 'bmi': 'bpl', 'bvc': 'bvs', 'bvs': 'bvc'}
src, cc = sys.argv[1], sys.argv[2]
for it in range(20):
    r = subprocess.run([cc + '/ca65', '-I', 'src', '-o', '/tmp/x.o', src], capture_output=True, text=True)
    errs = collections.defaultdict(set)
    for f, n in re.findall(r'(\S+\.s):(\d+): Error: Range error', r.stderr):
        errs[f].add(int(n))
    if not errs:
        print('ok tras', it, 'pasadas'); print(r.stderr[:2000]); break
    for f, lines in errs.items():
        L = open(f).read().split('\n')
        for n in sorted(lines, reverse=True):
            l = L[n - 1]
            m = re.match(r'^(\S*:)?(\s+)(b(?:eq|ne|cc|cs|pl|mi|vc|vs))\s+(\S+)(.*)$', l)
            if not m: print('no sé arreglar', f, n, l); sys.exit(1)
            lab, sp, op, tgt, rest = m.groups()
            L[n - 1] = (lab or '') + sp + INV[op] + ' *+5' + rest
            L.insert(n, '        jmp ' + tgt)
        open(f, 'w').write('\n'.join(L))
