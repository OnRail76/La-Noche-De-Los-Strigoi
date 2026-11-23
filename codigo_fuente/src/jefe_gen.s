; ===============================================================
; JEFE GENÉRICO (residente): Căpcăun, Rey Strigoi y la cabeza final.
; El módulo de la fase pasa un bloque de parámetros (GPAR) y salta a garena.
; Ataques (lista de códigos acabada en 0):
;   1 lluvia de cristales · 2 parábolas (huesos / fuego) · 3 enjambre
;   4 onda de choque por el suelo · 5 murciélagos · 6 abre la boca (vulnerable)
; ===============================================================
        .segment "HIBSS"
g_pk:   .res 1              ; 0 paquete de la arena
g_s1:   .res 1              ; 1-2 filas donde cambia el juego de caracteres
g_s2:   .res 1
g_s3:   .res 1
g_blk:  .res 2              ; 3 bloque del jefe
g_r:    .res 1              ; 5 rectángulo del bloque
g_c:    .res 1
g_w:    .res 1
g_h:    .res 1
g_alt:  .res 2              ; 9 bloque alternativo (boca abierta) o 0
g_hl:   .res 1              ; 11 caja de la cabeza (x, líneas)
g_hr:   .res 1
g_ht:   .res 1
g_hb:   .res 1
g_bl:   .res 1              ; 15 caja del cuerpo
g_br:   .res 1
g_bt:   .res 1
g_bb:   .res 1
g_hp:   .res 1              ; 19 vida
g_atk:  .res 2              ; 20 lista de ataques
g_wait: .res 1              ; 22 espera entre ataques
g_ax:   .res 1              ; 23 de dónde salen los ataques
g_ay:   .res 1
g_next: .res 2              ; 25 qué viene tras vencerlo
g_mode: .res 1              ; 27 1 = solo vulnerable con la boca abierta
g_rx:   .res 1              ; 28 x inicial de Radu
g_self: .res 2              ; 29 entrada (para reaparecer)
GPARN = 32
ga_st:  .res 1
ga_i:   .res 1
ga_n:   .res 1
ga_t:   .res 1
ga_code:.res 1
g_open: .res 1

        .segment "CODE"
; A/X = parámetros (lo, hi)
garena: sta ptr
        stx ptr+1
        ldy #GPARN-1
@cp:    lda (ptr),y
        sta g_pk,y
        dey
        bpl @cp
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr snd_off
        jsr m_wait
        lda g_pk
        jsr pack_load
        ldx #ADLLEN-1
@dl:    lda ADLTPL,x
        sta DLGAME,x
        dex
        bpl @dl
        jsr arena_bg_all
        ldx #39
@hu:    lda HUDA,x
        sta HUD,x
        dex
        bpl @hu
        ldx #21
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
        dex
        bpl @dt
        lda #0              ; suelo liso: sin mapa de colisión
        sta mapb
        lda #<AIDENT
        sta clsp
        lda #>AIDENT
        sta clsp+1
        jsr respawn_state
        lda #0
        sta camx
        sta camx+1
        sta rxh
        lda g_rx
        sta rxl
        lda #0
        sta bphase
        sta bflash
        sta bwin
        sta ga_st
        sta ga_t
        sta ga_i
        sta g_open
        sta dact
        sta dact+1
        sta dact+2
        sta dact+3
        lda g_hp            ; HARDCORE: jefes con más aguante
        ldx diff
        beq *+5
        clc
        adc #4
        sta bhp
        jsr g_draw
        lda g_bl
        sta bx_l
        lda g_br
        sta bx_r
        lda g_ht
        sta bx_t
        lda g_bb
        sec
        sbc #8
        sta bx_b
        jsr hud_arena
        jsr pm_init
        lda #>ARA
        sta CHBAS
        lda #$00
        sta COLOR4
        sta COLOR2
        lda #$0C
        sta COLOR1
        lda #COL_PF3
        sta COLOR3
        lda #$31
        sta GPRIOR
        lda #<DLGAME
        sta SDLSTL
        lda #>DLGAME
        sta SDLSTH
        lda #3
        sta GRACTL
        lda #<dli_arena
        sta VDSLST
        lda #>dli_arena
        sta VDSLST+1
        lda #2
        sta gmode
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        jsr m_wait
        lda #$C0
        sta NMIEN
        lda #19
        jsr sfx
        lda #2
        jsr mus_play

gloop:  jsr pm_wait
        jsr m_mando
        jsr radu
        jsr baltag
        jsr enemies
        jsr collide
        jsr gboss
        jsr draw
        jsr debris_draw
        jsr pm_end
        lda bwin
        beq @nw
        dec bwin
        bne @nw
        lda g_mode          ; la cabeza final: directo al final del juego
        beq *+5
        jmp fin_juego
        lda g_next          ; ¿qué viene ahora?
        sta aftert
        lda g_next+1
        sta aftert+1
        lda #<DESC_VIC
        sta ptr
        lda #>DESC_VIC
        sta ptr+1
        lda #4
        jmp txt_score_wait
@nw:    lda rst
        cmp #3
        bne gloop
        dec rdead
        bne gloop
        dec lives
        bne @r
        jmp gameover
@r:     jmp (g_self)

; rectángulo del bloque y dibujo (normal o boca abierta)
g_rect: lda g_r
        sta blk_r
        lda g_c
        sta blk_c
        lda g_w
        sta blk_w
        lda g_h
        sta blk_h
        rts
