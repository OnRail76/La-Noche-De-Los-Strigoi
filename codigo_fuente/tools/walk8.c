/* bot8: juega contra el Strigoi Mort leyendo la memoria del juego en cada cuadro.
   uso: bot8 juego.xex game.lbl cuadros salida/ [cada_n_capturas] [invencible_no_importa]
   Escribe salida/log.txt (estado cada 30 cuadros) y capturas .raw cada n cuadros. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libatari800.h"

static unsigned char *M;
typedef struct { char n[32]; int a; } Lb;
static Lb lb[4096]; static int nlb;
static int A(const char *n){ for(int i=0;i<nlb;i++) if(!strcmp(lb[i].n,n)) return lb[i].a; fprintf(stderr,"falta %s\n",n); exit(1); }
static int R(const char *n){ return M[A(n)]; }

int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"uso: bot8 xex lbl cuadros dir [n]\n");return 1;}
  FILE *f=fopen(argv[2],"r"); char line[256];
  while(fgets(line,256,f)){ unsigned a; char nm[64]; if(sscanf(line,"al %x .%63s",&a,nm)==2 && nlb<4096){ strncpy(lb[nlb].n,nm,31); lb[nlb].a=a; nlb++; } }
  fclose(f);
  int endf=atoi(argv[3]); const char *dir=argv[4]; int every=argc>5?atoi(argv[5]):0;
  char *args[]={getenv("MACH")?getenv("MACH"):"-xe","-ntsc","-nobasic",argv[1],NULL};
  if(!libatari800_init(4,args)){fprintf(stderr,"init\n");return 1;}
  M=libatari800_get_main_memory_ptr();
  char p[512]; snprintf(p,512,"%s/log.txt",dir); FILE *log=fopen(p,"w");
  FILE*wav=getenv("WAV")?fopen(getenv("WAV"),"wb"):NULL;
  input_template_t in;
  /* walk8: recorre el cementerio a la derecha saltando; captura cada n cuadros */
  for(int fr=0;fr<endf;fr++){
    libatari800_clear_input_array(&in);
    int joy=0,trig=0;
    if(fr>=100&&fr<104) trig=1; if(fr>=560&&fr<563) trig=1; if(R("gmode")==0 && fr%50<3 && fr>200 && fr<900) trig=1;
    int gm=R("gmode");
    if(fr>200 && gm==1){ int k=fr%40; joy = (k<4)?9:8; if(k==20||k==21) trig=1; }
    if(getenv("AUTOFIRE") && fr%100<3) trig=1;
    if(getenv("NOIN")){joy=0;trig=0;}
    if(getenv("HC") && fr>=400 && fr<410) joy=8;
    in.joy0=joy; in.trig0=trig;
    libatari800_next_frame(&in);
    if(wav) fwrite(libatari800_get_sound_buffer(),1,libatari800_get_sound_buffer_len(),wav);
    int rx=R("rxl")+256*R("rxh");
    if(fr%30==0) fprintf(log,"%d gm=%d rx=%d col=%d e=%d,%d st=%d,%d y=%d,%d spi=%d diff=%d arm=%d bhp=%d\n",fr,gm,rx,rx/4,M[A("etyp")],M[A("etyp")+1],M[A("est")],M[A("est")+1],M[A("ey")],M[A("ey")+1],M[A("spi")],R("diff"),R("rarmor"),R("bhp"));
    if(every && fr%every==0){ snprintf(p,512,"%s/f%05d.raw",dir,fr); FILE*o=fopen(p,"wb"); fwrite(libatari800_get_screen_ptr(),1,384*240,o); fclose(o); }
  }
  if(wav){fclose(wav);fprintf(stderr,"wav %d Hz %d ch %d B\n",libatari800_get_sound_frequency(),libatari800_get_num_sound_channels(),libatari800_get_sound_sample_size());}
  fclose(log); libatari800_exit(); return 0;
}
