; ===============================================================
; VÓRTICE 6 · INTRO (CINE=1) y FINAL (CINE=2)
;   frases en grande con fundido · imagen ANTIC E (160x192, 4 colores por franja de 4 líneas, DLI)
;   final: créditos que suben (modo 2, desplazamiento fino) y puntuación final
;   en el disco: al acabar carga el programa siguiente con el cargador residente ($0600)
; ===============================================================
        .include "hw.inc"
PERS    = $0580
P_MAGIC = PERS
P_DIF   = PERS+1
P_CHAIN = PERS+2
P_SCORE = PERS+3
P_DISK  = PERS+13           ; 1 = arrancado desde el disco (hay cargador en $0600)
LOADER  = $0710

        .segment "ZEROPAGE"
frame:  .res 1
trig:   .res 1
tmp:    .res 8
mbar:   .res 2
mpp:    .res 2
mins:   .res 2
src:    .res 2
dband:  .res 1
t1:     .res 1
t2:     .res 1
d1:     .res 1              ; temporales solo de la DLI
d2:     .res 1
level:  .res 1              ; brillo máximo (fundido de la imagen)
lvlw:   .res 1              ; brillo pedido
pon:    .res 1              ; 1 = imagen en pantalla (la VBI pone la franja 0)
fcol:   .res 1              ; color de las frases
scrl:   .res 1              ; créditos: desplazamiento fino
ctop:   .res 1              ; créditos: primera línea
wait:   .res 2
mt:     .res 1
mt1:    .res 1
mt2:    .res 1
mt3:    .res 1
tl:     .res 1              ; «TILÍN» (0 = callado)

        .segment "HIBSS"
mplay:  .res 1
msong:  .res 1
mrow:   .res 1
mbarn:  .res 1
malt:   .res 1
mtick:  .res 1
MCI:    .res 4
MCN:    .res 4
MCE:    .res 4
MCA:    .res 4
MCF:    .res 4
CURBK:  .res 64
CUR0:   .res 64
CUR1:   .res 64
CUR2:   .res 64
TXT:    .res 64             ; las dos líneas de la frase (modo 7)
DLC:    .res 128            ; lista de los créditos (se reescribe)
SCORL:  .res 64

        .segment "INITSEG"
init:   lda PORTB
        ora #$02
        sta PORTB
        rts

        .segment "PICA"
        .incbin "build/cine/pic.bin", 0, 4080
        .segment "PICB"
        .incbin "build/cine/pic.bin", 4080

        .segment "CODE"
        .include "cinedata.s"

; lista de la imagen: 24 en blanco, 192 líneas modo E; DLI en la línea 2 de cada franja de 4: espera el final
; de esa línea, prepara los colores durante la 3 y los cambia justo al empezar la siguiente franja
DLPIC:  .byte $70,$70,$70
        .byte $4E, <$5010, >$5010
        .repeat 101, I
        .if (I+1) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $CE, <$6000, >$6000         ; línea 102 (no cruza 4 KB), con DLI
        .repeat 89, I
        .if (I+103) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $41, <DLPIC, >DLPIC
; lista de las frases: dos líneas grandes centradas en vertical
DLTXT:  .byte $70,$70,$70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte $47, <TXT, >TXT
        .byte $70
        .byte $47, <(TXT+20), >(TXT+20)
        .byte $41, <DLTXT, >DLTXT

; ---------------------------------------------------------------
start:  cld
        sei
        lda #0
        sta NMIEN
        cli
        lda PORTB
        ora #$02
        sta PORTB
        lda #0
        sta SDMCTL
        sta pon
        sta mplay
        lda #3
        sta SKCTL
        lda #0
        sta AUDCTL
        lda #<dli
        sta VDSLST
        lda #>dli
        sta VDSLST+1
        lda #7
        ldy #<vbi
        ldx #>vbi
        jsr SETVBV
        lda #$40
        sta NMIEN
        lda #>FONT
        sta CHBAS
        lda #0
        sta COLOR4
        sta COLOR2
        lda #1
        sta trig
.if CINE = 1
        lda #0              ; la música de la intro empieza con las frases (su parte oscura)
        jsr musstart
.endif
        ; ---- frases
        ldx #0
@fr:    stx tmp+7
        jsr frase
        bcs @pic            ; FIRE: directo a la imagen
        ldx tmp+7
        inx
        cpx #NFRASES
        bne @fr
