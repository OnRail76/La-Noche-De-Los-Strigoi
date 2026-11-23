; ---------------------------------------------------------------
; SDI '86 · PROTOCOLO FINAL · Atari 8 bits (NTSC) · 2026 - Tony C. Ware
; PROGRAMA 2 · OPERACIÓN DEFENSA SDI (al estilo de Galaxian)
;
; Pantalla: marcador + 22 filas ANTIC 4 + marcador.
;   Filas 3-6: la formación (carril 0): artilleros arriba, cazadores abajo; se balancea con el scroll fino.
;   Filas 18-19: el CENTINELA-4 del jugador en su propio carril (4 colores; se mueve con el scroll fino).
;   Filas 20-21: la Tierra. P2/P3 cazadores en picado · P0/P1 el ICBM (o sus dos cabezas MIRV)
;   M0 el disparo del jugador · M1-M3 las balas enemigas.
; Objetivo: acabar con la formación. Si 3 ICBM (o cabezas) llegan a la Tierra: GAME OVER.
; ---------------------------------------------------------------
        .include "hw.inc"
        .include "blk.inc"
FASE    = 2
MUSICA  = 1
MUS_TITULO   = 0
MUS_SUPERADA = 1
MUS_GAMEOVER = 2

; --------------------------------------------------------------- memoria
PMA     = $A000
PMB     = $A800
PMY0    = 32
PMN     = 192
SCR     = $B000             ; 22 x 40 fijo (estrellas, Tierra)
RF0     = $B400             ; formación: 4 anillos de 128
RP0     = $B600             ; nave: 2 anillos
RP1     = $B680
DLGAME  = $B700
DLTEXT  = $B780
HUDT    = $B800
HUDB    = $B828
TSCR    = $B880

NCAR    = 2                 ; carril 0 formación, 1 nave
CAR_K   = 13
CAR_NROWS = 6
EXTRA_STEP = $06

POS0    = 211               ; carril 0 con balanceo 0: la columna 0 queda en x = 32
Y_F0    = 64                ; primera fila de la formación (línea PMG)
Y_SHIP  = 191               ; parte visible de la nave
SHOT_Y0 = 186
SHIPPOS = car_pos+1
Y_EARTH = 200
NE      = 32                ; enemigos: 4 filas x 8

FX_SHOT   = 0
FX_EXPL   = 1
FX_HIT    = 2
FX_BURST  = 3
FX_DEATH  = 4
FX_SWOOP  = 5
FX_IMPACT = 6
FX_BEEP   = 7
FX_EBUL   = 8
FX_EXTRA  = 9
FX_THUMP  = 10
FX_DEATH2 = 11
FX_MIRV   = 12
FX_KLAX1  = 13
FX_KLAX2  = 14

; ---------------------------------------------------------------
        .segment "ZEROPAGE"
shipx:  .res 1              ; x de la nave (campo, 0-159)
pst:    .res 1              ; 0 viva · 1 muriendo
ptm:    .res 1
invt:   .res 1
shoty:  .res 1              ; disparo (0 = no hay)
shotx:  .res 1
sway:   .res 1              ; balanceo de la formación (con signo, -16..16)
swdir:  .res 1
alive:  .res 1              ; enemigos que quedan (en formación y en picado)
impacts:.res 1
ist:    .res 1              ; ICBM: 0 nada · 1 entero · 2 cabezas MIRV · 3 estallando
ix:     .res 1
iy:     .res 1
iyf:    .res 1
cur:    .res 1

        .segment "HIBSS"
EA:     .res NE             ; 0 muerto · 1 en formación · 2 en picado
XR:     .res 4              ; explosiones en la formación: fila, columna, tiempo ($FF libre)
XC:     .res 4
XT:     .res 4
DS:     .res 2              ; cazadores en picado: 0 libre · 1 picando · 2 volviendo · 3 estallando
DE:     .res 2
DXH:    .res 2
DXL:    .res 2
DYH:    .res 2
DYL:    .res 2
DVXH:   .res 2
DVXL:   .res 2
DVYH:   .res 2
DVYL:   .res 2
DT:     .res 2
BT:     .res 3              ; balas enemigas
BX:     .res 3
BY:     .res 3
ihp:    .res 1
ifl:    .res 1
ibt:    .res 1
HS:     .res 3              ; cabezas MIRV: 0 nada · 1 viva · 2 estallando (la 3.ª, la del centro, en vueltas altas)
HX:     .res 3
HXF:    .res 3
HB:     .res 3
HPL:    .res 3              ; player de cada cabeza (0, 1 y P2 o P3 libre)
eflash: .res 1
dvtm:   .res 1
aftm:   .res 1
ictm:   .res 2
anim:   .res 1
p_dvi:  .res 1              ; parámetros de la vuelta
p_dmax: .res 1
p_afi:  .res 1
p_bsp:  .res 1
p_ici:  .res 2
p_ivy:  .res 1
p_swk:  .res 1
p_mirv: .res 1

        .segment "CODE"
        .include "data2.s"
        .include "motor/nucleo.s"
        .include "motor/pmg.s"
        .include "motor/dli.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/carril.s"
        .include "motor/pantalla.s"
        .include "motor/musica.s"
        .include "comun.s"

