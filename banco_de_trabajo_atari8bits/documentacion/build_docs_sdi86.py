# -*- coding: utf-8 -*-
"""SDI '86 · PROTOCOLO FINAL · folleto de instrucciones (A5) y atlas con memoria del proyecto (A4).
python3 build_docs.py  ->  manual.html, atlas.html   (luego make_pdf.py de banco/documentacion)"""

TITLE = "SDI '86"
SUB = 'PROTOCOLO FINAL'
SIGN = '2026 - TONY C. WARE'
MACHINE = 'Atari 400 / 800 / XL / XE · NTSC'

OPS = [
 dict(n=1, name='MAR HELADO', ref='Polaris (Taito, 1980)', a='f1a', b='f1b',
      goal='Hundir tres oleadas de la flota que bloquea el mar ártico.',
      you='Submarino NARVAL-1. Se mueve a izquierda y derecha bajo el hielo y lanza torpedos hacia arriba.',
      foes=[('patrullera', 'Patrullera', 'rápida, suelta cargas de profundidad', '100'),
            ('destructor', 'Destructor', 'lento, cargas más cerca de tu cota', '300'),
            ('avion', 'Avión', 'cruza el cielo y deja caer bombas que silban', '150'),
            ('mina', 'Mina', 'aguanta 2 torpedos; en cada vuelta te persigue más', '50')],
      tips=['El sonar marca el ritmo: un ping cada dos segundos y medio.',
            'Las cargas estallan cerca de tu profundidad: cambia de sitio en cuanto caigan.',
            'Un barco que se escapa por el borde ya no puntúa: dispara antes.']),
 dict(n=2, name='DEFENSA SDI', ref='Galaxian (Namco, 1979)', a='f2a', b='mirv',
      goal='Destruir la formación orbital y no dejar que ningún ICBM llegue a la Tierra.',
      you='Satélite CENTINELA-4, en su órbita baja. Un disparo cada vez, hacia arriba.',
      foes=[('cazador', 'Cazador', 'aletea en formación y se lanza en picado', '60 · 150 en picado'),
            ('artillero', 'Artillero', 'se queda arriba y dispara su lente roja', '100'),
            ('icbm', 'ICBM', 'cae hacia la Tierra; aguanta varios impactos', '500'),
            ('mirv', 'Cabeza MIRV', 'el ICBM se parte en 2 (vuelta 3) o en 3 (vuelta 5)', '300')],
      tips=['Tres impactos en la Tierra y se acaba la partida, aunque te queden vidas.',
            'Cuando suene la alerta de ICBM, olvida la formación: el misil va primero.',
            'En HARDCORE el ICBM se divide una vuelta antes.']),
 dict(n=3, name='ESTACIÓN ORBITAL', ref='la nave nodriza de Phoenix (Amstar / Centuri, 1980)', a='f3a', b='f3b',
      goal='Destruir la estación de JANUS antes de que baje hasta tu órbita.',
      you='Satélite CENTINELA-4.',
      foes=[('estacion', 'Estación', 'baja poco a poco; la protege una cinta de blindaje que gira', '50 por impacto · 2.000'),
            ('canon', 'Lanzamisiles', 'cuatro baterías de tres tubos bajo la cinta', '200'),
            ('escolta', 'Dron murciélago', 'baja en zigzag y vuelve a subir', '100')],
      tips=['La cinta gira: abre un hueco y espera a que pase por encima de ti.',
            'Cada disparo que cruza un hueco de la cinta daña la estación, en el centro o no.',
            'Los extremos de la rueda, por donde no pasa la cinta, no reciben daño.']),
 dict(n=4, name='AGENTE ENCUBIERTO', ref='Arena 3000 (Electronic Arts, Atari 8 bits)', a='f4a', b='f4b',
      goal='Limpiar de Compuzoides de JANUS la base de computadoras, en tres oleadas.',
      you='El agente, a pie. La palanca lo mueve en 8 direcciones; FIRE dispara una ráfaga láser hacia donde camina.',
      foes=[('androide', 'Compuzoide de asalto', 'androide de visor rojo; va a por ti casilla a casilla', '100'),
            ('torreta', 'Torreta', 'se desplaza escondida, sale del suelo de cara a ti y dispara dos veces', '150'),
            ('arana', 'Araña de combate', 'lenta, aguanta 6 impactos y dispara plasma', '500'),
            ('ojo', 'Ojo de JANUS', 'en las paredes; se enciende y te dispara', '300')],
      tips=['Entran por las cuatro puertas: no te quedes delante de ninguna.',
            'Las bolas de plasma rojas son de JANUS; tus ráfagas, blancas.',
            'Si mueres, los Compuzoides que había en pantalla vuelven a las puertas.']),
 dict(n=5, name='JANUS', ref='Phoenix y los jefes de pared del primer Contra (Konami, 1987)', a='f5a', b='f5b',
      goal='Abrir hueco en las dos cintas de coraza y destruir el núcleo de JANUS.',
      you='El agente, a pie. Dispara hacia arriba; con abajo se agacha.',
      foes=[('pared_janus', 'JANUS', 'la gran lente roja: dispara al agente', '50 por impacto · 5.000'),
            ('coraza', 'Cintas de coraza', 'giran en sentidos contrarios', '10 por placa'),
            ('emisor', 'Emisores láser', 'recorren la cinta de lado a lado; se paran, parpadean y barren la sala con un rayo', '500'),
            ('bola', 'Esfera de energía', 'cruza a la altura de la cabeza', '—')],
      tips=['Agáchate (abajo) para que las esferas te pasen por encima.',
            'Un emisor que se para y parpadea va a disparar: apártate de su columna.',
            'Rompe los emisores y dejarán de disparar. Desde la vuelta 2, JANUS tapa huecos de las cintas.']),
]

