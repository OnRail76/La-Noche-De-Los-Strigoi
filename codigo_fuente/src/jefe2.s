; ===============================================================
; JEFE DE LA FASE 2: ARIC, EL SASTRE DE LAS SOMBRAS
; Taller de la Torre de los Sastres. Aric flota en el centro (bloque fijo);
; seis retales encantados protegen su cabeza y hay que arrancarlos uno a uno.
; Ataques: tijeras oxidadas que cruzan la sala (tipo 11) y agujas de hierro
; que caen y se clavan en el suelo cerrando el paso (tipo 12 y estacas).
; Mesas de corte a los lados: desde ellas, saltando, se alcanza la cabeza.
; ===============================================================
ASHIELD = 6
AHEAD_T = ARIC_Y0+40        ; caja de la cabeza (líneas) y x de pantalla
AHEAD_B = ARIC_Y0+40+28
AHEAD_L = ARIC_X0+3
AHEAD_R = ARIC_X0+62
ATOR_L  = ARIC_X0+18        ; torso: tocarlo hace daño
ATOR_R  = ARIC_X0+46
ATOR_T  = ARIC_Y0+40+24
ATOR_B  = ARIC_Y0+40+62

        .segment "HIBSS"
ashield:.res 1
a_st:   .res 1
a_t:    .res 1
aatk:   .res 1
andl:   .res 1
stk_c:  .res 2              ; estacas (agujas clavadas): columna, tiempo, casillas guardadas
stk_t:  .res 2
stk_s0: .res 2
stk_s1: .res 2

        .segment "MOD2"
arena2: lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr snd_off
        jsr m_wait
        lda #PK_AR2
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
        lda #>ARQ
        cpx #12
        bcs @cb
        lda #>ARP
        cpx #6
        bcs @cb
        lda #>ARA
@cb:    sta DTCH,x
        lda #0
        sta DTHS,x
        dex
        bpl @dt
        lda #>AMAP
        sta mapb
        lda #<AIDENT
        sta clsp
        lda #>AIDENT
        sta clsp+1
        jsr respawn_state
        lda #0
        sta camx
        sta camx+1
        lda #8
        sta rxl
        lda #0
        sta rxh
        ; Aric
        lda #0
        sta bphase
        sta bflash
        sta bwin
        sta a_st
        sta a_t
        sta aatk
        sta stk_t
        sta stk_t+1
        sta dact
        sta dact+1
        sta dact+2
        sta dact+3
        lda #ASHIELD
        sta ashield
        lda #16
        sta bhp
        jsr aric_rect
        lda #<ARIC_S
        sta ptr
        lda #>ARIC_S
        sta ptr+1
        jsr blk_draw
        ; caja para las explosiones finales
        lda #ARIC_X0+8
        sta bx_l
        lda #ARIC_X0+56
        sta bx_r
        lda #ARIC_Y0+48
        sta bx_t
        lda #ARIC_Y0+136
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
        lda #2              ; tema del jefe
        jsr mus_play

aloop2: jsr pm_wait
        jsr m_mando
        jsr radu
        jsr baltag
        jsr enemies
        jsr collide
        jsr boss2
        jsr draw
        jsr debris_draw
        jsr pm_end
        lda bwin
        beq @nw
        dec bwin
        bne @nw
        jmp victory2
@nw:    lda rst
        cmp #3
        bne aloop2
        dec rdead
        bne aloop2
        dec lives
        bne @r
        jmp gameover
@r:     jmp arena2

victory2:
        lda #<fase3_start   ; tras la pantalla, la fase 3
        sta aftert
        lda #>fase3_start
        sta aftert+1
        lda #<DESC_VIC
        sta ptr
        lda #>DESC_VIC
        sta ptr+1
        lda #4
        jmp txt_score_wait

aric_rect:
        lda #ARIC_R
        sta blk_r
        lda #ARIC_C
        sta blk_c
        lda #ARIC_W
        sta blk_w
        lda #ARIC_H
        sta blk_h
        rts

; ---------------------------------------------------------------
boss2:  jsr flash_update
        jsr debris_update
        jsr stakes_update
        lda bphase
        cmp #3
        bne @a
        jmp dying
@a:     cmp #2
        bne @f
        rts
@f:     jsr aric_hits
        lda bphase
        beq aric_logic
        rts

; ataques: espera, tijeras, espera, tres agujas...
aric_logic:
        inc a_t
        lda a_st
        bne @s1
        lda #70             ; espera (más corta cuando le queda poca vida)
        ldx bhp
        cpx #8
        bcs @w
        lda #40
@w:     cmp a_t
        bcs @r
        lda #0
        sta a_t
        lda aatk
        eor #1
        sta aatk
        beq @ndl
        ; tijeras: salen del costado de Aric hacia Radu
        lda etyp
        bne @r
        ldx #0
        lda #11
        sta etyp,x
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        sta exh,x
        lda #ARIC_X0+28
        sta exl,x
        jsr face_radu
        lda ry              ; a la altura del cuerpo de Radu
        sec
        sbc #2
        sta ey,x
        lda #1
        sta a_st
        lda #12
        jmp sfx
@ndl:   lda #3
        sta andl
        lda #2
        sta a_st
@r:     rts
@s1:    cmp #1
        bne @s2
        lda etyp            ; esperar a que vuelvan las tijeras
        bne @r
        lda #0
        sta a_st
        sta a_t
        rts
@s2:    lda a_t             ; una aguja cada 24 cuadros
        cmp #24
        bcc @r
        lda #0
        sta a_t
        lda andl
        bne @nd
        sta a_st
        rts
