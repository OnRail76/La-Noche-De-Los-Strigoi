; ===============================================================
; MOTOR · núcleo: arranque, VBI, espera de cuadro, mando
; El juego define:  vbi_juego  (se llama en cada VBI; puede ser un rts)
; Reglas (lecciones de Vórtice 5/6 y Zak Attack):
;  - la VBI usa SOLO sus temporales (vt); cld al entrar
;  - ATRACT = 0 en cada VBI: el Atari nunca entra en modo atracción
;  - los flancos de la palanca y del FIRE viven en variables propias
; ===============================================================
        .segment "ZEROPAGE"
frame:  .res 1              ; cuenta de cuadros (la sube la VBI)
tmp:    .res 8              ; temporales del programa principal
ptr:    .res 2
src:    .res 2
dst:    .res 2
vt:     .res 4              ; temporales SOLO de la VBI
stk:    .res 1              ; palanca: bit0 arriba, bit1 abajo, bit2 izq., bit3 der. (1 = pulsado)
stked:  .res 1              ; direcciones que se acaban de pulsar en este cuadro
stkold: .res 1
fire:   .res 1              ; 1 = FIRE pulsado
fireed: .res 1              ; 1 = FIRE se acaba de pulsar
fireold:.res 1

J_UP    = 1
J_DOWN  = 2
J_LEFT  = 4
J_RIGHT = 8

        .segment "CODE"
; arranque común: BASIC fuera, solo VBI, sonido y vídeo apagados, VBI diferida propia
m_init: cld
        lda PORTB           ; XL/XE: BASIC fuera, $A000-$BFFF = RAM
        ora #$02
        sta PORTB
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta AUDCTL
        sta stkold
        sta fireold
        lda #3
        sta SKCTL
        lda #7
        ldy #<m_vbi
        ldx #>m_vbi
        jsr SETVBV
        rts

m_vbi:  cld
        lda #0
        sta ATRACT          ; nunca entra el modo atracción
        inc frame
        jsr vbi_juego
.ifdef MUSICA
        jsr mus_tick        ; la música primero: los efectos la pisan en su canal
.endif
        jsr snd_tick
        jmp XITVBV

; espera al siguiente cuadro
m_wait: lda frame
@w:     cmp frame
        beq @w
        rts

; espera X cuadros
m_waitn:
        jsr m_wait
        dex
        bne m_waitn
        rts

; lee palanca y FIRE (una vez por cuadro)
m_mando:
        lda STICK0
        eor #15
        and #15
        sta stk
        lda stkold
        eor #$FF
        and stk
        sta stked
        lda stk
        sta stkold
        ldx #0
        lda STRIG0
        bne @nf
        inx
@nf:    stx fire
        lda fireold
        eor #1
        and fire
        sta fireed
        lda fire
        sta fireold
        rts

; copia X bytes de src a dst
m_copy: ldy #0
@l:     lda (src),y
        sta (dst),y
        iny
        dex
        bne @l
        rts

; llena X bytes de dst con A
m_fill: ldy #0
@l:     sta (dst),y
        iny
        dex
        bne @l
        rts
