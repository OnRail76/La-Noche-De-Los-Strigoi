# Pantalla de mando (de SDI '86)

Plantilla de pantalla de título con menú, al estilo de un tablero militar de los ochenta. Sirve de punto de partida
para otros juegos: cambia los textos, el mapa y los colores.

- `mando.s` contiene la carátula (ANTIC E con una DLI por franja) y la pantalla de mando:
  - Logotipo con degradado: una sola DLI que recorre sus 20 líneas con WSYNC.
  - Mapa ANTIC E con trayectorias que se pintan punto a punto, cabeza en M0, impacto en P3 y radar en P1.
  - Teletipo, menú en negativo, DEFCON con cuenta atrás, cintas de peligro con scroll fino y pantalla de récords.
- `mando.py` contiene las costas del mapa (polígonos lon/lat a grandes rasgos), las trayectorias, el logotipo y los textos.
  El generador del juego (`tools/gen.py` de SDI '86) los convierte en datos.
- Usa el motor común (`motor/`): `m_mando`, `sfx`, `put6`, `txt_build`, `txt_show` y las tablas de la DLI.
