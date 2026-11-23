# Banco de trabajo · juegos para Atari 8 bits

Lo que se usó para hacer **Vórtice 5**, **Zak Attack**, **Boloncio**, **Vórtice 6**, **SDI '86** y **La Noche de los Strigoi** y sirve para el próximo título:
herramientas, el flujo de trabajo de principio a fin y las lecciones aprendidas por el camino.

| Carpeta | Qué hay |
|---|---|
| `motor/` | **Motor común** (sección 13): núcleo, PMG con doble búfer, DLI por tablas, carriles con scroll fino, sonido, marcador y pantallas de texto. `motor/ejemplo/` lo prueba solo |
| `plantilla/pantalla_mando/` | Carátula + pantalla de título con menú de SDI '86 (mapa, teletipo, DEFCON, récords) |
| `arnes/` | `run8.c`: el emulador sin pantalla con guiones (sección 3) |
| `plantilla/` | `hw.inc`, configuraciones de ld65 (`fases.cfg` es la de Vórtice 6), `build.sh`, `music.s` (reproductor de 4 voces) |
| `graficos/` | `canvas.py`, `pal.py`; `atpic.py` convierte ilustraciones a ANTIC E con 4 colores por franja |
| `audio/` | `musica.py` (compositor y empaquetador para `music.s`) y el análisis de temas de referencia |
| `cine/` | `cine.s` + `gencine.py`: intro y final (frases con fundido, ilustración con DLI, créditos con scroll fino) |
| `empaquetado/` | XEX, ATR sencillo, **disco multiprograma** (`boot_disco.s` + `mkdisk.py`) y **cartucho AtariMax 1 MB** (`cartldr.s`, `cartboot.s`, `mkcart.py`) |
| `analisis/` | capturas, bots, perfiles, `chkbul.py` (balas visibles), `partida.py` (partida automática con capturas y volcados), `fixbr.py` (saltos fuera de alcance, para cualquier fuente) |
| `documentacion/` | atlas y manuales; `atlas_html.py` + `atlas_pdf.py` es el Atlas final de Vórtice 6 (HTML → PDF con Chrome) |
| `conversion_cpc/` | herramientas del port de Boloncio |
| `empaquetado/modulos/` | **Módulos por fase de La Noche de los Strigoi** (sección 18): un mismo flujo de registros servido desde los bancos del 130XE (`cargador.s`), el disco o el cartucho (`cargador_medio.s`, `arranque_disco.s`, `arranque_cart.s`, `mkmedio.py`); compresor LZ (`lz.py` + `lz_unpack` en `carga.s`) y reparto bajo el SO (`modulos.py`) |
| `graficos/tramos/` | Generador de tramos con desplazamiento fino (`tramo.py`) y utilidades (`tramo_util.py`: celdas PF3 invertidas, `stamp`, hojas de control) |
| `jefes/` | Motor de jefes genérico por datos (`jefe_gen.s`, bloque de 32 bytes + lista de ataques), arena común (DLI, explosiones, escombros) y un módulo de ejemplo (`fase4.s`) |
| `motor/dli_por_filas_strigoi.s` | La DLI por filas segura en ANTIC 4 ancho (sección 18) |
| `arnes/walk8.c`, `arnes/bot11.c` | Bot que recorre tramos (máquina, dificultad, fuego automático, sonido por variables de entorno) y bot de jefe genérico |
| `analisis/strigoi/` | `medir_dli.py` (colores tardíos en la primera línea de cada fila) y `hoja_capturas.py` (hojas de contactos) |
| `documentacion/strigoi/` | Folleto A5 y atlas A4 de La Noche de los Strigoi (HTML → PDF con Chrome) |

## 1. Montar las herramientas (Linux, una vez)

| Herramienta | Para qué | Cómo |
|---|---|---|
| cc65 2.19 (ca65 + ld65) | Ensamblar y enlazar | `git clone https://github.com/cc65/cc65 && make -C cc65` → binarios en `cc65/bin` |
| atari800 (libatari800) | Emulador sin pantalla para pruebas automáticas | `git clone https://github.com/atari800/atari800 && cd atari800 && ./autogen.sh && ./configure --target=libatari800 --disable-netsio && make CFLAGS="-O2 -Wno-error"` (con GCC reciente `-Werror` para la compilación por un `ULONG` redefinido) |
| `run8` | El arnés de pruebas (este banco) | `gcc -O2 -I atari800/src/libatari800 -I atari800/src -o run8 arnes/run8.c atari800/src/libatari800.a -lm` |
| Python 3 + Pillow + numpy | Gráficos, generadores, análisis | `pip install pillow numpy scipy` |
| Playwright + Chromium | Documentación HTML → PDF | `pip install playwright && playwright install chromium` |
| ffmpeg | Grabar la banda sonora a MP3 | paquete del sistema |

Para jugar de verdad: Altirra (Windows) o atari800 con pantalla.

## 2. El flujo de trabajo

```
gfx/*.py  ──►  tools/gen.py  ──►  src/data.s  ──►  ca65/ld65  ──►  main.bin
(dibujos en texto)  (charsets, mapas,   (generado)                     │
                     oleadas, jefes,                      mkxex.py ───┼──► .xex
                     música, textos)                      mkpack.py ──┴──► .atr + .car
```

1. **Dibujar en texto.** Sprites, tiles, escenarios y jefes son cuadrículas de caracteres
   en Python (`graficos/canvas.py` da rectángulos, elipses, trazos y espejo; `graficos/pal.py`
   convierte códigos de color $HL a RGB NTSC). La misma fuente sirve al juego y a los documentos.
2. **Generar los datos.** Un script convierte los dibujos en charsets de 1 KB, metatiles,
   mapas, tablas de enemigos, jefes partidos en dos juegos de caracteres y música en tablas.
   Comprueba los límites (128 caracteres por juego, sprites por franja…) y avisa si algo no cabe.
