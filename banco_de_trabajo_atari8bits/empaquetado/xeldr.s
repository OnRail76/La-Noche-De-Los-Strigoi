; ===============================================================
; SDI '86 · versión 130XE: cargador residente ($0700-$087F), misma interfaz que el disco y el cartucho.
;   LOADER ($0710): A = programa (0 título · 1-5 operaciones). Copia sus páginas desde la memoria
;   extendida (o desde la RAM bajo el SO) a $2000, página a página a través de un búfer en $0600
;   (el banco se ve en $4000-$7FFF, justo donde también hay que escribir), y salta a su arranque.
; ===============================================================
SETVBV  = $E45C
SYSVBV  = $E45F
XITVBV  = $E462
SDMCTL  = $022F
NMIEN   = $D40E
DMACTL  = $D400
AUDCTL  = $D208
AUDF1   = $D200
COLOR4  = $02C8
PORTB   = $D301
PERS    = $0580
NPROG   = 6
BUF     = $0600
src     = $CB
dst     = $CD

        .org $0700
        .byte "XE"
        jmp xboot               ; $0702
        .res $0710 - *, $EA
; ---------------------------------------------------------------
LOADER: sta prg                 ; $0710
        lda #0
        sta SDMCTL
        sta DMACTL
        lda #$40
        sta NMIEN
        lda #6
        ldy #<SYSVBV
        ldx #>SYSVBV
        jsr SETVBV
        lda #7
        ldy #<XITVBV
        ldx #>XITVBV
        jsr SETVBV
        lda #0
        ldx #7
@s:     sta AUDF1,x
        dex
        bpl @s
        sta AUDCTL
        sta COLOR4
        lda prg
        asl a
        clc
        adc prg
        asl a                   ; *6
        tax
        lda PTAB,x
        sta vp
        lda PTAB+1,x
        sta vp+1
        lda PTAB+2,x
        sta pcnt
        lda PTAB+3,x
        sta pcnt+1
        lda PTAB+4,x
        sta prun
        lda PTAB+5,x
        sta prun+1
        lda #0
        sta src
        sta dst
        lda #$20
        sta dst+1
@pg:    jsr vmap
        sta src+1
        sei
        lda #0
        sta NMIEN
        lda pb
        sta PORTB
        ldy #0
@c:     lda (src),y
        sta BUF,y
        iny
        bne @c
        lda #$FF                ; todo en su sitio: SO, sin BASIC, sin banco
        sta PORTB
        lda #$40
        sta NMIEN
        cli
@c2:    lda BUF,y
        sta (dst),y
        iny
        bne @c2
        inc dst+1
        inc vp
        bne @n
        inc vp+1
@n:     lda pcnt
        bne @d
        dec pcnt+1
@d:     dec pcnt
        lda pcnt
        ora pcnt+1
        bne @pg
        jmp (prun)

; página virtual vp -> A = página real, pb = PORTB
vmap:   lda vp+1
        bne @os
        lda vp
        lsr a
        lsr a
        lsr a
        lsr a
        and #$0C
        ora #$E3
        sta pb
        lda vp
        and #$3F
        ora #$40
        rts
@os:    lda #$FE
        sta pb
        lda vp
        cmp #16
        bcs @hi
        ora #$C0
        rts
@hi:    clc
        adc #$D8-16
        rts
; ---------------------------------------------------------------
xboot:  lda #$FF                ; SO, BASIC fuera, sin banco
        sta PORTB
        lda #$86                ; bloque compartido: válido, NORMAL, con cargador
        sta PERS
        ldx #33
        lda #0
@z:     sta PERS+1,x
        dex
        bpl @z
        lda #1
        sta PERS+1
        sta PERS+34
        lda #0
        jmp LOADER
prg:    .byte 0
pb:     .byte 0
vp:     .word 0
pcnt:   .word 0
prun:   .word 0
; tabla: página virtual, páginas, arranque (la rellena mkxe130.py)
        .res $0840 - *, 0
PTAB:   .res NPROG*6, 0
        .res $0880 - *, 0
