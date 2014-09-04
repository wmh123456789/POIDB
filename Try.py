# try
# -*- coding: utf-8 -*-
import time
import os
import urllib2
import chardet
import codecs
import time 
from bs4 import BeautifulSoup 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# import numpy as np
# import matplotlib.pyplot as plt
# import theano
# By convention, the tensor submodule is loaded as T
# import theano.tensor as T

# theano.test()



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

A = ['a','a',u'b','c','d','d']
B = [1,2,3,4,4,5]
AB = zip(A,B)
d1 = {}  #{'a':1}
d2 = {}  #{1:'a'}
C = {'type': '\xe6\x9c\x8d\xe8\xa3\x85', 'tag': ['\xe5\xa5\xb3\xe8\xa3\x85'], 'cnname': '???', 'name': 'BUOUBVOV', 'enname': u'BUOUBVOV'}
D = C.pop('type')

filepath = '.\TXT\ANSI.txt'
filenew = '.\TXT\utf8.txt'
fp = open(filepath)

data = fp.read()
# print data[0].decode('utf-16').encode('utf-8')
# print len(data[0]),len(data[1]),len(data[2]),len(data[3])
newdata = data.decode('gb18030').encode('utf-8')#.decode('utf-16').encode('utf8')
# print u"ascii多ascii".decode('utf-8').encode('utf-16').decode('utf-16').encode('utf-8')#, u'尚'
print newdata
# print len(newdata)
# open(filenew,'w').write(newdata)



# if data[:2] == codecs.BOM_UTF16_LE:
# 	data = data[2:]
# 	newdata = data.decode('UTF-16LE').encode('utf-8')
# print newdata[:8]
# # fn.close()
# fp.close()




# data = open("Test.txt").read()
# if data[:3] == codecs.BOM_UTF8:
#  data = data[3:]
# print data.decode("utf-8")