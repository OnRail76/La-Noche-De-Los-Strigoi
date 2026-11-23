"""SDI '86 · pantalla de mando de JANUS (título): logotipo, mapa de guerra, trayectorias, textos.

Mapa: ANTIC E 160 x 60, equirectangular, longitudes -135..150 y latitudes 75..12 (hemisferio norte,
como un tablero de mando de los ochenta). Con el píxel NTSC (1,6 de ancho) sale casi 1:1 en grados.
  0 mar (negro) · 1 tierra (verde oscuro) · 2 costa y retícula (verde claro) · 3 trayectorias (rojo)
"""
LON0, LON1, LAT0, LAT1 = -135.0, 150.0, 75.0, 12.0
MW, MH = 160, 60

def proj(lon, lat):
    return (lon - LON0) / (LON1 - LON0) * MW, (LAT0 - lat) / (LAT0 - LAT1) * MH

# ---------------------------------------------------------------- costas (lon, lat), a grandes rasgos
NORTEAMERICA = [(-168, 65.5), (-165, 68), (-156, 71), (-141, 69.7), (-125, 70), (-110, 68), (-95, 68), (-85, 69.5),
    (-82, 66), (-88, 64), (-94, 58.8), (-92, 57), (-85, 55.5), (-82, 52.5), (-79, 51.5), (-77, 56), (-78, 60),
    (-78, 62.5), (-72, 61.5), (-65, 60), (-61, 56), (-56, 52), (-60, 49.5), (-65, 49), (-64, 45.5), (-61, 45.5),
    (-66, 44.5), (-70, 43), (-70, 41.5), (-74, 40.5), (-76, 38), (-76, 35), (-81, 31), (-80, 27), (-80, 25.2),
    (-82, 26), (-83, 29), (-86, 30.3), (-89, 30), (-94, 29.5), (-97, 27.5), (-97.5, 25), (-97, 21), (-95, 18.5),
    (-91, 18.8), (-90, 21.3), (-87, 21.5), (-88, 18), (-88, 16), (-84, 15.5), (-83.5, 11), (-80, 9), (-85, 10),
    (-87, 13), (-92, 14.5), (-96, 15.7), (-101, 17.5), (-105, 20), (-105.5, 22.5), (-109, 25.5), (-112.5, 29),
    (-114.5, 31.5), (-114, 30), (-112, 27), (-110, 23.5), (-112, 24.5), (-115, 28), (-117, 32.5), (-120.5, 34.5),
    (-122.5, 37.5), (-124, 40.5), (-124, 46), (-124.5, 48.3), (-123, 49), (-127, 50.5), (-130, 54.5), (-134, 58),
    (-139, 59.8), (-146, 60.5), (-152, 59), (-158, 57), (-163, 55), (-158, 58.5), (-162, 60), (-165, 62.5), (-164, 64.5)]
ARTICO_CA = [(-120, 74), (-100, 76), (-80, 76.5), (-75, 73), (-85, 70), (-100, 70.5), (-115, 72), (-125, 72.5)]
BAFFIN = [(-80, 73.5), (-70, 70.5), (-62, 66.5), (-66, 62), (-75, 64.5), (-80, 69)]
GROENLANDIA = [(-73, 78), (-60, 82), (-35, 83), (-20, 82), (-18, 77), (-21, 71), (-25, 68.5), (-35, 65.5), (-42, 60),
    (-48, 61), (-52, 65), (-54, 69), (-56, 74), (-66, 76.5)]
