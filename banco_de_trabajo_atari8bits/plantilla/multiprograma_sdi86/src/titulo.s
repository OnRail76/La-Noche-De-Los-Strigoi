; ---------------------------------------------------------------
; SDI '86 · PROTOCOLO FINAL · Atari 8 bits (NTSC) · 2026 - Tony C. Ware
; PROGRAMA 0 · CARÁTULA, PANTALLA DE MANDO DE JANUS (menú) y RÉCORDS
; Elige la operación y la amenaza, las deja en el bloque compartido y llama al cargador.
; ---------------------------------------------------------------
        .include "hw.inc"
        .include "blk.inc"
MUSICA  = 1
MUS_TITULO   = 0
MUS_SUPERADA = 1
MUS_GAMEOVER = 2
DLI_N   = 40
DLTEXT  = $B680
TSCR    = $B800
FX_BEEP  = 0
FX_KLAX1 = 1
FX_KLAX2 = 2
FX_CLICK = 3
FX_TBOOM = 4
EXTRA_STEP = $06

        .segment "ZEROPAGE"
gmode:  .res 1              ; 0 texto · 2 pantalla de mando · 3 carátula
dif:    .res 1

        .segment "INITSEG"
init:   lda PORTB
        ora #$02
        sta PORTB
        rts

        .segment "CODE"
        .include "data0.s"
        .include "motor/nucleo.s"
        .include "motor/dli.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/pantalla.s"
        .include "motor/musica.s"
        .include "mando.s"

start:  jsr m_init
        lda #>CHARSET
        sta CHBAS
        lda #0
        sta gmode
        lda B_SIG           ; sin cargador (XEX suelto): bloque nuevo
        cmp #SIGV
        beq @ok
        lda #SIGV
        sta B_SIG
        lda #1
        sta B_DIF
        lda #0
        sta B_SEL
        sta B_CHEAT
        sta B_BOOT
        sta B_CHAIN
        sta B_LDR
        ldx #17
@z:     sta REC,x
        dex
        bpl @z
@ok:    lda B_DIF
        sta dif
        lda B_SEL
        sta sel
        lda B_BOOT
        bne @nc
        lda #1
        sta B_BOOT
        jsr cover           ; JANUS al encender (empieza la marcha)
        jmp mando
@nc:    lda #MUS_TITULO
        jsr mus_play
        jmp mando

vbi_juego:
        lda gmode
        cmp #2
        bne @g3
        jmp mando_vbi
@g3:    cmp #3
        bne @r
        jmp cover_vbi
@r:     rts

;        0 beep 1 klax1 2 klax2 3 clic 4 bum
SX_CH:  .byte 3,   3,   3,   3,   2
SX_F:   .byte $20, $1C, $28, $01, $60
SX_S:   .byte $FF, 0,   0,   0,   2
SX_V:   .byte 10,  12,  12,  5,   9
SX_D:   .byte 30,  8,   8,   2,   30
SX_C:   .byte $A0, $C0, $C0, $80, $80
SX_P:   .byte 4,   3,   3,   2,   2
SX_K:   .byte 7,   0,   0,   0,   3
