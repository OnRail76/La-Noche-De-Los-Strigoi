; ===============================================================
; MÓDULO 5 · EL CASTILLO DEL TRONO DE SANGRE
; Caballeros no muertos (tres golpes), pinchos y la cabeza gigante del Rey
; Strigoi: solo se le hace daño con la boca abierta.
; ===============================================================
        .segment "MOD5"
; caballero no muerto (tipo 21): avanza despacio hacia Radu sin caerse
e_knight:
        inc et,x
        lda et,x
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        lda et,x
        and #63
        bne @w
        jsr face_radu
@w:     jmp walk_edge

GP6:    .byte PK_AR6, G6_S1, G6_S2, G6_S3
        .word G6_BLK
        .byte G6_R, G6_C, G6_W, G6_H
        .word G6_ALT
        .byte G6_HL, G6_HR, G6_HT, G6_HB, G6_BL, G6_BR, G6_BT, G6_BB
        .byte 16
        .word ATK6
        .byte 50, G6_AX, G6_AY
        .word ending
        .byte 1, G6_RX
        .word arena6
ATK6:   .byte 2, 6, 5, 2, 6, 1, 3, 6, 0
arena6: lda #<GP6
        ldx #>GP6
        jmp garena

; ===============================================================
; EL FINAL: el castillo se derrumba, amanece sobre Sighișoara,
; desfile de jefes y criaturas, créditos y la puntuación final.
; ===============================================================
fin_juego:
        lda #8              ; toda la sala revienta
        sta bx_l
        lda #150
        sta bx_r
        lda #48
        sta bx_t
        lda #180
        sta bx_b
        lda #0
        sta bdt
        sta cr_i
        lda #4              ; Radu huye corriendo hacia la derecha
        sta rinv
@lp:    jsr pm_wait
        inc bdt
        lda bdt
        and #3
        bne @nb
        jsr blast_spawn
@nb:    lda bdt
        and #15
        bne @ns
        lda #9
        jsr sfx
        lda #2
        jsr sfx
@ns:    lda bdt             ; destellos
        cmp #60
        bcs @nf
        and #8
        beq @fo
        lda #$44
        bne @fs
@fo:    lda #$0E
@fs:    ldx #20
@f1:    sta DTBK,x
        dex
        bpl @f1
        jmp @cr
@nf:    bne @cr
        ldx #20
        lda #0
@f2:    sta DTBK,x
        dex
        bpl @f2
@cr:    lda bdt             ; la sala se viene abajo, fila a fila
        and #7
        bne @nc
        lda cr_i
        cmp #21
        bcs @nc
        tax
        lda ASROW_LO,x
        sta dst
        lda ASROW_HI,x
        sta dst+1
        ldy #39
        lda #0
@cz:    sta (dst),y
        dey
        bpl @cz
        lda cr_i
        asl a
        asl a
        asl a
        clc
        adc #40
        sta tyy
        lda RANDOM
        and #127
        sta tcol
        lda #10
        sta cr_w
        jsr debris_spawn
        jsr debris_spawn
        inc cr_i
@nc:    jsr debris_update
        jsr enemies
        jsr draw
        jsr debris_draw
        jsr pm_end
        lda bdt
        cmp #220
        bcs *+5
        jmp @lp
        ; --- amanecer
        jsr scr_titulo
        lda #<TT_TOP
        sta src
        lda #>TT_TOP
        sta src+1
        ldx #0
        jsr scr_line
        jsr scr_on
        lda #4
        jsr mus_play
        lda #0
        sta sc_t
        sta sc_ph
@dw:    jsr pm_wait
        jsr bats_deco
        lda ey              ; los murciélagos se van
        cmp #50
        bcc @bh
        dec elife
        dec elife+1
@bh:    inc sc_t
        bne @nt
        inc sc_ph
        lda sc_ph           ; cada 256 cuadros, un paso del amanecer
        cmp #4
        bcs @nt
        tax
        jsr dawn_step
@nt:    lda sc_ph
        cmp #2
        bne @nx
        lda sc_t
        bne @nx
        lda #<TT_FIN1       ; «LA NOCHE / HA TERMINADO»
        sta src
        lda #>TT_FIN1
        sta src+1
        ldx #1
        jsr scr_line
        lda #<TT_FIN2
        sta src
        lda #>TT_FIN2
        sta src+1
        ldx #2
        jsr scr_line
@nx:    jsr draw
        jsr pm_end
        lda sc_ph
        cmp #4
        bcc @dw
        ; --- desfile de jefes y criaturas, créditos
        lda #<CRED1
        jsr cred_page
        lda #<CRED2
        jsr cred_page
        lda #<CRED3
        jsr cred_page
        jmp ending

; X = paso (1-3): el cielo de la escena pasa de la noche al día
dawn_step:
        dex
        txa
        asl a
        asl a
        asl a
        tax
        ldy #0
@k:     lda DAWN,x
        sta DTBK+6,y
        lda DAWNM,x         ; la luna se apaga
        sta DTPF1+6,y
        inx
        iny
        cpy #8
        bne @k
        rts
DAWN:   .byte $70,$72,$74,$44,$46,$34,$22,$00     ; violeta y rosa
        .byte $84,$86,$88,$3A,$2A,$28,$26,$24     ; naranja de la aurora
        .byte $96,$98,$9A,$9C,$9E,$2C,$2A,$28     ; azul de la mañana
DAWNM:  .byte $0A,$0A,$0A,$0A,$0A,$08,$08,$08
        .byte $3A,$3A,$3A,$3A,$3A,$08,$08,$08
        .byte $9C,$9C,$9C,$9C,$9C,$08,$08,$08

; A = página de créditos (lo; todas en la misma página alta)
cred_page:
        sta ptr
        lda #>CRED1
        sta ptr+1
        lda #0
        sta gmode
        lda #4
        sta rinv
        jsr txt_build
        jsr txt_colors
        jsr txt_show
        ldx #240
        jsr m_waitn
        ldx #60
        jmp m_waitn

CRED1:  .byte $70,$70,$70,$70,$70,$70
        .byte 7, <CR_T1, >CR_T1
        .byte $70,$70
        .byte 6, <CR_1, >CR_1
        .byte $70
        .byte 6, <CR_2, >CR_2
        .byte $30
        .byte 6, <CR_2B, >CR_2B
        .byte $70
        .byte 6, <CR_3, >CR_3
        .byte $70
        .byte 6, <CR_4, >CR_4
        .byte $70
        .byte 6, <CR_5, >CR_5
        .byte $FF
CRED2:  .byte $70,$70,$70,$70,$70,$70
        .byte 7, <CR_T2, >CR_T2
        .byte $70,$70
        .byte 6, <CR_E1, >CR_E1
        .byte $70
        .byte 6, <CR_E2, >CR_E2
        .byte $70
        .byte 6, <CR_E3, >CR_E3
        .byte $70
        .byte 6, <CR_E4, >CR_E4
        .byte $70
        .byte 6, <CR_E5, >CR_E5
        .byte $70
        .byte 6, <CR_E6, >CR_E6
        .byte $FF
CRED3:  .byte $70,$70,$70,$70,$70,$70,$70,$70
        .byte 6, <CR_A1, >CR_A1
        .byte $70
        .byte 7, <CR_A2, >CR_A2
        .byte $70
        .byte 6, <CR_A3, >CR_A3
        .byte $30
        .byte 6, <CR_A4, >CR_A4
        .byte $70,$70,$70
        .byte 7, <CR_G, >CR_G
        .byte $FF
        .assert >CRED1 = >CRED3, error, "créditos: misma página"
