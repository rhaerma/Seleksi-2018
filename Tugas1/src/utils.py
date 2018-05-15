""" UTILITIES FOR SCRAPING AND PARSING
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
import time
import json
import re
import random

## Control arguments on command line
def controlArgv(cities):
    listArgv = sys.argv
    isRequestAll = False
    if (len(listArgv) > 1):
        if ('all' in sys.argv):
            isRequestAll = True
            listArgv.remove('all')
        if (len(listArgv) > 1):
            city = listArgv[1].split(',')
            if (set(city).issubset(set(cities))):
                cities = list(set(city))
            else:
                print('[!] Invalid Arguments. Scrapping in default setting ..')        
    return cities, isRequestAll

## Get Raw Source of page in url
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

## Save Data to JSON File
def saveJSONToFile(JSONObject):
    global foldername
    foldername = 'scrapped_'+time.strftime("%Y-%m-%d_%H.%M.%S")
    filename = 'coupons_data.json'
    dirpath = 'data/'+foldername+'/'

    os.makedirs(os.path.dirname(dirpath))
    with open(dirpath+filename, "w") as outfile:
        json.dump(JSONObject, outfile, indent=4)
    print('---> Your data has successfully saved to file!')

# Normalize JSON format to Dataframe and save to file
def normalizeData(data):
    global foldername
    df = pd.io.json.json_normalize(data)
    out = df.to_json(orient='records')

    # Save to file
    filename = 'coupons_normalized.json'
    dirpath = 'data/'+foldername+'/Normalized/'
    os.makedirs(os.path.dirname(dirpath+filename))
    with open(dirpath+filename, 'w') as f:
        f.write(out)
    
    filename = 'coupons_dataframe.txt'
    with open(dirpath+filename, 'w') as f:
        f.write(df.to_string())