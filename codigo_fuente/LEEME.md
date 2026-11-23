# La Noche de los Strigoi · código fuente

| Carpeta / fichero | Qué es |
|---|---|
| `src/` | Ensamblador ca65: `strigoi.s` (programa residente, incluye todo), módulos de fase (`jefe1-3.s`, `enemigos_*.s`, `fase4.s`, `fase5.s`), cargadores (`cargador.s`, `cargador_medio.s`), arranques de disco y cartucho, `motor/` (núcleo, PMG, música, sonido, marcador) y los datos generados (`tr_*.s`, `arena*.s`, `pantallas_*.s`, `spr2.s`, `musdata.s`) |
| `gfx/` | Generadores en Python: tramos (`fase1.py`, `escalera.py`, `ciudadela.py`, `minas.py`, `carpatos.py`, `castillo.py`), arenas y jefes, sprites (`spr2.py`), título y GAME OVER (`pantallas.py`), bocetos y borradores (incluido el Balaur descartado) |
| `tools/` | `musica.py` (los seis temas), `lz.py`, `modulos.py`, `mkxex.py`, `mkmedio.py`, `fixbr.py`; bots y arnés en C (`walk8.c`, `bot8-11.c`), `medir_dli.py`, `hoja_capturas.py` |
| `doc/` | Generadores del folleto y del atlas (`instrucciones.py`, `atlas.py`, `comun.py`), sus imágenes y el material de partida (guion y bibliografía) |
| `build.sh` | Una construcción: `DEFS` y `OUTNAME` eligen la variante |
| `build_all.sh` | Los tres formatos y las versiones de prueba en `dist/` |

## Variantes (`DEFS`)

| Definición | Efecto |
|---|---|
| *(nada)* | XEX para 130XE |
| `-D MEDIO=1` | Disco ATR |
| `-D MEDIO=2` | Cartucho CAR |
| `-D PRUEBA=1` | Radu invencible |
| `-D FASEn_TEST=1` | Empieza en la fase n (2-5) |
| `-D ARENA_TEST=1` | Empieza en el jefe de la fase |
| `-D MUS_TEST=n` | El título toca el tema n (0 fase A, 1 fase B, 2 jefes, 3 título, 4 final, 5 GAME OVER) |

Ejemplo: `DEFS="-D PRUEBA=1 -D FASE3_TEST=1" OUTNAME=prueba ./build.sh` deja `build/prueba.xex`.

## Herramientas

- cc65 2.19: `CC65=/ruta/a/cc65/bin ./build_all.sh`.
- Python 3 con Pillow.
- Bots y arnés: compilar contra libatari800, por ejemplo
  `gcc -O2 -o tools/walk8 tools/walk8.c -I atari800/src/libatari800 -I atari800/src atari800/src/libatari800.a -lm -lz -lpng`.
  `walk8 juego etiquetas cuadros carpeta [cada_n]`; variables `MACH=-xl`, `HC=1` (HARDCORE), `AUTOFIRE=1`, `NOIN=1`, `WAV=fichero.raw`.
