#!/usr/bin/env python3
"""La Noche de los Strigoi · Atlas visual, memoria del proyecto y aprendizaje (A4).
Uso: atlas.py salida.pdf"""
import sys
from comun import pagina, documento, a_pdf, img

S = 'La Noche de los Strigoi · Atlas visual y memoria'
n = [0]
def P(contenido, titulo, sub=None):
    n[0] += 1
    return pagina(contenido, titulo, sub, serie=S, pie_izq='2026 - TONY C. WARE · Atlas visual · versión final', pie_der=str(n[0] + 1))
def cap(nombre, ley=None):
    return '<img class="pix" src="%s">%s' % (img(nombre if '.' in nombre else nombre + '.png'), '<div class="leyenda">%s</div>' % ley if ley else '')
def foto(nombre, ley=None, estilo=''):
    return '<img class="foto" style="%s" src="%s">%s' % (estilo, img(nombre), '<div class="leyenda">%s</div>' % ley if ley else '')
def caja(et, txt, osc=False):
    return '<div class="caja%s"><span class="et">%s</span>%s</div>' % (' osc' if osc else '', et, txt)

EXTRA = r"""
.portada { background: #0d0a10; }
.portada .cuerpo { padding: 0; }
.portada .arte { height: 240mm; width: auto; display: block; margin: 0 auto; }
.portada .banda { position: absolute; left: 0; right: 0; bottom: 0; height: 57mm; background: #0d0a10; border-top: 1.2mm solid #9e1b2b;
   padding: 7mm 14mm 0; color: #f3e6c8; }
.portada .banda .t1 { font: bold 9pt 'DejaVu Sans'; letter-spacing: .25em; color: #c9a45a; text-transform: uppercase; }
.portada .banda .t2 { font: bold 25pt 'DejaVu Serif'; margin: 2mm 0 1mm; }
.portada .banda .t3 { font: 10pt 'DejaVu Serif'; color: #d8c8a8; }
.mapa { display: flex; height: 13mm; border: .4mm solid #17121d; border-radius: 1mm; overflow: hidden; margin: 2mm 0 1mm; }
.mapa div { font: bold 5.6pt 'DejaVu Sans'; color: #fff; padding: 1mm; border-right: .3mm solid rgba(255,255,255,.5); overflow: hidden; line-height: 1.2; }
.esc { font: 5.6pt 'DejaVu Sans Mono'; color: #6a5844; display: flex; justify-content: space-between; margin-bottom: 3mm; }
.num { font: bold 20pt 'DejaVu Serif'; color: #9e1b2b; line-height: 1; }
.cifra { text-align: center; }
.cifra .num { display: block; }
.cifra span.l { font: 7pt 'DejaVu Sans'; color: #5a4a3a; }
.crono td:first-child { white-space: nowrap; font-weight: bold; color: #9e1b2b; width: 23mm; }
"""

pags = []
# ---------------------------------------------------------------- portada
pags.append("""<section class="pg portada"><div class="cuerpo"><img class="arte" src="%s">
<div class="banda"><div class="t1">Atari 8 bits · versión final</div><div class="t2">Atlas visual y memoria del proyecto</div>
<div class="t3">Del guion a la ROM: escenarios, criaturas, jefes, música, técnica, decisiones y lo aprendido por el camino</div>
<div class="t1" style="margin-top:6mm">2026 - Tony C. Ware</div></div></div></section>""" % img('caratula_oficial.jpg'))

# ---------------------------------------------------------------- ficha
pags.append(P("""
<div class="g3" style="margin-bottom:4mm">
<div class="caja cifra"><span class="num">5</span><span class="l">fases, 11 tramos y arenas</span></div>
<div class="caja cifra"><span class="num">7</span><span class="l">jefes (6 en el juego, 1 descartado)</span></div>
<div class="caja cifra"><span class="num">6</span><span class="l">temas musicales originales</span></div>
</div>
<div class="g2"><div>
<h2>Ficha del juego</h2>
<table>
<tr><td><b>Género</b></td><td>Acción y plataformas, avance lateral</td></tr>
<tr><td><b>Sistema</b></td><td>Atari XL/XE de 64 KB (disco y cartucho) · 130XE (XEX)</td></tr>
<tr><td><b>Vídeo</b></td><td>NTSC, 60 cuadros por segundo</td></tr>
<tr><td><b>Formatos</b></td><td>ATR sin DOS · CAR AtariMax 8 Mbit · XEX 130XE</td></tr>
<tr><td><b>Dificultad</b></td><td>NORMAL y HARDCORE</td></tr>
<tr><td><b>Créditos</b></td><td>2026 - Tony C. Ware</td></tr>
</table>
<h2>Índice</h2>
<table>
<tr><td>Un mundo real, una noche imposible</td><td>3</td></tr>
<tr><td>Radu: del concepto al sprite</td><td>4</td></tr>
<tr><td>Las cinco fases</td><td>5-9</td></tr>
<tr><td>Los jefes: del borrador al combate</td><td>10</td></tr>
<tr><td>Bestiario</td><td>11</td></tr>
<tr><td>Título, GAME OVER y final</td><td>12</td></tr>
<tr><td>Banda sonora</td><td>13</td></tr>
<tr><td>Arquitectura: memoria y formatos</td><td>14</td></tr>
<tr><td>Pantalla y color</td><td>15</td></tr>
<tr><td>Herramientas y pruebas</td><td>16</td></tr>
<tr><td>Del guion al juego</td><td>17</td></tr>
<tr><td>Memoria del proyecto</td><td>18-19</td></tr>
<tr><td>Aprendizaje</td><td>20-21</td></tr>
<tr><td>Referencias y créditos</td><td>22</td></tr>
</table>
</div><div>
%s
<h2 style="margin-top:3mm">En cifras</h2>
<table>
<tr><td>Programa residente</td><td>$4000-$8BCE · 19,4 KB</td></tr>
<tr><td>Módulos de fase</td><td>5 · de 3,8 a 7,6 KB cada uno, comprimidos</td></tr>
<tr><td>Tramos y arenas</td><td>14 paquetes LZ: de 94 KB a 26 KB</td></tr>
<tr><td>Disco</td><td>211 de 720 sectores</td></tr>
<tr><td>Cartucho</td><td>7 bancos de datos + arranque</td></tr>
<tr><td>Fuentes</td><td>43 ficheros de ensamblador, unas 22.000 líneas con los generadores</td></tr>
</table>
</div></div>
""" % cap('01_titulo', 'Pantalla de título del juego final.'), 'La Noche de los Strigoi', 'Ficha e índice'))

