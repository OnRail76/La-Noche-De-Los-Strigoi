; ---------------------------------------------------------------
; SDI '86 · PROTOCOLO FINAL · Atari 8 bits (NTSC) · 2026 - Tony C. Ware
; PROGRAMA 5 · JANUS (Phoenix + los jefes de pared del primer Contra)
;
; Pantalla: marcador · la PARED de JANUS (ANTIC E, 40 líneas: armarios y la gran lente)
;   · dos CINTAS de coraza (ANTIC 4) que giran en sentidos contrarios y se agujerean
;   · fila de 4 EMISORES láser · 12 filas de sala (por ellas baja el rayo) · 2 filas de suelo · marcador
; El agente (P0 uniforme, P1 piel) va a pie por el suelo: dispara hacia arriba (M0-M1),
; se agacha (abajo) para que las BOLAS (P2-P3) le pasen por encima y se aparta del rayo.
; La lente dispara (M2-M3). Objetivo: abrir hueco en las dos cintas y destruir el NÚCLEO.
; ---------------------------------------------------------------
        .include "hw.inc"
        .include "blk.inc"
FASE    = 5
MUSICA  = 1
MUS_TITULO   = 0
MUS_SUPERADA = 1
MUS_GAMEOVER = 2

PMA     = $A000
PMB     = $A800
PMY0    = 32
PMN     = 192
WALL    = $B000             ; 40 x 40 (ANTIC E)
SCR     = $B680             ; 17 filas x 40: cinta A, cinta B, emisores, 12 de sala, 2 de suelo
DLGAME  = $B940
DLTEXT  = $B9C0
HUDT    = $BA40
HUDB    = $BA68
TSCR    = $BA90
EXTRA_STEP = $06

BELTA   = SCR+2             ; las cintas ocupan las columnas 2-37
BELTB   = SCR+40+2
EMIROW  = SCR+80
AIR0    = SCR+120
NBELT   = 36
AY      = 184               ; el agente, de pie en el suelo
AXMIN   = 48+8
AXMAX   = 48+144
BALL_Y  = 180
WALL_Y1 = 80                ; primera línea por debajo de la pared

FX_SHOT   = 0
FX_EXPL   = 1
FX_HIT    = 2
FX_BURST  = 3
FX_DEATH  = 4
FX_ALERT  = 5
FX_BIG    = 6
FX_BEEP   = 7
FX_EBUL   = 8
FX_EXTRA  = 9
FX_THUMP  = 10
FX_DEATH2 = 11
FX_CHIP   = 12
FX_KLAX1  = 13
FX_KLAX2  = 14
FX_LASER  = 15
FX_BALL   = 16

; ---------------------------------------------------------------
        .segment "ZEROPAGE"
ax:     .res 1
aface:  .res 1
afr:    .res 1
crouch: .res 1
pst:    .res 1
ptm:    .res 1
invt:   .res 1
ftm:    .res 1
nhp:    .res 1              ; vida del núcleo
nemi:   .res 1              ; emisores en pie
boom:   .res 1
bmt:    .res 1
bmx:    .res 1
bmy:    .res 1
hitfl:  .res 1
cur:    .res 1
scp:    .res 2
said:   .res 1              ; frases de JANUS ya dichas (bits)
bcur:   .res 1
amov:   .res 1              ; el agente anda (para el ciclo de pasos)
fpose:  .res 1              ; cuadros con los brazos en alto tras disparar

        .segment "HIBSS"
BA:     .res NBELT          ; cintas (códigos de carácter; 0 = hueco)
BB:     .res NBELT
SXP:    .res 2              ; disparos del agente (y = 0: libre)
SYP:    .res 2
BXP:    .res 2              ; balas de la lente
BYP:    .res 2
BDP:    .res 2
OXP:    .res 2              ; bolas (P2, P3): x (0 libre), sentido
ODX:    .res 2
EHP:    .res 4              ; emisores: vida, estado (0 quieto, 1 aviso, 2 rayo), tiempo
EST:    .res 4
ETM:    .res 4
btm:    .res 1
eftm:   .res 1
obtm:   .res 1
lztm:   .res 1
lzon:   .res 1              ; emisor con el rayo ($FF ninguno)
p_brot: .res 1
p_fire: .res 1
p_ball: .res 1
p_bsp:  .res 1
p_lz:   .res 1
p_emv:  .res 1
ECOL:   .res 4              ; columna de cada emisor (recorren la cinta de lado a lado)
EDR:    .res 4              ; su sentido (+1 / -1)
EMT:    .res 4              ; cuadros hasta su siguiente paso

        .segment "CODE"
        .include "data5.s"
        .include "motor/nucleo.s"
        .include "motor/pmg.s"
        .include "motor/dli.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/pantalla.s"
        .include "motor/musica.s"
        .include "comun.s"