; ===============================================================
; VBI de la operación: carriles y su scroll fino
f_vbi:  jsr car_vbi
        lda #0
        sta dlin
        lda car_hs
        ldx #3
@a:     sta DTHS,x
        inx
        cpx #8
        bne @a
        lda car_hs+1
        sta DTHS+18
        sta DTHS+19
        sta DTHS+20
        rts

; ---------------------------------------------------------------
f_screen:
        jsr scr_off
        lda #<DLTPL
        sta src
        lda #>DLTPL
        sta src+1
        lda #<DLGAME
        sta dst
        lda #>DLGAME
        sta dst+1
        ldx #DLLEN
        jsr m_copy
        lda #<SCR_INIT
        sta src
        lda #>SCR_INIT
        sta src+1
        lda #<SCR
        sta dst
        lda #>SCR
        sta dst+1
        ldx #4
        jsr cp220
        lda #0              ; anillos vacíos
        tax
@r:     sta RF0,x
        sta RF0+$100,x
        sta RP0,x
        inx
        bne @r
        jsr pm_init
        ldx #22
@t:     lda TABBK,x
        sta DTBK,x
        lda TABP0,x
        sta DTPF0,x
        lda TABP1,x
        sta DTPF1,x
        lda TABP2,x
        sta DTPF2,x
        lda #0
        sta DTHS,x
        dex
        bpl @t
        lda #0
        sta car_sl
        sta car_sh
        sta car_sl+1
        sta car_sh+1
        lda #POS0
        sta car_pos
        jmp scr_on

; colores por fila (entrada i = fila i; 22 = marcador de abajo)
;            0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22
TABBK:  .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$82,$86,$82,$00
TABP0:  .byte $00,$00,$00,$0A,$0A,$08,$08,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$0E,$0E,$C6,$C4,$00
TABP1:  .byte $00,$00,$00,$46,$46,$46,$46,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$96,$96,$84,$82,$0C
TABP2:  .byte $0E,$0A,$0C,$96,$96,$1E,$1E,$0A,$0E,$08,$0C,$0A,$0E,$08,$0A,$0C,$0E,$0A,$9E,$9E,$9C,$00,$00

DLTPL:  .byte $70,$70,$70
        .byte $C2
        .word HUDT
        .repeat 22, I
        .if I >= 3 && I <= 6
        .byte $D4
        .word RF0+(I-3)*128
        .elseif I = 18
        .byte $D4
        .word RP0
        .elseif I = 19
        .byte $D4
        .word RP1
        .else
        .byte $C4
        .word SCR+I*40
        .endif
        .endrepeat
        .byte $42
        .word HUDB
        .byte $41
        .word DLGAME
DLLEN = * - DLTPL

CROW_DL:   .byte 7+3*3, 7+3*4, 7+3*5, 7+3*6, 7+3*18, 7+3*19
CROW_RL:   .byte <RF0, <(RF0+128), <(RF0+256), <(RF0+384), <RP0, <RP1
CROW_RH:   .byte >RF0, >(RF0+128), >(RF0+256), >(RF0+384), >RP0, >RP1
CROW_LANE: .byte 0, 0, 0, 0, 1, 1
RFL:    .byte <RF0, <(RF0+128), <(RF0+256), <(RF0+384)
RFH:    .byte >RF0, >(RF0+128), >(RF0+256), >(RF0+384)

; ---------------------------------------------------------------
; empieza (o repite) la operación
f_start:
        ldx #NE-1
        lda #1
@e:     sta EA,x
        dex
        bpl @e
        lda #NE
        sta alive
        ldx #NE-1
@d:     txa
        pha
        jsr e_draw
        pla
        tax
        dex
        bpl @d
        lda #$FF
        ldx #3
@x:     sta XR,x
        dex
        bpl @x
        lda #0
        sta DS
        sta DS+1
        sta BT
        sta BT+1
        sta BT+2
        sta ist
        sta impacts
        sta shoty
        sta sway
        sta eflash
        sta anim
        lda #1
        sta swdir
        jsr params
        lda p_ici
        sta ictm
        lda p_ici+1
        sta ictm+1
        lda #90
        sta dvtm
        sta aftm
        jmp ship_reset

; parámetros según la vuelta y la amenaza
params: lda loopn
        cmp #5
        bcc @l
        lda #5
