# Cuenta, en capturas .raw de 384x240, los píxeles de la primera línea de cada fila con colores de la fila anterior (DLI tardía)
import sys,glob
fs=sorted(glob.glob(sys.argv[1]+'/f*.raw'))
tot={};nf=0;fr={}
for f in fs:
    d=open(f,'rb').read(); nf+=1
    for y0 in range(41,233,8):
        body=set(d[(y0+k)*384+x] for k in range(1,8) for x in range(384))
        prev=set(d[(y0-k)*384+x] for k in range(2,8) for x in range(384))
        bad=sum(1 for x in range(384) if d[y0*384+x] in prev and d[y0*384+x] not in body)
        if bad: tot[y0]=tot.get(y0,0)+bad; fr[y0]=fr.get(y0,0)+1
print(nf,'cuadros', [(y,tot[y],fr[y]) for y in sorted(tot)])
