; ===============================================================
; MOTOR · carriles con scroll fino horizontal (ANTIC 4/5)
; Un carril es una franja de pantalla que se desliza entera: todo lo que hay en ella
; (barcos, aviones, explosiones) se mueve a la vez y sin coste de dibujo.
;  - Cada fila de carril es un anillo de 64 columnas escrito dos veces (128 bytes,
;    alineado a 128): la ventana de 48 bytes que lee ANTIC nunca da la vuelta.
;  - pos (8 bits, relojes de color) recorre el anillo entero: 64 columnas x 4 = 256.
;    LMS = anillo + pos/4 · HSCROL = 3 - (pos & 3).
;  - Columna de una x del campo: (x + pos + CAR_K) / 4.  x de una columna: col*4 - pos - CAR_K.
; El juego define:
;   NCAR           número de carriles
;   CAR_K          ajuste medido entre la x del campo y el anillo
;   CAR_NROWS, CROW_DL (desplazamiento del LMS en DLGAME), CROW_RL/CROW_RH (anillo), CROW_LANE
;   DLGAME         display list del juego
; ===============================================================
        .segment "HIBSS"
car_pos:  .res NCAR         ; posición (relojes de color)
car_frac: .res NCAR
car_sl:   .res NCAR         ; velocidad 8.8 (fracción)
car_sh:   .res NCAR         ; velocidad 8.8 (entero)
car_dir:  .res NCAR         ; 0: el contenido va a la izquierda · 1: a la derecha
car_posb: .res NCAR*2       ; posición congelada por búfer (la usa la VBI)
car_hs:   .res NCAR         ; HSCROL del cuadro mostrado
car_old:  .res 1

        .segment "CODE"
; X = carril. Mueve el carril; C = 1 si ha cambiado de columna
car_move:
        lda car_pos,x
        lsr a
        lsr a
        sta car_old
        lda car_dir,x
        bne @r
        lda car_frac,x
        clc
        adc car_sl,x
        sta car_frac,x
        lda car_pos,x
        adc car_sh,x
        sta car_pos,x
        jmp @c
@r:     lda car_frac,x
        sec
        sbc car_sl,x
        sta car_frac,x
        lda car_pos,x
        sbc car_sh,x
        sta car_pos,x
@c:     lsr a
        lsr a
        cmp car_old
        beq @s
        sec
        rts
@s:     clc
        rts

; X = carril, A = x del campo -> A = columna del anillo (0-63)
car_col:
        clc
        adc car_pos,x
        clc
        adc #CAR_K
        lsr a
        lsr a
        rts

; X = carril, A = columna -> A = x del campo (0-159 visible)
car_x:  asl a
        asl a
        sec
        sbc car_pos,x
        sec
        sbc #CAR_K
        rts

; escribe A en la columna Y del anillo dst (y en su copia +64); conserva X e Y
car_put:
        sta (dst),y
        pha
        tya
        ora #64
        tay
        pla
        sta (dst),y
        pha
        tya
        and #63
        tay
        pla
        rts

; programa principal: congela las posiciones para el búfer en preparación (rb)
car_freeze:
        ldx #NCAR-1
@l:     txa
        asl a
        ora rb
        tay
        lda car_pos,x
        sta car_posb,y
        dex
        bpl @l
        rts

; VBI: LMS de cada fila de carril y HSCROL de cada carril para el búfer mostrado
car_vbi:
        ldx #NCAR-1
@h:     txa
        asl a
        ora shown
        tay
        lda car_posb,y
        and #3
        eor #3
        sta car_hs,x
        dex
        bpl @h
        ldx #CAR_NROWS-1
@r:     lda CROW_LANE,x
        asl a
        ora shown
        tay
        lda car_posb,y
        lsr a
        lsr a
        clc
        adc CROW_RL,x
        ldy CROW_DL,x
        sta DLGAME,y
        lda CROW_RH,x
        sta DLGAME+1,y
        dex
        bpl @r
        rts
