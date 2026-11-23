; ===============================================================
; MÓDULO 4 · EL PASO DE LOS CÁRPATOS
; Lupari (licántropos que corren a por ti), fuegos fatuos (cambian los
; mandos), el Căpcăun y, tras él, el Rey Strigoi alado.
; ===============================================================
        .segment "MOD4"
; lupari (tipo 19): corre hacia Radu sin despeñarse y salta cuando está cerca
e_lupari:
        inc et,x
        bne @vive           ; tras unos segundos se va al bosque
        lda #0
        sta etyp,x
        rts
@vive:  lda et,x
        lsr a
        lsr a
        and #1
        sta efr,x
        lda est,x
        bne @jump
        lda et,x
        and #31
        bne @run
        jsr face_radu
@run:   jsr walk_edge
        jsr walk_edge
        lda frame
        and #1
        beq @r
        jsr walk_edge
        jsr walk_edge
        jsr dist_x
        cmp #28
        bcs @r
        lda #1              ; ¡salta!
        sta est,x
        lda #16
        sta elife,x
        lda #3
        jmp sfx
@jump:  jsr vstep
        dec elife,x
        lda elife,x
        cmp #8
        bcc @dn
        dec ey,x
        dec ey,x
@r:     rts
@dn:    inc ey,x
        inc ey,x
        lda elife,x
        bne @r
        lda #0
        sta est,x
        rts

; fuego fatuo (tipo 20): flota ondulando y se acerca; si te toca, cambia los mandos
e_fatuo:
        inc et,x
        lda et,x
        bne *+5
        jmp @gone
        lda frame
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        lda est,x
        bne @f
        lda ey,x
        sta elife,x
        lda #1
        sta est,x
@f:     lda frame
        and #3
        bne @y
        jsr step_to_radu
@y:     lda et,x
        lsr a
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
        rts
@gone:  lda #0
        sta etyp,x
        rts

; el Căpcăun: ondas con el fémur, huesos en parábola y alguna lluvia
GP4:    .byte PK_AR4, G4_S1, G4_S2, G4_S3
        .word G4_BLK
        .byte G4_R, G4_C, G4_W, G4_H
        .word 0
        .byte G4_HL, G4_HR, G4_HT, G4_HB, G4_BL, G4_BR, G4_BT, G4_BB
        .byte 14
        .word ATK4
        .byte 70, G4_AX, G4_AY
        .word arena5_go
        .byte 0, G4_RX
        .word arena4
ATK4:   .byte 4, 2, 4, 2, 4, 1, 0
arena4: lda #<GP4
        ldx #>GP4
        jmp garena

; el Rey Strigoi alado: fuego infernal en parábola, murciélagos y lluvia
GP5:    .byte PK_AR5, G5_S1, G5_S2, G5_S3
        .word G5_BLK
        .byte G5_R, G5_C, G5_W, G5_H
        .word 0
        .byte G5_HL, G5_HR, G5_HT, G5_HB, G5_BL, G5_BR, G5_BT, G5_BB
        .byte 16
        .word ATK5
        .byte 60, G5_AX, G5_AY
        .word fase5_start
        .byte 0, G5_RX
        .word arena5
ATK5:   .byte 2, 5, 2, 1, 3, 2, 5, 0
arena5: lda #<GP5
        ldx #>GP5
        jmp garena
