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
## isRequestAll to request all pages in each city
def scrapeAllCoupons(cities, isRequestAll):
    allCouponList = []
    for city in cities:
        url = home_url+'/cities/'+city+'/best-selling-deals'
        print('\n---> Scrape best deals in ' + city)
        localCouponList = scrapeMultiPages(url, isRequestAll) # Get coupon data from current city
        currCouponList = allCouponList
        allCouponList = mergeCouponLists(currCouponList, localCouponList)
    #Scrape details
    print('\n---> Scrape Page Details')
    allCouponList = scrapePageDetail(allCouponList)
    return allCouponList

## Scrape pages 
## return couponList json object
def scrapeMultiPages(url, isRequestAll):
    counter = 1     # Control timelimit for scrapper
    i = 1
    print('>>> Scrape Page ' + str(i))
    soup = utils.getRawSource(url, counter)
    localCouponList = parseMainPage(soup)
    if (isRequestAll):
        # Find total pages
        result = utils.getTextPattern(soup, main_div, numpage_script)
        sum_data = int(result.group(0).split('"')[1])
        page_count = round(sum_data/data_per_page)
        num_page = page_count
    else:
        num_page = 1
    # Scrape pages
    while (i < num_page):
        counter += 1
        i += 1
        urlNext = url+'?page='+str(i)
        print('>>> Scrape Page ' + str(i))
        soup = utils.getRawSource(urlNext, counter)
        nextCouponList = parseMainPage(soup)
        localCouponList += nextCouponList
    return localCouponList
    
## Parse page of item thumbnails on BeautifulSoup form to json object
def parseMainPage(soup):
    result = utils.getTextPattern(soup, main_div, data_script)
    jsonStr = '[{' + result.group(1) + '}]'
    couponList = json.loads(jsonStr)
    couponList = formCouponList(couponList)
    return couponList

## Add and format couponList fields
def formCouponList(couponList):
    for i in range(0, len(couponList)):
        couponList[i] = formatCoupon(couponList[i])
    return couponList

## Return formatted coupon with neccessary fields added
def formatCoupon(coupon):
    newCoupon = {}
    newCoupon['id'] = coupon['id']
    newCoupon['title'] = coupon['name']
    newCoupon['original_price'] = coupon['original_price_cents']/100
    newCoupon['discounted_price'] = coupon['discounted_price_cents']/100
    newCoupon['discount'] = coupon['discount']
    newCoupon['start_date'] = coupon['start_date']
    newCoupon['due_date'] = coupon['end_date']
    newCoupon['purchases_count'] = coupon['purchases_count']
    newCoupon['today_purchases_count'] = coupon['today_purchases_count']

    newCoupon['partner'] = {}
    newCoupon['partner']['company_name'] = coupon['company_name']
    newCoupon['partner']['location'] = {}
    newCoupon['partner']['location']['latitude'] = coupon['latitude']
    newCoupon['partner']['location']['longitude'] = coupon['longitude']

    newCoupon['average_rating'] = coupon['average_rating']
    newCoupon['number_of_clicks'] = coupon['hotness']
    
    #newCoupon['description'] = coupon['description']    
    #newCoupon['url'] = coupon['url']
    city = coupon['url'].split('/')[2]
    newCoupon['customer_city'] = [city]

    return newCoupon

## Scrape detail page of a coupon item
def scrapePageDetail(couponList):
    numItem = len(couponList)
    count = 1
    for coupon in couponList:
        city = coupon['customer_city'][0]
        url = home_url+'/cities/'+city+'/offers/'+str(coupon['id'])
        print(' ['+str(count)+'/'+str(numItem)+'] Scrape item id='+ str(coupon['id']))
        soup = utils.getRawSource(url, 1)
        #Get Category
        result = utils.getTextPattern(soup, detail_div, category_script)
        coupon['category'] = result.group(1).split('"')[1]
        count += 1
    return couponList

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
            if (idx == -1):
                allCouponList.append(coupon)
            else:
                allCouponList[idx]['customer_city'] += coupon['customer_city']
    else:
        allCouponList = couponList
    return allCouponList

## Main Program
if __name__ == '__main__':
    print(' ~=~ Coupon Data Scrapper ~=~  ')
    print('      Source: MyFave.com        ')
    # Control arguments
    cities, isRequestAll = utils.controlArgv(cities)
    random.shuffle(cities)
    # Scrape data from various cities
    allCouponList = scrapeAllCoupons(cities, isRequestAll)
    # Save to File
    utils.saveJSONToFile(allCouponList)
    # Transform to normalized JSON
    utils.normalizeData(allCouponList)