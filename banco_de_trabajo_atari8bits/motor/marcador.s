; ===============================================================
; MOTOR · puntuación BCD de 6 cifras, récord y vida extra
; El juego define EXTRA_STEP: cuánto sube el umbral de vida extra (byte alto BCD: $06 = 60.000)
; ===============================================================
        .segment "ZEROPAGE"
score:  .res 3              ; BCD, byte 0 = unidades y decenas
hisc:   .res 3
nextx:  .res 3              ; siguiente vida extra
sca:    .res 1
scx:    .res 1
digb:   .res 1

        .segment "CODE"
; suma A (unidades y decenas, BCD) y X (centenas y millares, BCD)
; vuelve con C = 1 si se ha pasado el umbral de vida extra (y lo sube)
addsc:  sta sca
        stx scx
        sed
        clc
        lda score
        adc sca
        sta score
        lda score+1
        adc scx
        sta score+1
        lda score+2
        adc #0
        sta score+2
        cld
        lda score+2
        cmp nextx+2
        bcc @no
        bne @yes
        lda score+1
        cmp nextx+1
        bcc @no
        bne @yes
        lda score
        cmp nextx
        bcc @no
@yes:   sed
        clc
        lda nextx+2
        adc #EXTRA_STEP
        sta nextx+2
        cld
        sec
        rts
@no:    clc
        rts

; récord = puntuación si es mayor
hiupd:  lda score+2
        cmp hisc+2
        bcc @r
        bne @c
        lda score+1
        cmp hisc+1
        bcc @r
        bne @c
        lda score
        cmp hisc
        bcc @r
@c:     lda score
        sta hisc
        lda score+1
        sta hisc+1
        lda score+2
        sta hisc+2
@r:     rts

; escribe 3 bytes BCD (src, de mayor a menor) en dst; A = código del '0'
put6:   sta digb
        ldy #2
        lda (src),y
        jsr put2
        ldy #1
        lda (src),y
        jsr put2
        ldy #0
        lda (src),y
put2:   pha
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc digb
        ldy #0
        sta (dst),y
        pla
        and #15
        clc
        adc digb
        iny
        sta (dst),y
        lda dst
        clc
        adc #2
        sta dst
        bcc @r
        inc dst+1
@r:     rts

; A (0-99 binario) -> dos cifras en dst (digb ya puesto)
putdec2:
        ldx #0
@d:     cmp #10
        bcc @u
        sbc #10
        inx
        bne @d
@u:     pha
        txa
        clc
        adc digb
        ldy #0
        sta (dst),y
        pla
        clc
        adc digb
        iny
        sta (dst),y
        rts
