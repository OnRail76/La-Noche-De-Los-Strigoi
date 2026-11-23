        .segment "MOD3"
; ---------------------------------------------------------------
; MOROI: aparición que se desvanece y vuelve a tomar cuerpo más cerca.
; Solo daña (y se le puede dar) cuando es sólido. Tres apariciones y se va.
e_moroi:
        inc et,x
        lda frame
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        lda est,x
        bne @s1
        lda frame           ; 0: invisible, se acerca despacio
        and #3
        bne @w0
        jsr step_to_radu
        lda ry
        sec
        sbc #14
        jsr y_toward
@w0:    lda et,x
        cmp #40
        bcc @r
        lda #1
        bne @ns
@s1:    cmp #1
        bne @s2
        lda et,x            ; 1: toma cuerpo
        cmp #20
        bcc @r
        lda #18
        jsr sfx
        lda #2
        bne @ns
@s2:    cmp #2
        bne @s3
        lda frame           ; 2: sólido, flota hacia Radu
        and #1
        bne @w2
        jsr step_to_radu
        lda ry
        sec
        sbc #14
        jsr y_toward
@w2:    lda et,x
        cmp #90
        bcc @r
        lda #3
        bne @ns
@s3:    lda et,x            ; 3: se desvanece
        cmp #20
        bcc @r
        dec ehp,x
        bne @again
        lda #0
        sta etyp,x
        rts
@again: lda #0
@ns:    sta est,x
        lda #0
        sta et,x
@r:     rts

; ---------------------------------------------------------------
; VÂLVA BĂII: espíritu minero; pasea por su roca y lanza picos en parábola
e_valva:
        inc et,x
        lda est,x
        bne @thr
        lda et,x
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        jsr walk_edge
        lda et,x
        cmp #90
        bcc @r
        jsr face_radu
        lda #1
        sta est,x
        lda #0
        sta et,x
@r:     rts
@thr:   lda #2
        sta efr,x
        lda et,x
        cmp #16
        bcc @r
        lda #3
        sta efr,x
        lda et,x
        cmp #16
        bne @end
        txa                 ; pico en el otro hueco
        eor #1
        tay
        lda etyp,y
        bne @end
        lda #16
        sta etyp,y
        lda #0
        sta est,y
        sta et,y
        sta efr,y
        lda edir,x
        sta edir,y
        lda exl,x
        sta exl,y
        lda exh,x
        sta exh,y
        lda ey,x
        sec
        sbc #16
        sta ey,y
        lda #$FC            ; sube con -4 y cae
        sta elife,y
        lda #12
        jsr sfx
@end:   lda et,x
        cmp #30
        bcc @r
        lda #0
        sta est,x
        sta et,x
        rts

