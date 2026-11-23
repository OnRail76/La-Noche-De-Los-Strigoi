; ---------------------------------------------------------------
; MOTOR · ejemplo mínimo (banco de pruebas del motor común)
; Pantalla de texto -> FIRE -> un carril con bloques que se desliza, un player que se mueve
; con la palanca y dispara un misil hacia arriba; cada bloque destruido suma 10 puntos.
; Sirve para comprobar el motor sin ningún juego encima:  ./build.sh  y  run8 ejemplo.xex
; ---------------------------------------------------------------
        .include "hw.inc"

PMA     = $8000
PMB     = $8800
PMY0    = 32
PMN     = 192
SCR     = $9000             ; filas fijas
RING    = $9400             ; anillo del carril (128 bytes, alineado a 128)
DLGAME  = $9600
DLTEXT  = $9680
TSCR    = $9780
HUD     = $9700
NCAR    = 1
CAR_K   = 13                ; medido en SDI '86 con esta misma display list (ANTIC 4 + HSCROL)
CAR_NROWS = 1
EXTRA_STEP = $05

        .segment "ZEROPAGE"
gmode:  .res 1
px:     .res 1
py:     .res 1
shx:    .res 1
shy:    .res 1

        .segment "HIBSS"
dummy:  .res 1

        .segment "INITSEG"
        lda PORTB
        ora #$02
        sta PORTB
        rts

        .segment "CODE"
; juego de caracteres propio (1 KB alineado): 0 vacío, 1 bloque PF0, 2 bloque PF1 con borde PF2
CHARSET:
        .res 8, 0
        .byte $55,$55,$55,$55,$55,$55,$55,$00
        .byte $FF,$AB,$AB,$AB,$AB,$AB,$FF,$00
        .res 1024-24, 0

        .include "motor/nucleo.s"
        .include "motor/pmg.s"
        .include "motor/dli.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/carril.s"
        .include "motor/pantalla.s"

; texto en códigos internos de ANTIC (fuente de la ROM)
.macro TXT s
        .repeat .strlen(s), I
        .byte .strat(s, I) - 32
        .endrepeat
        .res 20 - .strlen(s), 0
.endmacro

start:  jsr m_init
        lda #<m_dli
        sta VDSLST
        lda #>m_dli
        sta VDSLST+1
        lda #0
        sta gmode
        sta hisc
        sta hisc+1
        sta hisc+2
title:  lda #0
        sta gmode
        lda #$E0            ; fuente de la ROM para el texto
        sta CHBAS
        lda #<DESC
        sta ptr
        lda #>DESC
        sta ptr+1
        jsr txt_build
        lda #$0E
        sta COLOR0
        lda #$9A
        sta COLOR1
        lda #$36
        sta COLOR2
        lda #0
        sta COLOR4
        jsr txt_show
        lda #1
        sta fireold
@w:     jsr m_wait
        jsr m_mando
        lda fireed
        beq @w
        jmp game

DESC:   .byte $70,$70,$70,$70,$70
        .byte 7, <T1, >T1
        .byte $70,$70
        .byte 6, <T2, >T2
        .byte $FF
T1:     TXT "  MOTOR COMUN"
T2:     TXT "    PULSA FIRE"

; ---------------------------------------------------------------
game:   lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        jsr m_wait
        ; display list
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
        ; filas fijas vacías, marcador
        lda #<SCR
        sta dst
        lda #>SCR
        sta dst+1
        lda #0
        ldx #160
        jsr m_fill
        lda #<HUD
        sta dst
        lda #>HUD
        sta dst+1
        lda #0
        ldx #40
        jsr m_fill
        ; carril: bloques cada 5 columnas
        lda #<RING
        sta dst
        lda #>RING
        sta dst+1
        ldy #0
@r:     tya
        ldx #0
@m:     cmp #5
        bcc @k
        sbc #5
        bcs @m
@k:     tax
        lda BLK,x
        jsr car_put
        iny
        cpy #64
        bne @r
        ; carril a 0,75 relojes por cuadro hacia la izquierda
        lda #$C0
        sta car_sl
        lda #0
        sta car_sh
        sta car_dir
        sta score
        sta score+1
        sta score+2
        ; colores por fila (entrada 0 = fila 0 del campo; 4 = marcador de abajo)
        ldx #4
