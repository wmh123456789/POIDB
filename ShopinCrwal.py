# -*- coding: utf-8 -*-
# ShopinCrwal

# import json
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

def GetPage(PageURL):
	headers = {
		'Referer':'http://www.shopin.net',
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
	# Find dir
	if not os.path.isdir(OutputDir):
		os.mkdir(OutputDir)
	# print ImgName
	fp = open(OutputDir+'/'+ImgName,'wb')
	fp.write(ImgData)
	fp.close()
def DownloadPicsInBrand(BrandName,BrandURL,RootURL,OutputDir):
	BrandDir = os.path.join(OutputDir,BrandName)
	BrandPage = GetPage(BrandURL)
	soup = BeautifulSoup(BrandPage)
	IMGLinks = soup.findAll('a',attrs = {'class':'productImg'})
	for link in IMGLinks:
		try:
			SKUImgLink = re.sub(u'.resize_to.*?.jpg','',link.img['data-original'])+'.jpg'
			PicID =  SKUImgLink.split('/')[-1].split('_')[0].replace('Pic','')
			SKUName = link.h3.text + '_' + PicID +'.jpg'
			print SKUName
			DownloadPic(SKUImgLink,SKUName,BrandDir)
		except Exception, e:
			print e
		pass
	NextSoup = soup.find('a',attrs = {'class':'transition next'})
	NextURL = ''
	if NextSoup:
		NextURL = RootURL + NextSoup['href'] 

	while NextURL!='':
		BrandPage = GetPage(NextURL)
		soup = BeautifulSoup(BrandPage)
		IMGLinks = soup.findAll('a',attrs = {'class':'productImg'})
		# print len(IMGLinks)
		for link in IMGLinks:
				try:
					SKUImgLink = re.sub(u'.resize_to.*?.jpg','',link.img['data-original'])+'.jpg'
					PicID =  SKUImgLink.split('/')[-1].split('_')[0].replace('Pic','')
					SKUName = link.h3.text + '_' + PicID +'.jpg'
					print SKUName
					DownloadPic(SKUImgLink,SKUName,BrandDir)
				except Exception, e:
					print e
				pass
		NextSoup = soup.find('a',attrs = {'class':'transition next'})
		NextURL = ''
		if NextSoup:
			NextURL = RootURL + NextSoup['href'] 
		
BrandName = 'WRC'
BrandURL= 'http://search.shopin.net/brandlist/0-508-0-0-0-0-0-0-1-0.html'
RootURL = 'http://search.shopin.net'
OutputDir = 'E:\POIClassify\Sites\ShopIn'
DownloadPicsInBrand(BrandName,BrandURL,RootURL,OutputDir)
