; ===============================================================
; La Noche de los Strigoi · sectores de arranque del disco (3 × 128 bytes en $0700)
; Lee el cargador (sectores 4..) en $9C00 con el SIO del sistema y salta a él:
; el cargador trae el resto (fuente, programa, título y GAME OVER bajo el OS).
; ===============================================================
SIOV    = $E459
DDEVIC  = $0300
SDMCTL  = $022F
DMACTL  = $D400
PORTB   = $D301

        .org $0700
        .byte 0, 3
        .word $0700, $0706
        jmp boot                ; $0706
boot:   lda #0
        sta SDMCTL
        sta DMACTL
        lda PORTB               ; BASIC fuera ($A000-$BFFF = RAM)
        ora #$02
        sta PORTB
@rd:    ldx #11
@p:     lda DCB,x
        sta DDEVIC,x
        dex
        bpl @p
        jsr SIOV
        bmi @rd                 ; error: se repite
        inc DCB+5
        inc DCB+10
        dec nsec
        bne @rd
        jmp (dbootv)
; D1:, lectura de 256 bytes en $9C00 desde el sector 4
DCB:    .byte $31, 1, $52, $40, $00, $9C, 7, 0, 0, 1, 4, 0
nsec:   .byte 3                 ; sectores del cargador (mkmedio.py)
dbootv: .word 0                 ; entrada del cargador (mkmedio.py)
        .res $0880 - *, 0
