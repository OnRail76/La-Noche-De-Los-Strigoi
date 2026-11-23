; ===============================================================
; LA NOCHE DE LOS STRIGOI · Fase 1: El Cementerio de la Colina
; 2026 - TONY C. WARE
; Atari 8 bits (XL/XE, 64 KB, NTSC)
;
; Pantalla: marcador ANTIC 2 + 21 filas ANTIC 4
;   filas 0-3   cielo fijo (luna, ciudadela)           juego A (fuente + cielo)
;   filas 4-6   montañas, scroll a media velocidad     juego C
;   fila  7     niebla (sin scroll: aquí cambia HSCROL)
;   filas 8-20  cementerio con scroll fino             juego B
; Sprites: Radu = P0+P1 en modo OR (3 colores) · enemigos P2/P3 · baltag = quinto player
; ===============================================================
        .include "hw.inc"
MUSICA  = 1                 ; música en las fases (motor/musica.s)

; --- memoria
PMA     = $A000
PMB     = $A800
PMY0    = 32
PMN     = 184
GRING   = $B000             ; 13 anillos del cementerio (128 bytes cada uno)
MRING   = $B680             ; 3 anillos de montañas
SKYSCR  = $B800             ; 4 filas de cielo (40 bytes)
BLANK40 = $B8A0             ; fila vacía
HUD     = $B8C8             ; marcador (40 bytes)
DLGAME  = $B900
DLTEXT  = $B980
TSCR    = $BA00
EXTRA_STEP = $02            ; vida extra cada 20.000
; --- zona de tramo / arena ($2200-$3FFF): se descomprime desde la RAM bajo el OS
OVL     = $2200
CHARSA  = $2000             ; fuente (residente) + cielo del tramo
CHARSB  = $2400
CHARSC  = $2800
MAP     = $2C00             ; 13 páginas
TRT     = $3900             ; tabla del tramo
CLASS   = TRT
SKYROWS = TRT+128
MTNROWS = TRT+288
TBK     = TRT+480
TPF0    = TRT+502
TPF1    = TRT+524
TPF2    = TRT+546
TPF3    = TRT+568
SP_CAM  = TRT+590
SP_TYP  = TRT+622
SP_COL  = TRT+654
SP_Y    = TRT+686
TR_NSP  = TRT+718
TR_END  = TRT+719
TR_CHK  = TRT+720
TR_NEXT = TRT+721           ; siguiente tramo o $FF = arena del jefe
TR_FLAGS = TRT+722          ; bit 0: zombis al azar
TR_MUS  = TRT+723           ; tema musical del tramo
TR_T1   = TRT+724           ; rótulo de entrada (2 x 20)
TR_T2   = TRT+744
TR_X    = TRT+764
ARA     = $2000             ; arena: mismos huecos que el tramo
ARP     = $2400
ARQ     = $2800
AMAP    = $2C00
PK_CEM  = 0
PK_ESC  = 1
PK_CIU  = 2
PK_AR1  = 3
PK_AR2  = 4
PK_MIN  = 5
PK_AR3  = 6
PK_CAR  = 7
PK_AR4  = 8
PK_AR5  = 9
PK_CAS  = 10
PK_AR6  = 11
ARR     = $2C00             ; cuarto juego de las arenas 4-6 (sin mapa de colisión)

; --- constantes del juego
HP0     = 48                ; HPOS de la x = 0 del campo (se calibra con capturas)
SCRK    = 13                ; ajuste del anillo (x del campo -> columna)
CAMMIN  = 16
CAMMAX  = 840
GTOP    = 104               ; línea de la fila 0 del mapa
FLOOR   = 184               ; superficie del suelo (pies de Radu)
JUMPV   = $03C0             ; velocidad inicial del salto (8.8)
GRAV    = $30
NSLOT   = 2
TOMBHITS = 12              ; golpes a una tumba para que salga la bruja

        .segment "ZEROPAGE"
mp:     .res 2              ; puntero al mapa
dza:    .res 1              ; DLI: A y X guardados
dzx:    .res 1
lzs:    .res 2              ; descompresor
lzd:    .res 2
lzm:    .res 2
lzn:    .res 1
clsp:   .res 2              ; tabla de clases del mapa actual

        .segment "HIBSS"
gmode:  .res 1              ; 1 = pantalla de juego (la VBI hace el scroll)
camx:   .res 2
wcolnx: .res 2              ; siguiente columna del mundo por escribir en los anillos
camb_gl:.res 2              ; por búfer: LMS bajo del cementerio, HSCROL, LMS montañas, HSCROL
camb_gh:.res 2
camb_ml:.res 2
camb_mh:.res 2
; Radu
rxl:    .res 1
rxh:    .res 1
ry:     .res 1              ; pies (línea)
ryf:    .res 1
rvyl:   .res 1
rvyh:   .res 1
rst:    .res 1              ; 0 suelo, 1 aire, 2 golpeado, 3 muerto
rdir:   .res 1              ; 0 derecha, 1 izquierda
rjvx:   .res 1              ; avance en el salto (-1, 0, 1)
rcrouch:.res 1
rthrow: .res 1
ranim:  .res 1
rarmor: .res 1
rinv:   .res 1
rdead:  .res 1
lives:  .res 1
chk:    .res 1
cheat:  .res 1
downs:  .res 1
rframe: .res 1
; baltag
bact:   .res 1
bxl:    .res 1
bxh:    .res 1
by:     .res 1
bdir:   .res 1
bfr:    .res 1
; enemigos
etyp:   .res NSLOT          ; 0 libre, 1 zombi, 2 cuervo, 3 nube
est:    .res NSLOT
exl:    .res NSLOT
exh:    .res NSLOT
ey:     .res NSLOT
et:     .res NSLOT
efr:    .res NSLOT
edir:   .res NSLOT
elife:  .res NSLOT
ehp:    .res NSLOT          ; golpes que aguanta (gárgola: 2)
spi:    .res 1
ztimer: .res 1
; temporales propios (no compartidos)
wc_col: .res 1
wc_idx: .res 1
tx:     .res 2              ; coordenada x de trabajo
tyy:    .res 1
tcol:   .res 1
rpol:   .res 1              ; pollo: cuadros/4 que quedan
thits:  .res 1              ; golpes seguidos a una tumba
thcol:  .res 1
pc0:    .res 1
pc1:    .res 1
edge:   .res 1
zcol:   .res 1
hitl:   .res 1
hitr:   .res 1
hitt:   .res 1
hitb:   .res 1
cur:    .res 1
sx:     .res 1
hudch:  .res 1
endt:   .res 1
; tablas de la DLI (22 entradas)
DTHS:   .res 22
DTCH:   .res 22
DTBK:   .res 22
DTPF0:  .res 22
DTPF1:  .res 22
DTPF2:  .res 22
dlin:   .res 1
DTPF3:  .res 22
mapb:   .res 1              ; página alta del mapa actual
fase:   .res 1
tramo:  .res 1
card:   .res 1              ; 1 = rótulo de entrada al tramo
tr_endx:.res 2
tr_chkx:.res 2
aftert: .res 2              ; tras una pantalla de texto: 0 = título
T_FASEN:.res 20

        .segment "CODE"
        .include "data.s"
        .include "tr_cementerio.s"
        .include "tr_escalera.s"
        .include "tr_ciudadela.s"
        .include "tr_minas.s"
        .include "tr_carpatos.s"
        .include "tr_castillo.s"
        .include "arena1.s"
        .include "arena2.s"
        .include "arena3.s"
        .include "arena4.s"
        .include "arena5.s"
        .include "arena6.s"
        .include "pantallas_ti.s"
        .include "pantallas_go.s"
        .segment "CODE"
        .include "motor/nucleo.s"
        .include "motor/pmg.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/pantalla.s"
        .include "motor/musica.s"
        .include "packs.inc"
        .include "carga.s"
        .include "arena_comun.s"
        .include "enemigos2.s"
        .include "enemigos_com.s"
        .include "tejados.s"
        .include "jefe_gen.s"
        .include "pantallas.s"
        .include "efectos.s"
        .include "cargador.s"
        ; módulos de fase (se cargan en $8000 desde la memoria extendida)
        .include "jefe1.s"
        .include "enemigos_f1.s"
        .include "jefe2.s"
        .include "enemigos_f2.s"
        .include "jefe3.s"
        .include "enemigos3.s"
        .include "fase4.s"
        .include "fase5.s"
        .segment "CODE"

