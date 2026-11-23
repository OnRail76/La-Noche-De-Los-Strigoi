; ===============================================================
; ARENAS: lo común a todos los jefes (residente)
; pantalla fija, bloques de casillas, marcador, destellos, muerte espectacular
; ===============================================================
ASCR    = $BC00             ; pantalla de la arena (21 x 40)
BHP_MAX = 16                ; 10 golpes a Mort + 6 al lobo
BHP_WOLF = 6
MORT_W  = 13
MORT_H  = 11
WOLF_W  = 8
WOLF_H  = 4
WOLF_ROW = 14
WOLF_MAXC = 40 - WOLF_W

        .segment "HIBSS"
bphase: .res 1              ; 0 Mort, 1 lobo, 2 vencido
bhp:    .res 1
mstate: .res 1
mt:     .res 1
mpos:   .res 1              ; tumba (0-2)
matk:   .res 1
mvis:   .res 1              ; Mort dibujado
bflash: .res 1
spos:   .res 1              ; columna de las esquirlas
wstate: .res 1
wt:     .res 1
wx:     .res 1
wdir:   .res 1              ; 1 = hacia la izquierda
bwin:   .res 1
blk_r:  .res 1
blk_c:  .res 1
blk_w:  .res 1
blk_h:  .res 1
blk_i:  .res 1
bx_l:   .res 1              ; caja del jefe (x de pantalla, líneas)
bx_r:   .res 1
bx_t:   .res 1
bx_b:   .res 1
bdt:    .res 1              ; tiempo de la secuencia de muerte
bdur:   .res 1
bfinal: .res 1              ; 1 = muerte final, 0 = transformación en lobo
cr_r0:  .res 1              ; bloque que se desmorona
cr_c:   .res 1
cr_w:   .res 1
cr_h:   .res 1
cr_i:   .res 1
dact:   .res 4              ; escombros (missiles)
dpx:    .res 4
dpy:    .res 4
dpyf:   .res 4
dvx:    .res 4
dvyl:   .res 4
dvyh:   .res 4

        .segment "CODE"
AIDENT: .byte 0,1           ; clases del mapa de la arena (el valor ya es la clase)

victory:
        lda #<fase2_start   ; tras la pantalla: la fase 2
        sta aftert
        lda #>fase2_start
        sta aftert+1
        lda #<DESC_VIC
        sta ptr
        lda #>DESC_VIC
        sta ptr+1
        lda #4
        jmp txt_score_wait

DESC_VIC:
        .byte $70,$70,$70,$70
        .byte 7, <T_V1, >T_V1
        .byte $70,$70
        .byte 6, <T_V2, >T_V2
        .byte 6, <T_V3, >T_V3
        .byte $70,$70
        .byte 6, <T_V4, >T_V4
        .byte $70,$70
        .byte 6, <T_PTS, >T_PTS
        .byte $FF

; DLI de la arena: en la primera línea de una fila ANTIC 4 la CPU apenas tiene ciclos,
; así que tras WSYNC van primero CHBASE, PF1 y PF2 (los que cambian entre capa y tumbas)
dli_arena:
        sta dza
        stx dzx
        ldx dlin
        stx WSYNC
        lda DTCH,x
        sta CHBASE
        lda DTPF1,x
        sta COLPF1
        lda DTPF2,x
        sta COLPF2
        lda DTPF0,x
        sta COLPF0
        lda DTBK,x
        sta COLBK
        lda DTPF3,x
        sta COLPF3
        inc dlin
        ldx dzx
        lda dza
        rti

; display list de la arena: marcador + 21 filas, todas con DLI
ADLTPL: .byte $70,$70,$70
        .byte $C2, <HUD, >HUD
        .byte $C4, <ASCR, >ASCR
        .repeat 20
        .byte $84
        .endrepeat
        .byte $41, <DLGAME, >DLGAME
ADLLEN = * - ADLTPL

; direcciones de las filas de la pantalla y del fondo
ASROW_LO: .repeat 21, I
        .byte <(ASCR+I*40)
        .endrepeat
