#!/usr/bin/env python3

# config.py
# Part of Fantasy City Planner.
# See fcp.py for license details.

def load_yaml_file(conf_file):
    import yaml

    try:
        stream = open(conf_file, 'r')

    except IOError as e: 
        print("Error opening ["+conf_file+"]: "+str(e)+"\n")

    config = yaml.load(stream)
    return config


def load_config_file(conf_file='config.yaml'):
    defaults = load_yaml_file('defaults.yaml')
    config = load_yaml_file(conf_file)
    merged=defaults.copy()
    merged.update(config)
    #print("----------------------------\nDefault config:\n")
    #print(yaml.dump(defaults))
    #print("----------------------------\nRead config:\n")
    #print(yaml.dump(config))
    #print("----------------------------\nMerged config:\n")
    #print(yaml.dump(merged))
    
    return merged


if __name__ == "__main__":
    import sys
    import yaml


    if len(sys.argv)<2:
        conf_file = 'config.yaml'
    else:
        conf_file = sys.argv[1]

    config = load_config_file(conf_file)



    places = load_yaml_file('places.yaml')
    print(places)

    resources = load_yaml_file('resources.yaml')
    print(resources)