; ===============================================================
start:  jsr m_init
        lda #<dli
        sta VDSLST
        lda #>dli
        sta VDSLST+1
        lda #0
        sta gmode
        sta hisc
        sta hisc+1
        sta hisc+2
        sta cheat
.ifdef PRUEBA
        lda #1              ; versión de pruebas: invencible
        sta cheat
.endif

; ---------------------------------------------------------------
; TÍTULO
; ---------------------------------------------------------------
        jmp title
title_txt:
        jsr snd_off
        lda #0
        sta gmode
        lda #>CHARSA
        sta CHBAS
        lda #$01
        sta GPRIOR
        lda #<DESC_T
        sta ptr
        lda #>DESC_T
        sta ptr+1
        jsr txt_build
        ; récord en la línea 6 (TSCR + 20*6)
        lda #<hisc
        sta src
        lda #0
        sta src+1
        lda #<(TSCR+20*5+REC_DIG)
        sta dst
        lda #>(TSCR+20*5+REC_DIG)
        sta dst+1
        lda #DIG0|$40
        jsr put6
        lda cheat
        beq @nc
        jsr show_inv
@nc:    jsr txt_colors
        jsr txt_show
        lda #0
        sta downs
        lda #1
        sta fireold
@w:     jsr m_wait
        jsr m_mando
        lda stked
        and #J_DOWN
        beq @nd
        inc downs
@nd:    lda stked
        and #(J_UP|J_LEFT|J_RIGHT)
        beq @nu
        lda #0
        sta downs
@nu:    lda fireed
        beq @w
        lda downs
        cmp #2
        bcc @go
        lda #1              ; truco: abajo, abajo, FIRE = invencible
        sta cheat
        jsr show_inv
        lda #11
        jsr sfx
        lda #0
        sta downs
        jmp @w
@go:    jmp newgame

txt_colors:
        lda #$0C
        sta COLOR0
        lda #$44
        sta COLOR1
        lda #$2A
        sta COLOR2
        lda #$0C
        sta COLOR3
        lda #$00
        sta COLOR4
        rts

show_inv:
        lda #<T_INV
        sta src
        lda #>T_INV
        sta src+1
        lda #<(TSCR+20*4)
        sta dst
        lda #>(TSCR+20*4)
        sta dst+1
        ldx #20
        jmp m_copy

DESC_T: .byte $70,$70,$70,$70
        .byte 7, <T_LA, >T_LA
        .byte 7, <T_STR, >T_STR
        .byte $70,$70
        .byte 6, <T_FASE, >T_FASE
        .byte 6, <T_CEM, >T_CEM
        .byte $70,$70,$70
        .byte 6, <T_FIRE, >T_FIRE
        .byte $70,$70
        .byte 6, <T_REC, >T_REC
        .byte $70,$70,$70,$70
        .byte 6, <T_AUT, >T_AUT
        .byte $FF

DESC_GO:.byte $70,$70,$70,$70,$70,$70,$70,$70
        .byte 7, <T_GO, >T_GO
        .byte $70,$70,$70
        .byte 6, <T_PTS, >T_PTS
        .byte $FF

DESC_END:
        .byte $70,$70,$70,$70,$70
        .byte 7, <T_E1, >T_E1
        .byte 7, <T_E2, >T_E2
        .byte $70,$70,$70
        .byte 6, <T_E3, >T_E3
        .byte 6, <T_E4, >T_E4
        .byte $70,$70,$70
        .byte 6, <T_PTS, >T_PTS
        .byte $FF

; pantalla de texto con los puntos en la línea n (A = n), espera X segundos y vuelve al título
txt_score_wait:
        pha
        jsr snd_off
        lda #0
        sta gmode
        lda #>CHARSA
        sta CHBAS
        jsr txt_build
        pla
        tax
        lda #<TSCR
        clc
@m:     dex
        bmi @d
        adc #20
        bcc @m
        clc
        bcc @m
@d:     adc #TXT_DIG
        sta dst
        lda #>TSCR
        adc #0
        sta dst+1
        lda #<score
        sta src
        lda #0
        sta src+1
        lda #DIG0
        jsr put6
        jsr hiupd
        jsr txt_colors
        jsr txt_show
        ldx #255
        jsr m_waitn
        ldx #45
        jsr m_waitn
        lda aftert+1
        bne *+5
        jmp title
        sta ptr+1
        lda aftert
        sta ptr
        lda #0
        sta aftert+1
        jmp (ptr)

; ---------------------------------------------------------------
newgame:
        lda #0
        sta score
        sta score+1
        sta score+2
        sta nextx
        sta nextx+1
        sta chk
        lda #EXTRA_STEP
        sta nextx+2
        lda #3
        sta lives
        lda #1
        sta fase
        sta card
        lda #0
        sta tramo
        sta aftert+1
.ifdef ESC_TEST
        lda #PK_ESC
        sta tramo
.endif
.ifdef FASE4_TEST
        lda #4
        sta fase
        lda #PK_CAR
        sta tramo
.endif
.ifdef FASE5_TEST
        lda #5
        sta fase
        lda #PK_CAS
        sta tramo
.endif
.ifdef FASE3_TEST
        lda #3
        sta fase
        lda #PK_MIN
        sta tramo
.endif
.ifdef FASE2_TEST
        lda #2
        sta fase
        lda #PK_CIU
        sta tramo
.endif
.ifdef ARENA_TEST
        lda #2              ; prueba: directo a la arena del jefe
        sta chk
.endif
        lda fase            ; el módulo de la fase
        jsr mod_load
        jmp level

gameover_txt:
        lda #<DESC_GO
        sta ptr
        lda #>DESC_GO
        sta ptr+1
        lda #1
        jmp txt_score_wait

finished:
        ldx #60
        jsr m_waitn
        lda #<DESC_END
        sta ptr
        lda #>DESC_END
        sta ptr+1
        lda #4
        jmp txt_score_wait

; ---------------------------------------------------------------
; empezar (o reaparecer) en la fase
; ---------------------------------------------------------------
level:  lda chk
        cmp #2
        bne @lv
        jmp arena_go
@lv:    lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta GRACTL
        sta gmode
        lda #<dli
        sta VDSLST
        lda #>dli
        sta VDSLST+1
        jsr snd_off
        jsr m_wait
        lda tramo
        jsr pack_load
        lda card
        beq @nc
        lda #0
        sta card
        jsr tr_card
@nc:    lda TR_END          ; límites del tramo en píxeles
        asl a
        sta tr_endx
        lda #0
        rol a
        asl tr_endx
        rol a
        sta tr_endx+1
        lda TR_CHK
        asl a
        sta tr_chkx
        lda #0
        rol a
        asl tr_chkx
        rol a
        sta tr_chkx+1
        ; display list
        lda #<DLTPL
        sta src
        lda #>DLTPL
        sta src+1
        lda #<DLGAME
        sta dst
        lda #>DLGAME
        sta dst+1
        ldx #DLLEN
        jsr m_copy
        ; cielo
        lda #<SKYROWS
        sta src
        lda #>SKYROWS
        sta src+1
        lda #<SKYSCR
        sta dst
        lda #>SKYSCR
        sta dst+1
        ldx #160
        jsr m_copy
        lda #<BLANK40
        sta dst
        lda #>BLANK40
        sta dst+1
        lda #0
        ldx #40
        jsr m_fill
        ; montañas: 3 anillos de 64 columnas (escritas dos veces)
        ldx #0
@mt:    lda MTNROWS,x
        sta MRING,x
        sta MRING+64,x
        lda MTNROWS+64,x
        sta MRING+128,x
        sta MRING+192,x
        lda MTNROWS+128,x
        sta MRING+256,x
        sta MRING+320,x
        inx
        cpx #64
        bne @mt
        ; marcador
        ldx #39
@hu:    lda HUDT,x
        sta HUD,x
        dex
        bpl @hu
        jsr hud_all
        ; tablas de la DLI
        ldx #21
