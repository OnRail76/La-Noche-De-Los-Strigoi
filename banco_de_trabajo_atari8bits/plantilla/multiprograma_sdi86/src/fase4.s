; ---------------------------------------------------------------
; SDI '86 · PROTOCOLO FINAL · Atari 8 bits (NTSC) · 2026 - Tony C. Ware
; PROGRAMA 4 · OPERACIÓN AGENTE ENCUBIERTO (al estilo de Arena 3000)
;
; Pantalla: marcador + 22 filas ANTIC 4 (la arena: paredes, puertas, cajas, 4 drones) + marcador.
; Los enemigos son caracteres que se mueven de casilla en casilla (como en Arena 3000): caben muchos.
; El agente: P0 (uniforme) + P1 (piel). P2 la mira. M0-M1 sus disparos · M2-M3 las balas enemigas.
; Control: la palanca mueve al agente en 8 direcciones; FIRE dispara hacia donde camina
; (quieto, hacia donde caminó por última vez).
; ---------------------------------------------------------------
        .include "hw.inc"
        .include "blk.inc"
FASE    = 4
MUSICA  = 1
MUS_TITULO   = 0
MUS_SUPERADA = 1
MUS_GAMEOVER = 2

PMA     = $A000
PMB     = $A800
PMY0    = 32
PMN     = 192
SCR     = $B000
DLGAME  = $B400
DLTEXT  = $B480
HUDT    = $B500
HUDB    = $B528
TSCR    = $B580
CHSET2  = $B800              ; el juego de caracteres de la arena: el mismo, con el carácter 0 = chapa del suelo
EXTRA_STEP = $06

NEN     = 10                ; enemigos a la vez (tope)
AXMIN   = 48+8              ; límites del agente (HPOS / línea PMG)
AXMAX   = 48+144
AYMIN   = 48
AYMAX   = 192

FX_SHOT   = 0
FX_EXPL   = 1
FX_HIT    = 2
FX_BURST  = 3
FX_DEATH  = 4
FX_ALERT  = 5
FX_BIG    = 6
FX_BEEP   = 7
FX_EBUL   = 8
FX_EXTRA  = 9
FX_THUMP  = 10
FX_DEATH2 = 11
FX_STEP   = 12
FX_KLAX1  = 13
FX_KLAX2  = 14

; ---------------------------------------------------------------
        .segment "ZEROPAGE"
ax:     .res 1              ; agente: HPOS
ay:     .res 1              ; línea PMG de arriba
adir:   .res 1              ; hacia dónde apunta (0 arriba, 1 arriba-der., ... 7 arriba-izq.)
aface:  .res 1              ; 0 derecha · 1 izquierda
afr:    .res 1
pst:    .res 1
ptm:    .res 1
invt:   .res 1
ftm:    .res 1
wave:   .res 1
wcount: .res 1              ; enemigos de la oleada que quedan (en pantalla y por salir)
cur:    .res 1
scur:   .res 1              ; disparo en curso (ene_hit usa cur para el enemigo)
scp:    .res 2              ; puntero a una celda de SCR
edx:    .res 1              ; paso de un enemigo: distancia al agente (con signo)
edy:    .res 1
save4:  .res 1

        .segment "HIBSS"
DTCH:   .res 23             ; juego de caracteres por fila (DLI)
ETY:    .res NEN            ; tipo ($FF libre): 0 soldado · 1 tirador · 2 blindado
ECO:    .res NEN            ; columna, fila (casilla de arriba a la izquierda)
ERO:    .res NEN
EHP:    .res NEN
ETM:    .res NEN
EST:    .res NEN            ; tirador: 0 anda · 1 dispara
ESH:    .res NEN
EFR:    .res NEN
EFC:    .res NEN            ; hacia dónde mira (0 derecha, 1 izquierda)
XR:     .res 4              ; explosiones: fila, columna, anchura, alto, tiempo ($FF libre)
XC:     .res 4
XW:     .res 4
XH:     .res 4
XT:     .res 4
SXP:    .res 2              ; disparos del agente (M0, M1): x, y, dirección (y = 0: libre)
SYP:    .res 2
SDP:    .res 2
BXP:    .res 2              ; balas enemigas (M2, M3)
BYP:    .res 2
BDP:    .res 2
BSB:    .res 2
DHP:    .res 4              ; drones
dal:    .res 1              ; dron en alerta ($FF ninguno)
dat:    .res 1
dtm:    .res 1
q_s:    .res 1              ; por salir: soldados, tiradores, blindados
q_t:    .res 1
q_b:    .res 1
sptm:   .res 1
non:    .res 1              ; enemigos en pantalla
p_sm:   .res 1
p_max:  .res 1
p_dr:   .res 1
p_tf:   .res 1

        .segment "CODE"
        .include "data4.s"
        .include "motor/nucleo.s"
        .include "motor/pmg.s"
        .include "motor/dli.s"
        .include "motor/sonido.s"
        .include "motor/marcador.s"
        .include "motor/pantalla.s"
        .include "motor/musica.s"
        .include "comun.s"

; ===============================================================
f_vbi:  lda #0
        sta dlin
        rts

f_screen:
        jsr scr_off
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
        jsr pm_init
        ldx #22
@t:     lda TABBK,x
        sta DTBK,x
        lda TABP0,x
        sta DTPF0,x
        lda TABP1,x
        sta DTPF1,x
        lda TABP2,x
        sta DTPF2,x
        lda #0
        sta DTHS,x
        dex
        bpl @t
        lda #>CHSET2        ; la arena con el suelo de chapa; el marcador de abajo, con el de siempre
        ldx #21
