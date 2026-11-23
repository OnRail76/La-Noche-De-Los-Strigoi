; ===============================================================
; PANTALLAS: TÍTULO (logo + Sighișoara de noche) y GAME OVER
; (la calavera de Radu cae y bota; «HA GANADO LA NOCHE...»).
; Usan el motor de las arenas: pantalla fija ASCR, DLI por fila y
; las tablas AT_* del paquete (siempre bajo el OS).
; ===============================================================
PK_TI   = 12
PK_GO   = 13
        .segment "HIBSS"
diff:   .res 1              ; 0 NORMAL · 1 HARDCORE
sc_t:   .res 1
sc_ph:  .res 1
go_vy:  .res 1
go_b:   .res 1
scr_tr: .res 1              ; primera entrada de las tablas que es texto
        .segment "CODE"

; plantillas de display list (en DLGAME)
TDLT:   .byte $70,$70,$C6,<TSCR,>TSCR
        .byte $C4,<ASCR,>ASCR
        .repeat 13
        .byte $84
        .endrepeat
        .byte $C6,<(TSCR+20),>(TSCR+20),$86,$10,$06
        .byte $41,<DLGAME,>DLGAME
TDLLEN = * - TDLT
GDLT:   .byte $70,$70,$F0
        .byte $C4,<ASCR,>ASCR
        .repeat 15
        .byte $84
        .endrepeat
        .byte $C6,<(TSCR+20),>(TSCR+20),$86,$10,$06
        .byte $41,<DLGAME,>DLGAME
GDLLEN = * - GDLT

; A = paquete, X/Y = plantilla (lo/hi), g_s1..g_s3 = juegos por fila
scr_prep:
        pha
        stx src
        sty src+1
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        sta SIZEP2
        sta SIZEP3
        jsr snd_off
        jsr m_wait
        pla
        jsr pack_load
        .assert TDLLEN = GDLLEN, error, "plantillas"
        ldy #TDLLEN-1
@dl:    lda (src),y
        sta DLGAME,y
        dey
        bpl @dl
        jsr arena_bg_all
        ldx #20
@dt:    lda AT_BK,x
        sta DTBK,x
        lda AT_PF0,x
        sta DTPF0,x
        lda AT_PF1,x
        sta DTPF1,x
        lda AT_PF2,x
        sta DTPF2,x
        lda AT_PF3,x
        sta DTPF3,x
        lda #>ARR
        cpx g_s3
        bcs @cb
        lda #>ARQ
        cpx g_s2
        bcs @cb
        lda #>ARP
        cpx g_s1
        bcs @cb
        lda #>ARA
@cb:    sta DTCH,x
        lda #0
        sta DTHS,x
        cpx scr_tr          ; renglones de texto de abajo
        bcc @nt
        lda #>CHARSA
        sta DTCH,x
        lda #$00
        sta DTBK,x
        lda #$0E
        sta DTPF0,x
        lda #$46
        sta DTPF1,x
        lda #$0A
        sta DTPF2,x
        lda #$04
        sta DTPF3,x
@nt:    dex
        bpl @dt
        ldx #79             ; texto en blanco
        lda #0
@cl:    sta TSCR,x
        dex
        bpl @cl
        lda #0
        sta etyp
        sta etyp+1
        sta bact
        sta dact
        sta dact+1
        sta dact+2
        sta dact+3
        sta camx
        sta camx+1
        sta rxh
        sta rst
        sta rpol
        sta rdir
        jsr pm_init
        lda #>ARA
        sta CHBAS
        lda #$0C
        sta COLOR0
        lda #$46
        sta COLOR1
        lda #$0A
        sta COLOR2
        lda #$00
        sta COLOR4
        lda #$31
        sta GPRIOR
        lda #<dli_arena
        sta VDSLST
        lda #>dli_arena
        sta VDSLST+1
        rts

scr_on: lda #<DLGAME
        sta SDLSTL
        lda #>DLGAME
        sta SDLSTH
        lda #3
        sta GRACTL
        lda #2
        sta gmode
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        lda #$C0
        sta NMIEN
        rts

