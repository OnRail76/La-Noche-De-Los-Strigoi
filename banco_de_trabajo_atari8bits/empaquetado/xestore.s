; ===============================================================
; SDI '86 · versión 130XE en un solo XEX: rutina de guardado (INITAD de cada trozo, en $0600)
;   Cada trozo del XEX trae hasta 32 páginas en $2000-$3FFF y sus datos en XPAR:
;   página virtual de inicio (2 bytes) y número de páginas. Esta rutina las guarda en la
;   memoria extendida del 130XE (páginas virtuales 0-255: bancos 0-3 en $4000-$7FFF) o, desde la
;   256, en la RAM que hay bajo el sistema operativo ($C000-$CFFF y $D800-$FFFF).
;   La primera llamada (XCHK) comprueba que hay 128 KB.
; ===============================================================
PORTB   = $D301
NMIEN   = $D40E
SAVMSC  = $58
src     = $CB
dst     = $CD

        .org $0600
        jmp xstore              ; $0600: guardar un trozo
        jmp xchk                ; $0603: comprobar 130XE
; ---------------------------------------------------------------
xstore: lda #$00
        sta src
        sta dst
        lda #$20
        sta src+1
        lda XPAR+2
        sta cnt
@pg:    jsr vmap                ; PORTB y página de destino de la página virtual XPAR
        sta dst+1
        sei
        lda #0
        sta NMIEN
        lda pb
        sta PORTB
        ldy #0
@c:     lda (src),y
        sta (dst),y
        iny
        bne @c
        lda #$FF
        sta PORTB
        lda #$40
        sta NMIEN
        cli
        inc src+1
        inc XPAR
        bne @n
        inc XPAR+1
@n:     dec cnt
        bne @pg
        rts

; página virtual XPAR -> A = página real, pb = valor de PORTB
vmap:   lda XPAR+1
        bne @os
        lda XPAR                ; banco = v / 64
        lsr a
        lsr a
        lsr a
        lsr a
        and #$0C                ; (v >> 6) << 2
        ora #$E3                ; bit 4 = 0: la CPU ve el banco en $4000-$7FFF
        sta pb
        lda XPAR
        and #$3F
        ora #$40
        rts
@os:    lda #$FE                ; SO fuera
        sta pb
        lda XPAR
        cmp #16
        bcs @hi
        ora #$C0
        rts
@hi:    clc
        adc #$D8-16
        rts

; ---------------------------------------------------------------
xchk:   lda #$E3                ; banco 0
        sta PORTB
        lda #$5A
        sta $4000
        lda #$FF
        sta PORTB
        lda #$A5
        sta $4000
        lda #$E3
        sta PORTB
        ldx $4000
        lda #$FF
        sta PORTB
        cpx #$5A
        bne @no
        rts
@no:    ldy #0                  ; sin 128 KB: aviso y alto
@m:     lda MSG,y
        cmp #$FF
        beq *
        sta (SAVMSC),y
        iny
        bne @m
MSG:    .byte $33,$24,$29,$00,$07,$18,$16,$00,$2E,$25,$23,$25,$33,$29,$34,$21,$00,$35,$2E,$00,$21,$34,$21,$32,$29,$00,$11,$13,$10,$38,$25,$00,$08,$11,$12,$18,$00,$2B,$22,$09,$FF   ; "SDI '86 NECESITA UN ATARI 130XE (128 KB)" (códigos internos)
pb:     .byte 0
cnt:    .byte 0
        .res $06F0 - *, 0
XPAR:   .res 3, 0
