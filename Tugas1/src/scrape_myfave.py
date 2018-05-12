import re
import json

## Parse page of item thumbnails on html form to json object
## soup: BeautifulSoup object contains web view-source
## return couponList: JSONObject of best deals on current page
def parseMainPage(soup):
    pattern = re.compile(r'OffersViewNonCat')
    rawData = soup.find('script', text=pattern) #Get certain data inside <script> tag
    result = re.search(r'.*listings: \[{(.*)}\],\n', str(rawData))
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
        #delete unnecessary fields
        del coupon['time_diff']
        del coupon['thumbnail']
        del coupon['slug']
        del coupon['rectangular_thumbnail']
        del coupon['featured_thumbnail_image']
        #format price
        coupon['discounted_price'] = coupon['discounted_price_cents'][:-2]
        coupon['original_price'] = coupon['original_price_cents'][:-2]
        #delete unnecessary price tags
        del coupon['discounted_price_cents']
        del coupon['original_price_cents']

        city = coupon['url'].split('/')[1]
        coupon['customer_city'] = []
        coupon['customer_city'].append(city)
        #inside 
        coupon['company_city'] 
        coupon['category']

    return couponList

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
def mergeCoupon(allCouponList, couponList):
    for coupon in couponList:
        idx = checkCouponOccurence(coupon, allCouponList)
        if (idx != -1):
            allCouponList.append(coupon)
            allCouponList[idx]['customer_city'] += coupon['customer_city']
    return allCouponList