3. **Ensamblar.** `build.sh` regenera, ensambla, enlaza y empaqueta los tres formatos.
4. **Probar sin manos** con `run8` (sección 3).
5. **Medir** velocidad, sprites ocultos y duplicados (sección 4).
6. **Documentar** con los generadores de `documentacion/` (sección 5).

## 3. El arnés `run8`

Ejecuta un .xex/.atr/.car en atari800 sin pantalla siguiendo un guion de texto:

```
in  F0 F1 joy trig start   # entre los cuadros F0 y F1: joy (1 arriba, 2 abajo, 4 izq., 8 der.; se suman), fuego 0/1, START 0/1
shot F nombre.raw          # captura de pantalla en el cuadro F (384×240, códigos de color)
mem  F 0080 128 z.bin      # volcado de memoria (dirección en hex, longitud en decimal)
end  F                     # último cuadro
```

- `WAV=salida.raw run8 juego.xex guion` graba el sonido (PCM 16 bits, 44.100 Hz, mono).
- `shot.py` convierte capturas a PNG; `memq.py` lee variables por nombre con el fichero de etiquetas.
- Con una versión invulnerable (`-D CHEAT=1`) un bot recorre el juego entero en un minuto de reloj.

## 4. Medir

| Script | Qué da |
|---|---|
| `fullrun.py` | Guion de partida completa: elige dificultad, juega en zigzag con fuego y vuelca memoria cada N cuadros |
| `allstats.sh` + `stats.py` | Por tramo (fase/jefe y sector): velocidad (vueltas de lógica por cuadro), balas, balas/disparos/sprites que se quedan sin dibujar, duplicados |
| `nodprof.sh` + `prof.py` | Coste en ciclos de cada rutina, con sondas `PROF n` (VCOUNT + cuadro) y DMA apagado |

Una vuelta de lógica que pasa de un cuadro tarda dos: el juego va al 50 % en ese momento.
Lo que importa es que casi todas las vueltas quepan en un cuadro, no la media.

## 5. Documentar

- `render_assets.py`: sprites, tiles, cráteres y jefes desde los mismos `gfx/*.py`, más recortes de capturas reales.
- `build_atlas.py` (A4 apaisado) y `build_manual.py` (A5) escriben HTML; `make_pdf.py` lo pasa a PDF.
- `common.py` reúne los textos compartidos (créditos, historia, lema, datos de sectores).

## 6. Lecciones aprendidas (Vórtice 5)

**Pantalla y DLI**
- Tablas DLI de más de 256 bytes con índice Y dan la vuelta: una tabla por campo (32 bytes), rutinas A/B con direccionamiento absoluto.
- Con VSCROL = 7 la primera línea mide un scanline y su DLI llega dentro de la anterior: deja una línea en blanco tras el marcador y carga la línea 0 en la VBI.
- Pon el bit de DLI solo en la línea anterior a una línea que cambia algo, con una máscara de cambios por línea. Un barrido desenrollado de la máscara vale más que ordenar listas.
- Doble búfer: dos display lists y dos juegos de tablas; la lógica prepara el cuadro siguiente y la VBI solo cambia punteros.
- La PMG de resolución de una línea deja libre $B000–$B2FF: buen sitio para tablas de trabajo.

**Sprites**
- Multiplexar P2/P3 por franjas y los 4 misiles como un solo recurso compartido entre disparos y balas.
- **Turnos**: lo que no cupo en un cuadro va primero en el siguiente. Así nada queda invisible dos cuadros seguidos; como mucho parpadea.
- Un sprite que no cambió (posición, gráfico, player) no se borra ni se repinta. Que cada objeto conserve su player.
- Recorre los objetos en el orden en que suelen estar ya (el reparto de huecos lo marca): la ordenación por inserción sale casi gratis.

**Rendimiento**
- VBI inmediata propia en juego (copiar sombras a mano) en vez de pasar por el SO.
- No toques los LMS si el scroll no se movió; cachea lo que solo cambia con el scroll.
- Colisiones contra listas compactas de lo que está vivo y en pantalla.
- Si un tramo sigue lento, a veces la solución es de diseño: espaciar las oleadas.

**Sonido**
- Lo que corre en la VBI necesita sus propios temporales de página cero.
- Nunca cortes en seco: bucles que cierran en el acorde que lleva al principio y fundido en cada cambio de pista.
- AUDCTL $78 (dos voces de 16 bits) para pantallas; $28 en juego (bajo de 16 bits, melodía de 8, efectos en su canal).

**Juego justo**
- Ninguna bala nace dentro de una zona alrededor de la nave; tope de balas según la dificultad.
- Una bala nueva no nace encima de otra igual; un enemigo que devuelve disparos, con enfriamiento.

**Formatos**
- ATR autoarrancable sin DOS: tope de 255 sectores (~32 KB); vigílalo.
- Cartucho AtariMax 128 KB: el banco 0 copia los demás a RAM y desconecta el cartucho.
- Desconecta el BASIC de los XL/XE (PORTB) si usas $A000–$BFFF.

## 7. Lista para el próximo título

1. Copia `plantilla/` (build.sh, vortice5.cfg, cart.s) y los empaquetadores.
2. Define paleta y reglas del hardware antes de dibujar (cuántos colores, sprites por franja, tamaño de jefes).
3. Dibuja en `gfx/` con `canvas.py`; haz que el generador compruebe los límites.
4. Haz una versión con `CHEAT` y `PROF` desde el primer día; mide en cada cambio grande.
5. Prueba los tres formatos al final de cada ronda.

## 8. Lecciones aprendidas (Zak Attack, run and gun con scroll horizontal)

