# try
# -*- coding: utf-8 -*-
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
		'Referer':'http://www.tmall.com',
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}

	request = urllib2.Request(PageURL, headers=headers)
	ResultContent =urllib2.urlopen(request,timeout=50).read()
	# TransCode for the page
	return ResultContent



BrandName = u'雅诗兰黛'
BrandLink = 'http://esteelauder.tmall.com/category.htm?spm=p738340179.1.w8127914-7045974293.3.HTg7Ia&search=y&scene=taobao_shop'

data = GetPage(BrandLink)
soup = BeautifulSoup(data)
fp = open('tmp.txt','w')
fp.write(data)
fp.close()
# SKUInfo = re.findall(u'<img.*?\"(.*?)_b.*?>[\s\S]*?<p.*?productTitle[\s\S]*?title=\"(.*?)\"',data)   # For Makeup
# PicLinks = re.findall('<img.*?\"(.*?)_b.*?>',data)   # For Makeup
PicLinks = re.findall('<img[\s\S]*?\"(.*?)_30x30.*?>',data)  # For Cloths
if PicLinks:
	link = PicLinks[0]
else:
	link = ''
PicName = re.findall(u'.*?!!(.*?).jpg',link)
print link,PicName
# print re.findall('<img.*?\"'+link+'_b.*?>[\s\S]*?productTitle[\s\S]*?title=\"(.*?)\"',data)
print re.findall(u'<img[\s\S]*?\"'+link+'_30x30.*?>[\s\S]*?class=\"item-name\".*?\">(.*?)</a>',data)[0]



# AllSKU = soup.findAll('div',attrs={'data-id':True})
# for SKU in  AllSKU:
# 	title  = SKU.find('p','productTitle').a['title']
# 	print title

