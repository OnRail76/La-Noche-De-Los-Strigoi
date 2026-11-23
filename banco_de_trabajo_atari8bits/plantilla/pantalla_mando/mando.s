; ===============================================================
; SDI '86 · CARÁTULA y PANTALLA DE MANDO DE JANUS (título)
;
; Pantalla de mando (todo en la RAM de $A000-$BFFF, que en el título no usa nadie más):
;   ANTIC 2  DEFCON · ALERTA · T-MENOS
;   ANTIC 4  cinta de peligro (scroll fino a la derecha)
;   ANTIC E  logotipo SDI '86, 20 líneas con degradado por DLI
;   ANTIC 6  PROTOCOLO FINAL
;   ANTIC E  mapa de guerra 160 x 60: trayectorias que se dibujan, cabeza = M0, impacto = P3, radar = P1
;   ANTIC 2  teletipo de JANUS · 6 operaciones (la elegida, en negativo) · AMENAZA y RÉCORD
;   ANTIC 4  cinta de peligro (al revés) · ANTIC 2 PULSA FIRE y créditos
; El DEFCON baja solo con el reloj T-MENOS (30 s sin tocar el mando). En DEFCON 1 suena la alarma;
; a 00:00 sale la pantalla de récords. Tocar el mando vuelve a DEFCON 5.
; ===============================================================
TMAP    = $A830             ; 60 x 40: la línea 50 empieza justo en $B000 (límite de 4 KB)
TLOGO   = $B1A0             ; 20 x 40
DLTITLE = $B900
TTXT    = $BA00             ; HUD 40 · PF 20 · teletipo 40 · menú 240 · amenaza 40 · créditos 40
TT_O_PF   = 40
TT_O_TELE = 60
TT_O_MENU = 100
TT_O_AMEN = 340
TT_O_CRED = 380
TSTRIPE = $BC00
COVER   = $A010             ; carátula (solo al encender): la línea 102 empieza en $B000
DLCOVER = $BE40
MAPY0   = 76                ; línea PMG de la primera fila del mapa
TSEG0   = $30               ; segundos de la cuenta atrás (BCD)

; entradas de la DLI (la DLI de cada línea prepara la siguiente). El logotipo no lleva una DLI por línea:
; sus líneas miden un solo scanline y las DLI se anidarían. La DLI de la cinta 1 (entrada E_LOGO) recorre
; las 20 líneas con WSYNC escribiendo el degradado y deja puestos los colores de PROTOCOLO FINAL.
E_STR1  = 0
E_LOGO  = 1
E_MAP   = 2
E_TELE  = 3
E_MENU  = 4                 ; 4-9
E_AMEN  = 10
E_STR2  = 11
E_CRED  = 12
DLI_USED = 13

        .segment "ZEROPAGE"
apx:    .res 2              ; trayectoria en curso: x e y
apy:    .res 2
tptr:   .res 2              ; teletipo
d1:     .res 1              ; temporales SOLO de la DLI de la carátula
d2:     .res 1
dband:  .res 1

        .segment "HIBSS"
sel:    .res 1              ; operación elegida (0 ARCADE, 1-5)
sel0:   .res 1              ; (truco: la elegida antes de abajo, abajo)
tdef:   .res 1              ; DEFCON 1-5
tseg:   .res 1              ; segundos que faltan (BCD)
tfr:    .res 1
tal:    .res 1              ; cuadros de alarma a 00:00
tcol:   .res 1              ; teletipo: columna, retardo, espera, mensaje
tdel:   .res 1
thold:  .res 1
tmsg:   .res 1
tforce: .res 1              ; 1 = el mensaje en curso es de aviso (no se cambia hasta acabar)
arcn:   .res 1              ; trayectoria en curso
arcp:   .res 1              ; punto
arcst:  .res 1              ; 0 dibujando · 1 impacto · 2 pausa · 3 espera antes de borrar el mapa
arct:   .res 1
headx:  .res 1
heady:  .res 1
oheady: .res 1
burx:   .res 1
bury:   .res 1
sweep:  .res 1
pos1:   .res 1
pos2:   .res 1
blink:  .res 1
REC:    .res 18             ; récord por operación (6 x 3 BCD)

        .segment "CODE"
