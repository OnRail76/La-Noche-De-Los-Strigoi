        .segment "MOD2"
; ---------------------------------------------------------------
; IELE (tipo 9): espíritus del aire que giran alrededor de Radu,
; cerrando el círculo; al rato se marchan
; ---------------------------------------------------------------
e_iele: inc et,x
        bne *+5
        inc est,x           ; est cuenta vueltas de 256 cuadros
        lda frame
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        lda est,x           ; una vuelta y se marcha
        cmp #1
        bcc @orb
        dec ey,x            ; se va volando
        dec ey,x
        lda ey,x
        cmp #48
        bcs @r
        lda #0
        sta etyp,x
@r:     rts
@orb:   ; ángulo = et/2 (32 pasos)
        lda et,x
        lsr a
        and #31
        tay
        lda SIN32+8,y       ; coseno
        jsr irad
        clc
        adc rxl
        sta tx
        lda hitr            ; signo extendido
        adc rxh
        sta tx+1
        lda SIN32,y
        cmp #$80
        ror a               ; seno / 2
        jsr irad
        clc
        adc ry
        sec
        sbc #30
        sta tyy
        ; x hacia el objetivo, 2 px por cuadro
        ldy #2
@mx:    lda exh,x
        cmp tx+1
        bne @dx
        lda exl,x
        cmp tx
        beq @my
@dx:    bcc @rt
        lda exl,x
        bne *+5
        dec exh,x
        dec exl,x
        jmp @nx
@rt:    inc exl,x
        bne *+5
        inc exh,x
@nx:    dey
        bne @mx
@my:    lda ey,x
        cmp tyy
        beq @rr
        bcc @dn
        dec ey,x
        rts
@dn:    inc ey,x
@rr:    rts
; A = desplazamiento (-32..32) -> escalado por el radio (se cierra con el tiempo); hitr = signo
irad:   sta hitl
        lda est,x
        bne @k1
        lda hitl            ; primera vuelta: x 1,5
        cmp #$80
        ror a
        clc
        adc hitl
        jmp @sg
@k1:    lda hitl            ; segunda: x 1
@sg:    sta hitl
        lda #0
        bit hitl
        bpl *+4
        lda #$FF
        sta hitr
        lda hitl
        rts

; ---------------------------------------------------------------
; GÁRGOLA (tipo 10): estatua de piedra en una cornisa; al acercarse Radu
; despierta, pasea por su tejado sin caerse y se para a escupir piedras.
; Aguanta dos golpes.
; ---------------------------------------------------------------
e_garg: lda est,x
        bne @s1
        lda #0
        sta efr,x
        jsr dist_x
        cmp #64
        bcc *+5
        jmp @r
        lda #1
        sta est,x
        lda #0
        sta et,x
        lda #19
        jmp sfx
@s1:    inc et,x
        cmp #1
        bne @s2
        lda et,x            ; despierta
        cmp #24
        bcs *+5
        jmp @r
        jsr face_radu
        lda #2
        sta est,x
        lda #0
        sta et,x
        lda #17
        jmp sfx
@s2:    cmp #2
        beq @walk
        jmp @aim
@walk:  lda et,x            ; pasos: fotogramas 1 / 3
        lsr a
        lsr a
        lsr a
        and #1
        asl a
        ora #1
        sta efr,x
        lda frame
        and #1
        bne @tw
        ; ¿borde o pared delante?
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
@ck:    lda ey,x            ; suelo delante
        stx cur
        jsr t_solid_a
        ldx cur
        bcc @turn
        lda ey,x            ; pared delante
        sec
        sbc #6
        stx cur
        jsr t_solid_a
        ldx cur
        bcs @turn
        jsr vstep
        jmp @tw
@turn:  lda edir,x
        eor #1
        sta edir,x
@tw:    lda et,x            ; cada rato se para a escupir
        cmp #70
        bcc @r
        lda #3
        sta est,x
        lda #0
        sta et,x
@r:     rts
@aim:   lda #2
        sta efr,x
        jsr face_radu
        lda et,x
        cmp #18
        bcc @r
        lda #2
        sta est,x
        lda #0
        sta et,x
        ; piedra en el otro hueco, si está libre
        txa
        eor #1
        tay
        lda etyp,y
        bne @r
        lda #13
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
        sbc #8
        sta ey,y
        lda ry              ; apunta a la altura del pecho de Radu
        sec
        sbc #12
        sta elife,y
        lda #12
        jmp sfx

; piedra (tipo 13): recta hacia donde estaba Radu
e_stone:
        inc et,x
        lda et,x
        cmp #100
        bcc @m
        lda #0
        sta etyp,x
        rts
@m:     jsr vstep
        jsr vstep
        lda ey,x
        cmp elife,x
        beq @r
        bcc @dn
        dec ey,x
        rts
@dn:    inc ey,x
@r:     rts

