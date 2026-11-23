#!/bin/sh
# SDI '86 · genera los datos y ensambla los 6 programas (0 título · 1-5 operaciones);
# empaqueta el disco (.atr), el cartucho (.car) y un .xex suelto por operación.
# Además, la versión de prueba (invencible) de las operaciones y su disco, para las partidas automáticas.
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
mkdir -p build
python3 tools/musica.py
PROGS=${PROGS:-"0 1 2 3 4 5"}
for N in $PROGS; do
  python3 tools/gen.py $N > /dev/null
  if [ $N = 0 ]; then SRC=titulo; else SRC=fase$N; fi
  $CC65/ca65 -g -I src -o build/p$N.o -l build/p$N.lst src/$SRC.s
  $CC65/ld65 -C src/sdi.cfg -m build/p$N.map -Ln build/p$N.lbl -o build/p$N.bin build/p$N.o
  if [ $N != 0 ]; then
    python3 tools/mkxex.py build/p$N.bin build/p$N.lbl build/sdi86_operacion$N.xex
    $CC65/ca65 -g -D PRUEBA=1 -I src -o build/p${N}p.o src/$SRC.s
    $CC65/ld65 -C src/sdi.cfg -Ln build/p${N}p.lbl -o build/p${N}p.bin build/p${N}p.o
  fi
done
$CC65/ca65 -g -o build/boot.o src/boot.s
$CC65/ld65 -t none -Ln build/boot.lbl -o build/boot.bin build/boot.o
$CC65/ca65 -o build/cartldr.o src/cartldr.s
$CC65/ld65 -t none -o build/cartldr.bin build/cartldr.o
if [ -f build/p5.bin ]; then
  python3 tools/mkdisk.py build/sdi86.atr
  python3 tools/mkdisk.py build/sdi86_PRUEBA.atr p
  python3 tools/mkcart.py build/sdi86.car
  python3 tools/mkxe130.py build/SDI_130XE.xex
fi