ASROW_HI: .repeat 21, I
        .byte >(ASCR+I*40)
        .endrepeat
ABROW_LO: .repeat 21, I
        .byte <(ARENA_BG+I*40)
        .endrepeat
ABROW_HI: .repeat 21, I
        .byte >(ARENA_BG+I*40)
        .endrepeat

; copia todo el fondo a la pantalla
arena_bg_all:
        lda #0
        sta blk_r
        sta blk_c
        lda #40
        sta blk_w
        lda #21
        sta blk_h
        jmp blk_erase

; ---------------------------------------------------------------
; bloques: blk_r, blk_c, blk_w, blk_h; ptr = códigos (para dibujar)
; ---------------------------------------------------------------
; dibuja el bloque de ptr; los códigos 0 dejan el fondo
blk_draw:
        lda #0
        sta blk_i
@row:   lda blk_r
        clc
        adc blk_i
        tax
        lda ASROW_LO,x
        clc
        adc blk_c
        sta dst
        lda ASROW_HI,x
        adc #0
        sta dst+1
        ldy #0
@col:   lda (ptr),y
        beq @sk
        sta (dst),y
@sk:    iny
        cpy blk_w
        bne @col
        lda ptr
        clc
        adc blk_w
        sta ptr
        bcc @n
        inc ptr+1
@n:     inc blk_i
        lda blk_i
        cmp blk_h
        bne @row
        rts

; repone el fondo en el rectángulo del bloque
blk_erase:
        lda #0
        sta blk_i
@row:   lda blk_r
        clc
        adc blk_i
        tax
        lda ASROW_LO,x
        clc
        adc blk_c
        sta dst
        lda ASROW_HI,x
        adc #0
        sta dst+1
        lda ABROW_LO,x
        clc
        adc blk_c
        sta src
        lda ABROW_HI,x
        adc #0
        sta src+1
        ldy #0
@col:   lda (src),y
        sta (dst),y
        iny
        cpy blk_w
        bne @col
        inc blk_i
        lda blk_i
        cmp blk_h
        bne @row
        rts

; ---------------------------------------------------------------
; marcador de la arena: puntos, vidas y barra de vida del jefe
; ---------------------------------------------------------------
hud_arena:
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(HUD+HUD_SC)
        sta dst
        lda #>(HUD+HUD_SC)
        sta dst+1
        lda #DIG0
        jsr put6
        lda lives
        cmp #10
        bcc @l
        lda #9
@l:     clc
        adc #DIG0
        sta HUD+HUDA_BAR-3
        ldx #0
@b:     lda #BAR_CODE
        cpx bhp
        bcc @on
        lda #0
@on:    sta HUD+HUDA_BAR,x
        inx
        cpx #16
        bne @b
        rts

flash_update:
        lda bflash
        beq @off
        dec bflash
        and #2
        beq @off
        lda #$0E
        ldx #17
@on:    sta DTPF1,x
        dex
        cpx #5
        bcs @on
        rts
@off:   lda bphase
        cmp #1
        beq @wolf
        ldx #17
@o1:    lda AT_PF1,x
        sta DTPF1,x
        dex
        cpx #5
        bcs @o1
        rts
@wolf:  ldx #12
@o2:    lda AT_PF1,x
        sta DTPF1,x
        dex
        cpx #5
        bcs @o2
        ldx #4
@o3:    lda WT_PF1,x
        sta DTPF1+13,x
        dex
        bpl @o3
        rts

; ---------------------------------------------------------------
; MUERTE ESPECTACULAR: explosiones en cadena, destellos, el cuerpo se
; desmorona fila a fila y los escombros saltan (los 4 missiles).
; A = 1 muerte final, 0 transformación; blk_* = bloque del jefe
; ---------------------------------------------------------------
death_start:
        sta bfinal
        lda blk_r
        sta cr_r0
        lda blk_c
        sta cr_c
        lda blk_w
        sta cr_w
        lda blk_h
        sta cr_h
        lda #0
        sta cr_i
        sta bdt
        sta bact
        sta mvis
        lda #3
        sta bphase
        lda #$0C            ; por si soplaba el viento: fuera esquirlas
        sta DTPF3+SHARD_ROW
        lda #SHARD_ROW
        sta blk_r
        lda #0
        sta blk_c
        lda #40
        sta blk_w
        lda #1
        sta blk_h
        jsr blk_erase
        lda #60             ; transformación: corta
        ldx bfinal
        beq @d
        lda #130            ; muerte final: larga
