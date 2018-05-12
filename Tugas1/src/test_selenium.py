'''
    UNUSED
'''
from selenium import webdriver
import time

url = 'https://myfave.com/cities/bandung/best-selling-deals'
driver = webdriver.PhantomJS()
driver.get(url)
htmlSource = driver.page_source
#find = driver.find_elements_by_xpath('//listings: //')

#innerHTML = driver.GetAttribute('innerHTML')
innerHtml = driver.find_element_by_id('OffersViewNonCat').get_attribute('innerHTML')
print(innerHtml)
# tulis di file

f = open('hahahe.txt','w+')
#f.write(innerHtml)
f.close()