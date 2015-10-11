#FINE CONFIGURAZIONE INIZIALE


def get_default_places(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH):
    defaultPlace={}

    # center, urban, free, rural,
    defaultPlace['CASTLE']=((MIN_PLACE_SIZE*WEALTH/2),(MAX_PLACE_SIZE*WEALTH)/2,'center','#85DADA')
    defaultPlace['MARKET']=(30,20*WEALTH,'center','#FFCC99')
    defaultPlace['PARK']=(30,35*WEALTH,'urban','#2EB82E')
    defaultPlace['SANCTUARY']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'free','#009999')
    defaultPlace['CHURCH']=(MAX_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#009999')
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
    defaultPlace['BARRACK']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#666666')#CASERMA
    defaultPlace['HERBALISTS']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'urban','#669900')
    defaultPlace['LAZARETTO']=(MAX_PLACE_SIZE/2,MAX_PLACE_SIZE*2,'urban','#FFFFFF')
    defaultPlace['BUTCHER_SHOP']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#FF9999')#macelleria
    defaultPlace['WHOREHOUSE']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#CC0000')#BORDELLO
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
    defaultPlace['OBSERVATORY']=(MIN_PLACE_SIZE,MAX_PLACE_SIZE*2,'rural','#0000CC')
    defaultPlace['unknown']= (MIN_PLACE_SIZE,MAX_PLACE_SIZE,'urban','#000066')

    return defaultPlace

def getDefaultPlace(name, defaultPlace):
    res=defaultPlace['unknown']
    if name in list(defaultPlace.keys()):
        res=defaultPlace[name]
    return res
    

def get_default_resurces(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH):
    defaultResurce={}
    defaultResurce['WOOD']=('green','removable')
    defaultResurce['RIVER']=('#00CCFF','fixed')
    defaultResurce['RIVERX']=('#00CCFF','fixed')
    defaultResurce['RIVERY']=('#00CCFF','fixed')
    defaultResurce['CAVE']=('#323232','fixed')

    return defaultResurce

