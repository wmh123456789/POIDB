# -*- coding: utf-8 -*-
'''
Fetch the POI in JD
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

RootPath  = u"E:\= Workspaces\Python Space\POICrwal\\"


def GetPage(PageURL):
	headers = {
		'Referer':'http://www.jd.com',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}

	request = urllib2.Request(PageURL, headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=50).read()
	# TransCode for the page
	return ResultContent


def ListBrandByProduct(ProductLink,TagList,browser):
	BrandTagDict = {}
	PageText = GetPage(ProductLink)
	browser.get(ProductLink) # Load page
	soup = BeautifulSoup(str(browser.page_source))
	Brands = BeautifulSoup(str(soup.find("div","tabcon"))).div


	# soup = BeautifulSoup(PageText)
	# soup.prettify()
	# Brands = soup.findAll(attrs = {'brand':True})
	# if len(Brands)==0:
	# 	Brands = soup.findAll(attrs = {'more':True})
	print 'Find '+str(len(Brands))+' brands in '+TagList[-1]+'\n'

	for brand in Brands.contents:
		if BrandTagDict.has_key(brand.text):
			BrandTagDict[brand.text].append(TagList)
		else:
			BrandTagDict.update({brand.text:TagList})

	return BrandTagDict


def LoopOverCategories(BSAllClass,OutputDir):
	fp = open('ProductList.txt','w')
	browser = webdriver.Firefox() # Get local session of firefox
	for i_category in xrange(7,len(BSAllClass.contents),2):
		try:
			# For each class, contents[1] is head, contents[3] is body
			CategoryName = BSAllClass.contents[i_category].contents[1].h2.string.replace(u"/",u"_")
			CategoryBody = BSAllClass.contents[i_category].contents[3]
			for i_SubCate in xrange(1,len(CategoryBody.contents),2):
				try:
					# In sub-class, [1] is head, [3] is body
					SubCateName = CategoryBody.contents[i_SubCate].contents[1].next.string.replace(u"/",u"_")
					SubCateBody = CategoryBody.contents[i_SubCate].contents[3]
					fp.write('\n-----------------------------\n')
					fp.write(SubCateName+'\n')
					fp.write('-----------------------------\n')
								
					# Output all products in 
					for i_product in xrange(1,len(SubCateBody.contents),2):
						try:
							ProductName = SubCateBody.contents[i_product].next.string.replace(u"/",u"_")
							ProductLink = SubCateBody.contents[i_product].next['href']
							fp.write(ProductName+': '+ProductLink+'\n')

							# Output All brands of a product
							fp_product = open(OutputDir+ProductName+'.txt','w')
							BrandDict = ListBrandByProduct(ProductLink,[CategoryName,ProductName],browser)
							for brand in BrandDict:
								fp_product.write(brand+':')
								for tag in BrandDict[brand]:
									try:
										fp_product.write(' '+tag)
									except Exception, e:
										print e,tag
									
														
								fp_product.write('\n')
							fp_product.close()
						except Exception, e:
							print e
				except Exception, e:
					print e
		except Exception, e:
			print e


	fp.close()
	browser.close()

OfflineFilePath = "JDAllBrand.htm"
FileLines = open(OfflineFilePath,'r').readlines()
FileText = ' '.join(FileLines).decode('GB2312').encode('utf8')
FileText.replace('\n','')
FileText.replace(' ','')
soup = BeautifulSoup(FileText)
soup.prettify()
#Contents in the left colum
AllClassLeft = soup.contents[2].contents[3].contents[17].contents[1]
#Contents in the right colum
AllClassRight = soup.contents[2].contents[3].contents[17].contents[4]
# From contents[7],start with'Computer', than [11],[13]




LoopOverCategories(AllClassRight,RootPath+u'JD\\')




# fp = open('bed.txt','w')

# TempLink = 'http://list.jd.com/1620-1621-1626.html'
# PageText = GetPage(TempLink)
# soup = BeautifulSoup(str(PageText))
# # Brands = soup.findAll(attrs = {'id':True})
# print soup.find("div","tabcon")

# fp.write(PageText)



# BrandDict = ListBrandByProduct(TempLink,['a'])
# print len(BrandDict)
# for brand in BrandDict:
# 	print brand,BrandDict[brand],'\n'

# for brand in BrandDict:
# 	fp.write(brand+':')
# 	for tag in BrandDict[brand]:
# 		fp.write(' '+tag)
# 	fp.write('\n')


# fp.close()


 