; ===============================================================
f_vbi:  lda #0
        sta dlin
        rts

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
        jsr pm_init
        ldx #18
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
        jmp scr_on

; entradas de la DLI: 0 pared · 1-2 cintas · 3 emisores · 4-15 sala · 16-17 suelo · 18 marcador
;            0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18
TABBK:  .byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$02,$02,$00,$00,$00
TABP0:  .byte $04,$08,$06,$08,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$06,$06,$00
TABP1:  .byte $46,$84,$94,$84,$44,$44,$44,$44,$44,$44,$44,$44,$44,$44,$44,$44,$04,$04,$0C
TABP2:  .byte $1C,$0E,$0C,$46,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$4E,$1A,$1A,$00

DLTPL:  .byte $70,$70,$70
        .byte $C2
        .word HUDT
        .byte $4E
        .word WALL
        .repeat 38
        .byte $0E
        .endrepeat
        .byte $8E
        .repeat 17, I
        .byte $C4
        .word SCR+I*40
        .endrepeat
        .byte $42
        .word HUDB
        .byte $41
        .word DLGAME
DLLEN = * - DLTPL

; ---------------------------------------------------------------
; filas de la sala (dst = fila, X = cuántas): copia AIR_ROW
air_rows:
        stx tmp
@r:     lda #<AIR_ROW
        sta src
        lda #>AIR_ROW
        sta src+1
        ldx #40
        jsr m_copy
        lda dst
        clc
        adc #40
        sta dst
        bcc @n
        inc dst+1
@n:     dec tmp
        bne @r
        rts

f_start:
        lda #<WALL_BM
        sta src
        lda #>WALL_BM
        sta src+1
        lda #<WALL
        sta dst
        lda #>WALL
        sta dst+1
        ldx #7
        jsr cp220           ; 1540 bytes (src y dst avanzan)
        ldx #60
        jsr m_copy
        ldx #NBELT-1
        lda #CH_CA
@b:     sta BA,x
        sta BB,x
        dex
        bpl @b
        ldx #119            ; cintas y emisores (las columnas de los lados, vacías)
        lda #0
@e:     sta SCR,x
        dex
        bpl @e
        jsr belt_draw
        lda #<AIR0
        sta dst
        lda #>AIR0
        sta dst+1
        ldx #12
        jsr air_rows
        ldx #39
@f:     lda #CH_SA
        sta SCR+15*40,x
        lda #CH_SB
        sta SCR+16*40,x
        dex
        bpl @f
        lda #0
        sta fpose
        ldx #3
@em:    lda EMI_COL,x
        sta ECOL,x
        lda EDR0,x          ; dos a la izquierda, dos a la derecha
        sta EDR,x
        txa
        asl a
        asl a
        sta EMT,x
        lda #6
        sta EHP,x
        lda #0
        sta EST,x
        jsr emi_draw
        dex
        bpl @em
        lda #4
        sta nemi
        lda #$FF
        sta lzon
        lda #0
        sta boom
        sta said
        sta hitfl
        sta OXP
        sta OXP+1
        jsr params
        lda #M_J1
        jsr msg
        lda #64
        sta klax
        lda #1
        sta hudd
        jmp ag_reset

params: lda loopn
        cmp #4
        bcc @l
        lda #4
@l:     sta tmp
        asl a
        asl a
        asl a
        clc
        adc tmp
        adc tmp             ; x10
        sta tmp+1
        clc
        adc #30             ; núcleo: 30 + 10 x vuelta
        ldx dif
        bne @h
        sec
        sbc #10
@h:     cpx #2
        bne @h2
        clc
        adc #10
@h2:    sta nhp
        lda #12             ; giro de las cintas
        sec
        sbc tmp
        sbc tmp
        sta p_brot
        lda #80             ; disparo de la lente
        sec
        sbc tmp+1
        ldx dif
        clc
        adc DIF_F,x
        sta p_fire
        lda #120
        sta eftm
        lda #160            ; bolas
        sec
        sbc tmp+1
        sbc tmp+1
        sta p_ball
        lda #150
        sta obtm
        lda #2
        ldx tmp
        cpx #2
        bcc @s
        lda #3
