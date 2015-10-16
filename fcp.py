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

random.seed(1029384756) # repeatabilty for testing

print(config)
print(places)
print(resources)

FONT_DIR="fonts/"
font_size = config['FONT_SIZE']
font_size_sm = int(font_size*0.75)
font_size_lg = int(font_size*1.25)
font   = ImageFont.truetype(FONT_DIR+config['FONT_LIST'][0], font_size)
fontsm = ImageFont.truetype(FONT_DIR+config['FONT_LIST'][0], font_size_sm)
fontlg = ImageFont.truetype(FONT_DIR+config['FONT_LIST'][0], font_size_lg)

#THIS IS ONLY FOR HUMAN READABLE USAGE
KIND_OF_RESOURCES=('WOOD','FISH','LEATHER','PIG','HORSE','CAVE','SILK','WOOL')

#PARAMETRI DI CONFIGURAZIONE INIZIALE DELLO SCRIPT
METER_PIXEL_RATIO=0.5

if config['INHABITANTS'] is not None:
    INHABITANTS=config['INHABITANTS']
else:
    #london dc => 15'000 inhabitants  530m*530m
    #london 1100dc => 15'000 inhabitants  530m*530m   = .0534 people/m^2
    #london 1300dc => 80'000 inhabitants  1500m*1000m = .0533 people/m^2

    PEOPLE_PER_METER_SQ = 80000/(1500*1000)

    SUGGESTED_INHABITANTS_BY_LONDON=int((config['CITY_SIZE_X'] * config['CITY_SIZE_Y'] * METER_PIXEL_RATIO**2) * PEOPLE_PER_METER_SQ)

    print("Suggested inhabitants: "+str(SUGGESTED_INHABITANTS_BY_LONDON))

    INHABITANTS=SUGGESTED_INHABITANTS_BY_LONDON

print("Current inhabitants: "+str(INHABITANTS))

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
    p1=Point(random.randint(0,config['CITY_SIZE_X']), random.randint(0,config['CITY_SIZE_Y']))
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
        p1=Point(random.randint(0,config['CITY_SIZE_X']),random.randint(0,config['CITY_SIZE_Y']))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='center'):
        p1=Point(random.randint(p.x-MPS,p.x+MPS),random.randint(p.y-MPS,p.y+MPS))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='urban'):
        p1=Point(random.randint(int(p.x-int(config['CITY_SIZE_X']/3)-MPS),int(p.x+int(config['CITY_SIZE_X']/3)+MPS)),random.randint(int(p.y-int(config['CITY_SIZE_Y']/3)-MPS),p.y+int(config['CITY_SIZE_Y']/3)+MPS))
        p2=Point(random.randint(p1.x+mps,p1.x+MPS), random.randint(p1.y+mps,p1.y+MPS))

    if(defaultPlace[name][2]=='rural'):
        p1=Point(random.randint(int(p.x-int(config['CITY_SIZE_X']/3)-MPS),int(p.x+int(config['CITY_SIZE_X']/3)+MPS)),random.randint(int(p.y-int(config['CITY_SIZE_Y']/3)-MPS),p.y+int(config['CITY_SIZE_Y']/3)+MPS))
        if(random.randint(0,1)==0):
            p1.x=p1.x+int(config['CITY_SIZE_X']/3)
        else:
            p1.x=p1.x-int(config['CITY_SIZE_X']/3)
        if(random.randint(0,1)==0):
            p1.y=p1.y+int(config['CITY_SIZE_Y']/3)
        else:
            p1.y=p1.y-int(config['CITY_SIZE_Y']/3)
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

# Creates a rect anywhere on the map, with dimensions (dx,dy)
def createNatureFree(dx,dy):
    p1=Point(random.randint(0,config['CITY_SIZE_X']), random.randint(0,config['CITY_SIZE_Y']))
    p2=Point(p1.x+dx,p1.y+dy)
    place=Rect(p1,p2)
    return place


# Creates a rect with dimensions (dx,dy), relative to the top_left corner of old_place
def createNature(old_place,sx,sy,dx,dy):
    p1=Point( random.randint(old_place.top_left().x-sx-dx, old_place.top_left().x+sx+dx), 
              random.randint(old_place.top_left().y-sy-dy, old_place.top_left().y+sy+dy) )
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
            if(x>config['CITY_SIZE_X']/2):
                x=h.right+dx
            if(y>config['CITY_SIZE_Y']/2):
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


