#!/usr/bin/env python3
'''
    This file is part of Fantasy City Planner.
    Fantasy City Planner is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Fantasy City Planner is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Fantasy City Planner.  If not, see <http://www.gnu.org/licenses/>.

    @author DangerBlack
    @version 1.0

'''
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from random import randrange
from multiprocessing import Pool
from functools import partial
import os
import pickle
import parser

from rect import Point
from rect import Rect
from hull import *
from resources import *
from defaults import *
from config import *


config = load_config_file()
places = load_yaml_file('places.yaml')
resources = load_yaml_file('resources.yaml')

print(config)
print(places)
print(resources)

print(config['MIN_PLACE_SIZE'])
FONT_SIZE=20

FONT_LIST=("MedievalSharp-Oblique.ttf", "OldLondon.ttf", "Ruritania.ttf")
FONT_DIR="fonts/"
font = ImageFont.truetype(FONT_DIR+FONT_LIST[0], FONT_SIZE)

#THIS IS ONLY FOR HUMAN READABLE USAGE
KIND_OF_RESOURCES=('WOOD','FISH','LEATHER','PIG','HORSE','CAVE','SILK','WOOL')

#PARAMETRI DI CONFIGURAZIONE INIZIALE DELLO SCRIPT
METER_PIXEL_RATIO=0.5

CITY_NAME="Carcosa"
CITY_SIZE_X=300
CITY_SIZE_Y=300

#london dc => 15'000 inhabitants  530m*530m

#london 1100dc => 15'000 inhabitants  530m*530m   = .0534 people/m^2
#london 1300dc => 80'000 inhabitants  1500m*1000m = .0533 people/m^2

PEOPLE_PER_METER_SQ = 80000/(1500*1000)

SUGGESTED_INHABITANTS_BY_LONDON=int((CITY_SIZE_X * CITY_SIZE_Y * METER_PIXEL_RATIO**2) * PEOPLE_PER_METER_SQ)

print("Suggested inhabitants: "+str(SUGGESTED_INHABITANTS_BY_LONDON))

INHABITANTS=640
INHABITANTS=SUGGESTED_INHABITANTS_BY_LONDON

RESOURCES=['WOOD','FISH','LEATHER','HORSE','WALL','CAVE']
WEALTH=6 #1-10
PLACES=['CASTLE','SANCTUARY','CHURCH']
DEFENCE=1 #1-10
SEA=("NO","NO","NO","NO")

MAX_PLACE_SIZE=20
MIN_PLACE_SIZE=6

DEFAULT_COLOR='#505050'

WOOD_SPREADING=3


#deduct from resources and find inconsistency!
resource_consistency_check(PLACES, RESOURCES, WEALTH, INHABITANTS)

#end consistency checker

#get defaults

defaultPlace = get_default_places(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH)
defaultResurce = get_default_resurces(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH) 


def createPlaceFree():
    p1=Point(random.randint(0,CITY_SIZE_X), random.randint(0,CITY_SIZE_Y))
    p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),   random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
    place=Rect(p1,p2)
    return place

def eval_eqn(string):
    #print("In -> "+str(string))
    code=parser.expr(str(string)).compile()
    evaluated=eval(code)
    #print("Out-> ",str(evaluated))
    return evaluated


def createPlaceDefault(p,name):

    if not name in list(defaultPlace.keys()):
        name='unknown'

    MIN_PLACE_SIZE=config['MIN_PLACE_SIZE']
    MAX_PLACE_SIZE=config['MAX_PLACE_SIZE']
    WEALTH=config['WEALTH']

    mps=eval_eqn(defaultPlace[name][0])
    MPS=eval_eqn(defaultPlace[name][1])

    print(mps,MPS)

    if(defaultPlace[name][2]=='free'):
        p1=Point(random.randint(0,CITY_SIZE_X),random.randint(0,CITY_SIZE_Y))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='center'):
        p1=Point(random.randint(p.x-MPS,p.x+MPS),random.randint(p.y-MPS,p.y+MPS))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='urban'):
        p1=Point(random.randint(int(p.x-int(CITY_SIZE_X/3)-MPS),int(p.x+int(CITY_SIZE_X/3)+MPS)),random.randint(int(p.y-int(CITY_SIZE_Y/3)-MPS),p.y+int(CITY_SIZE_Y/3)+MPS))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='rural'):
        p1=Point(random.randint(int(p.x-int(CITY_SIZE_X/3)-MPS),int(p.x+int(CITY_SIZE_X/3)+MPS)),random.randint(int(p.y-int(CITY_SIZE_Y/3)-MPS),p.y+int(CITY_SIZE_Y/3)+MPS))
        if(random.randint(0,1)==0):
            p1.x=p1.x+int(CITY_SIZE_X/3)
        else:
            p1.x=p1.x-int(CITY_SIZE_X/3)
        if(random.randint(0,1)==0):
            p1.y=p1.y+int(CITY_SIZE_Y/3)
        else:
            p1.y=p1.y-int(CITY_SIZE_Y/3)
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    place=Rect(p1,p2)
    return place


