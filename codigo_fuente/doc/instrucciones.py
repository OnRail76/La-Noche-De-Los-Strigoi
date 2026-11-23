#!/usr/bin/env python3
"""La Noche de los Strigoi · folleto de instrucciones ilustrado (A5) con la carátula oficial.
Uso: instrucciones.py salida.pdf"""
import sys
from comun import pagina, documento, a_pdf, img

S = 'La Noche de los Strigoi · Instrucciones'
n = [0]
def P(contenido, titulo, sub=None):
    n[0] += 1
    return pagina(contenido, titulo, sub, serie=S, pie_izq='2026 - TONY C. WARE', pie_der=str(n[0] + 1))

def cap(nombre, ley=None):
    return '<img class="pix" src="%s">%s' % (img(nombre + '.png'), '<div class="leyenda">%s</div>' % ley if ley else '')

EXTRA = r"""
.portada { background: #000; }
.portada .cuerpo { padding: 0; }
.portada img { width: 148mm; height: 210mm; object-fit: contain; object-position: center top; display: block; background: #000; }
.contra { background: #17121d; color: #eadfc8; }
.contra .cuerpo { padding: 14mm 12mm; }
.contra h2 { color: #c9a45a; }
.contra p { font-size: 8.4pt; }
.cuerpo { padding: 5mm 8mm 0; }
.cab { padding: 0 8mm; }
.pie { left: 8mm; right: 8mm; }
p, li { font-size: 7.9pt; }
"""

pags = []
# 1 · portada
pags.append('<section class="pg portada"><div class="cuerpo"><img src="%s"></div></section>' % img('caratula_oficial.jpg'))

# 2 · la leyenda
pags.append(P("""
<p class="cita">Sighișoara, Transilvania, 1847. Al caer la noche del solsticio de invierno, las campanas de la colina
anuncian una desgracia: los Strigoi han quebrado el sello del inframundo y regresan para reclamar la carne de los vivos.</p>
<p>Tras años de conflictos, la vida en la ciudadela y en las aldeas cercanas parecía haber recuperado la calma.
Ahora las familias cierran sus puertas, cuelgan ajos en los dinteles y aprietan cruces de madera.</p>
<p>Solo <b>Radu</b>, un haiduc de los Cárpatos, se atreve a cruzar el cementerio. Con su <b>baltag</b> y lo que sabe de
montañas y bosques, tendrá que llegar al <b>Trono de Sangre</b> y acabar con el señor de la noche antes de que amanezca.</p>
<div class="caja"><span class="et">El viaje</span>
<table>
<tr><td><b>1</b></td><td>El Cementerio de la Colina y la Escalera Cubierta</td></tr>
<tr><td><b>2</b></td><td>La Ciudadela y las Torres de los Gremios</td></tr>
<tr><td><b>3</b></td><td>Las Minas de Sal y las Criptas</td></tr>
<tr><td><b>4</b></td><td>El Paso de los Cárpatos</td></tr>
<tr><td><b>5</b></td><td>El Castillo del Trono de Sangre</td></tr>
</table></div>
<img class="foto" src="%s">
<div class="leyenda">La Escalera Cubierta, de noche. Ilustración de la preproducción.</div>
""" % img('escena_sighisoara.jpg'), 'La leyenda', 'Una noche que no debía llegar'))

# 3 · Radu
pags.append(P("""
<div class="g23"><div><img class="foto" src="%s"></div><div>
<p><b>Radu</b> es un forajido y héroe popular, como los haiducs que protegían a los pastores de los Cárpatos.</p>
<p>Viste una chaqueta de cuero forrada con piel de lobo, camisa de lino bordada, el cinturón ancho de los montañeses
(<i>brâu</i>) y un gorro de piel (<i>căciulă</i>).</p>
<p>Su arma es el <b>baltag</b>, el hacha de los pastores, que lanza y recupera una y otra vez.</p>
</div></div>
<h2 style="margin-top:3mm">Radu en tu Atari</h2>
%s
<div class="leyenda">Quieto, andando, saltando, lanzando el baltag y agachado.</div>
<div class="caja"><span class="et">La chaqueta de cuero</span>
<p>En <b>NORMAL</b>, Radu empieza cada vida con la chaqueta puesta: el primer golpe se la arranca y lo echa hacia atrás;
el segundo, sin chaqueta, le cuesta la vida. En <b>HARDCORE</b> no hay chaqueta: un golpe y fuera.</p></div>
""" % (img('ilus_fase5.jpg'), cap('radu_sprites')), 'Radu, el haiduc', 'El héroe de los Cárpatos'))