; ---------------------------------------------------------------
; CARÁTULA: JANUS y el misil (ANTIC E con 3 colores por franja de 4 líneas). Solo al encender.
cover:  lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr m_wait
        lda #<COVER_BM      ; 7.680 bytes a COVER
        sta src
        lda #>COVER_BM
        sta src+1
        lda #<COVER
        sta dst
        lda #>COVER
        sta dst+1
        ldx #30
@cp:    txa
        pha
        ldy #0
@cb:    lda (src),y
        sta (dst),y
        iny
        bne @cb
        inc src+1
        inc dst+1
        pla
        tax
        dex
        bne @cp
        lda #<DLCOVER_T
        sta src
        lda #>DLCOVER_T
        sta src+1
        lda #<DLCOVER
        sta dst
        lda #>DLCOVER
        sta dst+1
        ldx #DLCOVER_LEN
        jsr m_copy
        lda #<cover_dli
        sta VDSLST
        lda #>cover_dli
        sta VDSLST+1
        lda #0
        sta COLOR4
        lda #<DLCOVER
        sta SDLSTL
        lda #>DLCOVER
        sta SDLSTH
        lda #3
        sta gmode
        jsr m_wait
        lda #$22
        sta SDMCTL
        jsr m_wait
        lda #$C0
        sta NMIEN
        lda #MUS_TITULO
        jsr mus_play
        lda #1
        sta fireold
        ldx #104            ; 6 segundos (104 + 256) o FIRE
        ldy #2
@w:     txa
        pha
        tya
        pha
        jsr m_wait
        jsr m_mando
        pla
        tay
        pla
        tax
        lda fireed
        bne @x
        dex
        bne @w
        dey
        bne @w
@x:     lda #$40
        sta NMIEN
        lda #<m_dli
        sta VDSLST
        lda #>m_dli
        sta VDSLST+1
        rts

; la DLI va en la línea 2 de cada franja: espera su final, prepara los colores durante la 3
; y los escribe al empezar la franja siguiente (como cine.s del banco)
cover_dli:
        sta WSYNC
        pha
        txa
        pha
        tya
        pha
        inc dband
        ldx dband
        lda COVER_C1,x
        sta d1
        ldy COVER_C2,x
        lda COVER_C0,x
        ldx d1
        sta WSYNC
        sta COLPF0
        stx COLPF1
        sty COLPF2
        pla
        tay
        pla
        tax
        pla
        rti

cover_vbi:
        lda #0
        sta dband
        sta COLBK
        lda COVER_C0
        sta COLPF0
        lda COVER_C1
        sta COLPF1
        lda COVER_C2
        sta COLPF2
        rts

DLCOVER_T:
        .byte $70,$70,$70
        .byte $4E, <COVER, >COVER
        .repeat 101, I
        .if (I+1) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $CE, <$B000, >$B000
        .repeat 89, I
        .if (I+103) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $41, <DLCOVER, >DLCOVER
DLCOVER_LEN = * - DLCOVER_T

; ===============================================================
; PANTALLA DE MANDO
; entrada: la música del título ya suena
mando:  jsr mando_init
mloop:  jsr m_wait
        jsr m_mando
        inc blink
        ; --- cualquier toque del mando: vuelta a DEFCON 5
        lda stked
        ora fireed
        beq @nt
        jsr t_reset
@nt:    ; --- START: empezar
        lda CONSOL
        and #1
        bne @ns
        jmp m_start
@ns:    ; --- arriba / abajo: operación (y el truco abajo, abajo, FIRE)
        lda stked
        and #J_DOWN
        beq @nd
        lda chk
        bne @c1
        lda sel
        sta sel0
@c1:    lda chk
        cmp #2
        bcs @c2
        inc chk
@c2:    lda sel
        cmp #5
        bcs @nd2
        inc sel
        jsr t_menu
        jmp @nd2
@nd:    lda stked
        beq @nd2
        lda #0
        sta chk