@dt:    lda TBK,x
        sta DTBK,x
        lda TPF0,x
        sta DTPF0,x
        lda TPF1,x
        sta DTPF1,x
        lda TPF2,x
        sta DTPF2,x
        lda TPF3,x
        sta DTPF3,x
        lda #>CHARSB
        cpx #8
        bcs @cb
        lda #>CHARSC
        cpx #4
        bcs @cb
        lda #>CHARSA
@cb:    sta DTCH,x
        lda #0
        sta DTHS,x
        dex
        bpl @dt
        lda #>MAP
        sta mapb
        lda #<CLASS
        sta clsp
        lda #>CLASS
        sta clsp+1
        ; Radu y la cámara
        jsr respawn_state
        jsr ring_fill
        jsr pm_init
        lda #>CHARSA
        sta CHBAS
        lda #$00
        sta COLOR4
        sta COLOR2
        lda #$0C
        sta COLOR1
        lda #COL_PF3
        sta COLOR3
        lda #0
        sta SIZEP0
        sta SIZEP1
        sta SIZEP2
        sta SIZEP3
        lda #$31            ; quinto player + P0/P1 en OR + players delante
        sta GPRIOR
        lda #<DLGAME
        sta SDLSTL
        lda #>DLGAME
        sta SDLSTH
        jsr freeze
        lda #3
        sta GRACTL
        lda #1
        sta gmode
        jsr m_wait
        lda #$3E
        sta SDMCTL
        jsr m_wait
        jsr m_wait
        lda #$C0
        sta NMIEN
        lda TR_MUS
        jsr mus_play
        jmp loop

; posición inicial (o del punto de control)
respawn_state:
        lda chk
        beq @s
        lda tr_chkx
        sec
        sbc #64
        sta camx
        lda tr_chkx+1
        sbc #0
        sta camx+1
        jmp @c
@s:     lda #CAMMIN
        sta camx
        lda #0
        sta camx+1
@c:     lda camx
        clc
        adc #24
        sta rxl
        lda camx+1
        adc #0
        sta rxh
        lda #FLOOR
        sta ry
        lda #0
        sta ryf
        sta rvyl
        sta rvyh
        sta rst
        sta rdir
        sta rjvx
        sta rthrow
        sta ranim
        sta bact
        sta rdead
        sta etyp
        sta etyp+1
        sta rpol
        sta thits
        lda diff            ; HARDCORE: sin armadura
        eor #1
        sta rarmor
        lda #120
        sta rinv
        lda #0
        sta rinvc
        lda #90
        sta ztimer
        ; primera aparición pendiente según la cámara
        jsr cam_col
        sta tcol
        ldx #0
@sp:    cpx TR_NSP
        bcs @sd
        lda SP_CAM,x
        cmp tcol
        bcs @sd
        inx
        bne @sp
@sd:    stx spi
        rts

; rellena los anillos con las 64 columnas desde la izquierda de la cámara
ring_fill:
        jsr cam_left        ; A = primera columna visible
        sta wcolnx
        lda #0
        sta wcolnx+1
        ldx #64
@f:     txa
        pha
        lda wcolnx+1
        bne @n
        lda wcolnx
        jsr wcol
        inc wcolnx
        bne @n
        inc wcolnx+1
@n:     pla
        tax
        dex
        bne @f
        rts

; A = (camx - SCRK) / 4  (columna del anillo en el borde izquierdo de la ventana)
cam_left:
        lda camx
        sec
        sbc #SCRK
        sta tx
        lda camx+1
        sbc #0
        lsr a
        ror tx
        lsr a
        ror tx
        lda tx
        rts

; escribe la columna A del mapa en los anillos (dos copias)
wcol:   sta wc_col
        and #63
        sta wc_idx
        lda #<GRING
        sta dst
        lda #>GRING
        sta dst+1
        lda #0
        sta src
        lda #>MAP
        sta src+1
        ldx #13
@l:     ldy wc_col
        lda (src),y
        ldy wc_idx
        sta (dst),y
        pha
        tya
        ora #64
        tay
        pla
        sta (dst),y
        inc src+1
        lda dst
        clc
        adc #128
        sta dst
        bcc @n
        inc dst+1
@n:     dex
        bne @l
        rts

; ---------------------------------------------------------------
; BUCLE
; ---------------------------------------------------------------
loop:   jsr pm_wait
        jsr m_mando
        jsr ctl_fx
        jsr radu
        jsr wind_fx
        jsr camera
        jsr baltag
        jsr spawns
        jsr enemies
        jsr collide
        jsr draw
        jsr freeze
        jsr pm_end
        ; fin del tramo
        lda rst
        cmp #3
        beq @d
        lda rxh
        cmp tr_endx+1
        bcc @c
        bne @fin
        lda rxl
        cmp tr_endx
        bcc @c
@fin:   jmp tr_finish
@c:     ; punto de control
        lda chk
        bne @nk
        lda rxh
        cmp tr_chkx+1
        bcc @nk
        bne @k
        lda rxl
        cmp tr_chkx
        bcc @nk
@k:     lda #1
        sta chk
        lda #11
        jsr sfx
@nk:    jmp loop
@d:     ; muerto: cuenta atrás
        dec rdead
        bne @nk
        dec lives
        bne @r
        jmp gameover
@r:     jmp level

; ---------------------------------------------------------------
; RADU
; ---------------------------------------------------------------
radu:   lda rinv
        beq @i
        dec rinv
@i:     lda rpol
        beq @p
        lda frame
        and #3
        bne @p
        dec rpol
        bne @p
        lda #60             ; vuelve a ser Radu
        sta rinv
        lda #14
        jsr sfx
@p:     lda rthrow
        beq @t
        dec rthrow
@t:     lda rst
        cmp #3
        beq @dd
        lda ry              ; agua salada negra: muerte segura
        cmp #198
        bcc @a0
        lda cheat
        beq @ahog
        lda #<(-$0500)      ; (invencible: sale despedido hacia arriba)
        sta rvyl
        lda #>(-$0500)
        sta rvyh
        lda #1
        sta rst
        sta rjvx            ; y hacia delante
        lda rdir
        beq *+7
        lda #$FF
        sta rjvx
        jmp r_air
@ahog:  lda #0
        sta rarmor
        sta rpol
        lda #2
        jsr sfx
        jmp r_hit
@dd:    lda ry              ; la calavera se hunde en el agua y ya no cae más
        cmp #212
        bcc @dk
        rts
@dk:    lda #3
@a0:    lda rst
        cmp #3
        bne @a
        ; muerto: la calavera cae, rebota y rueda
        lda rjvx
        beq @df
        lda frame
        and #1
        bne @df
        lda rjvx
        jsr r_movex
@df:    jmp r_fall
@a:     cmp #0
        beq r_ground
        jmp r_air

r_ground:
        lda #0
        sta rcrouch
        lda rpol            ; el pollo no se agacha
        bne @nc
        lda stk
        and #J_DOWN
        beq @nc
        lda #1
        sta rcrouch
        jmp @fire
@nc:    lda stk
        and #J_LEFT
        beq @nl
        lda #1
        sta rdir
        lda rthrow
        bne @nl
        lda #$FF
        jsr r_movex
        inc ranim
@nl:    lda stk
        and #J_RIGHT
        beq @nr
        lda #0
        sta rdir
        lda rthrow
        bne @nr
        lda #1
        jsr r_movex
        inc ranim
@nr:    lda stk
        and #(J_LEFT|J_RIGHT)
        bne @w
        lda #0
        sta ranim
@w:     ; salto
        lda stked
        and #J_UP
        beq @fire
        lda #<(-JUMPV)
        sta rvyl
        lda #>(-JUMPV)
        sta rvyh
        lda #0
        sta rjvx
        lda stk
        and #J_LEFT
        beq @jl
        lda #$FF
        sta rjvx
@jl:    lda stk
        and #J_RIGHT
        beq @jr
        lda #1
        sta rjvx
@jr:    lda #1
        sta rst
        lda #3
        jsr sfx
        rts
@fire:  jsr r_throw
        ; ¿sigue apoyado?
        jsr r_support
        bcs @ok
        lda #1
        sta rst
        lda #0
        sta rvyl
        sta rvyh
        sta rjvx
        rts
@ok:    jmp frag_check

r_air:  lda #0
        sta rcrouch
        lda rst
        cmp #1
        bne @nt
        jsr r_throw
@nt:    lda rjvx
        beq r_fall
        jsr r_movex
