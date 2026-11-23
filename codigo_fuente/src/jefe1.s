; ===============================================================
; JEFE DE LA FASE 1: EL STRIGOI MORT (y su forma de lobo) · módulo 1
; ===============================================================
        .segment "MOD1"
; ---------------------------------------------------------------
; montar la arena
; ---------------------------------------------------------------
arena:  lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        jsr snd_off
        jsr m_wait
        lda #PK_AR1
        jsr pack_load
        ; display list
        ldx #ADLLEN-1
@dl:    lda ADLTPL,x
        sta DLGAME,x
        dex
        bpl @dl
        ; fondo
        jsr arena_bg_all
        ; marcador
        ldx #39
@hu:    lda HUDA,x
        sta HUD,x
        dex
        bpl @hu
        ; tablas de la DLI (22 entradas)
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
        cpx #13
        bcs @cb
        lda #>ARP
        cpx #5
        bcs @cb
        lda #>ARA
@cb:    sta DTCH,x
        lda #0
        sta DTHS,x
        dex
        bpl @dt
        ; colisiones con el mapa de la arena
        lda #>AMAP
        sta mapb
        lda #<AIDENT
        sta clsp
        lda #>AIDENT
        sta clsp+1
        ; Radu entra por la izquierda
        jsr respawn_state
        lda #0
        sta camx
        sta camx+1
        lda #8
        sta rxl
        lda #0
        sta rxh
        ; el jefe
        lda #0
        sta bphase
        sta mstate
        sta mt
        sta matk
        sta mvis
        sta bflash
        sta bwin
        sta wstate
        lda #1
        sta mpos
        lda #0
        sta dact
        sta dact+1
        sta dact+2
        sta dact+3
        lda #BHP_MAX
        sta bhp
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

; ---------------------------------------------------------------
aloop:  jsr pm_wait
        jsr m_mando
        jsr radu
        jsr baltag
        jsr enemies
        jsr collide
        jsr boss
        jsr draw
        jsr debris_draw
        jsr pm_end
        lda bwin
        beq @nw
        dec bwin
        bne @nw
        jmp victory
@nw:    lda rst
        cmp #3
        bne aloop
        dec rdead
        bne aloop
        dec lives
        bne @r
        jmp gameover
@r:     jmp arena

mort_rect:
        ldx mpos
        lda MORT_COL,x
        sta blk_c
        lda #MORT_ROW
        sta blk_r
        lda #MORT_W
        sta blk_w
        lda #MORT_H
        sta blk_h
        rts

mort_draw:
        jsr mort_rect
        lda #<MORT_BLK
        sta ptr
        lda #>MORT_BLK
        sta ptr+1
        lda #1
        sta mvis
        jmp blk_draw

mort_erase:
        jsr mort_rect
        lda #0
        sta mvis
        jmp blk_erase

wolf_rect:
        lda wx
        sta blk_c
        lda #WOLF_ROW
        sta blk_r
        lda #WOLF_W
        sta blk_w
        lda #WOLF_H
        sta blk_h
        rts

wolf_draw:
        jsr wolf_rect
        lda wdir
        beq @r
        lda #<WOLF_L
        sta ptr
        lda #>WOLF_L
        sta ptr+1
        jmp blk_draw
@r:     lda #<WOLF_R
        sta ptr
        lda #>WOLF_R
        sta ptr+1
        jmp blk_draw

wolf_erase:
        jsr wolf_rect
        jmp blk_erase

; ---------------------------------------------------------------
; JEFE: un cuadro de lógica
; ---------------------------------------------------------------
boss:   jsr flash_update
        jsr debris_update
        lda bphase
        beq mort_logic
        cmp #1
        bne @d
        jmp wolf_logic
@d:     cmp #3
        bne @r
        jmp dying
@r:     rts

; destello blanco al recibir un golpe (PF1 de las filas del jefe)
; ---------------- Mort ----------------
mort_logic:
        inc mt
        lda mstate
        bne @s1
        ; 0: aparece parpadeando
        lda mt
        and #4
        beq @dr
        lda mvis
        beq @ck
        jsr mort_erase
        jmp @ck
@dr:    lda mvis
        bne @ck
        jsr mort_draw
@ck:    lda mt
        cmp #32
        bcs *+5
        jmp @hit
        jsr mort_draw
        lda #1
        sta mstate
        lda #0
        sta mt
        jmp @hit
@s1:    cmp #1
        bne @s2
        ; 1: espera y elige ataque
        lda mt
        cmp #40
        bcs *+5
        jmp @hit
        lda #0
        sta mt
        lda #2              ; viento helado: el único ataque de Mort
        sta mstate
        lda #39
        sta spos
        jmp @hit