@nd2:   lda stked
        and #J_UP
        beq @nu
        lda sel
        beq @nu
        dec sel
        jsr t_menu
@nu:    ; --- izquierda / derecha: amenaza
        lda stked
        and #J_LEFT
        beq @nl
        lda dif
        beq @nl
        dec dif
        jsr t_amen
@nl:    lda stked
        and #J_RIGHT
        beq @nr
        lda dif
        cmp #2
        bcs @nr
        inc dif
        jsr t_amen
@nr:    ; --- FIRE
        lda fireed
        beq @nf
        lda chk
        cmp #2
        bne @go
        lda #1              ; truco: abajo, abajo, FIRE -> invencible
        sta cheat
        lda #3
        sta chk
        lda sel0
        sta sel
        jsr t_menu
        lda #FX_BEEP
        jsr sfx
        jmp @nf
@go:    jmp m_start
@nf:    jsr t_clock
        jsr t_tele
        jsr t_arcs
        jsr t_blink
        lda tal             ; ¿alarma terminada? -> récords
        cmp #1
        beq *+5
        jmp mloop
        jsr records
        jsr mando_init
        jmp mloop

; FIRE o START: si la operación existe, a jugar
m_start:
        ldx sel
        lda TT_IMPL,x
        bne @ok
        lda #<TELE_PREP
        ldx #>TELE_PREP
        jsr t_say
        lda #FX_KLAX2
        jsr sfx
        jmp mloop
@ok:    lda sel
        sta mode
        jmp newgame

; ---------------------------------------------------------------
mando_init:
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr m_wait
        ; display list
        lda #<DLT_T
        sta src
        lda #>DLT_T
        sta src+1
        lda #<DLTITLE
        sta dst
        lda #>DLTITLE
        sta dst+1
        ldx #DLT_LEN
        jsr m_copy
        ; logotipo y mapa
        jsr t_logo
        jsr t_mapcopy
        ; textos
        lda #<TT_HUD
        sta src
        lda #>TT_HUD
        sta src+1
        lda #<TTXT
        sta dst
        lda #>TTXT
        sta dst+1
        ldx #40
        jsr m_copy
        lda #<TT_PF
        sta src
        lda #>TT_PF
        sta src+1
        lda #<(TTXT+TT_O_PF)
        sta dst
        lda #>(TTXT+TT_O_PF)
        sta dst+1
        ldx #20
        jsr m_copy
        lda #<(TTXT+TT_O_TELE)
        sta dst
        lda #>(TTXT+TT_O_TELE)
        sta dst+1
        lda #0
        ldx #40
        jsr m_fill
        lda #<TT_MENU
        sta src
        lda #>TT_MENU
        sta src+1
        lda #<(TTXT+TT_O_MENU)
        sta dst
        lda #>(TTXT+TT_O_MENU)
        sta dst+1
        ldx #240
        jsr m_copy
        lda #<TT_CRED
        sta src
        lda #>TT_CRED
        sta src+1
        lda #<(TTXT+TT_O_CRED)
        sta dst
        lda #>(TTXT+TT_O_CRED)
        sta dst+1
        ldx #40
        jsr m_copy
        ; cinta de peligro: A B A B ...
        ldx #55
@hz:    txa
        and #1
        tay
        lda HZC,y
        sta TSTRIPE,x
        dex
        bpl @hz
        ; PMG: borra la zona de una línea de $A300-$A7FF (el mapa empieza en $A830)
        lda #0
        tax
@pc:    sta $A300,x
        sta $A400,x
        sta $A500,x
        sta $A600,x
        sta $A700,x
        inx
        bne @pc
        ldx #MAP_H-1        ; radar: una raya vertical en P1 a lo alto del mapa
        lda #$80
@sw:    sta $A500+MAPY0,x
        dex
        bpl @sw
        lda #$A0
        sta PMBASE
        lda #$01
        sta GPRIOR
        lda #0
        sta SIZEM
        sta SIZEP1
        sta SIZEP3
        lda #$0E
        sta PCOLR0
        lda #$CC
        sta PCOLR1
        lda #$1C
        sta PCOLR3
        ; estado
        ldx #DLI_USED-1
        lda #0