ISLANDIA = [(-24, 66), (-14, 66.5), (-13.5, 64.5), (-18, 63.4), (-22.5, 63.8)]
CUBA = [(-85, 22), (-80, 23.1), (-74.2, 20.2), (-77.7, 19.9), (-81, 21.6)]
EURASIA_AFRICA = [(-9, 37), (-9, 43), (-2, 43.5), (-1.5, 46), (-4.5, 48), (-1.5, 49.5), (2, 51), (4, 52), (8, 53.5),
    (8.5, 55.5), (10.5, 57.5), (12, 56), (11, 54.5), (14, 54), (19, 54.5), (21, 55), (21, 57), (24, 57.5), (23.5, 59.5),
    (30, 60), (28, 60.5), (23, 60), (21.5, 61), (21.5, 63.5), (25, 65.5), (22, 65.8), (17, 62.5), (19, 60), (16.5, 57),
    (14.5, 56), (12.5, 56.3), (11, 58.5), (8, 58), (5.5, 59), (5, 62), (8, 63.5), (12, 65), (15, 68), (18, 69.8), (25, 71),
    (31, 70), (33, 69.3), (41, 67.5), (40, 66), (34, 66.5), (38, 64.5), (44, 66), (44, 68.5), (53, 68.5), (60, 69),
    (68, 69), (73, 72.5), (80, 72.5), (87, 74), (100, 76.5), (105, 77.7), (113, 73.7), (129, 73), (140, 72.5),
    (150, 71.5), (160, 70), (170, 69.8), (180, 68.5), (180, 65), (177, 62.5), (170, 60), (163, 60), (160, 61.5),
    (163, 54), (157, 51), (155, 56), (152, 59), (143, 59.3), (137, 54), (141, 52), (140, 48), (135, 43), (131, 42.5),
    (129, 40), (128, 35), (126, 35), (126.5, 37.7), (124.5, 38), (121.5, 40), (118, 39), (119, 37), (122.5, 37.3),
    (120.5, 34.5), (122, 31), (121.5, 28.5), (119.5, 25.5), (116.5, 22.8), (113, 22), (110, 21), (108, 21.5),
    (106, 19.5), (107, 16), (109, 12), (105, 9), (100, 13), (98, 16), (94, 16), (94.5, 19), (92, 21.5), (90, 22),
    (87, 21.5), (86.5, 20), (80.3, 15.5), (80, 10), (77, 8), (73, 16), (72.7, 21), (70, 22.3), (67, 24.8), (62, 25.2),
    (57.5, 25.7), (56.5, 27), (52, 27.8), (50, 30), (48, 30), (50, 26.5), (51.5, 24.5), (54, 24), (56, 26), (57, 23.5),
    (59.8, 22.4), (55, 17), (52, 16), (45, 12.7), (43, 13), (42.7, 16), (39, 21.5), (35, 28), (34.8, 29.5),
    (32.5, 30), (33.5, 27.5), (35.5, 24), (37.3, 19), (39.5, 15.5), (43.3, 12.4), (51, 11.5), (51, 5), (40, -5),
    (20, -35), (12, -5), (9, 4), (-8, 4.5), (-13, 8), (-17, 14.5), (-17, 21), (-13, 27.5), (-10, 29), (-9.5, 32),
    (-6, 35.8), (-2, 35.2), (3, 36.8), (9.5, 37.3), (10.5, 36.8), (10, 33.7), (15.5, 31.5), (19.5, 30.3), (20, 32.5),
    (25, 31.7), (30, 31.3), (32, 31.2), (35, 33), (36, 36.5), (30, 36.3), (26.5, 38), (26, 40), (23, 40.5), (22.5, 37),
    (21, 38.5), (19.5, 41.5), (15, 45), (13.5, 45.5), (12.3, 44.5), (16, 41.5), (18.5, 40.2), (16, 38), (15.6, 38),
    (12.5, 41.8), (10.5, 43.5), (8.5, 44.3), (6, 43.1), (3, 43.3), (3.2, 42), (0.5, 40.5), (-0.5, 38.5), (-2, 36.7),
    (-5.6, 36)]
MAR_NEGRO = [(28, 41.2), (28, 43), (29.5, 45), (31, 46.6), (33.5, 44.4), (36.5, 45.3), (38, 47), (39.3, 47.1),
    (37.5, 45), (41.5, 41.5), (38, 41), (34.5, 42), (31, 41.2)]
CASPIO = [(47, 44.7), (50, 46.7), (53, 47), (54, 42), (53, 40), (54, 37), (51, 36.7), (49, 37.6), (49.5, 40.2), (47.5, 42.8)]
GRAN_BRETANA = [(-5.7, 50), (1.5, 51), (1.7, 52.8), (0, 53.5), (-0.2, 54.5), (-2, 55.9), (-3, 58.6), (-5, 58.6),
    (-6.2, 56.5), (-4.8, 54.8), (-3, 53.8), (-4.6, 52.9), (-5.2, 51.7), (-3, 51.4)]
