; ---------------------------------------------------------------
; SDI '86 · PROTOCOLO FINAL · Atari 8 bits (NTSC) · 2026 - Tony C. Ware
; PROGRAMA 3 · OPERACIÓN ESTACIÓN ORBITAL (la nave nodriza de Phoenix)
;
; Pantalla (la display list se rehace en la VBI cuando la estación baja):
;   marcador · k líneas en blanco · CUERPO de la estación (ANTIC E, 32 líneas)
;   · CINTA de blindaje (ANTIC 4, gira y se agujerea) · fila de CAÑONES (ANTIC 4)
;   · (40 - k) líneas en blanco · 9 filas de estrellas · CENTINELA-4 en su carril · marcador
; P1-P3 las escoltas · P0 las explosiones del final · M0 el disparo · M1-M3 las balas enemigas.
; Objetivo: abrir un hueco en la cinta y destruir el NÚCLEO.
; ---------------------------------------------------------------
        .include "hw.inc"
        .include "blk.inc"
FASE    = 3
MUSICA  = 1
MUS_TITULO   = 0
MUS_SUPERADA = 1
MUS_GAMEOVER = 2

; --------------------------------------------------------------- memoria
PMA     = $A000
PMB     = $A800
PMY0    = 32
PMN     = 192
BODY    = $B000             ; 32 x 40 (ANTIC E)
BELTROW = $B500             ; 40
CANROW  = $B528             ; 40
STARROW = $B580             ; 9 x 40
RP0     = $B700             ; nave: 2 anillos
RP1     = $B780
DLGAME  = $B800
DLTEXT  = $B880
HUDT    = $B900
HUDB    = $B928
TSCR    = $B980

NCAR    = 1                 ; carril 0: la nave
CAR_K   = 13
CAR_NROWS = 2
EXTRA_STEP = $06
KMAX    = 40                ; lo que baja la estación
Y_SHIP  = 207
SHOT_Y0 = 202
SHIPPOS = car_pos           ; la nave es el carril 0

FX_SHOT   = 0
FX_EXPL   = 1
FX_HIT    = 2
FX_BURST  = 3
FX_DEATH  = 4
FX_SWOOP  = 5
FX_BIG    = 6
FX_BEEP   = 7
FX_EBUL   = 8
FX_EXTRA  = 9
FX_THUMP  = 10
FX_DEATH2 = 11
FX_CHIP   = 12
FX_KLAX1  = 13
FX_KLAX2  = 14

; ---------------------------------------------------------------
        .segment "ZEROPAGE"
shipx:  .res 1
pst:    .res 1
ptm:    .res 1
invt:   .res 1
shoty:  .res 1
shotx:  .res 1
sk:     .res 1              ; líneas que ha bajado la estación
stop:   .res 1              ; línea PMG de arriba de la estación
dirty:  .res 1              ; 1 = rehacer la display list en la VBI
nhp:    .res 1              ; vida del núcleo
nfl:    .res 1
boom:   .res 1              ; final: cuadros que quedan de explosiones
cur:    .res 1
ncan:   .res 1              ; cañones que quedan

        .segment "HIBSS"
BELT:   .res 22
CHP:    .res 4              ; vida de los cañones
CFL:    .res 4
ES:     .res 3              ; escoltas: 0 esperando · 1 volando · 2 estallando
EX:     .res 3
EY:     .res 3
EBH:    .res 3              ; línea base (8.8)
EBL:    .res 3
ET:     .res 3
EVX:    .res 3
ETM:    .res 3
BT:     .res 3
BX:     .res 3
BY:     .res 3
bmx:    .res 1
bmy:    .res 1
bmt:    .res 1
dtm:    .res 1
cftm:   .res 1
brtm:   .res 1
CROW_DL: .res 2             ; dónde están los LMS del carril (cambia al rehacer la display list)
p_desc: .res 1
p_cfi:  .res 1
p_brot: .res 1
p_nesc: .res 1
p_edl:  .res 1
p_bsp:  .res 1

        .segment "CODE"
        .include "data3.s"
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
f_vbi:  lda dirty
        beq @c
        jsr dl_build
        lda #0
        sta dirty
@c:     jsr car_vbi
        lda #0
        sta dlin
        lda car_hs
        sta DTHS+4
        sta DTHS+5
        sta DTHS+6
        rts

