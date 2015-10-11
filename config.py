#!/usr/bin/env python3

# config.py
# Part of Fantasy City Planner.
# See fcp.py for license details.


def set_defaults(self):
    return


def parse(conf_file):
    import yaml

    try:
        stream = open(conf_file, 'r')

    except IOError as e: 
        print("Error opening ["+conf_file+"]: "+str(e)+"\n")

    config = yaml.load(stream)
    return config






if __name__ == "__main__":
    import sys
    import yaml

    if len(sys.argv)<2:
        conf_file = 'config.yaml'
    else:
        conf_file = sys.argv[1]

    config = parse(conf_file)

    print(yaml.dump(config))
    