# ---------------------------------------------------------------- mundo real
pags.append(P("""
<div class="g32"><div>%s</div><div>
<h2>El núcleo</h2>
<p>Año <b>1847</b>, noche del solsticio de invierno. Los Strigoi quiebran el sello del inframundo y Sighișoara se encierra en sus casas.
Radu, un haiduc de los Cárpatos, cruza el cementerio con su baltag para llegar al Trono de Sangre.</p>
<h2>Realidad y ficción</h2>
<p>Sighișoara, el cementerio de la Iglesia de la Colina, la Escalera Cubierta, la Torre del Reloj y las torres de los gremios existen.
El universo sobrenatural, los jefes y la conexión entre los lugares son ficción. Las minas de sal se inspiran en las de Turda, que están
en otra localidad; su planta en el juego es fantástica.</p>
<p>El folclore rumano tiene muchas variantes: Strigoi, Moroi o Muma Pădurii no tienen una descripción única. Vâvâma y Lupari son
nombres del universo del juego.</p>
</div></div>
<h2>La ruta</h2>
<table>
<tr><th>Fase</th><th>Escenario</th><th>Criaturas</th><th>Jefe</th></tr>
<tr><td>1</td><td>Cementerio de la Colina y Escalera Cubierta</td><td>Zombis, cuervos, Vâvâma, murciélagos</td><td>Strigoi Mort (y su lobo)</td></tr>
<tr><td>2</td><td>Ciudadela y Torres de los Gremios</td><td>Iele, gárgolas, zombis</td><td>Aric, el Sastre de las Sombras</td></tr>
<tr><td>3</td><td>Minas de Sal y Criptas</td><td>Moroi, Vâlva Băii, estalactitas</td><td>Muma Pădurii</td></tr>
<tr><td>4</td><td>Paso de los Cárpatos</td><td>Lupari, fuegos fatuos, cuervos</td><td>Căpcăun y Rey Strigoi alado</td></tr>
<tr><td>5</td><td>Castillo del Trono de Sangre</td><td>Caballeros no muertos, murciélagos</td><td>La cabeza del Rey Strigoi</td></tr>
</table>
""" % foto('escena_sighisoara.jpg', 'Ilustración de preproducción: el cementerio y la Escalera Cubierta.'), 'Un mundo real, una noche imposible', 'Sighișoara, Transilvania, 1847'))

# ---------------------------------------------------------------- Radu
pags.append(P("""
<div class="g2"><div>%s</div><div>%s</div></div>
<div class="g2"><div>
<h2>Del concepto al sprite</h2>
<p>El primer modelo era grande y plano. En el juego, Radu son <b>dos jugadores superpuestos en modo OR</b>: tres colores (piel, camisa,
chaqueta y sombrero) en 8 píxeles de ancho, sin gastar caracteres del fondo.</p>
<p>El baltag es un quinto jugador hecho con los misiles: sale en línea recta, gira y vuelve. Agachado, Radu lo lanza a ras de suelo.</p>
<p>Su muerte es una calavera que cae y rebota, una petición expresa del autor, y la misma calavera protagoniza el GAME OVER.</p>
</div><div>
<h2>Reglas del héroe</h2>
<ul>
<li>3 vidas; vida extra cada 20.000 puntos.</li>
<li>En NORMAL, chaqueta de cuero: el primer golpe la arranca y empuja a Radu hacia atrás.</li>
<li>En HARDCORE, sin chaqueta; los jefes de las fases 4 y 5 aguantan 4 golpes más.</li>
<li>Puntos de control a mitad de cada tramo y a la entrada de cada arena.</li>
<li>Pollo durante 15 segundos si le alcanza el hechizo de la bruja.</li>
</ul>
</div></div>
%s
""" % (foto('radu_concepto.jpg', 'Hoja de poses de la preproducción.'), foto('ilus_fase5.jpg', 'Radu frente al señor de la noche. Arte de preproducción.'),
       cap('radu_sprites', 'Los sprites del juego: quieto, pasos, salto, lanzamiento y agachado (ampliados).')), 'Radu, el haiduc de los Cárpatos', 'Del concepto al sprite'))

