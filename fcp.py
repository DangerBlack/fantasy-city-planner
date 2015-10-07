import Image, ImageDraw
import ImageFont
import random
from random import randrange
from rect import Point
from rect import Rect
from hull import *


FONT_SIZE=20

FONT_LIST=("Treamd.ttf","OldLondon.ttf","Ruritania.ttf")

font = ImageFont.truetype(FONT_LIST[0], FONT_SIZE)


#PARAMETRI DI CONFIGURAZIONE INIZIALE DELLO SCRIPT

CITY_NAME="Carcosa"
CITY_SIZE_X=800
CITY_SIZE_Y=600

INHABITANTS=1000
RESOURCES=['WOOD','FISH','LEATHER','HORSE','WALL']
WEALTH=6 #1-10
PLACES=['CASTLE','SANCTUARY','CHURCH']
DEFENCE=1 #1-10
SEA=("NO","NO","NO","NO")

MAX_PLACE_SIZE=20
MIN_PLACE_SIZE=3

DEFAULT_COLOR='#505050'

WOOD_SPREADING=3

METER_PIXEL_RATIO=2

#FINE CONFIGURAZIONE INIZIALE

img = Image.new( 'RGB', (CITY_SIZE_X,CITY_SIZE_Y), "#C8C8C8") # create a new black image
pixels = img.load() # create the pixel map        
draw = ImageDraw.Draw(img)

defaultPlace={}


# center, urban, free, rural, 
defaultPlace['CASTLE']=((MIN_PLACE_SIZE*WEALTH/2),(MAX_PLACE_SIZE*WEALTH)/2,'center','#85DADA')
defaultPlace['MARKET']=(30,20*WEALTH,'center','#FFCC99')
defaultPlace['PARK']=(30,35*WEALTH,'urban','#2EB82E')
defaultPlace['SANCTUARY']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'free','#009999')
defaultPlace['CHURCH']=(MAX_PLACE_SIZE,MAX_PLACE_SIZE*2,'center','#009999')
defaultPlace['CATHEDRAL']=(MAX_PLACE_SIZE,MAX_PLACE_SIZE*3,'center','#009999')
defaultPlace['SAWMILL']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'rural','#333300')#SEGHERIA
defaultPlace['BAKERY']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#FFCC00')
defaultPlace['LEATHER_SHOP']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#CC3300')
defaultPlace['TAILOR_SHOP']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#CC6699')
defaultPlace['STABLE']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#996633')
defaultPlace['ARMOR_SHOP']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#CC3300')
defaultPlace['WEAPON_SHOP']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#0000FF')
defaultPlace['SMITHY']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#0000FF')#FUCINA
defaultPlace['INN']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#CC6600')
defaultPlace['GUILD_OF_WARRIOR']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#666666')
defaultPlace['GUILD_OF_ARTIST']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#00FF99')
defaultPlace['GUILD_OF_THIEF']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#FFFFFF')
defaultPlace['GUILD_OF_MAGE']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#FF9900')
defaultPlace['GUILD_OF_BUILDER']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#FF0000')
defaultPlace['GUILD_OF_HERBALISTS']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#669900')
defaultPlace['GUILD_OF_GOLDSMITH']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#FFFF00')
defaultPlace['GUILD_OF_IRONMONGER']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#5F5F5F')

defaultPlace['THEATRE']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#0066CC')
defaultPlace['ARENA']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#CC0000')
defaultPlace['unknown']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'center','#000066')


defaultResurce={}
defaultResurce['WOOD']=('green','removable')
defaultResurce['RIVER']=('#00CCFF','fixed')
defaultResurce['RIVERX']=('#00CCFF','fixed')
defaultResurce['RIVERY']=('#00CCFF','fixed')
defaultResurce['CAVE']=('#323232','fixed')

#deduct from resources and find inconsistency!

if(('WOOD' in RESOURCES)and(not 'SAWMILL' in PLACES)):
	print('Inconsistenza WOOD but not SAWMILL')
	PLACES.append('SAWMILL')

if(('FISH' in RESOURCES)and((not 'RIVERX' in RESOURCES)and(not 'RIVERY' in RESOURCES))):
	print('inconsistency FISH but not RIVER')
	RESOURCES.append('RIVERX')	
	
if(('FISH' in RESOURCES)and(not 'MARKET' in PLACES)):
	print('inconsistency FISH but not MARKET')
	PLACES.append('MARKET')