IRLANDA = [(-6, 52), (-6, 54), (-7.5, 55.3), (-10, 54), (-10, 51.6)]
JAPON = [(130, 31), (131.5, 34), (135, 34.3), (140, 35), (141, 38), (141.5, 41.5), (145.5, 43.5), (144, 45),
    (141.5, 45.4), (140, 42.5), (139.8, 40), (139.5, 38.3), (137, 37), (133, 35.5), (129.6, 33.3)]
NUEVA_ZEMBLA = [(52, 71), (57, 75.5), (68, 77), (60, 73.5), (55, 70.5)]
TIERRA = [NORTEAMERICA, ARTICO_CA, BAFFIN, GROENLANDIA, ISLANDIA, CUBA, EURASIA_AFRICA, GRAN_BRETANA, IRLANDA,
          JAPON, NUEVA_ZEMBLA]
AGUA = [MAR_NEGRO, CASPIO]

# ---------------------------------------------------------------- trayectorias (origen, destino), alternando bandos
SITIOS = {'MOSCU': (37.6, 55.7), 'SVERDLOVSK': (60.6, 56.8), 'NOVOSIBIRSK': (82.9, 55.0), 'IRKUTSK': (104.3, 52.3),
          'MURMANSK': (33.1, 68.9), 'VLADIVOSTOK': (131.9, 43.1), 'CHEYENNE': (-104.8, 41.1), 'MINOT': (-101.3, 48.2),
          'MALMSTROM': (-111.2, 47.5), 'KANSAS': (-97.5, 38.5), 'ATLANTICO': (-35.0, 52.0), 'NOR_PACIFICO': (-160.0, 45.0),
          'WASHINGTON': (-77.0, 38.9), 'NUEVA_YORK': (-74.0, 40.7), 'CHICAGO': (-87.6, 41.9), 'LOS_ANGELES': (-118.2, 34.0),
          'SEATTLE': (-122.3, 47.6), 'HOUSTON': (-95.4, 29.8), 'LENINGRADO': (30.3, 59.9), 'KIEV': (30.5, 50.4),
          'BERLIN': (13.4, 52.5), 'LONDRES': (-0.1, 51.5), 'PEKIN': (116.4, 39.9), 'TOKIO': (139.7, 35.7)}
TRAYECTORIAS = [('MOSCU', 'WASHINGTON'), ('MINOT', 'MOSCU'), ('NOVOSIBIRSK', 'SEATTLE'), ('ATLANTICO', 'LENINGRADO'),
                ('SVERDLOVSK', 'CHICAGO'), ('CHEYENNE', 'KIEV'), ('MURMANSK', 'NUEVA_YORK'), ('MALMSTROM', 'SVERDLOVSK'),
                ('IRKUTSK', 'LOS_ANGELES'), ('KANSAS', 'BERLIN'), ('VLADIVOSTOK', 'TOKIO'), ('LONDRES', 'MOSCU')]

def trayectoria(a, b):
    """curva de Bézier en pantalla, levantada hacia el norte (como una ruta polar); puntos de píxel contiguos"""
    x0, y0 = proj(*SITIOS[a]); x1, y1 = proj(*SITIOS[b])
    d = abs(x1 - x0)
    cx, cy = (x0 + x1) / 2, min(y0, y1) - d * 0.45
    pts = []
    for i in range(2001):
        t = i / 2000
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
        p = (int(round(x)), max(1, int(round(y))))
        if 0 <= p[0] < MW and p[1] < MH and (not pts or pts[-1] != p): pts.append(p)
    return pts

