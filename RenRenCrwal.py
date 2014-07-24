# For RenRenPhoto
# -*- coding: utf-8 -*-
'''
Fetch the Photos in RenRen
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib2
import time 
from bs4 import BeautifulSoup 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

PageLink = 'http://photo.renren.com/photo/237501531/photo-7872005784?psource=7#/237501531/photo-7872005784'
browser.get(PageLink) # Load page
photoArea = browser.find_element_by_class_name('')



soup = BeautifulSoup(str(browser.page_source))