# ---------------------------------------------------------------- fases
FASES = [
 ('1', 'El Cementerio de la Colina', 'portada_fase1.jpg', ['03_fase1_cementerio', '04_fase1_escalera_cubierta'],
  ['05_jefe1_strigoi_mort', '06_jefe1_mort_lobo'],
  """<p><b>Cementerio:</b> cielo fijo con luna y la Torre del Reloj, cordillera con desplazamiento a media velocidad y 13 filas de juego con
  desplazamiento fino. 110 caracteres de mapa, 56 de cielo, 96 de montañas.</p>
  <p><b>Escalera Cubierta:</b> tramo propio que sube hasta el borde de la pantalla (lo pidió así el autor); los murciélagos caen de las vigas.</p>
  <p><b>Strigoi Mort:</b> calavera con cuernos y sin cuello, se teletransporta entre tres tumbas y sopla viento helado con esquirlas a la altura de la
  cabeza: se esquivan agachándose. A media vida revienta y sale el lobo. Los murciélagos de su primera versión se quitaron: eran difíciles de matar.</p>""",
  'mapa_fase1.png', 'El tramo del cementerio completo, tal como lo genera gfx/fase1.py.'),
 ('2', 'La Ciudadela y las Torres de los Gremios', 'portada_fase2.jpg', ['07_fase2_ciudadela'], ['08_jefe2_aric_el_sastre'],
  """<p>Calle empedrada, casas de entramado y pasarelas que se hunden (clase 3: si Radu se queda encima un cuarto de segundo, la fila de tablas
  se borra del mapa). 123 de 127 caracteres: el tramo más lleno del juego.</p>
  <p>Las <b>gárgolas</b> perseguían a Radu y no había forma de sobrevivir: ahora caminan por los tejados y escupen piedras. Las <b>Iele</b> se
  rebajaron: menos y menos insistentes.</p>
  <p>En la revisión final, el callejón bajo la pasarela de la torre de los zapateros era una trampa sin salida para el invencible: la torre tiene ahora un
  paso abierto a ras de calle.</p>
  <p><b>Aric:</b> seis retales encantados le protegen la cabeza; tijeras que cruzan la sala y agujas que cierran el paso.</p>""",
  'ciu_hoja.png', 'Hoja de control del tramo: cuatro posiciones de cámara.'),
 ('3', 'Las Minas de Sal y las Criptas', 'portada_fase3.jpg', ['09_fase3_minas_de_sal'], ['10_jefe3_muma_padurii'],
  """<p>Galerías con techo de estalactitas, puentes, repisas y agua salada negra (mortal). 47 caracteres de mapa, 53 de techo y 96 de galería.</p>
  <p>Los <b>Moroi</b> se desvanecen y reaparecen más cerca: solo dañan, y solo se les puede dar, cuando son sólidos. La <b>Vâlva Băii</b>
  lanza picos en arco y las estalactitas tiemblan antes de caer.</p>
  <p><b>Muma Pădurii</b> ocupa un tercio de la pantalla: lluvia de cristales de sal, raíces espinosas e insectos. Su cabeza se alcanza desde
  la repisa alta. En el suelo de su arena, el modo invencible se queda atrapado; en partida normal, caer allí es morir, y así se quedó.</p>""",
  'min_hoja.png', 'Hoja de control de las minas.'),
 ('4', 'El Paso de los Cárpatos', 'portada_fase4_balaur.jpg', ['11_fase4_carpatos'], ['12_jefe4_capcaun', '13_jefe4b_rey_strigoi'],
  """<p>Bosque alpino nevado, acantilados con viento que empuja hacia atrás, ríos helados con troncos que se hunden. En la revisión final se
  añadieron los <b>empalados del voivoda</b>: siete estacas junto al camino, con el cuerpo en granate oscuro, y una hilera de estacas en silueta en la cordillera.</p>
  <p>La ilustración de preproducción muestra al <b>Balaur</b>, el dragón de tres cabezas del guion. Se descartó (al autor le pareció feo) y en su lugar
  llegaron el <b>Căpcăun</b>, un ogro caníbal horrendo con un hueso enorme y empalados al fondo, y el <b>Rey Strigoi</b> alado.</p>""",
  'car_hoja.png', 'Hoja de control de los Cárpatos, con los empalados.'),
 ('5', 'El Castillo del Trono de Sangre', 'ilus_fase5.jpg', ['15_fase5_castillo'], ['16_jefe5_cabeza_del_rey'],
  """<p>Salones con bóvedas y lámparas, vidrieras de colores en la capa intermedia, pilares, antorchas y fosos de pinchos. Muros con
  <b>esqueletos encadenados y cruces invertidas de hierro</b>, añadidos en la revisión final con el quinto color.</p>
  <p>Los <b>caballeros no muertos</b> aguantan tres golpes. El jefe final es la <b>cabeza gigante del Rey Strigoi</b>, homenaje al jefe final de
  Crossbow: lo dispara todo y solo se le hace daño con la boca abierta.</p>
  <p>Al vencerla, el castillo se derrumba, amanece sobre Sighișoara y pasan los créditos.</p>""",
  'cas_hoja.png', 'Hoja de control del castillo.'),
]
for (num, nom, arte, caps, jefes, notas, hoja, lhoja) in FASES:
    cc = ''.join('<div>%s</div>' % cap(c, 'Jefe.' if c in jefes else None) for c in caps + jefes)
    pags.append(P("""
<div class="g23"><div>%s</div><div><h2>Notas de diseño</h2>%s</div></div>
<h2>En el juego</h2>
<div class="g3">%s</div>
<div style="margin-top:1mm"><img class="pix" style="width:auto;max-width:100%%;max-height:44mm" src="%s"><div class="leyenda">%s</div></div>
""" % (foto(arte, 'Arte de preproducción.' if 'balaur' not in arte else 'Arte de preproducción con el Balaur, descartado.', 'max-height:92mm;object-fit:cover;object-position:top'),
       notas, cc, img(hoja), lhoja), 'Fase %s · %s' % (num, nom)))

# ---------------------------------------------------------------- jefes
pags.append(P("""
<p>El autor quería ver los jefes dibujados antes de programarlos: «siempre son todos muy blocky». Cada jefe se pintó primero como un borrador a
tamaño real, con los colores y el número de caracteres que iba a tener, y solo después se programó. Todos mueren de forma espectacular:
explosiones, destellos y escombros.</p>
<div class="g3">
<div>%s</div><div>%s</div><div>%s</div>
<div>%s</div><div>%s</div><div>%s</div>
</div>
<div class="g32"><div>%s</div><div>
<h2>El motor de jefes genérico</h2>
<p>Los tres últimos jefes comparten un mismo motor: un bloque de 32 bytes describe el jefe (gráficos, punto débil, vida, colores) y una lista de
ataques lo anima: lluvia de cristales, arcos, enjambre, onda de choque, murciélagos y boca abierta.</p>
<p>Así, el Căpcăun, el Rey Strigoi y la cabeza caben en módulos de 0,3 y 0,6 KB de código.</p>
</div></div>
""" % (cap('jefe1_borrador', 'Strigoi Mort.'), cap('jefe2_borrador', 'Aric, el Sastre de las Sombras.'), cap('jefe3_borrador', 'Muma Pădurii.'),
       cap('jefe7_borrador', 'Căpcăun.'), cap('jefe5_borrador', 'Rey Strigoi alado.'), cap('jefe6_borrador', 'La cabeza del Rey Strigoi.'),
       cap('jefe4_borrador', 'El Balaur: dibujado, y descartado.')), 'Los jefes', 'Del borrador al combate'))

