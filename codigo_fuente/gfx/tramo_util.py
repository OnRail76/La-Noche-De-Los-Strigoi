"""utilidades comunes a los generadores de tramos (fases 4 y 5)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import fase1 as F
from canvas import C
from PIL import Image
from pal import atari_rgb

MCOLS, MROWS = 256, 13

def code4(cs, cell, cl=0):
    """celda con '4' (PF3): carácter inverso; en ella el '3' (PF2) no puede convivir"""
    if any('4' in r for r in cell):
        assert not any('3' in r for r in cell), 'PF2 y PF3 en la misma celda'
        return cs.code([r.replace('4', '3') for r in cell], cl) | 0x80
    return cs.code(cell, cl)

def clear3(canvas):
    """en las celdas con '4', el '3' del fondo pasa a '1' (motas de textura)"""
    for cy in range(canvas.h // 8):
        for cx in range(canvas.w // 4):
            ys, xs = range(cy * 8, cy * 8 + 8), range(cx * 4, cx * 4 + 4)
            if any(canvas.p[y][x] == '4' for y in ys for x in xs):
                for y in ys:
                    for x in xs:
                        if canvas.p[y][x] == '3': canvas.p[y][x] = '1'

def stamp(canvas, x0, y0, art, cols, flip=False):
    rows = art.strip('\n').split('\n')
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch in cols:
                canvas.set(x0 + ((len(r) - 1 - i) if flip else i), y0 + j, cols[ch])

def build(pix, cls, sky, mtn):
    csB = F.Charset(1, 127)
    MAP = [[code4(csB, F.cut(pix, c, r), cls[r][c]) for c in range(MCOLS)] for r in range(MROWS)]
    csA = F.Charset(64, 64)
    SKY = [[csA.code(F.cut(sky, c, r)) for c in range(40)] for r in range(4)]
    csC = F.Charset(1, 127)
    MTN = [[code4(csC, F.cut(mtn, c, r)) for c in range(64)] for r in range(3)]
    print('mapa %d · cielo %d · fondo %d caracteres' % (csB.next - 1, csA.next - 64, csC.next - 1))
    return csA, csB, csC, SKY, MTN, MAP

def preview(name, csA, csB, csC, SKY, MTN, MAP, BK, PF0, PF1, PF2, cams=(0, 60, 130, 200), PF3=None):
    PF3 = PF3 or [0x0C] * 22
    def row_img(codes, cs, r):
        img = Image.new('RGB', (len(codes) * 4, 8)); px = img.load()
        pal = [atari_rgb(c) for c in (BK[r], PF0[r], PF1[r], PF2[r])]
        for c, code in enumerate(codes):
            pp = pal if code < 128 else pal[:3] + [atari_rgb(PF3[r])]
            for y in range(8):
                b = cs.data[(code & 0x7F) * 8 + y]
                for x in range(4): px[c * 4 + x, y] = pp[(b >> (6 - 2 * x)) & 3]
        return img
    sheet = Image.new('RGB', (1280, 672))
    for i, cc in enumerate(cams):
        img = Image.new('RGB', (160, 168))
        for r in range(4): img.paste(row_img(SKY[r], csA, r), (0, r * 8))
        for r in range(3): img.paste(row_img([MTN[r][(cc // 2 + c) % 64] for c in range(40)], csC, 4 + r), (0, 32 + r * 8))
        img.paste(Image.new('RGB', (160, 8), atari_rgb(BK[7])), (0, 56))
        for r in range(13): img.paste(row_img(MAP[r][cc:cc + 40], csB, 8 + r), (0, 64 + r * 8))
        sheet.paste(img.resize((640, 336), Image.NEAREST), ((i % 2) * 640, (i // 2) * 336))
    sheet.save(os.path.join(HERE, '..', 'build', name))