@c:     sta DTCH,x
        dex
        bpl @c
        lda #>CHARSET
        sta DTCH+22
        lda #<CHARSET       ; copia del juego de caracteres
        sta src
        lda #>CHARSET
        sta src+1
        lda #<CHSET2
        sta dst
        lda #>CHSET2
        sta dst+1
        ldx #4
@p:     ldy #0
@pb:    lda (src),y
        sta (dst),y
        iny
        bne @pb
        inc src+1
        inc dst+1
        dex
        bne @p
        ldx #7
@g:     lda SUELO_G,x
        sta CHSET2,x
        dex
        bpl @g
        jsr scr_on
        lda #$40            ; la DLI propia de la arena
        sta NMIEN
        lda #<dli4
        sta VDSLST
        lda #>dli4
        sta VDSLST+1
        lda #$C0
        sta NMIEN
        lda #$0E            ; disparos del agente: blancos
        sta COLOR3
        rts

; DLI de la arena: como la del motor, y además el juego de caracteres de la fila siguiente.
; CHBASE se cambia antes del WSYNC: la última línea del suelo y la de un espacio son iguales (vacías).
dli4:   pha
        lda gmode
        bne @g
        pla
        jmp m_dli
@g:     txa
        pha
        ldx dlin
        lda DTCH,x
        sta CHBASE
        lda DTBK,x
        sta WSYNC
        sta COLBK
        lda DTPF0,x
        sta COLPF0
        lda DTPF1,x
        sta COLPF1
        lda DTPF2,x
        sta COLPF2
        inc dlin
        pla
        tax
        pla
        rti

; la base de computadoras: suelo de chapa oscuro; PF0 metal oscuro, PF1 metal claro (brillo), PF2 leds rojos (laten)
;            0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22
TABBK:  .byte $00,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$00,$00
TABP0:  .byte $06,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$06
        .byte $00
TABP1:  .byte $0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A,$0A
        .byte $0C
TABP2:  .byte $46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46,$46
        .byte $00

DLTPL:  .byte $70,$70,$70
        .byte $C2
        .word HUDT
        .repeat 22, I
        .byte $C4
        .word SCR+I*40
        .endrepeat
        .byte $42
        .word HUDB
        .byte $41
        .word DLGAME
DLLEN = * - DLTPL

ROWL:
        .repeat 22, I
        .byte <(SCR+I*40)
        .endrepeat
ROWH:
        .repeat 22, I
        .byte >(SCR+I*40)
        .endrepeat

; ---------------------------------------------------------------
f_start:
        lda #<SCR_INIT
        sta src
        lda #>SCR_INIT
        sta src+1
        lda #<SCR
        sta dst
        lda #>SCR
        sta dst+1
        ldx #4
        jsr cp220
        ldx #NEN-1
        lda #$FF
@e:     sta ETY,x
        dex
        bpl @e
        ldx #3
@x:     sta XR,x
        dex
        bpl @x
        sta dal
        ldx #3
        lda #3
@d:     sta DHP,x
        dex
        bpl @d
        lda #0
        sta non
.ifdef OLEADA0                      ; solo para pruebas: empezar en otra oleada
        lda #OLEADA0
.endif
        sta wave
        jsr params
        jsr wave_start
        jmp ag_reset

params: lda loopn
        cmp #5
        bcc @l
        lda #5
@l:     sta tmp
        asl a
        sta tmp+1           ; x2
        lda #18             ; pasos de los soldados: cada 18 - 2 x vuelta cuadros
        sec
        sbc tmp+1
        ldx dif
        clc
        adc DIF_SM,x
        cmp #5
        bcs @s
        lda #5
@s:     sta p_sm
        lda tmp             ; a la vez: 5 + vuelta (tope 9)
        clc
        adc #5
        ldx dif
        bne @m
        sec
        sbc #1
@m:     cmp #NEN
        bcc @m2
        lda #NEN-1
@m2:    sta p_max
        lda tmp             ; drones: cada 240 - 30 x vuelta (mínimo 100)
        asl a
        asl a
        asl a
        asl a
        sta tmp+1
        asl a
        sec
        sbc tmp+1           ; x16
        sta tmp+1
        lda tmp
        asl a
        clc
        adc tmp+1
        adc tmp+1           ; ~ x34
        sta tmp+1
        lda #240
        sec
        sbc tmp+1
        cmp #100
        bcs @d
        lda #100
@d:     sta p_dr
        sta dtm
        lda #56             ; disparo de los tiradores
        sec
        sbc tmp+1
        bcs @t
        lda #0
@t:     cmp #30
        bcs @t2
        lda #30
@t2:    sta p_tf
        rts
DIF_SM: .byte 4, 0, 254

; oleada: cuántos de cada tipo
wave_start:
        lda loopn
        cmp #4
        bcc @l
        lda #4
@l:     sta tmp
        lda #6              ; soldados: 6 + 2 x oleada + vuelta
        ldx wave
        beq @w
@w1:    clc
        adc #2
        dex
        bne @w1
@w:     clc
        adc tmp
        sta q_s
        lda #0              ; tiradores: desde la oleada 2 (2 + vuelta)
        ldx wave
        beq @t
        lda #2
        clc
        adc tmp
