import re
import json
import scrapper
import random

cities = ['bandung', 'jakarta', 'bali', 'medan', 'surabaya']
home_url = 'https://myfave.com'
data_per_page = 24
allCouponList = []
main_div = r'OffersViewNonCat'
categ_div = r'BuyNowSticky'

## Scrape pages 
## return couponList json object
def scrapeMultiPages(url):
    counter = 1
    i = 1
    print(' -- Scrape Page ' + str(i))
    soup = scrapper.getRawSource(url, counter)
    localCouponList = parseMainPage(soup)
    # Find total pages
    '''
    result = getTextPattern(soup, main_div, r'.*meta: ".*",')
    sumData = int(result.group(0).split('"'))
    numPage = round(sumData/data_per_page)
    '''
    numPage = 1
    # Scrape all pages
    while (i < numPage):
        counter += 1
        i += 1
        urlNext = url+'?page='+str(i)
        print(' -- Scrape Page ' + str(i))
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
def getTextPattern(soup, div_id, regex):
    pattern = re.compile(div_id)
    rawData = soup.find('script', text=pattern) #Get certain data inside <script> tag
    result = re.search(regex, str(rawData))
    return result
    
## Parse page of item thumbnails on html form to json object
## soup: BeautifulSoup object contains web view-source
## return couponList: JSONObject of best deals on current page
def parseMainPage(soup):
    result = getTextPattern(soup, main_div, r'.*listings: \[{(.*)}\],\n')
    #print(str(result))
    jsonStr = '[{' + result.group(1) + '}]'
    couponList = json.loads(jsonStr)

    couponList = formCouponList(couponList)
    return couponList

## Add and modificate fields in couponList
## couponList: coupon JSONObject
## return couponList with formatted fields
def formCouponList(couponList):
    #for coupon in couponList:
    for i in range(0, 1):
        coupon = couponList[i]
        coupon = formatCoupon(coupon)
        coupon = scrapePageDetail(coupon)

    return couponList

## Scrape page detail of coupon item
def scrapePageDetail(coupon):
    url = home_url+coupon['url']
    print(' - Scrape item '+ url)
    soup = scrapper.getRawSource(url, 1)
    #Get Category
    result = getTextPattern(soup, categ_div, r'"category":{"name":(.*),"id"')
    coupon['category'] = result.group(1).split('"')[1]
    #Get partner reputation
    return coupon

## Remove unnecessary and modificate coupon fields
## return formatted coupon
def formatCoupon(coupon):
    #format price
    coupon['discounted_price'] = coupon['discounted_price_cents']/100
    coupon['original_price'] = coupon['original_price_cents']/100
    #format partner
    coupon['partner'] = {}
    coupon['partner']['location'] = {}
    coupon['partner']['company_name'] = coupon['company_name']
    coupon['partner']['location']['latitude'] = coupon['latitude']
    coupon['partner']['location']['longitude'] = coupon['longitude']
    coupon['partner']['outlet_count'] = coupon['outlets_count']
    coupon['partner']['outlet_names'] = coupon['outlet_names']
    #delete unnecessary fields
    del coupon['discounted_price_cents']
    del coupon['original_price_cents']
    del coupon['company_name']
    del coupon['outlets_count']
    del coupon['outlet_names']
    del coupon['latitude']
    del coupon['longitude']
    del coupon['company_id']
    del coupon['image']
    del coupon['distance']
    del coupon['time_diff']
    del coupon['thumbnail']
    del coupon['slug']
    del coupon['rectangular_thumbnail']
    del coupon['featured_thumbnail_image']

    city = coupon['url'].split('/')[2]
    coupon['customer_city'] = []
    coupon['customer_city'].append(city)

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
    if (allCouponList != {}):
        for coupon in couponList:
            idx = checkCouponOccurence(coupon, allCouponList)
            if (idx != -1):
                allCouponList.append(coupon)
                print(coupon)
                allCouponList[idx]['customer_city'] += coupon['customer_city']
    else:
        allCouponList = couponList

    return allCouponList

## Collect list based on category
## Return finalCouponList ready to be saved on JSON file
def categorizeCouponList(allCouponList):
    finalCouponList = []
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
        url = home_url+'/cities/'+city+'/best-selling-deals'
        print(' --- Scrape Best Deals in ' + city)
        localCouponList = scrapeMultiPages(url) # Get coupon data from current city 
        currCouponList = allCouponList
        allCouponList = mergeCouponLists(currCouponList, localCouponList)
    # Categorize Coupon
    scrapper.saveJSONToFile(allCouponList)
    allCouponList = categorizeCouponList(allCouponList)
    print(allCouponList)
    # Save to File
    scrapper.saveJSONToFile(allCouponList)