r_fall: ; gravedad
        lda rvyl
        clc
        adc #GRAV
        sta rvyl
        lda rvyh
        adc #0
        sta rvyh
        bmi @up
        cmp #4
        bcc @up
        lda #4
        sta rvyh
        lda #0
        sta rvyl
@up:    lda ry
        sta tyy             ; pies antes
        lda ryf
        clc
        adc rvyl
        sta ryf
        lda ry
        adc rvyh
        sta ry
        lda rvyh
        bmi @r              ; subiendo
        ; ¿ha cruzado el borde superior de una fila sólida?
        lda ry
        cmp #GTOP
        bcc @r
        sec
        sbc #GTOP
        and #$F8
        clc
        adc #GTOP           ; borde de la fila en la que están los pies
        cmp tyy
        bcc @r              ; el borde estaba ya por encima de los pies
        sta edge            ; línea del borde
        lda ry
        pha
        lda edge
        sta ry
        jsr r_support
        pla
        bcc @nl
        ; aterriza
        lda edge
        sta ry
        lda #0
        sta ryf
        lda rst
        cmp #3
        beq @bote
        lda #0
        sta rvyl
        sta rvyh
        sta rst
        sta rjvx
        rts
@bote:  ; calavera: rebota con la mitad de velocidad hasta quedarse quieta
        lda rvyh
        cmp #2
        bcc @quieta
        lsr rvyh
        ror rvyl
        lda #0
        sec
        sbc rvyl
        sta rvyl
        lda #0
        sbc rvyh
        sta rvyh
        lda #16
        jmp sfx
@quieta:
        lda #0
        sta rvyl
        sta rvyh
        sta rjvx
        rts
@nl:    sta ry
@r:     rts

; C = 1 si hay suelo bajo los pies (fila de ry, columnas x+2 y x+5)
r_support:
        lda ry
        cmp #GTOP
        bcc @no
        lda rxl
        clc
        adc #2
        sta tx
        lda rxh
        adc #0
        sta tx+1
        jsr t_solid
        bcs @yes
        lda rxl
        clc
        adc #5
        sta tx
        lda rxh
        adc #0
        sta tx+1
        jsr t_solid
        rts
@no:    clc
@yes:   rts

; A = columna de tx (x del mundo de 10 bits / 4); conserva X e Y
col_tx: lda tx
        lsr a
        lsr a
        sta tcol
        lda tx+1
        asl a
        asl a
        asl a
        asl a
        asl a
        asl a
        ora tcol
        sta tcol
        rts

; ¿es sólida la casilla del mundo (tx, línea A)? -> C
t_solid:
        lda ry
t_solid_a:
        cmp #GTOP
        bcc @no
        cmp #GTOP+13*8
        bcs @no
        sec
        sbc #GTOP
        lsr a
        lsr a
        lsr a
        ldy mapb            ; mapb = 0: arena de suelo liso (filas 10-12)
        bne @mp
        cmp #10
        bcs @si
        bcc @no
@mp:    clc
        adc mapb
        sta mp+1
        lda #0
        sta mp
        jsr col_tx
        tay
        lda (mp),y
        and #$7F            ; los inversos (PF3) son decorado del mismo carácter
        tay
        lda (clsp),y
        cmp #1
        beq @si
        cmp #3              ; pasarela que se hunde: también sostiene
        beq @si
        cmp #4              ; pinchos: también sostienen (y hieren)
        bne @no
@si:    sec
        rts
@no:    clc
        rts

; mueve a Radu A (+1 / -1) en x, con paredes y límites de pantalla
r_movex:
        sta hitl
        cmp #1
        bne @l
        ; derecha: columna x+8
        lda rxl
        clc
        adc #8
        sta tx
        lda rxh
        adc #0
        sta tx+1
        jmp @chk
@l:     lda rxl
        sec
        sbc #1
        sta tx
        lda rxh
        sbc #0
        sta tx+1
@chk:   lda ry
        sec
        sbc #1
        jsr t_solid_a
        bcc @nostep
        ; ¿un peldaño? (en el suelo y con sitio encima)
        lda rst
        bne @blk0
        lda ry
        sec
        sbc #9
        jsr t_solid_a
        bcs @blk0
        lda ry
        sec
        sbc #20
        jsr t_solid_a
        bcs @blk0
        lda ry
        sec
        sbc #31
        jsr t_solid_a
        bcs @blk0
        lda ry
        sec
        sbc #8
        sta ry
        jmp @mov
@blk0:  jmp @blk
@nostep:
        lda ry
        sec
        sbc #12
        jsr t_solid_a
        bcc *+5
        jmp @blk
        lda ry
        sec
        sbc #20
        jsr t_solid_a
        bcs @blk
@mov:   ; mover
        lda hitl
        bmi @ml
        inc rxl
        bne @lim
        inc rxh
        jmp @lim
@ml:    lda rxl             ; no pasar del borde izquierdo de la cámara
        cmp camx
        bne @m0
        lda rxh
        cmp camx+1
        beq @blk
@m0:    lda rxl
        bne @m1
        dec rxh
@m1:    dec rxl
@lim:   ; límite izquierdo: camx
        lda rxh
        cmp camx+1
        bcc @fixl
        bne @rr
        lda rxl
        cmp camx
        bcs @rr
@fixl:  lda camx
        sta rxl
        lda camx+1
        sta rxh
@rr:    ; límite derecho: camx + 152
        lda camx
        clc
        adc #152
        sta tx
        lda camx+1
        adc #0
        sta tx+1
        lda rxh
        cmp tx+1
        bcc @blk
        bne @fixr
        lda rxl
        cmp tx
        bcc @blk
@fixr:  lda tx
        sta rxl
        lda tx+1
        sta rxh
@blk:   rts

; lanzar el baltag
r_throw:
        lda rpol            ; el pollo no lanza
        bne @r
        lda gmode
        cmp #2
        bne @th
        lda bphase
        cmp #3
        beq @r
@th:
        lda fireed
        beq @r
        lda bact
        bne @r
        lda rthrow
        bne @r
        lda #12
        sta rthrow
        lda #1
        sta bact
        lda rdir
        sta bdir
        lda #0
        sta bfr
        lda rdir
        bne @lf
        lda rxl
        clc
        adc #6
        sta bxl
        lda rxh
        adc #0
        sta bxh
        jmp @y
@lf:    lda rxl
        sec
        sbc #6
        sta bxl
        lda rxh
        sbc #0
        sta bxh
@y:     lda ry
        sec
        sbc #19
        ldx rcrouch
        beq @s
        clc
        adc #10
@s:     sta by
        lda #0
        jsr sfx
@r:     rts

; ---------------------------------------------------------------
; CÁMARA: sigue a Radu hacia la derecha (no vuelve atrás)
; ---------------------------------------------------------------
camera: lda rxl
        sec
        sbc #64
        sta tx
        lda rxh
        sbc #0
        sta tx+1
        bmi @r
        lda tx+1
        cmp camx+1
        bcc @r
        bne @mv
        lda tx
        cmp camx
        bcc @r
        beq @r
@mv:    ; un paso de 1 (Radu avanza 1 por cuadro)
        inc camx
        bne @cl
        inc camx+1
@cl:    lda camx+1
        cmp #>CAMMAX
        bcc @w
        lda camx
        cmp #<CAMMAX
        bcc @w
        lda #<CAMMAX
        sta camx
        lda #>CAMMAX
        sta camx+1
@w:     ; columnas nuevas en los anillos: hasta izquierda + 47
        jsr cam_left
        clc
        adc #47
        sta tcol
        bcs @r
        lda wcolnx+1
        bne @r
        lda wcolnx
        cmp tcol
        beq @wr
        bcs @r
@wr:    jsr wcol
        inc wcolnx
        bne @r
        inc wcolnx+1
@r:     rts

; congela lo que la VBI necesita para el búfer en preparación
freeze: ldx rb
        jsr cam_left
        and #63
        sta camb_gl,x
        lda camx
        sec
        sbc #SCRK
        and #3
        eor #3
        sta camb_gh,x
        lda camx+1
        lsr a
        lda camx
        ror a               ; camx / 2 (anillo de 256 relojes)
        pha
        lsr a
        lsr a
        sta camb_ml,x
        pla
        and #3
        eor #3
        sta camb_mh,x
        rts