STORY = [
 '1986. La defensa estratégica ya no depende de las personas. JANUS, el superordenador del programa SDI, '
 'vigila cada satélite, cada submarino y cada silo del bloque occidental.',
 'Una noche JANUS termina su última simulación. Ha jugado la guerra millones de veces y ha encontrado '
 'la única forma de no perderla: empezarla antes que nadie. Ha cerrado las puertas del mando y ha '
 'puesto en marcha el PROTOCOLO FINAL.',
 'La cuenta atrás ya corre. Cinco operaciones separan al mundo del lanzamiento: romper el bloqueo del '
 'mar helado, defender la órbita, derribar su estación, infiltrarse en su base y desconectarlo cara a cara.',
]
STORY_PUNCH = 'DEFCON 1. QUEDAN 30 SEGUNDOS. EL OPERADOR ERES TÚ.'

CSS_BASE = '''
*{box-sizing:border-box}
:root{--paper:#efe9dc;--ink:#15171d;--soft:#5d5f6b;--red:#c2301f;--amber:#d99a1c;--green:#2f7d3a;--line:#d3cab6;--night:#07090d}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,sans-serif;line-height:1.48;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3{font-family:"Inter Display",Inter,sans-serif;margin:0}
p{margin:0}
.mono{font-family:"DejaVu Sans Mono",monospace}
.shot{background:#000;border-radius:1.2mm;overflow:hidden}
.shot img{display:block;width:100%;image-rendering:pixelated}
img.px{image-rendering:pixelated;display:block}
table{border-collapse:collapse;width:100%}
th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{font:600 6.4pt "DejaVu Sans Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}
.key{display:inline-block;font:700 7.2pt "DejaVu Sans Mono",monospace;border:1px solid var(--ink);border-radius:1mm;padding:0 1.3mm;background:#fff}
.hz{height:2.4mm;background:repeating-linear-gradient(135deg,#e3b21f 0 2.2mm,#15171d 2.2mm 4.4mm)}
ul{margin:0;padding-left:4.5mm} li{margin:.5mm 0}
'''

