# Módulos por fase en tres soportes (La Noche de los Strigoi)

- `modulos.py` comprime los superpuestos con `lz.py`, los reparte por módulos, les da sitio bajo el SO y escribe
  `packs.inc`, `modtab.inc` y `build/modulos.json`.
- `cargador.s` (sin `MEDIO`): versión 130XE. `xcheck` avisa si no hay 128 KB, `xcopy` guarda trozos en los bancos durante
  la carga del XEX y `mod_load` copia un módulo a su sitio. `mkxex_130xe_modulos.py` monta el XEX.
- `cargador_medio.s` (con `-D MEDIO=1` disco, `-D MEDIO=2` cartucho): `mod_load` lee el mismo flujo de registros de
  sectores o de bancos; `dboot`/`cboot` cargan el «módulo 0» y saltan a `start`.
- `arranque_disco.s` (3 sectores en $0700) y `arranque_cart.s` (banco 0, copiado en el 127). `mkmedio.py atr|car salida`
  ensambla el arranque, rellena las tablas del cargador y monta el ATR o el CAR.
- `carga.s`: `pack_load` + `lz_unpack` (descompresión con el SO fuera) y `oscopy` (paquetes fijos bajo el SO desde el XEX).