@t:     sta q_t
        lda #0              ; blindados: en la oleada 3 (1, 2 desde la vuelta 2)
        ldx wave
        cpx #2
        bne @b
        lda #1
        ldx loopn
        beq @b
        lda #2
@b:     sta q_b
        lda q_s
        clc
        adc q_t
        adc q_b
        adc non
        sta wcount
        lda #30
        sta sptm
        lda #64
        sta klax
        lda #1
        sta hudd
        rts

; ---------------------------------------------------------------
f_frame:
        jsr glow
        jsr ag_update
        jsr shots_update
        jsr spawn
        jsr ene_update
        jsr xpl_update
        jsr drones
        jsr ebul_update
        jsr ag_touch
        ; oleadas
        lda pclear
        bne @r
        lda wcount
        bne @r
        inc wave
        lda wave
        cmp #3
        bne @n
        jmp phase_done
@n:     jsr wave_start
        lda wave
        clc
        adc #M_OLA2-1
        jmp msg
@r:     rts

; leds que laten y un brillo que recorre la base de arriba abajo
glow:   lda frame
        lsr a
        lsr a
        and #7
        tax
        lda LEDP,x
        ldx #21
@l:     sta DTPF2,x
        dex
        bpl @l
        lda frame
        and #63
        lsr a
        cmp #22
        bcs @r0
        tay
        lda #$0A
        ldx #21
@m:     sta DTPF1,x
        dex
        bpl @m
        lda #$0E
        sta DTPF1,y
        rts
@r0:    lda #$0A
        ldx #21
@n:     sta DTPF1,x
        dex
        bpl @n
        rts
LEDP:   .byte $42,$44,$46,$48,$4A,$48,$46,$44

f_status:
        lda wave
        cmp #3
        bcc @w
        lda #2
@w:     clc
        adc #DIG0+1
        sta HUDB+HUD_OL
        lda wcount
        ldx #HUD_EN
        jmp st_dec2

; ---------------------------------------------------------------
; celdas: scp = celda (fila Y, columna A)
cell:   clc
        adc ROWL,y
        sta scp
        lda ROWH,y
        adc #0
        sta scp+1
        rts

; carácter bajo el punto (x = A HPOS, y = X línea PMG) -> A; conserva X e Y
char_at:
        sty tmp+6
        sec
        sbc #48
        lsr a
        lsr a
        sta tmp+5
        txa
        sec
        sbc #40
        lsr a
        lsr a
        lsr a
        cmp #22
        bcs @no
        tay
        lda tmp+5
        cmp #40
        bcs @no
        jsr cell
        ldy #0
        lda (scp),y
        ldy tmp+6
        rts
@no:    lda #64             ; fuera: sólido
        ldy tmp+6
        rts

; ¿es sólido el carácter A? C = 1 si lo es (paredes, cajas, drones y enemigos para el agente no)
solid:  cmp #64
        bcc @n
        cmp #SOLID_END
        bcs @n
        sec
        rts
@n:     clc
        rts

; ---------------------------------------------------------------
; EL AGENTE
ag_reset:
        ; los enemigos en pantalla vuelven a las puertas
        ldx #NEN-1
@e:     ldy ETY,x
        bmi @en
        jsr ene_erase
        ldy ETY,x
        lda #$FF
        sta ETY,x
        cpy #1
        beq @qt
        bcs @qb
        inc q_s
        bne @en
@qt:    inc q_t
        bne @en
@qb:    inc q_b
@en:    dex
        bpl @e
        lda #0
        sta non
        lda #90
        sta sptm
        lda #124
        sta ax
        lda #144
        sta ay
        lda #0
        sta pst
        sta adir
        sta aface
        sta SYP
        sta SYP+1
        sta BYP
        sta BYP+1
        lda #180
        sta invt
        rts

; JDIR: palanca (bits arriba 1, abajo 2, izq. 4, der. 8) -> dirección ($FF ninguna)
JDIR:   .byte $FF,0,4,$FF,6,7,5,$FF,2,1,3,$FF,$FF,$FF,$FF,$FF
DXT:    .byte 0,3,4,3,0,<-3,<-4,<-3       ; disparo del agente: rápido, para que no se quede pegado al andar
DYT:    .byte <-6,<-4,0,4,6,4,0,<-4
EDXT:   .byte 0,1,1,1,0,$FF,$FF,$FF
EDYT:   .byte $FE,$FF,0,1,2,1,0,$FF

ag_update:
        lda pst
        beq @alive
        inc ptm
        lda ptm
        cmp #100
        bne @r
        jsr p_after
        bcc @r
        jmp ag_reset
@r:     rts
@alive: lda invt
        beq @i
        dec invt
@i:     ldx stk
        lda JDIR,x
        bmi @nd
        sta adir
        cmp #1              ; derecha / izquierda para el dibujo
        bcc @nd
        cmp #4
        bcs @lf
        lda #0
        sta aface
        beq @nd
@lf:    cmp #5
        bcc @nd
        lda #1
        sta aface
@nd:    lda fire           ; FIRE: dispara hacia donde camina (o hacia donde caminó por última vez)
        beq @nf
        dec ftm
        bpl @mv
        lda #7
        sta ftm
        jsr shot_new
        jmp @mv
@nf:    lda #0
        sta ftm
@mv:    lda stk
        beq @r
        inc afr
        lda stk             ; horizontal
        and #J_LEFT
        beq @nl
        lda ax
        cmp #AXMIN+1
        bcc @nl
        sec
        sbc #1
        jsr ag_try_x
