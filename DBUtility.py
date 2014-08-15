# -*- coding: utf-8 -*-
import os
import shutil
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
Read CSV file to a List
each line(record) in CSV is a element(dict) in the List
in each element(dict), keys are given by KeyList

'''
def ReadCSV(FilePath,KeyList):
	fp = open(FilePath,'r')
	AllData = []
	KeyLen = len(KeyList)
	Records = []
	for line in fp.readlines():
		words = line.split(',')[:-1]
		if len(words) == KeyLen:
			record = dict(zip(KeyList,words))
			Records.append(record)
			pass
		else:
			print 'Error, word length is not match.',len(words),KeyLen
	return Records


'''
Update the oldlist
if item in newlist is not in oldlist, add it.
'''
def UpdateList(oldlist,newlist):
	for item in newlist:
		if not item in oldlist:
			oldlist.append(item)
	return oldlist

'''
Distinguish the Chinese name by the first character.
transform the name list into ChineseName list and nonChineseName list
['中文','English'] => ['中文','???'], ['???','English']
'''
def CNNamelistFilter(Namelist):
	CnNameList = []
	EnNameList = []
	for name in Namelist:
		if re.findall(u'[\u4e00-\u9fa5]',name):
			CnNameList.append(name)
			EnNameList.append('???')
		else:
			EnNameList.append(name)
			CnNameList.append('???')

	return CnNameList,EnNameList


'''
The format of the brandDB record:
{PID:[name,cnname,enname,type,[tag1,tag2,...]]}
'''

def UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist=[],CnNameList=[],EnNameList=[],
							Typelist=[],Taglist=[]):
	# {PID:[name,cnname,enname,type,[tag1,tag2,...]]}

	pass

'''
Update dict by append the val_list
{key:[val1]} + {key:[val2]} = {key:[val1,val2]}
'''
def UpdateDictbyAppend(DB,items):
	for key in items.keys():
		if key in DB:
			DB[key] = list(set(DB[key]+items[key]))
		else:
			DB.update({key:items[key]})

'''
{PID:[name,....]} => {name:[PID1,PID2,....]}
'''
def IndexByName(BrandDB):
	NameDict = {}
	for pid in BrandDB:
		BrandDB['pid']
	pass

'''
{PID:[...,cnname,...]} => {cnname:[PID1,PID2,....]}
'''
def IndexByCnName(BrandDB):
	pass

'''
{PID:[...,enname,...]} => {enname:[PID1,PID2,....]}
'''
def IndexByEnName(BrandDB):
	pass







def main():
	KeyList = ['PID','name','type','tag','phone']
	FilePath = 'E:\POIClassify\ShuangAn.csv'
	data = ReadCSV(FilePath,KeyList)
	print data[50]['name'],data[50]['tag'],data[50]['type']

	Namelist = [record['name'] for record in data]
	CnNameList,EnNameList = CNNamelistFilter(Namelist)
	PIDlist = [record['PID'] for record in data]
	Typelist = [record['type'] for record in data]
	Taglist = [record['tag'] for record in data]
	Phonelist = [record['phone'] for record in data]


if __name__ == '__main__':
	main()