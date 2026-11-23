; ===============================================================
; MOTOR · efectos POKEY con prioridades (4 canales, AUDCTL = 0)
; El juego define las tablas por efecto (índice = número de efecto):
;   SX_CH canal 0-3 · SX_F frecuencia · SX_S paso de frecuencia por cuadro
;   SX_V volumen · SX_D duración · SX_C distorsión ($A0 tono, $80 ruido, $20...)
;   SX_P prioridad (1 = la más baja) · SX_K máscara de caída (el volumen baja cuando frame & SX_K = 0)
; Uso:  lda #efecto / jsr sfx      (conserva X e Y: se puede llamar dentro de bucles)
; snd_tick va en la VBI. Un efecto solo pisa otro de prioridad menor o igual.
; Con música (MUSICA = 1), los efectos pisan su canal mientras suenan y luego lo devuelven.
; ===============================================================
        .segment "HIBSS"
SDUR:   .res 4
SFRQ:   .res 4
SFST:   .res 4
SVOL:   .res 4
SCTL:   .res 4
SPRI:   .res 4
SDK:    .res 4
sfxx:   .res 1
sfxy:   .res 1

        .segment "CODE"
snd_off:
        lda #0
.ifdef MUSICA
        sta mplay
.endif
        ldx #7
@c:     sta AUDF1,x
        dex
        bpl @c
        ldx #3
@d:     sta SDUR,x
        sta SPRI,x
        dex
        bpl @d
        rts

sfx:    stx sfxx
        sty sfxy
        tay
        ldx SX_CH,y
        lda SX_P,y
        cmp SPRI,x
        bcc @r
        lda #0
        sta SDUR,x          ; la VBI no lo toca mientras se rellena
        lda SX_P,y
        sta SPRI,x
        lda SX_F,y
        sta SFRQ,x
        lda SX_S,y
        sta SFST,x
        lda SX_V,y
        sta SVOL,x
        lda SX_C,y
        sta SCTL,x
        lda SX_K,y
        sta SDK,x
        lda SX_D,y
        sta SDUR,x
@r:     ldx sfxx
        ldy sfxy
        rts

snd_tick:
        ldx #3
@l:     lda SDUR,x
        beq @off
        dec SDUR,x
        txa
        asl a
        tay
        lda SFRQ,x
        sta AUDF1,y
        lda SCTL,x
        ora SVOL,x
        sta AUDC1,y
        lda SFRQ,x
        clc
        adc SFST,x
        sta SFRQ,x
        lda frame
        and SDK,x
        bne @n
        lda SVOL,x
        beq @n
        dec SVOL,x
        jmp @n
@off:   lda #0
        sta SPRI,x
.ifdef MUSICA
        lda mplay           ; con música, el canal lo escribe el reproductor
        bne @n
.endif
        txa
        asl a
        tay
        lda #0
        sta AUDC1,y
@n:     dex
        bpl @l
        rts