@s:     sta p_bsp
        lda #170            ; rayos
        sec
        sbc tmp+1
        sbc tmp+1
        ldx dif
        clc
        adc DIF_F,x
        sta p_lz
        lda #180
        sta lztm
        lda p_brot
        sta btm
        lda #8              ; los emisores avanzan una columna cada 8 - vuelta cuadros (mínimo 3)
        sec
        sbc tmp
        ldx dif
        cpx #2
        bne @e
        sec
        sbc #2
@e:     cmp #3
        bcs @e2
        lda #3
@e2:    sta p_emv
        rts
EDR0:   .byte $FF, 1, $FF, 1
DIF_F:  .byte 30, 0, 236

; ---------------------------------------------------------------
f_frame:
        jsr ag_update
        jsr shots_update
        jsr end_update
        lda boom
        bne @r
        jsr belt_turn
        jsr eye_fire
        jsr ebul_update
        jsr balls
        jsr emi_move
        jsr lasers
        jsr taunts
@r:     ; destello de la lente
        lda hitfl
        beq @p
        dec hitfl
        lda #$0E
        sta DTPF2
        lda #$4A
        sta DTPF1
        rts
@p:     lda boom
        bne @x
        lda frame           ; la lente late
        lsr a
        lsr a
        and #7
        tax
        lda PULSE,x
        sta DTPF1
        lda #$1C
        sta DTPF2
@x:     rts
PULSE:  .byte $42,$44,$46,$48,$4A,$48,$46,$44

taunts: lda nhp
        cmp #16
        bcs @a
        lda said
        and #2
        bne @a
        lda said
        ora #2
        sta said
        lda #M_J3
        jmp msg
@a:     lda nemi
        cmp #2
        bcs @r
        lda said
        and #1
        bne @r
        lda said
        ora #1
        sta said
        lda #M_J2
        jmp msg
@r:     rts

f_status:
        lda nhp
        ldx #HUD_NU
        jsr st_dec2
        lda nemi
        clc
        adc #DIG0
        sta HUDB+HUD_EM
        rts

; ---------------------------------------------------------------
; CINTAS: la A gira a la izquierda, la B a la derecha
belt_turn:
        dec btm
        bne @r
        lda p_brot
        sta btm
        lda BA
        pha
        ldx #0
@l:     lda BA+1,x
        sta BA,x
        inx
        cpx #NBELT-1
        bne @l
        pla
        sta BA+NBELT-1
        lda BB+NBELT-1
        pha
        ldx #NBELT-1
@l2:    lda BB-1,x
        sta BB,x
        dex
        bne @l2
        pla
        sta BB
        ; desde la vuelta 2 JANUS repara: de vez en cuando tapa un hueco
        lda loopn
        beq @d
        lda RANDOM
        and #7
        bne @d
        lda RANDOM
        and #31
        tax
        lda BA,x
        bne @d2
        lda #CH_CR
        sta BA,x
@d2:    lda BB,x
        bne @d
        lda #CH_CR
        sta BB,x
@d:     jmp belt_draw
@r:     rts

belt_draw:
        ldx #NBELT-1
@l:     lda BA,x
        sta BELTA,x
        lda BB,x
        sta BELTB,x
        dex
        bpl @l
        rts

; dibuja el emisor X (según vida y estado)
emi_draw:
        ldy ECOL,x
        lda EHP,x
        beq @r
        lda EST,x
        cmp #1
        bne @n
        lda ETM,x
        and #4
        beq @n
        lda EMI_A
        sta EMIROW,y
        lda EMI_A+1
        sta EMIROW+1,y
        rts
@n:     lda EMI_N
        sta EMIROW,y
        lda EMI_N+1
        sta EMIROW+1,y
        rts
@r:     lda EMI_R
        sta EMIROW,y
        lda EMI_R+1
        sta EMIROW+1,y
        rts

; ---------------------------------------------------------------
; EL AGENTE
ag_reset:
        lda #124
        sta ax
        lda #0
        sta pst
        sta aface
        sta crouch
        sta SYP
        sta SYP+1
        sta BYP
        sta BYP+1
        sta OXP
        sta OXP+1
        lda #150
        sta invt
        rts

ag_update:
        lda pst
        beq @alive
        inc ptm
        lda ptm
        cmp #100
        bne @r
        jsr p_after
        bcc @r
        jmp ag_reset
