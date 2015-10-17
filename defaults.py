#FINE CONFIGURAZIONE INIZIALE


def get_default_places(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH):
    from config import load_yaml_file
    return load_yaml_file('places.yaml')    


def getDefaultPlace(name, defaultPlace):
    if name in list(defaultPlace.keys()):
        return defaultPlace[name]
    print("Warn: %s not found in place database (places.yaml)" % name)
    return defaultPlace['unknown']

def get_default_resurces(MIN_PLACE_SIZE, MAX_PLACE_SIZE, WEALTH):
    from config import load_yaml_file
    return load_yaml_file('resources.yaml')    