@d:     sta bdur
        lda #7
        jsr sfx
        lda #2
        jmp sfx

dying:  inc bdt
        lda #1              ; explosiones de doble anchura
        sta SIZEP2
        sta SIZEP3
        ; explosiones: una cada 4 cuadros, alternando los dos huecos de sprite
        lda bdt
        cmp bdur
        bcs @nob
        and #3
        bne @nob
        jsr blast_spawn
@nob:   ; destello: el fondo parpadea en rojo fuego
        lda bdt
        cmp #28
        bcs @fin_fl
        and #4
        beq @bkn
        lda bdt
        and #8
        beq @wh
        lda #$44            ; rojo sangre
        bne @fl
@wh:    lda #$0E            ; blanco
@fl:    ldx #20
@f1:    sta DTBK,x
        dex
        bpl @f1
        jmp @crum
@bkn:   ldx #20
@f2:    lda AT_BK,x
        sta DTBK,x
        dex
        bpl @f2
        jmp @crum
@fin_fl:
        bne @crum
        ldx #20
@f3:    lda AT_BK,x
        sta DTBK,x
        dex
        bpl @f3
@crum:  ; el cuerpo se desmorona: una fila cada 5 cuadros, soltando escombros
        lda bdt
        cmp #10
        bcc @snd
        ldx cr_i
        cpx cr_h
        bcs @snd
        sec
        sbc #10
@m5:    cmp #5
        bcc @md
        sbc #5
        jmp @m5
@md:    cmp #0
        bne @snd
        lda cr_r0
        clc
        adc cr_i
        sta blk_r
        lda cr_c
        sta blk_c
        lda cr_w
        sta blk_w
        lda #1
        sta blk_h
        jsr blk_erase
        lda cr_r0
        clc
        adc cr_i
        asl a
        asl a
        asl a
        clc
        adc #40
        sta tyy
        lda cr_c
        asl a
        asl a
        sta tcol
        jsr debris_spawn
        jsr debris_spawn
        inc cr_i
@snd:   ; estruendo
        lda bdt
        and #15
        bne @end
        lda #9
        jsr sfx
        lda #2
        jsr sfx
@end:   lda bdt
        sec
        sbc #30
        bcc @r
        cmp bdur
        bcc @r
        ; fin de la secuencia
        lda #0
        sta SIZEP2
        sta SIZEP3
        lda bfinal
        beq @wolf
        lda #2
        sta bphase
        lda #90
        sta bwin
        rts
@wolf:  jmp wolf_start
@r:     rts

; explosión grande (tipo 7) en un punto al azar de la caja del jefe
blast_spawn:
        lda bdt
        lsr a
        lsr a
        and #1
        tax
        lda #7
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        sta exh,x
        lda bx_r
        sec
        sbc bx_l
        sta tyy
        lda RANDOM
@mx:    cmp tyy
        bcc @x
        sbc tyy
        jmp @mx
@x:     clc
        adc bx_l
        sec
        sbc #8
        bcs @x2
        lda #0
@x2:    sta exl,x
        lda bx_b
        sec
        sbc bx_t
        sta tyy
        lda RANDOM
@my:    cmp tyy
        bcc @y
        sbc tyy
        jmp @my
@y:     clc
        adc bx_t
        sec
        sbc #8
        sta ey,x
        rts

e_blast:
        inc et,x
        lda et,x
        lsr a
        lsr a
        lsr a               ; 8 cuadros por fotograma: explosiones más duraderas
        sta efr,x
        cmp #4
        bcc @r
        lda #0
        sta etyp,x
@r:     rts

