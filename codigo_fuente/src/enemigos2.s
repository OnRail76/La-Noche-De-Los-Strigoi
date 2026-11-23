; ===============================================================
; ENEMIGOS DE LOS TRAMOS NUEVOS
;  6 murciélago de viga · 8 Vâvâma · 9 Iele · 10 gárgola
; ===============================================================

; aparición programada genérica: X = índice de la tabla del tramo
spawn_x:
        lda SP_TYP,x
        pha
        lda SP_COL,x
        sta zcol
        lda SP_Y,x
        sta tyy
        jsr free_slot
        pla
        bcs *+3
        rts
        cmp #9              ; nunca dos Iele a la vez
        bne @one
        ldy etyp
        cpy #9
        beq @no
        ldy etyp+1
        cpy #9
        bne @one
@no:    rts
@one:   sta etyp,x
        ldy #2
        cmp #21             ; el caballero aguanta tres
        bne *+4
        ldy #3
        tya
        sta ehp,x
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        sta edir,x
        lda zcol
        asl a
        asl a
        sta exl,x
        lda zcol
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        sta exh,x
        lda tyy
        sta ey,x
        lda #200
        sta elife,x
        rts

; A = |x enemigo - x Radu| (255 si es mayor)
dist_x: lda exl,x
        sec
        sbc rxl
        sta tx
        lda exh,x
        sbc rxh
        bcs @p
        ; negativo
        eor #$FF
        sta tx+1
        lda tx
        eor #$FF
        clc
        adc #1
        sta tx
        lda tx+1
        adc #0
@p:     beq @lo
        lda #255
        rts
@lo:    lda tx
        rts

; mueve el enemigo X un píxel hacia Radu en x
step_to_radu:
        lda exh,x
        cmp rxh
        bne @d
        lda exl,x
        cmp rxl
        beq @r
@d:     bcc @rt
        lda exl,x
        bne *+5
        dec exh,x
        dec exl,x
        lda #1
        sta edir,x
@r:     rts
@rt:    inc exl,x
        bne *+5
        inc exh,x
        lda #0
        sta edir,x
        rts

; ---------------------------------------------------------------
; murciélago: colgado de la viga hasta que Radu pasa cerca
e_bat:  lda est,x
        bne @fly
        lda #2
        sta efr,x
        jsr dist_x
        cmp #44
        bcs @r
        lda #1
        sta est,x
        lda #0
        sta et,x
        sta efr,x
        lda #5
        jmp sfx
@fly:   inc et,x
        lda frame
        and #7
        bne @nf
        lda efr,x
        eor #1
        and #1
        sta efr,x
@nf:    lda et,x
        cmp #200
        bcc @mv
        dec ey,x            ; se marcha hacia arriba
        dec ey,x
        lda ey,x
        cmp #48
        bcs @r
        lda #0
        sta etyp,x
@r:     rts
@mv:    lda frame
        and #3
        beq @y
        jsr step_to_radu
@y:     lda frame
        and #1
        bne @r
        lda ry
        sec
        sbc #26
        sta tyy
        lda et,x
        and #16
        beq @b
        lda tyy
        sec
        sbc #8
        sta tyy
@b:     lda tyy
        cmp ey,x
        beq @r
        bcc @up
        inc ey,x
        rts
@up:    dec ey,x
        rts

BATS:   .byte $81,$C3,$E7,$7E,$3C,$18,$00,$00
        .byte $00,$24,$66,$FF,$BD,$18,$00,$00
        .byte $18,$3C,$7E,$7E,$5A,$3C,$18,$00   ; colgado, alas plegadas
COL_BAT = $08

vstep:  lda edir,x
        bne @l
        inc exl,x
        bne @r
        inc exh,x
@r:     rts
@l:     lda exl,x
        bne *+5
        dec exh,x
        dec exl,x
        rts

SIN32:  .byte 0,6,12,18,23,27,30,31,32,31,30,27,23,18,12,6
        .byte 0,250,244,238,233,229,226,225,224,225,226,229,233,238,244,250
        .byte 0,6,12,18,23,27,30,31