@r:     rts
@alive: lda invt
        beq @i
        dec invt
@i:     lda fpose
        beq @i2
        dec fpose
@i2:    lda #0
        sta crouch
        sta amov
        lda stk
        and #J_DOWN
        beq @up
        lda #1              ; agachado: no anda
        sta crouch
        bne @fi
@up:    lda stk
        and #J_LEFT
        beq @nl
        lda #1
        sta aface
        sta amov
        inc afr
        jsr @step
        lda ax
        sec
        sbc tmp
        cmp #AXMIN
        bcc @nl
        sta ax
@nl:    lda stk
        and #J_RIGHT
        beq @fi
        lda #0
        sta aface
        inc afr
        inc amov
        jsr @step
        lda ax
        clc
        adc tmp
        cmp #AXMAX+1
        bcs @fi
        sta ax
@fi:    lda fire
        beq @nf
        dec ftm
        bpl @r2
        lda #7
        sta ftm
        jmp shot_new
@nf:    lda #0
        sta ftm
@r2:    rts
@step:  lda frame           ; 1,5 relojes de color por cuadro
        and #1
        clc
        adc #1
        sta tmp
        rts

ag_die: lda cheat
        ora invt
        ora pst
        ora boom
        bne @r
        lda #1
        sta pst
        lda #0
        sta ptm
        sta BYP
        sta BYP+1
        jmp p_die
@r:     rts

; caja del agente en tmp+0..3 (de pie o agachado)
ag_box: lda ax
        clc
        adc #1
        sta tmp+0
        adc #5
        sta tmp+1
        lda #AY+1
        ldx crouch
        beq @s
        lda #AY+8
@s:     sta tmp+2
        lda #AY+15
        sta tmp+3
        rts

; ---------------------------------------------------------------
; DISPAROS del agente: hacia arriba
shot_new:
        ldx #1
@f:     lda SYP,x
        beq @ok
        dex
        bpl @f
        rts
@ok:    lda ax
        clc
        adc #3
        sta SXP,x
        lda #AY
        ldy crouch
        beq @s
        lda #AY+7
@s:     sta SYP,x
        lda #8
        sta fpose
        lda #FX_SHOT
        jmp sfx

shots_update:
        ldx #1
@l:     lda SYP,x
        bne @a
        jmp @n
@a:     sec
        sbc #4
        sta SYP,x
        cmp #WALL_Y1
        bcs @below
        ; la pared: ¿la lente?
        lda boom
        bne @off
        lda SXP,x
        cmp #NUC_X0
        bcc @wall
        cmp #NUC_X1
        bcs @wall
        jsr core_hit
        jmp @off
@wall:  lda #FX_CHIP
        jsr sfx
@off:   lda #0
        sta SYP,x
@n:     dex
        bpl @l
        rts
@below: cmp #104
        bcs @n              ; en la sala
        ldy boom
        beq @bel
        jmp @off
@bel:
        ; cintas o emisores: columna
        stx cur
        sec
        sbc #WALL_Y1
        lsr a
        lsr a
        lsr a
        sta tmp+2           ; 0 cinta A, 1 cinta B, 2 emisores
        lda SXP,x
        sec
        sbc #48
        lsr a
        lsr a
        sta tmp+3           ; columna
        lda tmp+2
        cmp #2
        beq @emi
        lda tmp+3
        sec
        sbc #2
        cmp #NBELT
        bcs @nx
        tay
        lda tmp+2
        bne @bb
        lda BA,y
        beq @nx
        jsr belt_hit
        sta BA,y
        jmp @hit
@bb:    lda BB,y
        beq @nx
        jsr belt_hit
        sta BB,y
@hit:   jsr belt_draw
        ldx cur
        jmp @off
@nx:    ldx cur
        jmp @n
@emi:   ldx #3
@e:     lda tmp+3
        sec
        sbc ECOL,x
        cmp #2
        bcs @en
        lda EHP,x
        beq @en
        jsr emi_hit
        ldx cur
        jmp @off
@en:    dex
        bpl @e
        ldx cur
        jmp @n

; golpe a una placa (A = su código): devuelve el nuevo
belt_hit:
        sty tmp+4
        cmp #CH_CA
        bne @h
        lda #FX_CHIP
        jsr sfx
        lda #CH_CR
        rts
