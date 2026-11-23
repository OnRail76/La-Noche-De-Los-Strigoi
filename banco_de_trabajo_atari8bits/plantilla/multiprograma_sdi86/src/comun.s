; ===============================================================
; SDI '86 · COMÚN a las cinco operaciones: arranque, partida, marcador, mensajes, fase superada,
; paso a la operación siguiente (por el cargador), GAME OVER y récords.
;
; Cada operación (faseN.s) define FASE = N, incluye este fichero y aporta:
;   f_screen   monta su pantalla (display list, tablas de la DLI, juego de caracteres, PMG)
;   f_start    empieza (o repite, en la vuelta siguiente) la operación: enemigos, jugador, parámetros
;   f_frame    lógica de un cuadro; cuando cumple el objetivo llama a phase_done
;              (mientras pclear = 1 la operación no debe sacar enemigos nuevos)
;   f_render   dibuja el cuadro siguiente (pm_begin ... pm_end)
;   f_vbi      su parte de la VBI (carriles, scroll)
;   f_status   rellena su línea de estado en HUDB (las cifras; el texto ya está copiado)
;   y las tablas de efectos SX_* con, al menos, FX_EXTRA, FX_DEATH, FX_DEATH2, FX_KLAX1, FX_KLAX2, FX_BEEP
; Muerte del jugador: la operación llama a p_die (resta la vida y suena); su animación es cosa suya, y al
; acabarla llama a p_after: GAME OVER si no quedan vidas o, si quedan, vuelve con C = 1 para que reaparezca.
; ===============================================================
        .segment "ZEROPAGE"
gmode:  .res 1              ; 0 texto · 1 partida
mode:   .res 1              ; 0 ARCADE · 1-5 una operación suelta
dif:    .res 1              ; 0 FÁCIL · 1 NORMAL · 2 HARDCORE
cheat:  .res 1
loopn:  .res 1              ; vuelta (0 = primera)
lives:  .res 1
deaths: .res 1              ; muertes en esta vuelta (bonus sin bajas)
gover:  .res 1
pclear: .res 1              ; 1 = operación superada (fanfarria y bonus)
pctm:   .res 1
msgtm:  .res 1
msgid:  .res 1
hudd:   .res 1
klax:   .res 1              ; alarma: cuadros que le quedan

        .segment "INITSEG"
init:   lda PORTB           ; XL/XE: BASIC fuera, $A000-$BFFF = RAM
        ora #$02
        sta PORTB
        rts

        .segment "CODE"
; ---------------------------------------------------------------
start:  jsr m_init
        lda #<m_dli
        sta VDSLST
        lda #>m_dli
        sta VDSLST+1
        lda #>CHARSET
        sta CHBAS
        lda #0
        sta gmode
        jsr blk_in
        jsr mus_stop
        jsr snd_off
        ldx #39             ; marcadores en blanco hasta que se dibujen
        lda #0
@hc:    sta HUDT,x
        sta HUDB,x
        dex
        bpl @hc
        jsr f_screen
        jsr phase_start
play:   jsr pm_wait
        jsr m_mando
.ifdef RAPIDA                       ; solo para probar la cadena: cada operación se supera sola
        lda frame
        bne @rq
        jsr phase_done
@rq:
.endif
        jsr f_frame
        jsr clear_tick
        jsr msg_tick
        jsr hud_draw
        jsr klaxon
        jsr f_render
        lda gover
        beq play
        jmp gameover

vbi_juego:
        lda gmode
        bne @g
        rts
@g:     jsr pm_vbi
        jmp f_vbi

DLIVES: .byte 5, 3, 2

; ---------------------------------------------------------------
; bloque compartido -> partida
blk_in: lda B_SIG
        cmp #SIGV
        beq @ok
        ; sin cargador (XEX suelto): esta operación, NORMAL, récords a cero
        lda #SIGV
        sta B_SIG
        lda #1
        sta B_DIF
        sta B_BOOT
        lda #FASE
        sta B_MODE
        sta B_SEL
        lda #0
        sta B_CHEAT
        sta B_CHAIN
        sta B_LDR
        ldx #17