@th:    sta DTHS,x
        dex
        bpl @th
        sta chk
        sta tforce
        sta arcn
        sta arcp
        sta arcst
        sta headx
        sta burx
        sta oheady
        sta sweep
        sta tmsg
        jsr t_reset
        jsr t_menu
        jsr t_amen
        jsr t_nextmsg
        ; colores del marcador de arriba (sombras)
        lda #0
        sta COLOR4
        sta COLOR2
        lda #$0C
        sta COLOR1
        lda #>CHARSET
        sta CHBAS
        lda #<mando_dli
        sta VDSLST
        lda #>mando_dli
        sta VDSLST+1
        lda #<DLTITLE
        sta SDLSTL
        lda #>DLTITLE
        sta SDLSTH
        lda #3
        sta GRACTL
        lda #2
        sta gmode
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        lda #$C0
        sta NMIEN
        rts

HZC:    .byte CH_HZA, CH_HZB

t_logo: lda #<LOGO_BM
        sta src
        lda #>LOGO_BM
        sta src+1
        lda #<TLOGO
        sta dst
        lda #>TLOGO
        sta dst+1
        ldx #4              ; 4 x 200 = 800
; copia X bloques de 200 bytes de src a dst
cp200:  txa
        pha
        ldx #200
        jsr m_copy
        lda src
        clc
        adc #200
        sta src
        bcc @a
        inc src+1
@a:     lda dst
        clc
        adc #200
        sta dst
        bcc @b
        inc dst+1
@b:     pla
        tax
        dex
        bne cp200
        rts

; mapa limpio: 2.400 bytes (12 x 200)
t_mapcopy:
        lda #<MAP_BM
        sta src
        lda #>MAP_BM
        sta src+1
        lda #<TMAP
        sta dst
        lda #>TMAP
        sta dst+1
        ldx #12
        jmp cp200

; ---------------------------------------------------------------
; colores de todas las entradas de la DLI (según operación elegida y DEFCON)
t_colors:
        ldx #DLI_USED-1
@c:     lda #0
        sta DTBK,x
        dex
        bpl @c
        ; cintas
        lda #$1E
        ldx tdef
        cpx #2
        bcs @y
        lda blink
        and #8
        beq @y0
        lda #$36
        bne @y
@y0:    lda #$1E
@y:     sta DTPF0+E_STR1
        sta DTPF0+E_STR2
        ; mapa
        lda #$C2
        sta DTPF0+E_MAP
        lda #$C8
        sta DTPF1+E_MAP
        lda #$38
        sta DTPF2+E_MAP
        ; teletipo: verde fósforo
        lda #$0C
        sta DTPF1+E_TELE
        lda #$C0
        sta DTPF2+E_TELE
        ; menú: la elegida en negativo (barra verde, letras oscuras)
        ldx #5
@m:     lda #$08
        sta DTPF1+E_MENU,x
        lda #$C0
        sta DTPF2+E_MENU,x
        cpx sel
        bne @mn
        lda #$02
        sta DTPF1+E_MENU,x
        lda #$CA
        sta DTPF2+E_MENU,x
@mn:    dex
        bpl @m
        ; amenaza: ámbar
        lda #$0C
        sta DTPF1+E_AMEN
        lda #$20
        sta DTPF2+E_AMEN
        ; créditos
        lda #$0A
        sta DTPF1+E_CRED
        lda #$00
        sta DTPF2+E_CRED
        rts

; marca de la operación elegida, colores y récord
t_menu: ldx #5
@l:     lda MROW_L,x
        sta dst
        lda MROW_H,x
        sta dst+1
        lda #0
        cpx sel
        bne @n
        lda #CH_ARROWR
@n:     ldy #1
        sta (dst),y
        dex
        bpl @l
        jsr t_colors
        ; el récord de esa operación