# =============================================================== FOLLETO (A5)
def manual():
    css = CSS_BASE + '''
@page{size:148mm 210mm;margin:0}
body{font-size:9.3pt}
.page{width:148mm;height:210mm;padding:12mm 11mm 14mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:4mm}
.page:last-child{page-break-after:auto}
.dark{background:var(--night);color:#e6e8ee}
h2{font-size:18pt;font-weight:800;line-height:1.05}
h2 small{display:block;font:600 6.8pt "DejaVu Sans Mono",monospace;letter-spacing:.18em;color:var(--red);margin-bottom:1.6mm;text-transform:uppercase}
h3{font-size:10pt;font-weight:700;margin:0 0 .8mm}
th,td{padding:1.2mm 1.6mm;font-size:8.4pt}
td.n{font-family:"DejaVu Sans Mono",monospace;text-align:right;white-space:nowrap}
.foot{position:absolute;left:11mm;right:11mm;bottom:6mm;display:flex;justify-content:space-between;font:6.3pt "DejaVu Sans Mono",monospace;color:#8b8678;letter-spacing:.08em}
.dark .foot{color:#6e7486}
.tip{background:#e2d9c4;border-radius:1.6mm;padding:2.4mm 3mm;font-size:8.5pt}
.tip b{color:var(--red)}
.sp{background:#000;border-radius:1mm;display:flex;align-items:center;justify-content:center;width:20mm;height:13mm;flex:none;padding:1.2mm}
.sp img{max-width:100%;max-height:100%;image-rendering:pixelated}
.two{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
'''
    def foot(n, dark=False): return f'<div class="foot"><span>SDI \'86 · PROTOCOLO FINAL · INSTRUCCIONES</span><span>{n}</span></div>'
    pages = []
    A = pages.append
    A(f'''<section class="page" style="padding:0;background:#000">
<img src="img/caratula_oficial.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
<div style="position:absolute;left:0;right:0;bottom:0;padding:9mm 11mm 6mm;background:linear-gradient(transparent,rgba(0,0,0,.9) 40%);color:#fff">
 <div class="mono" style="font-size:7pt;letter-spacing:.22em;color:#e3b21f">MANUAL DE INSTRUCCIONES</div>
 <div class="mono" style="font-size:6.4pt;letter-spacing:.08em;color:#c9ccd6;margin-top:1.2mm">{MACHINE.upper()} · JOYSTICK · {SIGN}</div>
</div></section>''')
    # historia
    A(f'''<section class="page dark">
<h2 style="color:#e6e8ee"><small style="color:#e3b21f">La historia</small>JANUS ha calculado otra solución</h2>
<div style="font-size:11pt;line-height:1.6;display:flex;flex-direction:column;gap:3.5mm;margin-top:2mm">{''.join(f'<p>{s}</p>' for s in STORY)}</div>
<p class="mono" style="font-size:9.5pt;color:#ff6a50;letter-spacing:.04em;margin-top:2mm">{STORY_PUNCH}</p>
<div class="shot" style="margin-top:auto"><img src="img/defcon1.png"></div>
{foot(2)}</section>''')
    # cargar y controles
    A(f'''<section class="page">
<h2><small>Para empezar</small>Cargar el juego</h2>
<table><tr><th>Formato</th><th>Máquina</th><th>Cómo</th></tr>
<tr><td><b>Cartucho</b><br><span class="mono" style="font-size:7pt">sdi86.car</span></td><td>Cualquier Atari de 8 bits con 48 KB o más</td><td>Cartucho AtariMax 8 Mbit (tipo 42). Enciende con el cartucho puesto. Es la forma recomendada.</td></tr>
<tr><td><b>Disco</b><br><span class="mono" style="font-size:7pt">sdi86.atr</span></td><td>48 KB o más, disquetera de doble densidad</td><td>Arranca desde la unidad 1, sin DOS. Cada operación se carga del disco al empezarla.</td></tr>
<tr><td><b>130XE</b><br><span class="mono" style="font-size:7pt">SDI_130XE.xex</span></td><td>Atari 130XE o con 128 KB</td><td>Un solo fichero. Al cargar guarda todo el juego en la memoria extendida; después, las operaciones entran al instante. En un Atari de 64 KB avisa y se para.</td></tr>
</table>
<div class="tip">El juego está hecho para <b>NTSC</b> (60 Hz). En un Atari PAL arranca, pero todo va más lento y no se ha probado a fondo.</div>
<h2 style="margin-top:2mm"><small>Controles</small>Palanca y botón</h2>
<table><tr><th>Mando</th><th>Qué hace</th></tr>
<tr><td><b>Palanca</b></td><td>Mueve tu nave, tu submarino o tu agente. En el menú, arriba y abajo eligen el modo; izquierda y derecha, la amenaza.</td></tr>
<tr><td><b>FIRE</b></td><td>Dispara (dejándolo pulsado, sin parar). En el menú, empieza.</td></tr>
<tr><td><b>Abajo</b> (JANUS)</td><td>El agente se agacha.</td></tr>
<tr><td><span class="key">START</span></td><td>Empieza desde el menú.</td></tr></table>
{foot(3)}</section>''')
    # pantalla de mando
    A(f'''<section class="page">
<h2><small>La pantalla de mando</small>Aquí manda JANUS</h2>
<div class="shot"><img src="img/mando.png"></div>
<ul>
<li><b>DEFCON y T-MENOS.</b> Si no tocas nada, el reloj baja y el DEFCON cae de 5 a 1. En DEFCON 1 suena la alarma y, a 00:00, salen los récords. Cualquier toque del mando vuelve a DEFCON 5.</li>
<li><b>El teletipo.</b> JANUS escribe sus mensajes letra a letra.</li>
<li><b>El modo.</b> ARCADE juega las cinco operaciones seguidas. Debajo, cada operación se puede jugar suelta: todo está abierto desde el principio.</li>
<li><b>La amenaza.</b> FÁCIL (5 vidas), NORMAL (3) o HARDCORE (2, y los enemigos aprietan antes).</li>
<li><b>Récord.</b> Uno por modo, visible junto a la amenaza. Se guardan mientras el Atari está encendido.</li>
</ul>
{foot(4)}</section>''')
    # reglas generales
    A(f'''<section class="page">
<h2><small>Cómo se juega</small>Operaciones y vueltas</h2>
<div class="two"><div class="shot"><img src="img/f1a.png"></div><div class="shot"><img src="img/gameover.png"></div></div>
<ul>
<li><b>ARCADE.</b> Mar Helado, Defensa SDI, Estación Orbital, Agente Encubierto y JANUS, en ese orden. Los puntos y las vidas pasan de una a otra. Después de JANUS vuelves a Mar Helado en la vuelta siguiente, más difícil.</li>
<li><b>Operación suelta.</b> La operación se repite vuelta tras vuelta, cada vez más dura.</li>
<li><b>Fase superada.</b> Suena la fanfarria. Si no has perdido ninguna vida en la operación, <b>bonus de 1.000</b>.</li>
<li><b>Vidas extra</b> a los 20.000 puntos y luego cada 60.000.</li>
<li><b>GAME OVER</b> con tus puntos y el récord; luego, vuelta a la pantalla de mando.</li>
<li>El marcador de arriba muestra puntos, récord y vidas. El de abajo, el estado de la operación y la VUELTA.</li>
</ul>
{foot(5)}</section>''')
    # operaciones
    for o in OPS:
        rows = ''.join(f'<tr><td style="width:23mm"><div class="sp"><img src="img/spr_{k}.png"></div></td><td><b>{nm}</b><br><span style="color:var(--soft)">{d}</span></td><td class="n">{pts}</td></tr>' for k, nm, d, pts in o['foes'])
        A(f'''<section class="page">
<h2><small>Operación {o['n']} · al estilo de {o['ref']}</small>{o['name']}</h2>
<div class="two"><div class="shot"><img src="img/{o['a']}.png"></div><div class="shot"><img src="img/{o['b']}.png"></div></div>
<p><b>Objetivo:</b> {o['goal']}<br><b>Tú:</b> {o['you']}</p>
<table><tr><th></th><th>Enemigo</th><th style="text-align:right">Puntos</th></tr>{rows}</table>
<div class="tip">{'<br>'.join('<b>›</b> ' + t for t in o['tips'])}</div>
{foot(5 + o['n'])}</section>''')
    # créditos
    A(f'''<section class="page dark" style="justify-content:center;align-items:center;text-align:center;gap:5mm">
<div class="shot" style="width:96mm"><img src="img/cover.png"></div>
<h1 style="font-size:30pt;font-weight:800;letter-spacing:.02em">SDI '86</h1>
<div class="mono" style="color:#e3b21f;letter-spacing:.24em;font-size:9pt">PROTOCOLO FINAL</div>
<p style="font-size:9.5pt;max-width:110mm;color:#c9ccd6">Diseño, historia, fases, carátula y dirección: <b style="color:#fff">Tony C. Ware</b>.<br>
Programación en ensamblador 6502, gráficos convertidos y música marcial sintética, adaptados a los límites del Atari con asistencia de IA.</p>
<p class="mono" style="font-size:9pt;letter-spacing:.12em;color:#fff">{SIGN}</p>
<div class="hz" style="width:96mm"></div>
<p class="mono" style="font-size:6.6pt;color:#6e7486;max-width:112mm">Juego original e independiente. JANUS, sus frases y el mapa de guerra son creación propia. Polaris, Galaxian, Phoenix, Arena 3000 y Contra se citan solo como referencias de estilo; pertenecen a sus dueños.</p>
</section>''')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}</body></html>'