; ---------------------------------------------------------------
; caja y dibujo de los tipos 8+
; ---------------------------------------------------------------
EMINST: .byte 2,0,2,0,0,0,2,0,0,1,0,0,0,0,0,0,0   ; estado mínimo para golpear / tocar
ebox2:  tay
        lda est,x
        cmp EMINST-8,y
        bcc @no
        cpy #8              ; la Vâvâma escondida otra vez no cuenta
        bne @ok
        cmp #4
        bcs @no
@ok:    lda ey,x
        sta hitb
        sec
        sbc EHGT-8,y
        sta hitt
        sec
        rts
@no:    clc
        rts

e_draw2:
        tay
        cpy #14
        bcc @t8
        jmp e_col3
@t8:
        lda est,x           ; colores y visibilidad por tipo
        cpy #8
        bne @c9
        cmp #0
        beq @rr
        cmp #4
        beq @rr
        cmp #1
        bne @v
        lda frame
        and #2
        beq @rr
@v:     lda #$BA
        bne e2_col
@rr:    rts
@c9:    cpy #9
        bne @c10
        lda frame
        and #1
        beq @i1
        lda #$0E
        bne e2_col
@i1:    lda #$5C
        bne e2_col
@c10:   cpy #11
        bne @c12
        lda #$28            ; tijeras oxidadas
        bne e2_col
@c12:   cpy #12
        bne @c13
        lda #$0E            ; aguja de hierro
        bne e2_col
@c13:   cpy #13
        bne @c10b
        lda #$08            ; piedra
        bne e2_col
@c10b:  lda est,x
        cmp #0
        bne @g1
        lda #$06            ; piedra
        bne e2_col
@g1:    cmp #3              ; a punto de escupir: parpadea
        beq @gf
        cmp #1
        bne @g2
@gf:
        lda frame
        and #4
        beq *+6
        lda #$36
        bne e2_col
        lda #$06
        bne e2_col
@g2:    lda #$08
e2_col: jsr e_color
        lda etyp,x
        sec
        sbc #8
        tay
        lda ESPR_LO,y
        sta src
        lda ESPR_HI,y
        sta src+1
        lda efr,x
        sta hitl
@f:     lda hitl
        beq @d
        lda src
        clc
        adc EHGT,y
        sta src
        bcc *+4
        inc src+1
        dec hitl
        jmp @f
@d:     lda ey,x
        sec
        sbc EHGT,y
        pha
        lda EHGT,y
        tay
        pla
        jmp e_put


; colores de los tipos 14-18 (rts si no se dibuja)
e_col3: lda est,x
        cpy #14
        bne @v
        cmp #0              ; Moroi: invisible / parpadea / sólido
        beq @no
        cmp #2
        beq @m
        lda frame
        and #2
        beq @no
@m:     lda #$9C
        jmp e2_col
@v:     cpy #15
        bne @p
        lda #$38            ; Vâlva Băii: cobre del candil
        jmp e2_col
@p:     cpy #16
        bne @e
        lda #$0A
        jmp e2_col
@e:     cpy #17
        bne @i
        lda #$0E            ; estalactita de sal
        jmp e2_col
@i:     cpy #18
        bne @l
        lda #$C8            ; insectos
        jmp e2_col
@l:     cpy #19
        bne @f
        lda #$16            ; lupari: pardo
        jmp e2_col
@f:     cpy #20
        bne @k
        lda frame           ; fuego fatuo: cambia de color
        asl a
        asl a
        asl a
        asl a
        ora #$0A
        jmp e2_col
@k:     cpy #21
        bne @o
        lda #$06            ; caballero no muerto
        jmp e2_col
@o:     cpy #22
        bne @o2
        lda #$02            ; murciélagos del título
        jmp e2_col
@o2:    lda #$0E            ; onda de choque · calavera
        jmp e2_col
@no:    rts                 ; no se dibuja
        .include "spr2.s"

