#!/bin/sh
# La Noche de los Strigoi · construye los tres formatos y las versiones de prueba en dist/
#   dist/strigoi.atr          disco sin DOS (doble densidad), XL/XE de 64 KB
#   dist/strigoi.car          cartucho AtariMax 8 Mbit (CAR tipo 42), XL/XE de 64 KB
#   dist/Strigoi_130XE.xex    XEX para 130XE (128 KB)
#   dist/prueba/              invencible: disco y XEX que empiezan en cada fase
set -e
cd "$(dirname "$0")"
mkdir -p dist/prueba
DEFS="-D MEDIO=1" OUTNAME=strigoi ./build.sh > /dev/null && cp build/strigoi.atr dist/
DEFS="-D MEDIO=2" OUTNAME=strigoi ./build.sh > /dev/null && cp build/strigoi.car dist/
DEFS="-D PRUEBA=1 -D MEDIO=1" OUTNAME=prueba ./build.sh > /dev/null && cp build/prueba.atr dist/prueba/strigoi_PRUEBA.atr
for n in 2 3 4 5; do
  DEFS="-D PRUEBA=1 -D FASE${n}_TEST=1" OUTNAME=f$n ./build.sh > /dev/null
  cp build/f$n.xex dist/prueba/Strigoi_130XE_PRUEBA_fase$n.xex
done
DEFS="" OUTNAME=Strigoi_130XE ./build.sh > /dev/null && cp build/Strigoi_130XE.xex dist/
ls -l dist dist/prueba
