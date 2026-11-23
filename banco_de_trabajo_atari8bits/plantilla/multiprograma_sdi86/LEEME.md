# Plantilla: juego en varios programas (SDI '86)

Un título hecho de un programa de título y N operaciones; cada una se carga en $2000 y tiene la RAM entera para ella.

- `src/blk.inc`: el bloque compartido en $0580 (firma, dificultad, modo, truco, fase, vuelta, puntos, vidas, cadena,
  vida extra, selección, récords) y el cargador residente en $0710 (`LOADER`, A = programa).
- `src/comun.s`: el armazón de juego de cada operación. La operación da `FASE`, `f_screen`, `f_start`, `f_frame`
  (llama a `phase_done` al cumplir), `f_render`, `f_vbi`, `f_status` y sus tablas `SX_*`. `comun.s` lleva la partida:
  bloque de entrada, vidas, mensajes, marcador, alarma de oleada, fase superada (fanfarria, bonus), el paso a la
  siguiente operación (ARCADE) o a la siguiente vuelta (suelta), GAME OVER y vuelta al título.
- `src/centinela.s`: la nave del jugador en un carril (fases 2 y 3 de SDI '86), reutilizable con `SHIPPOS`, `Y_SHIP`.
- `src/fase4.s`, `src/fase5.s`: dos ejemplos completos (arena de enemigos en caracteres; jefe de pared con cintas).
- `boot.s` / `cartboot.s` / `cartldr.s` + `mkdisk.py` / `mkcart.py`: disco sin DOS y cartucho AtariMax 8 Mbit.
- `build.sh`: genera datos, ensambla cada programa, su versión invencible (`-D PRUEBA=1`) y empaqueta.
