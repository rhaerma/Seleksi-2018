""" MYFAVE BEST DEALS COUPON SCRAPPER
"""

import json
import utils
import random

cities = ['bandung', 'jakarta', 'bali', 'medan', 'surabaya']
home_url = 'https://myfave.com'
data_per_page = 24
allCouponList = []
# Regex for Parsing
main_div = r'OffersViewNonCat'
detail_div = r'BuyNowSticky'
data_script = r'.*listings: \[{(.*)}\],\n'
numpage_script = r'.*meta: ".*",'
category_script = r'"category":{"name":(.*),"id"'

## Scrape coupons from various cities
## If isRequestAll to request all pages each city
def scrapeAllCoupons(cities, isRequestAll):
    allCouponList = []
    for city in cities:
        url = home_url+'/cities/'+city+'/best-selling-deals'
        print('\n >>>> Scrape best deals in ' + city)
        localCouponList = scrapeMultiPages(url, isRequestAll) # Get coupon data from current city
        currCouponList = allCouponList
        allCouponList = mergeCouponLists(currCouponList, localCouponList)
    return allCouponList

## Scrape pages 
## return couponList json object
def scrapeMultiPages(url, isRequestAll):
    counter = 1     # Control timelimit for scrapper
    i = 1
    print(' >>> Scrape Page ' + str(i))
    soup = utils.getRawSource(url, counter)
    localCouponList = parseMainPage(soup)
    if (isRequestAll):
        # Find total pages
        result = utils.getTextPattern(soup, main_div, numpage_script)
        sum_data = int(result.group(0).split('"'))
        page_count = round(sum_data/data_per_page)
        num_page = page_count
    else:
        num_page = 1
    # Scrape pages
    while (i < num_page):
        counter += 1
        i += 1
        urlNext = url+'?page='+str(i)
        print(' >>> Scrape Page ' + str(i))
        soup = utils.getRawSource(urlNext, counter)
        nextCouponList = parseMainPage(soup)
        localCouponList += nextCouponList
    return localCouponList
    
## Parse page of item thumbnails on BeautifulSoup form to json object
## return couponList: JSONObject of best deals on current page
def parseMainPage(soup):
    result = utils.getTextPattern(soup, main_div, data_script)
    jsonStr = '[{' + result.group(1) + '}]'
    couponList = json.loads(jsonStr)
    couponList = formCouponList(couponList)
    return couponList

## Add and format fields in couponList
## return couponList with formatted fields
def formCouponList(couponList):
    for coupon in couponList:
        coupon = formatCoupon(coupon)
        coupon = scrapePageDetail(coupon) #get details of each item
    return couponList

## Return formatted coupon with neccessary fields added
def formatCoupon(coupon):
    newCoupon = {}
    newCoupon['id'] = coupon['id']
    newCoupon['title'] = coupon['name']
    newCoupon['description'] = coupon['description']
    newCoupon['original_price'] = coupon['original_price_cents']/100
    newCoupon['discounted_price'] = coupon['discounted_price_cents']/100
    newCoupon['discount'] = coupon['discount']
    newCoupon['start_date'] = coupon['start_date']
    newCoupon['due_date'] = coupon['end_date']
    newCoupon['purchases_count'] = coupon['purchases_count']
    newCoupon['today_purchases_count'] = coupon['today_purchases_count']
    newCoupon['last_purchased_at'] = coupon['last_purchased_at']

    newCoupon['partner'] = {}
    newCoupon['partner']['company_name'] = coupon['company_name']
    newCoupon['partner']['location'] = {}
    newCoupon['partner']['location']['latitude'] = coupon['latitude']
    newCoupon['partner']['location']['longitude'] = coupon['longitude']
    newCoupon['partner']['outlet_count'] = coupon['outlets_count']
    newCoupon['partner']['outlet_names'] = coupon['outlet_names']

    newCoupon['average_rating'] = coupon['average_rating']
    newCoupon['number_of_click'] = coupon['hotness']

    city = coupon['url'].split('/')[2]
    newCoupon['customer_city'] = [city]

    # Just in case needed
    #newCoupon['image']
    #newCoupon['thumbnail']
    return newCoupon

## Scrape detail page of a coupon item
def scrapePageDetail(coupon):
    url = home_url+'/cities/'+coupon['customer_city'][0]+'/offers/'+str(coupon['id'])
    print(' - Scrape item '+ url)
    soup = utils.getRawSource(url, 1)
    #Get Category
    result = utils.getTextPattern(soup, detail_div, category_script)
    coupon['category'] = result.group(1).split('"')[1]
    #Get partner reputation
    return coupon

## Check if a coupon object already on couponList
## Return index of occurence if available, otherwise return -1
def checkCouponOccurence(coupon, couponList):
    i = 0
    while (i<len(couponList)):
        if (coupon['id'] == couponList[i]['id']):
            return i
        else:
            i += 1
    return -1

## Merge multiple occurence of coupon from multiple cities
## Return allCouponList
def mergeCouponLists(allCouponList, couponList):
    if (allCouponList != []):
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
    cities, isRequestAll = utils.controlArgv(cities)
    # Control args
    random.shuffle(cities)
    # Scrape data from various cities
    allCouponList = scrapeAllCoupons(cities, isRequestAll)
    # Categorize list of coupon
    allCouponList = categorizeCouponList(allCouponList)
    # Save to File
    utils.saveJSONToFile(allCouponList)