; escombro: tcol = x del bloque, tyy = línea; sale disparado hacia arriba
debris_spawn:
        ldx #3
@f:     lda dact,x
        beq @ok
        dex
        bpl @f
        rts
@ok:    lda #1
        sta dact,x
        lda cr_w
        asl a
        asl a
        sta blk_i           ; ancho del bloque en píxeles
        lda RANDOM
@mw:    cmp blk_i
        bcc @in
        sbc blk_i
        jmp @mw
@in:    clc
        adc tcol
        sta dpx,x
        lda tyy
        sta dpy,x
        lda #0
        sta dpyf,x
        lda RANDOM
        and #3
        sec
        sbc #1
        sta dvx,x
        lda RANDOM
        sta dvyl,x
        lda #$FD
        sta dvyh,x
        rts

debris_update:
        ldx #3
@l:     lda dact,x
        beq @n
        lda dvyl,x
        clc
        adc #$28
        sta dvyl,x
        lda dvyh,x
        adc #0
        sta dvyh,x
        lda dpyf,x
        clc
        adc dvyl,x
        sta dpyf,x
        lda dpy,x
        adc dvyh,x
        sta dpy,x
        lda dpx,x
        clc
        adc dvx,x
        sta dpx,x
        lda dpy,x
        cmp #44             ; no subir hasta el marcador
        bcc @off
        cmp #FLOOR
        bcc @n
        cmp #240
        bcs @n
@off:   lda #0
        sta dact,x
@n:     dex
        bpl @l
        rts

; escombros en los missiles (2 x 2 píxeles, color PF3 de cada fila)
debris_draw:
        ldy rb
        lda #0
        ldx bphase
        cpx #3
        bne @sz
        lda #$55            ; missiles de doble anchura: trozos de 4 píxeles
@sz:    sta PSZM,y
        lda pmhi
        clc
        adc #3
        sta pmdst+1
        ldx #3
@l:     lda dact,x
        beq @n
        lda dpy,x
        sta pmdst
        ldy #0
        lda (pmdst),y
        ora DMASK,x
        sta (pmdst),y
        iny
        lda (pmdst),y
        ora DMASK,x
        sta (pmdst),y
        iny
        lda (pmdst),y
        ora DMASK,x
        sta (pmdst),y
        lda dpx,x
        clc
        adc #HP0
        ldy rb
        cpx #0
        bne @1
        sta PHM0,y
        jmp @n
@1:     cpx #1
        bne @2
        sta PHM1,y
        jmp @n
@2:     cpx #2
        bne @3
        sta PHM2,y
        jmp @n
@3:     sta PHM3,y
@n:     dex
        bpl @l
        rts
DMASK:  .byte $03,$0C,$30,$C0

; explosión grande: 4 cuadros de 16 líneas
BLAST:  .byte $00,$18,$3C,$7E,$7E,$FF,$FF,$FF,$FF,$FF,$FF,$7E,$7E,$3C,$18,$00
        .byte $92,$5A,$3E,$7F,$F7,$E3,$C3,$C3,$E3,$F7,$7F,$3E,$5A,$92,$01,$00
        .byte $82,$10,$45,$28,$80,$12,$40,$89,$20,$04,$A0,$05,$50,$09,$80,$12
        .byte $00,$20,$72,$27,$02,$10,$38,$12,$07,$42,$E0,$48,$1C,$08,$00,$00
BLASTCOL: .byte $0E,$1E,$3A,$06



; como blk_draw pero copiando también los códigos 0 (el fondo vacío)
blk_draw_all:
        lda #0
        sta blk_i
@row:   lda blk_r
        clc
        adc blk_i
        tax
        lda ASROW_LO,x
        clc
        adc blk_c
        sta dst
        lda ASROW_HI,x
        adc #0
        sta dst+1
        ldy #0
@col:   lda (ptr),y
        sta (dst),y
        iny
        cpy blk_w
        bne @col
        lda ptr
        clc
        adc blk_w
        sta ptr
        bcc @n
        inc ptr+1
@n:     inc blk_i
        lda blk_i
        cmp blk_h
        bne @row
        rts