@nl:    lda stk
        and #J_RIGHT
        beq @nr
        lda ax
        cmp #AXMAX
        bcs @nr
        clc
        adc #1
        jsr ag_try_x
@nr:    lda stk
        and #J_UP
        beq @nu
        lda ay
        cmp #AYMIN+1
        bcc @nu
        sec
        sbc #1
        jsr ag_try_y
@nu:    lda stk
        and #J_DOWN
        beq @r3
        lda ay
        cmp #AYMAX
        bcs @r3
        clc
        adc #1
        jmp ag_try_y
@r3:    rts

; mueve a x = A si los pies no pisan nada sólido
ag_try_x:
        sta tmp+2
        lda ay
        sta tmp+3
        jsr feet_free
        bcs @r
        lda tmp+2
        sta ax
@r:     rts
ag_try_y:
        sta tmp+3
        lda ax
        sta tmp+2
        jsr feet_free
        bcs @r
        lda tmp+3
        sta ay
@r:     rts

; ¿pies libres en (tmp+2, tmp+3)? C = 1 si chocan (4 puntos de la mitad de abajo)
feet_free:
        lda tmp+3
        clc
        adc #9
        tax
        lda tmp+2
        clc
        adc #1
        jsr char_at
        jsr solid
        bcs @r
        lda tmp+2
        clc
        adc #6
        jsr char_at
        jsr solid
        bcs @r
        lda tmp+3
        clc
        adc #15
        tax
        lda tmp+2
        clc
        adc #1
        jsr char_at
        jsr solid
        bcs @r
        lda tmp+2
        clc
        adc #6
        jsr char_at
        jsr solid
@r:     rts

; ¿toca el agente a un enemigo? (sus casillas)
ag_touch:
        lda pst
        ora invt
        ora cheat
        bne @r
        ldx #NEN-1
@l:     lda ETY,x
        bmi @n
        jsr ene_box
        lda ax
        clc
        adc #1
        sta tmp+0
        adc #5
        sta tmp+1
        lda ay
        clc
        adc #2
        sta tmp+2
        adc #12
        sta tmp+3
        jsr boxhit
        bcc @n
        jmp ag_die
@n:     dex
        bpl @l
@r:     rts

ag_die: lda cheat
        ora invt
        ora pst
        bne @r
        lda #1
        sta pst
        lda #0
        sta ptm
        sta BYP
        sta BYP+1
        jmp p_die
@r:     rts

; caja del enemigo X en tmp+4..7 (HPOS / líneas)
ene_box:
        lda ECO,x
        asl a
        asl a
        adc #48
        sta tmp+4
        lda ETY,x
        cmp #2
        bne @s
        lda tmp+4
        clc
        adc #15
        bne @w
@s:     lda tmp+4
        clc
        adc #7
@w:     sta tmp+5
        lda ERO,x
        asl a
        asl a
        asl a
        adc #40
        sta tmp+6
        clc
        adc #7
        ldy ETY,x
        cpy #2
        bne @h
        adc #8
@h:     sta tmp+7
        rts

; ---------------------------------------------------------------
; DISPAROS del agente (M0, M1)
shot_new:
        ldx #1
@f:     lda SYP,x
        beq @ok
        dex
        bpl @f
        rts
@ok:    lda ax
        clc
        adc #3
        sta SXP,x
        lda ay
        clc
        adc #6
        sta SYP,x
        lda adir
        sta SDP,x
        lda #FX_SHOT
        jmp sfx

shots_update:
        ldx #1
@l:     lda SYP,x
        bne @a
        jmp @n
@a:     ldy SDP,x
        lda SXP,x
        clc
        adc DXT,y
        sta SXP,x
        lda SYP,x
        clc
        adc DYT,y
        sta SYP,x
        cmp #40
        bcc @off
        cmp #212
        bcs @off
        lda SXP,x
        cmp #48
        bcc @off
        cmp #208
        bcs @off
        ; ¿qué hay?
        stx scur
        lda SYP,x
        tax
        ldy scur
        lda SXP,y
        jsr char_at
        ldx scur
        cmp #0
        beq @n
        cmp #ENE_LO
        bcc @so
        cmp #ENE_HI+1
        bcs @n              ; restos de explosión: sigue
        jsr shot_ene
        ldx scur
        jmp @off
@so:    jsr solid
        bcc @n
        jsr shot_drone      ; ¿un dron?
        ldx scur
@off:   lda #0
        sta SYP,x
@n:     dex
        bmi @x
        jmp @l
@x:     rts

; el disparo X ha dado en la casilla scp (enemigo): busca quién está ahí
shot_ene:
        lda tmp+5           ; columna
        sta tmp+2
        lda SYP,x
        sec
        sbc #40
        lsr a
        lsr a
        lsr a
        sta tmp+3           ; fila
        ldx #NEN-1
@l:     lda ETY,x
        bmi @n
        lda tmp+2
        sec
        sbc ECO,x
        bcc @n
        ldy ETY,x
        cmp ENW,y
        bcs @n
        lda tmp+3
        sec
        sbc ERO,x
        bcc @n
        cmp ENH,y
        bcs @n
        jmp ene_hit
@n:     dex
        bpl @l
        rts
ENW:    .byte 2, 2, 4
ENH:    .byte 1, 1, 2

shot_drone:
        lda tmp+5
        sta tmp+2
        ldx #3