@l:     sta tmp             ; vuelta (tope 5)
        ; picados: cada 150 - 20 x vuelta cuadros (FÁCIL +40, HARDCORE -30), mínimo 50
        asl a
        asl a
        sta tmp+1
        asl a
        asl a
        clc
        adc tmp+1           ; x20
        sta tmp+1
        lda #150
        sec
        sbc tmp+1
        ldx dif
        clc
        adc DIF_DV,x
        cmp #50
        bcs @d1
        lda #50
@d1:    sta p_dvi
        ; cazadores a la vez: 1 en FÁCIL la primera vuelta, si no 2
        lda #2
        ldx dif
        bne @m
        ldx loopn
        bne @m
        lda #1
@m:     sta p_dmax
        ; disparos de los artilleros
        lda tmp
        asl a
        asl a
        asl a
        clc
        adc tmp
        adc tmp             ; x10
        sta tmp+1
        lda #90
        sec
        sbc tmp+1
        ldx dif
        clc
        adc DIF_AF,x
        cmp #36
        bcs @a1
        lda #36
@a1:    sta p_afi
        ; balas: 2 líneas por cuadro; 3 desde la vuelta 3 o en HARDCORE
        lda #2
        ldx dif
        cpx #2
        beq @b3
        ldx tmp
        cpx #2
        bcc @b
@b3:    lda #3
@b:     sta p_bsp
        ; ICBM: cada 900 - 100 x vuelta cuadros (mínimo 420); velocidad
        lda #<900
        sta p_ici
        lda #>900
        sta p_ici+1
        ldx tmp
        beq @i2
@i1:    lda p_ici
        sec
        sbc #100
        sta p_ici
        bcs @i0
        dec p_ici+1
@i0:    dex
        bne @i1
@i2:    lda tmp
        asl a
        asl a
        asl a
        asl a
        clc
        adc #$30
        ldx dif
        cpx #2
        bne @v
        adc #$10
@v:     cmp #$90
        bcc @v1
        lda #$90
@v1:    sta p_ivy
        ; balanceo: 1 px cada 2 cuadros la primera vuelta, luego cada cuadro
        lda #1
        ldx loopn
        bne @s
        lda #2
@s:     sta p_swk
        ; MIRV: dos cabezas desde la vuelta 3 (desde la 2 en HARDCORE), tres desde la 5 (la 4)
        lda #0
        ldx loopn
        cpx #2
        bcs @mv
        ldy dif
        cpy #2
        bne @mn
        cpx #1
        bcc @mn
@mv:    lda #1
        cpx #4              ; tres cabezas: desde la vuelta 5 (desde la 4 en HARDCORE)
        bcs @m3
        ldy dif
        cpy #2
        bne @mn
        cpx #3
        bcc @mn
@m3:    lda #2
@mn:    sta p_mirv
        rts
DIF_DV: .byte 40, 0, 226     ; FÁCIL +40 · HARDCORE -30
DIF_AF: .byte 30, 0, 236     ; FÁCIL +30 · HARDCORE -20
IHP_D:  .byte 2, 3, 4

; ---------------------------------------------------------------
; un cuadro de la operación
f_frame:
        jsr ship_update
        jsr shot_update
        jsr sway_update
        jsr xpl_update
        jsr dive_start
        jsr dive_update
        jsr art_fire
        jsr bul_update
        jsr icbm_update
        jsr fx_update
        lda pclear
        bne @r
        lda alive
        bne @r
        jmp phase_done
@r:     rts

f_status:
        lda impacts
        clc
        adc #DIG0
        sta HUDB+HUD_IM
        lda alive
        ldx #HUD_FO
        jmp st_dec2

        .include "centinela.s"

; ---------------------------------------------------------------
; DISPARO del jugador
shot_update:
        lda shoty
        bne @go
        rts
@go:    sec
        sbc #6
        cmp #34
        bcs @s
        lda #0
        sta shoty
        rts
@s:     sta shoty
        ; ¿formación?
        cmp #Y_F0
        bcc @nf
        cmp #Y_F0+32
        bcs @nf
        jsr hit_form
        bcs @hit
@nf:    jsr hit_dive
        bcs @hit
        jsr hit_icbm
        bcc @r
@hit:   lda #0
        sta shoty
@r:     rts

; columna y fila de la formación bajo el disparo -> C = 1 si mata a alguien
hit_form:
        lda shotx
        sec
        sbc #48+32
        clc
        adc sway
        cmp #96
        bcs @no
        ldx #0              ; división por 12
@d:     cmp #12
        bcc @q
        sbc #12
        inx
        bne @d
@q:     cmp #8
        bcs @no
        stx tmp
        lda shoty
        sec
        sbc #Y_F0
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a               ; fila x 8
        ora tmp
        tax
        lda EA,x
        cmp #1
        bne @no
        jsr e_kill
        sec
        rts
