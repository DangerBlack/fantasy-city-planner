from networkx import nx
import random
from rect import Point
from rect import Rect
import numpy as np
from scipy.misc import comb

def generateRoads(RESOURCES,buildings,city_size_x,city_size_y):
	
	if(not 'ROADS' in RESOURCES):
		return []
	
	snode=[]
	important=["CATHEDRAL","CHURCH","INN","BARRACK","TAVERN","CASTLE","MARKET"]
	print(city_size_x)
	print(city_size_y)
	for house in buildings:
		if(house.name in important) and house.bottom>0 and (house.top+10)<city_size_y and house.left>0 and (house.right+10)<city_size_x:
			snode.append(house)
	
	G=nx.Graph()
	
	#ADD ENTRY POINT FORM N E S W
	
	if('ROAD_N' in RESOURCES):
		snode.append(Rect(Point(random.randint(0,city_size_x),0),Point(random.randint(0,city_size_x),0)))
	if('ROAD_E' in RESOURCES):
		snode.append(Rect(Point(city_size_x,random.randint(0,city_size_y)),Point(city_size_x,random.randint(0,city_size_y))))
	if('ROAD_S' in RESOURCES):
		snode.append(Rect(Point(random.randint(0,city_size_x),city_size_y),Point(random.randint(0,city_size_x),city_size_y)))
	if('ROAD_W' in RESOURCES):
		snode.append(Rect(Point(0,random.randint(0,city_size_y)),Point(0,random.randint(0,city_size_y))))
	
	for i in range(0,len(snode)):
		for j in range(0,len(snode)):
			p1=Point(snode[i].left,snode[i].top)
			p2=Point(snode[j].left,snode[j].top)
			G.add_edge(i,j,weight=p1.distance_to(p2))
		#G.add_edge(s.top,s.rigth,weight=1)
	
	mst=nx.minimum_spanning_edges(G,data=False)
	
	edgelist=sorted(list(mst))
	
	res=[]
	unified=[]
	for e in edgelist:
		res.append((snode[e[0]].left+snode[e[0]].size_x()/2,snode[e[0]].top+snode[e[0]].size_y()/2))
		res.append((snode[e[1]].left+snode[e[1]].size_x()/2,snode[e[1]].top+snode[e[1]].size_y()/2))
		unified.extend(e)
		
	#valuto il degree con G.degree(Nodo).values() se i nodi hanno degree 1  li metto nell'insieme, altrimenti mi fermo
	
	#HERE BE DRAGON, SORRY GUYS!
	path=[]
	for i in range(0,len(snode)+2):
		path.append([i])
		
	p=[]
	for p in path:
		while(p[-1]!='EOL' and unified.count(p[-1])<3):
			print(p)
			p.append(find_edge(p,edgelist,p[-1]))
			print(p)
			
	
	
	orderedpaths = reversed(sorted(path, key=len))
	path=list(orderedpaths)

			
	nogod=[]
	for i in range(0,len(path)):
		print('sono a '+str(i))
		for r in path[i]:
			print('controllo '+str(r))
			for j in range(i+1,len(path)):
				if r in path[j]:
					nogod.append(j)
					break
	for q in nogod:
		path[q]='EOL'
	
	for p in path:		
		print(p)
			
	fpath=[]
	for p in path:		
		if(len(p)>=3)and p!='EOL':
			fpath.append(p)
		
	lsp=[] #last stright path
	for e in edgelist:
		bot=0
		for f in fpath:
			if(e[0] in f and e[1] in f):
				p=f.index(e[0])
				q=f.index(e[1])
				if(abs(q-p)!=1):
					lsp.append(e)
			else:
				bot=bot+1
		if(bot==len(fpath)):
			lsp.append(e)
	
	print('Inzio a preoccuparmi dei path rimasti')
	print(lsp)
	
	clsp=[]
	for e in lsp:
		clsp.append([(snode[e[0]].left+snode[e[0]].size_x()/2,snode[e[0]].top+snode[e[0]].size_y()/2),(snode[e[1]].left+snode[e[1]].size_x()/2,snode[e[1]].top+snode[e[1]].size_y()/2)])
	
	print('Inzio a preoccuparmi dei path rimasti 2')
	print(clsp)
	
	controlPointPath=[]
	count=0	
	for q in fpath:
		controlPointPath.append([])
		for e in q:
			controlPointPath[count].append([snode[e].left+snode[e].size_x()/2,snode[e].top+snode[e].size_y()/2])	
		count=count+1
	
	
	beziers=[]
	for e in controlPointPath:
		beziers.append(bezier_curve(e))
	print(len(controlPointPath[0]))
	for l in clsp:
		beziers.append(l)
		
	print(len(beziers))		
	return beziers

def find_edge(p,edgelist,node):
	for e in edgelist:
		if(not e[1] in p) and (e[0]==node):
			print('cammino 1')
			return e[1]
		if(not e[0] in p) and (e[1]==node):
			print('cammino 2')
			return e[0]
	return 'EOL'
def get_point_from_edge(edgelist,snode):
	res=[]
	for e in edgelist:
		res.append((snode[e[0]].left+snode[e[0]].size_x()/2,snode[e[0]].top+snode[e[0]].size_y()/2))
		res.append((snode[e[1]].left+snode[e[1]].size_x()/2,snode[e[1]].top+snode[e[1]].size_y()/2))
	return res
	
def bernstein_poly(i, n, t):
	"""
	 The Bernstein polynomial of n, i as a function of t
	"""
	return comb(n, i) * ( t**(n-i) ) * (1 - t)**i
	
def bezier_curve(points, nTimes=1000):
	"""
	   Given a set of control points, return the
	   bezier curve defined by the control points.

	   points should be a list of lists, or list of tuples
	   such as [ [1,1], 
				 [2,3], 
				 [4,5], ..[Xn, Yn] ]
		nTimes is the number of time steps, defaults to 1000

		See http://processingjs.nihongoresources.com/bezierinfo/
	"""

	nPoints = len(points)
	xPoints = np.array([p[0] for p in points])
	yPoints = np.array([p[1] for p in points])

	t = np.linspace(0.0, 1.0, nTimes)

	polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

	xvals = np.dot(xPoints, polynomial_array)
	yvals = np.dot(yPoints, polynomial_array)
	
	path=[]
	for i in range(0,len(xvals)):
		path.append((xvals[i],yvals[i]))
		
	return path #xvals, yvals
