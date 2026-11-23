; ===============================================================
; SDI '86 · el CENTINELA-4 en su carril (fases 2 y 3)
; La nave son 4 x 2 caracteres en las columnas 0-3 de los anillos RP0/RP1 (carril 1):
; se mueve cambiando la posición del carril (pos = -CAR_K - x), así lleva sus 4 colores.
; La operación define RP0, RP1, SHIPPOS (posición de su carril), Y_SHIP (primera línea visible), SHOT_Y0 y FX_SHOT.
; ===============================================================
ship_reset:
        lda #72
        sta shipx
        lda #0
        sta pst
        lda #150
        sta invt
        lda #0
        sta BT
        sta BT+1
        sta BT+2
        lda #1
        jmp ship_draw

; A = 0 nada · 1 nave · 2-4 explosión (cuadro 0-2)
ship_draw:
        sta tmp+2
        lda #<RP0
        sta dst
        lda #>RP0
        sta dst+1
        ldy #0
@t:     jsr @c
        jsr car_put
        iny
        cpy #4
        bne @t
        lda #<RP1
        sta dst
        ldy #0
@b:     jsr @c2
        jsr car_put
        iny
        cpy #4
        bne @b
        rts
@c:     lda tmp+2
        beq @z
        cmp #1
        bne @x
        lda NAVE_T,y
        rts
@c2:    lda tmp+2
        beq @z
        cmp #1
        bne @x
        lda NAVE_B,y
        rts
@x:     sec                 ; explosión: cuadro (tmp+2 - 2), dos caracteres que se repiten
        sbc #2
        asl a
        sta tmp+3
        tya
        and #1
        ora tmp+3
        tax
        lda EXPL_C,x
        rts
@z:     lda #0
        rts

ship_update:
        lda pst
        beq @alive
        inc ptm
        lda ptm
        cmp #36
        bcs @e
        lsr a
        lsr a
        lsr a
        lsr a               ; 0-2
        clc
        adc #2
        jmp ship_draw
@e:     bne @w
        lda #0
        jmp ship_draw
@w:     cmp #100
        bne @r
        jsr p_after
        bcc @r
        jmp ship_reset
@r:     rts
@alive: lda stk
        and #J_LEFT
        beq @nl
        lda shipx
        cmp #6
        bcc @nl
        sbc #2
        sta shipx
@nl:    lda stk
        and #J_RIGHT
        beq @nr
        lda shipx
        cmp #139
        bcs @nr
        adc #2
        sta shipx
@nr:    lda #0              ; la nave está en las columnas 0-3 del anillo: pos = -13 - x
        sec
        sbc #CAR_K
        sec
        sbc shipx
        sta SHIPPOS
        lda invt            ; invulnerable: parpadea
        beq @f
        dec invt
        lda invt
        and #3
        bne @f
        lda invt
        and #4
        beq @on
        lda #0
        jsr ship_draw
        jmp @f
@on:    lda #1
        jsr ship_draw
@f:     lda fire
        beq @r2
        lda shoty
        bne @r2
        lda shipx
        clc
        adc #48+7
        sta shotx
        lda #SHOT_Y0
        sta shoty
        lda #FX_SHOT
        jmp sfx
@r2:    rts

; caja de la nave en tmp+4..7 (HPOS / líneas)
shipbox:
        lda shipx
        clc
        adc #48+1
        sta tmp+4
        adc #13
        sta tmp+5
        lda #Y_SHIP
        sta tmp+6
        lda #Y_SHIP+8
        sta tmp+7
        rts

kill_ship:
        lda cheat
        ora invt
        ora pst
        bne @r
        lda #1
        sta pst
        lda #0
        sta ptm
        jmp p_die
@r:     rts

