# fantasy-city-planner
A tool for creating random city in a middle age fantasy world


![alt text](https://raw.githubusercontent.com/DangerBlack/fantasy-city-planner/master/map/mappa_5.png "An example of what can be done with fcp")


#Usage

Edit this settings in order to custom your city
```python
#The name of the city
CITY_NAME="Carcosa"
#Dimension in pixel width 1px=0.5mt
CITY_SIZE_X=800
#Dimension in pixel height 1px=0.5mt
CITY_SIZE_Y=600
#Number of Inhabitants of the city
INHABITANTS=6400
#Resources (singular name)
RESOURCES=['WOOD','FISH','LEATHER','PIG','HORSE','CAVE','SILK','WOOL','WALL','RIVERX','RIVERY']
#Wealth of the city 1 poor, 10 rich
WEALTH=6 #1-10
#Important buildings or something that must be in the city
PLACES=['CASTLE','SANCTUARY','CHURCH']
#Dimension of the biggest house 1px=0.5mt
MAX_PLACE_SIZE=20
#Dimension of the smallest house 1px=0.5mt
MIN_PLACE_SIZE=6
#Default color for the buildings
DEFAULT_COLOR='#505050'
```

Map will be saved in the map folder!


##Requirment
You need python 2.7 in order to run this program
```bash
sudo apt install python
sudo apt install pip
pip install Pillow
```


##Fonts
The font is "MedievalSharp" by Wojciech Kalinowski, distributed under the SIL.
For the complete package, see http://openfontlibrary.org/