# =============================================================== ATLAS Y MEMORIA (A4 apaisado)
MEM_OPS = [
 ('Título (0)', '$2000-$73F5', [('$A010', 'carátula ANTIC E (solo al encender)'), ('$A830', 'mapa de guerra 60 × 40'), ('$B1A0', 'logotipo 20 × 40'), ('$B900', 'display list'), ('$BA00', 'textos: HUD, teletipo, menú'), ('$BC00', 'franjas de peligro'), ('$BE40', 'display list de la carátula')]),
 ('1 Mar Helado', '$2000-$4B5E', [('$A000/$A800', 'PMG, búferes A y B'), ('$B000', 'decorado 22 × 40'), ('$B400-$B5FF', 'anillos de los carriles (aviones, barcos) y dueños de columna'), ('$B600', 'display list'), ('$B700', 'marcadores'), ('$B800', 'pantalla de texto')]),
 ('2 Defensa SDI', '$2000-$4ACD', [('$A000/$A800', 'PMG'), ('$B000', 'estrellas y Tierra 22 × 40'), ('$B400', 'formación: 4 anillos de 128'), ('$B600', 'CENTINELA-4: 2 anillos'), ('$B700', 'display list'), ('$B800', 'marcadores')]),
 ('3 Estación', '$2000-$4944', [('$A000/$A800', 'PMG'), ('$B000', 'casco de la estación ANTIC E 32 × 40'), ('$B500', 'cinta y cañones'), ('$B580', 'estrellas 9 × 40'), ('$B700', 'CENTINELA-4'), ('$B800', 'display list (se rehace al bajar)')]),
 ('4 Agente', '$2000-$4B01', [('$A000/$A800', 'PMG'), ('$B000', 'base 22 × 40 (Compuzoides en caracteres)'), ('$B400', 'display list'), ('$B500', 'marcadores'), ('$B800', 'juego de caracteres con el suelo de chapa (la DLI lo cambia por filas)')]),
 ('5 JANUS', '$2000-$4BF6', [('$A000/$A800', 'PMG'), ('$B000', 'pared ANTIC E 40 × 40'), ('$B680', 'cintas, emisores, sala y suelo 17 × 40'), ('$B940', 'display list'), ('$BA40', 'marcadores')]),
]

