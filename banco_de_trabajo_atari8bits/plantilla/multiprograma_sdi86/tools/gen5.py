"""SDI '86 · datos del programa 5: JANUS (Phoenix + los jefes de pared de Contra)"""
import mar, agente as A, janus as J

def build(G):
    cut, emit, bl, spr = G.cut, G.emit, G.bl, G.spr
    def rev(rows): return [r[::-1] for r in rows]
    one = lambda rows, n: cut(rows, 1, n)[0][0]
    CA = one(J.CORAZA, 'coraza'); CR = one(J.CORAZA_ROTA, 'coraza rota')
    EM = cut(J.EMISOR, 2, 'emisor')[0]; EA = cut(J.EMISOR_ALERTA, 2, 'emisor alerta')[0]
    ER = cut(J.EMISOR_ROTO, 2, 'emisor roto')[0]
    RI = one(J.RAYO_I, 'rayo'); RD = one(J.RAYO_D, 'rayo')
    AI = one(J.AVISO_I, 'aviso'); AD = one(J.AVISO_D, 'aviso')
    SA = one(J.SUELO_A, 'suelo'); SB = one(J.SUELO_B, 'suelo')
    CB = one(J.CABLE, 'cable')
    G.emit_charset()
    emit('CH_CA = %d' % CA); emit('CH_CR = %d' % CR)
    emit('EMI_N: .byte %d,%d' % tuple(EM)); emit('EMI_A: .byte %d,%d' % tuple(EA)); emit('EMI_R: .byte %d,%d' % tuple(ER))
    emit('CH_RI = %d' % RI); emit('CH_RD = %d' % RD); emit('CH_AI = %d' % AI); emit('CH_AD = %d' % AD)
    emit('CH_SA = %d' % SA); emit('CH_SB = %d' % SB); emit('CH_CB = %d' % CB)
    emit('EMI_COL: .byte ' + ','.join(str((x - 4) // 4) for x in J.EMISORES_X))
    # la pared: 160 x 40 (3 líneas de cielo arriba)
    px = [[0] * 160 for _ in range(40)]
    for y, r in enumerate(J.PARED):
        for x, c in enumerate(r):
            if c != '.': px[3 + y][x] = int(c)
    emit('WALL_BM:'); bl(G.bitmap(px, 160, 40))
    x0, x1, y0, y1 = J.NUCLEO
    emit('NUC_X0 = %d' % (48 + x0)); emit('NUC_X1 = %d' % (48 + x1))
    # cables del fondo: columnas fijas
    air = [CB if c in (2, 9, 11, 17, 22, 28, 30, 37) else 0 for c in range(40)]
    emit('AIR_ROW:'); bl(air)
    # el agente: de pie (2 pasos) y agachado, a la derecha y a la izquierda
    frames = [A.AGENTE, A.AGENTE_PASO, rev(A.AGENTE), rev(A.AGENTE_PASO), A.AGENTE_AGACHADO, rev(A.AGENTE_AGACHADO),
              A.AGENTE_PASO_B, rev(A.AGENTE_PASO_B), A.AGENTE_ARRIBA]
    emit('AG_P0:')
    for f in frames: bl(spr(f, only='23'))
    emit('AG_P1:')
    for f in frames: bl(spr(f, only='1'))
    emit('BOLA_P:'); bl(spr(J.BOLA))
    emit('BOOM_P:')
    for f in mar.SUB_EXPLO: bl(spr(G.pad16(f), 4, 8))
    status = 'NÚCLEO 00   EMISORES 4    VUELTA 01     '
    G.textos_juego([('MSG_FASE', 'FASE 5 - JANUS. PROTOCOLO FINAL'),
                    ('MSG_J1', 'JANUS: INICIANDO PROTOCOLO FINAL'),
                    ('MSG_J2', 'JANUS: AMENAZA NO PREVISTA'),
                    ('MSG_J3', 'JANUS: ERROR EN EL NÚCLEO. ERROR'),
                    ('MSG_NUC', 'NÚCLEO DE JANUS DESTRUIDO'),
                    ('MSG_CLEAR', 'JANUS DESCONECTADO. EL MUNDO RESPIRA')], status)
    emit('HUD_NU = %d' % (status.index('NÚCLEO ') + 7))
    emit('HUD_EM = %d' % (status.index('EMISORES ') + 9))