# ---------------------------------------------------------------- bestiario
pags.append(P("""
%s
<table>
<tr><th>Criatura</th><th>Fase</th><th>Comportamiento</th><th>Golpes</th></tr>
<tr><td>Zombi</td><td>1, 2</td><td>Sale de la tierra y camina hacia Radu</td><td>1</td></tr>
<tr><td>Cuervo</td><td>1, 4</td><td>Cruza en picado</td><td>1</td></tr>
<tr><td>Vâvâma</td><td>1</td><td>Espera en el tronco, saca un zarpazo de 36 píxeles y vuelve</td><td>1</td></tr>
<tr><td>Murciélago</td><td>1, 5</td><td>Cae de las vigas o de las lámparas y revolotea</td><td>1</td></tr>
<tr><td>Iele</td><td>2</td><td>Gira alrededor de Radu cerrando el círculo y se marcha; solo una a la vez</td><td>1</td></tr>
<tr><td>Gárgola</td><td>2</td><td>Camina por los tejados y escupe piedras</td><td>2</td></tr>
<tr><td>Moroi</td><td>3</td><td>Se desvanece y reaparece más cerca; tres apariciones y se va</td><td>1</td></tr>
<tr><td>Vâlva Băii</td><td>3</td><td>Lanza picos en arco</td><td>2</td></tr>
<tr><td>Estalactita</td><td>3</td><td>Tiembla y cae cuando Radu pasa debajo</td><td>—</td></tr>
<tr><td>Lupari</td><td>4</td><td>Corre hacia Radu sin despeñarse y salta cuando está cerca</td><td>1</td></tr>
<tr><td>Fuego fatuo</td><td>4</td><td>Cambia izquierda por derecha si te toca</td><td>1</td></tr>
<tr><td>Caballero no muerto</td><td>5</td><td>Avanza despacio sin caerse de las plataformas</td><td>3</td></tr>
<tr><td>Bruja (homenaje)</td><td>1</td><td>Sale tras 12 golpes a una tumba; su hechizo convierte a Radu en pollo</td><td>1</td></tr>
</table>
<div class="g2"><div>%s</div><div>%s</div></div>
""" % (cap('bestiario_sprites', 'Sprites de las criaturas (jugadores 2 y 3), ampliados con su color del juego.'),
       cap('fase1_enemigos', 'Fase 1: zombis, cuervos, murciélagos, baltag y destellos.'), cap('homenaje', 'Pollo y bruja: el homenaje a Ghosts\'n Goblins.')),
 'Bestiario', 'Dos huecos de enemigo en pantalla, criaturas de todas las fases'))

# ---------------------------------------------------------------- pantallas
pags.append(P("""
<div class="g2"><div><h2>Boceto</h2>%s</div><div><h2>En el juego</h2>%s</div></div>
<div class="g2"><div>%s</div><div>%s</div></div>
<h2>El final</h2>
<div class="g3"><div>%s</div><div>%s</div><div>%s</div></div>
<p>El autor eligió el logo A (letras góticas rojas que gotean), el título 1 (Sighișoara de noche con la luna y Radu en la roca) y el GAME OVER 1,
con la frase «Ha ganado la Noche...». El final propuesto se aceptó tal cual: derrumbe del castillo, amanecer con el cielo pasando de la noche al día
en tres pasos de paleta, tres páginas de créditos y la pantalla de puntos antes de volver al título. Nunca entra el modo de demostración.</p>
""" % (cap('boceto_titulo', 'Bocetos de logo y título.'), cap('01_titulo'), cap('boceto_gameover', 'Boceto del GAME OVER.'),
       cap('23_game_over', 'La calavera cae, rebota dos veces y se queda.'), cap('17_derrumbe_del_castillo', 'Derrumbe.'),
       cap('18_amanecer', 'Amanecer.'), cap('21_creditos_autor', 'Créditos.')), 'Título, GAME OVER y final', 'De los bocetos a la pantalla'))

# ---------------------------------------------------------------- música
pags.append(P("""
<p>Seis temas originales para el reproductor de cuatro voces del banco de trabajo. Los canales 2 y 3 se reservan a los efectos, que pisan
la música cuando suenan.</p>
<table>
<tr><th>Tema</th><th>Dónde suena</th><th>Inspiración aportada por el autor</th><th>Carácter</th></tr>
<tr><td>Título</td><td>Pantalla de título</td><td>«Title» de Ghouls'n Ghosts</td><td>Fa sostenido menor, introducción de 4 compases y bucle</td></tr>
<tr><td>Fase A</td><td>Cementerio, Ciudadela, Cárpatos</td><td>«Ground BGM»</td><td>Melodía de marcha, ligera</td></tr>
<tr><td>Fase B</td><td>Escalera, Minas, Castillo</td><td>«Cave BGM»</td><td>Más grave y misteriosa</td></tr>
<tr><td>Jefes</td><td>Las seis arenas</td><td>«Theme of Satan»</td><td>Tensión con bajo insistente</td></tr>
<tr><td>Final</td><td>Amanecer y créditos</td><td>«High Score» de Ghouls'n Ghosts</td><td>Sol sostenido menor que acaba en mayor</td></tr>
<tr><td>GAME OVER</td><td>Calavera de Radu</td><td>«Game Over» de Ghouls'n Ghosts</td><td>Mi menor, 4 compases y silencio</td></tr>
</table>
%s
%s
""" % (caja('Las referencias inspiran, no se copian',
            '<p>Todas las melodías son nuevas. De las referencias se tomaron el tempo, el modo y el carácter; ni una frase.</p>'),
       caja('Lo que pidió el autor',
            '<p>La primera versión le pareció <b>demasiado ruidosa y atonal</b>: no dejaba oír los efectos. Se rehízo todo más melódico, suave y sencillo, '
            '«más de juego», sin batería y con menos notas por compás. Esa es la regla que se aplicó a los seis temas.</p>', True)
       + '<h2>Grabaciones del paquete</h2><table><tr><th>Fichero</th><th>Duración</th></tr>'
       + ''.join('<tr><td class="mono">banda_sonora/%s.mp3</td><td>%s</td></tr>' % t for t in (
           ('01_titulo', '1:02'), ('02_tema_de_fase_A', '1:18'), ('03_tema_de_fase_B', '1:18'), ('04_jefes', '1:10'),
           ('05_final', '1:02'), ('06_game_over', '0:14')))
       + '</table><p>Grabadas del emulador (libatari800, NTSC) a 44,1 kHz, sin retoques: es lo que suena en el Atari.</p>'),
 'Banda sonora', 'POKEY a cuatro voces, seis temas'))

