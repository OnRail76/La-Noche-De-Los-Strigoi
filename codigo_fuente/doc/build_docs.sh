#!/bin/sh
# Genera el folleto de instrucciones (A5) y el atlas (A4) en PDF con Chrome sin pantalla.
# Las imágenes están en img/ (capturas del juego, bocetos, borradores de jefes y arte de la preproducción).
set -e
cd "$(dirname "$0")"
python3 instrucciones.py Strigoi_Instrucciones.pdf
python3 atlas.py Strigoi_Atlas_y_Memoria.pdf
