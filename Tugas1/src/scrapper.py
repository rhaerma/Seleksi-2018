from urllib.request import urlopen
import requests
import time
import os
import json
from bs4 import BeautifulSoup

## Get Raw Source of page in url
## Return soup: BeautifulSoup object(in html)
def getRawSource(url):
    response = urlopen(url).read()
    soup = BeautifulSoup(response, 'html.parser')
    return soup

def saveToFile(result):
    with open("output.html", "w+") as file:
        for word in result.groups():
            file.write(word)

def saveJSONToFile(filename, JSONObject):
    dirname = time.strftime("%Y-%m-%d_%H:%M:%S")
    dirpath = os.path.join('/data/scrapped_'+dirname+'/'+filename+'.json')
    with open(dirpath, "w") as outfile:
        json.dump(JSONObject, outfile, indent=4)