@no:    clc
        rts

; X = enemigo en formación: muere (puntos, explosión en sus dos caracteres)
e_kill: lda #0
        sta EA,x
        dec alive
        lda #1
        sta hudd
        txa
        pha
        cpx #16
        bcs @cz
        lda #$00            ; artillero: 100
        ldx #$01
        jsr score_add
        jmp @x
@cz:    lda #$60            ; cazador: 60
        ldx #$00
        jsr score_add
@x:     lda #FX_EXPL
        jsr sfx
        pla
        tax
        ; hueco de explosión
        ldy #3
@f:     lda XR,y
        bmi @ok
        dey
        bpl @f
        ldy #0
@ok:    txa
        lsr a
        lsr a
        lsr a
        sta XR,y
        txa
        and #7
        sta tmp
        asl a
        adc tmp             ; columna = 3 x slot
        sta XC,y
        lda #0
        sta XT,y
        rts

; dibuja (o borra, si está muerto) el enemigo X en su anillo
e_draw: txa
        lsr a
        lsr a
        lsr a
        tay
        lda RFL,y
        sta dst
        lda RFH,y
        sta dst+1
        lda EA,x
        cmp #1
        bne @z
        cpx #16
        bcs @c
        lda #AR_A
        bne @p
@c:     lda #CZ_A
@p:     sta tmp+2
        jmp @w
@z:     lda #0
        sta tmp+2
@w:     txa
        and #7
        sta tmp
        asl a
        adc tmp
        tay
        lda tmp+2
        jsr car_put
        iny
        lda tmp+2
        beq @w2
        clc
        adc #1
@w2:    jmp car_put

; explosiones en la formación: 3 cuadros de 6
xpl_update:
        ldx #3
@l:     lda XR,x
        bmi @n
        lda XT,x
        inc XT,x
        cmp #18
        bcs @end
        and #7
        cmp #0
        bne @n
        lda XT,x            ; cuadro = t / 6 aprox. (0, 8, 16 -> 0, 1, 2)
        lsr a
        lsr a
        lsr a
        asl a
        sta tmp+2
        jsr @put
        jmp @n
@end:   lda #$FF
        sta tmp+2
        jsr @put
        lda #$FF
        sta XR,x
@n:     dex
        bpl @l
        rts
@put:   ldy XR,x
        lda RFL,y
        sta dst
        lda RFH,y
        sta dst+1
        ldy XC,x
        lda tmp+2
        cmp #$FF
        beq @z
        stx tmp+3
        tax
        lda EXPL_C,x
        jsr car_put
        iny
        lda EXPL_C+1,x
        jsr car_put
        ldx tmp+3
        rts
@z:     lda #0
        jsr car_put
        iny
        lda #0
        jmp car_put

; balanceo y aleteo
sway_update:
        lda pst
        ora pclear
        bne @a
        lda frame
        ldx p_swk
        cpx #1
        beq @m
        and #1
        bne @a
@m:     lda swdir
        bne @rt
        dec sway
        lda sway
        cmp #<-16
        bne @a
        lda #1
        sta swdir
        bne @a
@rt:    inc sway
        lda sway
        cmp #16
        bne @a
        lda #0
        sta swdir
@a:     lda #POS0
        clc
        adc sway
        sta car_pos
        ; aleteo: cada 16 cuadros cambia el dibujo de los caracteres
        lda frame
        and #15
        bne @r
        lda anim
        eor #16
        sta anim
        tax
        ldy #0
@c:     lda CZ_FR,x
        sta CHARSET+CZ_A*8,y
        lda AR_FR,x
        sta CHARSET+AR_A*8,y
        inx
        iny
        cpy #16
        bne @c
@r:     rts

; x (HPOS) del hueco del enemigo X en la formación
slot_x: txa
        and #7
        sta tmp
        asl a
        adc tmp
        asl a
        asl a               ; 12 x slot
        clc
        adc #32+48
        sec
        sbc sway
        rts

; ---------------------------------------------------------------
; CAZADORES EN PICADO (P2, P3)
dive_start:
        lda pclear
        ora pst
        bne @r
        dec dvtm
        bne @r
        lda RANDOM
        and #31
        adc p_dvi
        sta dvtm
        ldy #0              ; ¿hueco libre? (y que no lo use la cabeza MIRV del centro)
@f:     lda DS,y
        bne @fn
        lda HS+2
        beq @ok
        lda ist
        cmp #2
        bne @ok
        tya
        clc
        adc #2
        cmp HPL+2
        bne @ok
@fn:    iny
        cpy p_dmax
        bcc @f
@r:     rts
@ok:    sty cur
        lda RANDOM          ; un cazador en formación (filas 2-3)
        and #15
        tax
        ldy #16