; display list según sk (en la VBI: solo X, Y y vt)
dl_build:
        ldy #0
        ldx #0
@h:     lda DLHEAD,x
        sta DLGAME,y
        iny
        inx
        cpx #6
        bne @h
        lda sk
        jsr @blank
        ldx #0
@b:     lda DLBODY,x
        sta DLGAME,y
        iny
        inx
        cpx #DLBODY_LEN
        bne @b
        lda #KMAX
        sec
        sbc sk
        jsr @blank
        ldx #0
@s:     lda DLSTAR,x
        sta DLGAME,y
        iny
        inx
        cpx #DLSTAR_LEN
        bne @s
        tya
        clc
        adc #1
        sta CROW_DL
        adc #3
        sta CROW_DL+1
        ldx #0
@t:     lda DLTAIL,x
        sta DLGAME,y
        iny
        inx
        cpx #DLTAIL_LEN
        bne @t
        rts
; A líneas en blanco
@blank: sta vt
@bl:    lda vt
        beq @br
        cmp #8
        bcc @bs
        lda #$70
        sta DLGAME,y
        iny
        lda vt
        sec
        sbc #8
        sta vt
        jmp @bl
@bs:    sec
        sbc #1
        asl a
        asl a
        asl a
        asl a
        sta DLGAME,y
        iny
@br:    rts

DLHEAD: .byte $70,$70,$70,$C2,<HUDT,>HUDT
DLBODY: .byte $4E,<BODY,>BODY
        .repeat 30
        .byte $0E
        .endrepeat
        .byte $8E                           ; última línea del cuerpo: DLI (cinta)
        .byte $C4,<BELTROW,>BELTROW         ; cinta: DLI (cañones)
        .byte $C4,<CANROW,>CANROW           ; cañones: DLI (estrellas)
DLBODY_LEN = * - DLBODY
DLSTAR: .byte $44,<STARROW,>STARROW
        .repeat 7
        .byte $04
        .endrepeat
        .byte $84                           ; última fila de estrellas: DLI (carril)
DLSTAR_LEN = * - DLSTAR
DLTAIL: .byte $D4,<RP0,>RP0,$D4,<RP1,>RP1,$00,$42,<HUDB,>HUDB,$41,<DLGAME,>DLGAME   ; (una línea en blanco: el color cambia sin verse)
DLTAIL_LEN = * - DLTAIL

CROW_RL:   .byte <RP0, <RP1
CROW_RH:   .byte >RP0, >RP1
CROW_LANE: .byte 0, 0

; ---------------------------------------------------------------
f_screen:
        jsr scr_off
        jsr body_copy
        lda #<STARS_INIT
        sta src
        lda #>STARS_INIT
        sta src+1
        lda #<STARROW
        sta dst
        lda #>STARROW
        sta dst+1
        ldx #180
        jsr m_copy
        lda #<(STARS_INIT+180)
        sta src
        lda #>(STARS_INIT+180)
        sta src+1
        lda #<(STARROW+180)
        sta dst
        lda #>(STARROW+180)
        sta dst+1
        ldx #180
        jsr m_copy
        lda #0
        tax
@r:     sta RP0,x
        inx
        bne @r
        ldx #79
@c:     sta BELTROW,x
        dex
        bpl @c
        jsr pm_init
        ldx #7
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
        sta sk
        jsr dl_build
        jmp scr_on

body_copy:
        lda #<BODY_BM
        sta src
        lda #>BODY_BM
        sta src+1
        lda #<BODY
        sta dst
        lda #>BODY
        sta dst+1
        ldx #5
@p:     ldy #0
@b:     lda (src),y
        sta (dst),y
        iny
        bne @b
        inc src+1
        inc dst+1
        dex
        bne @p
        rts

; entradas de la DLI: 0 cuerpo · 1 cinta · 2 cañones · 3 estrellas · 4-5 nave · 6 marcador
TABBK:  .byte $00,$00,$00,$00,$00,$00,$00,$00
TABP0:  .byte $08,$06,$08,$00,$0E,$0E,$00,$00
TABP1:  .byte $96,$84,$26,$00,$96,$96,$0C,$00
TABP2:  .byte $46,$0C,$1E,$0A,$9E,$9E,$00,$00

