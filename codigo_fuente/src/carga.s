; ===============================================================
; TRAMOS Y ARENAS COMPRIMIDOS
; Cada tramo/arena es un bloque de $2200-$3FFF comprimido (LZ) que se
; guarda en la RAM bajo el OS ($C000-$CFFF y $D800-$FFF9) durante la carga
; del XEX (segmentos INIT que llaman a oscopy) y se descomprime al empezar.
; Formato LZ: c=0 fin · $01-$7F c literales · $80-$BF copia (c&$3F)+3 con
; distancia de 1 byte · $C0-$FF igual con distancia de 2 bytes (lo, hi)
; ===============================================================

; A = número de paquete -> descomprimido en OVL
pack_load:
        tax
        lda PK_LO,x
        sta lzs
        lda PK_HI,x
        sta lzs+1
        lda #<OVL
        sta lzd
        lda #>OVL
        sta lzd+1
        sei
        lda #0
        sta NMIEN
        lda PORTB
        and #$FE
        sta PORTB
        jsr lz_unpack
        lda PORTB
        ora #$01
        sta PORTB
        lda #$40
        sta NMIEN
        cli
        rts

lz_unpack:
        ldy #0
@tok:   lda (lzs),y
        tax
        inc lzs
        bne *+4
        inc lzs+1
        txa
        bne *+3
        rts
        bmi @mt
@lit:   lda (lzs),y
        sta (lzd),y
        inc lzs
        bne *+4
        inc lzs+1
        inc lzd
        bne *+4
        inc lzd+1
        dex
        bne @lit
        beq @tok
@mt:    and #$3F
        clc
        adc #3
        sta lzn
        lda lzd
        sec
        sbc (lzs),y
        sta lzm
        lda lzd+1
        sbc #0
        sta lzm+1
        inc lzs
        bne *+4
        inc lzs+1
        txa
        and #$40
        beq @cp
        lda lzm+1
        sec
        sbc (lzs),y
        sta lzm+1
        inc lzs
        bne *+4
        inc lzs+1
@cp:    ldx lzn
@c1:    lda (lzm),y
        sta (lzd),y
        inc lzm
        bne *+4
        inc lzm+1
        inc lzd
        bne *+4
        inc lzd+1
        dex
        bne @c1
        beq @tok

; INIT durante la carga: $A000 = destino (2), longitud (2), datos
LOADBUF = $A000
oscopy: sei
        lda #0
        sta NMIEN
        lda PORTB
        and #$FE
        sta PORTB
        lda #<(LOADBUF+4)
        sta lzs
        lda #>(LOADBUF+4)
        sta lzs+1
        lda LOADBUF
        sta lzd
        lda LOADBUF+1
        sta lzd+1
        ldx LOADBUF+3       ; páginas completas
        ldy #0
@pg:    cpx #0
        beq @rest
@p1:    lda (lzs),y
        sta (lzd),y
        iny
        bne @p1
        inc lzs+1
        inc lzd+1
        dex
        jmp @pg
@rest:  ldx LOADBUF+2
        beq @fin
@r1:    lda (lzs),y
        sta (lzd),y
        iny
        dex
        bne @r1
@fin:   lda PORTB
        ora #$01
        sta PORTB
        lda #$40
        sta NMIEN
        cli
        rts

; rótulo al entrar en un tramo (textos de la tabla del tramo)
tr_card:
        ldx #19
@cf:    lda T_FASE,x
        sta T_FASEN,x
        dex
        bpl @cf
        lda fase
        clc
        adc #$80+DIG0
        sta T_FASEN+12
        jsr snd_off
        lda #0
        sta gmode
        lda #>CHARSA
        sta CHBAS
        lda #<DESC_CARD
        sta ptr
        lda #>DESC_CARD
        sta ptr+1
        jsr txt_build
        jsr txt_colors
        jsr txt_show
        lda #11
        jsr sfx
        ldx #150
        jsr m_waitn
        jsr snd_off
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        jmp m_wait

DESC_CARD:
        .byte $70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte 6, <T_FASEN, >T_FASEN
        .byte $70,$70,$70
        .byte 7, <TR_T1, >TR_T1
        .byte $70
        .byte 6, <TR_T2, >TR_T2
        .byte $FF

; final de un tramo: el siguiente o la arena del jefe
tr_finish:
        lda TR_NEXT
        cmp #$FF
        beq @ar
        sta tramo
        lda #0
        sta chk
        lda #1
        sta card
        lda #$00            ; bonificación de tramo: 1.000
        ldx #$10
        jsr addsc
        jmp level
@ar:    lda #2
        sta chk
arena_go:
        lda fase
        cmp #5
        bne @f4
        jmp arena6
@f4:    cmp #4
        bne @f3
        lda chk
        cmp #3
        bne *+5
        jmp arena5
        jmp arena4
@f3:    cmp #3
        bne @f2
        jmp arena3
@f2:    cmp #2
        bne @f1
        jmp arena2
@f1:    jmp arena

fase5_start:
        lda #5
        jsr mod_load
        lda #5
        sta fase
        lda #PK_CAS
        sta tramo
        lda #0
        sta chk
        lda #1
        sta card
        jmp level

fase4_start:
        lda #4
        jsr mod_load
        lda #4
        sta fase
        lda #PK_CAR
        sta tramo
        lda #0
        sta chk
        lda #1
        sta card
        jmp level

; tras el Căpcăun, el Rey Strigoi (si muere aquí, vuelve a esta arena)
arena5_go:
        lda #3
        sta chk
        jmp arena5

; FINAL: pantalla de despedida y al título
ending: lda #0
        sta aftert+1
        lda #<DESC_FIN
        sta ptr
        lda #>DESC_FIN
        sta ptr+1
        lda #5
        jmp txt_score_wait

DESC_FIN:
        .byte $70,$70,$70,$70
        .byte 7, <T_F1, >T_F1
        .byte $70
        .byte 7, <T_F2, >T_F2
        .byte $70,$70
        .byte 6, <T_F3, >T_F3
        .byte $30
        .byte 6, <T_F4, >T_F4
        .byte $70,$70
        .byte 6, <T_F5, >T_F5
        .byte $70
        .byte 6, <T_PTS, >T_PTS
        .byte $FF

fase3_start:
        lda #3
        jsr mod_load
        lda #3
        sta fase
        lda #PK_MIN
        sta tramo
        lda #0
        sta chk
        lda #1
        sta card
        jmp level

fase2_start:
        lda #2
        jsr mod_load
        lda #2
        sta fase
        lda #PK_CIU
        sta tramo
        lda #0
        sta chk
        lda #1
        sta card
        jmp level