# piantare alcuni alberi
def plantForest(seedlings, wealth, spreading ):

    print('Planting forest')
    nature=[]
    if('WOOD' in RESOURCES):
        print(' Planting %s random seedlings' % seedlings)
        for i in range(0,seedlings):
            element=createNatureFree(3,3)
            element.set_name('WOOD')
            nature.append(element)
            
        print(' Growing forest')
        num_seedlings = len(nature)
        for i in range(0,200*wealth):
            seedling = random.randint(0,num_seedlings-1)
            element=createNature(nature[seedling],3,3,3,3)
            element.set_name('WOOD')
            nature.append(element)
        

        #Move the trees around to enlarge the forest
        touch=spreading
        while(touch):
            touch-=1
            print('*', end=' ')
            for place in nature:        
                for place2 in nature:
                    if(not (id(place)==id(place2))):
                        if(place.overlaps(place2)):
                            # move 20-30 px in the cardinal directions
                            place.move(random.randint(0,4),random.randint(20,30))   
    return nature

nature = plantForest(config['SEEDLINGS'], config['WEALTH'], config['WOOD_SPREADING'])
print('[10/10]')

print('Building river')

for p in range(0,RESOURCES.count('RIVERX')):
    rivert=[]
    liney=random.randint(0,config['CITY_SIZE_Y'])
    river_size=random.randint(3,120)
    for i in range(0,config['CITY_SIZE_X']):
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
    linex=random.randint(0,config['CITY_SIZE_X'])
    river_size=random.randint(3,120)
    for i in range(0,config['CITY_SIZE_Y']):
        element=Rect(Point(linex,i),Point(linex+river_size,i))
        element.set_name('RIVER')
        rivert.append(element)  
    prev=0;
    for f in rivert:
        prev=prev+random.randint(-1,1)
        f.move(2,prev)
    nature.extend(rivert)       

for p in range(0,RESOURCES.count('CAVE')):
    p=Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2))
    MPS=200
    mps=30
    if(random.randint(0,1)==0):
        p1=Point(random.randint(0,int(config['CITY_SIZE_X']/3)),random.randint(0,config['CITY_SIZE_Y']))
    else:
        p1=Point(random.randint(0,config['CITY_SIZE_X']),random.randint(0,int(config['CITY_SIZE_Y']/3)))
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
    #place=createPlacePoint(Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2)))
    info=getDefaultPlace(PLACESN[i], defaultPlace)
    
    if(not (info[2]=='rural') or (info[2]=='free')):
        #se no e gia tra gli edifici aggiungilo e rimuovlo
        #se non e tra gli edifici saltalo
        if(not contains(buildings, PLACESN[i])):        
            place=createPlaceDefault(Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2)),PLACESN[i])
            place.set_name(PLACESN[i])
            buildings.append(place)
            PLACES2.remove(PLACESN[i])
        else:
            pass
PLACESN=PLACES2            

