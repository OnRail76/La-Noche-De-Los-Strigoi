#!/bin/sh
# ejemplo del motor: ensambla, enlaza y empaqueta build/ejemplo.xex
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
mkdir -p build src/motor
cp ../*.s src/motor/            # el motor del banco, siempre la versión actual
cp ../hw.inc src/
$CC65/ca65 -g -I src -o build/ejemplo.o src/ejemplo.s
$CC65/ld65 -C src/ejemplo.cfg -Ln build/game.lbl -o build/dummy build/ejemplo.o
python3 tools/mkxex.py build/ejemplo.xex
