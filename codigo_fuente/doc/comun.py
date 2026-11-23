"""La Noche de los Strigoi · utilidades comunes de la documentación (HTML → PDF con Chrome)."""
import os, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')

CSS = r"""
@page { margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'DejaVu Sans', sans-serif; color: #241c1a; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.pg { position: relative; overflow: hidden; page-break-after: always; break-after: page;
      background: #f2e8d3; background-image: radial-gradient(rgba(120,90,50,.06) 1px, transparent 1px);
      background-size: 5px 5px; }
.pg:last-child { page-break-after: auto; break-after: auto; }
.cab { background: #17121d; color: #f3e6c8; padding: 0 9mm; border-bottom: 1.2mm solid #9e1b2b; }
.cab .serie { font: bold 6.5pt 'DejaVu Sans'; letter-spacing: .12em; color: #c9a45a; padding-top: 3.2mm; text-transform: uppercase; }
.cab h1 { font: bold 15pt 'DejaVu Serif'; margin: 1mm 0 0; padding-bottom: 1.2mm; text-transform: uppercase; letter-spacing: .02em; }
.cab .sub { font: 7.5pt 'DejaVu Sans'; color: #b9ab93; padding-bottom: 2.6mm; margin-top: -0.4mm; }
.cuerpo { padding: 6mm 9mm 0; }
.pie { position: absolute; bottom: 4mm; left: 9mm; right: 9mm; border-top: .3mm solid #b49a73;
       font: 6.2pt 'DejaVu Sans'; color: #7d6a55; padding-top: 1.2mm; display: flex; justify-content: space-between; }
h2 { font: bold 10.5pt 'DejaVu Serif'; color: #9e1b2b; margin: 0 0 1.6mm; text-transform: uppercase; letter-spacing: .03em; }
h3 { font: bold 8.6pt 'DejaVu Sans'; margin: 0 0 1mm; color: #17121d; }
p, li { font-size: 8.3pt; line-height: 1.42; margin: 0 0 1.7mm; }
ul { margin: 0 0 2mm; padding-left: 4.5mm; }
li { margin-bottom: .9mm; }
.caja { background: #fbf6ea; border: .3mm solid #d8c6a3; border-radius: 1.4mm; padding: 2.6mm 3.2mm; margin-bottom: 3mm;
        box-shadow: 0 .4mm 0 rgba(80,50,20,.12); }
.caja > .et { display: block; background: #9e1b2b; color: #fff; font: bold 6.8pt 'DejaVu Sans'; letter-spacing: .08em;
        text-transform: uppercase; margin: -2.6mm -3.2mm 2mm; padding: 1.2mm 3.2mm; border-radius: 1.4mm 1.4mm 0 0; }
.caja.osc { background: #1d1724; color: #eadfc8; border-color: #3a2f45; }
.caja.osc h3 { color: #f3e6c8; }
.caja.osc .et { background: #c9a45a; color: #17121d; }
.pix { image-rendering: pixelated; display: block; width: 100%; border: .5mm solid #17121d; border-radius: .8mm; }
.foto { display: block; width: 100%; border-radius: 1mm; border: .4mm solid #17121d; }
.leyenda { font: italic 6.8pt 'DejaVu Sans'; color: #6a5844; margin: .8mm 0 2.4mm; }
.g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.g3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2.6mm; }
.g23 { display: grid; grid-template-columns: 1fr 1.25fr; gap: 3.5mm; }
.g32 { display: grid; grid-template-columns: 1.25fr 1fr; gap: 3.5mm; }
table { border-collapse: collapse; width: 100%; font-size: 7.6pt; margin-bottom: 2.6mm; }
th { background: #17121d; color: #f3e6c8; font-weight: bold; text-align: left; padding: 1.2mm 1.6mm; font-size: 7pt; }
td { border-bottom: .25mm solid #d3c19c; padding: 1.1mm 1.6mm; vertical-align: top; }
tr:nth-child(even) td { background: rgba(255,255,255,.35); }
.k { display: inline-block; background: #17121d; color: #f3e6c8; font: bold 7pt 'DejaVu Sans Mono'; padding: .3mm 1.4mm; border-radius: .8mm; }
.mono { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.2pt; }
.rojo { color: #9e1b2b; }
.cita { border-left: 1mm solid #9e1b2b; padding: 1mm 0 1mm 3mm; font: italic 8.4pt 'DejaVu Serif'; color: #3a2a24; margin: 0 0 3mm; }
"""

def esc(t):
    return html.escape(t, quote=False)

def img(n):
    return 'file://' + os.path.join(IMG, n)

def pagina(contenido, titulo=None, sub=None, serie='La Noche de los Strigoi', pie_izq='', pie_der='', clase=''):
    cab = ''
    if titulo:
        cab = '<div class="cab"><div class="serie">%s</div><h1>%s</h1>%s</div>' % (
            serie, titulo, '<div class="sub">%s</div>' % sub if sub else '')
    pie = '<div class="pie"><span>%s</span><span>%s</span></div>' % (pie_izq, pie_der) if (pie_izq or pie_der) else ''
    return '<section class="pg %s">%s<div class="cuerpo">%s</div>%s</section>' % (clase, cab, contenido, pie)

def documento(paginas, ancho_mm, alto_mm, extra_css='', titulo='La Noche de los Strigoi'):
    css = CSS + '@page { size: %smm %smm; } .pg { width: %smm; height: %smm; }' % (ancho_mm, alto_mm, ancho_mm, alto_mm) + extra_css
    return '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>' % (
        titulo, css, ''.join(paginas))

def a_pdf(html_txt, nombre_html, nombre_pdf):
    ruta = os.path.join(HERE, nombre_html)
    open(ruta, 'w', encoding='utf-8').write(html_txt)
    subprocess.check_call(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                           '--allow-file-access-from-files', '--virtual-time-budget=4000',
                           '--print-to-pdf=' + nombre_pdf, 'file://' + ruta],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('pdf:', nombre_pdf)