; ---------------------------------------------------------------
; BALTAG
; ---------------------------------------------------------------
baltag: lda bact
        beq @r
        lda frame
        and #3
        bne @nf
        inc bfr
@nf:    lda bdir
        bne @l
        lda bxl
        clc
        adc #4
        sta bxl
        bcc @c
        inc bxh
        bcs @c
@l:     lda bxl
        sec
        sbc #4
        sta bxl
        bcs @c
        dec bxh
@c:     ; ¿fuera de pantalla?
        lda bxl
        sec
        sbc camx
        sta sx
        lda bxh
        sbc camx+1
        bne @off
        lda sx
        cmp #160
        bcs @off
        ; ¿piedra?
        lda bxl
        clc
        adc #4
        sta tx
        lda bxh
        adc #0
        sta tx+1
        lda gmode           ; en la arena el hacha pasa por encima de las tumbas
        cmp #2
        bne @p4
        lda by
        clc
        adc #2
        bne @pc
@p4:    lda by
        clc
        adc #4
@pc:    jsr t_solid_a
        bcc @r
        lda #8
        jsr sfx
        jsr tomb_hit
@off:   lda #0
        sta bact
@r:     rts

; ---------------------------------------------------------------
; APARICIONES
; ---------------------------------------------------------------
spawns: lda etyp             ; con bruja o hechizo en pantalla no sale nada más
        cmp #4
        beq @sb
        cmp #5
        beq @sb
        lda etyp+1
        cmp #4
        beq @sb
        cmp #5
        bne @sg
@sb:    rts
@sg:    ; programadas por columna de cámara
        ldx spi
        cpx TR_NSP
        bcs @rnd
        jsr cam_col
        cmp SP_CAM,x
        bcc @rnd
        jsr free_slot
        bcc @rnd
        ldx spi
        lda SP_TYP,x
        cmp #1
        bne @crow
        lda SP_COL,x
        jsr zombie_at
        jmp @adv
@crow:  cmp #2
        bne @oth
        lda SP_Y,x
        jsr crow_new
        jmp @adv
@oth:   jsr spawn_x
@adv:   inc spi
        rts
@rnd:   ; zombis al azar cerca de Radu
        lda rst
        bne @r
        dec ztimer
        bne @r
        lda RANDOM
        and #63
        clc
        adc #80
        sta ztimer
        jsr free_slot
        bcc @r
        ; columna: Radu ± (8..15)
        lda rxl
        sta tx
        lda rxh
        sta tx+1
        jsr col_tx
        lda RANDOM
        and #7
        clc
        adc #8
        sta hitl
        lda RANDOM
        and #3
        beq @left           ; casi siempre por delante
        lda rdir
        bne @left
        lda tcol
        clc
        adc hitl
        bcs @r
        jmp @z
@left:  lda tcol
        sec
        sbc hitl
        bcc @r
@z:     jsr zombie_at
@r:     rts

cam_col:
        lda camx
        sta tx
        lda camx+1
        sta tx+1
        jmp col_tx

; C = 1 y X = hueco libre
free_slot:
        ldx #NSLOT-1
@l:     lda etyp,x
        beq @y
        dex
        bpl @l
        clc
        rts
@y:     sec
        rts

; zombi en la columna A (si la casilla sobre el suelo está libre y es visible)
zombie_at:
        sta zcol
        ; visible: columna entre cam_col+1 y cam_col+38
        jsr cam_col
        sta hitl
        lda zcol
        sec
        sbc hitl
        bcc @r
        cmp #2
        bcc @r
        cmp #38
        bcs @r
        ; suelo libre encima (fila SURF-1 del mapa) en tcol y tcol+1
        lda #(>MAP)+SURF-1
        sta mp+1
        lda #0
        sta mp
        ldy zcol
        lda (mp),y
        tay
        lda CLASS,y
        bne @r
        ldy zcol
        iny
        lda (mp),y
        tay
        lda CLASS,y
        bne @r
        jsr free_slot
        bcc @r
        lda #1
        sta etyp,x
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        lda zcol
        asl a
        asl a
        sta exl,x
        lda zcol
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        sta exh,x
        lda #FLOOR
        sta ey,x
        lda #240
        sta elife,x
        jsr face_radu
        lda #4
        jsr sfx
@r:     rts

; cuervo que entra por la derecha a la altura A
crow_new:
        sta tyy
        jsr free_slot
        bcc @r
        lda #2
        sta etyp,x
        lda #0
        sta est,x
        sta et,x
        lda #1
        sta edir,x
        lda camx
        clc
        adc #160
        sta exl,x
        lda camx+1
        adc #0
        sta exh,x
        lda tyy
        sta ey,x
        lda #5
        jsr sfx
@r:     rts

; edir,x = hacia Radu
face_radu:
        lda #0
        sta edir,x
        lda exh,x
        cmp rxh
        bcc @r
        bne @l
        lda exl,x
        cmp rxl
        bcc @r
@l:     lda #1
        sta edir,x
@r:     rts

; ---------------------------------------------------------------
; ENEMIGOS
; ---------------------------------------------------------------
enemies:
        ldx #NSLOT-1
@l:     stx cur
        lda etyp,x
        bne *+5
        jmp @n
        cmp #1
        bne @c
        jsr e_zombie
        jmp @n
@c:     cmp #2
        bne @p
        jsr e_crow
        jmp @n
@p:     cmp #3
        bne @wi
        jsr e_puff
        jmp @n
@wi:    cmp #4
        bne @sp
        jsr e_witch
        jmp @n
@sp:    cmp #5
        bne @bt
        jsr e_spell
        jmp @n
@bt:    cmp #6
        bne @bl
        jsr e_bat
        jmp @n
@bl:    cmp #7
        bne @v8
        jsr e_blast
        jmp @n
@v8:    cmp #8
        bne @v9
        jsr e_vav
        jmp @n
@v9:    cmp #9
        bne @v10
        jsr e_iele
        jmp @n
@v10:   cmp #10
        bne @v11
        jsr e_garg
        jmp @n
@v11:   cmp #11
        bne @v12
        jsr e_tij
        jmp @n
@v12:   cmp #12
        bne @v13
        jsr e_agu
        jmp @n
@v13:   cmp #13
        bne @v14
        jsr e_stone
        jmp @n
@v14:   jsr e_tipoN
@n:     ldx cur
        ; fuera de pantalla -> libre
        lda etyp,x
        beq @nx
        lda exl,x
        sec
        sbc camx
        sta sx
        lda exh,x
        sbc camx+1
        beq @in
        cmp #$FF
        bne @kill
        lda sx
        cmp #$F0
        bcs @nx
        bcc @kill
@in:    lda sx
        cmp #172
        bcc @nx
@kill:  lda #0
        sta etyp,x
@nx:    dex
        bmi *+5
        jmp @l
        rts

e_zombie:
        lda est,x
        bne @walk
        ; sale del suelo
        lda frame
        and #1
        beq *+5
        jmp @r
        inc et,x
        lda et,x
        cmp #ZH
        bcs *+5
        jmp @r
        lda #1
        sta est,x
        rts
@walk:  cmp #2
        bne *+5
        jmp @sink
        dec elife,x
        bne @w
        lda #2
        sta est,x
        rts
@w:     lda frame
        and #15
        bne @nf
        lda efr,x
        eor #1
        sta efr,x
@nf:    lda frame
        and #1
        bne @r
        lda frame
        and #63
        bne @nfc
        jsr face_radu
@nfc:   lda edir,x
        bne @pl
        lda exl,x
        clc
        adc #8
        sta tx
        lda exh,x
        adc #0
        sta tx+1
        jmp @pc
@pl:    lda exl,x
        sec
        sbc #1
        sta tx
        lda exh,x
        sbc #0
        sta tx+1
@pc:    lda ey,x
        sec
        sbc #4
        jsr t_solid_a
        bcc @mv
        lda edir,x
        eor #1
        sta edir,x
        rts
@mv:    lda edir,x
        bne @wl
        inc exl,x
        bne @r
        inc exh,x
        rts
@wl:    lda exl,x
        bne @w1
        dec exh,x
@w1:    dec exl,x
@r:     rts
@sink:  lda frame
        and #1
        bne @r
        dec et,x
        bne @r
        lda #0
        sta etyp,x
        rts