**Pantalla**
- ANTIC 4 + HSCROL sobre un anillo de 64 columnas por fila (128 bytes, cada columna escrita dos veces): la ventana de 48 bytes nunca da la vuelta y basta tocar el byte bajo de 22 LMS en la VBI.
- HSCROL = 3 − (camx & 3); HPOS del píxel 0 del campo = 45 con este montaje.
- Fondo repetido cada 16 columnas + primer plano en tramos [fila, n, códigos]: 5 fases en ~8 KB.
- El generador comprueba que el fondo no use caracteres sólidos (en el tren, las colinas eran "suelo" invisible).
- Una DLI bajo el marcador cambia juego de caracteres y colores; otra en la última fila devuelve el borde a negro.
- Logotipo con juego de caracteres propio (41 celdas) y degradado por DLI línea a línea en el título.

**Errores que costaron**
- Otra vez el temporal compartido entre VBI y programa principal: la VBI usa SOLO sus variables (`vbt`). El síntoma fue fondo corrupto en la segunda vuelta.
- Una rutina de sonido que pisa X/Y dentro de un bucle de colisiones produjo puntuaciones BCD imposibles ("063<00"). `play_sfx` conserva X e Y.
- `cld` al principio de la VBI: puede llegar en medio de una suma BCD.
- Jefes: comprobar con números que el punto débil queda a la altura de los disparos (pies − 12 de pie, − 5 agachado, ~−60 saltando).

**Pruebas**
- `bot.py` + `runbot.sh`: corre, salta, se para a disparar y a veces se gira; con `-D CHEAT=1` los fosos lo devuelven arriba y no pierde vidas. Recorre las 5 fases en ~23 000 cuadros.
- `zp.py`: lee variables de página cero por nombre desde un volcado de `run8`.
- Contador `lagcnt` de cuadros perdidos: < 1 %, casi todo en cambios de fase.
- `atlas.py`: atlas gráfico desde los mismos datos del juego (pantallas simuladas), antes de programar nada.

**Segunda ronda (pruebas de Tony en atari800 de verdad)**
- Calibra la posición de los sprites contra el decorado desde el primer día: captura cruda, busca el color del sprite y el de un tile conocido y compara con las coordenadas del mundo. Aquí el sprite iba 9 color clocks a la derecha (Zak "se metía" en las cajas) y el campo visible empieza en camx + 12.
- Ninguna rutina devuelve intacto un puntero de página cero que no sea suyo: `aim_bullet` usaba `ptr3` y el bucle de torretas guardaba ahí su índice. Con el índice basura escribía fuera de las tablas: colores rotos (cielo rosa) y cuelgue.
- Aritmética con signo: `lsr` sobre un valor negativo lo convierte en uno enorme (el pescado aparecía abajo del todo). Usa `cmp #$80 / ror`.
- Recogibles: si no hay hueco de sprite, el evento espera; los enemigos se pierden, el pescado no.
- Enemigos de tierra con prueba de pared (`move_xw`): el soldado se para, el perro salta.
- Bot aleatorio (`randbot.py`) para buscar cuelgues: cuidado con los falsos positivos en pantallas de texto y GAME OVER.
- Música de marcha: batería en el canal de efectos (bombo con barrido de tono, caja y charles de ruido); un golpe de batería tapa el sonido del disparo, nunca una explosión o un golpe a Zak.

**Tercera ronda (puntería, dificultad, avisos)**
- Joystick de un botón y apuntar: "plantarse con FIRE" (FIRE desde quieto fija a Zak y la palanca apunta) conserva correr-saltar-disparar y añade diagonales en el suelo.
- Otra vez registros pisados: una rutina auxiliar (`scale_hp`) cambiaba Y en medio de un bucle que leía datos con (ptr),Y → todas las piezas del jefe mal colocadas. Toda rutina auxiliar guarda lo que toca.
- Los flancos de la palanca en una variable propia: `put_line` reutilizaba `tmp+2` y el menú cambiaba de dificultad solo.
- Inicializa explícitamente lo que vive en BSS (la dificultad salía con basura del cargador).
- Aviso de jefe genérico: la pieza que va a atacar invierte sus caracteres (bit 7) cada 4 cuadros y se restaura al terminar; proyectiles "en espera" (contador en el hueco del enemigo) para escombros y barridos.

## 9. Lecciones aprendidas (Boloncio, port desde Amstrad CPC)

**Origen**
- Un `.cpr` de GX4000 puede ser solo un BASIC de CPC metido en un disco ROM: mira el directorio AMSDOS
  antes de pensar en hardware Plus (`conversion_cpc/extract.py` + `detok.py`).
- Los decorados hechos con PRINT y salto de línea se reconstruyen fielmente simulando la pantalla del CPC
  (`rooms.py`); copiar a mano las cadenas largas lleva a errores.
- Leer los listados con lupa: errores de tecleo de revista (un token `LIST` colado en un LOCATE),
  variables que nunca se asignan (`OB$`), `+0.5` en variables enteras.

**Pantalla**
- MODE 0 del CPC (20 columnas de 8x8, 1 color por carácter) = ANTIC 6 casi uno a uno: 64 códigos y 4 colores
  (bits 6-7). El protagonista en PMG libera caracteres y le da color propio.
- Colores: tinta CPC (n = 9G + 3R + B, niveles 0/128/255) → código Atari más cercano en `pal.bin`.
- La colisión "leer el carácter de la pantalla" del BASIC se porta con una tabla de clase por código
  (libre, sólido, mortal, llave, pareja).

**Errores que costaron (cartucho)**
- Con la VBI del SO (no una propia), al desconectar el cartucho AtariMax el SO XL ve TRIG3 ≠ GINTLK
  y bloquea la máquina: copiar TRIG3 en GINTLK ($03FA) al arrancar.
- El cargador del cartucho copia sobre $2000-$9FFF y machaca la display list del SO con $FF (DLI en
  cada línea). Si se activa NMIEN=$C0 antes de poner una DL propia, las DLI se anidan y desbordan la pila.
  Activar la DLI solo con la DL del juego ya puesta; parar ANTIC (DMACTL=0) al empezar.
- Probar siempre los tres formatos: el .xex y el .atr iban bien y el .car no.