@t:     lda TBK,x
        sta DTBK,x
        lda TP0,x
        sta DTPF0,x
        lda TP1,x
        sta DTPF1,x
        lda TP2,x
        sta DTPF2,x
        lda #0
        sta DTHS,x
        dex
        bpl @t
        jsr pm_init
        lda #>CHARSET
        sta CHBAS
        lda #0
        sta COLOR4
        sta COLOR2
        lda #$0E
        sta COLOR1
        lda #$1E
        sta COLOR3
        lda #$11
        sta GPRIOR
        lda #120
        sta px
        lda #180
        sta py
        lda #0
        sta shy
        lda #<DLGAME
        sta SDLSTL
        lda #>DLGAME
        sta SDLSTH
        lda #3
        sta GRACTL
        lda #1
        sta gmode
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        jsr m_wait
        lda #$C0
        sta NMIEN
; bucle: lógica -> dibujo en el búfer oculto -> pm_end
loop:   jsr pm_wait
        jsr m_mando
        lda stk
        and #J_LEFT
        beq @nl
        dec px
@nl:    lda stk
        and #J_RIGHT
        beq @nr
        inc px
@nr:    lda fire
        beq @nf
        lda shy
        bne @nf
        lda px
        clc
        adc #3
        sta shx
        lda py
        sta shy
        lda #0
        jsr sfx
@nf:    ldx #0
        jsr car_move
        ; disparo: sube; al llegar a la fila del carril mira el anillo
        lda shy
        beq @ns
        sec
        sbc #5
        sta shy
        cmp #40
        bcs @in
        lda #0
        sta shy
        beq @ns
@in:    cmp #48
        bcs @ns
        lda shx
        sec
        sbc #48
        ldx #0
        jsr car_col
        tay
        lda #<RING
        sta dst
        lda #>RING
        sta dst+1
        lda (dst),y
        beq @ns
        lda #0
        jsr car_put
        sta shy
        lda #1
        jsr sfx
        lda #$10
        ldx #0
        jsr addsc
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(HUD+2)
        sta dst
        lda #>(HUD+2)
        sta dst+1
        lda #16             ; '0' en códigos internos de la ROM
        jsr put6
@ns:    ; dibujo
        jsr pm_begin
        ldx rb
        lda px
        sta PHP0,x
        lda #$0C
        sta PCP0,x
        lda #<SPR
        sta src
        lda #>SPR
        sta src+1
        ldx #0
        lda py
        ldy #8
        jsr pm_spr
        lda shy
        beq @d
        ldx rb
        lda shx
        sta PHM0,x
        ldx #0
        lda shy
        ldy #6
        jsr pm_mis
@d:     jsr car_freeze
        jsr pm_end
        jmp loop

vbi_juego:
        lda gmode
        bne @g
        rts
@g:     jsr pm_vbi
        jsr car_vbi
        lda #0
        sta dlin
        lda car_hs
        ldx #4
@h:     sta DTHS,x
        dex
        bpl @h
        sta HSCROL
        rts

BLK:    .byte 1, 1, 2, 0, 0
SPR:    .byte $18,$18,$3C,$7E,$FF,$FF,$7E,$24
TBK:    .byte $92,$80,$80,$80,$00
TP0:    .byte $C8,$00,$00,$00,$00
TP1:    .byte $0E,$00,$00,$00,$0C
TP2:    .byte $34,$00,$00,$00,$00

; marcador ANTIC 2, fila 0 de carril, 3 filas fijas ANTIC 4 y marcador
DLTPL:  .byte $70,$70,$70
        .byte $C2
        .word HUD
        .byte $D4
        .word RING          ; LMS en DLTPL+7: CROW_DL
        .byte $C4
        .word SCR
        .byte $C4
        .word SCR+40
        .byte $C4
        .word SCR+80
        .byte $42
        .word HUD
        .byte $41
        .word DLGAME
DLLEN = * - DLTPL
CROW_DL:   .byte 7
CROW_RL:   .byte <RING
CROW_RH:   .byte >RING
CROW_LANE: .byte 0

; efectos: disparo, golpe
SX_CH:  .byte 0, 1
SX_F:   .byte $10, $30
SX_S:   .byte 1, 1
SX_V:   .byte 8, 14
SX_D:   .byte 12, 30
SX_C:   .byte $A0, $80
SX_P:   .byte 1, 2
SX_K:   .byte 1, 3