def createPlacePoint(p):
    p1=Point(random.randint(p.x-MAX_PLACE_SIZE*WEALTH,p.x+MAX_PLACE_SIZE*WEALTH),random.randint(p.y-MAX_PLACE_SIZE*WEALTH,p.y+MAX_PLACE_SIZE*WEALTH))
    p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),   random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
    place=Rect(p1,p2)
    return place


def createPlace(old_place):
    p1=Point(random.randint(old_place.top_left().x-MAX_PLACE_SIZE,old_place.top_left().x+MAX_PLACE_SIZE),   random.randint(old_place.top_left().y-MAX_PLACE_SIZE,old_place.top_left().y+MAX_PLACE_SIZE))
    p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),   random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
    place=Rect(p1,p2)
    return place


def createNatureFree(dx,dy):
    p1=Point(random.randint(0,CITY_SIZE_X), random.randint(0,CITY_SIZE_Y))
    p2=Point(p1.x+dx,p1.y+dy)
    place=Rect(p1,p2)
    return place


def createNature(old_place,sx,sy,dx,dy):
    p1=Point(random.randint(old_place.top_left().x-sx-dx,old_place.top_left().x+sx+dx), random.randint(old_place.top_left().y-sy-dy,old_place.top_left().y+sy+dy))
    p2=Point(p1.x+dx,p1.y+dy)
    place=Rect(p1,p2)
    return place


def createPolygonFromRect(r,ndot):
    upper=[]
    downer=[]
    lefter=[]
    righter=[]
    for x in range(r.left,r.right,5):
        upper.append([x,r.top])
    for x in range(r.right,r.left,-5):
        downer.append([x,r.bottom])
    for y in range(r.bottom,r.top,-5):
        lefter.append([r.left,y])
    for y in range(r.top,r.bottom,5):
        righter.append([r.right,y])
    ptop=r.top
    for u in upper:
        ptop=ptop+random.randint(-2,2)
        if(ptop<r.top):
            ptop=r.top
        u[1]=ptop

    pbot=r.bottom
    for u in downer:
        pbot=pbot+random.randint(-2,2)
        if(pbot>r.bottom):
            pbot=r.bottom
        u[1]=pbot

    pleft=r.left
    for u in lefter:
        pleft=pleft+random.randint(-2,2)
        if(pleft<r.left):
            pleft=r.left
        u[0]=pleft

    pright=r.right
    for u in righter:
        pright=pright+random.randint(-2,2)
        if(pright>r.right):
            pright=r.right
        u[0]=pright
    polygon=[]
    for u in upper:
        polygon.append((u[0],u[1]))
    for u in righter:
        polygon.append((u[0],u[1]))
    for u in downer:
        polygon.append((u[0],u[1]))
    for u in lefter:
        polygon.append((u[0],u[1]))
    return polygon


def perimetralWall(house_pure):
    points=[]
    for h in house_pure:
        info=getDefaultPlace(h.name, defaultPlace)
        if(h.name=='HOUSE') or (not info[2]=='rural') or (not info[2]=='free'):
            dx=h.right-h.left
            dy=h.bottom-h.top
            x=h.left-dx
            y=h.top-dy
            if(x>CITY_SIZE_X/2):
                x=h.right+dx
            if(y>CITY_SIZE_Y/2):
                y=h.bottom+dy
            points.append((x,y))
    perim=convex_hull(points)
    perim.append(perim[0])
    return perim

homeNumberMax=int(INHABITANTS/(15-WEALTH))#dai 15 abitandi per casa di 49 mquadri <-> 5 abitanti per casa di 400 mquadri | 1000/9 => 111 house
homeNumberMin=int(INHABITANTS/(12-WEALTH))#dai 12 abitanti per casa di 49 mquadri <-> 2 abitanti per casa di 400 mquadri | 1000/6 => 166 house
homeNumber=random.randint(homeNumberMax,homeNumberMin)


