# Motor común para Atari 8 bits

Sale de SDI '86 (fase 1, Mar Helado) y recoge lo que funcionó en Vórtice 5, Vórtice 6 y Zak Attack.
Son módulos de ca65 que se incluyen en el fuente del juego. Cada módulo declara sus propias
variables (página cero y `HIBSS`), así que un juego solo tiene que definir unas pocas constantes y tablas.

`ejemplo/` es un programa mínimo que usa todos los módulos. `./build.sh` lo compila y sirve para
comprobar el motor sin ningún juego encima.

## Módulos

| Fichero | Qué hace | El juego tiene que definir |
|---|---|---|
| `nucleo.s` | Arranque (`m_init`), VBI propia (`m_vbi`), espera de cuadro (`m_wait`, `m_waitn`), mando (`m_mando`), copia y relleno (`m_copy`, `m_fill`) | `vbi_juego` (se llama en cada VBI) |
| `pmg.s` | Sprites con doble búfer a resolución de una línea: `pm_init`, `pm_wait`, `pm_begin`, `pm_spr`, `pm_mis`, `pm_misp`, `pm_end` y `pm_vbi`. Cuenta los cuadros perdidos en `pm_lag`. | `PMA`, `PMB` (2 KB, alineados a 2 KB), `PMY0`, `PMN` |
| `dli.s` | DLI por tablas, una entrada por fila: `HSCROL`, `COLBK` y `PF0`–`PF2` | Rellenar `DTBK`, `DTPF0`–`DTPF2` y `DTHS`; poner `dlin = 0` en la VBI |
| `carril.s` | Carriles con scroll fino: franjas que se deslizan enteras (barcos, aviones, cintas, convoyes) | `NCAR`, `CAR_K`, `CAR_NROWS`, `CROW_DL`, `CROW_RL`, `CROW_RH`, `CROW_LANE`, `DLGAME` |
| `sonido.s` | Efectos POKEY con prioridad y caída de volumen: `sfx` (conserva X e Y), `snd_tick` (en la VBI), `snd_off` | Tablas `SX_CH`, `SX_F`, `SX_S`, `SX_V`, `SX_D`, `SX_C`, `SX_P`, `SX_K` |
| `musica.s` | Reproductor de 4 voces del banco: `mus_play` (A = tema), `mus_stop`, `mus_tick` (en la VBI, antes de los efectos). Un tema con bucle `None` suena una vez y deja `mplay = 0` | `MUSICA = 1` antes de incluir `nucleo.s`, y `src/musdata.s` generado por `audio/musica.py` (ejemplo completo: `audio/musica_sdi86.py`) |
| `marcador.s` | Puntos BCD de 6 cifras (`addsc`, que avisa de la vida extra), récord (`hiupd`), cifras en pantalla (`put6`, `putdec2`) | `EXTRA_STEP` |
| `pantalla.s` | Pantallas de texto ANTIC 6/7 desde un descriptor (`txt_build`, `txt_show`): título, GAME OVER, mensajes | `DLTEXT`, `TSCR` |
| `hw.inc` | Registros del hardware (incluye `HSCROL` y `SIZEP0`/`SIZEP1`) | — |

## El cuadro

```
loop:   jsr pm_wait       ; espera a que la VBI haya mostrado el cuadro anterior
        jsr m_mando
        ... lógica ...    ; mover, disparar, colisiones (car_move, car_col, sfx, addsc)
        jsr pm_begin      ; borra el búfer oculto (rb)
        ... dibujo ...    ; pm_spr / pm_mis y las tablas PHPx, PHMx, PSZM, PCPx en la entrada rb
        jsr car_freeze    ; posiciones de los carriles para ese búfer
        jsr pm_end        ; listo: lo muestra la siguiente VBI
        jmp loop

vbi_juego:                ; solo en la pantalla de juego
        jsr pm_vbi        ; PMBASE, posiciones, tamaños y colores del búfer mostrado
        jsr car_vbi       ; LMS de las filas de carril y car_hs (HSCROL de cada carril)
        lda #0
        sta dlin
        ... copiar car_hs a DTHS ...
```

La lógica va un cuadro por delante de la imagen. Al calibrar posiciones con capturas, hay que
comparar la captura con la memoria del cuadro anterior.

## Reglas que el motor da por hechas

- **ANTIC 4/5:** un píxel mide un reloj de color, igual que un player a anchura normal. A doble anchura,
  los sprites salen con píxeles el doble de anchos que el decorado.
- **Un solo juego de caracteres de 1 KB:** los códigos 0–63 son la fuente (ANTIC 2, 6 y 7) y los 64–127,
  los caracteres multicolor del escenario. Así no hace falta cambiar `CHBASE` entre el marcador y el campo.
- **Quinto player** (`GPRIOR = $11`): todos los misiles salen en `PF3`. Hay que dejar `COLOR3` fijo
  y no usar caracteres invertidos en ANTIC 4.
- **Carriles:** el anillo es de 64 columnas escritas dos veces (128 bytes alineados a 128); `car_put`
  escribe siempre las dos copias. Cuando un carril cambia de columna, el juego borra la columna que acaba
  de salir de la pantalla, y las unidades nacen en la zona oculta del otro lado.
- **`CAR_K`** depende de la display list (scroll horizontal activado = lectura ancha). Se mide una vez
  con una captura: con ANTIC 4 a anchura normal y HSCROL = 3 − (pos & 3), sale **13**.
- **HSCROL por fila:** la DLI lo escribe antes del `WSYNC`, es decir, en la última línea de la fila actual.
  Solo puede cambiar al salir de una fila **sin** scroll; las filas con scroll repiten el valor que ya tienen.
- La VBI usa solo sus temporales (`vt`), pone `ATRACT = 0` en cada cuadro y empieza con `cld`.
- **Música y efectos:** la música escribe los 4 canales y los efectos pisan el suyo mientras duran. Con `MUSICA = 1`,
  un canal de efectos libre no se calla, porque es del reproductor. En la pantalla de juego de SDI no suena música:
  los 4 canales son de los efectos.
