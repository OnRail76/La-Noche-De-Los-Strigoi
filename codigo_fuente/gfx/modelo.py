#!/usr/bin/env python3
"""Mini-ilustrador para jefes: volúmenes iluminados a alta resolución -> píxel ancho del Atari.

Coordenadas de diseño: "unidades cuadradas" (1 unidad = medio píxel de ANTIC 4 en x,
1 línea en y). El lienzo interno trabaja a S veces esa resolución.
Cada forma pinta un material y un valor de luz (0 = sombra, 1 = luz).
Al reducir: cada píxel del Atari (2 x 1 unidades) toma el material mayoritario y la
luz media; si la cobertura es baja queda transparente. Luego la luz se convierte en
uno de los tonos de la rampa del material (con tramado 2x2 suave en la frontera).
"""
import math
import numpy as np
from PIL import Image, ImageDraw

LX, LY, LZ = -0.55, -0.6, 0.58          # luz de luna: arriba a la izquierda
_n = math.sqrt(LX * LX + LY * LY + LZ * LZ); LX, LY, LZ = LX / _n, LY / _n, LZ / _n
BAYER = np.array([[0.0, 0.5], [0.75, 0.25]])


class Modelo:
    def __init__(s, w, h, S=4):
        s.w, s.h, s.S = w, h, S             # w en píxeles del Atari, h en líneas
        s.U, s.V = w * 2 * S, h * S
        s.mat = np.zeros((s.V, s.U), dtype=np.int16)      # 0 = vacío
        s.lux = np.zeros((s.V, s.U), dtype=np.float32)
        uu, vv = np.meshgrid(np.arange(s.U) + 0.5, np.arange(s.V) + 0.5)
        s.uu, s.vv = uu / S, vv / S         # en unidades de diseño
        s.ramps = {}                        # material -> lista de colores (oscuro -> claro)
        s.over = {}

    def material(s, mid, ramp):
        s.ramps[mid] = ramp

    def _mask_poly(s, pts):
        im = Image.new('1', (s.U, s.V), 0)
        ImageDraw.Draw(im).polygon([(a * s.S, b * s.S) for a, b in pts], fill=1)
        return np.array(im, dtype=bool)

    def _paint(s, m, mid, lux):
        s.mat[m] = mid
        s.lux[m] = np.clip(lux if np.isscalar(lux) else lux[m], 0, 1)

    # ---- volúmenes
    def esfera(s, cx, cy, rx, ry, mid, amb=0.18, k=1.0, clip=None):
        nx = (s.uu - cx) / rx; ny = (s.vv - cy) / ry
        d = nx * nx + ny * ny
        m = d <= 1.0
        if clip is not None: m &= clip
        nz = np.sqrt(np.clip(1 - d, 0, 1))
        lam = np.clip(nx * LX + ny * LY + nz * LZ, 0, 1)
        s._paint(m, mid, amb + k * lam * (1 - amb))
        return m

    def poli(s, pts, mid, lux=0.5, grad=None, clip=None):
        """polígono; grad = (luz_arriba, luz_abajo) o función(u, v) -> luz"""
        m = s._mask_poly(pts)
        if clip is not None: m &= clip
        if grad is None:
            L = lux
        elif callable(grad):
            L = grad(s.uu, s.vv)
        else:
            v0 = min(p[1] for p in pts); v1 = max(p[1] for p in pts)
            t = np.clip((s.vv - v0) / max(1, v1 - v0), 0, 1)
            L = grad[0] + (grad[1] - grad[0]) * t
        s._paint(m, mid, L)
        return m

    def tubo(s, pts, r0, r1, mid, amb=0.2):
        """miembro cilíndrico a lo largo de una polilínea suave (radio de r0 a r1)"""
        P = np.array(pts, dtype=float)
        # remuestrear
        seg = []
        for i in range(len(P) - 1):
            for t in np.linspace(0, 1, 12, endpoint=False):
                seg.append(P[i] * (1 - t) + P[i + 1] * t)
        seg.append(P[-1]); seg = np.array(seg)
        n = len(seg)
        best_d = np.full(s.uu.shape, 1e9); best_i = np.zeros(s.uu.shape, dtype=int)
        for i, (a, b) in enumerate(seg):
            d = (s.uu - a) ** 2 + (s.vv - b) ** 2
            msk = d < best_d
            best_d[msk] = d[msk]; best_i[msk] = i
        rad = r0 + (r1 - r0) * best_i / max(1, n - 1)
        dist = np.sqrt(best_d)
        m = dist <= rad
        # normal aproximada: perpendicular al eje
        nxt = np.clip(best_i + 1, 0, n - 1); prv = np.clip(best_i - 1, 0, n - 1)
        tx = seg[nxt, 0] - seg[prv, 0]; ty = seg[nxt, 1] - seg[prv, 1]
        tl = np.sqrt(tx * tx + ty * ty) + 1e-6
        px_ = -(ty / tl); py_ = tx / tl
        off = ((s.uu - seg[best_i, 0]) * px_ + (s.vv - seg[best_i, 1]) * py_) / np.maximum(rad, 0.1)
        off = np.clip(off, -1, 1)
        nz = np.sqrt(np.clip(1 - off * off, 0, 1))
        lam = np.clip(off * px_ * LX + off * py_ * LY + nz * LZ, 0, 1)
        s._paint(m, mid, amb + lam * (1 - amb))
        return m

    def tela(s, pts, mid, period=10.0, amp=0.35, base=0.45, phase=None, vgrad=0.0, clip=None):
        """tela con pliegues verticales que siguen phase(v) (desplazamiento en u)"""
        m = s._mask_poly(pts)
        if clip is not None: m &= clip
        ph = 0 if phase is None else phase(s.vv)
        v0 = min(p[1] for p in pts); v1 = max(p[1] for p in pts)
        t = np.clip((s.vv - v0) / max(1, v1 - v0), 0, 1)
        L = base + amp * np.sin(2 * math.pi * (s.uu - ph) / period) + vgrad * (t - 0.5)
        s._paint(m, mid, L)
        return m

    def borrar(s, pts):
        m = s._mask_poly(pts); s.mat[m] = 0
        return m

    def mask_mat(s, mid):
        return s.mat == mid

    def luz_mas(s, m, delta):
        s.lux[m] = np.clip(s.lux[m] + delta, 0, 1)

    # ---- retoques en píxel del Atari
    def ascii(s, x0, y0, txt, cmap):
        for j, row in enumerate(txt.strip('\n').split('\n')):
            for i, ch in enumerate(row):
                if ch in cmap:
                    s.over[(x0 + i, y0 + j)] = cmap[ch]

    def reducir(s, cover=0.45, dither=True, outline=None):
        """-> matriz (h, w) de códigos de color Atari (-1 = transparente)"""
        S = s.S
        out = np.full((s.h, s.w), -1, dtype=np.int16)
        bw, bh = 2 * S, S
        for y in range(s.h):
            for x in range(s.w):
                bm = s.mat[y * bh:(y + 1) * bh, x * bw:(x + 1) * bw]
                bl = s.lux[y * bh:(y + 1) * bh, x * bw:(x + 1) * bw]
                nz = bm[bm > 0]
                if nz.size < cover * bm.size:
                    continue
                vals, cnt = np.unique(nz, return_counts=True)
                mid = int(vals[np.argmax(cnt)])
                L = float(bl[bm == mid].mean())
                ramp = s.ramps[mid]
                n = len(ramp)
                f = L * n
                if dither:
                    f += (BAYER[y & 1, x & 1] - 0.375) * 0.6
                i = int(np.clip(math.floor(f), 0, n - 1))
                out[y, x] = ramp[i]
        if outline is not None:
            o = out.copy()
            for y in range(s.h):
                for x in range(s.w):
                    if out[y, x] == -1:
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            xx, yy = x + dx, y + dy
                            if 0 <= xx < s.w and 0 <= yy < s.h and out[yy, xx] not in (-1, outline):
                                o[y, x] = outline; break
            out = o
        for (x, y), c in s.over.items():
            if 0 <= x < s.w and 0 <= y < s.h:
                out[y, x] = c
        return out


def limpiar(a, keep=()):
    """quita píxeles sueltos (rodeados por 3-4 vecinos de otro color común)"""
    h, w = a.shape
    b = a.copy()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            c = a[y, x]
            if c in keep: continue
            nb = [a[y - 1, x], a[y + 1, x], a[y, x - 1], a[y, x + 1]]
            if nb.count(c) == 0:
                vals = {v: nb.count(v) for v in nb}
                v, k = max(vals.items(), key=lambda t: t[1])
                if k >= 3:
                    b[y, x] = v
    return b
