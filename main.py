#coding:utf-8
import random,pygame,math,time,numpy,os
from PIL import Image
from pygame.locals import *

pygame.init()
btex,btey=1280,1024
tex,tey=1280,1024
def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)
def rxx(x): return float(float(x)/float(btex)*float(tex))
def ryy(y): return float(float(y)/float(btey)*float(tey))
fenetre=pygame.display.set_mode([tex,tey],pygame.FULLSCREEN)
pygame.display.set_caption("Super Racing")

font1=pygame.font.SysFont("Arial",ry(16))
font2=pygame.font.SysFont("Arial",ry(20))
font3=pygame.font.SysFont("Arial",ry(25))
font4=pygame.font.SysFont("Arial",ry(30))
font5=pygame.font.SysFont("Arial",ry(35))

dimg="images/"
dmape="mapes/"

tc=rx(150)

emape=[]
emape.append( ["herbe",75,pygame.transform.scale(pygame.image.load(dimg+"herbe.png"),[tc,tc])] )
emape.append( ["route",100,pygame.transform.scale(pygame.image.load(dimg+"route.png"),[tc,tc])] )
emape.append( ["mur1",False,pygame.transform.scale(pygame.image.load(dimg+"mur1.png"),[tc,tc])] )
emape.append( ["arrivee",100,pygame.transform.scale(pygame.image.load(dimg+"arive.png"),[tc,tc])] )
emape.append( ["place depart",100,pygame.transform.scale(pygame.image.load(dimg+"place_dep.png"),[tc,tc])] )
emape.append( ["route2",100,pygame.transform.scale(pygame.image.load(dimg+"route2.png"),[tc,tc])] )
emape.append( ["arivée",100,pygame.transform.scale(pygame.image.load(dimg+"arrivee.png"),[tc,tc])] )
#0=nom 1=pmd 2=img

voitures=[]
voitures.append( ["nula",rx(75),rx(75),rx(30),rxx(0.2),rxx(0.10),rxx(1),rxx(0.1),3,"v1.png"] )
voitures.append( ["forta",rx(75),rx(75),rx(100),rxx(0.5),rxx(0.25),rxx(1),rxx(0.1),4,"v2.png"] )
#0=nom 1=tx 2=ty 3=vit max 4=acc 5=recul 6=frein 7=decc 8=tournant 9=img

di=1

pmmx,pmmy=rx(1000),ry(25)
tmmx,tmmy=rx(200),ry(200)
tcx,tcy=int(tc/tex*tmmx),int(tc/tey*tmmy)


