# -*- coding: utf-8 -*-
# TMallCrwal
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

def FindBrands(PageURL):
	PageData = GetPage(PageURL)
	soup = BeautifulSoup(PageData)
	Cats = soup.findAll('li',attrs ={'data-tag':'cat'})
	CatNames = [re.sub(u'([^\w \u4e00-\u9fa5])+','',Name.a['title']) for Name in Cats]

	URL_unfold = soup.find('div','av-options').find('a',attrs = {'data-url': True})['data-url']
	Data_unfold = GetPage(URL_unfold)
	RootURL = 'http://list.tmall.com/search_product.htm'
	Data_json = json.loads(Data_unfold.decode('gbk').encode('utf8'))
	brand1 = RootURL + Data_json[0]['href'].replace('&amp;','&')

	for CatName in CatNames:
		print CatName
		fp_cat = open('.\TMall\\'+CatName+'.log','w')
		for item in Data_json:
			BrandInfo = item['title']+'::'+CatName+'::'+RootURL+item['href'].replace('&amp;','&')
			fp_cat.write(BrandInfo+'\n')
		fp_cat.close()

def FindTagsInBrand(PageURL):
	fp_brand = open('brandTag.txt','w')
	data = GetPage(PageURL)
	fp_brand.write(data)
	fp_brand.close()
	soup = BeautifulSoup(data)
	Attrs = [Attr for Attr in soup.findAll('div','attrValues')]
	Tags = []
	for Attr in Attrs:
		# remove (***) after the tag
		Tags = Tags + [re.sub(u'\([0-9]+\)','',tag.text.strip()) for tag in Attr.findAll('li')]
	
	return Tags

def FindPicLinksInPage(data):
	# PicLinks = re.findall('<img.*?\"(.*?)_30x30.*?\"',data)  # For Cloths
	# PicLinks = re.findall(u'<img.*?\"(.*?)_b.*?\"',data)   # For Makeup
	Keywords = ['_30x30','_b']
	PicLinks = []
	for word in Keywords:
		PicLinks += re.findall(u'<img.*?\"(.*?)'+word+u'.*?\"',data)
	return PicLinks

def FindSKUNameInPage(PicLink,data):
	# SKUName = re.findall(u'<img.*?\"'+link+u'_b.*?>[\s\S]*?productTitle[\s\S]*?title=\"(.*?)\"',data)   # For Makeup
	# SKUName = re.findall('<img.*?\"'+link+'_30x30.*?\"[\s\S]*?productTitle[\s\S]*?title=\"(.*?)\"',data)  # For Cloths
	Keywords = ['_30x30','_b']
	SKUName = ['NoName']
	for word in Keywords:
		SKUName += re.findall('<img.*?\"'+PicLink+word+'.*?\"[\s\S]*?productTitle[\s\S]*?title=\"(.*?)\"',data)
	return SKUName


def FindImgInBrand(PageURL,PicDir):
	RootURL = 'http://list.tmall.com/search_product.htm'
	data = GetPage(PageURL).replace('\n\r','')
	soup = BeautifulSoup(data)
	# Find Pics
	PicLinks = FindPicLinksInPage(data)
	fp= open('pagetext.txt','w')
	fp.write(data)
	fp.close()
	print len(PicLinks)
	for link in PicLinks:
		print link
		try:
			SKUName = FindSKUNameInPage(link,data)
			Name = SKUName[-1].decode('gbk').encode('utf8').replace(u'/','')
			Name = re.sub(u'([^\w \u4e00-\u9fa5])+','',Name)
			DownloadPic(link,Name+u'.jpg',PicDir)
			
		except Exception, e:
			print 'at 1',e
		time.sleep(0.5)
	# Walk in other pages
	PageCount = 1
	while soup.find('a','ui-page-next'):
		PageCount = PageCount+1 
		try: 
			NextURL = RootURL + soup.find('a','ui-page-next')['href']
			data = GetPage(NextURL).strip()
			soup = BeautifulSoup(data)

			NewLinks = FindPicLinksInPage(data)
			PicLinks = PicLinks + NewLinks
			for link in NewLinks:
				try:
					SKUName = FindSKUNameInPage(link,data)
					Name = SKUName[-1].decode('gbk').encode('utf8').replace(u'/','')
					Name = re.sub(u'([^\w \u4e00-\u9fa5])+','',Name)
					DownloadPic(link,Name+u'.jpg',PicDir)
				except Exception, e:
					print 'at 2',e 
				time.sleep(1)
		except Exception, e:
			print 'Error In Page:',str(PageCount),e
	return PicLinks

