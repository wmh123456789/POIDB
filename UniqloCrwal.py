# -*- coding: utf-8 -*-
'''
Fetch the Pic in UNIQLO
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
def DownloadPic(ImgURL,ImgName,OutputDir):
	ImgData = GetPage(ImgURL)
	if ImgName == '':
		ImgName = ImgURL.split('/')[-1]
	# print ImgName
	fp = open(OutputDir+'/'+ImgName,'wb')
	fp.write(ImgData)
	fp.close()

OutputDir = 'E:\= Workspaces\PythonSpace\POICrwal\UNIQLO2\\'
# browser = webdriver.Firefox() # Get local session of firefox
fp = open('UNIQLO.txt','w')
StartURL = 'http://www.uniqlo.cn/search.htm'
for i in xrange(21,51):
	print i
	StartURL = 'http://www.uniqlo.cn/search.htm?orderType=_newOn&viewType=grid&pageNum='+str(i)
	StartPage = GetPage(StartURL)
	soup = BeautifulSoup(StartPage)
	SKUs = soup.findAll('div','desc')

	for i_sku in xrange(0,len(SKUs)) :
		SKUPage = GetPage(SKUs[i_sku].a['href'])
		# browser.get(SKUs[i_sku].a['href']) # Load page
		# soup = BeautifulSoup(SKUPage)
		# soup = BeautifulSoup(str(browser.page_source))
		# gallery = browser.find_elements_by_class_name("gallery")
		PicLinks =  re.findall('<a.*?style=\"background:url\((.*?)_30x30.*?>',SKUPage)
		for ImgURL in PicLinks:
			# ImgURL = soup.find('div','zoom-cache').img['src']
			# ImgName = soup.h3.text.replace('(','_').replace(')','_').replace(' ','_')
			# ImgName = re.sub(u'([^\w \u4e00-\u9fa5])+','',ImgName)+'.jpg'
			ImgName = ''
			DownloadPic(ImgURL,ImgName,OutputDir)

# fp.write(browser.page_source)

# PageURL = 'http://www.uniqlo.cn/search.htm?orderType=_newOn&viewType=grid&pageNum=5'
# PageData = GetPage(PageURL)
# soup = BeautifulSoup(PageData)
# SKUs = soup.findAll('div','desc')
# print len(SKUs)
# SKUPage = GetPage(SKUs[1].a['href'])

# # soup = BeautifulSoup(SKUPage)
# # print soup.find('a',atrrs = {'href':'#'})
# PicLinks =  re.findall('<a.*?style=\"background:url\((.*?)_30x30.*?>',SKUPage)
# print PicLinks

# fp.write(SKUPage)
fp.close()
# browser.close()