class Car:
    def __init__(self,x,y,tp,agl):
        vtp=voitures[tp]
        self.nom=vtp[0]
        self.px=x
        self.py=y
        self.tx=vtp[1]
        self.ty=vtp[2]
        self.vitesse_max=vtp[3]/di
        self.vitesse_actuelle=0
        self.acceleration=vtp[4]/di
        self.recul=vtp[5]/di
        self.frein=vtp[6]/di
        self.decceleration=vtp[7]/di
        self.tournant=vtp[8]
        self.agl=agl
        self.img_b=pygame.transform.scale(pygame.image.load(dimg+vtp[9]),[self.tx,self.ty])
        self.img=pygame.transform.rotate(self.img_b,-self.agl)
        self.dbg=time.time()
        self.tbg=0.01/di
        self.dkey=time.time()
        self.tkey=0.01
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.tour=0
        self.fini=False
        self.img_cvit=pygame.transform.scale( pygame.image.load(dimg+"cvit.png"), [rx(200),ry(200)])
        self.img_bvit=pygame.transform.scale( pygame.image.load(dimg+"cvit_b.png"), [rx(200),ry(200)])
        self.dacc=time.time()
        self.tacc=0.01
        self.dfrein=time.time()
        self.tfrein=0.01
        self.dtourn=time.time()
        self.ttourn=0.01
        self.drecul=time.time()
        self.trecul=0.01
        self.isacc=False
    def bouger(self,aa):
        if True:
            if aa=="up":
                if time.time()-self.dacc >= self.tacc:
                    self.dacc=time.time()
                    self.vitesse_actuelle+=self.acceleration
                    if self.vitesse_actuelle>self.vitesse_max: self.vitesse_actuelle=self.vitesse_max
            elif aa=="down":
                if time.time()-self.drecul >= self.trecul:
                    self.drecul=time.time()
                    self.vitesse_actuelle-=self.recul
                    if self.vitesse_actuelle<-self.vitesse_max: self.vitesse_actuelle=-self.vitesse_max
            elif aa=="left":
                if time.time()-self.dtourn >= self.ttourn:
                    self.dtourn=time.time()
                    self.agl-=self.tournant
                    if self.agl<0: self.agl=360+self.agl
                    self.img=pygame.transform.rotate(self.img_b,-self.agl)
            elif aa=="right":
                if time.time()-self.dtourn >= self.ttourn:
                    self.dtourn=time.time()
                    self.agl+=self.tournant
                    if self.agl>360: self.agl=self.agl-360
                    self.img=pygame.transform.rotate(self.img_b,-self.agl)
            elif aa=="space":
                if time.time()-self.dfrein>=self.tfrein:
                    self.dfrein=time.time()
                    if self.vitesse_actuelle>0:
                        if self.vitesse_actuelle>=self.frein: self.vitesse_actuelle-=self.frein
                        else: self.vitesse_actuelle=0
                    if self.vitesse_actuelle<0:
                        if self.vitesse_actuelle<=-self.frein: self.vitesse_actuelle+=self.frein
                        else: self.vitesse_actuelle=0
    def update(self,mape):
        if time.time()-self.dbg>=self.tbg:
            self.dbg=time.time()
            if not self.isacc:
                if self.vitesse_actuelle>0:
                    if self.vitesse_actuelle>=self.decceleration: self.vitesse_actuelle-=self.decceleration
                    else: self.vitesse_actuelle=0
                if self.vitesse_actuelle<0:
                    if self.vitesse_actuelle<=-self.decceleration: self.vitesse_actuelle+=self.decceleration
                    else: self.vitesse_actuelle=0
            xx,yy=0,0
            if self.agl>=0 and self.agl<90:
                yy=-math.cos( math.radians(self.agl) )*self.vitesse_actuelle
                xx=math.sin( math.radians(self.agl) )*self.vitesse_actuelle
                self.py+=yy
                self.px+=xx
            elif self.agl>=90 and self.agl<180:
                xx=math.cos( math.radians(self.agl-90) )*self.vitesse_actuelle
                yy=math.sin( math.radians(self.agl-90) )*self.vitesse_actuelle
                self.px+=xx
                self.py+=yy
            elif self.agl>=180 and self.agl<270:
                yy=math.cos( math.radians(self.agl-180) )*self.vitesse_actuelle
                xx=-math.sin( math.radians(self.agl-180) )*self.vitesse_actuelle
                self.py+=yy
                self.px+=xx
            elif self.agl>=270 and self.agl<360:
                xx=-math.cos( math.radians(self.agl-270) )*self.vitesse_actuelle
                yy=-math.sin( math.radians(self.agl-270) )*self.vitesse_actuelle
                self.px+=xx
                self.py+=yy
            self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
            for x in range(int((self.px)/tc-3),int((self.px)/tc+3)):
                for y in range(int((self.py)/tc-3),int((self.py)/tc+3)):
                    if x>=0 and y>=0 and x < mape.shape[0] and y < mape.shape[1]: 
                        mrect=pygame.draw.rect(fenetre,(0,0,0),(x*tc,y*tc,tc,tc),2)
                        if self.rect.colliderect(mrect):
                            if emape[mape[x,y]][1]==False:
                                self.px-=xx
                                self.py-=yy
                                self.vitesse_actuelle=0
                            elif mape[x,y]==3:
                                self.tour+=1

def load_mape(m):
    f=open(dmape+m,"r").readlines()
    tx=len(f[0])
    ty=len(f)
    mape=numpy.zeros([tx,ty],dtype=int)
    for x in range(tx-1):
        for y in range(ty-1):
            mape[x,y]=int(f[y][x])
    return mape

def aff(mape,cars,mycar,cam,fps,imgminimape):
    fenetre.fill((100,100,100))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][2],[cam[0]+x*tc,cam[1]+y*tc])
    for c in cars:
        fenetre.blit( c.img , [cam[0]+c.px,cam[1]+c.py] )
    #cadran vitesse
    agl=-(mycar.vitesse_actuelle/mycar.vitesse_max*305)+15
    ray=(rx(100)+ry(100))/2
    if agl >= 0 and agl < 90:
        nagl=-agl
        adj=math.cos( math.radians(nagl) )*ray
        opp=math.sin( math.radians(nagl) )*ray
        posv=[rx(800)+opp,ry(150)-adj]
    elif agl >= 90 and agl < 180:
        nagl=-agl-90
        adj=math.cos( math.radians(nagl) )*ray
        opp=math.sin( math.radians(nagl) )*ray
        posv=[rx(800)+adj,ry(150)+opp]
    elif agl >= 180 and agl < 270:
        nagl=-agl-180
        adj=math.cos( math.radians(nagl) )*ray
        opp=math.sin( math.radians(nagl) )*ray
        posv=[rx(800)-opp,ry(150)+adj]
    else:
        nagl=-agl-270
        adj=math.cos( math.radians(nagl) )*ray
        opp=math.sin( math.radians(nagl) )*ray
        posv=[rx(800)-adj,ry(150)-opp]
    fenetre.blit( mycar.img_cvit , [rx(700),ry(50)])
    pygame.draw.line(fenetre,(200,200,255),(rx(800),ry(150)),posv,3)
    pygame.draw.rect(fenetre,(150,150,150),(rx(740),ry(130),rx(100),ry(40)),0)
    pygame.draw.rect(fenetre,(0,0,0),(rx(740),ry(130),rx(100),ry(40)),rx(2))
    fenetre.blit( font2.render(str(int(mycar.vitesse_actuelle))+" km/h",True,(0,155,0)) , [rx(745),ry(140)])
    #minimape
    fenetre.blit( imgminimape , [pmmx,pmmy])
    pygame.draw.rect(fenetre,(0,0,0),(pmmx,pmmy,tmmx,tmmy),rx(2))
    pygame.draw.circle(fenetre,(0,100,255),( pmmx+int(mycar.px/(mape.shape[0]*tc)*tmmx) , pmmy+int(mycar.py/(mape.shape[1]*tc)*tmmy) ),rx(3),0)
    pygame.draw.circle(fenetre,(0,0,0),( pmmx+int(mycar.px/(mape.shape[0]*tc)*tmmx) , pmmy+int(mycar.py/(mape.shape[1]*tc)*tmmy) ),rx(3),rx(1))
    #texte
    fenetre.blit( font2.render("vitesse : "+str(mycar.vitesse_actuelle)[:5],True,(255,255,255)) , [rx(15),ry(15)] )
    fenetre.blit( font2.render("px : "+str(mycar.px)[:5],True,(255,255,255)) , [rx(15),ry(35)] )
    fenetre.blit( font2.render("py : "+str(mycar.py)[:5],True,(255,255,255)) , [rx(15),ry(55)] )
    fenetre.blit( font2.render("agl : "+str(mycar.agl)[:5],True,(255,255,255)) , [rx(15),ry(75)] )
    fenetre.blit( font1.render("fps : "+str(fps),True,(255,255,255)) , [tex-rx(55),ry(15)] )
    pygame.display.update()


