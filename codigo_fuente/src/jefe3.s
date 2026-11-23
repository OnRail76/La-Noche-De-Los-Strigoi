; ===============================================================
; JEFE DE LA FASE 3: MUMA PĂDURII, la Madre del Bosque
; Galería de sal. Muma ocupa la derecha; su cabeza es el punto débil y se
; alcanza saltando desde la repisa alta. Ataques: lluvia de cristales de sal
; (golpe de bastón), raíces espinosas que brotan del suelo y enjambres de
; insectos venenosos que salen de su boca.
; ===============================================================
MHEAD_L = MUMA_X0+26
MHEAD_R = MUMA_X0+60
MHEAD_T = MUMA_Y0+4+40
MHEAD_B = MUMA_Y0+56+40
MBODY_L = MUMA_X0+30
MBODY_R = MUMA_X0+76
MBODY_T = MUMA_Y0+40+40
MBODY_B = MUMA_Y0+128+40
MCLAW_L = MUMA_X0+4
MCLAW_R = MUMA_X0+30
MCLAW_T = MUMA_Y0+74+40
MCLAW_B = MUMA_Y0+92+40

        .segment "HIBSS"
m_st:   .res 1
m_t:    .res 1
m_n:    .res 1
m_atk:  .res 1
rt_c:   .res 1              ; raíz: columna, tiempo (tell + espinas), casillas guardadas
rt_t:   .res 1
rt_s:   .res 4

        .segment "MOD3"
arena3: lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr snd_off
        jsr m_wait
        lda #PK_AR3
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
        cpx #A3_SPLIT2
        bcs @cb
        lda #>ARP
        cpx #A3_SPLIT1
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
        lda #0
        sta bphase
        sta bflash
        sta bwin
        sta m_st
        sta m_t
        sta m_atk
        sta rt_t
        sta dact
        sta dact+1
        sta dact+2
        sta dact+3
        lda #16
        sta bhp
        jsr muma_rect
        lda #<MUMA_BLK
        sta ptr
        lda #>MUMA_BLK
        sta ptr+1
        jsr blk_draw
        lda #MBODY_L-20
        sta bx_l
        lda #MBODY_R
        sta bx_r
        lda #MHEAD_T
        sta bx_t
        lda #MBODY_B-8
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

aloop3: jsr pm_wait
        jsr m_mando
        jsr radu
        jsr baltag
        jsr enemies
        jsr collide
        jsr boss3
        jsr draw
        jsr debris_draw
        jsr pm_end
        lda bwin
        beq @nw
        dec bwin
        bne @nw
        jmp victory3
@nw:    lda rst
        cmp #3
        bne aloop3
        dec rdead
        bne aloop3
        dec lives
        bne @r
        jmp gameover
@r:     jmp arena3

victory3:
        lda #<fase4_start   ; tras la pantalla, la fase 4
        sta aftert
        lda #>fase4_start
        sta aftert+1
        lda #<DESC_VIC
        sta ptr
        lda #>DESC_VIC
        sta ptr+1
        lda #4
        jmp txt_score_wait

muma_rect:
        lda #MUMA_R
        sta blk_r
        lda #MUMA_C
        sta blk_c
        lda #MUMA_W
        sta blk_w
        lda #MUMA_H
        sta blk_h
        rts

; ---------------------------------------------------------------
boss3:  jsr flash_update
        jsr debris_update
        jsr root_update
        lda bphase
        cmp #3
        bne @a
        jmp dying
@a:     cmp #2
        bne @f
        rts
@f:     jsr muma_hits
        lda bphase
        beq muma_logic
        rts

; espera · cristales · espera · raíces · espera · insectos
muma_logic:
        inc m_t
        lda m_st
        bne @atk
        lda #60
        ldx bhp
        cpx #8
        bcs @w
        lda #36
@w:     cmp m_t
        bcs @r
        lda #0
        sta m_t
        ldx m_atk
        inx
        cpx #3
        bcc *+4
        ldx #0
        stx m_atk
        inx
        stx m_st            ; 1 cristales, 2 raíces, 3 insectos
        lda #4
        cpx #2
        bne *+4
        lda #1
        cpx #3
        bne *+4
        lda #3
        sta m_n
        lda #16             ; golpe de bastón / rugido
        jsr sfx
        lda #9
        jmp sfx
