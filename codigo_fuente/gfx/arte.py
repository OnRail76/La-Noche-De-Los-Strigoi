#!/usr/bin/env python3
"""Lienzo para dibujar con las reglas reales del Atari en ANTIC 4.

- Se dibuja en coordenadas "cuadradas": 2 unidades por píxel del Atari en horizontal
  (el píxel de ANTIC 4 es el doble de ancho que de alto) y 1 por línea en vertical.
- Cada forma lleva su capa; al reducir a píxel ancho manda la capa de encima.
- La pantalla se divide en bandas de 8 líneas (filas de caracteres). Cada banda tiene
  su paleta: [COLBK, PF0, PF1, PF2] y, opcional, PF3 (solo en casillas invertidas,
  que cambian PF2 por PF3: una casilla de 4x8 no puede usar PF2 y PF3 a la vez).
- verify() cuenta colores fuera de paleta, conflictos PF2/PF3 y casillas distintas.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from pal import atari_rgb

T = -1   # transparente


class Lienzo:
    def __init__(s, w, h):
        s.w, s.h = w, h                      # en píxeles del Atari
        s.col = np.full((h, w * 2), T, dtype=np.int16)
        s.lay = np.zeros((h, w * 2), dtype=np.int32)
        s.layer = 0
        s.over = {}                          # retoques píxel a píxel (x, y) -> color

    # ---------- formas (coordenadas cuadradas: u = 2 * x) ----------
    def _mask_paint(s, mask, c):
        s.layer += 1
        s.col[mask] = c
        s.lay[mask] = s.layer

    def _img(s):
        return Image.new('1', (s.w * 2, s.h), 0)

    def poly(s, pts, c):
        im = s._img(); ImageDraw.Draw(im).polygon([(float(a), float(b)) for a, b in pts], fill=1)
        s._mask_paint(np.array(im, dtype=bool), c)

    def ell(s, cx, cy, rx, ry, c):
        im = s._img(); ImageDraw.Draw(im).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=1)
        s._mask_paint(np.array(im, dtype=bool), c)

    def rect(s, x0, y0, x1, y1, c):
        im = s._img(); ImageDraw.Draw(im).rectangle([x0, y0, x1, y1], fill=1)
        s._mask_paint(np.array(im, dtype=bool), c)

    def line(s, pts, wdt, c):
        im = s._img(); d = ImageDraw.Draw(im)
        d.line([(float(a), float(b)) for a, b in pts], fill=1, width=max(1, int(round(wdt))))
        for (a, b) in pts:
            r = wdt / 2.0
            d.ellipse([a - r, b - r, a + r, b + r], fill=1)
        s._mask_paint(np.array(im, dtype=bool), c)

    def curve(s, p0, p1, p2, wdt, c, n=24, w1=None):
        """curva de Bézier cuadrática; el grosor puede ir de wdt a w1"""
        w1 = wdt if w1 is None else w1
        import math as _m
        ln = _m.hypot(p1[0] - p0[0], p1[1] - p0[1]) + _m.hypot(p2[0] - p1[0], p2[1] - p1[1])
        n = max(n, int(ln / 0.6) + 1)
        pts = []
        for i in range(n + 1):
            t = i / n
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            pts.append((x, y, wdt + (w1 - wdt) * t))
        im = s._img(); d = ImageDraw.Draw(im)
        for (a, b, r) in pts:
            r = max(0.5, r / 2.0)
            d.ellipse([a - r, b - r, a + r, b + r], fill=1)
        s._mask_paint(np.array(im, dtype=bool), c)

    def mask_fn(s, fn, c):
        """pinta donde fn(u, y) es cierto (u en coordenadas cuadradas)"""
        uu, yy = np.meshgrid(np.arange(s.w * 2), np.arange(s.h))
        s._mask_paint(fn(uu, yy), c)

    def clip_paint(s, region_color, fn, c):
        """pinta c solo sobre lo que ya es region_color y cumple fn (sombreado dentro de una forma)"""
        uu, yy = np.meshgrid(np.arange(s.w * 2), np.arange(s.h))
        m = (s.col == region_color) & fn(uu, yy)
        s._mask_paint(m, c)

    # ---------- píxel a píxel (coordenadas del Atari) ----------
    def px(s, x, y, c):
        s.over[(x, y)] = c

    def ascii(s, x0, y0, txt, cmap):
        for j, row in enumerate(l for l in txt.strip('\n').split('\n')):
            for i, ch in enumerate(row):
                if ch in cmap:
                    s.over[(x0 + i, y0 + j)] = cmap[ch]

    # ---------- a píxel ancho ----------
    def wide(s):
        a = s.col[:, 0::2]; b = s.col[:, 1::2]
        la = s.lay[:, 0::2]; lb = s.lay[:, 1::2]
        out = np.where(lb > la, b, a)
        for (x, y), c in s.over.items():
            if 0 <= x < s.w and 0 <= y < s.h:
                out[y, x] = c
        return out


def rgbdist(a, b):
    ra, rb = atari_rgb(a), atari_rgb(b)
    return sum((p - q) ** 2 for p, q in zip(ra, rb))


class Escena:
    """pantalla de juego: marcador + 21 filas de ANTIC 4 (160 x 168)"""
    def __init__(s, bands):
        s.bands = bands                      # 21 paletas [BK, PF0, PF1, PF2, (PF3)]
        s.base = np.full((168, 160), T, dtype=np.int16)
        s.sprites = []                       # (x, y, filas de bits, color) encima

    def paste(s, wide, x0, y0):
        h, w = wide.shape
        for y in range(h):
            for x in range(w):
                c = wide[y, x]
                if c != T and 0 <= x0 + x < 160 and 0 <= y0 + y < 168:
                    s.base[y0 + y, x0 + x] = c

    def quantize(s):
        """ajusta cada banda a su paleta y resuelve PF2/PF3 por casilla; devuelve índices 0-4"""
        idx = np.zeros((168, 160), dtype=np.int8)
        report = {'fuera': 0, 'conflictos': 0}
        for r in range(21):
            pal = s.bands[r]
            for y in range(r * 8, r * 8 + 8):
                for x in range(160):
                    c = s.base[y, x]
                    if c == T:
                        idx[y, x] = 0; continue
                    if c in pal:
                        idx[y, x] = pal.index(c)
                    else:
                        report['fuera'] += 1
                        idx[y, x] = min(range(len(pal)), key=lambda i: rgbdist(c, pal[i]))
            if len(pal) > 4:
                for cx in range(40):
                    cell = idx[r * 8:r * 8 + 8, cx * 4:cx * 4 + 4]
                    n2 = int((cell == 3).sum()); n3 = int((cell == 4).sum())
                    if n2 and n3:
                        report['conflictos'] += 1
                        lose, win = (3, 4) if n3 >= n2 else (4, 3)
                        for yy in range(8):
                            for xx in range(4):
                                if cell[yy, xx] == lose:
                                    cands = [0, 1, 2, win]
                                    cell[yy, xx] = min(cands, key=lambda i: rgbdist(pal[lose], pal[i]))
        s.idx = idx
        return report

    def cells(s, rows):
        """casillas distintas (para el presupuesto de caracteres) en esas filas"""
        seen = set()
        for r in rows:
            for cx in range(40):
                cell = s.idx[r * 8:r * 8 + 8, cx * 4:cx * 4 + 4].copy()
                inv = (cell == 4).any()
                cell[cell == 4] = 3
                b = cell.tobytes()
                if cell.any():
                    seen.add(b)
        return len(seen)

    def colors_per_band(s):
        return [len(set(s.bands[r])) for r in range(21)]

    def render(s, scale=3, hud=None):
        """imagen RGB con el píxel ancho (2:1) y escala"""
        W, H = 160 * 2, 168
        img = Image.new('RGB', (W, H))
        px = img.load()
        for y in range(168):
            pal = s.bands[y // 8]
            for x in range(160):
                c = atari_rgb(pal[s.idx[y, x]])
                px[2 * x, y] = c; px[2 * x + 1, y] = c
        for (x, y, rows, col) in s.sprites:
            for j, bits in enumerate(rows):
                for i in range(8):
                    if (bits >> (7 - i)) & 1:
                        xx, yy = x + i, y + j
                        if 0 <= xx < 160 and 0 <= yy < 168:
                            c = atari_rgb(col)
                            px[2 * xx, yy] = c; px[2 * xx + 1, yy] = c
        img = img.resize((W * scale, H * scale), Image.NEAREST)
        if hud:
            top = Image.new('RGB', (W * scale, 8 * scale), (0, 0, 0))
            from PIL import ImageDraw as D
            D.Draw(top).text((6, 4), hud, fill=atari_rgb(0x0C))
            full = Image.new('RGB', (W * scale, (H + 8) * scale))
            full.paste(top, (0, 0)); full.paste(img, (0, 8 * scale))
            return full
        return img


class LienzoS(Lienzo):
    """Lienzo que escala todas las coordenadas y grosores por s (para reducir un dibujo)"""
    def __init__(s, w, h, k):
        super().__init__(w, h)
        s.k = k

    def poly(s, pts, c):
        super().poly([(a * s.k, b * s.k) for a, b in pts], c)

    def ell(s, cx, cy, rx, ry, c):
        super().ell(cx * s.k, cy * s.k, rx * s.k, ry * s.k, c)

    def rect(s, x0, y0, x1, y1, c):
        super().rect(x0 * s.k, y0 * s.k, x1 * s.k, y1 * s.k, c)

    def line(s, pts, wdt, c):
        super().line([(a * s.k, b * s.k) for a, b in pts], max(1.0, wdt * s.k), c)

    def curve(s, p0, p1, p2, wdt, c, n=24, w1=None):
        k = s.k
        super().curve((p0[0] * k, p0[1] * k), (p1[0] * k, p1[1] * k), (p2[0] * k, p2[1] * k),
                      max(1.0, wdt * k), c, n, None if w1 is None else max(0.8, w1 * k))
