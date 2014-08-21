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


# key = ['x']*10
# A = xrange(0,10)
# B = ['']*1
# C = []
# # print [{k:[v,b]} for k,v,b in zip(key,A,B)]

# # empty = lambda l: l=key if l==[]

# BrandDB = {'0':{'name':'','cnname':'','enname':'','type':'','tag':['']}}
# BrandDB['0']['tag'] = ['a','b']
# print str(len(BrandDB))+'ok', BrandDB

# fp = open('test.txt','a')
# fp.write('adfad\n')
# fp.close()
# fp = open('test.txt','a')
# fp.write(str(key)+'\n')
# fp.close()
# fp = open('test.txt','a')
# fp.write(str(BrandDB)+'\n')
# fp.close()

A = ['a','a','b','c','d','d']
B = [1,2,3,4,4,5]
AB = zip(A,B)
d1 = {}  #{'a':1}
d2 = {}  #{1:'a'}

for a,i in AB :
	# For d1:
	if a in d1:
		d1[a] = list(set(d1[a]+[i]))
	else:
		d1[a] = [i]

	# For d2:
	if i in d2:
		d2[i] = list(set(d2[i]+[a]))
	else:
		d2[i] = [a]


print d1
print d2