@l:     lda tmp+2
        sec
        sbc DRN_COL,x
        cmp #2
        bcs @n
        lda tmp+3
        cmp DRN_ROW,x
        bne @n
        lda DHP,x
        beq @n
        dec DHP,x
        bne @h
        jsr drone_draw
        lda #FX_EXPL
        jsr sfx
        cpx dal
        bne @p
        lda #$FF
        sta dal
@p:     lda #$00            ; 300
        ldx #$03
        jmp score_add
@h:     lda #FX_HIT
        jmp sfx
@n:     dex
        bpl @l
        rts

; ---------------------------------------------------------------
; ENEMIGOS
spawn:  lda pclear
        bne @r
        dec sptm
        bne @r
        lda #56
        sta sptm
        lda non
        cmp p_max
        bcs @r
        lda q_s
        ora q_t
        ora q_b
        beq @r
        ldx #NEN-1          ; hueco libre
@f:     lda ETY,x
        bmi @ok
        dex
        bpl @f
@r:     rts
@ok:    stx cur
        ; tipo: blindado si queda y toca, tirador, soldado
        lda q_b
        beq @t
        lda RANDOM
        and #3
        bne @t
        dec q_b
        lda #2
        bne @ty
@t:     lda q_t
        beq @s
        lda RANDOM
        and #1
        bne @s
        dec q_t
        lda #1
        bne @ty
@s:     lda q_s
        bne @s1
        lda q_t             ; solo quedan de los otros
        beq @b2
        dec q_t
        lda #1
        bne @ty
@b2:    dec q_b
        lda #2
        bne @ty
@s1:    dec q_s
        lda #0
@ty:    sta ETY,x
        ; puerta al azar
        lda RANDOM
        and #3
        tay
        lda DOOR_C,y
        sta ECO,x
        lda DOOR_R,y
        sta ERO,x
        ; ¿cabe?
        jsr ene_free
        bcc @in
        ldy ETY,x           ; la puerta está ocupada: vuelve a la cola
        lda #$FF
        sta ETY,x
        lda #10
        sta sptm
        cpy #1
        beq @qt
        bcs @qb
        inc q_s
        rts
@qt:    inc q_t
        rts
@qb:    inc q_b
        rts
@in:    ldy ETY,x
        lda EHP_T,y
        sta EHP,x
        lda #0
        sta EST,x
        sta ESH,x
        sta EFR,x
        sta EFC,x
        lda p_sm
        sta ETM,x
        inc non
        jmp ene_draw
DOOR_C: .byte 19, 19, 2, 36
DOOR_R: .byte 1, 19, 10, 10
EHP_T:  .byte 1, 2, 6

; ¿están libres las casillas del enemigo X en su sitio? C = 1 si no
ene_free:
        ldy ETY,x
        lda ENW,y
        sta tmp+2
        lda ENH,y
        sta tmp+3
        ldy ERO,x
        lda ECO,x
        jsr cell
@rw:    ldy #0
@c:     lda (scp),y
        bne @no
        iny
        cpy tmp+2
        bne @c
        dec tmp+3
        beq @yes
        lda scp
        clc
        adc #40
        sta scp
        bcc @rw
        inc scp+1
        bne @rw
@yes:   clc
        rts
@no:    sec
        rts

; dibuja (A = 0: borra) el enemigo X
ene_draw:
        lda #1
        bne ene_put
ene_erase:
        lda #0
ene_put:
        sta tmp+4
        ldy ETY,x
        lda ENW,y
        sta tmp+2
        lda ENH,y
        sta tmp+3
        ; códigos del dibujo
        lda ETY,x
        bne @nt
        lda EFR,x           ; soldado: 2 dibujos
        and #1
        asl a
        clc
        adc #<SOL_F
        sta src
        lda #>SOL_F
        adc #0
        sta src+1
        jmp @go
@nt:    cmp #1
        bne @bl
        lda EFC,x           ; tirador: de pie o rodilla en tierra, a la derecha o a la izquierda
        asl a
        ora EST,x
        asl a
        clc
        adc #<TIR_F
        sta src
        lda #>TIR_F
        adc #0
        sta src+1
        jmp @go
@bl:    lda #<BLI_F
        sta src
        lda #>BLI_F
        sta src+1
@go:    ldy ERO,x
        lda ECO,x
        jsr cell
        lda #0
        sta tmp+5           ; índice en el dibujo
@rw:    ldy #0
@c:     lda tmp+4
        beq @z
        sty tmp+6
        ldy tmp+5
        lda (src),y
        ldy tmp+6
@z:     sta (scp),y
        inc tmp+5
        iny
        cpy tmp+2
        bne @c
        dec tmp+3
        beq @x
        lda scp
        clc
        adc #40
        sta scp
        bcc @rw
        inc scp+1
        bne @rw
@x:     rts

ene_update:
        ldx #NEN-1
@l:     lda ETY,x
        bpl @a
        jmp @n
@a:     ; tirador plantado: dispara
        cmp #1
        bne @mv
        lda EST,x
        beq @mv
        dec ETM,x
        bne @nj
        lda p_tf
        sta ETM,x
        jsr ene_fire
        inc ESH,x
        lda ESH,x
        cmp #2
        bcc @nj
        lda #$88            ; a andar otra vez: 8 pasos antes de volver a plantarse
        sta ESH,x
        jsr ene_erase
        lda #0
        sta EST,x
        jsr ene_draw