@s:     lda EA+16,x
        cmp #1
        beq @g
        inx
        txa
        and #15
        tax
        dey
        bne @s
        rts
@g:     txa
        clc
        adc #16
        tax
        lda #2
        sta EA,x
        lda #0              ; fuera de la formación (ya no es del carril)
        sta EA,x
        jsr e_draw
        lda #2
        sta EA,x
        ldy cur
        txa
        sta DE,y
        jsr slot_x
        sta DXH,y
        txa
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a
        adc #Y_F0
        sta DYH,y
        lda #0
        sta DXL,y
        sta DYL,y
        sta DVXH,y
        sta DVXL,y
        lda #$FF            ; sube un poco antes de caer
        sta DVYH,y
        lda #$00
        sta DVYL,y
        lda #1
        sta DS,y
        lda #FX_SWOOP
        jmp sfx

dive_update:
        ldx #1
@l:     lda DS,x
        bne @a
        jmp @n
@a:     cmp #3
        bne @a2
        dec DT,x            ; estallando
        bne @n2
        lda #0
        sta DS,x
@n2:    jmp @n
@a2:    cmp #2
        bne @dv
        jmp @ret
@dv:    ; gravedad
        lda DVYL,x
        clc
        adc #$10
        sta DVYL,x
        lda DVYH,x
        adc #0
        sta DVYH,x
        bmi @g
        cmp #2
        bcc @g
        lda #2
        sta DVYH,x
        lda #0
        sta DVYL,x
@g:     ; hacia la nave
        lda shipx
        clc
        adc #48+4
        cmp DXH,x
        bcc @lft
        lda DVXL,x
        clc
        adc #$0C
        sta DVXL,x
        lda DVXH,x
        adc #0
        sta DVXH,x
        jmp @cl
@lft:   lda DVXL,x
        sec
        sbc #$0C
        sta DVXL,x
        lda DVXH,x
        sbc #0
        sta DVXH,x
@cl:    lda DVXH,x          ; tope +-1,5
        bmi @cn
        beq @mv
        cmp #1
        bne @cp
        lda DVXL,x
        cmp #$80
        bcc @mv
@cp:    lda #1
        sta DVXH,x
        lda #$80
        sta DVXL,x
        bne @mv
@cn:    cmp #$FE
        bcc @cm
        bne @mv
        lda DVXL,x
        cmp #$80
        bcs @mv
@cm:    lda #$FE
        sta DVXH,x
        lda #$80
        sta DVXL,x
@mv:    lda DXL,x
        clc
        adc DVXL,x
        sta DXL,x
        lda DXH,x
        adc DVXH,x
        sta DXH,x
        lda DYH,x
        sta tmp+3           ; y anterior
        lda DYL,x
        clc
        adc DVYL,x
        sta DYL,x
        lda DYH,x
        adc DVYH,x
        sta DYH,x
        ; dispara al cruzar la línea 120
        lda tmp+3
        cmp #120
        bcs @nf
        lda DYH,x
        cmp #120
        bcc @nf
        lda DYH,x
        clc
        adc #8
        sta tmp+4
        lda DXH,x
        clc
        adc #3
        jsr bul_new
@nf:    lda DYH,x
        cmp #208
        bcc @col
        lda #2              ; por abajo: vuelve por arriba a su hueco
        sta DS,x
        lda #32
        sta DYH,x
        jmp @n
@col:   jsr dive_hit_ship
        jmp @n
@ret:   ; volver: baja y se acerca a su hueco
        txa
        pha
        lda DE,x
        tax
        jsr slot_x
        sta tmp+2
        txa
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a
        adc #Y_F0
        sta tmp+3
        pla
        tax
        lda DXH,x
        cmp tmp+2
        beq @ry
        bcc @rr
        dec DXH,x
        jmp @ry
@rr:    inc DXH,x
@ry:    lda DYH,x
        cmp tmp+3
        bcs @at
        inc DYH,x
        lda DYH,x
        cmp tmp+3
        bcs @at
        inc DYH,x
        jmp @n
@at:    lda tmp+3
        sta DYH,x
        lda DXH,x
        cmp tmp+2
        bne @n
        lda #0              ; en su hueco: vuelve a la formación
        sta DS,x
        txa
        pha
        lda DE,x
        tax
        lda #1
        sta EA,x
        jsr e_draw
        pla
        tax
@n:     dex
        bmi @x
        jmp @l
@x:     rts

; el cazador X choca con la nave
dive_hit_ship:
        lda pst
        bne @r
        jsr shipbox
        lda DXH,x
        sta tmp+0
        clc
        adc #7
        sta tmp+1
        lda DYH,x
        sta tmp+2
        clc
        adc #7
        sta tmp+3
        jsr boxhit
        bcc @r
        stx cur
        jsr kill_ship
        ldx cur
        lda cheat
        bne @r
        jmp dive_die
