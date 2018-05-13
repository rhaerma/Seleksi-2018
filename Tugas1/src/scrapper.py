from urllib.request import urlopen
import requests
import time
import json
import random
from bs4 import BeautifulSoup

## Get Raw Source of page in url
## Return soup: BeautifulSoup object(in html)
def getRawSource(url, counter):
    if counter%10 == 0:
        print('~+~+ Sleep +~+~')
        time.sleep(random.randint(3, 5))
        print('~-~- Continue -~-~')
    time.sleep(random.randint(0, 2))
    response = urlopen(url).read()
    soup = BeautifulSoup(response, 'html.parser')
    return soup

def saveJSONToFile(JSONObject):
    filename = time.strftime("%Y-%m-%d_%H.%M.%S")
    dirpath = '../data/'+filename+'.json'
    with open(dirpath, "w") as outfile:
        json.dump(JSONObject, outfile, indent=4)
    print('Your scrape has successfully saved!')