@nj:    jmp @n
@mv:    dec ETM,x
        beq @go
        jmp @n
@go:    lda p_sm
        ldy ETY,x
        cpy #2
        bne @tm
        asl a               ; el blindado va a la mitad
        asl a
        pha
        lda RANDOM          ; y dispara de vez en cuando
        and #3
        bne @nb
        jsr ene_fire
@nb:    pla
@tm:    sta ETM,x
        ; ¿tirador alineado con el agente? se planta (si no acaba de disparar)
        lda ETY,x
        cmp #1
        bne @step
        lda ESH,x
        beq @al
        dec ESH,x           ; $88 -> $80: sigue andando
        lda ESH,x
        cmp #$80
        bne @step
        lda #0
        sta ESH,x
        beq @step
@al:    jsr ag_cell
        lda tmp+1           ; misma fila
        cmp ERO,x
        beq @pl
        lda tmp
        sec
        sbc ECO,x
        cmp #2
        bcs @step
@pl:    jsr ene_erase
        lda tmp             ; mira al agente
        cmp ECO,x
        lda #0
        bcs @fc
        lda #1
@fc:    sta EFC,x
        lda #1
        sta EST,x
        lda #20
        sta ETM,x
        jsr ene_draw
        jmp @n
@step:  jsr ene_step
@n:     dex
        bmi @x
        jmp @l
@x:     rts

; casilla del agente: tmp = columna (centro), tmp+1 = fila (centro)
ag_cell:
        lda ax
        clc
        adc #4
        sec
        sbc #48
        lsr a
        lsr a
        sta tmp
        lda ay
        clc
        adc #8
        sec
        sbc #40
        lsr a
        lsr a
        lsr a
        sta tmp+1
        rts

; un paso hacia el agente (el eje con más distancia; a veces el otro)
ene_step:
        jsr ag_cell
        lda tmp
        sec
        sbc ECO,x
        sta edx
        lda tmp+1
        sec
        sbc ERO,x
        sta edy
        lda edx
        bpl @ax
        eor #$FF
        clc
        adc #1
@ax:    sta tmp+6
        lda edy
        bpl @ay
        eor #$FF
        clc
        adc #1
@ay:    sta tmp+7
        lda RANDOM
        and #3
        beq @oth
        lda tmp+6
        cmp tmp+7
        bcs @hor
@ver:   jsr try_v
        bcc @ok
        jsr try_h
        bcc @ok
        jmp @stk
@oth:   lda tmp+6
        cmp tmp+7
        bcs @ver
@hor:   jsr try_h
        bcc @ok
        jsr try_v
        bcc @ok
        ; atascado: un paso de lado al azar
@stk:   lda RANDOM
        ora #1
        sta edx
        sta edy
        and #2
        beq @sv
        jsr try_h
        jmp @ok
@sv:    jsr try_v
@ok:    inc EFR,x
        jmp ene_draw
try_h:  lda edx
        beq @no
        jsr ene_erase
        lda ECO,x
        sta save4
        lda edx
        bmi @l
        lda #0
        sta EFC,x
        inc ECO,x
        jmp @t
@l:     lda #1
        sta EFC,x
        dec ECO,x
@t:     jsr ene_free
        bcc @y
        lda save4
        sta ECO,x
@no:    sec
        rts
@y:     clc
        rts
try_v:  lda edy
        beq @no
        jsr ene_erase
        lda ERO,x
        sta save4
        lda edy
        bmi @u
        inc ERO,x
        jmp @t
@u:     dec ERO,x
@t:     jsr ene_free
        bcc @y
        lda save4
        sta ERO,x
@no:    sec
        rts
@y:     clc
        rts

; el enemigo X dispara hacia el agente
ene_fire:
        lda pst
        bne @r
        ldy #1
@f:     lda BYP,y
        beq @ok
        dey
        bpl @f
@r:     rts
@ok:    lda ECO,x
        asl a
        asl a
        adc #48+3
        sta BXP,y
        lda ERO,x
        asl a
        asl a
        asl a
        adc #40+4
        sta BYP,y
        sty tmp+7
        jsr aim             ; A = dirección
        ldy tmp+7
        sta BDP,y
        lda #FX_EBUL
        jmp sfx

; dirección (0-7) desde (BXP,y / BYP,y de tmp+7) hacia el agente
aim:    ldy tmp+7
        lda ax
        clc
        adc #4
        sec
        sbc BXP,y
        sta tmp+2           ; dx (relojes de color)
        lda ay
        clc
        adc #8
        sec
        sbc BYP,y
        sta tmp+3           ; dy (líneas)
        lda tmp+2
        bpl @a
        eor #$FF
        clc
        adc #1
@a:     sta tmp+4           ; |dx|
        asl a               ; un reloj de color mide ~1,6 líneas: |dx| x 2 frente a |dy|
        sta tmp+5
        lda tmp+3
        bpl @b
        eor #$FF
        clc
        adc #1
@b:     sta tmp+6           ; |dy|
        ; ¿casi vertical, casi horizontal o diagonal?
        lsr a
        cmp tmp+5
        bcs @vert           ; |dy|/2 >= 2|dx| -> vertical
        lda tmp+5
        lsr a
        lsr a
        cmp tmp+6
        bcs @horz           ; 2|dx|/4 >= |dy| -> horizontal
        ; diagonal
        lda tmp+2
        bmi @dl
        lda tmp+3
        bmi @ur
        lda #3
        rts
