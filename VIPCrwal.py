# -*- coding: utf-8 -*-
'''
Fetch the POI in VIP.com
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

# browser = webdriver.Firefox() # Get local session of firefox
# PageLink = 'http://brand.vip.com/' 
# browser.get(PageLink) # Load page
# soup = BeautifulSoup(str(browser.page_source))

FileName = './VIP/vip.htm'
FileLines = open(FileName,'r').readlines()
FileText = ' '.join(FileLines)
FileText.replace('\n','')
FileText.replace(' ','')
soup = BeautifulSoup(FileText)

soup.prettify()
Brands = soup.findAll('li')

# PicPath = './VIP/Logo/'
# brand = Brands[0]
# print len(Brands)
# print brand.img['data-original']
# ImgData = urllib2.urlopen(brand.img['data-original']).read()
# ImgName = brand.span.text.replace('\n','')+'.jpg'
# fp_img = open(PicPath+ImgName,'wb')
# fp_img.write(ImgData)
# fp_img.close()


PicPath = './VIP/Logo/'
fp_result = open('./VIP/VIPResult.txt','w')
for brand in Brands:
	try:
		if brand.find('img'):
			print brand.a['title']
			# wtite the result into the txt file
			fp_result.write(brand.findAll('span')[0].text.replace('\n','')+' :: ')
			fp_result.write(brand.findAll('span')[1].text.replace('\n','')+' :: ')
			fp_result.write(brand.a['href']+'\n')
			# save the logo image
			ImgData = urllib2.urlopen(brand.img['data-original']).read()
			ImgName = brand.span.text.replace('\n','').replace('*','')+'.jpg'
			fp_img = open(PicPath+ImgName,'wb')
			fp_img.write(ImgData)
			fp_img.close()
	except Exception, e:
		print e

