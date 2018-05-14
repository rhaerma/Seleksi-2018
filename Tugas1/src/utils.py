""" UTILITIES FOR SCRAPING AND PARSING
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import time
import json
import re
import random

## Control arguments on command
def controlArgv(cities):
    listArgv = sys.argv
    city = cities
    isRequestAll = False
    if (len(listArgv) > 1):
        if ('--all' in sys.argv):
            isRequestAll = True
            listArgv.remove('--all')
        if (len(listArgv) > 1):
            city = listArgv[1].split('-')[1]
            city = city.split(',')
            if (set(city).issubset(set(cities))):
                city = list(set(city))
            else:
                print('[!] Invalid Arguments. Scrapping in default setting ..')
        else:
            print('[!] Invalid Arguments. Scrapping in default setting ..')            
    return city, isRequestAll

## Get Raw Source of page in url
## Return soup: BeautifulSoup object(in html)
def getRawSource(url, counter):
    time.sleep(random.randint(0, 2))
    response = urlopen(url).read()
    soup = BeautifulSoup(response, 'html.parser')
    return soup

## Return string contains regex from soup object
def getTextPattern(soup, div_id, regex):
    pattern = re.compile(div_id)
    rawData = soup.find('script', text=pattern) #Get certain data inside <script> tag
    result = re.search(regex, str(rawData))
    return result

## Save Data to File
def saveJSONToFile(JSONObject):
    filename = time.strftime("%Y-%m-%d_%H.%M.%S")
    dirpath = '../data/scrapped_'+filename+'.json'
    with open(dirpath, "w") as outfile:
        json.dump(JSONObject, outfile, indent=4)
    print('> Your data has successfully saved to file!')