@ur:    lda #1
        rts
@dl:    lda tmp+3
        bmi @ul
        lda #5
        rts
@ul:    lda #7
        rts
@vert:  lda tmp+3
        bmi @up
        lda #4
        rts
@up:    lda #0
        rts
@horz:  lda tmp+2
        bmi @lf
        lda #2
        rts
@lf:    lda #6
        rts

; el enemigo X recibe un disparo
ene_hit:
        dec EHP,x
        beq @k
        lda #FX_HIT
        jmp sfx
@k:     jsr ene_erase
        ; explosión en sus casillas
        ldy #3
@f:     lda XR,y
        bmi @ok
        dey
        bpl @f
        ldy #0
@ok:    lda ERO,x
        sta XR,y
        lda ECO,x
        sta XC,y
        lda ETY,x
        sta tmp
        stx cur
        tax
        lda ENW,x
        sta XW,y
        lda ENH,x
        sta XH,y
        lda #0
        sta XT,y
        ldx tmp
        lda SC_LO,x
        pha
        lda SC_HI,x
        tax
        pla
        jsr score_add
        ldx cur
        lda #$FF
        sta ETY,x
        dec non
        dec wcount
        lda #1
        sta hudd
        lda #FX_EXPL
        jsr sfx
        lda tmp
        cmp #2
        bne @r
        lda #FX_THUMP
        jmp sfx
@r:     rts
SC_LO:  .byte $00, $50, $00
SC_HI:  .byte $01, $01, $05

; explosiones de enemigos en sus casillas (3 cuadros de 6)
xpl_update:
        ldx #3
@l:     lda XR,x
        bmi @n
        lda XT,x
        inc XT,x
        cmp #18
        bcs @end
        ldy #0
@q:     cmp #6
        bcc @w
        sbc #6
        iny
        bne @q
@w:     cmp #0
        bne @n
        tya
        asl a
        sta tmp+6           ; cuadro x 2
        jsr @put
        jmp @n
@end:   lda #$FF
        sta tmp+6
        jsr @put
        lda #$FF
        sta XR,x
@n:     dex
        bpl @l
        rts
@put:   stx cur
        ldy XR,x
        lda XC,x
        jsr cell
        lda XW,x
        sta tmp+2
        lda XH,x
        sta tmp+3
@rw:    ldy #0
@c:     lda tmp+6
        cmp #$FF
        beq @z
        tya
        and #1
        ora tmp+6
        tax
        lda EXPL_C,x
        ldx cur
        jmp @p
@z:     lda #0
@p:     sta (scp),y
        iny
        cpy tmp+2
        bne @c
        dec tmp+3
        beq @x
        lda scp
        clc
        adc #40
        sta scp
        bcc @rw
        inc scp+1
        bne @rw
@x:     ldx cur
        rts

; ---------------------------------------------------------------
; DRONES: uno avisa parpadeando y dispara al agente
drones: lda dal
        bpl @al
        lda pclear
        ora pst
        bne @r
        dec dtm
        bne @r
        lda p_dr
        sta dtm
        lda RANDOM
        and #3
        tax
        ldy #4
@f:     lda DHP,x
        bne @g
        inx
        txa
        and #3
        tax
        dey
        bne @f
@r:     rts
@g:     stx dal
        lda #40
        sta dat
        lda #FX_ALERT
        jmp sfx
@al:    tax
        dec dat
        bne @b
        jsr drone_draw      ; vuelve a su dibujo y dispara
        lda #$FF
        sta dal
        ldy #1
@bf:    lda BYP,y
        beq @bo
        dey
        bpl @bf
        rts
@bo:    lda DRN_COL,x
        asl a
        asl a
        adc #48+3
        sta BXP,y
        lda DRN_ROW,x
        asl a
        asl a
        asl a
        adc #40+4
        sta BYP,y
        sty tmp+7
        jsr aim
        ldy tmp+7
        sta BDP,y
        lda #FX_EBUL
        jmp sfx
@b:     lda dat             ; parpadeo
        and #4
        beq drone_draw
        ldy DRN_ROW,x
        lda DRN_COL,x
        jsr cell
        ldy #0
        lda DRN_A
        sta (scp),y
        iny
        lda DRN_A+1
        sta (scp),y
        rts

; dibuja el dron X (normal o roto)
drone_draw:
        ldy DRN_ROW,x
        lda DRN_COL,x
        jsr cell
        ldy #0
        lda DHP,x
        beq @r
        lda DRN_N
        sta (scp),y
        iny
        lda DRN_N+1
        sta (scp),y
        rts
@r:     lda DRN_R
        sta (scp),y
        iny
        lda DRN_R+1
        sta (scp),y
        rts

; balas enemigas (M2, M3): avanzan dos subpasos por cuadro
ebul_update:
        ldx #1
@l:     lda BYP,x
        beq @n
        ldy BDP,x
        lda BXP,x
        clc
        adc EDXT,y
        sta BXP,x
        lda BYP,x
        clc
        adc EDYT,y
        sta BYP,x
        cmp #40
        bcc @off
        cmp #212
        bcs @off
        lda BXP,x
        cmp #48
        bcc @off
        cmp #208
        bcs @off
        ; pared
        stx cur
        lda BYP,x
        tax
        ldy cur
        lda BXP,y
        jsr char_at
        ldx cur
        jsr solid
        bcs @off
        ; agente
        lda pst
        ora invt
        bne @n
        lda BXP,x
        sec
        sbc ax
        cmp #8
        bcs @n
        lda BYP,x
        sec
        sbc ay
        cmp #16
        bcs @n
        jsr ag_die
        ldx cur