@z:     sta REC,x
        dex
        bpl @z
@ok:    lda B_DIF
        sta dif
        lda B_MODE
        sta mode
        lda B_CHEAT
        sta cheat
.ifdef PRUEBA
        lda #1
        sta cheat
.endif
        lda mode            ; récord de este modo
        asl a
        adc mode
        tax
        lda REC,x
        sta hisc
        lda REC+1,x
        sta hisc+1
        lda REC+2,x
        sta hisc+2
        lda #0
        sta gover
        lda B_CHAIN
        beq @new
        lda #0              ; viene de la operación anterior: conserva la partida
        sta B_CHAIN
        lda B_SCORE
        sta score
        lda B_SCORE+1
        sta score+1
        lda B_SCORE+2
        sta score+2
        lda B_NEXTX
        sta nextx
        lda B_NEXTX+1
        sta nextx+1
        lda B_NEXTX+2
        sta nextx+2
        lda B_LIVES
        sta lives
        lda B_LOOP
        sta loopn
        rts
@new:   lda #0
        sta score
        sta score+1
        sta score+2
        sta nextx
        sta nextx+1
.ifdef VUELTA0                      ; solo para pruebas: empezar en otra vuelta
        lda #VUELTA0
.endif
        sta loopn
        lda #$02            ; primera vida extra a 20.000
        sta nextx+2
        ldx dif
        lda DLIVES,x
        sta lives
        rts

; récord de este modo al bloque
rec_out:
        jsr hiupd
        lda mode
        asl a
        adc mode
        tax
        lda hisc
        sta REC,x
        lda hisc+1
        sta REC+1,x
        lda hisc+2
        sta REC+2,x
        rts

; ---------------------------------------------------------------
phase_start:
        lda #0
        sta pclear
        sta deaths
        lda #M_FASE
        ldx loopn
        beq @m
        lda #M_VUELTA
@m:     jsr msg
        lda #1
        sta hudd
        jmp f_start

; la operación ha cumplido su objetivo
phase_done:
        lda pclear
        bne @r
        lda #1
        sta pclear
        lda #255
        sta pctm
        lda #MUS_SUPERADA
        jsr mus_play
        lda #M_CLEAR
        jmp msg
@r:     rts

clear_tick:
        lda pclear
        beq @r
        dec pctm
        lda pctm
        cmp #128
        bne @n
        lda deaths
        bne @r
        lda #0
        ldx #$10            ; 1.000
        jsr addsc
        jsr extra
        lda #M_BONUS
        jmp msg
@n:     lda pctm
        bne @r
        jmp next_phase
@r:     rts

; siguiente: en ARCADE, la operación que sigue (tras JANUS, la 1 en la vuelta siguiente) por el cargador;
; suelta, la misma operación en la vuelta siguiente
next_phase:
        lda mode
        beq @ar
@one:   jsr loop_up
        jmp phase_start
@ar:    lda B_LDR
        beq @one            ; sin cargador (XEX suelto): se queda en esta operación
        ldx #FASE+1
        cpx #6
        bcc @go
        jsr loop_up
        ldx #1
@go:    stx B_PHASE
        lda #1
        sta B_CHAIN
        lda score
        sta B_SCORE
        lda score+1
        sta B_SCORE+1
        lda score+2
        sta B_SCORE+2
        lda nextx
        sta B_NEXTX
        lda nextx+1
        sta B_NEXTX+1
        lda nextx+2
        sta B_NEXTX+2
        lda lives
        sta B_LIVES
        lda loopn
        sta B_LOOP
        jsr rec_out
        jsr load_prep
        lda B_PHASE
        jmp LOADER

