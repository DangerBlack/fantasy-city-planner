#FINE CONFIGURAZIONE INIZIALE


def get_default_places(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH):
    from config import load_yaml_file
    return load_yaml_file('places.yaml')    


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