@s2:    cmp #2
        bne @s3
        jsr wind
        jmp @hit
@s3:    cmp #3
        bne @s4
        ; 3: se queda quieto (ventana para golpearle)
        lda mt
        cmp #90
        bcc @hit
        lda #4
        sta mstate
        lda #0
        sta mt
        jmp @hit
@s4:    ; 4: desaparece parpadeando y cambia de tumba
        lda mt
        and #4
        beq @d2
        lda mvis
        beq @c4
        jsr mort_erase
        jmp @c4
@d2:    lda mvis
        bne @c4
        jsr mort_draw
@c4:    lda mt
        cmp #24
        bcc @hit
        lda mvis
        beq @nx
        jsr mort_erase
@nx:    ; de las otras dos tumbas, la más alejada de Radu
        ldx mpos
        lda NEXT1,x
        sta blk_i
        lda NEXT2,x
        sta blk_w
        ldx blk_i
        jsr tomb_dist
        sta blk_h
        ldx blk_w
        jsr tomb_dist
        cmp blk_h
        bcs @far2
        lda blk_i
        bcc @p
@far2:  lda blk_w
@p:     sta mpos
        lda #0
        sta mstate
        sta mt
        lda #19
        jsr sfx
@hit:   ; caja de Mort y golpes (no se le puede dar mientras parpadea)
        lda mvis
        bne @v
        rts
@v:     lda mstate
        beq @no
        cmp #4
        bne @si
@no:    rts
@si:    ldx mpos
        lda MORT_COL,x
        asl a
        asl a
        clc
        adc #16
        sta bx_l
        adc #20
        sta bx_r
        lda #(40+40+16)         ; Mort: de los hombros (línea 96) a los pies (168)
        sta bx_t
        lda #(FLOOR-16)
        sta bx_b
        jsr boss_hits
        rts

NEXT1:  .byte 1,2,0
NEXT2:  .byte 2,0,1

; A = distancia entre el centro de la tumba X y Radu
tomb_dist:
        lda MORT_COL,x
        asl a
        asl a
        clc
        adc #26
        sec
        sbc rxl
        bcs @r
        eor #$FF
        adc #1
@r:     rts

; los murciélagos salen de las manos
wind:   lda mt
        cmp #40
        bcs @go
        ; aviso: los ojos parpadean en blanco
        lda frame
        and #4
        beq @e1
        lda #$0E
        bne @e2
@e1:    lda #$46
@e2:    sta DTPF3+7
        rts
@go:    cmp #40
        bne @nb
        lda #$46
        sta DTPF3+7
        lda #$0E            ; las esquirlas en blanco (PF3 de su fila)
        sta DTPF3+SHARD_ROW
        lda #18
        jsr sfx
@nb:    lda mt
        cmp #190
        bcc @run
        ; fin del viento
        jsr shards_clear
        lda #$0C
        sta DTPF3+SHARD_ROW
        lda #3
        sta mstate
        lda #0
        sta mt
        rts
@run:   ; empuja a Radu hacia la izquierda (1 de cada 2 cuadros)
        lda rst
        cmp #3
        beq @sh
        lda frame
        and #1
        bne @sh
        lda #$FF
        jsr r_movex
@sh:    ; esquirlas: avanzan una casilla cada 2 cuadros hacia la izquierda
        lda frame
        and #1
        bne @col
        jsr shards_clear
        dec spos
        bpl @dw
        lda #39
        sta spos
@dw:    jsr shards_draw
@col:   ; ¿alcanzan a Radu? (de pie, con la cabeza en la fila de las esquirlas)
        lda rst
        cmp #3
        beq @r
        lda rcrouch
        bne @r
        lda rinv
        bne @r
        lda cheat
        bne @r
        lda ry
        cmp #(40+SHARD_ROW*8)
        bcc @r              ; Radu muy arriba (saltando por encima)
        lda ry
        sec
        sbc #22
        cmp #(40+SHARD_ROW*8+8)
        bcs @r              ; cabeza por debajo de la fila
        lda spos
        asl a
        asl a
        sta tyy             ; x de la primera esquirla
        lda rxl
        clc
        adc #6
        cmp tyy
        bcc @r
        lda tyy
        clc
        adc #11
        cmp rxl
        bcc @r
        jsr r_hit
@r:     rts

shards_clear:
        lda #SHARD_ROW
        sta blk_r
        lda #0
        sta blk_c
        lda #40
        sta blk_w
        lda #1
        sta blk_h
        jsr blk_erase
        lda mvis            ; vuelve a pintar la parte de Mort de esa fila
        beq @r
        jmp mort_draw
