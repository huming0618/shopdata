import json

config = None
with open('config.json','r') as configFile:
     config = json.loads(configFile.read())
