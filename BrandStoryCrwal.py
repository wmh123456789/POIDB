# -*- coding: utf-8 -*-
# BrandStoryCrwal
import json
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
import time
import os
import urllib2
import time 
from bs4 import BeautifulSoup 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 正则：保留英文大小写，中文，空格（适合文件名命名）
# print re.sub(u'([^\w \u4e00-\u9fa5])+','',u'j dq2rp 8hJoiFSIO JA2山东IFS223z____x**(&')
# print u'\u9fa7',u'\u9fa4',u'\u9fa3',u'\u9fa2',u'\u9fa1',u'\u9fa0',


def GetPage(PageURL):
	headers = {
		'Referer':'http://www.tmall.com',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}

	request = urllib2.Request(PageURL, headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=50).read()
	# TransCode for the page
	return ResultContent
