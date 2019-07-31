import sys
import json

from util.params import getArgDict

argDict = getArgDict(sys.argv)

with open(argDict['config'] if 'config' in argDict else './config.json') as file:
    CONFIG = json.load(file)