; ---------------------------------------------------------------
f_start:
        jsr body_copy
        lda #40
        sta stop
        lda #0
        sta sk
        sta boom
        sta shoty
        sta nfl
        sta bmt
        sta BT
        sta BT+1
        sta BT+2
        lda #1
        sta dirty
        ldx #21             ; cinta entera, eslabones alternos
@b:     txa
        and #1
        tay
        lda BELTC,y
        sta BELT,x
        dex
        bpl @b
        jsr belt_draw
        ldx dif
        lda CHP_D,x
        ldx #3
@c:     sta CHP,x
        pha
        lda #0
        sta CFL,x
        jsr can_draw
        pla
        dex
        bpl @c
        lda #4
        sta ncan
        lda loopn           ; vida de la estación: 16 + 6 por vuelta (tope 50)
        asl a
        sta nhp
        asl a
        clc
        adc nhp
        adc #16
        cmp #51
        bcc @n
        lda #50
@n:     sta nhp
        jsr params
        ldx #2
@e:     lda #0
        sta ES,x
        lda ESD,x
        sta ETM,x
        dex
        bpl @e
        lda p_desc
        sta dtm
        lda #90
        sta cftm
        lda p_brot
        sta brtm
        jmp ship_reset
BELTC:  .byte CH_CA, CH_CB
CHP_D:  .byte 2, 3, 4
ESD:    .byte 60, 140, 220

params: lda loopn
        cmp #5
        bcc @l
        lda #5
@l:     sta tmp
        asl a
        asl a
        asl a
        asl a
        sta tmp+1           ; x16
        lda #110            ; bajada: 1 línea cada 110 - 16 x vuelta cuadros (mínimo 40)
        sec
        sbc tmp+1
        cmp #40
        bcs @d
        lda #40
@d:     sta p_desc
        lda #100            ; cañones
        sec
        sbc tmp+1
        ldx dif
        clc
        adc DIF_CF,x
        cmp #36
        bcs @c
        lda #36
@c:     sta p_cfi
        lda #10             ; cinta: un paso cada 10 cuadros (6 desde la vuelta 2)
        ldx loopn
        beq @r
        lda #6
@r:     sta p_brot
        lda #2              ; escoltas: 2 en FÁCIL, 3 si no
        ldx dif
        beq @e
        lda #3
@e:     sta p_nesc
        lda tmp             ; bajada de las escoltas (8.8)
        asl a
        asl a
        asl a
        asl a
        adc #$30
        sta p_edl
        lda #2
        ldx dif
        cpx #2
        beq @b3
        ldx tmp
        cpx #2
        bcc @b
@b3:    lda #3
@b:     sta p_bsp
        rts
DIF_CF: .byte 30, 0, 236

; ---------------------------------------------------------------
f_frame:
        jsr ship_update
        jsr shot_update
        jsr st_update
        jsr esc_update
        jsr can_fire
        jsr bul_update
        jmp end_update

f_status:
        lda nhp
        ldx #HUD_NU
        jsr st_dec2
        lda ncan
        clc
        adc #DIG0
        sta HUDB+HUD_CN
        rts

        .include "centinela.s"

; ---------------------------------------------------------------
; LA ESTACIÓN: baja, gira la cinta, destellos
st_update:
        lda sk
        clc
        adc #40
        sta stop
        lda boom
        bne @r
        dec dtm
        bne @nb
        lda p_desc
        sta dtm
        lda sk
        cmp #KMAX
        bcs @nb
        inc sk
        lda #1
        sta dirty
        lda sk
        cmp #1
        bne @nb
        lda #M_BAJA
        jsr msg
@nb:    dec brtm
        bne @fl
        lda p_brot
        sta brtm
        lda loopn           ; vueltas pares a la izquierda, impares a la derecha
        and #1
        bne @rr
        lda BELT            ; gira a la izquierda
        pha
        ldx #0
@l:     lda BELT+1,x
        sta BELT,x
        inx
        cpx #21
        bne @l
        pla
        sta BELT+21
        jmp @dr
@rr:    lda BELT+21
        pha
        ldx #21
@l2:    lda BELT-1,x
        sta BELT,x
        dex
        bne @l2
        pla
        sta BELT
@dr:    jsr belt_draw
@fl:    lda nfl             ; destello del núcleo
        beq @r
        dec nfl
        bne @r
        lda TABP1
        sta DTPF1
        lda TABP2
        sta DTPF2