@pic:   jsr cleartxt
.if CINE = 2
        lda #0              ; el final: la música entra con la imagen de Elara Voss
        jsr musstart
.endif
        jsr showpic
.if CINE = 2
        lda #<420           ; Elara, en calma: 7 s o FIRE
        ldx #>420
        jsr hold
        jsr glint           ; le brilla el ojo: «TILÍN»
        lda #<150
        ldx #>150
        jsr hold
        jsr picfadeout
        lda #<90            ; negro un momento
        ldx #>90
        jsr hold
        jsr credits
.else
        lda #<900           ; 15 s o FIRE
        ldx #>900
        jsr hold
        jsr picfadeout
.endif
        ; ---- fin del programa
        lda P_DISK
        beq @again
        jsr sndoff
        lda #0              ; la partida ha terminado: el título, no la fase
        sta P_CHAIN
        lda #1              ; disco: al título (fase 1)
        jmp LOADER
@again: jmp start

; ---------------------------------------------------------------
; frase X: fundido de entrada, espera, fundido de salida. C=1 si se pulsa FIRE
frase:  txa
        asl a
        tay
        lda FRASES,y
        sta src
        lda FRASES+1,y
        sta src+1
        ldy #39
@c:     lda (src),y
        sta TXT,y
        dey
        bpl @c
        lda #<DLTXT
        sta SDLSTL
        lda #>DLTXT
        sta SDLSTL+1
        lda #$22            ; ANTIC: campo normal, sin jugadores
        sta SDMCTL
        lda #0
        sta fcol
@in:    jsr waitfr
        jsr fireedge
        bcs @x
        lda frame
        and #3
        bne @in
        lda fcol
        clc
        adc #1
        sta fcol
        jsr fcolor
        lda fcol
        cmp #14
        bcc @in
        lda #<200
        ldx #>200
        jsr hold
        bcs @x
@out:   jsr waitfr
        lda frame
        and #3
        bne @out
        dec fcol
        jsr fcolor
        lda fcol
        bne @out
        clc
        rts
@x:     sec
        rts
fcolor: lda fcol            ; rojo-naranja que se enciende (tono 3), blanco al máximo
        cmp #13
        bcc @f
        lda #$0E
        sta COLOR0
        rts
@f:     ora #$30
        sta COLOR0
        rts
cleartxt:
        lda #0
        sta COLOR0
        sta SDMCTL
        rts

; ---------------------------------------------------------------
; imagen: fundido de entrada desde negro
showpic:
        lda #0
        sta level
        sta lvlw
        jsr fadecalc
        lda #<DLPIC
        sta SDLSTL
        lda #>DLPIC
        sta SDLSTL+1
        lda #$C0            ; DLI + VBI
        sta NMIEN
        lda #1
        sta pon
        lda #$22
        sta SDMCTL
@f:     jsr waitfr
        jsr waitfr
        jsr waitfr
        jsr waitfr
        inc level
        jsr fadecalc
        lda level
        cmp #15
        bcc @f
        rts
picfadeout:
@f:     jsr waitfr
        jsr waitfr
        jsr waitfr
        jsr waitfr
        dec level
        jsr fadecalc
        lda level
        bne @f
        lda #0
        sta pon
        sta SDMCTL
        lda #$40
        sta NMIEN
        rts
; colores de cada franja con el brillo limitado a «level» (negro por debajo de 2)
fadecalc:
        ldx #NBANDS-1
@l:     lda PALBK,x
        jsr dim
        sta CURBK,x
        lda PAL0,x
        jsr dim
        sta CUR0,x
        lda PAL1,x
        jsr dim
        sta CUR1,x
        lda PAL2,x
        jsr dim
        sta CUR2,x
        dex
        bpl @l
        rts
dim:    sta t1
        and #15
        cmp level
        bcc @ok
        lda level
@ok:    cmp #2
        bcc @blk
        sta t2
        lda t1
        and #$F0
        ora t2
        rts
@blk:   lda #0
        rts

; espera A/X cuadros; C=1 si FIRE
hold:   sta wait
        stx wait+1
@w:     jsr waitfr
        jsr fireedge
        bcs @r
        lda wait
        bne @d
        lda wait+1
        beq @end
        dec wait+1
