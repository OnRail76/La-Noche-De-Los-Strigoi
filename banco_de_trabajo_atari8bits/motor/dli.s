; ===============================================================
; MOTOR · DLI por tablas: una entrada por fila de la display list
; La DLI de la fila i prepara la fila i+1 con la entrada dlin (la VBI pone dlin = 0).
;   DTHS  HSCROL: se escribe ANTES del WSYNC (en la última línea de la fila actual).
;         Regla: solo puede cambiar al salir de una fila SIN scroll horizontal;
;         en las demás, la entrada debe repetir el valor que ya tiene.
;   DTBK, DTPF0-2: colores, escritos justo tras el WSYNC (antes de que empiece el campo).
; Coste: unos 60 ciclos por fila.
; ===============================================================
        .segment "ZEROPAGE"
dlin:   .res 1

.ifndef DLI_N
DLI_N   = 32                ; entradas (el juego puede definir más antes de incluir el motor)
.endif
        .segment "HIBSS"
DTBK:   .res DLI_N
DTPF0:  .res DLI_N
DTPF1:  .res DLI_N
DTPF2:  .res DLI_N
DTHS:   .res DLI_N

        .segment "CODE"
m_dli:  pha
        txa
        pha
        ldx dlin
        lda DTHS,x
        sta HSCROL
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
