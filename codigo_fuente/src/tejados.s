; ===============================================================
; PASARELAS QUE SE HUNDEN (clase 3): si Radu se queda encima ~1/4 s,
; la fila de tablas se desploma (se borra del mapa y de los anillos)
; ===============================================================
        .segment "HIBSS"
frag_t: .res 1
fr_r:   .res 1
fr_c:   .res 1
        .segment "CODE"

; clase de la casilla (tx, línea A) -> A
t_class:
        cmp #GTOP
        bcc @no
        cmp #GTOP+13*8
        bcs @no
        sec
        sbc #GTOP
        lsr a
        lsr a
        lsr a
        clc
        adc mapb
        sta mp+1
        lda #0
        sta mp
        jsr col_tx
        tay
        lda (mp),y
        and #$7F            ; los inversos (PF3) son decorado del mismo carácter
        tay
        lda (clsp),y
        rts
@no:    lda #0
        rts

frag_check:
        lda gmode
        cmp #1
        bne @r
        lda rxl
        clc
        adc #4
        sta tx
        lda rxh
        adc #0
        sta tx+1
        lda ry
        jsr t_class
        cmp #3
        beq @f
        cmp #4              ; pinchos
        bne @nz
        lda rinv
        ora cheat
        bne @nz
        jmp r_hit
@nz:    lda #0
        sta frag_t
@r:     rts
@f:     inc frag_t
        lda frag_t
        cmp #3              ; crujido al pisar
        bne @n
        lda #16
        jsr sfx
@n:     lda frag_t
        cmp #16
        bcc @r
        lda #0
        sta frag_t
        ; fila y columna (mp+1 y tcol de t_class)
        lda mp+1
        sta fr_r
        lda tcol
        sta fr_c
        ; hacia la izquierda mientras sea clase 3
@lf:    ldy fr_c
        beq @go
        dey
        lda (mp),y
        tay
        lda CLASS,y
        cmp #3
        bne @go
        dec fr_c
        jmp @lf
@go:    lda #9
        jsr sfx
        lda #2
        jsr sfx
@cl:    lda fr_r
        sta mp+1
        lda #0
        sta mp
        ldy fr_c
        lda (mp),y
        tay
        lda CLASS,y
        cmp #3
        bne @done
        ldy fr_c
        lda #0
        sta (mp),y
        ; ¿columna dentro del anillo? (cam_left <= c < cam_left+64)
        jsr cam_left
        sta hitl
        lda fr_c
        sec
        sbc hitl
        cmp #64
        bcs @nx
        lda fr_c
        jsr wcol
@nx:    inc fr_c
        bne @cl
@done:  rts