@nd:    lda etyp+1
        bne @r
        dec andl
        ldx #1
        lda #12
        sta etyp,x
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        sta exh,x
        ldy andl            ; a los lados de Radu y la última encima
        lda rxl
        clc
        adc NDLOFF,y
        sta exl,x
        lda #84
        sta ey,x
        lda #12
        jmp sfx

NDLOFF: .byte 1,236,22     ; -20, +22 y encima (andl = 0, 1, 2 tras restar)
; ---------------------------------------------------------------
; tijeras (tipo 11): cruzan hasta el borde y vuelven a Aric
e_tij:  inc et,x
        lda et,x
        lsr a
        lsr a
        and #1
        sta efr,x
        lda est,x
        bne @back
        ldy #2
@m:     jsr vstep
        dey
        bne @m
        lda exl,x
        cmp #4
        bcc @turn
        cmp #150
        bcc @r
@turn:  lda #1
        sta est,x
        lda edir,x
        eor #1
        sta edir,x
        lda #12
        jsr sfx
@r:     rts
@back:  ldy #2
@m2:    jsr vstep
        dey
        bne @m2
        lda exl,x           ; ¿de vuelta en Aric?
        sec
        sbc #ARIC_X0+24
        cmp #10
        bcs @r
        lda #0
        sta etyp,x
        rts

; aguja (tipo 12): cae y se clava en el suelo (o se pierde en una mesa)
e_agu:  lda ey,x
        clc
        adc #3
        sta ey,x
        cmp #FLOOR
        bcc @r
        lda #0
        sta etyp,x
        lda exl,x
        lsr a
        lsr a
        jsr stake_place
        lda #16
        jmp sfx
@r:     rts

; estaca en la columna A (solo en el suelo libre entre las mesas)
stake_place:
        sta tcol
        cmp #11
        bcc @r
        cmp #30
        bcs @r
        ; no clavarla encima de Radu
        lda rxl
        lsr a
        lsr a
        sta hitl
        lda tcol
        sec
        sbc hitl
        cmp #3
        bcc @r
        cmp #$FF
        beq @r
        ldy #0
        lda stk_t
        beq @y
        iny
        lda stk_t+1
        bne @r
@y:     lda #200
        sta stk_t,y
        lda tcol
        sta stk_c,y
        tax
        lda ASCR+16*40,x
        sta stk_s0,y
        lda ASCR+17*40,x
        sta stk_s1,y
        lda #NEEDLE_T
        sta ASCR+16*40,x
        lda #NEEDLE_B
        sta ASCR+17*40,x
        lda #1
        sta AMAP+8*256,x
        sta AMAP+9*256,x
@r:     rts

stakes_update:
        ldy #1
@l:     lda stk_t,y
        beq @n
        sec
        sbc #1
        sta stk_t,y
        bne @n
        ldx stk_c,y
        lda stk_s0,y
        sta ASCR+16*40,x
        lda stk_s1,y
        sta ASCR+17*40,x
        lda #0
        sta AMAP+8*256,x
        sta AMAP+9*256,x
@n:     dey
        bpl @l
        rts

; ---------------------------------------------------------------
; golpes: el baltag contra los retales / la cabeza; Radu contra el torso
aric_hits:
        lda bact
        bne *+5
        jmp @radu
        lda bxl
        clc
        adc #7
        cmp #AHEAD_L
        bcs *+5
        jmp @tor
        lda bxl
        cmp #AHEAD_R
        bcc *+5
        jmp @tor
        lda by
        clc
        adc #7
        cmp #AHEAD_T
        bcs *+5
        jmp @tor
        lda by
        cmp #AHEAD_B
        bcc *+5
        jmp @tor
        ; golpe en la cabeza o en un retal
        lda #0
        sta bact
        lda #6
        sta bflash
        lda #1
        jsr sfx
        dec bhp
        lda ashield
        beq @head
        ; arranca el siguiente retal
        lda #ASHIELD
        sec
        sbc ashield
        tax
        lda PATCH_LO,x
        sta ptr
        lda PATCH_HI,x
        sta ptr+1
        ldy #0
        lda (ptr),y
        sta blk_r
        iny
        lda (ptr),y
        sta blk_c
        iny
        lda (ptr),y
        sta blk_w
        iny
        lda (ptr),y
        sta blk_h
        lda ptr
        clc
        adc #4
        sta ptr
        bcc *+4
        inc ptr+1
        jsr blk_draw_all
        dec ashield
        lda #2
        jsr sfx
        lda #$00
        ldx #$01
        jsr addsc
        jmp hud_arena
@head:  lda #$00
        ldx #$02
        jsr addsc
        jsr hud_arena
        lda bhp
        bne @r
        lda #$00            ; gran final
        ldx #$50
        jsr addsc
        jsr hud_arena
        lda #0
        sta etyp
        sta etyp+1
        jsr aric_rect
        lda #1
        jmp death_start
@tor:   ; el baltag rebota en el torso
        lda bxl
        clc
        adc #7
        cmp #ATOR_L
        bcc @radu
        lda bxl
        cmp #ATOR_R
        bcs @radu
        lda by
        clc
        adc #7
        cmp #ATOR_T
        bcc @radu
        lda by
        cmp #ATOR_B
        bcs @radu
        lda #0
        sta bact
        lda #16
        jsr sfx
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
        cmp #ATOR_L
        bcc @r
        lda rxl
        clc
        adc #1
        cmp #ATOR_R
        bcs @r
        lda ry
        cmp #ATOR_T
        bcc @r
        lda ry
        sec
        sbc #22
        cmp #ATOR_B
        bcs @r
        jmp r_hit
@r:     rts