print('This city needs '+str(homeNumber)+' house' + ("s" if homeNumber>1 else ""))

#homeNumber=5

buildings=[]

nature=[]


print('Building forest')
if('WOOD' in RESOURCES):
    for i in range(0,15):
        element=createNatureFree(3,3)
        element.set_name('WOOD')
        nature.append(element)
        
    for i in range(0,200*WEALTH):
        element=createNature(nature[random.randint(0,len(nature)-1)],3,3,3,3)
        element.set_name('WOOD')
        nature.append(element)
    
    touch=0 
    while(touch<WOOD_SPREADING):
        touch=touch+1
        print('*', end=' ')
        for place in nature:        
            for place2 in nature:
                if(not (id(place)==id(place2))):
                    if(place.overlaps(place2)):
                        place.move(random.randint(0,4),random.randint(20,30))   
print('[10/10]')
print('Building river')

for p in range(0,RESOURCES.count('RIVERX')):
    rivert=[]
    liney=random.randint(0,CITY_SIZE_Y)
    river_size=random.randint(3,120)
    for i in range(0,CITY_SIZE_X):
        element=Rect(Point(i,liney),Point(i,liney+river_size))
        element.set_name('RIVER')
        rivert.append(element)
    
    prev=0;
    for f in rivert:
        prev=prev+random.randint(-1,1)
        f.move(1,prev)
    nature.extend(rivert)

for p in range(0,RESOURCES.count('RIVERY')):
    rivert=[]
    linex=random.randint(0,CITY_SIZE_X)
    river_size=random.randint(3,120)
    for i in range(0,CITY_SIZE_Y):
        element=Rect(Point(linex,i),Point(linex+river_size,i))
        element.set_name('RIVER')
        rivert.append(element)  
    prev=0;
    for f in rivert:
        prev=prev+random.randint(-1,1)
        f.move(2,prev)
    nature.extend(rivert)       

for p in range(0,RESOURCES.count('CAVE')):
    p=Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2))
    MPS=200
    mps=30
    if(random.randint(0,1)==0):
        p1=Point(random.randint(0,int(CITY_SIZE_X/3)),random.randint(0,CITY_SIZE_Y))
    else:
        p1=Point(random.randint(0,CITY_SIZE_X),random.randint(0,int(CITY_SIZE_Y/3)))
    p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))
    place=Rect(p1,p2)
    place.set_name('CAVE')
    nature.append(place)

def contains(l, e):
    for x in l:
        if x.name==e:
            return True
    return False
    
print('Building the house')
#CREAZIONE EDIFICI
PLACESN=list(PLACES)
PLACES2=list(PLACES)
for i in range(0,len(PLACESN)):
    #place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
    info=getDefaultPlace(PLACESN[i], defaultPlace)
    
    if(not (info[2]=='rural') or (info[2]=='free')):
        #se no e gia tra gli edifici aggiungilo e rimuovlo
        #se non e tra gli edifici saltalo
        if(not contains(buildings, PLACESN[i])):        
            place=createPlaceDefault(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)),PLACESN[i])
            place.set_name(PLACESN[i])
            buildings.append(place)
            PLACES2.remove(PLACESN[i])
        else:
            pass
PLACESN=PLACES2            

print('Building free house')
for i in range(0,int((homeNumber/20))-len(buildings)):
    place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
    buildings.append(place)

old_town=homeNumber//100*20
new_town=homeNumber//100*80

print('Old city will have '+str(old_town)+' house')


def deduce_direction(field,duty):
    YY=field[0]
    XX=field[1]
    direction=[0,1,2,3]
    if XX==0 and YY==0:
        direction.remove(2)
        direction.remove(3)
    if XX==1 and YY==0:
        direction.remove(0)
        direction.remove(3)
    if XX==0 and YY==1:
        direction.remove(2)
        direction.remove(1)
    if XX==1 and YY==1:
        direction.remove(0)
        direction.remove(1)
    return direction


def get_direction(field,duty):
    direction=[0,1,2,3]
    if(duty>0.1) and (duty*random.random()>0.5):
            direction=deduce_direction(field,duty)
    return direction[random.randint(0,len(direction)-1)]


