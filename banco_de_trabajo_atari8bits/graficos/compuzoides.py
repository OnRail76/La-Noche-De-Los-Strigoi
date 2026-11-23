"""SDI '86 · FASE 4 · los Compuzoides de JANUS (elegidos: todo A). Base de computadoras, metal y leds.
Colores de la fase: '1' metal oscuro (PF0), '2' metal claro (PF1, con el brillo que recorre la base), '3' led rojo (PF2, late)."""
import propuestas_f4b as P

ANDROIDE = [P.ANDROIDE['A'][1], P.ANDROIDE['A'][1][:6] + ['..2..2..', '..22.22.']]       # dos pasos
TORRETA = [['........', '........', '........', '........', '...33...', '..2112..', '22222222', '1.1111.1'],   # escondida (anda)
           P.TORRETA['A'][1]]                                                               # desplegada (dispara)
ARANA = P.ARANA['A'][1] + ['................'] * 4                                          # 16 x 16 (2 filas)
OJO = P.OJO['A'][1]
OJO_ALERTA = ['..2222..', '.233332.', '23333332', '23333332', '23333332', '.233332.', '..2222..', '........']
OJO_ROTO = ['........', '1..1....', '.11.1...', '..1.....', '..1.....', '.1.1....', '1...1...', '........']
MURO = P.MURO['A'][1][:8]                                                                   # armario de servidores (paredes laterales)
MURO_H = ['2222', '1111', '1231', '1111', '1321', '1111', '1111', '2222']                    # el mismo, tumbado (arriba y abajo)
CONSOLA = P.CONSOLA['A'][1]                                                                 # ordenador de cintas (8 x 16)
SUELO = ['1111', '1...', '1...', '1...', '1...', '1...', '1...', '1...']                     # chapa (el carácter 0 de la arena)