if(('LEATHER' in RESOURCES)and(not 'LEATHER_SHOP' in PLACES)):
	print('inconsistency LEATHER but not LEATHER_SHOP')
	PLACES.append('LEATHER_SHOP')
	
if(('HORSE' in RESOURCES)and(not 'STABLE' in PLACES)):
	print('inconsistency HORSE but not STABLE')
	PLACES.append('STABLE')	
	
if(('SILK' in RESOURCES)and(not 'TAILOR_SHOP' in PLACES)):
	print('inconsistency SILK but not TAILOR_SHOP')
	PLACES.append('TAILOR_SHOP')	

if(('WEAPON_SHOP' in PLACES)and(not 'CAVE' in RESOURCES)):
	print('inconsistency WEAPON_SHOP but not CAVE')
	RESOURCES.append('CAVE')
	
if(('SMITHY' in PLACES)and(not 'CAVE' in RESOURCES)):
	print('inconsistency SMITHY but not CAVE')
	RESOURCES.append('CAVE')

if((WEALTH<5)and(not 'SANCTUARY' in PLACES)):
	print('inconsistency ORRIBLE WEALTH but not SANCTUARY')
	PLACES.append('SANCTUARY')

if((WEALTH>4)and(not 'BAKERY' in PLACES)):
	print('inconsistency HUMAN WEALTH but not BAKERY')
	PLACES.append('BAKERY')

if((WEALTH>7)and(not 'INN' in PLACES)):
	print('inconsistency HIGH WEALTH but not INN')
	PLACES.append('INN')

if((WEALTH>7)and(not 'WALL' in PLACES)):
	print('inconsistency HIGH WEALTH but no WALL')
	RESOURCES.append('WALL')

if((WEALTH>3)and(PLACES.count('INN')<WEALTH/2)):
	print('inconsistency FEW INN despite GOOD WEALTH')
	for i in range(0,WEALTH/2-PLACES.count('INN')):
		PLACES.append('INN')
	
if((WEALTH>7)and(not 'MARKET' in PLACES)):
	print('inconsistency HIGH WEALTH but not MARKET')
	PLACES.append('MARKET')

if((WEALTH>7)and(not 'CHURCH' in PLACES)):
	print('inconsistency HIGH WEALTH but not CHURCH')
	PLACES.append('CHURCH')
	
if((WEALTH>7)and(not 'THEATRE' in PLACES)and(INHABITANTS>2000)):
	print('inconsistency HIGH WEALTH but not THEATRE and lot of INHABITANTS')
	PLACES.append('THEATRE')	
	
if((WEALTH>7)and(not 'ARENA' in PLACES)and(INHABITANTS>2500)):
	print('inconsistency HIGH WEALTH but not ARENA and lot of INHABITANTS')
	PLACES.append('ARENA')
	
if((WEALTH>8)and(not 'CATHEDRAL' in PLACES)):
	print('inconsistency VERY HIGH WEALTH but not CATHEDRAL')
	PLACES.append('CATHEDRAL')
	
if((WEALTH>8)and(not 'CASTLE' in PLACES)):
	print('inconsistency VERY HIGH WEALTH but not CASTLE')
	PLACES.append('CASTLE')
	
if((INHABITANTS>3000)and(not 'CASTLE' in PLACES)):
	print('inconsistency VERY HIGH INHABITANTS but not CASTLE')
	PLACES.append('CASTLE')
	
if((INHABITANTS>3000)and(not 'MARKET' in PLACES)):
	print('inconsistency VERY HIGH INHABITANTS but not MARKET')
	PLACES.append('MARKET')
	
#end consistency checker

def createPlaceFree():
	p1=Point(random.randint(0,CITY_SIZE_X),	random.randint(0,CITY_SIZE_Y))
	p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),	random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
	place=Rect(p1,p2)
	return place