@d:     dec wait
        jmp @w
@end:   clc
@r:     rts

waitfr: lda frame
@w:     cmp frame
        beq @w
        rts
fireedge:
        lda STRIG0
        bne @up
        lda trig
        bne @no
        lda #1
        sta trig
        sec
        rts
@up:    lda #0
        sta trig
@no:    clc
        rts
sndoff: lda #0
        sta mplay
        ldx #7
@c:     sta AUDF1,x
        dex
        bpl @c
        rts

; ---------------------------------------------------------------
vbi:    cld
        lda #0
        sta ATRACT
        inc frame
        lda pon
        beq @m
        lda #0
        sta dband
        lda CURBK
        sta COLBK
        lda CUR0
        sta COLPF0
        lda CUR1
        sta COLPF1
        lda CUR2
        sta COLPF2
@m:     jsr mus
.if CINE = 2
        jsr tilin
.endif
        jmp XITVBV

dli:    sta WSYNC           ; fin de la línea 2 de la franja (el resto se hace durante la 3)
        pha
        txa
        pha
        tya
        pha
        inc dband
        ldx dband
        lda CUR1,x
        sta d1
        lda CURBK,x
        sta d2
        ldy CUR2,x
        lda CUR0,x
        ldx d1
        sta WSYNC
        sta COLPF0
        stx COLPF1
        sty COLPF2
        lda d2
        sta COLBK
        pla
        tay
        pla
        tax
        pla
        rti

.if CINE = 2
; ---------------------------------------------------------------
; DESTELLO en el ojo de Elara (jugador 0 en blanco, resolución de una línea) y «TILÍN»
GLX     = 48+68-7           ; HPOS: el centro del destello en la columna 68 (doble ancho)
GLY     = 32+84             ; línea de pantalla: fila 84 de la imagen (empieza en la 32)
PMB     = $7800             ; jugadores de una línea: P0 en PMB+$400
glint:  lda #0
        tax
@c:     sta PMB+$400,x
        inx
        bne @c
        lda #>PMB
        sta PMBASE
        lda #1
        sta SIZEP0          ; doble ancho
        lda #1              ; jugadores por delante de la imagen
        sta GPRIOR
        lda #GLX
        sta HPOSP0
        lda #$0E
        sta PCOLR0
        lda #2
        sta GRACTL
        lda #$3A            ; campo normal + jugadores, una línea
        sta SDMCTL
        lda #1
        sta tl              ; suena
        ldx #0
@st:    stx tmp+6
        lda GLSEQ,x
        bmi @done
        jsr glshape
        lda #3
        sta tmp+7
@w:     jsr waitfr
        lda frame           ; titila: blanco / gris claro
        and #2
        ora #$0C
        sta PCOLR0
        dec tmp+7
        bne @w
        ldx tmp+6
        inx
        bne @st
@done:  lda #0
        sta GRACTL
        sta HPOSP0
        lda #$22
        sta SDMCTL
        rts
; dibuja la forma A (0 nada · 1 punto · 2 pequeña · 3 media · 4 grande), 13 líneas centradas en GLY
glshape:
        asl a
        tay
        lda GLSH,y
        sta src
        lda GLSH+1,y
        sta src+1
        ldy #12
@l:     lda (src),y
        sta PMB+$400+GLY-6,y
        dey
        bpl @l
        rts
GLSEQ:  .byte 1,2,3,4,4,3,4,4,4,3,4,3,2,3,2,1,1,0,$FF
GLSH:   .word GL0, GL1, GL2, GL3, GL4
GL0:    .byte 0,0,0,0,0,0,0,0,0,0,0,0,0
GL1:    .byte 0,0,0,0,0,0,$10,0,0,0,0,0,0
GL2:    .byte 0,0,0,0,0,$10,$38,$10,0,0,0,0,0
GL3:    .byte 0,0,0,$10,$10,$38,$FE,$38,$10,$10,0,0,0
GL4:    .byte $10,$10,$10,$10,$54,$38,$FE,$38,$54,$10,$10,$10,$10
; «TILÍN»: canal 4, tono puro. «TI» corto y «LÍN» más agudo que se apaga (en la VBI, tras la música)
tilin:  lda tl
        beq @r
        inc tl
        cmp #7
        bcs @lin
        lda #$14            ; ~1,5 kHz
        sta AUDF4
        lda #$AB
        sta AUDC4