t_rec:  lda sel
        asl a
        adc sel
        clc
        adc #<REC
        sta src
        lda #>REC
        adc #0
        sta src+1
        lda #<(TTXT+TT_O_AMEN+TT_RECC)
        sta dst
        lda #>(TTXT+TT_O_AMEN+TT_RECC)
        sta dst+1
        lda #DIG0
        jmp put6

MROW_L:
        .repeat 6, I
        .byte <(TTXT+TT_O_MENU+I*40)
        .endrepeat
MROW_H:
        .repeat 6, I
        .byte >(TTXT+TT_O_MENU+I*40)
        .endrepeat

; línea de amenaza (dificultad) y récord
t_amen: lda #<TT_AMEN
        sta src
        lda #>TT_AMEN
        sta src+1
        lda #<(TTXT+TT_O_AMEN)
        sta dst
        lda #>(TTXT+TT_O_AMEN)
        sta dst+1
        ldx #40
        jsr m_copy
        lda dif
        asl a
        sta tmp
        asl a
        asl a
        asl a               ; dif * 16
        sec
        sbc tmp             ; dif * 14
        clc
        adc #<TT_DIFS
        sta src
        lda #>TT_DIFS
        adc #0
        sta src+1
        lda #<(TTXT+TT_O_AMEN+TT_DIFC)
        sta dst
        lda #>(TTXT+TT_O_AMEN+TT_DIFC)
        sta dst+1
        ldx #14
        jsr m_copy
        jmp t_rec

; ---------------------------------------------------------------
; reloj: T-MENOS y DEFCON
t_reset:
        lda #TSEG0
        sta tseg
        lda #0
        sta tfr
        sta tal
        lda #5
        sta tdef
        jsr t_hud
        jmp t_colors

t_clock:
        lda tal             ; alarma a 00:00
        beq @run
        dec tal
        lda blink
        and #31
        bne @r
        lda #FX_KLAX1
        jmp sfx
@run:   inc tfr
        lda tfr
        cmp #60
        bcc @r
        lda #0
        sta tfr
        sed
        lda tseg
        sec
        sbc #1
        sta tseg
        cld
        ; DEFCON: 5 hasta 24 s, 4, 3, 2 y 1 por debajo de 6 s
        ldx #5
        lda tseg
        cmp #$24
        bcs @d
        dex
        cmp #$18
        bcs @d
        dex
        cmp #$12
        bcs @d
        dex
        cmp #$06
        bcs @d
        dex
@d:     cpx tdef
        beq @nd
        stx tdef
        cpx #1
        bne @nd
        lda #<TELE_AL       ; DEFCON 1: aviso en el teletipo
        ldx #>TELE_AL
        jsr t_say
        lda #1
        sta tforce
@nd:    lda tseg
        bne @h
        lda #200            ; a 00:00: alarma 3 s y luego récords
        sta tal
@h:     jsr t_hud
        jmp t_colors
@r:     rts

; DEFCON y T-MENOS en el marcador; ALERTA parpadeando en DEFCON 2 y 1
t_hud:  lda tdef
        clc
        adc #DIG0
        sta TTXT+TT_DEF
        lda #DIG0
        sta digb
        lda tseg
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIG0
        sta TTXT+TT_SEG
        lda tseg
        and #15
        clc
        adc #DIG0
        sta TTXT+TT_SEG+1
        rts

t_blink:
        ; ALERTA y fondo del marcador
        lda tdef
        cmp #3
        bcs @off
        lda blink
        and #16
        beq @off
        ldx #9
@a:     lda TT_ALERTA,x
        sta TTXT+TT_AL,x
        dex
        bpl @a
        lda #$34
        sta COLOR2
        bne @pf
@off:   ldx #9
        lda #0
@b:     sta TTXT+TT_AL,x
        dex
        bpl @b
        sta COLOR2
@pf:    ; PULSA FIRE parpadeando
        lda blink
        and #31
        bne @c
        lda blink
        and #32
        beq @on
        ldx #9
        lda #0
@z:     sta TTXT+TT_O_CRED+2,x
        dex
        bpl @z
        bmi @c
@on:    ldx #9
@o:     lda TT_CRED+2,x
        sta TTXT+TT_O_CRED+2,x
        dex
        bpl @o