def createPlaceDefault(p,name):
	
	if not name in defaultPlace.keys():
		name='unknown'
		
	MPS=defaultPlace[name][1]
	mps=defaultPlace[name][0]
	if(defaultPlace[name][2]=='free'):
		p1=Point(random.randint(0,CITY_SIZE_X),random.randint(0,CITY_SIZE_Y))
		p2=Point(random.randint(p1.x+mps,p1.x+MPS),	random.randint(p1.y+mps,p1.y+MPS))
		
	if(defaultPlace[name][2]=='center'):
		p1=Point(random.randint(p.x-MPS,p.x+MPS),random.randint(p.y-MPS,p.y+MPS))
		p2=Point(random.randint(p1.x+mps,p1.x+MPS),	random.randint(p1.y+mps,p1.y+MPS))
		
	if(defaultPlace[name][2]=='urban'):
		p1=Point(random.randint(int(p.x-int(CITY_SIZE_X/3)-MPS),int(p.x+int(CITY_SIZE_X/3)+MPS)),random.randint(int(p.y-int(CITY_SIZE_Y/3)-MPS),p.y+int(CITY_SIZE_Y/3)+MPS))
		p2=Point(random.randint(p1.x+mps,p1.x+MPS),	random.randint(p1.y+mps,p1.y+MPS))
		
	if(defaultPlace[name][2]=='rural'):
		p1=Point(random.randint(int(p.x-int(CITY_SIZE_X/3)-MPS),int(p.x+int(CITY_SIZE_X/3)+MPS)),random.randint(int(p.y-int(CITY_SIZE_Y/3)-MPS),p.y+int(CITY_SIZE_Y/3)+MPS))
		print("sono qui")	
		if(random.randint(0,1)==0):
			p1.x=p1.x+int(CITY_SIZE_X/3)
		else:
			p1.x=p1.x-(CITY_SIZE_X/3)
		if(random.randint(0,1)==0):
			p1.y=p1.y+int(CITY_SIZE_Y/3)
		else:
			p1.y=p1.y-int(CITY_SIZE_Y/3)
		p2=Point(random.randint(p1.x+mps,p1.x+MPS),	random.randint(p1.y+mps,p1.y+MPS))
		
	place=Rect(p1,p2)
	return place

def createPlacePoint(p):
	p1=Point(random.randint(p.x-MAX_PLACE_SIZE*WEALTH,p.x+MAX_PLACE_SIZE*WEALTH),random.randint(p.y-MAX_PLACE_SIZE*WEALTH,p.y+MAX_PLACE_SIZE*WEALTH))
	p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),	random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
	place=Rect(p1,p2)
	return place
	
def createPlace(old_place):
	p1=Point(random.randint(old_place.top_left().x-MAX_PLACE_SIZE,old_place.top_left().x+MAX_PLACE_SIZE),	random.randint(old_place.top_left().y-MAX_PLACE_SIZE,old_place.top_left().y+MAX_PLACE_SIZE))
	p2=Point(random.randint(p1.x+MIN_PLACE_SIZE,p1.x+MAX_PLACE_SIZE),	random.randint(p1.y+MIN_PLACE_SIZE,p1.y+MAX_PLACE_SIZE))
	place=Rect(p1,p2)
	return place
	
def createNatureFree(dx,dy):
	p1=Point(random.randint(0,CITY_SIZE_X),	random.randint(0,CITY_SIZE_Y))
	p2=Point(p1.x+dx,p1.y+dy)
	place=Rect(p1,p2)
	return place

def createNature(old_place,sx,sy,dx,dy):
	p1=Point(random.randint(old_place.top_left().x-sx-dx,old_place.top_left().x+sx+dx),	random.randint(old_place.top_left().y-sy-dy,old_place.top_left().y+sy+dy))
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
		if(h.name=='HOUSE') or (not defaultPlace[h.name][2]=='rural') or (not defaultPlace[h.name][2]=='free'):
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

#homeNumber=5

buildings=[]

nature=[]


print('Genero le foreste')
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
		print('*'),
		for place in nature:		
			for place2 in nature:
				if(not (id(place)==id(place2))):
					if(place.overlaps(place2)):
						place.move(random.randint(0,4),random.randint(20,30))	
print('[10/10]')
print('Genero i Fiumi')

for p in range(0,RESOURCES.count('RIVERX')):
	rivert=[]
	liney=random.randint(0,CITY_SIZE_Y)
	river_size=random.randint(3,20)
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
	river_size=random.randint(3,20)
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
		p1=Point(random.randint(0,CITY_SIZE_X/3),random.randint(0,CITY_SIZE_Y))
	else:
		p1=Point(random.randint(0,CITY_SIZE_X),random.randint(0,CITY_SIZE_Y/3))
	p2=Point(random.randint(p1.x+mps,p1.x+MPS),	random.randint(p1.y+mps,p1.y+MPS))
	place=Rect(p1,p2)
	place.set_name('CAVE')
	nature.append(place)