# ---------------------------------------------------------------- arquitectura
MAPA = [('#3a3446', 2, '$0000 página cero, pila, SO'), ('#7a5a2a', 1, '$2000 fuente'),
        ('#2f6b4f', 7.5, '$2200-$3FFF tramo, arena o pantalla (superpuestos)'), ('#9e1b2b', 19, '$4000-$8BFF programa residente'),
        ('#c9a45a', 3, '$8C00 módulo de la fase'), ('#555', 1, '$9800 variables'), ('#334f7a', 1, '$9C00 cargador'),
        ('#4a3a6a', 8, '$A000-$BFFF jugadores, anillos de pantalla, listas de display'), ('#6b2f2f', 4, '$C000 paquetes de la fase (bajo el SO)'),
        ('#222', 2, '$D000 chips'), ('#6b2f2f', 10, '$D800-$FFF9 paquetes, título y GAME OVER (bajo el SO)')]
mapa = '<div class="mapa">%s</div>' % ''.join('<div style="background:%s;flex:%s">%s</div>' % m for m in MAPA)
pags.append(P("""
<h2>Mapa de memoria</h2>
%s
<div class="esc"><span>$0000</span><span>$4000</span><span>$8000</span><span>$C000</span><span>$FFFF</span></div>
<div class="g2"><div>
<h3>Superpuestos y compresión</h3>
<p>Cada tramo (cielo, dos juegos de caracteres, mapa de 13 páginas y tablas) y cada arena ocupan la misma zona de 7,5 KB en $2200. Se guardan
comprimidos con un LZ propio (<span class="mono">tools/lz.py</span> y <span class="mono">lz_unpack</span>) en la RAM que hay bajo el sistema
operativo y se descomprimen al entrar, con el SO y las NMI apagados.</p>
<h3>Módulos de fase</h3>
<p>El código de cada fase (sus enemigos y su jefe) es un módulo de hasta 3 KB que se carga en $8C00. Un módulo es una lista de registros
<i>destino, longitud, datos</i> que termina con un destino 0: su código y sus paquetes comprimidos.</p>
</div><div>
<table>
<tr><th>Módulo</th><th>Código</th><th>Imagen</th><th>Contenido</th></tr>
<tr><td>1</td><td>1.657</td><td>7.594</td><td>Cementerio, Escalera, Mort</td></tr>
<tr><td>2</td><td>1.729</td><td>5.707</td><td>Ciudadela, Aric</td></tr>
<tr><td>3</td><td>1.338</td><td>5.029</td><td>Minas, Muma</td></tr>
<tr><td>4</td><td>282</td><td>6.935</td><td>Cárpatos, Căpcăun, Rey</td></tr>
<tr><td>5</td><td>623</td><td>3.840</td><td>Castillo, cabeza, final</td></tr>
</table>
<p class="leyenda">Tamaños en bytes. Los 14 paquetes pasan de 94 KB a 26 KB.</p>
</div></div>
<h2>Un formato, tres soportes</h2>
<table>
<tr><th>Soporte</th><th>Dónde viven los módulos</th><th>Cómo se cargan</th></tr>
<tr><td><b>XEX 130XE</b></td><td>Bancos de memoria extendida (2 de 4)</td><td>Al cargar el XEX, segmentos INIT los copian a los bancos; al empezar una fase se copian a su sitio. Sin 128 KB, aviso y alto</td></tr>
<tr><td><b>ATR</b></td><td>Sectores de 256 bytes desde el sector 6</td><td>3 sectores de arranque leen el cargador; este lee cada sector con el SIO y lo analiza con el SO fuera</td></tr>
<tr><td><b>CAR</b></td><td>Bancos 1-7 de un AtariMax 8 Mbit</td><td>El banco 0 (copiado en el 127) pone el cargador en $9C00; se lee página a página y el cartucho se desconecta al acabar</td></tr>
</table>
<p>El arranque usa el mismo lector para un «módulo 0» con la fuente, el programa residente y los paquetes fijos. El programa residente es idéntico en
los tres soportes: solo cambia el cargador de $9C00, con <span class="mono">mod_load</span> siempre en la misma dirección.</p>
""" % mapa, 'Arquitectura', 'Memoria, módulos y formatos'))

# ---------------------------------------------------------------- pantalla y color
pags.append(P("""
<div class="g2"><div>
<h2>La pantalla del juego</h2>
<ul>
<li>Marcador en ANTIC 2; cielo fijo de 4 filas; cordillera de 3 filas con desplazamiento a media velocidad; una fila vacía; 13 filas de juego en
ANTIC 4 con desplazamiento fino. Cada fila de juego lee de un anillo de 128 bytes: avanzar es cambiar 13 direcciones en la VBI.</li>
<li>Una interrupción de lista de display (DLI) por fila cambia el juego de caracteres, el desplazamiento fino y los cinco colores: 22 entradas por tabla.</li>
<li>Radu, dos enemigos y el baltag son jugadores y misiles; el resto, caracteres.</li>
</ul>
<h2>El quinto color</h2>
<p>En ANTIC 4 un carácter invertido pinta sus píxeles «11» con COLPF3 en lugar de COLPF2. Los empalados (granate oscuro), sus siluetas lejanas
(negras) y los huesos de los esqueletos usan caracteres invertidos: un color más por fila sin quitar ninguno a la roca, la nieve o los pinos. El motor
enmascara el bit 7 al consultar la clase de la casilla, así que la decoración no se pisa.</p>
</div><div>
%s
%s
</div></div>
%s
""" % (cap('11_fase4_carpatos', 'Cárpatos: empalados en PF3 y estacas lejanas en la cordillera.'),
       cap('15_fase5_castillo', 'Castillo: esqueletos y cruces de hierro con el mismo truco.'),
       caja('La lección de la DLI',
            '<p>En la revisión final aparecieron líneas que parpadeaban al hacer scroll (como el amarillo sobre el empedrado). La última línea de una fila ANTIC 4 '
            'ancha deja a la CPU a media velocidad; la DLI llegaba a veces tarde a WSYNC y la primera línea de la fila siguiente salía con los colores viejos. '
            'Se dejó lo mínimo antes de WSYNC (guardar A y X en página cero, leer el índice), después el juego de caracteres y los colores más visibles, y '
            'el desplazamiento fino al final, con una tabla que ya trae el valor de la fila siguiente. Medido en 300 cuadros: de 223 fallos a ninguno.</p>', True)),
 'Pantalla y color', 'ANTIC, DLI y un color de más'))