g_draw: jsr g_rect
        lda g_blk
        sta ptr
        lda g_blk+1
        sta ptr+1
        jmp blk_draw_all
g_dalt: jsr g_rect
        lda g_alt
        sta ptr
        lda g_alt+1
        sta ptr+1
        jmp blk_draw_all

; ---------------------------------------------------------------
gboss:  jsr flash_update
        jsr debris_update
        lda bphase
        cmp #3
        bne @a
        jmp dying
@a:     cmp #2
        bne @f
        rts
@f:     jsr g_hits
        lda bphase
        beq g_logic
        rts

g_logic:
        lda g_open          ; boca abierta: se cierra sola
        beq @o
        dec g_open
        bne @o
        jsr g_draw
@o:     inc ga_t
        lda ga_st
        bne @run
        lda g_wait
        ldx bhp
        cpx #6
        bcs *+3
        lsr a               ; con poca vida, más rápido
        cmp ga_t
        bcs @r
        ; siguiente ataque de la lista
        lda g_atk
        sta ptr
        lda g_atk+1
        sta ptr+1
        ldy ga_i
        lda (ptr),y
        bne @c
        ldy #0
        sty ga_i
        lda (ptr),y
@c:     inc ga_i
        sta ga_code
        lda #3
        sta ga_n
        lda #1
        sta ga_st
        lda #0
        sta ga_t
        lda #9
        jsr sfx
        lda ga_code
        cmp #6
        bne @r
        jsr g_dalt          ; abre la boca
        lda #120
        sta g_open
        lda #0
        sta ga_st
        lda #17
        jmp sfx
@r:     rts
@run:   lda ga_t
        cmp #16
        bcc @r
        jsr free_slot
        bcc @r
        lda #0
        sta ga_t
        sta est,x
        sta et,x
        sta efr,x
        sta exh,x
        lda g_ax
        sta exl,x
        lda g_ay
        sta ey,x
        lda #1
        sta edir,x
        lda ga_code
        cmp #1
        bne @a2
        lda #17             ; cristal que cae cerca de Radu
        sta etyp,x
        lda #2
        sta est,x
        lda RANDOM
        and #31
        sec
        sbc #16
        clc
        adc rxl
        cmp #150
        bcc *+4
        lda #140
        sta exl,x
        lda #60
        sta ey,x
        jmp @cnt
@a2:    cmp #2
        bne @a3
        lda #16             ; parábola hacia Radu
        sta etyp,x
        jsr face_radu
        lda RANDOM
        and #1
        clc
        adc #$FB
        sta elife,x
        lda #12
        jsr sfx
        jmp @cnt
@a3:    cmp #3
        bne @a4
        lda #18             ; enjambre a la altura de Radu
        sta etyp,x
        lda ry
        sec
        sbc #12
        sta elife,x
        sta ey,x
        lda #5
        jsr sfx
        jmp @cnt
@a4:    cmp #4
        bne @a5
        lda #23             ; onda de choque por el suelo
        sta etyp,x
        lda #FLOOR
        sta ey,x
        lda g_bl
        sec
        sbc #8
        sta exl,x
        lda #2
        jsr sfx
        lda #1
        sta ga_n
        jmp @cnt
@a5:    lda #6              ; murciélagos
        sta etyp,x
        lda #1
        sta est,x
        lda #5
        jsr sfx
@cnt:   dec ga_n
        bne @rr
        lda #0
        sta ga_st
        sta ga_t
@rr:    rts

; onda de choque (tipo 23): corre por el suelo hasta el borde
e_shock:
        inc et,x
        lda et,x
        lsr a
        lsr a
        and #1
        sta efr,x
        jsr vstep
        jsr vstep
        jsr vstep
        lda exl,x
        cmp #4
        bcs @r
        lda #0
        sta etyp,x
@r:     rts

; ---------------------------------------------------------------
g_hits: lda bact
        bne *+5
        jmp @radu
        lda bxl
        clc
        adc #7
        cmp g_hl
        bcc @radu
        lda bxl
        cmp g_hr
        bcs @radu
        lda by
        clc
        adc #7
        cmp g_ht
        bcc @radu
        lda by
        cmp g_hb
        bcs @radu
        lda #0
        sta bact
        lda g_mode          ; ¿solo con la boca abierta?
        beq @hit
        lda g_open
        bne @hit
        lda #16             ; rebota
        jmp sfx
@hit:   lda #6
        sta bflash
        lda #1
        jsr sfx
        lda #$00
        ldx #$02
        jsr addsc
        dec bhp
        jsr hud_arena
        lda bhp
        bne @radu
        lda #$00            ; gran final
        ldx #$50
        jsr addsc
        jsr hud_arena
        lda #0
        sta etyp
        sta etyp+1
        sta g_open
        jsr g_rect
        lda #1
        jmp death_start
@radu:  lda rst
        cmp #3
        beq @r
        lda rinv
        bne @r
        lda cheat
        bne @r
        lda rxl
        clc
        adc #6
        cmp g_bl
        bcc @r
        lda rxl
        clc
        adc #1
        cmp g_br
        bcs @r
        lda ry
        cmp g_bt
        bcc @r
        lda ry
        sec
        sbc #22
        cmp g_bb
        bcs @r
        jmp r_hit
@r:     rts