**Pruebas**
- Compilación BOT: el juego lee las acciones de una tabla generada por un BFS (`route.py`) en vez de
  la palanca; así no hay desfases entre el guion de `run8` y los pasos de la lógica. Con CHEAT y
  monstruos "atravesables" recorre las 8 salas, abre puertas y llega a la pantalla final sin manos.
- Compilación con `-D STARTROOM=n` para capturar cada sala directamente.

## 10. Lecciones aprendidas (Vórtice 6, visor de láminas desde un GDD)

**Herramientas**
- En una sesión nueva sin cc65 ni atari800: `git clone` de GitHub y compilar como en la sección 1 (unos 3 minutos). No hace falta escribir ensamblador ni emulador propios.

**Pantalla**
- Los textos de los marcadores (ANTIC 2 con LMS) también cuentan para el límite de 4 KB: un marcador que empezaba en $7FEC salió corrupto. El generador coloca filas *y* textos con la misma comprobación.
- Datos primero: los juegos de caracteres en $2000 quedan alineados a 1 KB sin relleno; el RUNAD y el salto del ATR se leen de la etiqueta `start` en `game.lbl` (`mkxex.py`, `mkatr.py`).
- PMG en $A000 y DL + tablas en $A800 con el BASIC desconectado por PORTB al arrancar (y en el segmento INIT del .xex).
- Escenario de 64 columnas + 48 repetidas por fila: scroll infinito, la VBI solo suma el desplazamiento grueso a 20 LMS. Filas iguales se comparten (151 filas únicas para 10 láminas).
- DLI con 15 tablas (una por campo) y dos rutas: ligera por fila (fondo + P2/P3) y completa en los cambios de zona (juego de caracteres, PF0-3, los 4 players). En la galería, los 4 players se multiplexan por bandas.

**Sprites**
- Nave de 12 píxeles y 3 colores con solo P0+P1: P1 desplazado 4 cc y PRIOR $21 (modo OR). Columnas 0-3 solo P0, 8-11 solo P1, 4-7 los tres colores.
- Cápsulas y balas de jefe como pareja P2+P3 en OR (cáscara + letra).

**Documentación**
- Atlas en PIL directamente (sin Playwright): páginas A4 apaisadas a 150 ppp → PDF con `save_all`. Capturas de `run8` + dibujos desde los mismos `gfx/*.py`.
- Cuando el GDD y la lámina se contradicen (armas, número de enemigos, PAL/NTSC), decidir con el usuario antes de dibujar y dejarlo escrito en el atlas.

## 11. Lecciones aprendidas (Vórtice 6, fase 1 jugable)

**Lo que pidió Tony al probar** (y es la norma para los shooters): balas siempre visibles, sin parpadeos, sin sprites cortados ni corruptos. Las torretas de decorado no compensan: mejor enemigos voladores.

- Multiplexar "a quien quepa" por fila da parpadeo. Lo correcto: franjas fijas con 2 huecos y objetos confinados a su franja; el generador de oleadas reparte entre la franja y su vecina, y lo que no cabe espera.
- El color de los misiles M2/M3 sale de COLPM2/COLPM3 de esa franja: en franjas sin enemigo hay que poner un color de bala vivo (si no, bala negra sobre fondo negro). Todos los enemigos con luminancia alta.
- Doble búfer de verdad también para la PMG: dos zonas de 2 KB (PMBASE en la VBI) y HPOS de P0/P1/M0-3 congelados por búfer. Los misiles se borran enteros y se repintan cada cuadro: adiós a las balas fantasma que dejaba "desactivar sin borrar".
- `lda (src,x)` NO es "(src) + x": indexa el puntero. Usado como contador de bucle copia basura (sprites "peinados"). Para copiar: `(src),y` con el destino en la misma Y.
- `tools/chkbul.py`: comprueba en las capturas crudas de `run8` que cada bala enemiga activa (según la memoria) tiene píxeles visibles en su sitio.
- `tools/fixbr.py`: convierte los saltos condicionales fuera de alcance que señala ca65 en salto invertido + jmp.

## 12. Lecciones aprendidas (Vórtice 6 completo: 5 fases, intro, final, disco y cartucho)

**Un programa por fase**
- Cuando el juego no cabe en 64 KB: un programa por fase (más intro y final), todos cargados en $2000 y con la misma interfaz.
  Cada uno monta solo su música, su jefe y el código de sus enemigos (`.if FASE = n`).
- Un **bloque compartido** en la página 5 ($0580) pasa la partida de un programa a otro: firma $56, dificultad, «encadenado»,
  puntos, vidas, láser, escudo, récord, truco y «arrancado desde el cargador».
- Un **cargador residente** en $0710 con interfaz fija (A = número de programa) sirve igual para el disco y el cartucho:
  los programas no saben de dónde vienen.
- **Error que costó:** al terminar el final, el bloque seguía marcado como «encadenado» y la fase 1 empezaba directamente con los puntos
  de la partida anterior. Quien termina la partida (final o GAME OVER) limpia `P_CHAIN` antes de volver al título.

**Disco multiprograma** (`boot_disco.s`, `mkdisk.py`)
- ATR de doble densidad (720 sectores de 256 bytes; los 3 primeros de 128). Arranque propio de 3 sectores en $0700, sin DOS.
- El cargador lee por el SIO del SO (SIOV) sector a sector y salta a la etiqueta `start` del programa, sacada de su `.lbl`.
- Antes de cargar: DMA y DLI fuera, vectores de VBI del SO de vuelta (SETVBV con SYSVBV/XITVBV) y POKEY en silencio.

**Cartucho AtariMax 8 Mbit** (`cartldr.s`, `cartboot.s`, `mkcart.py`)
- 128 bancos de 8 KB en $A000–$BFFF; $D500+n elige banco y $D580 desconecta. CAR tipo 42.
- El banco de arranque copia el mismo cargador a $0700; los datos van por páginas desde el banco 1.
- **NMIEN = 0 mientras se conecta o desconecta el cartucho**, y `TRIG3 → GINTLK` al terminar: si una VBI del SO XL ve TRIG3 ≠ GINTLK, cuelga la máquina.
- El tipo «viejo» arranca en el banco 127 y el «nuevo» en el 0: el banco de arranque va repetido en los dos.
- Con todo en RAM por debajo de $A000 se copia directamente con el cartucho conectado; si algo cargara en $A000–$BFFF haría falta un búfer en RAM baja.