#THIS METHOD IS DONE PARALLEL DUE TO THE HUGE AMOUNT OF WORK!
def conflictSolver(field,buildings,area,duty):
    top=[]
    left=[]
    right=[]
    bottom=[]
    touch=False
    while(not touch):
        touch=True
        for place in list(buildings):
            for place2 in list(buildings):
                if(not (id(place)==id(place2))):
                    if(place.overlaps(place2)):
                        if(place.name=='HOUSE'):
                            place.move(get_direction(field,duty),random.randint(0,int(MAX_PLACE_SIZE)))
                            if(not area.overlaps(place)):
                                tripla=random.randint(0,100)
                                #print('mi spingo fuori '+str(tripla))
                                if(place.top<area.top):
                                    top.append(place)
                                else:
                                    if(place.left<area.left):
                                        left.append(place)
                                    else:
                                        if(place.right>area.right):
                                            right.append(place)
                                        else:
                                            if(place.bottom>area.bottom):
                                                bottom.append(place)
                                            else:
                                                print('Martin you are not thinking quadrimensionally '+str(tripla))
                                                print(str(place)+' '+str(tripla))
                                                print(str(area)+' '+str(tripla))
                                if(place in buildings):
                                    buildings.remove(place)
                            touch=False
                            break
                        else:
                            place2.move(get_direction(field,duty),random.randint(0,int(MAX_PLACE_SIZE)))
                            if(not area.overlaps(place2)):
                                tripla=random.randint(0,100)
                                #print('mi spingo fuori '+str(tripla))
                                if(place2.top<area.top):
                                    top.append(place2)
                                else:
                                    if(place2.left<area.left):
                                        left.append(place2)
                                    else:
                                        if(place2.right>area.right):
                                            right.append(place2)
                                        else:
                                            if(place2.bottom>area.bottom):
                                                bottom.append(place2)
                                            else:
                                                print('Martin you are not thinking quadrimensionally '+str(tripla))
                                                print(str(place2)+' '+str(tripla))
                                                print(str(area)+' '+str(tripla))
                                if(place2 in buildings):
                                    buildings.remove(place2)
                            touch=False
                            break
    return (field,buildings,top,left,right,bottom)


def generaPlace(buildings,homeNumber):
    for i in range(0,int(homeNumber)):
        old_place=buildings[random.randint(0,len(buildings)-1)]
        place=createPlace(old_place)
        buildings.append(place)
    return buildings


def map_all_and_work(zone,duty):
    workers=[]
    pool = Pool()
    nw=Rect(Point(0,0),Point(CITY_SIZE_X/2,CITY_SIZE_Y/2))
    ne=Rect(Point(CITY_SIZE_X/2,0),Point(CITY_SIZE_X,CITY_SIZE_Y/2))
    sw=Rect(Point(0,CITY_SIZE_Y/2),Point(CITY_SIZE_X/2,CITY_SIZE_Y))
    se=Rect(Point(CITY_SIZE_X/2,CITY_SIZE_Y/2),Point(CITY_SIZE_X,CITY_SIZE_Y))
    workers.append(pool.apply_async(conflictSolver,[(0,0),zone[0][0],nw,duty]))
    workers.append(pool.apply_async(conflictSolver,[(0,1),zone[0][1],ne,duty]))
    workers.append(pool.apply_async(conflictSolver,[(1,0),zone[1][0],sw,duty]))
    workers.append(pool.apply_async(conflictSolver,[(1,1),zone[1][1],se,duty]))

    pool.close()
    pool.join()
    zone=[[[],[]],[[],[]]]
    scambi=False
    bimbi_perduti=0
    for w in workers:
        res=w.get()
        #print(res)
        #print("index x:" +str(res[0][0]))
        #print("index y:" +str(res[0][1]))
        zone[res[0][0]][res[0][1]].extend(res[1])
        YY=res[0][0]
        XX=res[0][1]
        if((YY-1)>=0):#top
            if(len(res[2])>0):
                scambi=True
            zone[YY-1][XX].extend(res[2])
        else:
            bimbi_perduti=bimbi_perduti+len(res[2])
        if((XX-1)>=0):#left
            if(len(res[3])>0):
                scambi=True
            zone[YY][XX-1].extend(res[3])
        else:
            bimbi_perduti=bimbi_perduti+len(res[3])
        if((XX+1)<=1):#right
            if(len(res[4])>0):
                scambi=True
            zone[YY][XX+1].extend(res[4])
        else:
            bimbi_perduti=bimbi_perduti+len(res[4])
        if((YY+1)<=1):#bottom
            if(len(res[5])>0):
                scambi=True
            zone[YY+1][XX].extend(res[5])
        else:
            bimbi_perduti=bimbi_perduti+len(res[5])

    #print('abbiamo perso n '+str(bimbi_perduti))
    return (zone,scambi)