loop_up:
        lda loopn
        cmp #98
        bcs @x
        inc loopn
@x:     rts

; antes de saltar al cargador: silencio y pantalla apagada
load_prep:
        lda #0
        sta gmode
        jsr mus_stop
        jsr snd_off
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        rts

; ---------------------------------------------------------------
; mensajes del marcador de abajo
msg:    sta msgid
        lda #150
        sta msgtm
        lda #1
        sta hudd
        rts
msg_tick:
        lda msgtm
        beq @r
        dec msgtm
        bne @r
        lda #1
        sta hudd
@r:     rts

; vida extra si addsc devolvió C = 1
extra:  bcc @r
        inc lives
        lda #FX_EXTRA
        jsr sfx
        lda #M_VIDA
        jsr msg
@r:     rts

; suma puntos (A unidades/decenas, X centenas/millares, BCD) con vida extra
score_add:
        jsr addsc
        jsr extra
        lda #1
        sta hudd
        rts

; el jugador muere (el truco y la invulnerabilidad los mira la operación)
p_die:  dec lives
        inc deaths
        lda #1
        sta hudd
        lda #FX_DEATH
        jsr sfx
        lda #FX_DEATH2
        jmp sfx

; al acabar la animación de la muerte: C = 1 si reaparece, o GAME OVER
p_after:
        lda lives
        bne @y
        lda #1
        sta gover
        clc
        rts
@y:     sec
        rts

; ALARMA de oleada: dos tonos que se alternan cada 8 cuadros (la operación pone klax = 64)
klaxon: lda klax
        beq @r
        dec klax
        lda klax
        and #7
        bne @r
        lda klax
        and #8
        beq @a
        lda #FX_KLAX1
        jmp sfx
@a:     lda #FX_KLAX2
        jmp sfx
@r:     rts

; ---------------------------------------------------------------
; MARCADOR
hud_draw:
        lda hudd
        bne @go
        rts
@go:    lda #0
        sta hudd
        jsr hiupd
        lda #<HUD_TOP_T
        sta src
        lda #>HUD_TOP_T
        sta src+1
        lda #<HUDT
        sta dst
        lda #>HUDT
        sta dst+1
        ldx #40
        jsr m_copy
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(HUDT+HUD_SC)
        sta dst
        lda #>(HUDT+HUD_SC)
        sta dst+1
        lda #DIG0
        jsr put6
        lda #<hisc
        sta src
        lda #<(HUDT+HUD_HI)
        sta dst
        lda #>(HUDT+HUD_HI)
        sta dst+1
        lda #DIG0
        jsr put6
        lda lives
        cmp #10
        bcc @lv
        lda #9
@lv:    clc
        adc #DIG0
        sta HUDT+HUD_LV
        lda msgtm
        beq @st
        ldx msgid
        lda MSG_L,x
        sta src
        lda MSG_H,x
        sta src+1
        jmp @cp
@st:    lda #<HUD_BOT_T
        sta src
        lda #>HUD_BOT_T
        sta src+1
@cp:    lda #<HUDB
        sta dst
        lda #>HUDB
        sta dst+1
        ldx #40
        jsr m_copy
        lda msgtm
        bne @r
        lda #DIG0
        sta digb
        lda #<(HUDB+HUD_VU)
        sta dst
        lda #>(HUDB+HUD_VU)
        sta dst+1
        lda loopn
        clc
        adc #1
        jsr putdec2
        jmp f_status
@r:     rts

; dos cifras (A, 0-99) en la columna X de la línea de estado
st_dec2:
        stx tmp+7
        pha
        lda #DIG0
        sta digb
        lda tmp+7
        clc
        adc #<HUDB
        sta dst
        lda #>HUDB
        adc #0
        sta dst+1
        pla
        jmp putdec2