# ---------------------------------------------------------------- logotipo SDI '86 (ANTIC E, 20 líneas)
GLIFOS = {
    'S': [' XXXXXX', 'XX     ', ' XXXXX ', '     XX', 'XXXXXX '],
    'D': ['XXXXXX ', 'XX   XX', 'XX   XX', 'XX   XX', 'XXXXXX '],
    'I': ['XXX'] * 5,
    "'": ['XX', 'XX', ' X', '  ', '  '],
    '8': ['XXXXXXX', 'XX   XX', 'XXXXXXX', 'XX   XX', 'XXXXXXX'],
    '6': ['XXXXXXX', 'XX     ', 'XXXXXXX', 'XX   XX', 'XXXXXXX'],
}
LOGO_TXT = "SDI'86"
CW, CH = 3, 4                       # cada celda del glifo: 3 píxeles x 4 líneas
LOGO_H = 20
# degradado del relleno (PF0) línea a línea: cromado azulado con una línea de brillo, como la carátula
LOGO_GRAD = [0x0E, 0x0E, 0x9E, 0x9E, 0x9C, 0x9C, 0x9A, 0x9A, 0x0E, 0x0C, 0x9A, 0x98, 0x98, 0x96, 0x96, 0x94,
             0x94, 0x92, 0x92, 0x90]

def logo_pixels():
    """160 x 20 con índices 0-3: 1 relleno, 2 sombra/barras rojas, 3 brillo"""
    cells = []
    for i, ch in enumerate(LOGO_TXT):
        g = GLIFOS[ch]
        w = len(g[0])
        cells.append((g, w))
    total = sum(w * CW for g, w in cells) + (len(cells) - 1) * 4
    x0 = (MW - total) // 2
    img = [[0] * MW for _ in range(LOGO_H)]
    x = x0
    for g, w in cells:
        for r in range(5):
            for c in range(w):
                if g[r][c] != 'X': continue
                up = r > 0 and g[r - 1][c] == 'X'
                dn = r < 4 and g[r + 1][c] == 'X'
                rt = c < w - 1 and g[r][c + 1] == 'X'
                for yy in range(CH):
                    for xx in range(CW):
                        v = 1
                        if yy == 0 and not up: v = 3
                        if yy == CH - 1 and not dn: v = 2
                        if xx == CW - 1 and not rt and yy > 0: v = 2
                        img[r * CH + yy][x + c * CW + xx] = v
        x += w * CW + 4
    # barras rojas a los lados (como en la carátula)
    for yy in (6, 7, 10, 11, 14, 15):
        for xx in list(range(4, x0 - 5)) + list(range(x0 + total + 5, MW - 4)):
            img[yy][xx] = 2
    return img

# ---------------------------------------------------------------- textos (ANTIC 2: 40 columnas; ANTIC 6: 20)
HUD = ' DEFCON 5                    T-MENOS 00:30'[:40].ljust(40)
ALERTA = '■ ALERTA ■'
PF = 'PROTOCOLO FINAL'
MENU = ['ARCADE - LAS CINCO OPERACIONES', 'OPERACIÓN MAR HELADO', 'OPERACIÓN DEFENSA SDI',
        'OPERACIÓN ESTACIÓN ORBITAL', 'OPERACIÓN AGENTE ENCUBIERTO', 'OPERACIÓN JANUS']
IMPLEMENTADA = [1, 1, 0, 0, 0, 0]          # modos que ya se pueden jugar
AMENAZA = ('  AMENAZA:' + ' ' * 17 + 'RÉCORD 000000').ljust(40)
DIFS = ['◂ FÁCIL ▸', '◂ NORMAL ▸', '◂ HARDCORE ▸']
CREDITOS = ('  PULSA FIRE' + ' ' * 9 + '2026 - TONY C. WARE').ljust(40)
TELETIPO = [                        # 37 caracteres como mucho (prompt + texto + cursor = 40)
    '1986. EL MUNDO ESPERA LA PAZ.',
    'JANUS HA CALCULADO OTRA SOLUCIÓN.',
    'PROBABILIDAD DE PAZ: 0,00 %',
    'OBJETIVOS FIJADOS: 1.024',
    'BLOQUEO NAVAL DEL MAR HELADO: ACTIVO',
    'SATÉLITES SDI: SIN RESPUESTA',
    'PROTOCOLO FINAL: ESPERANDO OPERADOR',
]
TELE_ALERTA = 'ALERTA: LANZAMIENTO INMINENTE'
TELE_PREP = 'OPERACIÓN EN PREPARACIÓN. ELIJA OTRA.'
RECORDS_NOMBRES = ['ARCADE', 'MAR HELADO', 'DEFENSA SDI', 'ESTACIÓN', 'AGENTE', 'JANUS']