; X = renglón (0-3), src = texto de 20 caracteres
scr_line:
        lda SCRL_LO,x
        sta dst
        lda #>TSCR
        sta dst+1
        ldx #20
        jmp m_copy
SCRL_LO: .byte <TSCR, <(TSCR+20), <(TSCR+40), <(TSCR+60)

; título y amanecer comparten la escena: prepara la pantalla del título
scr_titulo:
        lda #TI_S1
        sta g_s1
        lda #TI_S2
        sta g_s2
        lda #TI_S3
        sta g_s3
        lda #14
        sta scr_tr
        lda #PK_TI
        ldx #<TDLT
        ldy #>TDLT
        jsr scr_prep
        lda #TI_RX          ; Radu en su roca
        sta rxl
        lda #TI_RY
        sta ry
        lda #0
        sta rinv
        lda #22             ; murciélagos que cruzan la luna
        sta etyp
        sta etyp+1
        lda #20
        sta exl
        lda #110
        sta exl+1
        lda #90
        sta elife
        lda #100
        sta elife+1
        lda #0
        sta exh
        sta exh+1
        rts

; murciélagos del título: cruzan despacio, ondulando
bats_deco:
        ldx #1
@l:     lda frame
        and #1
        bne @y
        inc exl,x
        lda exl,x
        cmp #164
        bcc @y
        lda #0
        sta exl,x
@y:     lda frame
        clc
        adc SCRL_LO,x
        lsr a
        lsr a
        and #31
        tay
        lda SIN32,y
        cmp #$80
        ror a
        cmp #$80
        ror a
        clc
        adc elife,x
        sta ey,x
        lda frame
        lsr a
        lsr a
        lsr a
        and #1
        sta efr,x
        dex
        bpl @l
        rts

; ---------------------------------------------------------------
title:  jsr scr_titulo
        lda #<TT_TOP
        sta src
        lda #>TT_TOP
        sta src+1
        ldx #0
        jsr scr_line
        jsr ti_diff
        jsr ti_rec
        jsr scr_on
.ifdef MUS_TEST
        lda #MUS_TEST
.else
        lda #3
.endif
        jsr mus_play
        lda #0
        sta downs
        sta sc_t
        sta sc_ph
        lda #1
        sta fireold
@w:     jsr pm_wait
        jsr m_mando
        jsr bats_deco
        inc sc_t
        lda sc_t            ; «PULSA FIRE» parpadea
        and #31
        bne @nb
        lda sc_t
        and #32
        beq @f1
        lda #<TT_BLK
        ldx #>TT_BLK
        bne @f2
@f1:    lda #<TT_FIRE
        ldx #>TT_FIRE
@f2:    sta src
        stx src+1
        ldx #1
        jsr scr_line
@nb:    lda sc_t            ; récord y autor, alternando
        bne @nr
        inc sc_ph
        jsr ti_rec
@nr:    lda stked           ; dificultad con izquierda / derecha
        and #J_LEFT
        beq @nl
        lda #0
        beq @sd
@nl:    lda stked
        and #J_RIGHT
        beq @nd0
        lda #1
@sd:    sta diff
        jsr ti_diff
        lda #11
        jsr sfx
@nd0:   lda stked           ; truco: abajo, abajo, FIRE = invencible
        and #J_DOWN
        beq @nd
        inc downs
@nd:    lda stked
        and #(J_UP|J_LEFT|J_RIGHT)
        beq @nu
        lda #0
        sta downs
@nu:    jsr draw
        jsr pm_end
        lda fireed
        bne *+5
        jmp @w
        lda downs
        cmp #2
        bcc @go
        lda #1
        sta cheat
        jsr ti_rec
        lda #11
        jsr sfx
        lda #0
        sta downs
        jmp @w
@go:    jmp newgame

ti_diff:
        lda #<TT_D0
        ldx #>TT_D0
        ldy diff
        beq *+6
        lda #<TT_D1
        ldx #>TT_D1
        sta src
        stx src+1
        ldx #2
        jmp scr_line

