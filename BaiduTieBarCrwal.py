# -*- coding: utf-8 -*-
'''
Fetch the Lian`ai in TieBa
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

def GetPage(PageURL):
	headers = {
		'Referer':'http://www.jd.com',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}

	request = urllib2.Request(PageURL, headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=50).read()
	# TransCode for the page
	return ResultContent

rootpath =r'http://tieba.baidu.com/f?ie=utf-8&kw=%B8%DF%D6%D0&fr=search'

WebText = GetPage(rootpath).decode('GBK').encode('utf8')
soup = BeautifulSoup(WebText)
soup.prettify()
# keywords = soup.findAll('div', attrs={'title':re.compile(u'恋爱')})
keywords = re.findall('.{3}恋爱.{3}',WebText)
print len(keywords)
for word in keywords:
	print str(word)

fp = open('teibar.txt','w')
fp.write(str(soup))
fp.close()