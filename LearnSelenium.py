# LearnSelenium

from bs4 import BeautifulSoup 
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


fp = open("SeleniumResult.txt",'w')

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://list.jd.com/1620-1621-1626.html") # Load page

# fp.write(str(browser.page_source))
soup = BeautifulSoup(str(browser.page_source))
Brands = BeautifulSoup(str(soup.find("div","tabcon"))).div
print len(Brands)
for product in Brands.contents:
	print product.text
# elem = browser.find_elements_by_class_name("hide")
# for nm in elem:
# 	fp.write(str(nm.text))
time.sleep(0.2) # Let the page load, will be added to the API

browser.close()
fp.close()

