"""SDI '86 · datos del programa 4: AGENTE ENCUBIERTO (al estilo de Arena 3000)"""
import mar, agente as A, compuzoides as C

def build(G):
    cut, emit, bl, spr = G.cut, G.emit, G.bl, G.spr
    def rev(rows): return [r[::-1] for r in rows]
    # 1) lo sólido (paredes, cajas, drones) primero: códigos 64 .. SOLID_END-1
    MU = cut(C.MURO, 1, 'muro')[0][0]
    MH = cut(C.MURO_H, 1, 'muro h')[0][0]
    CJ = cut(C.CONSOLA, 2, 'consola')
    DN = cut(C.OJO, 2, 'ojo')[0]
    DA = cut(C.OJO_ALERTA, 2, 'ojo alerta')[0]
    DR = cut(C.OJO_ROTO, 2, 'ojo roto')[0]
    solid_end = 64 + len(G.GLIST)
    # 2) enemigos: ENE_LO .. ENE_HI
    ene_lo = solid_end
    SO = [cut(f, 2, 'androide')[0] for f in C.ANDROIDE]
    TI = [cut(f, 2, 'torreta')[0] for f in C.TORRETA]
    TIL = [cut(rev(f), 2, 'torreta izq.')[0] for f in C.TORRETA]
    BL = cut(C.ARANA, 4, 'araña')
    ene_hi = 64 + len(G.GLIST) - 1
    # 3) explosiones (ni sólidas ni enemigas)
    EXP = [cut(f, 2, 'explosion')[0] for f in mar.EXPLO]
    SCR = [[0] * 40 for _ in range(22)]
    for c in range(40):
        if not 18 <= c <= 21: SCR[0][c] = SCR[21][c] = MH
    for r in range(22):
        if not 10 <= r <= 11:
            for c in (0, 1, 38, 39): SCR[r][c] = MU
    DRONES = [(0, 3), (0, 35), (21, 3), (21, 35)]
    for r, c in DRONES: SCR[r][c:c + 2] = DN
    for r, c in ((5, 9), (5, 29), (15, 9), (15, 29), (10, 19)):
        SCR[r][c:c + 2] = CJ[0]; SCR[r + 1][c:c + 2] = CJ[1]
    G.emit_charset()
    emit('SUELO_G:'); bl(G.cell_bytes(C.SUELO, 0))
    emit('SOLID_END = %d' % solid_end)
    emit('ENE_LO = %d' % ene_lo); emit('ENE_HI = %d' % ene_hi)
    emit('SCR_INIT:')
    for r in SCR: bl(r, 20)
    emit('DRN_ROW: .byte ' + ','.join(str(r) for r, c in DRONES))
    emit('DRN_COL: .byte ' + ','.join(str(c) for r, c in DRONES))
    emit('DRN_N: .byte %d,%d' % tuple(DN)); emit('DRN_A: .byte %d,%d' % tuple(DA)); emit('DRN_R: .byte %d,%d' % tuple(DR))
    # enemigos: tipo 0 soldado (2 dibujos), 1 tirador (de pie / rodilla), 2 blindado (4 x 2)
    emit('SOL_F: .byte %d,%d,%d,%d' % tuple(SO[0] + SO[1]))
    emit('TIR_F: .byte ' + ','.join(str(c) for c in TI[0] + TI[1] + TIL[0] + TIL[1]))   # de pie, rodilla; a la derecha y a la izquierda
    emit('BLI_F: .byte ' + ','.join(str(c) for c in BL[0] + BL[1]))
    emit('EXPL_C:'); bl([c for f in EXP for c in f])
    # el agente: P0 uniforme ('2' y '3'), P1 piel ('1'); paso 0 y 1, mirando a la derecha y a la izquierda
    frames = [A.AGENTE, A.AGENTE_PASO, rev(A.AGENTE), rev(A.AGENTE_PASO), A.AGENTE_PASO_B, rev(A.AGENTE_PASO_B)]
    emit('AG_P0:')
    for f in frames: bl(spr(f, only='23'))
    emit('AG_P1:')
    for f in frames: bl(spr(f, only='1'))
    emit('BOOM_P:')
    for f in mar.SUB_EXPLO: bl(spr(G.pad16(f), 4, 8))
    status = 'OLEADA 1/3  COMPUZOIDES 00  VUELTA 01   '
    G.textos_juego([('MSG_FASE', 'FASE 4 - OPERACIÓN AGENTE ENCUBIERTO'),
                    ('MSG_OLA2', 'SEGUNDA OLEADA: TORRETAS DE JANUS'),
                    ('MSG_OLA3', 'TERCERA OLEADA: ARAÑAS DE COMBATE'),
                    ('MSG_CLEAR', 'BASE LIMPIA. AGENTE A SALVO')], status)
    emit('HUD_OL = %d' % (status.index('OLEADA ') + 7))
    emit('HUD_EN = %d' % (status.index('COMPUZOIDES ') + 12))
