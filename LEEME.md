# LA NOCHE DE LOS STRIGOI · VERSIÓN FINAL

Acción y plataformas para Atari de 8 bits (XL/XE, NTSC).
2026 - TONY C. WARE

Sighișoara, 1847. Radu, un haiduc de los Cárpatos, cruza el cementerio con su baltag para llegar al Trono de Sangre.

## Qué hay aquí

| Carpeta / fichero | Qué es |
|---|---|
| `juego/strigoi.car` | Cartucho AtariMax 8 Mbit (CAR tipo 42) para Atari XL/XE de 64 KB. Arranca solo y carga cada fase al instante |
| `juego/strigoi.atr` | Disco autoarrancable sin DOS (doble densidad) para XL/XE de 64 KB. Lee cada fase al empezarla |
| `juego/Strigoi_130XE.xex` | XEX para Atari 130XE (128 KB): guarda las fases en la memoria extendida. En 64 KB avisa y se para |
| `juego/prueba/` | Solo para pruebas, con Radu invencible: el disco y un XEX que empieza en cada fase (2 a 5) |
| `documentos/Strigoi_Instrucciones.pdf` | Folleto de instrucciones ilustrado (A5) con la carátula oficial |
| `documentos/Strigoi_Atlas_y_Memoria.pdf` | Atlas visual (A4): fases, jefes, bestiario, música, técnica, memoria del proyecto y aprendizaje |
| `documentos/Strigoi_Caratula_Oficial_Para_Imprimir.pdf` | La carátula oficial para imprimir (y en `.jpg`) |
| `banda_sonora/` | Los seis temas grabados del emulador: título, fase A, fase B, jefes, final y GAME OVER |
| `capturas/` | 23 pantallas del juego: título, las cinco fases, los seis jefes, el final y el GAME OVER |
| `codigo_fuente/` | Código, gráficos, música, herramientas y generadores de la documentación. `build_all.sh` reconstruye los tres formatos idénticos byte a byte |
| `banco_de_trabajo_atari8bits/` | El banco de trabajo actualizado: motor común, empaquetado (ahora con módulos por fase en 130XE, disco y cartucho), motor de jefes, arnés, análisis y la GUIA con las lecciones de este juego |

## Jugar

- **Título:** izquierda y derecha eligen NORMAL o HARDCORE; FIRE empieza. Nunca entra el modo de demostración.
- **Palanca:** izquierda y derecha andan, arriba salta, abajo agacha; FIRE lanza el baltag.
- **Vidas:** 3, y una más cada 20.000 puntos. En NORMAL, Radu empieza cada vida con su chaqueta de cuero, que aguanta un golpe.
- **GAME OVER:** la calavera de Radu, la puntuación y vuelta al título con el récord.
- **Truco:** en el título, abajo, abajo, FIRE: Radu invencible (sale INVENCIBLE).
- Emulador: Altirra o atari800 con un 800XL para el disco y el cartucho, o un 130XE para el XEX. Vídeo NTSC.

## Las fases

1. **El Cementerio de la Colina y la Escalera Cubierta.** Jefe: el Strigoi Mort y su lobo.
2. **La Ciudadela y las Torres de los Gremios.** Jefe: Aric, el Sastre de las Sombras.
3. **Las Minas de Sal y las Criptas.** Jefe: Muma Pădurii.
4. **El Paso de los Cárpatos.** Jefes: el Căpcăun y el Rey Strigoi alado.
5. **El Castillo del Trono de Sangre.** Jefe final: la cabeza del Rey Strigoi.

## Probado en el emulador

- Disco y cartucho en XL de 64 KB y en 130XE; el XEX en 130XE.
- Cada jefe vencido carga la fase siguiente en disco y en cartucho; las cinco fases y el final completo.
- Varias partidas seguidas: GAME OVER, título y nueva partida, recargando la fase 1.
- NORMAL y HARDCORE, y el truco del invencible.

## Para reconstruir

En `codigo_fuente/`: `./build_all.sh` (cc65 2.19 y Python 3 con Pillow). Deja el juego en `dist/`.
`doc/build_docs.sh` regenera los dos PDF (necesita Google Chrome).
