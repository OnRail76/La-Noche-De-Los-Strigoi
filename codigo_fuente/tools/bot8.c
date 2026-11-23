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
  if(!libatari800_init(4,args)){fprintf(stderr,"init: %s\n",libatari800_error_message());return 1;}
  M=libatari800_get_main_memory_ptr();
  char p[512]; snprintf(p,512,"%s/log.txt",dir); FILE *log=fopen(p,"w");
  input_template_t in; int firet=0;
  int TOMB[3]={24,72,116};
  for(int fr=0;fr<endf;fr++){
    libatari800_clear_input_array(&in);
    int joy=0, trig=0;
    if(fr>=100 && fr<104) trig=1; if(fr>=560 && fr<563) trig=1; if(R("gmode")==0 && fr%50<3 && fr>200 && fr<900) trig=1;
    int gm=R("gmode");
    if(gm==2 && R("rst")!=3){
      int rx=R("rxl"), ry=R("ry"), ph=R("bphase");
      if(ph==0){
        int mp=R("mpos"), ms=R("mstate"), mt=R("mt");
        int mx=M[A("MORT_COL")+mp]*4+26;
        int best=-1, bd=999;
        for(int t=0;t<3;t++){ if(t==mp) continue; int d=abs((TOMB[t]+6)-rx); if(d<bd){bd=d;best=t;} }
        int t0=TOMB[best];
        int wind = (ms==2 && mt>=38 && mt<192);
        int on = (ry==168 && rx+5>=t0 && rx+2<t0+20);
        if(wind && (ry==184 || on)){ joy=2; }
        else if(on){
          int face=(mx>rx)?8:4;
          int k=fr%12;
          if(k==0) joy=face; else if(k<3) trig=1;
        } else if(ry==184){
          if(rx < t0-22) joy=8;
          else if(rx > t0+30) joy=4;
          else if(rx < t0) joy=9;              /* salto hacia la derecha */
          else joy=5;                          /* salto hacia la izquierda */
        }
      } else if(ph==1){
        int ws=R("wstate"), wx=R("wx")*4, wd=R("wdir");
        int wc=wx+16, d=wc-(rx+4);
        if(ry==168) { joy=8; }
        else if(ry!=184) { joy=0; }
        else if(ws==1 && ((wd==1 && d>0 && d<44) || (wd==0 && d<0 && d>-44))){ joy=1; }
        else if(rx<40 && ws!=2) joy=8;
        else if(rx>110 && ws!=2) joy=4;
        else {
          int face=(wc>rx)?8:4;
          int k=fr%10;
          if(k==0) joy=face; else if(k<3) joy=0; else if(k<5){ joy=0; trig=1; } else joy=0;
        }
      }
    }
    in.joy0=joy; in.trig0=trig;
    libatari800_next_frame(&in);
    if((getenv("TODO") ? 1 : fr%30==0) && gm==2) fprintf(log,"%d fase=%d vida=%d mstate=%d mpos=%d wstate=%d wx=%d rx=%d ry=%d vidas=%d bwin=%d\n",
        fr,R("bphase"),R("bhp"),R("mstate"),R("mpos"),R("wstate"),R("wx"),R("rxl"),R("ry"),R("lives"),R("bwin"));
    if(fr%30==0 && gm!=2) fprintf(log,"%d gmode=%d fase=%d tramo=%d\n",fr,gm,R("fase"),R("tramo"));
    if(fr==endf-1){ snprintf(p,512,"%s/final.raw",dir); FILE*o=fopen(p,"wb"); fwrite(libatari800_get_screen_ptr(),1,384*240,o); fclose(o); }
    if(every && fr%every==0 && gm==2){ snprintf(p,512,"%s/f%05d.raw",dir,fr); FILE*o=fopen(p,"wb"); fwrite(libatari800_get_screen_ptr(),1,384*240,o); fclose(o); }
  }
  fclose(log); libatari800_exit(); return 0;
}