@r:     rts

belt_draw:
        ldx #21
@l:     lda BELT,x
        sta BELTROW+BELT_C0,x
        dex
        bpl @l
        rts

; X = cañón: dibuja entero o roto
can_draw:
        ldy CAN_COL,x
        lda CHP,x
        beq @r
        lda CANON_C
        sta CANROW,y
        lda CANON_C+1
        sta CANROW+1,y
        rts
@r:     lda CANON_R
        sta CANROW,y
        lda CANON_R+1
        sta CANROW+1,y
        rts

; ---------------------------------------------------------------
; DISPARO del jugador: cañones, cinta, cuerpo y núcleo
shot_update:
        lda shoty
        bne @go
        rts
@go:    sec
        sbc #6
        cmp #34
        bcs @s
@end:   lda #0
        sta shoty
        rts
@s:     sta shoty
        lda boom
        bne @r
        jsr esc_shot
        bcs @r
        lda shotx
        sec
        sbc #48
        sta tmp+2           ; x en el campo
        lsr a
        lsr a
        sta tmp+3           ; columna
        lda shoty
        sec
        sbc stop
        bcc @r              ; por encima de la estación
        cmp #48
        bcs @r              ; por debajo
        cmp #40
        bcs @can
        cmp #32
        bcs @belt
        ; cuerpo: ¿núcleo?
        sta tmp+4
        cmp #NUC_Y0
        bcc @px
        cmp #NUC_Y1
        bcs @px
        lda tmp+2
        cmp #NUC_X0
        bcc @px
        cmp #NUC_X1
        bcs @px
        jsr core_hit
        jmp @end
@px:    jsr body_px      ; casco: bajo la cinta (por un hueco) se resiente; fuera de la cinta, no
        beq @r
        lda tmp+3
        sec
        sbc #BELT_C0
        cmp #22
        bcs @end
        jsr core_hit
        jmp @end
@r:     rts
@can:   ldx #3
@cl:    lda tmp+3
        sec
        sbc CAN_COL,x
        cmp #2
        bcc @ch
        dex
        bpl @cl
        rts
@ch:    lda CHP,x
        beq @r2
        dec CHP,x
        lda #6
        sta CFL,x
        lda CHP,x
        bne @ch1
        jsr can_draw
        dec ncan
        lda #1
        sta hudd
        lda #FX_EXPL
        jsr sfx
        lda #$00            ; 200
        ldx #$02
        jsr score_add
        jmp @end
@ch1:   lda #FX_HIT
        jsr sfx
        jmp @end
@r2:    rts
@belt:  lda tmp+3
        sec
        sbc #BELT_C0
        cmp #22
        bcs @r2
        tax
        lda BELT,x
        beq @r2             ; hueco: sigue subiendo
        cmp #CH_CD
        beq @b0
        lda #CH_CD
        bne @bs
@b0:    lda #0
@bs:    sta BELT,x
        jsr belt_draw
        lda #FX_CHIP
        jsr sfx
        lda #$10
        ldx #$00
        jsr score_add
        jmp @end

; píxel del cuerpo en x = tmp+2, línea tmp+4: Z = 0 si hay casco
body_px:
        lda tmp+4
        sta dst
        lda #0
        sta dst+1
        asl dst
        rol dst+1
        asl dst
        rol dst+1
        lda dst
        clc
        adc tmp+4
        sta dst
        bcc @a
        inc dst+1
@a:     asl dst
        rol dst+1
        asl dst
        rol dst+1
        asl dst
        rol dst+1           ; x 40
        lda tmp+3
        clc
        adc dst
        adc #<BODY
        sta dst
        lda dst+1
        adc #>BODY
        sta dst+1
        lda tmp+2
        and #3
        tax
        ldy #0
        lda (dst),y
        and PXM,x
        rts
PXM:    .byte $C0, $30, $0C, $03

core_hit:
        lda #$0E            ; destello
        sta DTPF2
        lda #$0C
        sta DTPF1
        lda #8
        sta nfl
        lda #FX_HIT
        jsr sfx
        lda #$50
        ldx #$00
        jsr score_add
        dec nhp
        lda #1
        sta hudd
        lda nhp
        bne @r
        ; NÚCLEO DESTRUIDO
        lda #180
        sta boom
        lda #FX_BIG
        jsr sfx
        lda #FX_THUMP
        jsr sfx
        lda #$00            ; 2000
        ldx #$20
        jsr score_add
        lda #M_NUC
        jsr msg