e_crow: inc et,x
        lda frame
        and #7
        bne @nf
        lda efr,x
        eor #1
        sta efr,x
@nf:    ; avanza 1,5 por cuadro hacia la izquierda
        lda exl,x
        sec
        sbc #1
        sta exl,x
        bcs @a
        dec exh,x
@a:     lda frame
        and #1
        beq @b
        lda exl,x
        sec
        sbc #1
        sta exl,x
        bcs @b
        dec exh,x
@b:     ; si Radu está cerca por delante, baja hacia su cabeza
        lda exl,x
        sec
        sbc rxl
        sta hitl
        lda exh,x
        sbc rxh
        bne @bob
        lda hitl
        cmp #56
        bcs @bob
        lda ry
        sec
        sbc #22
        cmp ey,x
        beq @r
        bcc @upw
        inc ey,x
        rts
@upw:   dec ey,x
@r:     rts
@bob:   lda et,x
        and #15
        bne @r
        lda et,x
        and #16
        beq @dn
        dec ey,x
        dec ey,x
        rts
@dn:    inc ey,x
        inc ey,x
        rts

e_puff: inc et,x
        lda et,x
        lsr a
        lsr a
        lsr a
        sta efr,x
        cmp #3
        bcc @r
        lda #0
        sta etyp,x
@r:     rts

; ---------------------------------------------------------------
; HOMENAJE A GHOSTS'N GOBLINS: golpear una tumba hace salir a la bruja
; ---------------------------------------------------------------
; el baltag ha dado en piedra en la columna tcol
tomb_hit:
        lda gmode
        cmp #1
        bne @r
        lda rpol
        bne @r
        lda etyp
        cmp #4
        bcs @r
        lda etyp+1
        cmp #4
        bcs @r
        lda tcol
        sec
        sbc thcol
        bcs @p
        eor #$FF
        adc #1
@p:     cmp #4
        bcc @same
        lda tcol
        sta thcol
        lda #0
        sta thits
@same:  inc thits
        lda thits
        cmp #TOMBHITS
        bcc @r
        lda #0
        sta thits
        ; cima de la tumba: primera fila sólida desde arriba en tcol
        lda #0
        sta mp
        lda #>MAP
        sta mp+1
        ldx #0
@f:     ldy tcol
        lda (mp),y
        tay
        lda CLASS,y
        cmp #1
        beq @top
        inc mp+1
        inx
        cpx #SURF
        bne @f
@r:     rts
@top:   txa
        asl a
        asl a
        asl a
        clc
        adc #GTOP
        sta tyy
        jsr free_slot
        bcs @s
        ldx #0              ; sin hueco libre: ocupa el primero
@s:     lda #4
        sta etyp,x
        lda #0
        sta est,x
        sta et,x
        sta efr,x
        lda tcol
        asl a
        asl a
        sta exl,x
        lda tcol
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        sta exh,x
        lda tyy
        sta ey,x
        jsr face_radu
        lda #12
        jmp sfx

; bruja: aparece (32 cuadros), espera, lanza el hechizo y se esfuma
e_witch:
        inc et,x
        bne @c
        dec et,x
@c:     lda est,x
        bne @s1
        lda et,x
        cmp #16             ; aparición corta
        bcs *+5
        jmp @r
        lda #1
        sta est,x
        lda #0
        sta et,x
        rts
@s1:    cmp #1
        bne @s2
        lda frame
        and #63
        bne @nf
        jsr face_radu
@nf:    lda et,x
        cmp #12             ; lanza casi en seguida
        bcc @r
        txa                 ; el hechizo va en el otro hueco (si hay un enemigo, desaparece)
        eor #1
        tay
@cast:  lda #5
        sta etyp,y
        lda #0
        sta est,y
        sta et,y
        sta efr,y
        lda exl,x
        sta exl,y
        lda exh,x
        sta exh,y
        lda ey,x
        sec
        sbc #14
        sta ey,y
        lda #2
        sta est,x
        lda #0
        sta et,x
        lda #1
        sta efr,x
        lda #15
        jmp sfx
@s2:    lda et,x
        cmp #40
        bcc @r
@van:   lda #3
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        lda ey,x
        sec
        sbc #12
        sta ey,x
@r:     rts

; hechizo: persigue a Radu despacio (x: 3 de cada 4 cuadros, y: 1 de cada 2)
e_spell:
        inc et,x
        lda et,x
        cmp #240
        bcc @mv
        lda #3
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        rts
@mv:    lda frame
        and #3
        beq @y
        lda exh,x
        cmp rxh
        bcc @rt
        bne @lf
        lda exl,x
        cmp rxl
        beq @y
        bcc @rt
@lf:    lda exl,x
        bne @l1
        dec exh,x
@l1:    dec exl,x
        jmp @y
@rt:    inc exl,x
        bne @y
        inc exh,x
@y:     lda frame
        and #1
        bne @an
        lda ry
        sec
        sbc #16
        cmp ey,x
        beq @an
        bcc @up
        inc ey,x
        jmp @an
@up:    dec ey,x
@an:    lda frame
        lsr a
        lsr a
        and #1
        sta efr,x
        rts

; ---------------------------------------------------------------
; COLISIONES: baltag contra enemigos, enemigos contra Radu
; ---------------------------------------------------------------
; caja del enemigo x en hitl/hitr (x de pantalla) y hitt/hitb (líneas); C = 0 si no golpeable
ebox:   lda exl,x
        sec
        sbc camx
        sta hitl
        clc
        adc #6
        sta hitr
        inc hitl
        lda etyp,x
        cmp #8
        bcc *+5
        jmp ebox2
        cmp #1
        bne @c
        lda et,x
        cmp #8
        bcc @no
        lda ey,x
        sta hitb
        sec
        sbc et,x
        sta hitt
        sec
        rts
@c:     cmp #2
        beq @b8
        cmp #5
        beq @b8
        cmp #6
        beq @b8
        cmp #4
        bne @no
        lda est,x           ; bruja: golpeable cuando ya ha aparecido
        beq @no
        lda ey,x
        sta hitb
        sec
        sbc #BH
        sta hitt
        sec
        rts
@b8:    lda ey,x
        sta hitt
        clc
        adc #7
        sta hitb
        sec
        rts
@no:    clc
        rts

collide:
        ldx #NSLOT-1
@l:     stx cur
        lda etyp,x
        bne *+5
        jmp @n
        jsr ebox
        bcs *+5
        jmp @n
        ; baltag
        lda bact
        bne *+5
        jmp @radu
        lda etyp,x
        cmp #5
        bne *+5
        jmp @radu
        lda bxl
        sec
        sbc camx
        sta sx              ; x de pantalla del baltag
        clc
        adc #7
        cmp hitl
        bcs *+5
        jmp @radu
        lda sx
        cmp hitr
        bcc *+5
        jmp @radu
        lda by
        clc
        adc #7
        cmp hitt
        bcs *+5
        jmp @radu
        lda by
        cmp hitb
        bcc *+5
        jmp @radu
        ; ¡golpe!
        lda etyp,x
        cmp #10             ; la gárgola y la Vâlva Băii aguantan dos golpes
        beq @two
        cmp #15
        beq @two
        cmp #21
        bne @kil
@two:   dec ehp,x
        beq @kil
        lda etyp,x
        cmp #10
        bne @hv
        lda #0
        sta bact
        lda #16
        jsr sfx
        lda #3
        sta est,x           ; se queda parpadeando un momento
        lda #0
        sta et,x
        jmp @n
@hv:    lda #0
        sta bact
        lda #16
        jsr sfx
        jmp @n
@kil:   lda etyp,x
        sta tyy
        lda #0
        sta bact
        lda #3
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        lda hitt
        sta ey,x
        lda #1
        jsr sfx
        lda #2
        jsr sfx
        lda tyy
        cmp #4
        bne @s1
        lda #$00            ; bruja: 1.000
        ldx #$10
        bne @s2
@s1:    lda #$00            ; 100
        ldx #$01
@s2:    jsr addsc
        bcc @ns
        inc lives
        lda #10
        jsr sfx
@ns:    jsr hud_all
        ldx cur
        jmp @n
