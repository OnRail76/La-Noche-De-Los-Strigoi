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
  char *args[]={"-xe","-ntsc","-nobasic",argv[1],NULL};
  if(!libatari800_init(4,args)){fprintf(stderr,"init\n");return 1;}
  M=libatari800_get_main_memory_ptr();
  char p[512]; snprintf(p,512,"%s/log.txt",dir); FILE *log=fopen(p,"w");
  FILE*wav=getenv("WAV")?fopen(getenv("WAV"),"wb"):NULL;
  input_template_t in; int jt=-1;
  /* bot10: pelea contra Muma desde la repisa alta */
  for(int fr=0;fr<endf;fr++){
    libatari800_clear_input_array(&in);
    int joy=0,trig=0;
    if(fr>=100&&fr<104) trig=1; if(fr>=560&&fr<563) trig=1; if(R("gmode")==0 && fr%50<3 && fr>200 && fr<900) trig=1;
    int gm=R("gmode");
    if(gm==2 && R("rst")!=3){
      int rx=R("rxl"), ry=R("ry"), e0=R("etyp"), ex=M[A("exl")], ey=M[A("ey")];
      int danger = (e0==11 && abs(ex-rx)<36 && ey>ry-30 && ey<ry+30);
      int danger2 = (e0==18||M[A("etyp")+1]==18);
      if(ry==184){ if(rx<8) joy=8; else if(rx>12) joy=4; else joy=9; }
      else if(ry==160){ if(rx<34) joy=8; else joy=9; }
      else if(ry==136){
        if(rx<58) joy=8;
        else if(R("rdir")!=0) joy=8;
        else if(danger2 && fr%20==0){ joy=1; jt=0; }
        else if(fr%28==0){ joy=1; jt=0; }
      }
      if(jt>=0){ jt++; if(jt==9||jt==10) trig=1; if(jt>40) jt=-1; }
    }
    in.joy0=joy; in.trig0=trig;
    libatari800_next_frame(&in);
    if(wav) fwrite(libatari800_get_sound_buffer(),1,libatari800_get_sound_buffer_len(),wav);
    if(fr%30==0) fprintf(log,"%d gm=%d rx=%d ry=%d bhp=%d sh=%d fase=%d e=%d,%d lives=%d bwin=%d\n",fr,gm,R("rxl"),R("ry"),R("bhp"),R("m_st"),R("bphase"),R("etyp"),M[A("etyp")+1],R("lives"),R("bwin"));
    if(every && fr%every==0){ snprintf(p,512,"%s/f%05d.raw",dir,fr); FILE*o=fopen(p,"wb"); fwrite(libatari800_get_screen_ptr(),1,384*240,o); fclose(o); }
  }
  if(wav){fclose(wav);fprintf(stderr,"wav %d Hz %d ch %d B\n",libatari800_get_sound_frequency(),libatari800_get_num_sound_channels(),libatari800_get_sound_sample_size());}
  fclose(log); libatari800_exit(); return 0;
}
