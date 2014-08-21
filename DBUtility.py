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
Merge 2 Records(New and Old) in safe way:
name is main key. if New name matches old cnname or enname, update. 
if not, output Records and not merge
for cnname,enname,type, if not conflict, update. 
if conflict, output Records and not merge
for  tag, merge the tag list 
'''

def MergeBrandDBRecord(NewBrRecord,OldBrRecord):
	Record_M = {'name':'','cnname':'','enname':'','type':'','tag':['']}
	fp = open('MergeFailedRecords.txt','a')
	for key in NewBrRecord:
		if key == 'name':
			if not (NewBrRecord[key] in ['','???']): 
				if (OldBrRecord[key] in ['','???']):
					Record_M[key] = NewBrRecord[key]
				elif OldBrRecord[key] != NewBrRecord[key]:
					if NewBrRecord[key] in [OldBrRecord['enname'],OldBrRecord['cnname']]:
						Record_M[key] = NewBrRecord[key]
					else:
						fp.write(str(OldBrRecord)+' => '+str(NewBrRecord)+'\n')
						return OldBrRecord
				else:  #OldBrRecord[key] == NewBrRecord[key]
					Record_M[key] = OldBrRecord[key]
			else: #NewBrRecord[key] in ['','???']
				Record_M[key] = OldBrRecord[key]

			pass
		elif key in ['cnname','enname','type']:
			if not (NewBrRecord[key] in ['','???']):
				if (OldBrRecord[key] in ['','???']):
					Record_M[key] = NewBrRecord[key]
				elif OldBrRecord[key] != NewBrRecord[key]:
					fp.write(str(OldBrRecord)+' => '+str(NewBrRecord)+'\n')
					return OldBrRecord
				else: #OldBrRecord[key] == NewBrRecord[key]
					Record_M[key] = OldBrRecord[key]
			else: #NewBrRecord[key] in ['','???']
				Record_M[key] = OldBrRecord[key]
			pass
		elif key == 'tag':
			Record_M['tag'] = list(set(NewBrRecord['tag']+OldBrRecord['tag']))
		else: 
			print 'Key Error, cannot find the key:', key

	fp.close()
	return Record_M


'''
Merge 2 Records(New and Old) in unsafe way:
Update the data with the NewBrRecord if conflict
Append the new tags
'''
def UpdateBrandDBRecord(NewBrRecord,OldBrRecord):
	Record_M = {'name':'','cnname':'','enname':'','type':'','tag':['']}
	for key in NewBrRecord:
		if key in ['name','cnname','enname','type']
			if NewBrRecord[key] in ['','???']:
				Record_M = OldBrRecord[key]
			else:
				Record_M = NewBrRecord[key]
		elif key == 'tag':
			Record_M['tag'] = list(set(NewBrRecord['tag']+OldBrRecord['tag']))
		else:
			print 'Key Error, cannot find the key:', key
	return Record_M




'''
The format of the brandDB record:
{PID:{name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}}
'''

def UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist=[],CnNameList=[],EnNameList=[],
							Typelist=[],Taglist=[]):
	# {PID:[name,cnname,enname,type,[tag1,tag2,...]]}
	if BrandDB == {}:
		BrandDB = {'0':{'name':'','cnname':'','enname':'','type':'','tag':['']}}

	# Deal with empty list
	EmptyList = lambda N: ['']*N
	N = len(PIDlist)
	if CnNameList == []:
		CnNameList = EmptyList(N)
	if EnNameList == []:
		EnNameList = EmptyList(N)
	if TypeList == []:
		TypeList = EmptyList(N)
	if TagList == []:
		TagList = EmptyList(N)


	NewItems = {pid:{'name':name,'cnname':cnname,'enname':enname,'type':typ,'tag':tag} 
					for pid,name,cnname,enname,typ,tag in 
					zip(PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist)}
	NameIndex = IndexByName(BrandDB,'name')

	# Search By Name
	for pid in NewItems:
		if NewItems['pid']['name'] in  NameIndex:
			NewBrRecord = {'name':NewItems['pid']['name'],
			 			 'cnname':NewItems['pid']['cnname'],
						 'enname':NewItems['pid']['enname'],	
						 'type':NewItems['pid']['type'],
						 'tag':NewItems['pid']['tag']}
			BrID_cur = NameIndex[NewItems['pid']['name']]
			Record_M = MergeBrandDBRecord(NewBrRecord,BrandDB[BrID_cur])
			BrandDB.update({BrID_cur:Record_M})
			pass
		else:
			# Insert new record
			BrandDB.update({str(len(BrandDB)):{'name':NewItems['pid']['name'],
								 'cnname':NewItems['pid']['cnname'],
								 'enname':NewItems['pid']['enname'],	
								 'type':NewItems['pid']['type'],
								 'tag':NewItems['pid']['tag']}})



	pass

'''
Update dict by append the val_list
{key:[val1]} + {key:[val2]} = {key:[val1,val2]}
'''
def UpdateDictbyAppend(DB,items):
	for key in items.keys():
		if key in DB:
			DB[key] = list(set(DB[key]+[items[key]]))
		else:
			DB.update({key:[items[key]]})


'''
@param BrandDB :  The DB to be indexed
@param NameField: The field to be indexed
@usage:
NameField = 'name':   {PID:[name,....]} => {name:[PID1,PID2,....]}
NameField = 'cnname': {PID:[cnname,....]} => {cnname:[PID1,PID2,....]}
'''
def IndexByName(DB,NameField):
	NameDict = {}
	for key in DB:
		UpdateDictbyAppend(NameDict,{DB[key][NameField]:key})
	pass
	return NameDict

def main():
	KeyList = ['PID','name','type','tag','phone']
	FilePath = '.\DataInMall\ShuangAn.csv'
	data = ReadCSV(FilePath,KeyList)
	print data[50]['name'],data[50]['tag'],data[50]['type']

	Namelist = [record['name'] for record in data]
	CnNameList,EnNameList = CNNamelistFilter(Namelist)
	PIDlist = [record['PID'] for record in data]
	Typelist = [record['type'] for record in data]
	Taglist = [record['tag'] for record in data]
	Phonelist = [record['phone'] for record in data]

	DB = {pid:{'name':name} for pid,name in zip(PIDlist,Namelist)}
	NameDict = IndexByName(DB,'name')

	NewBrRecord = {'name':'2','cnname':'???','enname':'12','type':'33','tag':['ad']}
	OldBrRecord = {'name':'111','cnname':'2','enname':'12','type':'33','tag':['as']}
	print str(MergeBrandDBRecord(NewBrRecord,OldBrRecord))


if __name__ == '__main__':
	main()