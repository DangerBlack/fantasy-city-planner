from networkx import nx
import random
from rect import Point
from rect import Rect

def generateRoads(buildings,city_size_x,city_size_y):
	snode=[]
	important=["CATHEDRAL","CHURCH","INN","BARRACK","TAVERN","CASTLE","MARKET"]
	print(city_size_x)
	print(city_size_y)
	for house in buildings:
		if(house.name in important) and house.bottom>0 and (house.top+10)<city_size_y and house.left>0 and (house.right+10)<city_size_x:
			snode.append(house)
	
	G=nx.Graph()
	
	#ADD ENTRY POINT FORM N E S W
	
	snode.append(Rect(Point(random.randint(0,city_size_x),0),Point(random.randint(0,city_size_x),0)))
	#snode.append(Rect(Point(city_size_x,random.randint(0,city_size_y)),Point(city_size_x,random.randint(0,city_size_y))))
	snode.append(Rect(Point(random.randint(0,city_size_x),city_size_y),Point(random.randint(0,city_size_x),city_size_y)))
	#snode.append(Rect(Point(0,random.randint(0,city_size_y)),Point(0,random.randint(0,city_size_y))))
	
	for i in range(0,len(snode)):
		for j in range(0,len(snode)):
			p1=Point(snode[i].left,snode[i].top)
			p2=Point(snode[j].left,snode[j].top)
			G.add_edge(i,j,weight=p1.distance_to(p2))
		#G.add_edge(s.top,s.rigth,weight=1)
	
	mst=nx.minimum_spanning_edges(G,data=False)
	
	edgelist=sorted(list(mst))
	
	res=[]
	for e in edgelist:
		res.append((snode[e[0]].left+snode[e[0]].size_x()/2,snode[e[0]].top+snode[e[0]].size_y()/2))
		res.append((snode[e[1]].left+snode[e[1]].size_x()/2,snode[e[1]].top+snode[e[1]].size_y()/2))
	print('Le edge sono queste')
	print(edgelist)
	print('Fine edge')
	print('I punti sono questi')
	print(res)
	print('Fine punti')
	return res
