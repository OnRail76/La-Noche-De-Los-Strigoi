#!/usr/bin/env python3
"""SDI '86 · genera src/dataN.s para el programa N (0 título · 1-5 fases) desde gfx/.
Uso: gen.py N"""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gencomun as G
n = int(sys.argv[1])
importlib.import_module('gen%d' % n).build(G)
G.write(n)