print('Genero gli edifici')
#CREAZIONE EDIFICI
for i in range(0,len(PLACES)):
	#place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
	if(not ((defaultPlace[PLACES[i]][2]=='rural') or (defaultPlace[PLACES[i]][2]=='free'))):
		place=createPlaceDefault(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)),PLACES[i])
		place.set_name(PLACES[i])
		buildings.append(place)

print('genero case libere')
for i in range(0,homeNumber/20):
	place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
	buildings.append(place)

old_town=homeNumber/100*20
new_town=homeNumber/100*80

def generaPlace(buildings,homeNumber):
	print('genero case dipendenti')
	for i in range(5,homeNumber):
		old_place=buildings[random.randint(0,len(buildings)-1)]
		place=createPlace(old_place)
		buildings.append(place)

	print('Controllo conflitti edifici')
	touch=False
	while(not touch):	
		touch=True
		for place in buildings:		
			for place2 in buildings:
				if(not (id(place)==id(place2))):
					if(place.overlaps(place2)):
						if(place.name=='HOUSE'):
							place.move(random.randint(0,4),random.randint(0,MAX_PLACE_SIZE))
							#print('muovo una casa '+place.name)
							touch=False
						else:
							place2.move(random.randint(0,4),random.randint(0,MAX_PLACE_SIZE))
							#print('muovo una casa '+place2.name)
							touch=False
	return buildings
	
buildings.extend(generaPlace(buildings,old_town))

perim=()
if( 'WALL' in RESOURCES ):
	perim= perimetralWall(buildings)

print(perim)

#CREAZIONE EDIFICI RURALI
for i in range(0,len(PLACES)):
	#place=createPlacePoint(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)))
	if(defaultPlace[PLACES[i]][2]=='rural') or (defaultPlace[PLACES[i]][2]=='free'):
		place=createPlaceDefault(Point(int(CITY_SIZE_X/2),int(CITY_SIZE_Y/2)),PLACES[i])
		place.set_name(PLACES[i])
		buildings.append(place)
		
buildings.extend(generaPlace(buildings,new_town))	

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
							x=5
#FINE CREAZIONE EDIFICI


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
		color=defaultPlace[place.name][3]
		draw.rectangle(place.get_list(), outline=DEFAULT_COLOR, fill=color )
		draw.text((place.top_left().x+5,place.top_left().y),place.name[0:1],fill="red",font=font)
	else:
		draw.rectangle(place.get_list(), outline=color)

#GENERA DIMENSIONE TESTO LEGENDA SU MAPPA
maxsize=1
for i in range(0,len(PLACES)):
	if(font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]>maxsize):
		maxsize=font.getsize(PLACES[i][0:1]+": "+PLACES[i].lower().title())[0]
		
#STAMPA LEGENDA
maxsize=maxsize+30
draw.rectangle((CITY_SIZE_X-maxsize-5,45,CITY_SIZE_X-5,50+len(PLACES)*(FONT_SIZE+1)), fill='white' )
draw.rectangle((CITY_SIZE_X-maxsize-5,45,CITY_SIZE_X-5,50+len(PLACES)*(FONT_SIZE+1)), outline='black' )
for i in range(0,len(PLACES)):
	draw.rectangle((CITY_SIZE_X-maxsize,50+i*(FONT_SIZE)+1,CITY_SIZE_X-maxsize+5,50+i*(FONT_SIZE)+FONT_SIZE-2),fill=defaultPlace[PLACES[i]][3])
	draw.text((CITY_SIZE_X-maxsize+10,50+i*(FONT_SIZE)),PLACES[i][0:1]+": "+PLACES[i].lower().title(),fill="red",font=font)


LUNGHEZZA_CAMPIONE=250
draw.line((CITY_SIZE_X-5-LUNGHEZZA_CAMPIONE,CITY_SIZE_Y-10,CITY_SIZE_X-5,CITY_SIZE_Y-10),width=2,fill='red');
TEXT=str(METER_PIXEL_RATIO*LUNGHEZZA_CAMPIONE)+' m'
draw.text((CITY_SIZE_X-LUNGHEZZA_CAMPIONE+LUNGHEZZA_CAMPIONE/3,CITY_SIZE_Y-10-(FONT_SIZE)),TEXT,fill="red",font=font)

draw.text((10,10),"City of "+CITY_NAME,fill="red",font=font)

img.show()


print("Fantasy City Planner has finish to create city of "+CITY_NAME)
#im.save(sys.stdout, "PNG")