@r:     rts

shards_draw:
        ldx #SHARD_ROW
        lda ASROW_LO,x
        sta dst
        lda ASROW_HI,x
        sta dst+1
        ldx #0
@l:     txa
        clc
        adc spos
        cmp #40
        bcs @n
        tay
        ; no pintar encima de Mort
        lda mvis
        beq @p
        sty tyy
        ldy mpos
        lda MORT_COL,y
        ldy tyy
        cmp tyy
        beq @n
        bcs @p
        clc
        adc #MORT_W
        cmp tyy
        bcs @n
@p:     lda #SHARD
        sta (dst),y
@n:     inx
        cpx #3
        bne @l
        rts

; ---------------- el lobo ----------------
wolf_start:
        lda #1
        sta bphase
        lda #0
        sta wstate
        sta wt
        ; paleta del lobo en las filas 13-17
        ldx #4
@p:     lda WT_BK,x
        sta DTBK+13,x
        lda WT_PF0,x
        sta DTPF0+13,x
        lda WT_PF1,x
        sta DTPF1+13,x
        lda WT_PF2,x
        sta DTPF2+13,x
        lda WT_PF3,x
        sta DTPF3+13,x
        dex
        bpl @p
        lda #WOLF_MAXC
        sta wx
        lda #1
        sta wdir
        jsr wolf_draw
        lda #17
        jmp sfx

wolf_logic:
        inc wt
        lda wstate
        bne @s2
        ; aviso: se agacha y aúlla (parpadea)
        lda wt
        cmp #1
        bne @t
        lda #17
        jsr sfx
        lda #30
        sta bflash
@t:     lda wt
        cmp #45
        bcc @box
        lda #1
        sta wstate
        lda #0
        sta wt
        jmp @box
@s2:    cmp #1
        bne @s3
        ; embestida: una casilla (4 píxeles) por cuadro
        jsr wolf_erase
        lda wdir
        beq @rt
        dec wx
        bne @dr
        beq @hitw
@rt:    inc wx
        lda wx
        cmp #WOLF_MAXC
        bne @dr
@hitw:  jsr wolf_draw
        lda #2
        sta wstate
        lda #0
        sta wt
        lda #16
        jsr sfx
        jmp @box
@dr:    jsr wolf_draw
        jmp @box
@s3:    ; aturdido contra la pared, luego da la vuelta
        lda wt
        cmp #80
        bcc @box
        lda wdir
        eor #1
        sta wdir
        jsr wolf_draw
        lda #0
        sta wstate
        sta wt
@box:   lda wx
        asl a
        asl a
        clc
        adc #2
        sta bx_l
        adc #28
        sta bx_r
        lda #(FLOOR-24)
        sta bx_t
        lda #FLOOR
        sta bx_b
        jmp boss_hits

; ---------------------------------------------------------------
; golpes: baltag contra la caja del jefe y Radu contra el jefe
; ---------------------------------------------------------------
boss_hits:
        lda bphase          ; reventando: ni golpes ni daño
        cmp #3
        bcc @ok
        rts
@ok:
        lda bact
        bne *+5
        jmp @radu
        lda bxl
        clc
        adc #7
        cmp bx_l
        bcc @radu
        lda bxl
        cmp bx_r
        bcs @radu
        lda by
        clc
        adc #7
        cmp bx_t
        bcc @radu
        lda by
        cmp bx_b
        bcs @radu
        ; ¡golpe al jefe!
        lda #0
        sta bact
        lda #6
        sta bflash
        lda #1
        jsr sfx
        lda #$00
        ldx #$01
        jsr addsc
        dec bhp
        jsr hud_arena
        lda bhp
        cmp #BHP_WOLF
        bne @dead
        lda bphase
        bne @dead
        ; Mort revienta y se transforma en lobo
        jsr mort_rect
        lda #0
        jmp death_start
@dead:  lda bhp
        bne @radu
        ; vencido
        lda bphase
        cmp #1
        bne @radu
        lda #$00            ; gran final
        ldx #$50
        jsr addsc
        jsr hud_arena
        jsr wolf_rect
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
        cmp bx_l
        bcc @r
        lda rxl
        clc
        adc #1
        cmp bx_r
        bcs @r
        lda ry
        cmp bx_t
        bcc @r
        lda ry
        sec
        sbc #22
        ldy rcrouch
        beq @nc
        clc
        adc #9
@nc:    cmp bx_b
        bcs @r
        jmp r_hit
@r:     rts