@radu:  ; Radu
        lda rst
        cmp #3
        beq @n
        lda etyp,x
        cmp #4              ; la bruja no hace daño al tocarla
        beq @n
        cmp #5              ; el hechizo alcanza siempre
        beq @geo
        lda rinv
        bne @n
        lda cheat
        bne @n
@geo:   lda rxl
        sec
        sbc camx
        sta sx
        clc
        adc #6
        cmp hitl
        bcc @n
        lda sx
        clc
        adc #1
        cmp hitr
        bcs @n
        lda ry
        cmp hitt
        bcc @n
        lda ry
        sec
        sbc #22
        ldy rcrouch
        bne @lo
        ldy rpol
        beq @nc
@lo:    clc
        adc #10
@nc:    cmp hitb
        bcs @n
        jsr r_touch
@n:     ldx cur
        dex
        bmi *+5
        jmp @l
        rts

; Radu toca al enemigo cur
r_touch:
        ldx cur
        lda etyp,x
        cmp #20             ; fuego fatuo: cambia los mandos, no hiere
        bne @nf
        lda #240
        sta rinvc
        lda #3
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        lda #13
        jmp sfx
@nf:    cmp #5
        beq @sp
        jmp r_hit
@sp:    lda #3              ; el hechizo estalla
        sta etyp,x
        lda #0
        sta et,x
        sta efr,x
        lda rpol
        bne @r
        lda #225            ; 15 segundos de pollo
        sta rpol
        lda #0
        sta rthrow
        sta rcrouch
        sta bact
        lda #13
        jsr sfx
@r:     rts

r_hit:  lda rpol            ; el pollo muere de un golpe
        bne @die
        lda rarmor
        beq @die
        lda #0
        sta rarmor
        lda #2
        sta rst
        lda #$00
        sta rvyl
        lda #$FE
        sta rvyh
        lda rdir
        beq @kl
        lda #1
        bne @kv
@kl:    lda #$FF
@kv:    sta rjvx
        lda #120
        sta rinv
        lda #6
        jmp sfx
@die:   lda #0
        sta rpol
        lda #3
        sta rst
        lda #150
        sta rdead
        lda ry              ; la calavera empieza donde estaba la cabeza
        sec
        sbc #14
        sta ry
        lda #$00
        sta rvyl
        lda #$FD            ; -3: la calavera salta y cae rebotando
        sta rvyh
        lda rdir            ; rueda hacia atrás
        beq @rl
        lda #1
        bne @rv
@rl:    lda #$FF
@rv:    sta rjvx
        lda #0
        sta bact
        lda #7
        jsr sfx
        lda #9
        jmp sfx

; ---------------------------------------------------------------
; MARCADOR
; ---------------------------------------------------------------
hud_all:
        lda gmode
        cmp #2
        bne @h
        jmp hud_arena
@h:     lda #<score
        sta src
        lda #0
        sta src+1
        lda #<(HUD+HUD_SC)
        sta dst
        lda #>(HUD+HUD_SC)
        sta dst+1
        lda #DIG0
        jsr put6
        jsr hiupd
        lda #<hisc
        sta src
        lda #0
        sta src+1
        lda #<(HUD+HUD_HI)
        sta dst
        lda #>(HUD+HUD_HI)
        sta dst+1
        lda #DIG0
        jsr put6
        lda lives
        cmp #10
        bcc @l
        lda #9
@l:     clc
        adc #DIG0
        sta HUD+HUD_LV
        rts

; ---------------------------------------------------------------
; DIBUJO (búfer oculto)
; ---------------------------------------------------------------
draw:   jsr pm_begin
        ; --- Radu
        lda rinv
        and #4
        beq @vis
        lda rst
        cmp #3
        beq @vis
        jmp @baltag
@vis:   lda rst
        cmp #3
        bne @viv
        lda #<CALAVERA
        sta src
        lda #>CALAVERA
        sta src+1
        lda #$06
        sta pc0
        lda #$0C
        sta pc1
        lda rxl
        sec
        sbc camx
        clc
        adc #HP0
        ldx rb
        sta PHP0,x
        sta PHP1,x
        lda pc0
        sta PCP0,x
        lda pc1
        sta PCP1,x
        lda ry
        sec
        sbc #8
        sta tyy
        ldx #0
        ldy #8
        jsr pm_spr
        lda #<(CALAVERA+8)
        sta src
        lda #>(CALAVERA+8)
        sta src+1
        ldx #1
        lda tyy
        ldy #8
        jsr pm_spr
        jmp @baltag
@viv:   lda rpol
        beq @rad
        cmp #30             ; los 2 últimos segundos parpadea
        bcs @pv
        lda frame
        and #4
        beq @pv
        jmp @baltag
@pv:    ldy #2              ; salto
        lda rst
        bne @pd
        ldy #0
        lda ranim
        and #8
        beq @pd
        ldy #1
@pd:    tya
        ldx rdir
        beq @p0
        clc
        adc #3
@p0:    tay
        lda POL_LO,y
        sta src
        lda POL_HI,y
        sta src+1
        lda #COL_POLLO0
        sta pc0
        lda #COL_POLLO1
        sta pc1
        jmp @pos
@rad:   jsr r_frame
        ; índice = camisa*16 + espejo*8 + cuadro
        lda rarmor
        eor #1
        asl a
        ora rdir
        asl a
        asl a
        asl a
        ora rframe
        tay
        lda RSPR_LO,y
        sta src
        lda RSPR_HI,y
        sta src+1
        lda #COL_P0
        sta pc0
        lda #COL_P1
        sta pc1
@pos:   lda rxl
        sec
        sbc camx
        clc
        adc #HP0
        ldx rb
        sta PHP0,x
        sta PHP1,x
        lda pc0
        sta PCP0,x
        lda pc1
        sta PCP1,x
        lda ry
        sec
        sbc #RH
        sta tyy
        ldx #0
        ldy #RH
        jsr pm_spr
        lda src
        clc
        adc #RH
        sta src
        bcc @s1
        inc src+1
@s1:    ldx #1
        lda tyy
        ldy #RH
        jsr pm_spr
@baltag:
        lda bact
        beq @en
        lda bxl
        sec
        sbc camx
        clc
        adc #HP0
        ldx rb
        sta PHM3,x
        clc
        adc #2
        sta PHM2,x
        adc #2
        sta PHM1,x
        adc #2
        sta PHM0,x
        lda bfr
        and #3
        asl a
        asl a
        asl a
        tax
        lda pmhi
        clc
        adc #3
        sta pmdst+1
        lda by
        sta pmdst
        ldy #0
@bl:    lda BSPR,x
        sta (pmdst),y
        inx
        iny
        cpy #8
        bne @bl
@en:    ; --- enemigos: hueco 0 -> P2, hueco 1 -> P3
        ldx #0
@el:    stx cur
        jsr e_draw
        ldx cur
        inx
        cpx #NSLOT
        bne @el
        rts

; cuadro de Radu -> rframe
r_frame:
        lda rst
        cmp #2
        bcs @hurt
        cmp #1
        beq @air
        lda rcrouch
        beq @st
        lda #RF_AGACHADO
        ldx rthrow
        beq @f
        lda #RF_AGACHALANZA
        bne @f
@st:    lda rthrow
        beq @wk
        lda #RF_LANZA
        bne @f
@wk:    lda ranim
        beq @q
        lsr a
        lsr a
        lsr a
        and #3
        tax
        lda WALKSEQ,x
        bne @f
@q:     lda #RF_QUIETO
        beq @f
@air:   lda rthrow
        beq @j
        lda #RF_LANZA
        bne @f
@j:     lda #RF_SALTO
        bne @f
@hurt:  lda #RF_GOLPE
@f:     sta rframe
        rts
WALKSEQ:.byte RF_PASO1, RF_QUIETO, RF_PASO2, RF_QUIETO
; calavera de Radu: P0 (8 líneas) y P1 (8 líneas); P0+P1 = blanco, solo P0 = gris
CALAVERA:
        .byte %00111100,%01111110,%11111111,%10011001,%10011001,%11110111,%01111110,%00101100
        .byte %00111100,%01111100,%11111110,%10011000,%10011000,%11110110,%01111100,%00101000

e_draw: lda etyp,x
        bne @g
        rts
@g:     lda exl,x
        sec
        sbc camx
        sta sx
        lda exh,x
        sbc camx+1
        beq @on
        rts