@r:     rts
@lin:   sec
        sbc #7
        lsr a
        lsr a               ; /4
        eor #$FF
        clc
        adc #16             ; 15 - (t/4)
        bmi @off
        beq @off
        ora #$A0
        sta AUDC4
        lda frame           ; un leve temblor de campana
        and #1
        clc
        adc #$0E            ; ~2,1 kHz
        sta AUDF4
        rts
@off:   lda #0
        sta tl
        sta AUDC4
        rts

; ---------------------------------------------------------------
; CRÉDITOS: 24 líneas de modo 2 que suben con desplazamiento fino; al final, la puntuación
credits:
        lda #0
        sta ctop
        sta scrl
        jsr dlcred
        lda #<DLC
        sta SDLSTL
        lda #>DLC
        sta SDLSTL+1
        lda #$0E
        sta COLOR1
        lda #0
        sta COLOR2
        sta COLOR4
        lda #$22
        sta SDMCTL
@l:     jsr waitfr
        jsr waitfr
        jsr waitfr
        jsr waitfr
        inc scrl
        lda scrl
        cmp #8
        bcc @v
        lda #0
        sta scrl
        inc ctop
        lda ctop
        cmp #NCRED-24
        bcs @end
        jsr dlcred
@v:     lda scrl
        sta VSCROL
        jmp @l
        lda #<300           ; la última línea, quieta 5 s
        ldx #>300
        jsr hold
@end:   ; pantalla final: puntuación
        lda #0
        sta VSCROL
        jsr scoreline
        lda #<DLSC
        sta SDLSTL
        lda #>DLSC
        sta SDLSTL+1
        lda #<1200
        ldx #>1200
        jmp hold
; reconstruye la lista: 24 líneas desde ctop (con desplazamiento vertical salvo la última)
dlcred: ldx #0
        lda #$70
        sta DLC,x
        inx
        sta DLC,x
        inx
        lda ctop
        sta tmp
        lda #0
        sta tmp+1
        ; tmp*40
        lda tmp
        asl a
        rol tmp+1
        asl a
        rol tmp+1
        asl a
        rol tmp+1           ; *8
        sta tmp+2
        lda tmp+1
        sta tmp+3
        asl tmp+2
        rol tmp+3
        asl tmp+2
        rol tmp+3           ; *32
        lda tmp+2
        clc
        adc tmp             ; +*8 (tmp aún = ctop*8? no) — se recalcula abajo
        ldy #0
        lda ctop
        sta tmp+4
        lda #<CRED
        sta src
        lda #>CRED
        sta src+1
@m:     lda tmp+4           ; src = CRED + ctop*40
        beq @go
        lda src
        clc
        adc #40
        sta src
        bcc @mm
        inc src+1
@mm:    dec tmp+4
        jmp @m
@go:    ldy #24
@ln:    cpy #1
        beq @last
        lda #$62            ; modo 2 + LMS + desplazamiento vertical
        bne @st
@last:  lda #$42
@st:    sta DLC,x
        inx
        lda src
        sta DLC,x
        inx
        lda src+1
        sta DLC,x
        inx
        lda src
        clc
        adc #40
        sta src
        bcc @nn
        inc src+1
@nn:    dey
        bne @ln
        lda #$41
        sta DLC,x
        inx
        lda #<DLC
        sta DLC,x
        inx
        lda #>DLC
        sta DLC,x
        rts
; línea con la puntuación final (BCD de 3 bytes en P_SCORE)
scoreline:
        ldx #39
        lda #CH_SPACE
@c:     sta SCORL,x
        dex
        bpl @c
        lda P_MAGIC
        cmp #$56
        bne @r
        ldx #2
        ldy #17
@d:     lda P_SCORE,x
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIG0
        sta SCORL,y
        iny
        lda P_SCORE,x
        and #15
        clc
        adc #DIG0
        sta SCORL,y
        iny
        dex
        bpl @d
@r:     rts
DLSC:   .byte $70,$70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte $42, <TXSCORE, >TXSCORE
        .byte $70
        .byte $42, <SCORL, >SCORL
        .byte $70,$70,$70
        .byte $42, <TXFIRE, >TXFIRE
        .byte $41, <DLSC, >DLSC
.endif

        .include "music.s"