**Intro y final** (`cine/`)
- Ilustración en ANTIC E (160 × 192) con 4 colores por franja de 4 líneas cambiados por DLI. La DLI va en la línea 2 de cada franja:
  `WSYNC`, prepara los registros, `WSYNC` y los escribe al empezar la franja siguiente. Hecha de una vez, los colores llegaban una línea tarde.
- La imagen se parte en dos LMS para no cruzar un límite de 4 KB ($5010 y $6000).
- `atpic.py`: convierte una carátula con un negro fijo + 3 colores por franja (o 4 libres) y Floyd–Steinberg en serpentina;
  penaliza cambiar de color entre franjas. Retocar a mano lo que importa (ojos, logotipos).
- La DLI con temporales propios (`d1`, `d2`): compartirlos con el fundido corrompía los colores.
- Destello sobre la ilustración: un jugador en resolución de una línea (PMBASE libre por encima del programa) y un efecto de sonido
  escrito en la VBI *después* del reproductor, en el canal 4, para que pise la música solo mientras suena.
- Créditos: ANTIC 2 con desplazamiento fino vertical, la DL se rehace por línea; que entren desde abajo con la pantalla vacía y sin que FIRE los salte.

**Música**
- `musica.py` compone por patrones e instrumentos (envolvente, arpegio, temblor, sonido fijo de batería) y genera `musdata.s`.
- Mide la afinación grabando con `WAV=` y elige la tonalidad de cada tema para que el bajo de 8 bits caiga en notas afinadas.
- Variables `V6FASE` (tema de fase + jefe) y `V6TEMAS` (temas sueltos, para grabar MP3).

**Pruebas**
- Para recorrer el juego entero encadenado: compilar con `-D FASTCLEAR` (el jefe cae al llegar a su arena) y `-D PRUEBA` (invencible)
  mediante un `ca65` envoltorio en `CC65=…`, sin tocar los scripts; luego reconstruir la versión normal.
- Partida automática de la intro al título en disco y en cartucho, comprobando el bloque compartido con `mem`.
- `run8 … -pal` para comprobar que arranca en PAL.
- Reconstruir desde una copia limpia del paquete de fuentes y comparar con `cmp`: el entregable debe salir idéntico byte a byte.

**Documentación: el Atlas final**
- HTML + CSS a A4 y PDF con Playwright usando el Chrome del sistema (`atlas_pdf.py`): fuentes OTF (Inter) que reportlab no carga.
- `atlas_title.py`: rótulos con la fuente del juego en degradado, como imágenes pixeladas.
- `atlas_sprites.py`: los sprites desde los mismos datos que el juego (letras a/b/c = P2, P3 y la mezcla en OR), con proporción de píxel NTSC (6 × 4).
- Capturas nuevas de la versión final con guiones de `run8` de las versiones `_PRUEBA`; repasar las hojas de contactos y elegir a mano.
- Comprobar la maqueta rasterizando el PDF (`pdftoppm`): títulos largos que se salen, imágenes que pisan el pie de página.

**Lo que pidió Tony** (norma para los siguientes)
- Créditos: «2026 - TONY C. WARE». En Vórtice 6, además: dirigido y diseñado, gráficos, fases y música por Tony; programa y asistencia, GPT y Claude.
- Nada de «prototipo» ni de sistema de vídeo en las pantallas de un juego terminado.
- Paquetes sin scripts de publicación.

## 13. El motor común (desde SDI '86)

A partir de SDI '86 los juegos no empiezan de cero: `motor/` reúne en módulos lo que se repetía en cada título.
Su `LEEME.md` explica qué hace cada módulo y qué tiene que definir el juego.

**Para empezar un juego nuevo**
1. Copia `motor/` en `src/motor/` y `hw.inc` en `src/`. En el fuente del juego, incluye primero los datos
   (el juego de caracteres en $2000, alineado) y después los módulos.
2. Define las constantes de memoria (`PMA`, `PMB`, `PMY0`, `PMN`, `DLGAME`, `DLTEXT`, `TSCR`), `vbi_juego`
   y las tablas de efectos (`SX_*`).
3. Usa el bucle de `motor/LEEME.md`: lógica, `pm_begin`, dibujo, `car_freeze` y `pm_end`.
4. `motor/ejemplo/build.sh` siempre debe compilar: si un cambio del motor lo rompe, el cambio no es genérico.

**Lo que se mejoró respecto a Vórtice y Zak**
- PMG: todo se redibuja en el búfer oculto cada cuadro (unos 6.000 ciclos con el borrado desenrollado). Así no hay
  balas fantasma ni sprites cortados, y no hace falta llevar la cuenta de lo que había dibujado.
- `pm_lag` cuenta los cuadros perdidos sin perfilador. En SDI '86, 6 en 7.200 cuadros, todos en cambios de oleada.
- `sfx` conserva X e Y y lleva la caída de volumen por efecto (`SX_K`): un sonar que suena 1 s sin código aparte.
- Carriles: un convoy entero se mueve con 3 bytes de LMS y un HSCROL por cuadro, sin dibujar nada.

## 14. Lecciones aprendidas (SDI '86, fase 1: Mar Helado)

**Pantalla**
- ANTIC 4 tiene 160 píxeles: **un píxel = un reloj de color**, como un player a anchura normal. Al principio el
  submarino y las minas iban a doble anchura y se veían el doble de bastos que los barcos.
- Carriles con scroll fino: `CAR_K = 13` con esta display list. Se mide con una captura y la memoria del cuadro
  anterior (la imagen va un cuadro por detrás de la lógica por el doble búfer).