@h:     lda #FX_HIT
        jsr sfx
        lda #$10            ; 10 puntos
        ldx #$00
        jsr score_add
        ldy tmp+4
        lda #0
        rts

emi_hit:
        dec EHP,x
        beq @k
        lda #FX_HIT
        jmp sfx
@k:     dec nemi
        lda #1
        sta hudd
        cpx lzon
        bne @d
        jsr beam_off
@d:     lda #0
        sta EST,x
        jsr emi_draw
        lda #FX_EXPL
        jsr sfx
        lda #$00            ; 500
        ldx #$05
        jmp score_add

core_hit:
        stx cur
        lda #6
        sta hitfl
        lda #FX_THUMP
        jsr sfx
        lda #$50
        ldx #$00
        jsr score_add
        lda #1
        sta hudd
        dec nhp
        bne @r
        ; ¡el núcleo cae!
        lda #180
        sta boom
        lda #0
        sta bmt
        sta OXP
        sta OXP+1
        sta BYP
        sta BYP+1
        jsr beam_off
        lda #FX_BIG
        jsr sfx
        lda #$00            ; 5.000
        ldx #$50
        jsr score_add
        lda #M_NUC
        jsr msg
@r:     ldx cur
        rts

; ---------------------------------------------------------------
; EL FINAL: explosiones por la pared y JANUS se apaga
end_update:
        lda boom
        bne *+5
        jmp @r
        cmp #1              ; 1: JANUS ya no está (se queda así hasta el cambio de fase)
        beq @r
        dec boom
        lda boom
        cmp #1
        bne @n
        jmp phase_done
@n:     lda frame
        and #2
        beq @w
        lda #$0E
        bne @s
@w:     lda #$46
@s:     sta DTPF1
        dec bmt
        bpl @a
        lda #9
        sta bmt
        lda RANDOM
        and #127
        adc #64
        sta bmx
        lda RANDOM
        and #63
        adc #36
        sta bmy
        lda #FX_EXPL
        jsr sfx
@a:     lda boom
        cmp #90
        bne @r
        lda #<WALL          ; a mitad: la pared se apaga
        sta dst
        lda #>WALL
        sta dst+1
        ldx #7
@z:     lda #0
        ldy #0
@zb:    sta (dst),y
        iny
        bne @zb
        inc dst+1
        dex
        bne @z
        ldx #119
@z2:    sta SCR,x
        dex
        bpl @z2
        ldx #NBELT-1        ; y lo que se redibuja desde las tablas
@z3:    sta BA,x
        sta BB,x
        dex
        bpl @z3
        ldx #3
@z4:    sta EHP,x
        sta EST,x
        dex
        bpl @z4
        sta nemi
        lda #FX_BIG
        jmp sfx
@r:     rts

; ---------------------------------------------------------------
; LA LENTE dispara al agente (M2, M3)
eye_fire:
        lda pst
        bne @r
        dec eftm
        bne @r
        lda RANDOM
        and #15
        adc p_fire
        sta eftm
        ldy #1
@f:     lda BYP,y
        beq @ok
        dey
        bpl @f
@r:     rts
@ok:    lda #128
        sta BXP,y
        lda #WALL_Y1
        sta BYP,y
        sty tmp+7
        jsr aim
        ldy tmp+7
        sta BDP,y
        lda #FX_EBUL
        jmp sfx

; dirección (0-7) desde la bala tmp+7 hacia el agente
aim:    ldy tmp+7
        lda ax
        clc
        adc #4
        sec
        sbc BXP,y
        sta tmp+2
        lda #AY+8
        sec
        sbc BYP,y
        sta tmp+3
        lda tmp+2
        bpl @a
        eor #$FF
        clc
        adc #1
@a:     sta tmp+4
        asl a
        sta tmp+5
        lda tmp+3
        bpl @b
        eor #$FF
        clc
        adc #1
@b:     sta tmp+6
        lsr a
        cmp tmp+5
        bcs @vert
        lda tmp+2
        bmi @dl
        lda #3
        rts
@dl:    lda #5
        rts
@vert:  lda #4
        rts
EDXT:   .byte 0,1,1,1,0,$FF,$FF,$FF
EDYT:   .byte $FE,$FF,0,2,2,2,0,$FF

ebul_update:
        ldx #1