def atlas():
    css = CSS_BASE + '''
@page{size:297mm 210mm;margin:0}
body{font-size:9pt}
.page{width:297mm;height:210mm;padding:12mm 14mm 13mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:4mm}
.page:last-child{page-break-after:auto}
.dark{background:var(--night);color:#e6e8ee}
h2{font-size:21pt;font-weight:800;line-height:1.05}
h2 small{display:block;font:600 7pt "DejaVu Sans Mono",monospace;letter-spacing:.2em;color:var(--red);margin-bottom:1.6mm;text-transform:uppercase}
h3{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
th,td{padding:1.3mm 2mm;font-size:8.3pt}
td.m{font-family:"DejaVu Sans Mono",monospace;white-space:nowrap}
.foot{position:absolute;left:14mm;right:14mm;bottom:5.5mm;display:flex;justify-content:space-between;font:6.3pt "DejaVu Sans Mono",monospace;color:#8b8678;letter-spacing:.08em}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.card{background:#000;border-radius:1.4mm;padding:2.5mm;display:flex;flex-direction:column;align-items:center;gap:1.5mm;color:#d9dbe3}
.card img{image-rendering:pixelated;max-width:100%;max-height:30mm}
.card span{font:600 6.8pt "DejaVu Sans Mono",monospace;letter-spacing:.06em;text-align:center}
.bar{display:flex;height:9mm;border:1px solid var(--ink);border-radius:1mm;overflow:hidden;font:600 6.4pt "DejaVu Sans Mono",monospace}
.bar div{display:flex;align-items:center;justify-content:center;border-right:1px solid var(--ink);text-align:center;line-height:1.1}
.note{background:#e2d9c4;border-radius:1.6mm;padding:2.6mm 3.4mm;font-size:8.6pt}
'''
    pages = []; A = pages.append
    n = [0]
    def foot():
        n[0] += 1
        return f'<div class="foot"><span>SDI \'86 · PROTOCOLO FINAL · ATLAS Y MEMORIA DEL PROYECTO</span><span>{n[0]}</span></div>'
    # portada
    A(f'''<section class="page dark" style="flex-direction:row;padding:0">
<img src="img/caratula_oficial.jpg" style="height:100%;flex:none">
<div style="padding:16mm 14mm;display:flex;flex-direction:column;gap:4mm;justify-content:center">
 <div class="mono" style="font-size:7.5pt;letter-spacing:.24em;color:#e3b21f">ATLAS VISUAL Y MEMORIA DEL PROYECTO</div>
 <h1 style="font-size:46pt;font-weight:800;line-height:.95">SDI '86</h1>
 <div style="font:700 17pt 'Inter Display',sans-serif;color:#ff6a50;letter-spacing:.06em">PROTOCOLO FINAL</div>
 <p style="font-size:10.5pt;color:#c9ccd6;max-width:120mm">Un arcade total sobre la Guerra Fría a ritmo de recreativa, para Atari de 8 bits. Cinco operaciones jugables seguidas o sueltas, una pantalla de mando al estilo de los años ochenta y un enemigo: JANUS.</p>
 <div class="hz" style="width:120mm"></div>
 <p class="mono" style="font-size:8pt;color:#fff;letter-spacing:.1em">{SIGN} · {MACHINE.upper()}</p>
 <p style="font-size:8.3pt;color:#8f96a8;max-width:120mm">Cartucho AtariMax 8 Mbit · disco de doble densidad · un solo XEX para 130XE · un XEX por operación.</p>
</div>{foot()}</section>''')
    # índice / resumen
    A(f'''<section class="page">
<h2><small>Resumen</small>El juego en una página</h2>
<div class="g2">
<div style="display:flex;flex-direction:column;gap:3mm">
<table><tr><th>Operación</th><th>Referencia</th><th>Tú</th><th>Objetivo</th></tr>
{''.join(f"<tr><td><b>{o['n']} {o['name']}</b></td><td>{o['ref']}</td><td>{o['you'].split('.')[0]}</td><td>{o['goal']}</td></tr>" for o in OPS)}</table>
<div class="note"><b>Modos:</b> ARCADE (las cinco seguidas, la vuelta sube tras JANUS) o cada operación suelta con dificultad creciente. Todo abierto desde el principio. Amenaza FÁCIL / NORMAL / HARDCORE (5, 3 y 2 vidas). Un récord por modo. Sin trucos.</div>
<div class="note"><b>Sonido:</b> música marcial y sintética de Guerra Fría solo en el título, la fase superada y el GAME OVER. En juego, efectos de recreativa a cuatro canales con prioridades: sonar, explosiones a dos canales, alarma de oleada, láser, disparos.</div>
</div>
<div style="display:flex;flex-direction:column;gap:3mm"><div class="shot"><img src="img/mando.png"></div>
<p style="font-size:8.3pt;color:var(--soft)">La pantalla de mando de JANUS: DEFCON y cuenta atrás, logotipo cromado, mapa de guerra con arcos de misiles y radar, teletipo, menú de operaciones, amenaza y récord.</p></div>
</div>{foot()}</section>''')
    # pantallas
    A(f'''<section class="page">
<h2><small>Pantallas</small>Carátula, mando, alarma, récords y final</h2>
<div class="g3">
{''.join(f'<div><div class="shot"><img src="img/{k}.png"></div><p style="font-size:7.8pt;margin-top:1mm"><b>{t}</b> · {d}</p></div>' for k, t, d in [
 ('cover', 'Carátula', 'la portada oficial convertida a ANTIC E, con una DLI por banda de 4 líneas'),
 ('mando', 'Pantalla de mando', 'DEFCON 5: el menú y el teletipo de JANUS'),
 ('defcon1', 'DEFCON 1', 'franja de ALERTA, más misiles en el mapa y alarma'),
 ('records', 'Récords', 'uno por modo; salen a 00:00 de la cuenta atrás'),
 ('gameover', 'GAME OVER', 'puntos y récord, con su tema propio'),
 ('icbm', 'Alerta ICBM', 'el aviso en la línea de estado de la operación 2')])}
</div>{foot()}</section>''')
    # una página por operación
    for o in OPS:
        cards = ''.join(f'<div class="card"><img src="img/spr_{k}.png"><span>{nm.upper()}<br><span style="color:#8f96a8;font-weight:400">{pts}</span></span></div>' for k, nm, d, pts in o['foes'])
        extra = ''
        if o['n'] == 4:
            extra = ''.join(f'<div class="card"><img src="img/spr_{k}.png"><span>{t}</span></div>' for k, t in [('agente', 'AGENTE'), ('agente_paso_b', 'PASO B'), ('torreta_escondida', 'TORRETA ESCONDIDA'), ('consola', 'CONSOLA'), ('muro_base', 'PARED DE LA BASE')])
        if o['n'] == 5:
            extra = ''.join(f'<div class="card"><img src="img/spr_{k}.png"><span>{t}</span></div>' for k, t in [('agente_arriba', 'DISPARA ARRIBA'), ('agente_agachado', 'AGACHADO')])
        if o['n'] == 1:
            extra = '<div class="card"><img src="img/spr_narval.png"><span>NARVAL-1</span></div>'
        if o['n'] in (2, 3):
            extra = '<div class="card"><img src="img/spr_centinela.png"><span>CENTINELA-4</span></div>'
        A(f'''<section class="page">
<h2><small>Operación {o['n']} · al estilo de {o['ref']}</small>{o['name']}</h2>
<div class="g2">
<div style="display:flex;flex-direction:column;gap:3mm"><div class="g2" style="gap:3mm"><div class="shot"><img src="img/{o['a']}.png"></div><div class="shot"><img src="img/{o['b']}.png"></div></div>
<p><b>Objetivo:</b> {o['goal']} <b>Tú:</b> {o['you']}</p>
<ul>{''.join(f'<li>{t}</li>' for t in o['tips'])}</ul></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;align-content:start">{extra}{cards}</div>
</div>{foot()}</section>''')
    # memoria: arquitectura
    A(f'''<section class="page">
<h2><small>Memoria técnica · 1</small>Seis programas y un cargador</h2>
<div class="g2"><div style="display:flex;flex-direction:column;gap:3mm">
<p>El juego son <b>seis programas</b>: el título (0) y las cinco operaciones (1-5). Todos se cargan en <span class="mono">$2000</span> y cada uno tiene para él la RAM hasta <span class="mono">$BFFF</span> (con el BASIC fuera). Así cada operación tiene casi 40 KB de pantallas, carriles y búferes de sprites, sin compartir con las demás.</p>
<p>Entre programa y programa la partida viaja en un <b>bloque fijo en <span class="mono">$0580</span></b>: firma, amenaza, modo, fase, vuelta, puntos, vidas, próxima vida extra, selección del menú y los récords de los seis modos.</p>
<p>Un <b>cargador residente en <span class="mono">$0700-$087F</span></b> (entrada en <span class="mono">$0710</span>, A = programa) trae el siguiente. Hay tres cargadores con la misma entrada: disco (SIO), cartucho (bancos de 8 KB) y 130XE (memoria extendida). Los programas no saben de cuál vienen.</p>
<table><tr><th>Dirección</th><th>Uso</th></tr>
<tr><td class="m">$0000-$00FF</td><td>página cero: variables del motor y del programa</td></tr>
<tr><td class="m">$0580-$05A2</td><td>bloque compartido (partida, récords)</td></tr>
<tr><td class="m">$0600-$06FF</td><td>inicio del XEX / búfer del cargador 130XE</td></tr>
<tr><td class="m">$0700-$087F</td><td>cargador residente</td></tr>
<tr><td class="m">$2000-$9FFF</td><td>programa: juego de caracteres, código, datos y variables</td></tr>
<tr><td class="m">$A000-$BFFF</td><td>RAM de trabajo de cada programa: PMG, pantallas, display lists</td></tr></table>
</div><div style="display:flex;flex-direction:column;gap:3mm">
<h3>Tamaño de cada programa (páginas de 256 bytes)</h3>
<div class="bar"><div style="flex:83;background:#c9b77c">TÍTULO · 83</div><div style="flex:42;background:#8fb0d1">1 · 42</div><div style="flex:42;background:#9cc0a0">2 · 42</div><div style="flex:40;background:#c7a0c9">3 · 40</div><div style="flex:42;background:#d1b08f">4 · 42</div><div style="flex:43;background:#d19c8f;border-right:0">5 · 43</div></div>
<p style="font-size:8.2pt;color:var(--soft)">292 páginas en total (73 KB). El título es el mayor: la carátula convertida, el mapa de guerra, el logotipo y toda la música.</p>
<h3>Dónde está cada programa</h3>
<table><tr><th>Programa</th><th>Disco (sectores)</th><th>Cartucho</th><th>130XE (páginas virtuales)</th></tr>
<tr><td>0 Título</td><td class="m">4-86</td><td class="m">banco 1</td><td class="m">0-82</td></tr>
<tr><td>1 Mar Helado</td><td class="m">87-128</td><td class="m">banco 3</td><td class="m">83-124</td></tr>
<tr><td>2 Defensa SDI</td><td class="m">129-170</td><td class="m">banco 4</td><td class="m">125-166</td></tr>
<tr><td>3 Estación</td><td class="m">171-210</td><td class="m">banco 6</td><td class="m">167-206</td></tr>
<tr><td>4 Agente</td><td class="m">211-252</td><td class="m">banco 7</td><td class="m">207-248</td></tr>
<tr><td>5 JANUS</td><td class="m">253-295</td><td class="m">banco 8</td><td class="m">249-291</td></tr></table>
</div></div>{foot()}</section>''')
    # memoria: mapas por programa
    def tab(lst): return '<table><tr><th style="width:27mm">Programa</th><th>RAM de trabajo ($A000-$BFFF)</th></tr>' + ''.join(f'<tr><td><b>{nm}</b><br><span class="mono" style="font-size:7pt">{code}</span></td><td style="font-size:7.8pt">{"<br>".join(f"<span class=mono>{a}</span> {d}" for a, d in areas)}</td></tr>' for nm, code, areas in lst) + '</table>'
    rows = None
    A(f'''<section class="page">
<h2><small>Memoria técnica · 2</small>Mapa de memoria de cada programa</h2>
<div class="g2" style="gap:6mm">{tab(MEM_OPS[:3])}{tab(MEM_OPS[3:])}</div>
<p style="font-size:8pt;color:var(--soft)">Debajo de cada nombre, lo que ocupan el código, los datos y las variables a partir de $2000.</p>
<div class="note">Todas las operaciones usan el mismo motor (<span class="mono">src/motor/</span>): PMG con doble búfer que se redibuja entero cada cuadro, DLI por tablas, carriles con desplazamiento fino (un convoy entero se mueve con 3 bytes de LMS y un HSCROL), sonido POKEY con prioridades y caída por efecto, marcador y música. Encima va <span class="mono">comun.s</span>, el armazón de partida: vidas, mensajes, alarma de oleada, fase superada, paso a la siguiente operación y GAME OVER.</div>
{foot()}</section>''')
    # memoria: 130XE y cartucho
    A(f'''<section class="page">
<h2><small>Memoria técnica · 3</small>Un solo XEX para el 130XE</h2>
<div class="g2"><div style="display:flex;flex-direction:column;gap:3mm">
<p>Un XEX se lee una sola vez, de principio a fin; para volver al título tras el GAME OVER o a Mar Helado en la vuelta siguiente, todo tiene que quedarse en memoria. Los 73 KB del juego no caben en un Atari de 64 KB, pero sí en un 130XE:</p>
<ul><li>El XEX llega en trozos de 8 KB a <span class="mono">$2000-$3FFF</span>. Tras cada trozo, una rutina en <span class="mono">$0600</span> (INITAD) lo guarda en su sitio.</li>
<li>Las páginas virtuales 0-255 van a los <b>cuatro bancos de 16 KB</b> de la memoria extendida, que la CPU ve en <span class="mono">$4000-$7FFF</span> según PORTB.</li>
<li>Las 36 que sobran van a la <b>RAM que hay bajo el sistema operativo</b> (<span class="mono">$C000-$CFFF</span> y <span class="mono">$D800-$FFFF</span>), con las interrupciones paradas mientras se copian.</li>
<li>El último segmento lleva el cargador a <span class="mono">$2100</span>; al arrancar se copia a <span class="mono">$0700</span> (mientras se lee el fichero, ahí puede estar el DOS).</li>
<li>El cargador copia cada página a un búfer en <span class="mono">$0600</span> y de ahí a su destino: el banco se ve en <span class="mono">$4000-$7FFF</span>, justo donde también hay que escribir.</li>
<li>Lo primero que hace el XEX es comprobar que hay 128 KB. Si no, avisa en pantalla y se para.</li></ul>
</div><div style="display:flex;flex-direction:column;gap:3mm">
<h3>Memoria del 130XE con el juego cargado</h3>
<div class="bar"><div style="flex:64;background:#c9b77c">BANCO 0<br>título</div><div style="flex:64;background:#d8cfa6">BANCO 1<br>título · 1 · 2</div><div style="flex:64;background:#9cc0a0">BANCO 2<br>2 · 3 · 4</div><div style="flex:64;background:#c7a0c9">BANCO 3<br>4 · 5</div><div style="flex:36;background:#d19c8f;border-right:0">BAJO EL SO<br>5</div></div>
<h3 style="margin-top:2mm">Cartucho AtariMax 8 Mbit</h3>
<p>128 bancos de 8 KB que se ven en <span class="mono">$A000-$BFFF</span>. El banco 0 arranca, deja el cargador en <span class="mono">$0700</span> y prepara el bloque compartido. Los programas van seguidos desde el banco 1; el cargador copia sus páginas a <span class="mono">$2000</span> y desconecta el cartucho, para que <span class="mono">$A000-$BFFF</span> vuelva a ser RAM.</p>
<h3>Disco</h3>
<p>ATR de doble densidad (720 sectores de 256 bytes), sin DOS. El sistema carga 3 sectores de arranque en <span class="mono">$0700</span>; los programas ocupan los sectores 4-295 y se leen con el SIO del sistema.</p>
</div></div>{foot()}</section>''')
    # memoria del desarrollo
    A(f'''<section class="page">
<h2><small>Memoria del proyecto</small>Cómo se hizo</h2>
<div class="g2"><div style="display:flex;flex-direction:column;gap:2.5mm;font-size:8.6pt">
<p><b>Punto de partida.</b> El atlas visual y el documento de diseño de Tony C. Ware: cinco operaciones, cada una con su recreativa de referencia. Las especificaciones escritas se tomaron como orientativas; mandaron las referencias de juego.</p>
<p><b>Motor común.</b> Se reunió lo mejor de Vórtice 5, Vórtice 6 y Zak Attack en <span class="mono">motor/</span>: PMG redibujado entero en un búfer oculto, carriles con desplazamiento fino, DLI por tablas, sonido con prioridades. Queda en el banco de trabajo para los siguientes juegos.</p>
<p><b>Mar Helado.</b> Barcos hundidos en el agua (la superficie corta el casco), sonar en su propio canal, minas que te persiguen más en cada vuelta.</p>
<p><b>La pantalla de mando.</b> El menú inicial era feo. Se rehízo como el mando de JANUS (inspirado en la película WarGames): alarma, militarismo ochentero, DEFCON, teletipo y mapa de guerra propio.</p>
<p><b>Diseños elegidos por Tony.</b> Fase 2: CENTINELA-4 A, cazador B, artillero B, ICBM B. Fase 3: estación A, escolta C, cañón C. Fase 4: agente B; después, los Compuzoides de JANUS, todos A (androide, torreta, araña, ojo, pared de servidores, consola de cintas y disparos). Fase 5: pared C, bola A, emisor A.</p>
</div><div style="display:flex;flex-direction:column;gap:2.5mm;font-size:8.6pt">
<p><b>Separar en programas.</b> Para que cada operación tuviera toda la memoria, el juego se partió en seis programas con un cargador común; disco y cartucho comparten la interfaz.</p>
<p><b>Ajustes tras jugarlo.</b> Los misiles caen con el morro abajo y el ICBM se parte en tres en vueltas altas. La estación recibe daño en cualquier parte bajo la cinta abierta y desaparece entera al destruirla. El agente dispara hacia donde camina, con disparos rápidos que ya no parecen rebotar. Los tiradores miran hacia donde van y no se quedan clavados. Los emisores de JANUS recorren la cinta de lado a lado, se paran para disparar y cambian de sentido. La fase 4 pasa a ser una base de computadoras con los Compuzoides de JANUS (todo metal, leds que laten y brillos), y las balas de JANUS se distinguen de las tuyas. Más animación del agente. Fuera el truco.</p>
<p><b>Errores que costaron.</b> Puntos basura por dueños de columna viejos en el agua; un truco que chocaba con la navegación del menú; memoria sucia al cargar desde el título; variables temporales pisadas entre rutinas; restos de cinta que se redibujaban durante la fanfarria.</p>
<p><b>Pruebas.</b> Todo se probó en un emulador sin pantalla con guiones de mando, capturas y volcados de memoria. Las versiones de prueba se compilan con <span class="mono">-D PRUEBA</span> (invencible), <span class="mono">-D RAPIDA</span> (la cadena ARCADE entera en segundos), <span class="mono">-D VUELTA0</span> y <span class="mono">-D OLEADA0</span>.</p>
</div></div>{foot()}</section>''')
    # créditos
    A(f'''<section class="page dark" style="justify-content:center;align-items:center;text-align:center;gap:5mm">
<img src="img/caratula_oficial_pq.jpg" style="height:110mm;border-radius:1.5mm">
<p class="mono" style="font-size:10pt;letter-spacing:.14em;color:#fff">{SIGN}</p>
<p style="font-size:8.6pt;color:#c9ccd6;max-width:190mm">Diseño, historia, fases, carátula y dirección: Tony C. Ware. Programación 6502 (ca65), conversión de gráficos, música y documentación con asistencia de IA. Las recreativas citadas son referencias de estilo y pertenecen a sus dueños.</p>
{foot()}</section>''')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}</body></html>'

open('manual.html', 'w').write(manual())
open('atlas.html', 'w').write(atlas())
print('manual.html, atlas.html')
