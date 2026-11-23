; ===============================================================
; La Noche de los Strigoi · cartucho AtariMax 8 Mbit · banco de arranque
; (banco 0, copiado también en el 127). Copia el cargador a $9C00 y salta a él:
; el cargador lee de los bancos el resto del juego y desconecta el cartucho.
; ===============================================================
        .org $A000
cstart: sei
        lda #0
        sta $D40E               ; sin NMI
        sta $022F
        sta $D400
        lda $D301               ; BASIC fuera
        ora #$02
        sta $D301
        ldx #0
@c:     lda ldr,x
        sta $9C00,x
        lda ldr+$100,x
        sta $9D00,x
        lda ldr+$200,x
        sta $9E00,x
        inx
        bne @c
        jmp (cbootv)
cinit:  rts
cbootv: .word 0                 ; entrada del cargador (mkmedio.py)
ldr:    .incbin "build/ldr_cart.bin"
        .res $BFFA - *, $FF
        .word cstart            ; $BFFA arranque
        .byte 0                 ; $BFFC cartucho presente
        .byte $04               ; $BFFD arrancar el cartucho (sin disco)
        .word cinit             ; $BFFE inicialización