# ---------------------------------------------------------------- herramientas
pags.append(P("""
<h2>Del dibujo al disco</h2>
<table>
<tr><th>Paso</th><th>Herramienta</th><th>Qué hace</th></tr>
<tr><td>1</td><td><span class="mono">gfx/*.py</span></td><td>Escenarios, jefes y sprites dibujados en texto; generan juegos de caracteres, mapas, clases de colisión, apariciones y tablas de color. Avisan si un juego pasa de 127 caracteres o un texto no cabe</td></tr>
<tr><td>2</td><td><span class="mono">tools/musica.py</span></td><td>Compone y empaqueta los seis temas</td></tr>
<tr><td>3</td><td><span class="mono">build.sh</span></td><td>Dos pasadas de ca65/ld65: la segunda ya conoce dónde caen los paquetes comprimidos</td></tr>
<tr><td>4</td><td><span class="mono">tools/modulos.py</span></td><td>Comprime, reparte en módulos y coloca bajo el SO y en los bancos</td></tr>
<tr><td>5</td><td><span class="mono">mkxex.py · mkmedio.py</span></td><td>XEX 130XE, ATR y CAR</td></tr>
<tr><td>6</td><td><span class="mono">build_all.sh</span></td><td>Los tres formatos y las versiones de prueba, idénticos byte a byte en cada construcción</td></tr>
</table>
<h2>Pruebas sin manos</h2>
<div class="g2"><div>
<ul>
<li><b>libatari800</b> sin pantalla, con bots en C que leen la memoria del juego por nombre de etiqueta.</li>
<li><b>walk8:</b> recorre cualquier tramo saltando; con variables de entorno elige máquina (XL o XE), dificultad, fuego automático o silencio, y graba el sonido.</li>
<li><b>bot8 a bot11:</b> uno por jefe; esquivan sus ataques leyendo su estado y le dan hasta vencerlo.</li>
</ul></div><div>
<ul>
<li><b>Versiones de prueba:</b> <span class="mono">PRUEBA</span> (invencible), <span class="mono">FASEn_TEST</span> (empieza en la fase n), <span class="mono">ARENA_TEST</span> (directo al jefe), <span class="mono">MUS_TEST</span> (el título toca otro tema).</li>
<li><b>Métricas:</b> píxeles de la primera línea de cada fila con colores de la fila anterior (para la DLI), bajas del jefe, avance por columnas.</li>
</ul></div></div>
<h2>Lo comprobado en la versión final</h2>
<ul>
<li>Disco y cartucho arrancan en XL de 64 KB y en 130XE; el XEX en 130XE.</li>
<li>Cada jefe vencido carga la fase siguiente desde disco y cartucho (Mort → 2, Aric → 3, Muma → 4, Căpcăun → Rey → 5).</li>
<li>Varias partidas seguidas: GAME OVER, título y fase 1 de nuevo, recargando el módulo.</li>
<li>Las cinco fases se recorren enteras; el final completo vuelve al título.</li>
</ul>
""", 'Herramientas y pruebas', 'Cómo se hizo y cómo se comprobó'))

# ---------------------------------------------------------------- del guion al juego
pags.append(P("""
<p>El guion canónico revisado es la base. El juego lo sigue en lo esencial y cambia donde el autor lo decidió al ver los bocetos o al jugar.</p>
<table>
<tr><th style="width:24%%">Elemento</th><th style="width:38%%">Guion</th><th>Juego final</th></tr>
<tr><td>Strigoi Mort</td><td>Teletransporte, murciélagos, viento helado; lobo a media vida</td><td>Igual, sin murciélagos. Calavera con cuernos, sin cuello</td></tr>
<tr><td>Aric</td><td>Tijeras oxidadas, agujas de hierro, escudo de telas</td><td>Igual: seis retales que hay que arrancar antes de la cabeza</td></tr>
<tr><td>Muma Pădurii</td><td>Cristales, estalactitas, raíces, insectos</td><td>Igual; la cabeza se alcanza desde la repisa alta</td></tr>
<tr><td>Jefe de la fase 4</td><td>El Balaur, dragón de tres cabezas</td><td>Descartado. Căpcăun (jefe extra pedido por el autor) y el Rey Strigoi alado</td></tr>
<tr><td>Jefe final</td><td>El Rey Strigoi, quimera alada</td><td>El Rey Strigoi pasa a la fase 4; el final es su cabeza gigante (homenaje a Crossbow)</td></tr>
<tr><td>Fase 5</td><td>Versiones reducidas de jefes, caballeros de élite</td><td>Caballeros no muertos de tres golpes, murciélagos, pinchos</td></tr>
<tr><td>Lupari</td><td>Trepan por los árboles</td><td>Corren hacia Radu y saltan</td></tr>
<tr><td>Arsenal</td><td>Baltag, daga, lanza, agua bendita, cruz</td><td>Solo el baltag, que se lanza y vuelve</td></tr>
<tr><td>Homenaje</td><td>—</td><td>La tumba de los doce golpes, la bruja y el pollo</td></tr>
<tr><td>Decorado</td><td>—</td><td>Empalados en los Cárpatos; esqueletos y cruces invertidas en el castillo</td></tr>
</table>
<div class="g2"><div>%s</div><div>%s</div></div>
""" % (foto('portada_fase4_balaur.jpg', 'Portada de preproducción de la fase 4, con el Balaur.', 'height:96mm;object-fit:cover'),
       cap('12_jefe4_capcaun', 'El jefe que lo sustituyó: el Căpcăun, con empalados al fondo.') + cap('13_jefe4b_rey_strigoi', 'Y el Rey Strigoi alado.')),
 'Del guion al juego', 'Qué se mantuvo y qué cambió'))