def DownloadPic(ImgURL,ImgName,OutputDir):
	ImgData = GetPage(ImgURL)
	if ImgName == '':
		ImgName = ImgURL.split('/')[-1]
	# print ImgName
	fp = open(OutputDir+'/'+ImgName,'wb')
	fp.write(ImgData)
	fp.close()

def FindStoryInBrand(PageURL):
	Story = ''
	data = GetPage(PageURL)
	soup = BeautifulSoup(data)
	StorySoup = soup.find('a','m-story')
	if StorySoup:
		Story = StorySoup['title']
	return Story

def OutputBrandInfo(BrandName,BrandLink,OutputDir):
	RootDir = OutputDir
	print 'Crawaling',BrandName
	# Make a folder for the brand
	BrandDir = os.path.join(RootDir,BrandName)
	if not os.path.isdir(BrandDir):
		os.mkdir(BrandDir)

	# Output Tags
	fp_tag = open(os.path.join(BrandDir,BrandName+u'_Tag.txt'),'w')
	Tags = FindTagsInBrand(BrandLink)
	for tag in Tags:
		fp_tag.write(tag+'\n')
	fp_tag.close()
	print len(Tags),'tags are found.'

	# Output Story
	if FindStoryInBrand(BrandLink) != '':
		fp_story = open(os.path.join(BrandDir,BrandName+'_Story.txt'),'w')
		fp_story.write(FindStoryInBrand(BrandLink))
		fp_story.close()
		print 'Brand story is found.'

	# Output pictures
	PicDir = os.path.join(BrandDir,'Pictures')
	if not os.path.isdir(PicDir):
		os.mkdir(PicDir)
	print 'Getting pictures...'
	PicLinks = FindImgInBrand(BrandLink,PicDir)
	print len(PicLinks), 'pictures are downloaded.'

def main():
	# PageURL = 'http://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.hpOp2L&cat=50025174&sort=s&style=g&search_condition=7&from=sn_1_rightnav&active=1&industryCatId=50025174&theme=245#J_crumbs'
	# FindBrands(PageURL)
	# lines = open(u'E:\= Workspaces\Python Space\POICrwal\TMall\\精品男装.log').readlines()
	# for line in lines:
	# 	# line = 'Romon/罗蒙::精品男装::http://list.tmall.com/search_product.htm?cat=50025174&brand=29515&sort=s&style=g&search_condition=23&from=sn__brand-qp&active=1&industryCatId=50025174&theme=245&spm=a220m.1000858.0.0.hpOp2L#J_crumbs'
	# 	BrandName = line.split('::')[0].replace(u"/",u"_")
	# 	BrandLink = line.split('::')[-1].strip()
	# 	print BrandName
	# 	try:
	# 		OutputBrandInfo(BrandName,BrandLink,'.\TMall')
	# 	except Exception, e:
	# 		print e
	# PageURL = 'http://list.tmall.com/search_product.htm?spm=a220m.1000858.1000720.1.C7OkYT&cat=50026502&brand=3322567&q=sk+ii&sort=s&style=g&from=sn_1_brand-qp&suggest=0_2#J_crumbs'
	
	# FindTagsInBrand(PageURL)
	# FindImgLinkInBrand(PageURL)
	# FindStoryInBrand(PageURL)

	# BrandName = u'法国兰蔻'
	# BrandLink = 'http://list.tmall.com/search_product.htm?sort=s&style=g&from=sn_1_brand&brand=20067&search_condition=2#J_crumbs'
	
	BrandName = u'欧时力'
	BrandLink = 'http://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.S0MmYP&s=60&q=ochirly+%C5%B7%CA%B1%C1%A6&sort=s&style=g&from=rs_1_key-top-s&type=pc#J_Filter'
	

	OutputBrandInfo(BrandName,BrandLink,'.\TMall')


if __name__ == "__main__":
	main()
	