@r:     rts

; el cazador X estalla
dive_die:
        lda #3
        sta DS,x
        lda #24
        sta DT,x
        txa
        pha
        lda DE,x
        tax
        lda #0
        sta EA,x
        dec alive
        lda #1
        sta hudd
        pla
        tax
        lda #FX_EXPL
        jmp sfx

; ¿el disparo da a un cazador en picado?
hit_dive:
        ldx #1
@l:     lda DS,x
        beq @n
        cmp #3
        beq @n
        lda shotx
        sta tmp+0
        clc
        adc #1
        sta tmp+1
        lda shoty
        sta tmp+2
        clc
        adc #5
        sta tmp+3
        lda DXH,x
        sta tmp+4
        clc
        adc #7
        sta tmp+5
        lda DYH,x
        sta tmp+6
        clc
        adc #7
        sta tmp+7
        jsr boxhit
        bcc @n
        jsr dive_die
        lda #$50            ; en picado: 150
        ldx #$01
        jsr score_add
        sec
        rts
@n:     dex
        bpl @l
        clc
        rts

; ---------------------------------------------------------------
; ARTILLEROS: disparan desde la formación
art_fire:
        lda pclear
        ora pst
        bne @r
        dec aftm
        bne @r
        lda RANDOM
        and #15
        adc p_afi
        sta aftm
        lda RANDOM
        and #15
        tax
        ldy #16
@s:     lda EA,x
        cmp #1
        beq @g
        inx
        txa
        and #15
        tax
        dey
        bne @s
@r:     rts
@g:     txa
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a
        adc #Y_F0+7
        sta tmp+4
        jsr slot_x
        clc
        adc #3
        jmp bul_new

; nueva bala: A = x (HPOS), tmp+4 = y; conserva X
bul_new:
        sta tmp+5
        ldy #2
@f:     lda BT,y
        beq @ok
        dey
        bpl @f
        rts
@ok:    lda #1
        sta BT,y
        lda tmp+5
        sta BX,y
        lda tmp+4
        sta BY,y
        lda #FX_EBUL
        jmp sfx

bul_update:
        jsr shipbox
        ldx #2
@l:     lda BT,x
        beq @n
        lda BY,x
        clc
        adc p_bsp
        sta BY,x
        cmp #Y_EARTH
        bcc @c
        lda #0
        sta BT,x
        beq @n
@c:     lda pst
        bne @n
        lda BX,x
        sta tmp+0
        clc
        adc #1
        sta tmp+1
        lda BY,x
        sta tmp+2
        clc
        adc #3
        sta tmp+3
        jsr boxhit
        bcc @n
        lda #0
        sta BT,x
        stx cur
        jsr kill_ship
        ldx cur
@n:     dex
        bpl @l
        rts

; ---------------------------------------------------------------
; ICBM (P0 cuerpo, P1 bandas y llama) y cabezas MIRV
icbm_update:
        lda pclear          ; operación superada: el ICBM desaparece
        beq @np
        lda ist
        beq @np
        jmp icbm_end
@np:    lda ist
        bne @act
        lda pclear
        bne @r
        lda ictm
        bne @d
        dec ictm+1
@d:     dec ictm
        lda ictm
        ora ictm+1
        bne @r
        ; sale un ICBM
        lda RANDOM
        and #127
        clc
        adc #64
        sta ix
        lda #32
        sta iy
        lda #0
        sta iyf
        sta ifl
        ldx dif
        lda IHP_D,x
        sta ihp
        lda #1
        sta ist
        lda #64
        sta klax
        lda #M_ICBM
        jmp msg
@r:     rts
@act:   cmp #3
        bne @a1
        dec ibt             ; estallando
        bne @r
        jmp icbm_end
@a1:    lda ifl
        beq @fl
        dec ifl
@fl:    lda iyf             ; cae
        clc
        adc p_ivy
        sta iyf
        lda iy
        adc #0
        sta iy
        lda ist
        cmp #2
        beq @mirv
        ; entero: ¿se divide?
        lda p_mirv
        beq @nd
        lda iy
        cmp #110
        bcc @nd
        lda #2
        sta ist
        lda #1
        sta HS
        sta HS+1
        sta HPL+1
        lda #0
        sta HPL
        sta HS+2
        lda p_mirv          ; tres cabezas: la del centro va en un player de los cazadores que esté libre
        cmp #2
        bcc @c2
        ldy #0
        lda DS
        beq @c3
        iny
        lda DS+1
        bne @c2
@c3:    tya
        clc
        adc #2
        sta HPL+2
        lda #1
        sta HS+2
        lda ix
        clc
        adc #2
        sta HX+2
@c2:    lda ix
        sta HX
        sta HX+1
        lda #0
        sta HXF
        sta HXF+1
        lda #FX_MIRV
        jsr sfx
        lda #M_MIRV
        jmp msg