# ---------------------------------------------------------------- memoria del proyecto
CRONO = [
 ('Fase 1', 'El autor quiso empezar viendo el cementerio jugable; le encantó. Aprobó la lista de enemigos por fase (con cuervos y murciélagos de las vigas) y el orden de trabajo: primero los enemigos de todas las fases, después los jefes.'),
 ('Homenaje', 'Pidió el guiño a Ghosts\'n Goblins: muchos golpes a una tumba hacen salir una bruja que convierte a Radu en pollo amarillo durante 15 segundos; el hechizo debe ser rápido.'),
 ('Jefes', 'Quiso ver los jefes dibujados antes de programarlos. Descartó el Balaur; el Rey Strigoi pasó a la fase 4 y el final sería su cabeza gigante, al estilo de Crossbow, «sí o sí». Añadió el Căpcăun: horrendo, gigante, con un hueso y empalados al fondo.'),
 ('Mort', 'Sin cuello largo, cabeza de calavera con cuernos. Después, sin murciélagos: solo viento y lobo, reto suficiente para el primer jefe. Los jefes deben morir de forma espectacular.'),
 ('Escalera', 'La Escalera Cubierta debe llegar hasta el borde de la pantalla.'),
 ('Memoria', 'Se resuelve como en SDI \'86 y Vórtice 6: módulos por fase, compresión y tres formatos (ATR, XEX y CAR). Se jugará casi siempre en emulador o en un cartucho programable.'),
 ('Fase 2', 'Le gustó. Las gárgolas debían caminar y disparar en vez de perseguir; las Iele, menos insistentes. Se corrigió «GREMIO» por «TORRES DE GREMIOS» (el texto se cortaba sin avisar).'),
 ('Música', 'Temas de fase inspirados en sus «Ground BGM» y «Cave BGM», jefes en «Theme of Satan». La primera versión era ruidosa y atonal: se rehízo melódica, suave y sencilla, dejando oír los efectos.'),
 ('Título', 'Ideas de logo, título y GAME OVER: eligió el logo A, el título 1 y el GAME OVER 1 con «Ha ganado la Noche...». Aportó temas de Ghouls\'n Ghosts para título, final y GAME OVER.'),
 ('Final', 'Aceptó la propuesta: derrumbe del castillo, amanecer, créditos, puntos y vuelta al título. Selector NORMAL/HARDCORE; el truco abajo, abajo, FIRE; créditos «2026 - TONY C. WARE».'),
 ('Revisión', 'Encontró un callejón sin salida en la Ciudadela (arreglado con un paso en la torre), parpadeos de color al hacer scroll (arreglados en la DLI) y un foso en la arena de Muma que solo atrapa al invencible (se quedó así).'),
 ('Decorados', 'Pidió empalados «del gusto del señor Tepes» y, en el castillo, cruces invertidas y esqueletos. Eligió las opciones C y E; los empalados en gris «parecían churros» y se rehicieron en granate.'),
 ('Versión final', 'Paquete con el juego en tres formatos, banco de trabajo, banda sonora, fuentes, instrucciones ilustradas y este atlas, partiendo del dossier de preproducción, la carátula oficial y el guion canónico.'),
]
filas = ''.join('<tr><td>%s</td><td>%s</td></tr>' % c for c in CRONO)
pags.append(P("""
<p>Cómo se tomaron las decisiones, en el orden en que llegaron. Casi todas salieron de ver el juego funcionando o un boceto sobre una captura real.</p>
<table class="crono">%s</table>
""" % filas, 'Memoria del proyecto', 'Las decisiones del autor, paso a paso'))

pags.append(P("""
<div class="g2"><div>
<h2>Forma de trabajo</h2>
<ul>
<li><b>Ver antes de construir.</b> Cada jefe, pantalla o decorado se enseñó primero como boceto sobre una captura del juego y con los colores
que la fila permite. Así el autor eligió entre opciones reales y no imaginadas.</li>
<li><b>Fase a fase.</b> Una fase jugable de principio a fin, revisada por el autor, antes de pasar a la siguiente; las correcciones se aplicaban
al momento y se volvían a probar con los bots.</li>
<li><b>Reglas de la casa.</b> La dificultad difícil se llama siempre HARDCORE; nunca hay modo de demostración; el GAME OVER muestra la puntuación y vuelve al título;
los créditos dicen «2026 - TONY C. WARE»; el paquete final no lleva scripts de publicación.</li>
</ul>
<h2>Material de partida</h2>
<ul>
<li><b>Guion canónico revisado</b> (sinopsis, Radu, cinco fases y jefes, nota sobre realidad y ficción).</li>
<li><b>Atlas visual de preproducción</b> (35 páginas): portadas por fase, ilustraciones, siluetas de jefes, paletas y objetivos técnicos.</li>
<li><b>Carátula oficial para imprimir</b>, que abre este atlas y el folleto de instrucciones.</li>
<li><b>Bibliografía y criterios</b>, con los límites de la adaptación.</li>
</ul>
<p>De la preproducción a la ROM cambió lo que el juego pidió: el arsenal se redujo al baltag, el Balaur dejó su sitio al Căpcăun y el Rey Strigoi
se partió en dos combates.</p>
</div><div>
<h2>Bocetos de la revisión final</h2>
%s
%s
</div></div>
""" % (cap('boceto_empalados_granate.png', 'Boceto de los empalados en granate, la opción elegida, sobre la fase real.'),
       cap('boceto_castillo_E.png', 'Boceto E del castillo: esqueletos encadenados y cruz de hierro.')), 'Memoria del proyecto', 'Cómo se trabajó'))

