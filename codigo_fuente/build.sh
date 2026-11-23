#!/bin/sh
# La Noche de los Strigoi: genera datos, ensambla (dos pasadas: la segunda con las
# direcciones de los paquetes comprimidos), enlaza y empaqueta
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/cc65/bin}
python3 gfx/fase1.py > /dev/null
python3 gfx/arena1.py > /dev/null
python3 gfx/spr2.py > /dev/null
[ -f gfx/escalera.py ] && python3 gfx/escalera.py > /dev/null
[ -f gfx/ciudadela.py ] && python3 gfx/ciudadela.py > /dev/null
[ -f gfx/arena2.py ] && python3 gfx/arena2.py > /dev/null
python3 gfx/minas.py > /dev/null
python3 gfx/arena3.py > /dev/null
python3 gfx/carpatos.py > /dev/null
python3 gfx/castillo.py > /dev/null
python3 gfx/arena_gen.py > /dev/null
python3 gfx/spr2.py > /dev/null
python3 gfx/pantallas.py > /dev/null
python3 tools/musica.py > /dev/null
[ -f src/packs.inc ] || printf "PK_LO: .res 12\nPK_HI: .res 12\n" > src/packs.inc; [ -f src/modtab.inc ] || printf "MOD_BANK: .res 5\nMOD_LO: .res 5\nMOD_HI: .res 5\n" > src/modtab.inc
for pass in 1 2; do
  $CC65/ca65 -g -I src $DEFS -o build/strigoi.o src/strigoi.s
  $CC65/ld65 -C src/strigoi.cfg -Ln build/game.lbl -m build/game.map -o build/dummy build/strigoi.o
  python3 tools/modulos.py > build/packs.txt
done
case "$DEFS" in
  *MEDIO=1*) python3 tools/mkmedio.py atr build/${OUTNAME:-strigoi}.atr ;;
  *MEDIO=2*) python3 tools/mkmedio.py car build/${OUTNAME:-strigoi}.car ;;
  *) python3 tools/mkxex.py build/${OUTNAME:-strigoi}.xex ;;
esac