; renglón 3: invencible / récord / autor
ti_rec: lda cheat
        beq @n
        lda #<TT_INV
        ldx #>TT_INV
        bne @c
@n:     lda sc_ph
        and #1
        bne @rec
        lda #<TT_AUT
        ldx #>TT_AUT
@c:     sta src
        stx src+1
        ldx #3
        jmp scr_line
@rec:   lda #<TT_REC
        sta src
        lda #>TT_REC
        sta src+1
        ldx #3
        jsr scr_line
        lda #<hisc
        sta src
        lda #0
        sta src+1
        lda #<(TSCR+60+REC_DIG)
        sta dst
        lda #>(TSCR+60+REC_DIG)
        sta dst+1
        lda #DIG0|$80
        jmp put6

; ---------------------------------------------------------------
gameover:
        jsr hiupd
        lda #GO_S1
        sta g_s1
        lda #GO_S2
        sta g_s2
        lda #GO_S3
        sta g_s3
        lda #16
        sta scr_tr
        lda #PK_GO
        ldx #<GDLT
        ldy #>GDLT
        jsr scr_prep
        lda #<GO_T1
        sta src
        lda #>GO_T1
        sta src+1
        ldx #1
        jsr scr_line
        lda #<GO_T2
        sta src
        lda #>GO_T2
        sta src+1
        ldx #2
        jsr scr_line
        lda #<T_PTS
        sta src
        lda #>T_PTS
        sta src+1
        ldx #3
        jsr scr_line
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(TSCR+60+TXT_DIG)
        sta dst
        lda #>(TSCR+60+TXT_DIG)
        sta dst+1
        lda #DIG0
        jsr put6
        lda #4              ; Radu no se ve
        sta rinv
        lda #24             ; la calavera grande (dos mitades de doble ancho)
        sta etyp
        sta etyp+1
        lda #0
        sta efr
        sta est
        sta est+1
        sta go_vy
        sta go_b
        lda #1
        sta efr+1
        sta SIZEP2
        sta SIZEP3
        lda #64
        sta exl
        lda #80
        sta exl+1
        lda #0
        sta exh
        sta exh+1
        lda #51
        sta ey
        sta ey+1
        jsr scr_on
        lda #5
        jsr mus_play
        lda #0
        sta sc_t
@w:     jsr pm_wait
        jsr m_mando
        lda #1
        sta SIZEP2
        sta SIZEP3
        ; caída con rebote: el suelo está en la línea GO_FLOOR+32
        lda go_vy
        clc
        adc #1
        bmi @s
        cmp #24
        bcc @s
        lda #24
@s:     sta go_vy
        cmp #$80
        ror a
        cmp #$80
        ror a
        clc
        adc ey
        cmp #GO_FLOOR+32
        bcc @air
        lda go_b            ; bote (dos veces, cada vez más bajo)
        cmp #2
        bcs @st
        inc go_b
        lda #16
        jsr sfx
        lda go_b
        cmp #1
        bne @b2
        lda #$F0            ; -16
        bne @b3
@b2:    lda #$F8            ; -8
@b3:    sta go_vy
@st:    lda #GO_FLOOR+32
        ldx go_b
        cpx #2
        bcc @air
        ldx #0
        stx go_vy
@air:   sta ey
        sta ey+1
        ldx #31             ; la parte alta de los sprites no la borra el motor
        lda #0
@cz:    sta PMA+$600,x
        sta PMA+$700,x
        sta PMB+$600,x
        sta PMB+$700,x
        dex
        bpl @cz
        jsr draw
        jsr pm_end
        inc sc_t
        lda sc_t
        cmp #240            ; tras unos segundos, o con FIRE, al título
        bcs @out
        cmp #60
        bcs *+5
        jmp @w
        lda fireed
        bne *+5
        jmp @w
@out:   lda #0
        sta SIZEP2
        sta SIZEP3
        sta etyp
        sta etyp+1
        jmp title