@r:     rts
@atk:   cmp #2
        beq @roots
        lda m_t             ; uno cada 14 cuadros, si hay hueco
        cmp #14
        bcc @r
        jsr free_slot
        bcc @r
        lda #0
        sta m_t
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        sta exh,x
        lda m_st
        cmp #1
        bne @ins
        ; cristal de sal: cae sobre Radu o a su lado
        lda #17
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
@ins:   lda #18             ; insecto: de la boca hacia Radu
        sta etyp,x
        lda #MUMA_X0+30
        sta exl,x
        lda #1
        sta edir,x
        lda ry
        sec
        sbc #12
        sta elife,x
        sta ey,x
        lda #5
        jsr sfx
@cnt:   dec m_n
        bne @r2
        lda #0
        sta m_st
        sta m_t
@r2:    rts
@roots: lda rt_t            ; raíz bajo Radu (si está en el suelo; si no, a su lado)
        bne @r2
        lda rxl
        clc
        adc #2
        lsr a
        lsr a
        cmp #MUMA_C-2
        bcc *+4
        lda #MUMA_C-3
        sta rt_c
        tax
        lda ASCR+16*40,x
        sta rt_s
        lda ASCR+16*40+1,x
        sta rt_s+1
        lda ASCR+17*40,x
        sta rt_s+2
        lda ASCR+17*40+1,x
        sta rt_s+3
        lda #90
        sta rt_t
        lda #0
        sta m_st
        sta m_t
        lda #16
        jmp sfx

; raíces: 30 cuadros de aviso (asoma la base), 60 de espinas que hieren
root_update:
        lda rt_t
        bne *+3
        rts
        dec rt_t
        ldx rt_c
        lda rt_t
        bne @n0
        lda rt_s            ; se retira
        sta ASCR+16*40,x
        lda rt_s+1
        sta ASCR+16*40+1,x
        lda rt_s+2
        sta ASCR+17*40,x
        lda rt_s+3
        sta ASCR+17*40+1,x
        rts
@n0:    cmp #60
        bcc @full
        bne @tell           ; aviso: la base asoma a ratos
        lda #16
        jsr sfx
@tell:  lda frame
        and #4
        beq @off
        lda #ROOT_B
        sta ASCR+17*40,x
        sta ASCR+17*40+1,x
        rts
@off:   lda rt_s+2
        sta ASCR+17*40,x
        lda rt_s+3
        sta ASCR+17*40+1,x
        rts
@full:  lda #ROOT_T
        sta ASCR+16*40,x
        sta ASCR+16*40+1,x
        lda #ROOT_B
        sta ASCR+17*40,x
        sta ASCR+17*40+1,x
        ; ¿pincha a Radu?
        lda rst
        cmp #3
        beq @r
        lda ry
        cmp #176
        bcc @r
        lda rinv
        bne @r
        lda cheat
        bne @r
        lda rt_c
        asl a
        asl a
        sta hitl
        lda rxl
        clc
        adc #6
        cmp hitl
        bcc @r
        lda hitl
        clc
        adc #8
        cmp rxl
        bcc @r
        beq @r
        jmp r_hit
@r:     rts

; ---------------------------------------------------------------
muma_hits:
        lda bact
        bne *+5
        jmp @radu
        lda bxl
        clc
        adc #7
        cmp #MHEAD_L
        bcc @radu
        lda bxl
        cmp #MHEAD_R
        bcs @radu
        lda by
        clc
        adc #7
        cmp #MHEAD_T
        bcc @radu
        lda by
        cmp #MHEAD_B
        bcs @radu
        lda #0
        sta bact
        lda #6
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
        lda #$00
        ldx #$50
        jsr addsc
        jsr hud_arena
        lda #0
        sta etyp
        sta etyp+1
        lda rt_t
        beq @nr
        lda #1
        sta rt_t
@nr:    jsr muma_rect
        lda #1
        jmp death_start
@radu:  lda rst
        cmp #3
        beq @r
        lda rinv
        bne @r
        lda cheat
        bne @r
        ldx #0              ; cuerpo y brazo de las garras
@bx:    lda rxl
        clc
        adc #6
        cmp MBOX_L,x
        bcc @nx
        lda rxl
        clc
        adc #1
        cmp MBOX_R,x
        bcs @nx
        lda ry
        cmp MBOX_T,x
        bcc @nx
        lda ry
        sec
        sbc #22
        cmp MBOX_B,x
        bcs @nx
        jmp r_hit
@nx:    inx
        cpx #2
        bne @bx
@r:     rts
MBOX_L: .byte MBODY_L, MCLAW_L
MBOX_R: .byte MBODY_R, MCLAW_R
MBOX_T: .byte MBODY_T, MCLAW_T
MBOX_B: .byte MBODY_B, MCLAW_B
