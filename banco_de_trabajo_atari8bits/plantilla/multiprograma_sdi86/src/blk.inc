; ---------------------------------------------------------------
; SDI '86 · bloque compartido entre programas (página 5) y cargador residente
; El arranque del disco o del cartucho lo inicializa; los programas lo leen al empezar y lo
; escriben antes de llamar al cargador. Sin cargador (un XEX suelto), cada programa pone valores por defecto.
; ---------------------------------------------------------------
PERS    = $0580
B_SIG   = PERS+0            ; $86 = válido
B_DIF   = PERS+1            ; 0 FÁCIL · 1 NORMAL · 2 HARDCORE
B_MODE  = PERS+2            ; 0 ARCADE · 1-5 operación suelta
B_CHEAT = PERS+3
B_PHASE = PERS+4            ; operación que hay que jugar (1-5)
B_LOOP  = PERS+5            ; vuelta
B_SCORE = PERS+6            ; 3 BCD
B_LIVES = PERS+9
B_CHAIN = PERS+10           ; 1 = viene de la operación anterior en ARCADE (conserva puntos y vidas)
B_NEXTX = PERS+11           ; 3 BCD: siguiente vida extra
B_SEL   = PERS+14           ; operación elegida en el menú
B_BOOT  = PERS+15           ; 1 = la carátula ya se ha visto
REC     = PERS+16           ; 6 x 3 BCD: récord por modo
B_LDR   = PERS+34           ; 1 = hay cargador (disco o cartucho)
SIGV    = $86
LOADER  = $0710             ; A = programa (0 título · 1-5 operaciones)