@r:     rts

; final: explosiones por toda la estación y la estación desaparece
end_update:
        lda boom
        beq @r
        cmp #1              ; 1: la estación ya no está (se queda así hasta el cambio de fase)
        beq @r
        dec boom
        lda boom
        cmp #1
        bne @n
        jmp phase_done
@n:     lda frame
        and #3
        bne @c
        lda frame           ; el cuerpo parpadea
        and #4
        beq @w
        lda #$0E
        bne @s
@w:     lda TABP2
@s:     sta DTPF2
@c:     dec bmt             ; una explosión nueva cada 12 cuadros
        bpl @a
        lda #11
        sta bmt
        lda RANDOM
        and #127
        adc #64
        sta bmx
        lda RANDOM
        and #31
        adc stop
        sta bmy
        lda #FX_EXPL
        jsr sfx
@a:     lda boom
        cmp #90
        bne @r
        ldx #0              ; a mitad: la estación desaparece
        txa
@z:     sta BODY,x
        sta BODY+$100,x
        sta BODY+$200,x
        sta BODY+$300,x
        sta BODY+$400,x
        inx
        bne @z
        ldx #79
@z2:    sta BELTROW,x
        dex
        bpl @z2
        ldx #21
@z3:    sta BELT,x
        dex
        bpl @z3
        lda #FX_BIG
        jmp sfx
@r:     rts

; ---------------------------------------------------------------
; CAÑONES: disparan hacia abajo
can_fire:
        lda boom
        ora pst
        bne @r
        dec cftm
        bne @r
        lda RANDOM
        and #15
        adc p_cfi
        sta cftm
        lda RANDOM
        and #3
        tax
        ldy #4
@s:     lda CHP,x
        bne @g
        inx
        txa
        and #3
        tax
        dey
        bne @s
@r:     rts
@g:     lda CAN_COL,x
        asl a
        asl a
        adc #48+3
        sta tmp+5
        lda stop
        clc
        adc #47
        sta tmp+4
        lda tmp+5
        ; nueva bala: A = x, tmp+4 = y
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
        cmp #218
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
; ESCOLTAS (P1-P3): salen de la estación, bajan en zigzag y vuelven a subir
esc_update:
        ldx #2
@l:     lda ES,x
        bne @a
        ; esperando
        lda boom
        ora pclear
        beq *+5
        jmp @n
        cpx p_nesc
        bcc *+5
        jmp @n
        dec ETM,x
        beq *+5
        jmp @n
        lda #1
        sta ES,x
        lda RANDOM
        and #63
        adc #96
        sta EX,x
        lda stop
        clc
        adc #48
        sta EBH,x
        lda #0
        sta EBL,x
        sta ET,x
        lda #1
        ldy RANDOM
        bpl @v
        lda #$FF
@v:     sta EVX,x
        lda #FX_SWOOP
        jsr sfx
        jmp @n
@a:     cmp #2
        bne @f
        dec ETM,x           ; estallando
        beq *+5
        jmp @n
        lda #0
        sta ES,x
        lda #120
        sta ETM,x
        jmp @n
@f:     lda boom            ; con el núcleo destruido, todas estallan
        beq @f1
        jsr esc_die
        jmp @n
@f1:    lda EX,x            ; vuelo
        clc
        adc EVX,x
        sta EX,x
        cmp #52
        bcc @bx
        cmp #196
        bcc @y
@bx:    lda EVX,x
        eor #$FF
        clc
        adc #1
        sta EVX,x
@y:     lda EBL,x
        clc
        adc p_edl
        sta EBL,x
        lda EBH,x
        adc #0
        sta EBH,x
        cmp #186
        bcc @y2
        lda stop            ; abajo del todo: vuelve a salir de la estación
        clc
        adc #48
        sta EBH,x
@y2:    inc ET,x
        inc ET,x
        lda ET,x
        lsr a
        lsr a
        and #31
        tay
        lda EBH,x
        clc
        adc ESIN,y
        sta EY,x
        ; dispara de vez en cuando
        lda RANDOM
        and #127
        bne @hs
        lda EY,x
        clc
        adc #8
        sta tmp+4
        lda EX,x
        clc
        adc #3
        stx cur
        jsr bul_new
        ldx cur
