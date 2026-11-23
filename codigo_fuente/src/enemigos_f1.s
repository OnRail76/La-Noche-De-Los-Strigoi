        .segment "MOD1"
; ---------------------------------------------------------------
; VÂVÂMA (tipo 8): espera escondida en el tronco; sale, lanza un zarpazo
; de 36 píxeles hacia Radu y vuelve al árbol
; ---------------------------------------------------------------
e_vav:  lda est,x
        bne @s1
        jsr dist_x          ; 0: escondida
        cmp #52
        bcs @r
        lda #1
        sta est,x
        lda #0
        sta et,x
        lda #18
        jmp sfx
@s1:    inc et,x
        cmp #1
        bne @s2
        lda et,x            ; 1: aparece (parpadea)
        cmp #20
        bcc @r
        jsr face_radu
        lda #2
        sta est,x
        lda #0
        sta et,x
        lda #17
        jmp sfx
@s2:    cmp #2
        bne @s3
        lda et,x            ; 2: zarpazo
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        lda edir,x
        bne @a
        lda efr,x
        ora #2
        sta efr,x
@a:     lda et,x
        cmp #36
        bcs @back
        jmp vstep
@back:  lda #3
        sta est,x
        lda #0
        sta et,x
        rts
@s3:    cmp #3
        bne @s4
        lda et,x            ; 3: vuelve al árbol
        cmp #36
        bcs @hide
        lda edir,x
        eor #1
        sta edir,x
        jsr vstep
        lda edir,x
        eor #1
        sta edir,x
@r:     rts
@hide:  lda #4
        sta est,x
        lda #0
        sta et,x
        rts
@s4:    lda et,x            ; 4: descanso escondida
        cmp #90
        bcc @r
        lda #0
        sta est,x
        rts
; un píxel en la dirección edir