print('Building free house')
for i in range(0,int((homeNumber/20))-len(buildings)):
    place=createPlacePoint(Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2)))
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
    nw=Rect(Point(0,0),Point(config['CITY_SIZE_X']/2,config['CITY_SIZE_Y']/2))
    ne=Rect(Point(config['CITY_SIZE_X']/2,0),Point(config['CITY_SIZE_X'],config['CITY_SIZE_Y']/2))
    sw=Rect(Point(0,config['CITY_SIZE_Y']/2),Point(config['CITY_SIZE_X']/2,config['CITY_SIZE_Y']))
    se=Rect(Point(config['CITY_SIZE_X']/2,config['CITY_SIZE_Y']/2),Point(config['CITY_SIZE_X'],config['CITY_SIZE_Y']))
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
    CX=config['CITY_SIZE_X']
    CY=config['CITY_SIZE_Y']

    # Make 4 rectangles, one for each qudrant
    nw=Rect(Point(0,0), Point(CX//2, CY//2))
    ne=Rect(Point(CX//2,0), Point(CX//2,CY//2))
    sw=Rect(Point(0,CY//2), Point(CX//2,CY))
    se=Rect(Point(CX//2,CY//2), Point(CX,CY))

    if(xx==0)and(yy==0):
        if(not nw.overlaps(place)):
            print('errore micidiale 1 (nw)');
            return False
    if(xx==0)and(yy==1):
        if(not ne.overlaps(place)):
            print('errore micidiale 2 (ne)');
            return False
    if(xx==1)and(yy==0):
        if(not sw.overlaps(place)):
            print('errore micidiale 3 (sw)');
            return False
    if(xx==1)and(yy==1):
        if(not se.overlaps(place)):
            print('errore micidiale 4 (se)');
            return False
    return True


def mappa_zone(buildings):
    zone=[ [[], []], [[], []] ]
    for place in buildings:
        # xx and yy are normalized to [0,1] within the overall image.
        # 
        yy=not_less_bounds(int(place.top/(config['CITY_SIZE_Y']/2)),0,1)
        xx=not_less_bounds(int(place.left/(config['CITY_SIZE_X']/2)),0,1)
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
    #place=createPlacePoint(Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2)))
    #if(defaultPlace[PLACES[i]][2]=='rural') or (defaultPlace[PLACES[i]][2]=='free'):
    place=createPlaceDefault(Point(int(config['CITY_SIZE_X']/2),int(config['CITY_SIZE_Y']/2)),PLACESN[i])
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
print(LIGHT_PLACES, len(LIGHT_PLACES))
WIDTH_LEGEND=int(len(LIGHT_PLACES)*config['FONT_SIZE']/config['CITY_SIZE_Y']+1);
print('servirebbero +'+str(WIDTH_LEGEND)+' COLONNE')

#GENERA DIMENSIONE TESTO LEGENDA SU MAPPA
# get largest dimension of legend text, set the legend width based on that
maxsize=1
for i in range(0,len(PLACES)):
    if(font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]>maxsize):
        maxsize=font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]
maxsize=maxsize+30

CITY_SIZE_X_TRUE=config['CITY_SIZE_X']+maxsize*WIDTH_LEGEND+75  # 75px fudge-factor for buildinsg outside the eastern walls

img = Image.new( 'RGB', (int(CITY_SIZE_X_TRUE),int(config['CITY_SIZE_Y'])), "#C8C8C8") # create a new black image
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
# Label buildings
for place in buildings:
    outline = config['DEFAULT_COLOR']
    fill=None
    if(not place.name=='HOUSE'):
        info=getDefaultPlace(place.name, defaultPlace)
        fill = info[3]

    # Draw the rectangle firsts, so the text is on top.
    draw.rectangle(place.get_list(), outline=outline, fill=fill)

    if(not place.name=='HOUSE'):
        abbr = info[4]
        draw.text(
            (place.top_left().x+3,place.top_left().y),
            abbr,
            fill="red",font=fontsm
        )



#STAMPA LEGENDA
def draw_legend(draw):
    # Draw basic box
    draw.rectangle((CITY_SIZE_X_TRUE-maxsize*WIDTH_LEGEND-5,5,CITY_SIZE_X_TRUE-5,config['CITY_SIZE_Y']-5), fill='white', outline='black' )

    LEFT=WIDTH_LEGEND
    TOP=0

    # loop over sorted places
    for i in range(0,len(LIGHT_PLACES)):

        # move to next column if needed
        if((TOP*(config['FONT_SIZE']+1)+10)>config['CITY_SIZE_Y']):
            TOP=0
            LEFT=LEFT-1

        info=getDefaultPlace(LIGHT_PLACES[i], defaultPlace)

        CSXTL = CITY_SIZE_X_TRUE-maxsize*LEFT
        TFS = 10 + TOP*config['FONT_SIZE']

        # draw a colored box
        draw.rectangle( (
            CSXTL+5, TFS+1,
            CSXTL+10,TFS+config['FONT_SIZE']-2
            ),fill=info[3]
        )

        # Draw text
        label = LIGHT_PLACES[i].lower().title()
        abbr = info[4]
        string = abbr+': '+label
        x=CSXTL+15
        y=TFS
        print(int(x),int(y),"label="+string)
        draw.text( 
            ( x, y ),
            string,
            fill="red",font=font
        )

        TOP+=1

def myround(x, base=5):
    return int(base * round(float(x)/base))

def draw_scale(draw,ratio):
    # scale length, in px
    CX=config['CITY_SIZE_X']
    CY=config['CITY_SIZE_Y']

    LUNGHEZZA_CAMPIONE=min(200, int(ratio*myround(ratio*CX/2)))

    TEXT=str(LUNGHEZZA_CAMPIONE)+' m'
    text_width_px = fontlg.getsize(TEXT)[0]

    draw.line( (CX-LUNGHEZZA_CAMPIONE-5, CY-10, CX-5, CY-10),width=2,fill='red');
    draw.text( (CX-5-(text_width_px+LUNGHEZZA_CAMPIONE)//2, CY-10-int(1.25*config['FONT_SIZE'])-1), TEXT, fill="red", font=fontlg)

def draw_title(draw, name, font):
    draw.text((10,10),"City of "+name,fill="red",font=font)
    #draw.line((config['CITY_SIZE_X']/2,0,config['CITY_SIZE_X']/2,config['CITY_SIZE_Y']),width=1,fill='red');
    #draw.line((0,config['CITY_SIZE_Y']/2,config['CITY_SIZE_X'],config['CITY_SIZE_Y']/2),width=1,fill='red');


draw_legend(draw)
draw_scale(draw,config['METER_PIXEL_RATIO'])
draw_title(draw, config['CITY_NAME'], font)

img.show()


print("Fantasy City Planner has finnished creating the city of "+config['CITY_NAME'])


#SALVA MAPPA
mas=0
while(os.path.isfile('map/mappa_'+str(mas)+'.png')==True):
    mas=mas+1

filename='map/mappa_'+str(mas)
img.save(filename+'.png')

obj=((config['CITY_SIZE_X'],config['CITY_SIZE_Y']),RESOURCES,PLACES,buildings,nature)
f = open(filename+'.map', "wb")
pickle.dump(obj, f)



#im.save(sys.stdout, "PNG")
