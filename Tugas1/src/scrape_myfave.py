import re
import json
import scrapper
import random

cities = ['bandung', 'jakarta', 'bali', 'medan', 'surabaya']
home_url = 'https://myfave.com/'
data_per_page = 24
allCouponList = {}

## Scrape pages 
## return couponList json object
def scrapeMultiPages(url):
    counter = 1
    i = 1
    soup = scrapper.getRawSource(url, counter)
    localCouponList = parseMainPage(soup)
    # Find total pages
    result = getTextPattern(soup, r'.*meta: ".*",')
    sumData = int(result.group(0).split('"'))
    numPage = round(sumData/data_per_page)
    # Scrape all pages
    while (i < numPage):
        counter += 1
        i += 1
        urlNext = url+'?page='+str(i)
        soup = scrapper.getRawSource(urlNext, counter)
        nextCouponList = parseMainPage(soup)
        currCouponList = localCouponList
        localCouponList = uniteCouponLists(currCouponList, nextCouponList)

    return localCouponList

# Unite two coupon lists
def uniteCouponLists(couponList1, couponList2):
    for coupon in couponList2:
        couponList1.append(coupon)
    return couponList1

## Return string contains regex from soup object
def getTextPattern(soup, regex):
    pattern = re.compile(r'OffersViewNonCat')
    rawData = soup.find('script', text=pattern) #Get certain data inside <script> tag
    result = re.search(regex, str(rawData))
    return result
    
## Parse page of item thumbnails on html form to json object
## soup: BeautifulSoup object contains web view-source
## return couponList: JSONObject of best deals on current page
def parseMainPage(soup):
    result = getTextPattern(soup, r'.*listings: \[{(.*)}\],\n')
    #print(str(result))
    jsonStr = '[{' + result.group(1) + '}]'
    couponList = json.loads(jsonStr)

    couponList = formCouponList(couponList)
    return couponList

## Add and modificate fields in couponList
## couponList: coupon JSONObject
## return couponList with formatted fields
def formCouponList(couponList):
    for coupon in couponList:
        coupon = formatCoupon(coupon)
        #inside 
        coupon['company_city'] 
        coupon['category']

    return couponList

## Remove unnecessary and modificate coupon fields
## return formatted coupon
def formatCoupon(coupon):
    #delete unnecessary fields
    del coupon['time_diff']
    del coupon['thumbnail']
    del coupon['slug']
    del coupon['rectangular_thumbnail']
    del coupon['featured_thumbnail_image']
    #format price
    coupon['discounted_price'] = coupon['discounted_price_cents']/100
    coupon['original_price'] = coupon['original_price_cents']/100
    #delete unnecessary price tags
    del coupon['discounted_price_cents']
    del coupon['original_price_cents']

    city = coupon['url'].split('/')[1]
    coupon['customer_city'] = []
    coupon['customer_city'].append(city)

    return coupon

## Check if a coupon object already on couponList
## Return index of occurence if available, otherwise return -1
def checkCouponOccurence(coupon, couponList):
    i = 0
    while (i<couponList.length):
        if (coupon['id'] == couponList[i]['id']):
            return i
        else:
            i += 1

    return -1

## Merge multiple occurence of coupon from multiple cities
## Return allCouponList
def mergeCouponLists(allCouponList, couponList):
    if (allCouponList != {}):
        for coupon in couponList:
            idx = checkCouponOccurence(coupon, allCouponList)
            if (idx != -1):
                allCouponList.append(coupon)
                allCouponList[idx]['customer_city'] += coupon['customer_city']
    else:
        allCouponList = couponList

    return allCouponList

## Collect list based on category
## Return finalCouponList ready to be saved on JSON file
def categorizeCouponList(allCouponList):
    finalCouponList = {}
    for coupon in allCouponList:
        category = coupon['category']
        if (category not in finalCouponList):
            finalCouponList[category] = []
        finalCouponList[category].append(coupon)

    return finalCouponList

## Main Program
if __name__ == '__main__':
    random.shuffle(cities)
    ## Scrape data from various cities
    for city in cities:
        url = home_url+'cities/'+city+'/best-selling-deals'
        localCouponList = scrapeMultiPages(url) # Get coupon data from current city 
        currCouponList = allCouponList
        allCouponList = mergeCouponLists(currCouponList, localCouponList)
    # Categorize Coupon
    allCouponList = categorizeCouponList(allCouponList)
    # Save to File
    scrapper.saveJSONToFile(allCouponList)