; C = 1 si se tocan las cajas tmp+0..3 (x0,x1,y0,y1) y tmp+4..7
boxhit: lda tmp+1
        cmp tmp+4
        bcc @no
        lda tmp+5
        cmp tmp+0
        bcc @no
        lda tmp+3
        cmp tmp+6
        bcc @no
        lda tmp+7
        cmp tmp+2
        bcc @no
        sec
        rts
@no:    clc
        rts

; SIZEM doble y cuádruple por misil
MSZ2:   .byte $01, $04, $10, $40
MSZ4:   .byte $03, $0C, $30, $C0

; ===============================================================
; GAME OVER
gameover:
        jsr rec_out
        lda #0
        sta gmode
        jsr snd_off
        lda #MUS_GAMEOVER
        jsr mus_play
        lda #<DESC_GO
        sta ptr
        lda #>DESC_GO
        sta ptr+1
        jsr txt_build
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(TSCR+2*20+T_PTS_D)
        sta dst
        lda #>(TSCR+2*20+T_PTS_D)
        sta dst+1
        lda #DIG0C0
        jsr put6
        lda #<hisc
        sta src
        lda #<(TSCR+3*20+T_REC_D)
        sta dst
        lda #>(TSCR+3*20+T_REC_D)
        sta dst+1
        lda #DIG0C3
        jsr put6
        lda #$0E
        sta COLOR0
        lda #$9A
        sta COLOR1
        lda #$34
        sta COLOR2
        lda #$1C
        sta COLOR3
        lda #$00
        sta COLOR4
        jsr txt_show
        ldx #120            ; 2 s sin poder saltarla
        jsr m_waitn
        lda #1
        sta fireold
@w:     jsr m_wait          ; hasta que acabe la marcha (o FIRE)
        jsr m_mando
        lda fireed
        bne @t
        lda mplay
        bne @w
        ldx #60
        jsr m_waitn
@t:     lda #0
        sta B_CHAIN
        lda B_LDR
        bne @ldr
        jmp start           ; XEX suelto: otra partida
@ldr:   jsr load_prep
        lda #0              ; a la pantalla de mando
        jmp LOADER

DESC_GO:
        .byte $70,$70,$70,$70,$70,$70,$70
        .byte 7, <T_GO, >T_GO
        .byte $70,$70
        .byte 6, <T_GO2, >T_GO2
        .byte $70,$70,$70,$70
        .byte 6, <T_PTS, >T_PTS
        .byte $70
        .byte 6, <T_REC, >T_REC
        .byte $FF

; ---------------------------------------------------------------
; pantalla de juego: apagar mientras se monta y encender (display list en DLGAME, DLI m_dli)
scr_off:
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta gmode
        jmp m_wait

scr_on: lda #0              ; marcador de arriba (sombras)
        sta COLOR4
        sta COLOR2
        sta COLOR0
        lda #$0E
        sta COLOR1
        lda #$1E            ; quinto player: todos los misiles en PF3
        sta COLOR3
        lda #$11
        sta GPRIOR
        lda #0              ; players a anchura normal: 1 px = 1 px de ANTIC 4
        sta SIZEP0
        sta SIZEP1
        sta SIZEP2
        sta SIZEP3
        lda #<m_dli
        sta VDSLST
        lda #>m_dli
        sta VDSLST+1
        lda #<DLGAME
        sta SDLSTL
        lda #>DLGAME
        sta SDLSTH
        lda #3
        sta GRACTL
        lda #1
        sta gmode
        sta hudd
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        jsr m_wait
        lda #$C0
        sta NMIEN
        rts

; copia X bloques de 220 bytes de src a dst (22 filas de 40 = 4 bloques)
cp220:  txa
        pha
        ldx #220
        jsr m_copy
        lda src
        clc
        adc #220
        sta src
        bcc @a
        inc src+1
@a:     lda dst
        clc
        adc #220
        sta dst
        bcc @b
        inc dst+1
@b:     pla
        tax
        dex
        bne cp220
        rts
