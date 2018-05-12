from urllib.request import urlopen
import requests
import time
import os
import json
import random
from bs4 import BeautifulSoup

## Get Raw Source of page in url
## Return soup: BeautifulSoup object(in html)
def getRawSource(url, counter):
    if counter%20 == 0:
        print('- Sleep -')
        time.sleep(random.randint(30, 50))
    response = urlopen(url).read()
    time.sleep(random.randint(1, 3))
    soup = BeautifulSoup(response, 'html.parser')
    return soup

def saveJSONToFile(JSONObject):
    filename = time.strftime("%Y-%m-%d_%H:%M:%S")
    dirpath = os.path.join('/data/scrapped_'+filename+'.json')
    with open(dirpath, "w") as outfile:
        json.dump(JSONObject, outfile, indent=4)
