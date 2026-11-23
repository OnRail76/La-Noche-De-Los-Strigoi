; ===============================================================
; MOTOR · PMG con doble búfer (resolución de una línea)
; El juego define:
;   PMA, PMB   dos búferes de 2 KB alineados a 2 KB
;   PMY0, PMN  primera línea y número de líneas que se borran en cada cuadro
; Uso por cuadro:
;   jsr pm_wait     espera a que la VBI haya mostrado el cuadro anterior
;   ... lógica ...
;   jsr pm_begin    borra el búfer oculto (rb)
;   pm_spr / pm_mis y las tablas PHPx/PHMx/PSZM/PCPx en la entrada rb
;   jsr pm_end      el búfer queda listo; la VBI lo muestra
; La VBI (pm_vbi) solo cambia PMBASE, posiciones, tamaños y colores: nada se corta.
; Todo se redibuja cada cuadro: no quedan balas fantasma.
; ===============================================================
        .segment "ZEROPAGE"
shown:  .res 1              ; búfer en pantalla (0/1)
rb:     .res 1              ; búfer en preparación
ready:  .res 1              ; 1 = rb listo para mostrarse
pmhi:   .res 1              ; página base del búfer en preparación
pmdst:  .res 2
pmm:    .res 1              ; máscara del misil
pm_lastf: .res 1            ; cuadro del último pm_end
pm_lag: .res 2              ; cuadros perdidos (la lógica tardó más de un cuadro)

        .segment "HIBSS"
PHP0:   .res 2              ; posiciones horizontales por búfer
PHP1:   .res 2
PHP2:   .res 2
PHP3:   .res 2
PHM0:   .res 2
PHM1:   .res 2
PHM2:   .res 2
PHM3:   .res 2
PSZM:   .res 2              ; SIZEM por búfer
PCP0:   .res 2              ; colores de los players por búfer
PCP1:   .res 2
PCP2:   .res 2
PCP3:   .res 2

        .segment "CODE"
PMPAGE: .byte >PMA, >PMB
MBIT:   .byte $03, $0C, $30, $C0

; borra los dos búferes y deja visible el A
pm_init:
        lda #0
        tax
@c:     .repeat 8, K
        sta PMA+K*256,x
        sta PMB+K*256,x
        .endrepeat
        inx
        bne @c
        ldx #1
@h:     sta PHP0,x
        sta PHP1,x
        sta PHP2,x
        sta PHP3,x
        sta PHM0,x
        sta PHM1,x
        sta PHM2,x
        sta PHM3,x
        sta PSZM,x
        dex
        bpl @h
        sta shown
        sta ready
        lda #1
        sta rb
        lda #>PMA
        sta PMBASE
        rts

pm_wait:
        lda ready
        bne pm_wait
        rts

pm_end: lda #1
        sta ready
        lda frame           ; medida: cuadros desde el anterior pm_end
        sec
        sbc pm_lastf
        cmp #2
        bcc @ok
        inc pm_lag
        bne @ok
        inc pm_lag+1
@ok:    lda frame
        sta pm_lastf
        rts

pm_begin:
        lda shown
        eor #1
        sta rb
        tax
        lda PMPAGE,x
        sta pmhi
        lda #0
        sta PHP0,x
        sta PHP1,x
        sta PHP2,x
        sta PHP3,x
        sta PHM0,x
        sta PHM1,x
        sta PHM2,x
        sta PHM3,x
        sta PSZM,x
        txa
        bne pm_clrB
pm_clrA:
        lda #0
        ldx #PMN
@l:     sta PMA+$300+PMY0-1,x
        sta PMA+$400+PMY0-1,x
        sta PMA+$500+PMY0-1,x
        sta PMA+$600+PMY0-1,x
        sta PMA+$700+PMY0-1,x
        dex
        bne @l
        rts
pm_clrB:
        lda #0
        ldx #PMN
@l:     sta PMB+$300+PMY0-1,x
        sta PMB+$400+PMY0-1,x
        sta PMB+$500+PMY0-1,x
        sta PMB+$600+PMY0-1,x
        sta PMB+$700+PMY0-1,x
        dex
        bne @l
        rts

; dibuja un player: X = player (0-3), A = y, src = gráfico, Y = altura (1-128)
; conserva X
pm_spr: sta pmdst
        txa
        clc
        adc #4
        adc pmhi
        sta pmdst+1
        dey
@l:     lda (src),y
        sta (pmdst),y
        dey
        bpl @l
        rts

; dibuja un misil: X = misil (0-3), A = y, Y = altura (1-128); conserva X
pm_mis: pha
        lda MBIT,x
        sta pmm
        pla
; igual con la máscara ya puesta en pmm (dibujos parciales: rayas, destellos)
pm_misp:
        sta pmdst
        lda pmhi
        clc
        adc #3
        sta pmdst+1
        dey
@l:     lda (pmdst),y
        ora pmm
        sta (pmdst),y
        dey
        bpl @l
        rts

; VBI: muestra el búfer listo y aplica sus registros
pm_vbi: lda ready
        beq @n
        lda rb
        sta shown
        lda #0
        sta ready
@n:     ldx shown
        lda PMPAGE,x
        sta PMBASE
        lda PHP0,x
        sta HPOSP0
        lda PHP1,x
        sta HPOSP1
        lda PHP2,x
        sta HPOSP2
        lda PHP3,x
        sta HPOSP3
        lda PHM0,x
        sta HPOSM0
        lda PHM1,x
        sta HPOSM1
        lda PHM2,x
        sta HPOSM2
        lda PHM3,x
        sta HPOSM3
        lda PSZM,x
        sta SIZEM
        lda PCP0,x
        sta COLPM0
        lda PCP1,x
        sta COLPM1
        lda PCP2,x
        sta COLPM2
        lda PCP3,x
        sta COLPM3
        rts