@l:     lda BYP,x
        beq @n
        ldy BDP,x
        lda BXP,x
        clc
        adc EDXT,y
        sta BXP,x
        lda BYP,x
        clc
        adc EDYT,y
        sta BYP,x
        cmp #AY+16
        bcs @off
        lda BXP,x
        cmp #48
        bcc @off
        cmp #208
        bcs @off
        lda pst
        bne @n
        stx cur
        jsr ag_box
        ldx cur
        lda BXP,x
        cmp tmp+0
        bcc @n
        cmp tmp+1
        bcs @n
        lda BYP,x
        clc
        adc #2
        cmp tmp+2
        bcc @n
        lda BYP,x
        cmp tmp+3
        bcs @n
        jsr ag_die
        ldx cur
@off:   lda #0
        sta BYP,x
@n:     dex
        bpl @l
        rts

; ---------------------------------------------------------------
; BOLAS: cruzan la sala a la altura de la cabeza (agáchate)
balls:  lda pst
        bne @mv
        dec obtm
        bne @mv
        lda RANDOM
        and #31
        adc p_ball
        sta obtm
        ldx #1
@f:     lda OXP,x
        beq @ok
        dex
        bpl @f
        bmi @mv
@ok:    lda RANDOM
        bmi @rt
        lda #40
        sta OXP,x
        lda p_bsp
        sta ODX,x
        jmp @snd
@rt:    lda #208
        sta OXP,x
        lda #0
        sec
        sbc p_bsp
        sta ODX,x
@snd:   lda #FX_BALL
        jsr sfx
@mv:    ldx #1
@l:     lda OXP,x
        beq @n
        clc
        adc ODX,x
        sta OXP,x
        cmp #36
        bcc @off
        cmp #212
        bcs @off
        lda pst
        bne @n
        stx cur
        jsr ag_box
        ldx cur
        lda OXP,x
        clc
        adc #7
        cmp tmp+0
        bcc @n
        lda OXP,x
        cmp tmp+1
        bcs @n
        lda #BALL_Y+6
        cmp tmp+2
        bcc @n
        jsr ag_die
        ldx cur
        jmp @n
@off:   lda #0
        sta OXP,x
@n:     dex
        bpl @l
        rts

; ---------------------------------------------------------------
; LOS EMISORES se desplazan juntos de lado a lado (el rayo va con ellos)
emi_move:
        ldx #3
@l:     lda EHP,x           ; roto: se queda donde cayó
        beq @n
        lda EST,x           ; avisando o disparando: parado
        bne @n
        dec EMT,x
        bne @n
        lda p_emv
        sta EMT,x
        lda RANDOM          ; de vez en cuando cambia de sentido
        and #31
        bne @g
        jsr @rev
@g:     lda ECOL,x          ; columna nueva (sale por un lado y entra por el otro)
        clc
        adc EDR,x
        bpl @g1
        lda #38
@g1:    cmp #39
        bcc @g2
        lda #0
@g2:    sta tmp+2
        ldy #3              ; ¿choca con otro emisor? se da la vuelta
@k:     sty tmp+3
        cpx tmp+3
        beq @kn
        lda tmp+2
        sec
        sbc ECOL,y
        clc
        adc #1
        cmp #3              ; |nueva - otra| < 2
        bcc @bump
@kn:    dey
        bpl @k
        ldy ECOL,x          ; borra la vieja y dibuja la nueva
        lda #0
        sta EMIROW,y
        sta EMIROW+1,y
        lda tmp+2
        sta ECOL,x
        jsr emi_draw
        jmp @n
@bump:  jsr @rev
@n:     dex
        bpl @l
        rts
@rev:   lda #0
        sec
        sbc EDR,x
        sta EDR,x
        rts

; ---------------------------------------------------------------
; RAYOS: un emisor avisa parpadeando y barre la sala con un rayo hasta el suelo
lasers: ldx #3
@l:     lda EST,x
        beq @n
        dec ETM,x
        lda EST,x
        cmp #1
        bne @bm
        ; aviso
        jsr emi_draw
        lda ETM,x
        and #7
        bne @w
        jsr warn_draw
@w:     lda ETM,x
        bne @n
        lda #2              ; ¡rayo!
        sta EST,x
        lda #36
        sta ETM,x
        stx lzon
        jsr emi_draw
        jsr beam_on
        lda #FX_LASER
        jsr sfx
        jmp @n
@bm:    jsr beam_hit
        lda ETM,x
        bne @n
        jsr beam_off
        jsr emi_draw