@nd:    lda iy
        clc
        adc #ICBM_H
        cmp #Y_EARTH
        bcc @r2
        jsr impact
        jmp icbm_end
@r2:    rts
@mirv:  ; las cabezas de los lados se separan (sin salir de la pantalla)
        lda HX
        cmp #52
        bcc @ml
        lda HXF
        sec
        sbc #$60
        sta HXF
        lda HX
        sbc #0
        sta HX
@ml:    lda HX+1
        cmp #196
        bcs @mr
        lda HXF+1
        clc
        adc #$60
        sta HXF+1
        lda HX+1
        adc #0
        sta HX+1
@mr:    ldx #2
@h:     lda HS,x
        cmp #2
        bne @h1
        dec HB,x
        bne @h2
        lda #0
        sta HS,x
        beq @h2
@h1:    cmp #1
        bne @h2
        lda iy
        clc
        adc #MIRV_H
        cmp #Y_EARTH
        bcc @h2
        lda #0
        sta HS,x
        jsr impact
@h2:    dex
        bpl @h
        lda HS
        ora HS+1
        ora HS+2
        bne @r3
        jmp icbm_end
@r3:    rts

icbm_end:
        lda #0
        sta ist
        sta HS
        sta HS+1
        sta HS+2
        lda p_ici
        sta ictm
        lda p_ici+1
        sta ictm+1
        rts

; un ICBM (o una cabeza) llega a la Tierra
impact: inc impacts
        lda #1
        sta hudd
        lda #24
        sta eflash
        lda #FX_IMPACT
        jsr sfx
        lda #FX_THUMP
        jsr sfx
        lda impacts
        cmp #3
        bcc @m
        lda cheat
        bne @m
        lda #1
        sta gover
@m:     lda #M_IMP
        jmp msg

; ¿el disparo da al ICBM o a una cabeza?
hit_icbm:
        lda ist
        beq @no
        cmp #3
        beq @no
        lda shotx
        sta tmp+0
        clc
        adc #1
        sta tmp+1
        lda shoty
        sta tmp+2
        clc
        adc #5
        sta tmp+3
        lda iy
        sta tmp+6
        lda ist
        cmp #2
        beq @hd
        lda ix
        sta tmp+4
        clc
        adc #7
        sta tmp+5
        lda iy
        clc
        adc #ICBM_H-1
        sta tmp+7
        jsr boxhit
        bcc @no
        lda #6
        sta ifl
        dec ihp
        bne @ht
        lda #3              ; destruido
        sta ist
        lda #30
        sta ibt
        lda #FX_BURST
        jsr sfx
        lda #FX_THUMP
        jsr sfx
        lda #$00            ; 500
        ldx #$05
        jsr score_add
        sec
        rts
@ht:    lda #FX_HIT
        jsr sfx
        sec
        rts
@no:    clc
        rts
@hd:    lda iy
        clc
        adc #MIRV_H-1
        sta tmp+7
        ldx #2
@hl:    lda HS,x
        cmp #1
        bne @hn
        lda HX,x
        sta tmp+4
        clc
        adc #3
        sta tmp+5
        jsr boxhit
        bcc @hn
        lda #2
        sta HS,x
        lda #24
        sta HB,x
        lda #FX_EXPL
        jsr sfx
        lda #$00            ; 300
        ldx #$03
        jsr score_add
        sec
        rts
@hn:    dex
        bpl @hl
        clc
        rts

; destello de la Tierra y centelleo de las estrellas
fx_update:
        lda eflash
        beq @s
        dec eflash
        lda eflash
        and #4
        beq @o
        lda #$0E
        sta DTBK+20
        sta DTBK+21
        bne @s
@o:     lda TABBK+20
        sta DTBK+20
        lda TABBK+21
        sta DTBK+21
@s:     lda frame
        and #7
        bne @r
        ldx #17
@t:     lda TWINK,x
        clc
        adc frame
        and #7
        tay
        lda TWC,y
        sta DTPF2,x
        dex
        cpx #7
        bcs @t
        ldx #2
@t2:    lda TWINK,x
        clc
        adc frame
        and #7
        tay
        lda TWC,y
        sta DTPF2,x
        dex
        bpl @t2
@r:     rts
TWINK:  .byte 0,3,6,0,0,0,0,1,4,7,2,5,0,3,6,1,4,7
TWC:    .byte $02,$06,$0A,$0E,$0E,$0A,$06,$04

; ---------------------------------------------------------------
; DIBUJO del cuadro siguiente
f_render:
        jsr pm_begin
        ; cazadores en picado
        ldx #1
