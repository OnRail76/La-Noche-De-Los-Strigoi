; ===============================================================
; EFECTOS DE TRAMO (residente): viento de los acantilados, mandos
; cambiados por los fuegos fatuos y pinchos (clase 4)
; ===============================================================
        .segment "HIBSS"
rinvc:  .res 1              ; cuadros con los mandos cambiados
        .segment "CODE"

; izquierda y derecha cambiadas mientras dure el hechizo del fuego fatuo
ctl_fx: lda rinvc
        beq @r
        dec rinvc
        lda stk
        jsr @sw
        sta stk
        lda stked
        jsr @sw
        sta stked
@r:     rts
@sw:    sta tyy
        and #$F3
        sta hitl
        lda tyy
        and #4
        asl a
        ora hitl
        sta hitl
        lda tyy
        and #8
        lsr a
        ora hitl
        rts

; viento: en las columnas [TR_X, TR_X+1) y [TR_X+2, TR_X+3) empuja a Radu atrás
wind_fx:
        lda rst
        cmp #3
        beq @r
        lda frame
        and #1
        bne @r
        lda rxl
        sta tx
        lda rxh
        sta tx+1
        jsr col_tx
        lda tcol
        ldx #0
@z:     cmp TR_X,x
        bcc @n
        cmp TR_X+1,x
        bcs @n
        lda frame
        and #63
        bne @p
        lda #18
        jsr sfx
@p:     lda #$FF
        jmp r_movex
@n:     lda tcol
        inx
        inx
        cpx #4
        bne @z
@r:     rts