@c:     lda tdef            ; con DEFCON 1 las cintas cambian de color
        cmp #2
        bcs @r
        lda blink
        and #7
        bne @r
        jmp t_colors
@r:     rts

; ---------------------------------------------------------------
; teletipo: una letra cada 3 cuadros con un clic; espera y pasa al siguiente mensaje
t_say:  sta tptr
        stx tptr+1
        lda #0
        sta tcol
        sta tdel
        sta thold
        lda #<(TTXT+TT_O_TELE)
        sta dst
        lda #>(TTXT+TT_O_TELE)
        sta dst+1
        lda #0
        ldx #40
        jmp m_fill

t_nextmsg:
        lda #0
        sta tforce
        ldx tmsg
        lda TELE_L,x
        pha
        lda TELE_H,x
        tax
        pla
        jsr t_say
        inc tmsg
        lda tmsg
        cmp #TELE_N
        bcc @r
        lda #0
        sta tmsg
@r:     rts

t_tele: lda thold
        beq @type
        dec thold
        bne @cur
        jmp t_nextmsg
@cur:   lda blink           ; cursor parpadeando
        and #16
        beq @c0
        lda #CH_BLOCK
        bne @c1
@c0:    lda #0
@c1:    ldx tcol
        sta TTXT+TT_O_TELE,x
        rts
@type:  inc tdel
        lda tdel
        cmp #3
        bcc @r
        lda #0
        sta tdel
        ldy tcol
        lda (tptr),y
        cmp #$FF
        beq @end
        sta TTXT+TT_O_TELE,y
        lda #CH_BLOCK
        sta TTXT+TT_O_TELE+1,y
        inc tcol
        lda #FX_CLICK
        jmp sfx
@end:   lda #180
        sta thold
@r:     rts

; ---------------------------------------------------------------
; trayectorias de misil sobre el mapa
t_arcs: lda arcst
        bne @st
        ; dibujando: un punto por cuadro (dos con DEFCON 2 y 1)
        jsr @pt
        lda tdef
        cmp #3
        bcs @r0
        lda arcst
        bne @r0
        jsr @pt
@r0:    rts
@st:    cmp #1
        bne @p
        ; impacto: P3 con la explosión
        dec arct
        bne @bd
        lda #0
        sta burx
        jsr t_burclr
        lda #2
        sta arcst
        lda tdef            ; pausa: más corta cuanto más bajo el DEFCON
        asl a
        asl a
        asl a
        asl a
        adc #10
        sta arct
        rts
@bd:    jmp t_burst
@p:     cmp #2
        bne @w
        dec arct
        bne @r
        inc arcn
        lda #0
        sta arcp
        sta arcst
        lda arcn
        cmp #ARC_N
        bcc @r
        lda #3              ; todas dibujadas: espera y mapa limpio
        sta arcst
        lda #120
        sta arct
        rts
@w:     dec arct
        bne @r
        jsr t_mapcopy
        lda #0
        sta arcn
        sta arcp
        sta arcst
@r:     rts
; siguiente punto de la trayectoria arcn
@pt:    ldx arcn
        lda ARC_XL,x
        sta apx
        lda ARC_XH,x
        sta apx+1
        lda ARC_YL,x
        sta apy
        lda ARC_YH,x
        sta apy+1
        ldy arcp
        lda (apx),y
        sta tmp
        lda (apy),y
        sta tmp+1
        jsr t_plot
        lda tmp             ; cabeza del misil
        clc
        adc #48
        sta headx
        lda tmp+1
        clc
        adc #MAPY0
        sta heady
        inc arcp
        lda arcp
        ldx arcn
        cmp ARC_LEN,x
        bcc @pr
        ; llegó: impacto
        lda headx
        sec
        sbc #3
        sta burx
        lda heady
        sec
        sbc #4
        sta bury
        lda #0
        sta headx
        lda #1
        sta arcst
        lda #24
        sta arct
        lda #FX_TBOOM
        jsr sfx
@pr:    jmp t_head

