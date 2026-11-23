; ===============================================================
; CARGADOR DE MÓDULOS · versión XEX para 130XE (128 KB)
; Cada fase es un módulo: su código (en $8000) y sus tramos y arenas
; comprimidos (bajo el sistema operativo). Al cargar el XEX, los módulos
; van a los bancos de memoria extendida (xcopy); al empezar una fase,
; mod_load los copia a su sitio. Todo esto vive fuera de $4000-$7FFF,
; la ventana de los bancos.
; Registro de un módulo en su banco: destino (2), longitud (2), datos...;
; termina con un destino de página alta 0.
; ===============================================================
PB_NORMAL = $FF             ; OS dentro, BASIC fuera, banco extendido fuera
        .segment "LDR"
.ifdef MEDIO
        .include "cargador_medio.s"
.else

; A = módulo (1-5)
mod_load:
        tax
        lda MOD_LO-1,x
        sta lzs
        lda MOD_HI-1,x
        sta lzs+1
        lda MOD_BANK-1,x
        asl a
        asl a
        ora #$E2            ; banco, CPU en la memoria extendida, OS fuera
        sta ldpb
        sei
        lda #0
        sta NMIEN
        sta DMACTL
        sta GRACTL
        lda ldpb
        sta PORTB
        ldy #0
@rec:   lda (lzs),y         ; destino
        sta lzd
        iny
        lda (lzs),y
        sta lzd+1
        beq @fin
        iny
        lda (lzs),y         ; longitud
        sta lzm
        iny
        lda (lzs),y
        sta lzm+1
        lda lzs
        clc
        adc #4
        sta lzs
        bcc *+4
        inc lzs+1
        ldy #0
@cp:    lda lzm
        ora lzm+1
        beq @next
        lda (lzs),y
        sta (lzd),y
        inc lzs
        bne *+4
        inc lzs+1
        inc lzd
        bne *+4
        inc lzd+1
        lda lzm
        bne *+4
        dec lzm+1
        dec lzm
        jmp @cp
@next:  ldy #0
        jmp @rec
@fin:   lda #PB_NORMAL
        sta PORTB
        lda #$40
        sta NMIEN
        cli
        rts

; INIT durante la carga del XEX: $A000 = banco, destino en la ventana (2), longitud (2), datos
xcopy:  lda $A000
        asl a
        asl a
        ora #$E3            ; banco, CPU en la memoria extendida, OS dentro
        sei
        sta PORTB
        lda #<$A005
        sta lzs
        lda #>$A005
        sta lzs+1
        lda $A001
        sta lzd
        lda $A002
        sta lzd+1
        lda $A003
        sta lzm
        lda $A004
        sta lzm+1
        ldy #0
@cp:    lda lzm
        ora lzm+1
        beq @f
        lda (lzs),y
        sta (lzd),y
        inc lzs
        bne *+4
        inc lzs+1
        inc lzd
        bne *+4
        inc lzd+1
        lda lzm
        bne *+4
        dec lzm+1
        dec lzm
        jmp @cp
@f:     lda #PB_NORMAL
        sta PORTB
        cli
        rts

; INIT antes de nada: sin memoria extendida, aviso y alto (si no, los bancos
; se escribirían encima del programa)
xcheck: sei
        lda $7FFF
        sta ldpb
        lda #$E3            ; banco 0
        sta PORTB
        lda ldpb
        eor #$FF
        sta $7FFF
        lda #PB_NORMAL
        sta PORTB
        cli
        lda $7FFF
        cmp ldpb
        bne @no
        rts
@no:    lda ldpb
        sta $7FFF
        ldy #0
@m:     lda XMSG,y
        bmi @h
        sta ($58),y         ; pantalla del sistema (SAVMSC)
        iny
        bne @m
@h:     lda #$34
        sta $02C6           ; fondo rojo
@hl:    lda #0
        sta $4D             ; sin modo atracción
        jmp @hl
; "NECESITA UN 130XE (128 KB)" en códigos de pantalla
XMSG:   .byte $2E,$25,$23,$25,$33,$29,$34,$21,$00,$35,$2E,$00,$11,$13,$10,$38,$25
        .byte $00,$08,$11,$12,$18,$00,$2B,$22,$09,$FF
ldpb:   .res 1

        .include "modtab.inc"
.endif
        .segment "CODE"