- **Error que costó:** los desplazamientos de los LMS en la display list se escribieron a mano con la cuenta mal
  (3 + 3·fila + 1 en vez de 7 + 3·fila: faltaban las 3 líneas en blanco y el marcador). La VBI escribía el anillo en
  la fila anterior y los barcos salían una fila más arriba. Calcula los desplazamientos desde la plantilla de la DL.
- Un juego de caracteres de 1 KB compartido: fuente en 0–63 y escenario en 64–127. El marcador ANTIC 2 y las
  pantallas ANTIC 6/7 no necesitan otro `CHBASE`.
- Decorado que se repite cada pocos caracteres (estrellas, aurora) parece una valla. Mejor repartirlo al azar
  con semilla fija en el generador.

**Juego**
- La última unidad de una oleada acelera: se acabaron los tiempos muertos esperando al último barco.
- Las cargas de profundidad estallan cerca de la profundidad del submarino: obligan a moverse sin ser injustas.
- Al reaparecer, el submarino queda invulnerable 3 s, y se retiran las balas y las minas.

**Pruebas**
- `analisis/partida.py juego.xex cuadros cada_n salida/`: título, zigzag con fuego y capturas + volcados de página cero
  y de `HIBSS` cada N cuadros. Con la versión `_PRUEBA` (invencible) recorre oleadas y vueltas en un par de minutos.
- `fixbr.py` vale ya para cualquier fuente (antes buscaba `g1.s`).