; pinta el píxel tmp, tmp+1 con el color 3 en el mapa
t_plot: lda tmp+1           ; dst = TMAP + y * 40 + x / 4
        sta dst
        lda #0
        sta dst+1
        asl dst
        rol dst+1
        asl dst
        rol dst+1           ; y*4
        lda dst
        clc
        adc tmp+1
        sta dst
        bcc @a
        inc dst+1           ; y*5
@a:     asl dst
        rol dst+1
        asl dst
        rol dst+1
        asl dst
        rol dst+1           ; y*40
        lda tmp
        lsr a
        lsr a
        clc
        adc dst
        adc #<TMAP
        sta dst
        lda dst+1
        adc #>TMAP
        sta dst+1
        lda tmp
        and #3
        tax
        ldy #0
        lda (dst),y
        ora PIX3,x
        sta (dst),y
        rts
PIX3:   .byte $C0, $30, $0C, $03

; cabeza del misil: M0 de 2 líneas
t_head: ldx oheady
        beq @n
        lda $A300,x
        and #$FC
        sta $A300,x
        lda $A301,x
        and #$FC
        sta $A301,x
@n:     ldx heady
        stx oheady
        lda $A300,x
        ora #$03
        sta $A300,x
        lda $A301,x
        ora #$03
        sta $A301,x
        rts

t_burst:
        lda arct            ; 3 cuadros de explosión (24 -> 0), de pequeña a grande
        lsr a
        lsr a
        lsr a
        cmp #3
        bcc @f
        lda #2
@f:     eor #2
        asl a
        asl a
        asl a
        tax
        ldy bury
        lda #8
        sta tmp+2
@l:     lda MINAX_P,x
        sta $A700,y
        inx
        iny
        dec tmp+2
        bne @l
        rts

t_burclr:
        ldx bury
        ldy #8
        lda #0
@l:     sta $A700,x
        inx
        dey
        bne @l
        rts

; ---------------------------------------------------------------
; DLI de la pantalla de mando: la del motor, salvo en la entrada del logotipo
mando_dli:
        pha
        txa
        pha
        ldx dlin
        cpx #E_LOGO
        beq @logo
        lda DTHS,x
        sta HSCROL
        lda DTBK,x
        sta WSYNC
        sta COLBK
        lda DTPF0,x
        sta COLPF0
        lda DTPF1,x
        sta COLPF1
        lda DTPF2,x
        sta COLPF2
        inc dlin
        pla
        tax
        pla
        rti
@logo:  lda DTHS,x
        sta HSCROL
        lda LOGO_GRAD
        sta WSYNC           ; empieza la línea 0 del logotipo
        sta COLPF0
        lda #$34
        sta COLPF1
        lda #$0E
        sta COLPF2
        ldx #1
@l:     lda LOGO_GRAD,x
        sta WSYNC
        sta COLPF0
        inx
        cpx #LOGO_H
        bne @l
        lda #$34            ; PROTOCOLO FINAL (ANTIC 6, color 1 = PF1)
        ldx #$36
        sta WSYNC
        sta COLPF0
        stx COLPF1
        inc dlin
        pla
        tax
        pla
        rti

; ---------------------------------------------------------------
; VBI de la pantalla de mando: cintas, posiciones de los sprites, radar
mando_vbi:
        lda #0
        sta dlin
        lda frame
        and #1
        bne @s
        inc pos1
        dec pos2
@s:     lda pos1
        lsr a
        lsr a
        and #1
        clc
        adc #<TSTRIPE
        sta DLTITLE+DLT_S1
        lda pos2
        lsr a
        lsr a
        and #1
        clc
        adc #<TSTRIPE
        sta DLTITLE+DLT_S2
        lda pos1
        and #3
        eor #3
        sta DTHS+E_STR1
        sta DTHS+E_LOGO
        lda pos2
        and #3
        eor #3
        sta DTHS+E_STR2
        sta DTHS+E_CRED
        ; radar: barre el mapa de izquierda a derecha
        lda frame
        and #1
        bne @r
        inc sweep
        lda sweep
        cmp #160
        bcc @r
        lda #0
        sta sweep
