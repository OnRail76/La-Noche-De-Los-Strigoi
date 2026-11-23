"""SDI '86 · FASE 4 · LOS COMPUZOIDES DE JANUS · propuestas A/B/C (base de computadoras, todo metal, leds).
Partimos de lo elegido (agente B; androide, torreta, araña y ojo C) y se pasa todo a robot metalizado.
Colores de la fase: '1' metal oscuro, '2' metal claro, '3' led rojo de JANUS (los leds laten con una DLI)."""
TITULO = "SDI '86 · FASE 4 · COMPUZOIDES DE JANUS · PROPUESTAS (elige A, B o C de cada una)"
M = (0x06, 0x0C, 0x46)          # metal oscuro, metal claro, led
ANDROIDE = {   # sustituye al soldado: persigue al agente
    'A': ('Androide de visor rojo, pulido (el C de antes, en metal)', ['..2222..', '.213312.', '..1111..', '.222222.', '2.2112.2', '..1111..', '.2....2.', '.22..22.'], M),
    'B': ('Compuzoide de orugas con antena', ['...3....', '..222...', '.23232..', '.22222..', '1.111.1.', '..111...', '.11111..', '.1.1.1..'], M),
    'C': ('Humanoide con panel de leds en el pecho', ['..222...', '.21312..', '..222...', '2221222.', '2.131.2.', '2.111.2.', '..2.2...', '.22.22..'], M),
}
TORRETA = {    # sustituye al tirador: sale del suelo, apunta y dispara
    'A': ('Torreta que sale del suelo, pulida (el C de antes)', ['...33...', '..2112..', '.222222.', '.2.33.2.', '22222222', '11111111', '1.1111.1', '........'], M),
    'B': ('Cúpula con un led que gira', ['........', '..3333..', '.222222.', '22333322', '22222222', '11111111', '.1.11.1.', '........'], M),
    'C': ('Torre de dos cañones', ['.2....2.', '.2....2.', '.22..22.', '..2332..', '.222222.', '11111111', '1.1111.1', '........'], M),
}
ARANA = {      # sustituye al blindado: lenta y dura (16 x 12)
    'A': ('Araña mecánica, pulida (la C de antes, ojos-led)', [
        '................', '......2222......', '....22333322....', '...2223333222...', '..222222222222..', '.1.2222222222.1.',
        '1..1.222222.1..1', '1.1...1..1...1.1', '.1...1....1...1.', '1...1......1...1', '...1........1...', '................'], M),
    'B': ('Araña con núcleo de energía', [
        '................', '.....222222.....', '...2211331122...', '..221133331122..', '..222113311222..', '.1..22222222..1.',
        '1..1..2222..1..1', '.11..1....1..11.', '1...1......1...1', '1..1........1..1', '..1..........1..', '................'], M),
    'C': ('Cangrejo-tanque con pinzas', [
        '2..2........2..2', '.22..........22.', '..2..222222..2..', '...2223333222...', '..222222222222..', '.22222222222222.',
        '2222222222222222', '1111111111111111', '1.11.11.11.11.1.', '1111111111111111', '.11111111111111.', '................'], M),
}
OJO = {        # sustituye a los drones de pared: avisan y disparan
    'A': ('Ojo flotante, pulido (el C de antes)', ['..2222..', '.211112.', '21133112', '21333312', '21133112', '.211112.', '..2222..', '........'], M),
    'B': ('Ojo con antenas', ['3......3', '.2....2.', '..2222..', '.213312.', '.233332.', '.213312.', '..2222..', '........'], M),
    'C': ('Ojo en marco hexagonal', ['..1111..', '.122221.', '12233221', '12333321', '12233221', '.122221.', '..1111..', '........'], M),
}
MURO = {       # paredes de la base (4 x 8, en mosaico)
    'A': ('Armario de servidores con leds', ['1111', '1231', '1221', '1111', '1321', '1221', '1111', '2222'] * 2, M),
    'B': ('Chapa remachada', ['2222', '2112', '1311', '1111', '1113', '2112', '2222', '1111'] * 2, M),
    'C': ('Rejilla de ventilación', ['1111', '2222', '1111', '2222', '1311', '2222', '1111', '2222'] * 2, M),
}
CONSOLA = {    # sustituye a las cajas (8 x 16)
    'A': ('Ordenador de cintas (dos bobinas)', ['22222222', '21111112', '2.11.112', '1.31.31.', '2.11.112', '21111112', '22222222', '21333312',
                                                '21111112', '22222222', '21212122', '22222222', '21313122', '22222222', '11111111', '1......1'], M),
    'B': ('Terminal con pantalla', ['22222222', '21111112', '213..312', '21.33.12', '213..312', '21111112', '22222222', '.222222.',
                                    '22222222', '21212122', '22121212', '21212122', '22222222', '21133112', '22222222', '11111111'], M),
    'C': ('Bastidor de leds', ['22222222', '23.23.22', '22.23.32', '23.32.22', '22.23.32', '23.22.22', '22222222', '21111112',
                               '22222222', '23.32.22', '22.23.32', '23.22.22', '22.23.32', '23.32.22', '22222222', '11111111'], M),
}
DISPARO = {
    'A': ('Agente: ráfaga láser blanca, alargada en la dirección del disparo (misiles anchos). JANUS: bolas de plasma rojas (players)',
          ['........', '........', '22222222', '33333333', '22222222', '........', '..1..1..', '.111.111'], (0x46, 0x0E, 0x0E)),
    'B': ('Agente: dardo amarillo de dos tramos. JANUS: rombos rojos', ['........', '.3..3...', '.33.33..', '.3..3...', '........', '...1....', '..111...', '...1....'], (0x46, 0x0E, 0x1E)),
    'C': ('Agente: punto cian con estela. JANUS: anillos rojos', ['........', '.3......', '.33.....', '.33333..', '.33.....', '.3......', '..1.1...', '...1....'], (0x46, 0x0E, 0x9C)),
}
SECCIONES = [
    ('COMPUZOIDE DE ASALTO · persigue al agente (en lugar del soldado, 8 x 8)', ANDROIDE, 8, 3),
    ('TORRETA · sale del suelo, apunta y dispara (en lugar del tirador, 8 x 8)', TORRETA, 8, 3),
    ('ARAÑA · lenta y dura (en lugar del blindado, 16 x 12)', ARANA, 4, 3),
    ('OJO DE JANUS · en las paredes, avisa y dispara (en lugar del dron, 8 x 8)', OJO, 8, 3),
    ('PARED DE LA BASE (4 x 16, en mosaico)', MURO, 6, 3),
    ('CONSOLA · los obstáculos de la arena (en lugar de las cajas, 8 x 16)', CONSOLA, 4, 3),
    ('DISPAROS', DISPARO, 6, 3),
]
NOTAS = ['El agente se queda como está (B). Todo en metal: gris oscuro, gris claro y leds rojos de JANUS que laten; el suelo, chapa con rejilla y brillos.',
         'Al ser caracteres, los compuzoides comparten los colores de su fila con la base: por eso todo va en la misma gama metálica.']