**Sonido (segunda ronda de SDI '86)**
- Lo que pidió Tony: música marcial y sintética de Guerra Fría solo en el título, el GAME OVER y la fase superada;
  en juego, nada de música, todo sonido de recreativa y con contundencia.
- Contundencia en el POKEY: cada explosión son **dos efectos a la vez** (ruido en un canal y un golpe grave
  de distorsión C cayendo en otro), con volumen 15 y caída lenta (`SX_K`). La muerte, igual, pero más larga.
- El latido de la flota, como en las recreativas: 4 notas graves en distorsión C que bajan (N = 64, 73, 82, 86,
  ninguna múltiplo de 3 ni de 5, para que suene a nota). Va más deprisa cuantas menos unidades quedan.
- Alarma de oleada: dos efectos cortos alternados cada 8 cuadros; no hace falta código de sirena aparte.
- Temas de una vez (`bucle = None` en el compositor → `MUS_LOOP = 255`): el reproductor se para solo y el GAME OVER
  espera a que acabe la marcha (`mplay = 0`) antes de volver al título.
- Comprobar sin oír: grabar con `WAV=`, sacar la nota dominante cada 0,25 s con una FFT y compararla con la partitura.
  Para un efecto concreto, volcar `SFRQ`/`SDUR` de su canal cuadro a cuadro con `mem`.
- El compositor solo exporta los instrumentos que usan los temas: con todos, las envolventes pasaban de 256 bytes.

## 15. Lecciones aprendidas (SDI '86: carátula, pantalla de mando, modos)

**Memoria**
- Programa, datos y variables en $2000-$9FFF (el segmento `HIBSS` se enlaza detrás del código, sin ocupar fichero).
  La RAM de $A000-$BFFF se usa **por turnos**: la carátula al encender, la pantalla de mando en el título y la
  partida en juego. Cada pantalla reconstruye lo suyo al entrar.
- **Error que costó:** la display list del juego se copiaba una sola vez al arrancar; la carátula la machacaba y la
  partida salía en basura. Toda pantalla copia su display list al entrar.
- Un bitmap ANTIC E que cruza un límite de 4 KB necesita otro LMS en la línea que empieza en el límite: se elige la
  dirección de inicio para que ese límite caiga en un principio de línea ($A830 + 50 x 40 = $B000).

**DLI**
- Las líneas ANTIC E miden un solo scanline. Con una DLI por línea que hace WSYNC, la siguiente NMI llega antes de
  acabar y las DLI se anidan: los colores salían desplazados un bloque entero. Para un degradado línea a línea,
  **una sola DLI** (en la línea anterior) que recorre las líneas con WSYNC.
- `DLI_N` (motor/dli.s): el juego puede pedir más entradas que las 32 de serie.

**Datos y textos**
- Las líneas de texto ANTIC 2 deben medir **40 exactos**: una de 41 escribe su último carácter en la línea siguiente.
  El generador lo comprueba con `assert`. Con el teletipo pasa igual: prompt + mensaje + cursor = 40 como mucho.
- La fuente gana `%` y `>`. Un carácter que no existe sale como `?`.

**Juego**
- **Error que costó:** al hundir los barcos en el agua, la fila de abajo del carril dejó de estar vacía (carácter de agua
  en lugar de 0). El torpedo daba por tocado un barco que ya no estaba (dueño viejo) y sumaba puntos basura
  ("010703"). Ahora el agua cuenta como vacío, el dueño se comprueba (`UT` libre = nada) y al escaparse una unidad
  sus columnas se quedan sin dueño.
- El canal de un efecto que debe oírse siempre (el sonar) no lo comparten efectos frecuentes de la misma prioridad.

**Pruebas**
- `partida.py` sabe saltar la carátula y empezar desde el menú. Ahora vuelca $8000-$8FFF, donde están las variables.
- `fixbr.py` arregla también los ficheros incluidos (`mando.s`), no solo el fuente principal.
- Comprobar un efecto en la grabación: FFT por ventanas y buscar su frecuencia (el sonar, $2C en tono puro = 710 Hz).

## 16. Lecciones aprendidas (SDI '86 completo: 6 programas, ARCADE encadenado, disco y cartucho)

**Estructura** (plantilla en `plantilla/multiprograma_sdi86/`)
- Título y cada operación son programas aparte, todos en $2000. Pasan la partida por un bloque fijo ($0580) y saltan
  al cargador residente. Cada operación cabe con holgura (40 páginas) y tiene $A000-$BFFF para pantallas y PMG.
- `comun.s` hace de armazón: cada operación solo escribe su pantalla, su lógica y su dibujo. Con eso, las fases 4 y 5
  salieron en una sesión cada una.
- `-D RAPIDA=1` (cada operación se supera sola al cabo de 256 cuadros) prueba la cadena 1 → 5 → 1 completa en
  segundos. `-D PRUEBA=1` deja al jugador invencible para ver las fases enteras con un bot tonto.

**Errores que costaron**
- **Truco frente al menú:** el truco abajo, abajo, FIRE era también "elegir la operación 2 y empezar". El menú se
  comía la selección y parecía que la carga fallaba. Ahora solo cuentan los abajo que no mueven el cursor (ya está
  al fondo). Regla: un truco nunca debe ser una secuencia de navegación válida.
- **Memoria sucia al cargar:** una operación suelta en XEX arranca con la RAM a cero, pero cargada desde el título
  hereda lo que este dejó. Las columnas que la fase no rellenaba salían con basura. Cada pantalla borra **todo** lo
  que muestra, y el armazón deja en blanco los marcadores antes de encender la pantalla.
- **Variables temporales compartidas:** `ene_erase` / `ene_free` pisaban `tmp+2` y `tmp+3` mientras el paso del
  enemigo los usaba como distancia al agente, y los enemigos se quedaban quietos. Lo que tiene que sobrevivir a una
  llamada va en variables propias. Las rutinas que se llaman desde dentro de otro bucle con índice guardado (`cur`)
  guardan el suyo aparte (`bcur`).
- **Aparecer encima de un sólido:** el agente aparecía dentro de la caja central, no podía moverse y sus disparos
  morían al salir. Hay que comprobar el punto de aparición contra el mapa.
- **Etiquetas del arranque:** `ld65 -Ln` solo exporta las etiquetas si el fuente se ensambla con `-g`. Sin eso,
  `mkdisk.py` no encontraba `PTAB`.

**Diseño**
- Enemigos de caracteres que andan de casilla en casilla (como en Arena 3000): caben 10 en pantalla sin gastar
  players. El disparo busca el carácter bajo el misil y, por el rango de códigos, sabe si es pared, enemigo o dron.
- Jefe de pared: la pared en ANTIC E (40 líneas, 1.600 bytes) con una sola DLI. Las cintas y los emisores van en
  ANTIC 4 debajo. Girar una cinta de 36 casillas cada pocos cuadros (paso grueso) basta y se puede agujerear.
- Al morir en la arena, los enemigos en pantalla vuelven a la cola de las puertas. Así no te matan otra vez nada
  más reaparecer.

**Tras la primera prueba de Tony**
- **Sprites de cara al jugador:** un sprite que cae (el ICBM) va con el morro hacia donde se mueve. En el generador
  basta con `rows[::-1]`. Un enemigo de caracteres que dispara necesita su versión mirando a cada lado (`rev`).
- **Disparo en carrera:** si el disparo apenas es más rápido que el personaje, al andar y disparar parece que
  "rebota" pegado a él. Hay que hacerlo al menos 3 o 4 veces más rápido que el paso.
- **Un jefe con un único punto débil pequeño frustra.** La protección (la cinta) es el reto; donde no hay
  protección, todo el casco recibe daño.
- **Al destruir algo, que no siga nada suyo.** Si se vacía la pantalla pero no el array del que se redibuja, la
  rutina de giro vuelve a pintar la cinta. Una vez destruido, el estado se queda congelado (boom = 1) hasta el cambio
  de fase.
- **Más players que cabezas:** la tercera cabeza MIRV va en un player de los cazadores que esté libre, y ese hueco no
  se usa para picar mientras la cabeza viva.
- Para probar: `-D VUELTA0=n` y `-D OLEADA0=n` empiezan donde se quiere ver. `run8 mem` toma la dirección en
  **hexadecimal**.
- **El fin de un jefe no debe soltar el estado:** tras `phase_done` hay 255 cuadros de fanfarria en los que la fase
  sigue corriendo. Si el contador de explosión vuelve a 0, todo lo que dependía de él (giro de cintas, disparos,
  rayos) vuelve a funcionar sobre una pantalla vacía. Se deja en 1 y se vacían también las tablas.
- **Piezas del escenario que se mueven en una fila de caracteres** (los emisores): columnas en RAM (`ECOL`), y al
  moverlas se borra la fila entera, se redibuja y se vuelve a poner el rayo o el aviso en la columna nueva.
- SDI '86 se queda **sin trucos** (lo pidió Tony). El invencible solo existe en la versión de pruebas (`-D PRUEBA=1`).

## 17. Un juego de varios programas en un solo XEX (130XE) y el paquete final

**Versión 130XE** (`empaquetado/xestore.s`, `xeldr.s`, `xemove.s`, `mkxe130.py`)
- Un XEX se lee una vez. Si el juego tiene que volver a programas ya cargados (título tras el GAME OVER, fase 1 en
  la vuelta siguiente), todo tiene que quedarse en memoria. 74 KB no caben en 64 KB, pero sí en un 130XE:
  4 bancos de 16 KB (páginas virtuales 0-255) y 14 KB de RAM bajo el SO ($C000-$CFFF, $D800-$FFFF).
- El XEX trae trozos de 8 KB a $2000-$3FFF; tras cada uno, un INITAD en $0600 los guarda en su banco (PORTB
  `$E3 | banco<<2`, bit 4 a 0) o bajo el SO (PORTB `$FE`, con SEI y NMIEN = 0 mientras dura).
- El banco se ve en $4000-$7FFF, el mismo sitio donde a veces hay que escribir el programa: el cargador copia cada
  página a un búfer ($0600) y de ahí a su destino.
- El cargador residente no se puede cargar en $0700 desde el XEX (ahí está el DOS mientras se lee el fichero): va
  a $2100 y el arranque (RUNAD, $2000) lo copia a $0700.
- Lo primero, comprobar que hay 128 KB (escribir en el banco 0 y en la RAM normal y comparar); si no, avisar en
  pantalla con códigos internos y pararse.
- Probar con `run8 juego.xex guion -xe` (sin `-xe` el arnés emula un XL de 64 KB: sale el aviso).

**Paquete final** (lo habitual): `juego/` (cartucho, disco, XEX 130XE, un XEX por operación, disco de prueba),
`documentos/` (folleto A5 con la carátula oficial, atlas y memoria del proyecto en A4, la carátula), `banda_sonora/`,
`capturas/`, `codigo_fuente/` (reproducible byte a byte con `build.sh`) y el banco de trabajo. Sin scripts de
publicación. Los generadores del folleto y del atlas de SDI '86 están en `documentacion/build_docs_sdi86.py`.

**Base de computadoras de la operación 4 (los Compuzoides)**
- **Suelo con dibujo sin tocar la lógica:** las casillas vacías siguen siendo el carácter 0 (los enemigos solo pisan 0).
  Una copia del juego de caracteres en $B800 tiene el 0 dibujado como chapa, y una DLI propia (`dli4`) pone CHBASE
  por filas: la arena usa la copia y el marcador, el original. CHBASE se escribe antes del WSYNC; es seguro porque
  la última línea del carácter del suelo y la del espacio son iguales (vacías).
- **Leds que laten y brillo que recorre la base:** cada cuadro se reescribe la tabla de la DLI (PF2 con un ciclo de
  rojos y una fila de PF1 más clara que baja). Los enemigos de caracteres comparten colores de fila con la base, así
  que todo va en la misma gama metálica.
- **Balas que no se confunden:** con el quinto player todos los misiles salen del mismo color. Las balas enemigas
  pasan a P2-P3 (bolas rojas) y los disparos del jugador se quedan en misiles blancos, con SIZEM ancho según la
  dirección (ráfaga horizontal cuádruple, diagonal doble, vertical alta).

**Emisores de JANUS que patrullan:** cada uno con su columna, sentido y temporizador; salen por un borde y entran por
el otro, cambian de sentido al azar o al toparse con otro, y se paran mientras avisan y disparan (el rayo siempre
sale de un emisor quieto, así no hay que moverlo).
- **Error que costó (disparos que "rebotaban"):** el bucle de disparos guardaba su índice en `cur` y `ene_hit`
  guardaba en `cur` el del enemigo. Al volver, el bucle borraba otro hueco y seguía con un índice de enemigo,
  escribiendo encima de las coordenadas y la dirección de otro disparo: la bala cambiaba de rumbo. Cada bucle con
  su variable de índice propia (`scur`). Se encontró volcando `SXP/SYP/SDP` cada cuadro y comprobando que cada
  disparo avanza exactamente lo que dice su dirección.


## 18. Lecciones aprendidas (La Noche de los Strigoi: plataformas con scroll, 5 fases, 6 jefes)

**Memoria: módulos por fase en tres soportes**
- Programa residente 000-BFF; una zona superpuesta de 7,5 KB en 200 para el tramo, la arena o la pantalla de título;
  el código de cada fase en C00 (hasta 3 KB). Los 14 superpuestos van comprimidos con LZ (94 KB → 26 KB) bajo el SO.
- Un módulo es un **flujo de registros**: destino (2), longitud (2), datos, y un destino de página alta 0 para terminar. El mismo
  flujo sirve desde los bancos del 130XE, desde sectores de 256 bytes (SIO) o desde páginas de un AtariMax 8 Mbit. El arranque usa
  el mismo lector para un «módulo 0» (fuente, residente y paquetes fijos). El residente es idéntico en los tres soportes;
  `mod_load` siempre está en C00.
- Disco: el SIO necesita la VBI (temporizadores) y las IRQ; se lee cada sector con el SO dentro y se analiza con el SO fuera y sin NMI.
  Después de leer, **restaurar AUDCTL y SKCTL** (el SIO los deja a su manera) y apagar la música mientras dura la carga.
- Cartucho: con el cartucho dentro el SO vigila TRIG3; NMI apagadas mientras se lee, `sta ` al acabar y GINTLK = TRIG3.
- Probar disco y cartucho en XL de 64 KB (`MACH=-xl walk8`) además de en el 130XE.

**Pantalla**
- **DLI en ANTIC 4 ancho:** la última línea de la fila deja a la CPU a media velocidad. Antes de WSYNC, solo guardar A y X en página
  cero y leer el índice (ni pila ni cargas indexadas). Tras WSYNC: CHBASE, los colores que más se notan y HSCROL al final, con una
  tabla que ya trae el valor de la fila siguiente si la actual no desplaza. Medir con `medir_dli.py`: de 223 cuadros de 300 con
  error a ninguno.
- **El quinto color:** en ANTIC 4 un carácter invertido pinta «11» con PF3. Decorados enteros (empalados, esqueletos) con un color
  propio por fila. En la misma celda no pueden convivir PF2 y PF3 (`code4` lo comprueba); el motor enmascara el bit 7 al leer la clase.
- Los píxeles de ANTIC 4 son el doble de anchos que de altos: un personaje dibujado «cuadrado» sale achatado. Duplicar filas.

**Diseño y pruebas**
- Bocetos **sobre capturas reales** con los colores que permite cada fila: el autor elige entre cosas que se pueden montar.
- Un bot por jefe (lee su estado, esquiva y golpea) y `walk8` para los tramos; `ARENA_TEST`, `FASEn_TEST`, `PRUEBA`, `MUS_TEST`.
- Buscar fosos sin salida con el invencible: si no puede morir, cualquier hueco cerrado bloquea la partida.
- Prohibido `*+N`: un `bcs *+4` que debía ser `*+3` caía en mitad de una instrucción. Etiquetas anónimas.
- Los textos de los generadores se comprueban (`assert len <= ancho`): un «GREMIO» truncado en silencio llegó a la pantalla.
- Reservar margen de residente desde el principio: el juego acabó con ~50 bytes libres.
