; DLI por filas de La Noche de los Strigoi: lo mínimo antes de WSYNC (A y X a página cero), luego
; CHBASE y los colores más visibles; HSCROL al final (DTHS ya trae el valor de la fila siguiente).
; Necesita en página cero: dza, dzx, dlin; tablas DTCH, DTPF0-3, DTBK, DTHS de 22 entradas.
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
