; ===============================================================
; MOTOR · pantallas de texto (título, GAME OVER, mensajes) en ANTIC 6/7
; Descriptor: lista de entradas terminada en $FF
;   byte con (b & $0F) = 0  -> línea en blanco de la display list (se copia tal cual: $00-$70)
;   byte 6 o 7, <texto, >texto -> línea de 20 caracteres (se copia el texto a TSCR)
; Las líneas de texto quedan en TSCR + 20*n (n = orden de aparición), para retocarlas luego.
; El juego define DLTEXT (lista, < 128 bytes) y TSCR.
; ===============================================================
        .segment "CODE"
; ptr = descriptor
txt_build:
        lda #<TSCR
        sta dst
        lda #>TSCR
        sta dst+1
        ldx #0
@n:     ldy #0
        lda (ptr),y
        cmp #$FF
        beq @end
        pha
        and #$0F
        bne @mode
        pla
        sta DLTEXT,x
        inx
        inc ptr
        bne @n
        inc ptr+1
        jmp @n
@mode:  pla
        ora #$40
        sta DLTEXT,x
        inx
        lda dst
        sta DLTEXT,x
        inx
        lda dst+1
        sta DLTEXT,x
        inx
        stx tmp
        ldy #1
        lda (ptr),y
        sta src
        iny
        lda (ptr),y
        sta src+1
        ldx #20
        jsr m_copy
        ldx tmp
        lda dst
        clc
        adc #20
        sta dst
        bcc @d
        inc dst+1
@d:     lda ptr
        clc
        adc #3
        sta ptr
        bcc @n
        inc ptr+1
        jmp @n
@end:   lda #$41
        sta DLTEXT,x
        lda #<DLTEXT
        sta DLTEXT+1,x
        lda #>DLTEXT
        sta DLTEXT+2,x
        rts

; enciende la pantalla de texto (sin DLI ni sprites). Los colores, en las sombras COLOR0-4.
txt_show:
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        jsr m_wait
        lda #0
        ldx #7
@h:     sta HPOSP0,x
        dex
        bpl @h
        lda #<DLTEXT
        sta SDLSTL
        lda #>DLTEXT
        sta SDLSTH
        jsr m_wait
        lda #$22
        sta SDMCTL
        rts