@d:     lda DS,x
        beq @dn
        stx cur
        txa
        asl a
        ora rb
        tay
        lda DXH,x
        sta PHP2,y
        lda #$36
        sta PCP2,y
        lda DS,x
        cmp #3
        bne @dp
        lda DT,x            ; estallando
        lsr a
        lsr a
        lsr a
        eor #3
        cmp #3
        bcc @df
        lda #2
@df:    asl a
        asl a
        asl a
        clc
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        lda #$1C
        sta PCP2,y
        jmp @dd
@dp:    lda #<DIVE_P
        sta src
        lda #>DIVE_P
        sta src+1
@dd:    lda DYH,x
        pha
        txa
        clc
        adc #2
        tax
        pla
        ldy #8
        jsr pm_spr
        ldx cur
@dn:    dex
        bpl @d
        ; ICBM
        ldx rb
        lda ist
        bne @i
        jmp @shot
@i:     cmp #1
        bne @i2
        lda ix
        sta PHP0,x
        sta PHP1,x
        lda #$08
        ldy ifl
        beq @ic
        lda #$0E
@ic:    sta PCP0,x
        lda #$36
        sta PCP1,x
        lda #<ICBM_P0
        sta src
        lda #>ICBM_P0
        sta src+1
        ldx #0
        lda iy
        ldy #ICBM_H
        jsr pm_spr
        lda #<ICBM_P1
        sta src
        lda #>ICBM_P1
        sta src+1
        ldx #1
        lda iy
        ldy #ICBM_H
        jsr pm_spr
        jmp @shot
@i2:    cmp #3
        bne @i3
        lda ix              ; estallando
        sta PHP0,x
        lda #$1C
        sta PCP0,x
        lda ibt
        lsr a
        lsr a
        lsr a
        eor #3
        cmp #3
        bcc @if
        lda #2
@if:    asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        ldx #0
        lda iy
        clc
        adc #6
        ldy #8
        jsr pm_spr
        jmp @shot
@i3:    ; cabezas MIRV
        ldx #2
@h:     lda HS,x
        beq @hn
        stx cur
        lda HPL,x
        asl a
        ora rb
        tay
        lda HX,x
        sta PHP0,y
        lda #$0C
        sta PCP0,y
        lda #<MIRV_P
        sta src
        lda #>MIRV_P
        sta src+1
        lda #MIRV_H
        sta tmp+2
        lda HS,x
        cmp #2
        bne @hp
        lda #$1C
        sta PCP0,y
        lda HB,x
        lsr a
        lsr a
        lsr a
        cmp #3
        bcc @hf
        lda #2
@hf:    eor #2
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        lda #8
        sta tmp+2
@hp:    lda HPL,x
        tax
        lda iy
        ldy tmp+2
        jsr pm_spr          ; X = el player de la cabeza
        ldx cur
@hn:    dex
        bpl @h
@shot:  ; disparo (M0) y balas (M1-M3)
        lda shoty
        beq @nb
        ldx rb
        lda shotx
        sta PHM0,x
        ldx #0
        lda shoty
        ldy #6
        jsr pm_mis
@nb:    ldx #2
@b:     lda BT,x
        beq @bn
        stx cur
        txa
        clc
        adc #1
        tax
        asl a
        ora rb
        tay
        stx tmp+2
        ldx cur
        lda BX,x
        sta PHM0,y
        lda BY,x
        ldx tmp+2
        ldy #4
        jsr pm_mis
        ldx cur
@bn:    dex
        bpl @b
        jsr car_freeze
        jmp pm_end

; ---------------------------------------------------------------
;        0 disp 1 expl 2 golpe 3 estal 4 muerte 5 picado 6 impacto 7 beep 8 bala 9 vida 10 golpeG 11 muerte2 12 mirv 13 klax1 14 klax2
SX_CH:  .byte 0,   1,   0,   1,   1,   2,   2,   3,   2,   3,   2,   2,   3,   3,   3
SX_F:   .byte $06, $14, $08, $30, $20, $0C, $50, $20, $20, $40, $40, $20, $10, $1C, $28
SX_S:   .byte 3,   2,   2,   1,   1,   1,   1,   $FF, 2,   $FD, 3,   2,   4,   0,   0
SX_V:   .byte 12,  15,  14,  15,  15,  8,   15,  10,  6,   12,  15,  15,  12,  12,  12
SX_D:   .byte 14,  50,  10,  80,  130, 50,  120, 30,  8,   24,  26,  72,  30,  8,   8
SX_C:   .byte $A0, $80, $A0, $80, $80, $A0, $80, $A0, $A0, $A0, $C0, $C0, $A0, $C0, $C0
SX_P:   .byte 2,   3,   3,   4,   5,   1,   5,   4,   1,   4,   3,   5,   3,   3,   3
SX_K:   .byte 1,   3,   0,   7,   7,   7,   7,   7,   1,   7,   1,   3,   3,   0,   0