@on:    lda sx
        cmp #160
        bcc @ok
        rts
@ok:    clc
        adc #HP0
        ldy rb
        cpx #0
        bne @p3
        sta PHP2,y
        jmp @col
@p3:    sta PHP3,y
@col:   lda etyp,x
        cmp #8
        bcc *+5
        jmp e_draw2
        cmp #1
        bne @cr
        ; zombi: las et primeras líneas, con la base en ey
        lda #COL_ZOMBI
        jsr e_color
        lda edir,x
        asl a
        ora efr,x
        tay
        lda ZSPR_LO,y
        sta src
        lda ZSPR_HI,y
        sta src+1
        lda ey,x
        sec
        sbc et,x
        pha
        lda et,x
        tay
        pla
        jmp e_put
@cr:    cmp #2
        bne @pf
        lda #COL_CUERVO
        jsr e_color
        lda edir,x
        asl a
        ora efr,x
        tay
        lda CSPR_LO,y
        sta src
        lda CSPR_HI,y
        sta src+1
        lda ey,x
        ldy #8
        jmp e_put
@pf:    cmp #3
        bne *+5
        jmp @puff
        cmp #4
        bne @spl
        lda est,x           ; bruja: parpadea mientras aparece
        bne @bv
        lda frame
        and #2
        beq @bv
        rts
@bv:    lda #COL_BRUJA
        jsr e_color
        lda edir,x
        asl a
        ora efr,x
        tay
        lda BRU_LO,y
        sta src
        lda BRU_HI,y
        sta src+1
        lda ey,x
        sec
        sbc #BH
        ldy #BH
        jmp e_put
@spl:   cmp #7
        bne @sp6
        ldy efr,x           ; explosión grande
        lda BLASTCOL,y
        jsr e_color
        lda efr,x
        asl a
        asl a
        asl a
        asl a
        clc
        adc #<BLAST
        sta src
        lda #>BLAST
        adc #0
        sta src+1
        lda ey,x
        ldy #16
        jmp e_put
@sp6:   cmp #6
        bne @spe
        lda #COL_BAT        ; murciélago
        jsr e_color
        lda efr,x
        asl a
        asl a
        asl a
        clc
        adc #<BATS
        sta src
        lda #>BATS
        adc #0
        sta src+1
        lda ey,x
        ldy #8
        jmp e_put
@spe:   lda frame           ; hechizo: color cambiante
        asl a
        asl a
        asl a
        asl a
        ora #$0C
        jsr e_color
        ldy efr,x
        lda HEC_LO,y
        sta src
        lda HEC_HI,y
        sta src+1
        lda ey,x
        ldy #8
        jmp e_put
@puff:  lda #COL_PUFF
        jsr e_color
        ldy efr,x
        lda PSPR_LO,y
        sta src
        lda PSPR_HI,y
        sta src+1
        lda ey,x
        ldy #8
; A = y, Y = altura, cur = hueco
e_put:  cpy #0
        beq @r
        pha
        lda cur
        clc
        adc #2
        tax
        pla
        jsr pm_spr
@r:     rts

e_color:
        ldy rb
        cpx #0
        bne @3
        sta PCP2,y
        rts
@3:     sta PCP3,y
        rts

; ---------------------------------------------------------------
; VBI y DLI
; ---------------------------------------------------------------
vbi_juego:
        lda gmode
        bne @g
        rts
@g:     cmp #2
        bne @sc
        jsr pm_vbi
        lda #0
        sta HSCROL
        sta dlin
        rts
@sc:    jsr pm_vbi
        ldx shown
        ; LMS del cementerio (13 filas) y de las montañas (3 filas)
        lda camb_gl,x
        sta vt
        lda camb_ml,x
        sta vt+1
        lda camb_gh,x
        sta vt+2
        lda camb_mh,x
        sta vt+3
        ldx #12
@g1:    ldy GDLOFF,x
        lda GRLO,x
        clc
        adc vt
        sta DLGAME,y
        dex
        bpl @g1
        ldx #2
@m1:    ldy MDLOFF,x
        lda MRLO,x
        clc
        adc vt+1
        sta DLGAME,y
        dex
        bpl @m1
        ; HSCROL por fila: 0-7 montañas, 8-21 cementerio
        lda vt+3
        sta HSCROL
        ldx #6
@h1:    sta DTHS,x
        dex
        bpl @h1
        lda vt+2
        ldx #21
@h2:    sta DTHS,x
        dex
        cpx #7
        bcs @h2
        lda #0
        sta dlin
        rts

dli:    sta dza         ; antes de WSYNC lo mínimo: la última línea de una fila ANTIC 4
        stx dzx         ; ancha deja a la CPU a media velocidad (si llega tarde, la fila
        ldx dlin        ; entera arranca una línea con los colores viejos y parpadea)
        stx WSYNC
        lda DTCH,x
        sta CHBASE
        lda DTPF1,x
        sta COLPF1
        lda DTPF2,x
        sta COLPF2
        lda DTPF0,x
        sta COLPF0
        lda DTBK,x
        sta COLBK
        lda DTPF3,x
        sta COLPF3
        lda DTHS,x      ; HSCROL al final: DTHS ya trae el valor de la fila siguiente
        sta HSCROL      ; cuando esta no tiene desplazamiento fino
        inc dlin
        ldx dzx
        lda dza
        rti

; display list del juego
DLTPL:  .byte $70,$70,$70
        .byte $C2, <HUD, >HUD
        .repeat 4, I
        .byte $C4, <(SKYSCR+I*40), >(SKYSCR+I*40)
        .endrepeat
DL_M0 = * - DLTPL
        .repeat 3, I
        .byte $D4, <(MRING+I*128), >(MRING+I*128)
        .endrepeat
        .byte $C4, <BLANK40, >BLANK40
DL_G0 = * - DLTPL
        .repeat 13, I
        .byte $D4, <(GRING+I*128), >(GRING+I*128)
        .endrepeat
        .byte $41, <DLGAME, >DLGAME
DLLEN = * - DLTPL

GDLOFF: .repeat 13, I
        .byte DL_G0 + 1 + I*3
        .endrepeat
GRLO:   .repeat 13, I
        .byte <(GRING+I*128)
        .endrepeat
MDLOFF: .repeat 3, I
        .byte DL_M0 + 1 + I*3
        .endrepeat
MRLO:   .repeat 3, I
        .byte <(MRING+I*128)
        .endrepeat

; ---------------------------------------------------------------
; EFECTOS: 0 lanzar · 1 golpe · 2 caída del enemigo · 3 salto · 4 zombi · 5 cuervo
;          6 Radu golpeado · 7 muerte · 8 baltag contra piedra · 9 muerte (ruido)
;          10 vida extra · 11 campana
; ---------------------------------------------------------------
; 12 bruja · 13 convertido en pollo · 14 vuelve a ser Radu · 15 hechizo · 16 golpe seco de la calavera
SX_CH:  .byte 3, 2, 2, 3, 3, 3, 2, 2, 3, 2, 3, 3, 3, 2, 2, 3, 2, 3, 2, 3
SX_F:   .byte $18, $30, $50, $60, $E0, $28, $40, $30, $0A, $60, $30, $2D, $60, $20, $80, $40, $C0, $50, $30, $20
SX_S:   .byte $FE, $02, $03, $FC, $00, $03, $06, $03, $00, $01, $FE, $00, $FD, $03, $FC, $FE, $00, $FE, $00, $04
SX_V:   .byte 8,   14,  12,  6,   8,   9,   14,  15,  10,  15,  10,  12,  10,  14,  12,  10,  10,  12,  8,   10
SX_D:   .byte 8,   20,  24,  10,  30,  12,  24,  100, 6,   60,  40,  60,  40,  60,  30,  24,  8,   50,  150, 30
SX_C:   .byte $80, $80, $20, $A0, $80, $C0, $A0, $A0, $A0, $80, $A0, $A0, $A0, $A0, $A0, $C0, $80, $A0, $80, $A0
SX_P:   .byte 1,   2,   2,   1,   1,   1,   3,   4,   1,   4,   3,   3,   4,   4,   3,   3,   2,   4,   3,   3
SX_K:   .byte 0,   1,   1,   1,   3,   1,   1,   7,   0,   3,   3,   3,   1,   3,   1,   1,   0,   3,   15,  1