# 4 · cargar el juego
pags.append(P("""
<p>El juego viene en tres formatos. Todos son el mismo juego, con las mismas cinco fases, el título, el final y los récords.</p>
<table>
<tr><th>Formato</th><th>Fichero</th><th>Necesita</th></tr>
<tr><td><b>Cartucho</b><br>AtariMax 8 Mbit</td><td class="mono">strigoi.car</td><td>Atari XL/XE de 64 KB. La forma más cómoda: arranca sola y carga cada fase al instante</td></tr>
<tr><td><b>Disco</b><br>sin DOS</td><td class="mono">strigoi.atr</td><td>Atari XL/XE de 64 KB y una disquetera (o el emulador). Se arranca con el disco puesto; cada fase se lee al empezarla</td></tr>
<tr><td><b>XEX</b></td><td class="mono">Strigoi_130XE.xex</td><td>Atari 130XE (128 KB). Lo guarda todo en la memoria extendida al cargar. En un ordenador de 64 KB avisa y se para</td></tr>
</table>
<div class="caja"><span class="et">En el emulador</span>
<ul>
<li><b>Altirra:</b> sistema 800XL (64 KB) para el disco y el cartucho, o 130XE para el XEX. Arrastra el fichero a la ventana. El BASIC puede estar puesto o quitado: el juego lo desconecta.</li>
<li><b>atari800:</b> <span class="mono">atari800 -xl strigoi.atr</span>, <span class="mono">atari800 -xl strigoi.car</span> o <span class="mono">atari800 -xe Strigoi_130XE.xex</span>.</li>
<li>Vídeo <b>NTSC</b>: la música y la velocidad están pensadas para 60 cuadros por segundo.</li>
</ul></div>
<div class="caja"><span class="et">Cartuchos especiales</span>
<p>El <span class="mono">.car</span> funciona en cartuchos programables que aceptan imágenes AtariMax de 8 Mbit (tipo 42), y el
<span class="mono">.atr</span> o el <span class="mono">.xex</span> en lectores de tarjetas y emuladores de disquetera.</p></div>
""", 'Cargar el juego', 'Disco, cartucho o 130XE'))

# 5 · título y dificultad
pags.append(P("""
%s
<div class="g2"><div>
<h2>El título</h2>
<ul>
<li><b>Izquierda / derecha:</b> elige la dificultad.</li>
<li><b>FIRE:</b> empieza la partida.</li>
<li>Abajo se alternan el récord y los créditos.</li>
</ul></div><div>
<h2>Dificultad</h2>
<p><b>NORMAL:</b> cada vida empieza con la chaqueta de cuero.</p>
<p><b>HARDCORE:</b> sin chaqueta, y los últimos jefes aguantan más. Solo para haiducs de verdad.</p>
</div></div>
<div class="caja"><span class="et">El marcador</span>
<p>Arriba: <b>PUNTOS</b>, <b>RÉCORD</b> y las vidas que quedan (<b>RADU 3</b>). En los combates, la fila de estrellas es la vida que le
queda al jefe.</p>
<p>El récord se guarda mientras el Atari siga encendido.</p></div>
""" % cap('01_titulo', 'Sighișoara de noche: la ciudadela, la luna y Radu en su roca.'), 'Antes de empezar', 'La pantalla de título'))

# 6 · controles
pags.append(P("""
<table>
<tr><th style="width:34%%">Palanca</th><th>Qué hace Radu</th></tr>
<tr><td><span class="k">◄ ►</span></td><td>Anda a izquierda y derecha</td></tr>
<tr><td><span class="k">▲</span></td><td>Salta. Con izquierda o derecha a la vez, salta hacia ese lado</td></tr>
<tr><td><span class="k">▼</span></td><td>Se agacha: las esquirlas y los disparos altos le pasan por encima</td></tr>
<tr><td><span class="k">FIRE</span></td><td>Lanza el baltag en línea recta. Agachado, lo lanza a ras de suelo</td></tr>
</table>
<div class="g2"><div class="caja"><span class="et">Vidas y puntos</span>
<ul>
<li>Empiezas con <b>3 vidas</b>.</li>
<li><b>Vida extra</b> cada 20.000 puntos.</li>
<li>Criatura: <b>100</b>. La bruja: <b>1.000</b>.</li>
<li>Jefe derrotado: <b>bonificación 5.000</b>.</li>
</ul></div>
<div class="caja"><span class="et">Puntos de control</span>
<p>Cada tramo tiene un punto de control a mitad de camino. Si caes después de pasarlo, vuelves a empezar desde allí.</p>
<p>Si caes ante un jefe, vuelves a su guarida.</p></div></div>
<h2>Los peligros del camino</h2>
<table>
<tr><td><b>Agua negra y ríos helados</b></td><td>Caer en ellos es morir</td></tr>
<tr><td><b>Pinchos</b></td><td>Sostienen, pero hieren al pisarlos</td></tr>
<tr><td><b>Pasarelas y troncos</b></td><td>Se hunden si te quedas encima: cruza sin parar</td></tr>
<tr><td><b>Viento de los acantilados</b></td><td>Empuja a Radu hacia atrás</td></tr>
<tr><td><b>Fuegos fatuos</b></td><td>Si te tocan, cambian izquierda por derecha un buen rato</td></tr>
</table>
""", 'Controles', 'Una palanca y un botón'))