def not_less_bounds(number,lower,upper):
    if(number<lower):
        return lower
    if(number>upper):
        return upper
    return number


def test_temp(yy,xx,place):
    nw=Rect(Point(0,0),Point(CITY_SIZE_X/2,CITY_SIZE_Y/2))
    ne=Rect(Point(CITY_SIZE_X/2,0),Point(CITY_SIZE_X,CITY_SIZE_Y/2))
    sw=Rect(Point(0,CITY_SIZE_Y/2),Point(CITY_SIZE_X/2,CITY_SIZE_Y))
    se=Rect(Point(CITY_SIZE_X/2,CITY_SIZE_Y/2),Point(CITY_SIZE_X,CITY_SIZE_Y))
    if(xx==0)and(yy==0):
        if(not nw.overlaps(place)):
            print('errore micidiale 1');
    if(xx==0)and(yy==1):
        if(not ne.overlaps(place)):
            print('errore micidiale 2');
    if(xx==1)and(yy==0):
        if(not sw.overlaps(place)):
            print('errore micidiale 3');
    if(xx==1)and(yy==1):
        if(not se.overlaps(place)):
            print('errore micidiale 4');


def mappa_zone(buildings):
    zone=[ [[], []], [[], []] ]
    for place in buildings:
        yy=not_less_bounds(int(place.top/(CITY_SIZE_Y/2)),0,1)
        xx=not_less_bounds(int(place.left/(CITY_SIZE_X/2)),0,1)
        test_temp(xx,yy,place)
        zone[yy][xx].append(place)

    scambi=True
    duty=0
    while scambi:
        #print('Faccio iterazione')
        res=map_all_and_work(zone,duty)
        zone=res[0]
        scambi=res[1]
        duty=duty+0.1

    print("Duty in my job:"+str(duty))
    buildings=[]
    for row in zone:
        for col in row:
            buildings.extend(col)
    return buildings


#--------------------------------------------------------------------------

buildings=generaPlace(buildings,old_town)

buildings=mappa_zone(buildings)

print('Old city has '+str(len(buildings))+' instead of '+str(old_town))
perim=()
if( 'WALL' in RESOURCES ):
    perim= perimetralWall(buildings)


#CREAZIONE EDIFICI RURALI

for i in range(0,len(PLACESN)):
    #place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
    #if(defaultPlace[PLACES[i]][2]=='rural') or (defaultPlace[PLACES[i]][2]=='free'):
    place=createPlaceDefault(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)),PLACESN[i])
    place.set_name(PLACESN[i])
    buildings.append(place)

buildings=generaPlace(buildings,new_town)
buildings=mappa_zone(buildings)

print('Controllo conflitti natura')
for place in list(buildings):
    for n in list(nature):
        if(place.overlaps(n)):
            if(defaultResurce[n.name][1]=='removable'):
                nature.remove(n)
            else:
                if(place.name=='HOUSE'):
                    try:
                        buildings.remove(place)
                    except ValueError as e:
                        pass
                else:
                    print('muovo a nord '+place.name+' di : '+str(n.top-place.top))
                    place.move(1,n.top-place.top)

for place in list(buildings):
    for place2 in list(buildings):
        if(not (id(place)==id(place2))):
            if(place.overlaps(place2)):
                if(place.name=='HOUSE'):
                    if(place in buildings):
                        buildings.remove(place)
                else:
                    if(not place2.name=='HOUSE'):
                        r=random.randint(0,1)
                        if(r==0):
                            place.move(0,place.right-place.left+place2.right-place2.left)
                        if(r==1):
                            place.move(1,place.bottom-place.top+place2.bottom-place2.top)

print('The city has '+str(len(buildings))+
      ' instead of '+str(homeNumber)+
      ' suggested inhabitants '+str(len(buildings)*(14-WEALTH)))



#FINE CREAZIONE EDIFICI

#INIZIO STAMPA

LIGHT_PLACES=list(set(PLACES))
LIGHT_PLACES=sorted(LIGHT_PLACES)
print(LIGHT_PLACES)
print(len(LIGHT_PLACES))
WIDTH_LEGEND=len(LIGHT_PLACES)*FONT_SIZE/CITY_SIZE_Y+1;
print('servirebbero +'+str(WIDTH_LEGEND)+' COLONNE')

