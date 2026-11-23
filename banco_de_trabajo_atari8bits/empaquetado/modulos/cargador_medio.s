; ===============================================================
; CARGADOR DE MÓDULOS · disco (MEDIO=1, ATR) y cartucho (MEDIO=2, AtariMax 8 Mbit)
; Los módulos son los mismos flujos de registros que en el XEX de 130XE
; (destino, longitud, datos...; termina con un destino de página alta 0),
; pero se leen del disco por sectores de 256 bytes o de los bancos de 8 KB
; del cartucho. El arranque usa el mismo lector para el «módulo 0»: fuente,
; programa residente y los paquetes fijos (título y GAME OVER) bajo el OS.
; ===============================================================
PB_OSOFF = $FE              ; OS fuera, BASIC fuera
CRITIC   = $0042
SDMCTLS  = $022F
LBUF     = $9F00            ; disco: búfer de un sector (última página del cargador)

; A = módulo (1-5)
mod_load:
        tax
        lda MOD_A-1,x
        sta ldpos
        lda MOD_B-1,x
        sta ldpos+1
        jsr snd_off
        lda SDMCTLS
        sta ldsd
        jsr flujo
        lda ldsd
        sta SDMCTLS
        lda #0
        sta AUDCTL
        lda #3
        sta SKCTL
        rts

; analiza la página (lzs); C = 1 al acabar el flujo
feed:   ldy #0
@b:     lda (lzs),y
        ldx ldst
        beq @s0
        dex
        beq @s1
        dex
        beq @s2
        dex
        beq @s3
        ldx #0              ; datos
        sta (lzd,x)
        inc lzd
        bne *+4
        inc lzd+1
        lda lzm
        bne *+4
        dec lzm+1
        dec lzm
        lda lzm
        ora lzm+1
        bne @nx
        sta ldst            ; registro terminado
        beq @nx
@s0:    sta lzd
        inc ldst
        bne @nx
@s1:    sta lzd+1
        cmp #0
        beq @fin
        inc ldst
        bne @nx
@s2:    sta lzm
        inc ldst
        bne @nx
@s3:    sta lzm+1
        inc ldst
@nx:    iny
        bne @b
        clc
        rts
@fin:   sec
        rts

.if MEDIO = 1
; ---------------------------------------------------------------
; DISCO: ldpos = primer sector. Cada sector se lee con el SIO del sistema
; (OS dentro, VBI activa) y se analiza con el OS fuera y sin NMI.
DDEVIC = $0300
SIOV   = $E459
flujo:  lda #0
        sta ldst
        sta SDMCTLS
        sta DMACTL
        sta GRACTL
        lda #<LBUF
        sta lzs
@rd:    lda #$40
        sta NMIEN
        cli
        ldx #11
@p:     lda SIOR,x
        sta DDEVIC,x
        dex
        bpl @p
        lda ldpos
        sta DDEVIC+10
        lda ldpos+1
        sta DDEVIC+11
        jsr SIOV
        bmi @rd             ; error: se repite
        sei
        lda #0
        sta NMIEN
        lda #PB_OSOFF
        sta PORTB
        lda #>LBUF
        sta lzs+1
        jsr feed
        lda #PB_NORMAL
        sta PORTB
        bcs @end
        inc ldpos
        bne @rd
        inc ldpos+1
        bne @rd
@end:   lda #$40
        sta NMIEN
        cli
        rts
; bloque del SIO: D1:, lectura de 256 bytes en LBUF
SIOR:   .byte $31, 1, $52, $40, <LBUF, >LBUF, 7, 0, 0, 1, 0, 0

; arranque: el sector de arranque ya ha cargado este cargador en $9C00
dboot:  lda BOOT_A
        sta ldpos
        lda BOOT_B
        sta ldpos+1
        jsr flujo
        jmp start
.else
; ---------------------------------------------------------------
; CARTUCHO: ldpos = banco, ldpos+1 = página en la ventana $A0-$BF.
; Todo con NMI apagadas: el SO vigila TRIG3 mientras el cartucho está dentro.
CBANK  = $D500
COFF   = $D580
TRIG3  = $D013
GINTLK = $03FA
flujo:  sei
        lda #0
        sta NMIEN
        sta ldst
        sta lzs
        sta SDMCTLS
        sta DMACTL
        sta GRACTL
        lda ldpos+1
        sta lzs+1
@pg:    ldx ldpos
        sta CBANK,x
        lda #PB_OSOFF
        sta PORTB
        jsr feed
        lda #PB_NORMAL
        sta PORTB
        bcs @end
        inc lzs+1
        lda lzs+1
        cmp #$C0
        bne @pg
        lda #$A0
        sta lzs+1
        inc ldpos
        bne @pg
@end:   sta COFF            ; cartucho fuera: $A000-$BFFF vuelve a ser RAM
        lda TRIG3
        sta GINTLK
        lda #$40
        sta NMIEN
        cli
        rts

; arranque: el banco 0 ha copiado este cargador en $9C00
cboot:  lda BOOT_A
        sta ldpos
        lda BOOT_B
        sta ldpos+1
        jsr flujo
        jmp start
.endif

ldpos:  .res 2
ldst:   .res 1
ldsd:   .res 1
; tablas que rellena tools/mkmedio.py: arranque y módulos 1-5
; (disco: sector, 2 bytes · cartucho: banco y página $A0-$BF)
BOOT_A: .byte 0
BOOT_B: .byte 0
MOD_A:  .res 5
MOD_B:  .res 5