# 7-11 · las fases
FASES = [
 ('Fase 1', 'El Cementerio de la Colina', 'y la Escalera Cubierta', '03_fase1_cementerio', '04_fase1_escalera_cubierta',
  'Sepulturas, árboles nudosos y niebla bajo la luna. Después, la Escalera Cubierta sube hacia la parte alta de la ciudadela: de sus vigas se descuelgan los murciélagos.',
  [('Zombis', 'salen de la tierra y caminan hacia ti'), ('Cuervos', 'cruzan el cielo en picado'),
   ('Vâvâma', 'espíritus del bosque escondidos en los troncos: sacan una garra larga y vuelven a esconderse'),
   ('Murciélagos', 'caen de las vigas de la escalera')],
  'EL STRIGOI MORT', '05_jefe1_strigoi_mort',
  'Aparece y desaparece entre las tumbas y lanza ráfagas de viento helado con esquirlas: <b>agáchate</b> para que te pasen por encima. Con media vida se convierte en un <b>lobo</b> enorme que embiste: sáltalo y dale por la espalda.'),
 ('Fase 2', 'La Ciudadela', 'y las Torres de los Gremios', '07_fase2_ciudadela', None,
  'Callejones empedrados, tejados góticos y pasarelas de tablas entre las casas. Las pasarelas se hunden si te quedas quieto encima; la torre de los zapateros tiene un paso abierto a ras de calle.',
  [('Iele', 'espíritus del aire que giran a tu alrededor y cierran el círculo'),
   ('Gárgolas', 'despiertan en lo alto de las torres, caminan y escupen piedras'),
   ('Zombis', 'también rondan por la calle')],
  'ARIC, EL SASTRE DE LAS SOMBRAS', '08_jefe2_aric_el_sastre',
  'Flota en su taller, protegido por <b>seis retales encantados</b>: arráncalos uno a uno y luego golpea su cabeza. Lanza tijeras oxidadas que cruzan la sala y agujas de hierro que se clavan en el suelo. Sube a las mesas de corte para alcanzarlo.'),
 ('Fase 3', 'Las Minas de Sal', 'y las Criptas', '09_fase3_minas_de_sal', None,
  'Galerías de sal con agua negra en el fondo, puentes, repisas y criptas enterradas. Del techo cuelgan estalactitas de sal que se desprenden.',
  [('Moroi', 'apariciones que se desvanecen y vuelven a tomar cuerpo más cerca; solo se les puede dar cuando son sólidas'),
   ('Vâlva Băii', 'el espíritu de la mina: lanza picos en arco'),
   ('Estalactitas', 'caen cuando pasas por debajo')],
  'MUMA PĂDURII', '10_jefe3_muma_padurii',
  'La Madre del Bosque ocupa media galería. Golpea con su bastón y hace llover cristales de sal, hace brotar raíces espinosas y vomita enjambres de insectos. Su punto débil es la <b>cabeza</b>: alcánzala saltando desde la repisa alta.'),
 ('Fase 4', 'El Paso de los Cárpatos', 'bosque, nieve y empalados', '11_fase4_carpatos', None,
  'Bosque alpino nevado bajo la tormenta, entre las estacas del voivoda. Ríos helados con troncos que se hunden y acantilados donde el viento empuja hacia atrás.',
  [('Lupari', 'licántropos que corren a por ti y saltan cuando están cerca'),
   ('Fuegos fatuos', 'cambian los mandos si te tocan'),
   ('Cuervos de la tormenta', 'bajan en picado')],
  'EL CĂPCĂUN y EL REY STRIGOI', '12_jefe4_capcaun',
  'El <b>Căpcăun</b>, el ogro caníbal, golpea el suelo con su hueso: salta las ondas de choque y dale en la barriga. Cuando cae, llega el <b>Rey Strigoi</b> alado, con su corazón al descubierto como único punto débil.'),
 ('Fase 5', 'El Castillo', 'del Trono de Sangre', '15_fase5_castillo', None,
  'La fortaleza del señor de la noche: salones de piedra con vidrieras, esqueletos encadenados, cruces invertidas, fosos de pinchos y escalinatas.',
  [('Caballeros no muertos', 'armaduras que avanzan despacio; aguantan tres golpes'),
   ('Murciélagos', 'salen de las lámparas'),
   ('Pinchos', 'sostienen, pero hieren')],
  'LA CABEZA DEL REY STRIGOI', '16_jefe5_cabeza_del_rey',
  'El último combate. La cabeza gigante del Rey Strigoi lo dispara todo: proyectiles en arco, lluvias de cristales, murciélagos y enjambres. Solo se le hace daño <b>con la boca abierta</b>. Aguanta, espera el momento y apunta a la boca.'),
]
for (f, t1, t2, c1, c2, desc, enem, jefe, cj, tact) in FASES:
    li = ''.join('<li><b>%s:</b> %s.</li>' % e for e in enem)
    pags.append(P("""
<div style="width:70%%;margin:0 auto 1.5mm">%s</div>
<p>%s</p>
<div class="caja"><span class="et">Criaturas</span><ul>%s</ul></div>
<div class="caja osc"><span class="et">Jefe · %s</span>
<div class="g2"><div>%s</div><div><p>%s</p></div></div></div>
""" % (cap(c1), desc, li, jefe, '<img class="pix" src="%s">' % img(cj + '.png'), tact), '%s · %s' % (f, t1), t2))