@n:     dex
        bpl @l
        ; ¿otro emisor?
        lda lzon
        bpl @r
        lda pst
        bne @r
        dec lztm
        bne @r
        lda p_lz
        sta lztm
        lda nemi
        beq @r
        ; el emisor más cercano al agente que siga vivo (a veces uno al azar)
        lda RANDOM
        and #3
        tax
        lda RANDOM
        bmi @p
        jsr near_emi
@p:     ldy #4
@s:     lda EHP,x
        beq @nx
        lda EST,x
        beq @go
@nx:    inx
        txa
        and #3
        tax
        dey
        bne @s
@r:     rts
@go:    lda #1
        sta EST,x
        lda #48
        sta ETM,x
        stx lzon
        lda #FX_ALERT
        jmp sfx

; X = emisor más cercano al agente
near_emi:
        lda ax
        sec
        sbc #48-4
        lsr a
        lsr a
        sta tmp+2           ; columna del agente
        lda #$FF
        sta tmp+3           ; mejor distancia
        ldy #0
        ldx #3
@l:     lda EHP,x
        beq @n
        lda EST,x
        bne @n
        lda ECOL,x
        clc
        adc #1
        sec
        sbc tmp+2
        bcs @p
        eor #$FF
        adc #1
@p:     cmp tmp+3
        bcs @n
        sta tmp+3
        txa
        tay
@n:     dex
        bpl @l
        tya
        tax
        rts

; aviso: puntos que parpadean en la columna del emisor X
warn_draw:
        lda ETM,x
        and #8
        bne @on
        jmp beam_clear
@on:    lda #CH_AI
        sta tmp+2
        lda #CH_AD
        sta tmp+3
        jmp beam_put

beam_on:
        lda #CH_RI
        sta tmp+2
        lda #CH_RD
        sta tmp+3
; escribe tmp+2 / tmp+3 en la columna del emisor X, en las 12 filas de la sala (conserva X)
beam_put:
        stx bcur
        ldy ECOL,x
        lda #<AIR0
        sta scp
        lda #>AIR0
        sta scp+1
        ldx #12
@r:     lda tmp+2
        sta (scp),y
        iny
        lda tmp+3
        sta (scp),y
        dey
        lda scp
        clc
        adc #40
        sta scp
        bcc @n
        inc scp+1
@n:     dex
        bne @r
        ldx bcur
        rts

; restaura la sala en la columna del emisor lzon (conserva X)
beam_clear:
        stx bcur
        ldx lzon
        bmi @r
        ldy ECOL,x
        lda #<AIR0
        sta scp
        lda #>AIR0
        sta scp+1
        ldx #12
@l:     lda AIR_ROW,y
        sta (scp),y
        iny
        lda AIR_ROW,y
        sta (scp),y
        dey
        lda scp
        clc
        adc #40
        sta scp
        bcc @n
        inc scp+1
@n:     dex
        bne @l
@r:     ldx bcur
        rts

; apaga el rayo (o el aviso) en curso
beam_off:
        jsr beam_clear
        stx bcur
        ldx lzon
        bmi @r
        lda #0
        sta EST,x
        lda #$FF
        sta lzon
@r:     ldx bcur
        rts

; ¿el rayo del emisor X toca al agente?
beam_hit:
        lda pst
        bne @r
        lda ECOL,x
        asl a
        asl a
        adc #48+2
        sta tmp+4           ; el rayo: 4 relojes de color
        lda ax
        clc
        adc #6
        cmp tmp+4
        bcc @r
        lda tmp+4
        clc
        adc #3
        cmp ax
        bcc @r
        stx cur
        jsr ag_die
        ldx cur
@r:     rts

; ---------------------------------------------------------------
f_render:
        jsr pm_begin
        lda pst
        bne @dead
        lda invt
        and #4
        beq *+5
        jmp @ob
        ldx rb
        lda ax
        sta PHP0,x
        sta PHP1,x
        lda #$C6
        sta PCP0,x
        lda #$2A
        sta PCP1,x
        lda crouch
        beq @st
        lda aface
        ora #4
        bne @fr
@st:    lda fpose           ; disparando: brazos en alto
        beq @wk
        lda #8
        bne @fr
@wk:    lda afr             ; andando: ciclo de 4 pasos
        lsr a
        lsr a
        lsr a
        and #3
        ldx amov
        bne @w2
        lda #0
@w2:    ldx aface
        beq @w3
        ora #4
@w3:    tax
        lda WALKF,x