@r:     lda sweep
        clc
        adc #48
        sta HPOSP1
        lda headx
        sta HPOSM0
        lda burx
        sta HPOSP3
        lda #0
        sta HPOSP0
        sta HPOSP2
        sta HPOSM1
        sta HPOSM2
        sta HPOSM3
        rts

; display list de la pantalla de mando (se copia a DLTITLE)
DLT_T:  .byte $70,$70,$70
        .byte $C2, <TTXT, >TTXT                         ; DEFCON / ALERTA / T-MENOS
DLT_S1 = * - DLT_T + 1
        .byte $D4, <TSTRIPE, >TSTRIPE                   ; cinta 1
        .byte $4E, <TLOGO, >TLOGO                       ; logotipo (sin DLI: ver mando_dli)
        .repeat LOGO_H-1
        .byte $0E
        .endrepeat
        .byte $C6, <(TTXT+TT_O_PF), >(TTXT+TT_O_PF)     ; PROTOCOLO FINAL
        .byte $4E, <TMAP, >TMAP                         ; mapa: líneas 0-49
        .repeat 49
        .byte $0E
        .endrepeat
        .byte $4E, <$B000, >$B000                       ; líneas 50-59
        .repeat MAP_H-52
        .byte $0E
        .endrepeat
        .byte $8E
        .byte $C2, <(TTXT+TT_O_TELE), >(TTXT+TT_O_TELE) ; teletipo
        .byte $C2, <(TTXT+TT_O_MENU), >(TTXT+TT_O_MENU) ; menú
        .repeat 5
        .byte $82
        .endrepeat
        .byte $82                                       ; amenaza
DLT_S2 = * - DLT_T + 1
        .byte $D4, <TSTRIPE, >TSTRIPE                   ; cinta 2
        .byte $42, <(TTXT+TT_O_CRED), >(TTXT+TT_O_CRED) ; PULSA FIRE y créditos
        .byte $41, <DLTITLE, >DLTITLE
DLT_LEN = * - DLT_T

; ---------------------------------------------------------------
; RÉCORDS por operación (cada 30 s sin tocar el mando, como en las recreativas)
records:
        lda #0
        sta gmode
        lda #<DESC_REC
        sta ptr
        lda #>DESC_REC
        sta ptr+1
        jsr txt_build
        ldx #0              ; puntos de las 6 operaciones
@l:     txa
        pha
        asl a
        sta tmp+2
        pla
        pha
        clc
        adc tmp+2           ; x 3
        adc #<REC
        sta src
        lda #>REC
        adc #0
        sta src+1
        pla
        pha
        clc
        adc #2              ; filas 2-7 de TSCR
        tax
        lda TSROW_L,x
        clc
        adc #R_DIG
        sta dst
        lda TSROW_H,x
        adc #0
        sta dst+1
        lda #DIG0C3          ; cifras en ámbar
        jsr put6
        pla
        tax
        inx
        cpx #6
        bne @l
        lda #$36
        sta COLOR0
        lda #$CA
        sta COLOR1
        lda #$46
        sta COLOR2
        lda #$1C
        sta COLOR3
        lda #0
        sta COLOR4
        jsr txt_show
        lda #1
        sta fireold
        ldx #224            ; 8 s (224 + 256) o cualquier toque
        ldy #2
@w:     txa
        pha
        tya
        pha
        jsr m_wait
        jsr m_mando
        pla
        tay
        pla
        tax
        lda fireed
        ora stked
        bne @x
        dex
        bne @w
        dey
        bne @w
@x:     rts

TSROW_L:
        .repeat 10, I
        .byte <(TSCR+I*20)
        .endrepeat
TSROW_H:
        .repeat 10, I
        .byte >(TSCR+I*20)
        .endrepeat

DESC_REC:
        .byte $70,$70,$70,$70,$70,$70
        .byte 7, <R_TIT, >R_TIT
        .byte 6, <R_SUB, >R_SUB
        .byte $70,$70
        .repeat 6, I
        .byte 6, <(R_LIN+I*20), >(R_LIN+I*20)
        .byte $70
        .endrepeat
        .byte $FF
