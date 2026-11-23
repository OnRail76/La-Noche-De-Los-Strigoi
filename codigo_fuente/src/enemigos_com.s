; ===============================================================
; ENEMIGOS COMUNES A VARIAS FASES (residente)
; ===============================================================
e_tipoN:                    ; tipos 14 en adelante
        cmp #16
        bcc @f3
        bne *+5
        jmp e_pick
        cmp #17
        bne *+5
        jmp e_estal
        cmp #18
        bne *+5
        jmp e_insect
        cmp #19
        bne *+5
        jmp e_lupari
        cmp #20
        bne *+5
        jmp e_fatuo
        cmp #21
        bne *+5
        jmp e_knight
        jmp e_shock
@f3:    cmp #14
        bne *+5
        jmp e_moroi
        jmp e_valva

; y del enemigo X hacia A, un píxel
y_toward:
        cmp ey,x
        beq @r
        bcc @u
        inc ey,x
        rts
@u:     dec ey,x
@r:     rts

; un paso (cada 2 cuadros) sin caerse por el borde ni atravesar paredes
walk_edge:
        lda frame
        and #1
        bne @r
        lda exl,x
        sta tx
        lda exh,x
        sta tx+1
        lda edir,x
        bne @lf
        lda tx
        clc
        adc #8
        sta tx
        bcc @ck
        inc tx+1
        bcs @ck
@lf:    lda tx
        bne *+4
        dec tx+1
        dec tx
@ck:    lda ey,x
        stx cur
        jsr t_solid_a
        ldx cur
        bcc @turn
        lda ey,x
        sec
        sbc #6
        stx cur
        jsr t_solid_a
        ldx cur
        bcs @turn
        jmp vstep
@turn:  lda edir,x
        eor #1
        sta edir,x
@r:     rts

; ---------------------------------------------------------------
; pico: parábola (elife = velocidad vertical con signo)
e_pick: inc et,x
        lda et,x
        lsr a
        lsr a
        and #3
        sta efr,x
        jsr vstep
        jsr vstep
        lda et,x
        and #3
        bne @g
        inc elife,x         ; gravedad
@g:     lda ey,x
        clc
        adc elife,x
        sta ey,x
        cmp #200
        bcs @gone
        lda et,x
        cmp #120
        bcs @gone
        rts
@gone:  lda #0
        sta etyp,x
        rts

; ---------------------------------------------------------------
; estalactita: tiembla cuando Radu pasa debajo y cae
e_estal:
        lda est,x
        bne @s1
        jsr dist_x
        cmp #30
        bcs @r
        lda #1
        sta est,x
        lda #0
        sta et,x
        lda #16
        jmp sfx
@s1:    inc et,x
        cmp #1
        bne @fall
        lda et,x            ; tiembla
        and #1
        beq @j
        inc exl,x
        bne @k
@j:     dec exl,x
@k:     lda et,x
        cmp #22
        bcc @r
        lda #2
        sta est,x
        rts
@fall:  lda ey,x
        clc
        adc #3
        sta ey,x
        cmp #200
        bcs @rot
        lda exl,x
        clc
        adc #3
        sta tx
        lda exh,x
        adc #0
        sta tx+1
        lda ey,x
        stx cur
        jsr t_solid_a
        ldx cur
        bcc @r
@rot:   lda #3              ; se hace añicos
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        lda #16
        jmp sfx
@r:     rts

; ---------------------------------------------------------------
; insecto venenoso: vuela en línea ondulada (elife = altura base)
e_insect:
        inc et,x
        lda frame
        lsr a
        lsr a
        and #1
        sta efr,x
        jsr vstep
        lda frame
        and #1
        beq @y
        jsr vstep
@y:     lda et,x
        and #31
        tay
        lda SIN32,y
        cmp #$80
        ror a
        cmp #$80
        ror a
        clc
        adc elife,x
        sta ey,x
        lda et,x
        cmp #160
        bcc @r
        lda #0
        sta etyp,x
@r:     rts
