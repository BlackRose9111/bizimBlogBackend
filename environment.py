import json
configvariables : dict = None



def load_config():
    global configvariables
    with open("config.json") as f:
        configvariables = json.load(f)
def getconfig(key):
    if configvariables == None:
        load_config()
    return configvariables[key]