# 12 · la tumba encantada
pags.append(P("""
%s
<p>Dicen que algunas tumbas no soportan que las molesten. Si golpeas <b>la misma tumba doce veces seguidas</b>, sale de ella una
<b>bruja</b>. Tienes un instante para darle; si no, lanza su hechizo.</p>
<ul>
<li>Si la alcanza el hechizo, Radu se convierte en <b>pollo</b> durante quince segundos.</li>
<li>Un pollo solo puede andar y saltar: no lanza, no se agacha y muere de un golpe.</li>
<li>Derribar a la bruja da <b>1.000 puntos</b>.</li>
</ul>
<div class="caja"><span class="et">Un homenaje</span>
<p>Es un guiño a un clásico de los recreativos con un caballero, un mago y una armadura que no duraba nada.</p></div>
""" % cap('homenaje', 'El pollo y la bruja, tal como salen en el juego.'), 'La tumba encantada', 'Un secreto del cementerio'))

# 13 · fin de partida
pags.append(P("""
<div class="g2"><div>%s</div><div>%s</div></div>
<p>Tras cada jefe, la pantalla de <b>fase superada</b> suma la bonificación y te lleva a la fase siguiente. Si vences al Rey
Strigoi, el castillo se derrumba y por fin amanece sobre Sighișoara.</p>
<p>Si pierdes la última vida, la calavera de Radu rueda por el suelo: <b>ha ganado la Noche</b>. Tras unos segundos, o al pulsar FIRE,
vuelves al título con tu récord.</p>
<div class="caja"><span class="et">Secreto del haiduc</span>
<p>En la pantalla de título, pulsa <span class="k">▼</span> <span class="k">▼</span> <span class="k">FIRE</span>. Si sale la palabra
<b>INVENCIBLE</b>, Radu no sufrirá daño en toda la partida. Úsalo para conocer el camino; la gloria se gana sin él.</p></div>
<div class="g2"><div>%s</div><div>%s</div></div>
""" % (cap('14_fase_superada', 'Fase superada.'), cap('23_game_over', 'Ha ganado la Noche...'),
       cap('18_amanecer', 'El amanecer, si llegas al final.'), cap('22_la_noche_ha_terminado', 'La noche ha terminado.')), 'El final de la noche', 'Fase superada, amanecer o GAME OVER'))

# 14 · créditos (contraportada)
pags.append("""<section class="pg contra"><div class="cuerpo">
<h2>La Noche de los Strigoi</h2>
<p>Programa para ordenadores Atari de 8 bits (XL/XE).<br>Disco, cartucho AtariMax 8 Mbit y XEX para 130XE.</p>
<p style="margin-top:8mm"><b>Concepto, guion y dirección:</b><br>Tony C. Ware</p>
<p><b>Programa, gráficos y música:</b><br>Tony C. Ware</p>
<p style="margin-top:8mm">Sighișoara, la Iglesia de la Colina, la Escalera Cubierta, la Torre del Reloj y las torres de los gremios
existen de verdad. Todo lo sobrenatural de este juego —los Strigoi, sus criaturas, el sello del inframundo y el Rey Strigoi— es ficción.</p>
<p style="margin-top:22mm; font: bold 13pt 'DejaVu Serif'; color:#c9a45a">2026 - TONY C. WARE</p>
</div></section>""")

a_pdf(documento(pags, 148, 210, EXTRA, 'La Noche de los Strigoi · Instrucciones'), 'instrucciones.html', sys.argv[1])