#GENERA DIMENSIONE TESTO LEGENDA SU MAPPA
maxsize=1
for i in range(0,len(PLACES)):
    if(font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]>maxsize):
        maxsize=font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]
maxsize=maxsize+30

CITY_SIZE_X_TRUE=CITY_SIZE_X+maxsize*WIDTH_LEGEND

img = Image.new( 'RGB', (int(CITY_SIZE_X_TRUE),int(CITY_SIZE_Y)), "#C8C8C8") # create a new black image
pixels = img.load() # create the pixel map
draw = ImageDraw.Draw(img)


#STAMPA NATURA
for n in nature:
    if(not n.name=='CAVE'):
        draw.rectangle(n.get_list(), fill=defaultResurce[n.name][0])
    else:
        draw.polygon(createPolygonFromRect(n,5), fill=defaultResurce[n.name][0])

#STAMPA CINTA MURARIA
draw.line(perim,width=2,fill='#1A1A1A');

#STAMPA EDIFICI
for place in buildings:
    color=DEFAULT_COLOR;
    if(not place.name=='HOUSE'):
        info=getDefaultPlace(place.name, defaultPlace)
        color=info[3]
        draw.rectangle(place.get_list(), outline=DEFAULT_COLOR, fill=color )
        draw.text((place.top_left().x+5,place.top_left().y),place.name[0:1],fill="red",font=font)
    else:
        draw.rectangle(place.get_list(), outline=color)



#STAMPA LEGENDA
draw.rectangle((CITY_SIZE_X_TRUE-maxsize*WIDTH_LEGEND-5,5,CITY_SIZE_X_TRUE-5,CITY_SIZE_Y-5), fill='white' )
draw.rectangle((CITY_SIZE_X_TRUE-maxsize*WIDTH_LEGEND-5,5,CITY_SIZE_X_TRUE-5,CITY_SIZE_Y-5), outline='black' )

LEFT=WIDTH_LEGEND
TOP=0
for i in range(0,len(LIGHT_PLACES)):
    if((TOP*(FONT_SIZE+1)+10)>CITY_SIZE_Y):
        TOP=0
        LEFT=LEFT-1
    info=getDefaultPlace(LIGHT_PLACES[i], defaultPlace)
    draw.rectangle((CITY_SIZE_X_TRUE-maxsize*LEFT+5,10+TOP*(FONT_SIZE)+1,CITY_SIZE_X_TRUE-maxsize*LEFT+10,10+TOP*(FONT_SIZE)+FONT_SIZE-2),fill=info[3])
    draw.text((CITY_SIZE_X_TRUE-maxsize*LEFT+15,10+TOP*(FONT_SIZE)),LIGHT_PLACES[i][0:1]+": "+LIGHT_PLACES[i].lower().title(),fill="red",font=font)
    TOP=TOP+1


LUNGHEZZA_CAMPIONE=200
draw.line((CITY_SIZE_X-5-LUNGHEZZA_CAMPIONE,CITY_SIZE_Y-10,CITY_SIZE_X-5,CITY_SIZE_Y-10),width=2,fill='red');
TEXT=str(METER_PIXEL_RATIO*LUNGHEZZA_CAMPIONE)+' m'
draw.text((CITY_SIZE_X-LUNGHEZZA_CAMPIONE+LUNGHEZZA_CAMPIONE/3,CITY_SIZE_Y-10-(FONT_SIZE)),TEXT,fill="red",font=font)

draw.text((10,10),"City of "+CITY_NAME,fill="red",font=font)

#draw.line((CITY_SIZE_X/2,0,CITY_SIZE_X/2,CITY_SIZE_Y),width=1,fill='red');
#draw.line((0,CITY_SIZE_Y/2,CITY_SIZE_X,CITY_SIZE_Y/2),width=1,fill='red');

img.show()


print("Fantasy City Planner has finnished creating the city of "+CITY_NAME)


#SALVA MAPPA
mas=0
while(os.path.isfile('map/mappa_'+str(mas)+'.png')==True):
    mas=mas+1

filename='map/mappa_'+str(mas)
img.save(filename+'.png')

obj=((CITY_SIZE_X,CITY_SIZE_Y),RESOURCES,PLACES,buildings,nature)
f = open(filename+'.map', "wb")
pickle.dump(obj, f)



#im.save(sys.stdout, "PNG")