# ---------------------------------------------------------------- aprendizaje
APR = [
 ('Saltos relativos a mano', 'Un <span class="mono">bcs *+4</span> que debía ser <span class="mono">*+3</span> caía en mitad de una instrucción y volvía locos los ataques del motor de jefes. Se revisaron todos los <span class="mono">*+N</span> del código (también un <span class="mono">beq *+6</span> del rebote en el agua). Mejor etiquetas locales que contar bytes.'),
 ('Textos que se cortan solos', 'La tarjeta decía «GREMIO» porque el texto se truncaba sin avisar. Ahora el generador de textos falla si algo no cabe.'),
 ('Apariciones fuera de cámara', 'Los enemigos con columna de aparición por detrás de la cámara inicial nunca salían: se fijó un mínimo de columna 4. Y el generador de apariciones solo bloquea con brujas y hechizos en pantalla, no con cualquier tipo alto.'),
 ('Caracteres de sobra', 'Las arenas grandes no cabían en tres juegos: se pasó a cuatro y a un suelo liso sin mapa de colisión (mapb = 0).'),
 ('Sprites fuera de la zona visible', 'La calavera del GAME OVER no se veía: estaba por encima de la primera línea de jugadores y su página horizontal tenía basura. Se recolocó la escena y se limpió la parte alta.'),
 ('Pruebas con cargas largas', 'Los bots no pulsaban FIRE tras las cargas largas del XEX: se añadieron pulsaciones fijas y mientras el juego espera.'),
 ('El paso del título viejo', 'El arranque caía en el título de texto antiguo: faltaba un <span class="mono">jmp title</span>. Código muerto que sigue vivo si nada lo salta.'),
 ('DLI y WSYNC', 'Lo que va antes de WSYNC en una DLI debe caber en la línea, y en ANTIC 4 ancho la CPU va a media velocidad. Medir el error, no adivinarlo.'),
 ('Trampas para el invencible', 'Revisar cada hueco: si el truco impide morir, cualquier foso sin salida bloquea la partida. Se abrió un paso en la torre de la Ciudadela.'),
 ('Un formato para todo', 'Definir los módulos como flujos de registros (destino, longitud, datos) permitió servirlos desde bancos, sectores o páginas de cartucho con el mismo analizador.'),
 ('Tras leer del disco', 'El SIO deja POKEY a su manera: tras cada carga se restauran AUDCTL y SKCTL y se apaga el sonido, o la música suena desafinada.'),
 ('Colores con cabeza', 'Antes de pedir otro registro de color, mirar si sobra uno: el PF3 de los caracteres invertidos estaba libre en casi todas las fases.'),
]
filas = ''.join('<div class="caja"><h3>%s</h3><p>%s</p></div>' % a for a in APR)
pags.append(P('<div class="g2">%s</div>' % filas, 'Aprendizaje', 'Errores, arreglos y reglas que quedan para el próximo juego'))

pags.append(P("""
<div class="g2"><div>
<h2>Lo que funcionó</h2>
<ul>
<li><b>Dibujar en texto.</b> Escenarios, sprites y jefes como cuadrículas en Python: la misma fuente sirve al juego, a los bocetos y a este atlas.</li>
<li><b>Bocetos sobre capturas reales.</b> Cada opción se ve con su paleta y sus límites; no hay sorpresas al montarla.</li>
<li><b>Un bot por jefe.</b> Vencer a un jefe sin manos demuestra que se puede vencer y deja la fase siguiente probada.</li>
<li><b>Módulos comprimidos.</b> Cinco fases ricas en 64 KB, con el mismo programa residente en los tres soportes.</li>
<li><b>Motor de jefes por datos.</b> Tres jefes con 32 bytes de parámetros y una lista de ataques.</li>
</ul></div><div>
<h2>Para el próximo juego</h2>
<ul>
<li>Reservar desde el principio un margen de código residente: este juego acabó con unos 50 bytes libres.</li>
<li>Diseñar el reparto de colores pensando en PF3 desde la primera fase.</li>
<li>Escribir la DLI mínima antes de dibujar nada que dependa de cambios por fila.</li>
<li>Pasar un bot invencible por cada tramo buscando fosos sin salida.</li>
<li>Prohibir los <span class="mono">*+N</span>; usar etiquetas anónimas.</li>
</ul></div></div>
%s
""" % caja('Banco de trabajo', '<p>Todo lo reutilizable (cargador de módulos para 130XE, disco y cartucho, compresor LZ, generadores de tramos, bots y '
           'herramientas de medida) está en el banco de trabajo del paquete, con su guía actualizada.</p>', True),
 'Aprendizaje', 'Lo que funcionó y lo que conviene repetir'))

# ---------------------------------------------------------------- referencias
pags.append(P("""
<div class="g2"><div>
<h2>Patrimonio real</h2>
<ul>
<li>[H1] UNESCO / ICOMOS, <i>Historic Centre of Sighișoara</i>, evaluación histórica. whc.unesco.org/document/204</li>
<li>[H2] Comisión Nacional de Rumanía para la UNESCO, ficha del centro histórico. cnr-unesco.ro</li>
<li>[H3] Visit Mureș, recorrido histórico por Sighișoara. visitmures.com</li>
<li>[H4] Explore Sighișoara (2026), la Escalera Cubierta. exploresighisoara.ro</li>
<li>[H5] Cluj Tourism, Salina Turda. clujtourism.ro</li>
</ul>
<h2>Folclore</h2>
<ul>
<li>[F1] Chereches y Badea (2018), <i>De cadáveres desenterrados y corazones quemados</i>. dialnet.unirioja.es</li>
<li>[F2] Hovi, <i>The Vampire Tradition in Romania</i>. utupub.fi</li>
<li>[F3] Antonescu, <i>Dicționar de etnografie</i>, entradas sobre strigoi. cimec.ro</li>
</ul>
<h2>Límites de la adaptación</h2>
<ul>
<li>El solsticio de 1847, el sello infernal y el Rey Strigoi son ficción.</li>
<li>Los monumentos reales no avalan ningún hecho sobrenatural.</li>
<li>La Escalera Cubierta tiene cronologías contradictorias; no se fija una fecha.</li>
<li>Las minas son fantásticas y no reproducen Turda dentro de Sighișoara.</li>
<li>Vâvâma y Lupari son nombres del universo del juego.</li>
</ul>
</div><div>
<h2>Homenajes</h2>
<ul>
<li>La tumba, la bruja y el pollo: <i>Ghosts'n Goblins</i>.</li>
<li>La cabeza gigante del final: el último jefe de <i>Crossbow</i> (Atari 8 bits).</li>
<li>Música inspirada en temas aportados por el autor (fase, cueva, jefe, y <i>Ghouls'n Ghosts</i> para título, final y GAME OVER); todas las melodías son originales.</li>
</ul>
<h2>Créditos</h2>
<p><b>Concepto, guion base y dirección creativa:</b> Tony C. Ware.</p>
<p><b>Programa, gráficos, música y documentación:</b> Tony C. Ware.</p>
<p>Arte de la carátula y de la preproducción: material editorial del proyecto.</p>
<p style="margin-top:10mm; font: bold 16pt 'DejaVu Serif'; color:#9e1b2b">2026 - TONY C. WARE</p>
%s
</div></div>
""" % cap('22_la_noche_ha_terminado'), 'Referencias y créditos', 'Fuentes consultadas y autoría'))

a_pdf(documento(pags, 210, 297, EXTRA, 'La Noche de los Strigoi · Atlas visual y memoria'), 'atlas.html', sys.argv[1])