@off:   lda #0
        sta BYP,x
@n:     dex
        bpl @l
        rts

; ---------------------------------------------------------------
f_render:
        jsr pm_begin
        lda pst
        beq *+5
        jmp @dead
        lda invt
        and #4
        beq *+5
        jmp @sh
        ldx rb
        lda ax
        sta PHP0,x
        sta PHP1,x
        lda #$C6
        sta PCP0,x
        lda #$2A
        sta PCP1,x
        lda afr             ; dibujo: ciclo de 4 pasos (cada 8 cuadros andando) y lado
        lsr a
        lsr a
        lsr a
        and #3
        ldx stk
        bne @st
        lda #0
@st:    ldx aface
        beq @rt
        ora #4
@rt:    tax
        lda WALKF,x
        asl a
        asl a
        asl a
        asl a               ; x 16
        sta tmp
        clc
        adc #<AG_P0
        sta src
        lda #>AG_P0
        adc #0
        sta src+1
        ldx #0
        lda ay
        ldy #16
        jsr pm_spr
        lda tmp
        clc
        adc #<AG_P1
        sta src
        lda #>AG_P1
        adc #0
        sta src+1
        ldx #1
        lda ay
        ldy #16
        jsr pm_spr
        jmp @sh
@dead:  lda ptm
        cmp #36
        bcs @sh
        ldx rb
        lda ax
        sta PHP0,x
        lda #$1C
        sta PCP0,x
        lda ptm
        lsr a
        lsr a
        lsr a
        lsr a
        asl a
        asl a
        asl a
        adc #<BOOM_P
        sta src
        lda #>BOOM_P
        adc #0
        sta src+1
        ldx #0
        lda ay
        clc
        adc #4
        ldy #8
        jsr pm_spr
@sh:    ; disparos del agente (M0-M1): ráfaga alargada en la dirección del disparo
        ldx #1
@s:     lda SYP,x
        beq @sn
        stx cur
        ldy SDP,x
        lda SHW,y           ; anchura del misil (SIZEM) según la dirección
        cpx #0
        beq @w0
        asl a
        asl a
@w0:    ldy rb
        ora PSZM,y
        sta PSZM,y
        txa
        asl a
        ora rb
        tay
        lda SDP,x
        sta tmp+3
        lda SXP,x
        ldx tmp+3
        sec
        sbc SHX,x
        sta PHM0,y
        lda SHH,x
        sta tmp+2
        ldx cur
        lda SYP,x
        ldy tmp+2
        jsr pm_mis
        ldx cur
@sn:    dex
        bpl @s
        ; balas de JANUS (P2-P3): bolas de plasma rojas
        ldx #1
@b:     lda BYP,x
        beq @bn
        stx cur
        txa
        asl a
        ora rb
        tay
        lda BXP,x
        sec
        sbc #2
        sta PHP2,y
        lda frame
        and #6
        ora #$42
        sta PCP2,y
        lda #<PLASMA
        sta src
        lda #>PLASMA
        sta src+1
        lda BYP,x
        sec
        sbc #1
        pha
        txa
        clc
        adc #2
        tax
        pla
        ldy #4
        jsr pm_spr
        ldx cur
@bn:    dex
        bpl @b
        jmp pm_end
; misil del agente por dirección (arriba, arriba-der., der., ...): anchura (SIZEM: 0 normal, 1 doble, 3 cuádruple),
; corrimiento a la izquierda para centrarlo y altura
SHW:    .byte 0, 1, 3, 1, 0, 1, 3, 1
SHX:    .byte 0, 1, 3, 1, 0, 1, 3, 1
SHH:    .byte 6, 3, 2, 3, 6, 3, 2, 3
PLASMA: .byte $60, $F0, $F0, $60




WALKF:  .byte 0,1,0,4, 2,3,2,5   ; parado, paso A, parado, paso B (derecha · izquierda)

; ---------------------------------------------------------------
;        0 disp 1 expl 2 golpe 3 estal 4 muerte 5 alerta 6 enorme 7 beep 8 bala 9 vida 10 golpeG 11 muerte2 12 paso 13 klax1 14 klax2
SX_CH:  .byte 0,   1,   0,   1,   1,   3,   2,   3,   2,   3,   2,   2,   2,   3,   3
SX_F:   .byte $05, $14, $08, $30, $20, $10, $50, $20, $18, $40, $40, $20, $30, $1C, $28
SX_S:   .byte 2,   2,   2,   1,   1,   0,   1,   $FF, 1,   $FD, 3,   2,   0,   0,   0
SX_V:   .byte 11,  15,  14,  15,  15,  10,  15,  10,  7,   12,  15,  15,  4,   12,  12
SX_D:   .byte 8,   44,  10,  80,  130, 40,  150, 30,  8,   24,  26,  72,  3,   8,   8
SX_C:   .byte $80, $80, $A0, $80, $80, $A0, $80, $A0, $A0, $A0, $C0, $C0, $80, $C0, $C0
SX_P:   .byte 2,   3,   3,   4,   5,   3,   5,   4,   1,   4,   3,   5,   1,   3,   3
SX_K:   .byte 0,   3,   0,   7,   7,   0,   7,   7,   1,   7,   1,   3,   0,   0,   0