def verif_keys(car):
    if not car.fini:
        key=pygame.key.get_pressed()
        if key[K_UP]: car.bouger("up")
        if key[K_DOWN]: car.bouger("down")
        if key[K_LEFT]: car.bouger("left")
        if key[K_RIGHT]: car.bouger("right")
        if key[K_SPACE]: car.bouger("space")
    return car

def course():
    fm=random.choice( os.listdir(dmape) )
    mape=load_mape(fm)
    #
    img=Image.new("RGBA",[mape.shape[0],mape.shape[1]],(0,0,0,0))
    im=img.load()
    for x in range(mape.shape[0]):
        for y in range(mape.shape[1]):
            if mape[x,y] in [1,4,5]: im[x,y]=(155,155,155,255)
            elif mape[x,y]==2: im[x,y]=(0,0,0,255)
            elif mape[x,y] in [3,6]: im[x,y]=(255,255,255,255)
    img.save("mape.png")
    imgminimape=pygame.transform.scale(pygame.image.load("mape.png"),[tmmx,tmmy])
    #
    cdeb=[]
    cfin=[]
    for x in range(mape.shape[0]):
        for y in range(mape.shape[1]):
            if mape[x,y]==4: cdeb.append( [x,y] )
            elif mape[x,y]==6: cfin.append( [x,y] )
    nbvoit=1
    cars=[]
    pdebdc=[]
    for x in range(nbvoit):
        pc=random.choice(cdeb)
        while pc in pdebdc and len(pdebdc) < len(cdeb): pc=random.choice(cdeb)
        pcx,pcy=pc[0]*tc,pc[1]*tc
        cars.append( Car(pcx,pcy,1,90) )
    finis=[]
    mycar=cars[0]
    cam=[-mycar.px+tex/2,-mycar.py+tey/2]
    tmx,tmy=100,100
    fps=0
    fini=False
    encour=True
    while encour:
        t1=time.time()
        for c in cars:
            c.update(mape)
            rc=pygame.Rect(c.px,c.py,c.tx,c.ty)
            for ca in cfin:
                r=pygame.Rect(ca[0]*tc,ca[1]*tc,tc,tc)
                if rc.colliderect(r):
                    finis.append( c )
                    c.fini=True
        mycar=verif_keys(mycar)
        cam=[-mycar.px+tex/2,-mycar.py+tey/2]
        aff(mape,cars,mycar,cam,fps,imgminimape)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                mycar.isacc=True
            elif event.type==KEYUP:
                mycar.isacc=False
        if len(finis)==len(cars):
            encour=False
            fini=True
        t2=time.time()
        tt=t2-t1
        if tt!=0: fps=int(1./tt)
    ###
    if fini:
        fenetre.fill((0,0,0))
        fenetre.blit( font5.render("Fini",True,(255,255,255)) , [rx(300),ry(150)])
        pygame.display.update()
        encour2=True
        while encour2:
            for event in pygame.event.get():
                if event.type==QUIT: exit()
                elif event.type==KEYDOWN:
                    if event.key==K_ESCAPE: encour2=False

def aff_m():
    fenetre.fill( (0,0,0) )
    pygame.display.update()

def menu():
    encour=True
    while encour:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==K_KEY:
                if event.key==K_ESCAPE: encour=False
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()

course()



