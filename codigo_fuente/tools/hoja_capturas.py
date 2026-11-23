# Hoja de contactos de capturas .raw (384x240, códigos de color): hoja_capturas.py carpeta paso desde hasta salida.png
import sys,glob,os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gfx'))
from pal import atari_rgb
from PIL import Image,ImageDraw
P=bytes(sum((atari_rgb(i) for i in range(256)),()))
def img(f):
    d=open(f,'rb').read()
    im=Image.frombytes('P',(384,240),d); im.putpalette(P)
    return im.convert('RGB').crop((32,0,352,240))
d=sys.argv[1]; step=int(sys.argv[2]); a=int(sys.argv[3]) if len(sys.argv)>3 else 0; b=int(sys.argv[4]) if len(sys.argv)>4 else 99999
fs=[f for f in sorted(glob.glob(d+'/f[0-9]*.raw')) if a<=int(f[-9:-4])<=b and int(f[-9:-4])%step==0][:60]
S=Image.new('RGB',(10*160,((len(fs)+9)//10)*130),'black')
dr=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    S.paste(img(f).resize((160,120)),((i%10)*160,(i//10)*130))
    dr.text(((i%10)*160+2,(i//10)*130+118),f[-9:-4],fill=(255,255,0))
S.save(sys.argv[5] if len(sys.argv)>5 else '/tmp/sheet.png')