@fr:    asl a
        asl a
        asl a
        asl a
        sta tmp
        clc
        adc #<AG_P0
        sta src
        lda #>AG_P0
        adc #0
        sta src+1
        ldx #0
        lda #AY
        ldy #16
        jsr pm_spr
        lda tmp
        clc
        adc #<AG_P1
        sta src
        lda #>AG_P1
        adc #0
        sta src+1
        ldx #1
        lda #AY
        ldy #16
        jsr pm_spr
        jmp @ob
@dead:  lda ptm
        cmp #36
        bcs @ob
        ldx rb
        lda ax
        sta PHP0,x
        lda #$1C
        sta PCP0,x
        lda ptm
        lsr a
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        ldx #0
        lda #AY+4
        ldy #8
        jsr pm_spr
@ob:    ; bolas (P2, P3) o las explosiones del final (P3)
        lda boom
        beq @bl
        cmp #2
        bcc @bm
        lda bmt
        cmp #6
        bcc @bm
        ldx rb
        lda bmx
        sta PHP3,x
        lda #$2E
        sta PCP3,x
        lda #9
        sec
        sbc bmt
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        ldx #3
        lda bmy
        ldy #8
        jsr pm_spr
@bm:    jmp @ms
@bl:    ldx #1
@b:     lda OXP,x
        beq @bn
        stx cur
        txa
        clc
        adc #2
        sta tmp+2
        cmp #2
        bne @p3
        ldy rb
        lda OXP,x
        sta PHP2,y
        lda frame
        and #6
        ora #$18
        sta PCP2,y
        jmp @sp
@p3:    ldy rb
        lda OXP,x
        sta PHP3,y
        lda frame
        and #6
        ora #$18
        sta PCP3,y
@sp:    lda #<BOLA_P
        sta src
        lda #>BOLA_P
        sta src+1
        ldx tmp+2
        lda #BALL_Y
        ldy #8
        jsr pm_spr
        ldx cur
@bn:    dex
        bpl @b
@ms:    ; disparos M0-M1 y balas M2-M3
        ldx #1
@s:     lda SYP,x
        beq @sn
        stx cur
        txa
        asl a
        ora rb
        tay
        lda SXP,x
        sta PHM0,y
        lda SYP,x
        ldy #4
        jsr pm_mis
        ldx cur
@sn:    dex
        bpl @s
        ldx #1
@e:     lda BYP,x
        beq @en
        stx cur
        txa
        clc
        adc #2
        tax
        asl a
        ora rb
        tay
        stx tmp+2
        ldx cur
        lda BXP,x
        sta PHM0,y
        lda BYP,x
        ldx tmp+2
        ldy #3
        jsr pm_mis
        ldx cur
@en:    dex
        bpl @e
        jmp pm_end

WALKF:  .byte 0,1,0,6, 2,3,2,7   ; parado, paso A, parado, paso B (derecha · izquierda)

; ---------------------------------------------------------------
;        0 disp 1 expl 2 golpe 3 estal 4 muerte 5 alerta 6 enorme 7 beep 8 bala 9 vida 10 golpeG 11 muerte2 12 chip 13 klax1 14 klax2 15 rayo 16 bola
SX_CH:  .byte 0,   1,   0,   1,   1,   3,   2,   3,   2,   3,   2,   2,   0,   3,   3,   3,   2
SX_F:   .byte $05, $14, $08, $30, $20, $10, $50, $20, $18, $40, $40, $20, $06, $1C, $28, $60, $28
SX_S:   .byte 2,   2,   2,   1,   1,   0,   1,   $FF, 1,   $FD, 3,   2,   1,   0,   0,   $FE, 1
SX_V:   .byte 11,  15,  14,  15,  15,  10,  15,  10,  7,   12,  15,  15,  9,   12,  12,  14,  10
SX_D:   .byte 8,   44,  10,  80,  130, 40,  150, 30,  8,   24,  26,  72,  5,   8,   8,   36,  30
SX_C:   .byte $80, $80, $A0, $80, $80, $A0, $80, $A0, $A0, $A0, $C0, $C0, $80, $C0, $C0, $A0, $A0
SX_P:   .byte 2,   3,   3,   4,   5,   3,   5,   4,   1,   4,   3,   5,   1,   3,   3,   4,   2
SX_K:   .byte 0,   3,   0,   7,   7,   0,   7,   7,   1,   7,   1,   3,   0,   0,   0,   1,   1
