; SDI '86 · 130XE: arranque del XEX (RUNAD, en $2000). Pasa el cargador de $2100 a $0700-$087F
; (mientras se leía el fichero, ahí podía estar el DOS) y empieza.
        .org $2000
        ldx #0
@c:     lda $2100,x
        sta $0700,x
        cpx #$80
        bcs @n
        lda $2200,x
        sta $0800,x
@n:     inx
        bne @c
        jmp $0702