@hs:    jsr esc_ship
@n:     dex
        bmi @x
        jmp @l
@x:     rts
; seno de amplitud 16 (32 pasos)
ESIN:   .byte 0,3,6,9,11,13,15,16,16,16,15,13,11,9,6,3
        .byte 0,253,250,247,245,243,241,240,240,240,241,243,245,247,250,253

esc_die:
        lda #2
        sta ES,x
        lda #24
        sta ETM,x
        lda #FX_EXPL
        jmp sfx

esc_ship:
        lda pst
        bne @r
        jsr shipbox
        lda EX,x
        sta tmp+0
        clc
        adc #7
        sta tmp+1
        lda EY,x
        sta tmp+2
        clc
        adc #6
        sta tmp+3
        jsr boxhit
        bcc @r
        stx cur
        jsr kill_ship
        ldx cur
        lda cheat
        bne @r
        jmp esc_die
@r:     rts

; ¿el disparo da a una escolta? (se llama desde shot_update antes que la estación)
esc_shot:
        ldx #2
@l:     lda ES,x
        cmp #1
        bne @n
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
        lda EX,x
        sta tmp+4
        clc
        adc #7
        sta tmp+5
        lda EY,x
        sta tmp+6
        clc
        adc #7
        sta tmp+7
        jsr boxhit
        bcc @n
        jsr esc_die
        lda #$00            ; 100
        ldx #$01
        jsr score_add
        lda #0
        sta shoty
        sec
        rts
@n:     dex
        bpl @l
        clc
        rts

; ---------------------------------------------------------------
f_render:
        jsr pm_begin
        ldx #2
@e:     lda ES,x
        beq @en
        stx cur
        txa
        clc
        adc #1
        asl a
        ora rb
        tay
        lda EX,x
        sta PHP0,y
        lda #$46
        sta PCP0,y
        lda ES,x
        cmp #2
        bne @ep
        lda #$1C
        sta PCP0,y
        lda ETM,x
        lsr a
        lsr a
        lsr a
        cmp #3
        bcc @ef
        lda #2
@ef:    eor #2
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        jmp @ed
@ep:    lda frame
        and #8
        clc
        adc #<ESC_P
        sta src
        lda #>ESC_P
        adc #0
        sta src+1
@ed:    lda EY,x
        pha
        txa
        clc
        adc #1
        tax
        pla
        ldy #8
        jsr pm_spr
        ldx cur
@en:    dex
        bpl @e
        ; explosiones del final (P0)
        lda boom
        cmp #2
        bcc @sh
        ldx rb
        lda bmx
        sta PHP0,x
        lda #$1C
        sta PCP0,x
        lda bmt
        lsr a
        lsr a
        cmp #3
        bcc @bf
        lda #2
@bf:    eor #2
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        ldx #0
        lda bmy
        ldy #8
        jsr pm_spr
@sh:    lda shoty
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
;        0 disp 1 expl 2 golpe 3 estal 4 muerte 5 sale 6 enorme 7 beep 8 bala 9 vida 10 golpeG 11 muerte2 12 cinta 13 klax1 14 klax2
SX_CH:  .byte 0,   1,   0,   1,   1,   2,   2,   3,   2,   3,   2,   2,   0,   3,   3
SX_F:   .byte $06, $14, $08, $30, $20, $0C, $50, $20, $20, $40, $40, $20, $04, $1C, $28
SX_S:   .byte 3,   2,   2,   1,   1,   1,   1,   $FF, 2,   $FD, 3,   2,   1,   0,   0
SX_V:   .byte 12,  15,  14,  15,  15,  8,   15,  10,  6,   12,  15,  15,  9,   12,  12
SX_D:   .byte 14,  50,  10,  80,  130, 40,  150, 30,  8,   24,  26,  72,  5,   8,   8
SX_C:   .byte $A0, $80, $A0, $80, $80, $A0, $80, $A0, $A0, $A0, $C0, $C0, $80, $C0, $C0
SX_P:   .byte 2,   3,   3,   4,   5,   1,   5,   4,   1,   4,   3,   5,   2,   3,   3
SX_K:   .byte 1,   3,   0,   7,   7,   7,   7,   7,   1,   7,   1,   3,   0,   0,   0
