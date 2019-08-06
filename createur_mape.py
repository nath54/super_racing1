#coding:utf-8
import pygame,time,numpy,os
from pygame.locals import *

pygame.init()
tex,tey=1280,720
fenetre=pygame.display.set_mode([tex,tey])
font=pygame.font.SysFont("Arial",20)
pygame.key.set_repeat(40,30)

dimg="images/"
tc=100

emape=[]
emape.append( ["herbe",75,pygame.transform.scale(pygame.image.load(dimg+"herbe.png"),[tc,tc])] )
emape.append( ["route",100,pygame.transform.scale(pygame.image.load(dimg+"route.png"),[tc,tc])] )
emape.append( ["mur1",False,pygame.transform.scale(pygame.image.load(dimg+"mur1.png"),[tc,tc])] )
emape.append( ["départ",100,pygame.transform.scale(pygame.image.load(dimg+"arive.png"),[tc,tc])] )
emape.append( ["place depart",100,pygame.transform.scale(pygame.image.load(dimg+"place_dep.png"),[tc,tc])] )
emape.append( ["route2",100,pygame.transform.scale(pygame.image.load(dimg+"route2.png"),[tc,tc])] )
emape.append( ["arivée",100,pygame.transform.scale(pygame.image.load(dimg+"arrivee.png"),[tc,tc])] )
#0=nom 1=pmd 2=img

def load():
    f=open("mape.nath","r").readlines()
    tx=len(f[0])
    ty=len(f)
    mape=numpy.zeros([tx,ty],dtype=int)
    for x in range(tx-1):
        for y in range(ty-1):
            mape[x,y]=int(f[y][x])
    return mape

def save(mape):
    txt=""
    for x in range(mape.shape[0]):
        for y in range(mape.shape[1]):
            try:txt+=str(mape[y,x])
            except: pass
        txt+="\n"
    f=open("mape.nath","w")
    f.write(txt)
    f.close()

def aff(mape,tcurs,pos,emap,cam,tc):
    fenetre.fill((0,0,0))
    for x in range(int((-cam[0])/tc),int((-cam[0]+tex)/tc+1)):
        for y in range(int((-cam[1])/tc),int((-cam[1]+tey)/tc+1)):
            if x>=0 and x < mape.shape[0] and y >= 0 and y < mape.shape[1]:
                fenetre.blit(emape[mape[x,y]][2],[cam[0]+x*tc,cam[1]+y*tc])
    px=int(pos[0]/tc)*tc
    py=int(pos[1]/tc)*tc
    for x in range(-tcurs,tcurs+1):
        for y in range(-tcurs,tcurs+1):
            pygame.draw.rect(fenetre,(0,0,200),(px+x*tc,py+y*tc,tc,tc),2)
    pygame.draw.rect(fenetre,(0,0,0),(0,0,150,200),0)
    fenetre.blit( emape[emap][2] , [10,10])
    fenetre.blit( font.render(emape[emap][0],True,(255,255,255)) , [10,120])
    pygame.display.update()

def main():
    tc=100
    mtx,mty=100,100
    if "mape.nath" in os.listdir("./"): mape=load()
    else:
        mape=numpy.zeros([mtx,mty],dtype=int)
        for x in range(mtx):
            for y in range(mty):
                mape[x,y]=0
    tcurs=0
    cam=[0,0]
    emap=1
    dcm=time.time()
    tcm=0.5
    isclick=False
    encour=True
    while encour:
        pos=pygame.mouse.get_pos()
        aff(mape,tcurs,pos,emap,cam,tc)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                if time.time()-dcm>=tcm:
                    dcm=time.time()
                    if event.key==K_PAGEDOWN:
                        emap+=1
                        if emap>=len(emape): emap-=1
                    elif event.key==K_PAGEUP:
                        emap-=1
                        if emap<0: emap=0
                if event.key==K_UP: cam[1]+=tc
                elif event.key==K_DOWN: cam[1]-=tc
                elif event.key==K_LEFT: cam[0]+=tc
                elif event.key==K_RIGHT: cam[0]-=tc
                elif event.key==K_s: save(mape)
                elif event.key==K_END and tc>20:
                    tc-=1
                    for m in emape: m[2]=pygame.transform.scale(m[2],[tc,tc])
                elif event.key==K_HOME and tc<500:
                    tc+=1
                    for m in emape: m[2]=pygame.transform.scale(m[2],[tc,tc])
                elif event.key==K_r:
                    for x in range(mtx):
                        for y in range(mty):
                            mape[x,y]=0
            elif event.type==MOUSEBUTTONDOWN: isclick=True
            elif event.type==MOUSEBUTTONUP:
                isclick=False
                if event.button==5 and tcurs>0: tcurs-=1
                elif event.button==4 and tcurs<50: tcurs+=1
        if isclick:
            px=int((pos[0]-cam[0])/tc)
            py=int((pos[1]-cam[1])/tc)
            for x in range(-tcurs,tcurs+1):
                for y in range(-tcurs,tcurs+1):
                    xx,yy=x+px,y+py
                    if xx >= 0 and xx < mtx and yy >= 0 and yy < mty:
                        mape[xx,yy]=emap

main()

