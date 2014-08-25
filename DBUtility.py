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
def ReadCSV(FilePath,KeyList,SpaceMark=','):
	fp = open(FilePath,'r')
	AllData = []
	KeyLen = len(KeyList)
	Records = []
	for line in fp.readlines():
		words = line.split(SpaceMark)
		if len(words) >= KeyLen:
			record = dict(zip(KeyList,words))
			Records.append(record)
			pass
		else:
			print words
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
		name = unicode(name)
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
		if key in ['name','cnname','enname','type']:
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
The format of the BrandDB record:
{BrID:{name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}}
The format of the POIDB record:
{PID:{name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}}
'''

def UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist=[],CnNamelist=[],EnNamelist=[],
							Typelist=[],Taglist=[]):
	# {PID:{name:'',cnname:'',enname:'',type:'',tag:[tag1,tag2,...]}}
	if BrandDB == {}:
		BrandDB = {'-1':{'name':'','cnname':'','enname':'','type':'','tag':['']}}

	# Deal with empty list
	EmptyList = lambda N: ['']*N
	N = len(PIDlist)
	if CnNamelist == []:
		CnNamelist = EmptyList(N)
	if EnNamelist == []:
		EnNamelist = EmptyList(N)
	if Typelist == []:
		Typelist = EmptyList(N)
	if Taglist == []:
		Taglist = EmptyList(N)


	NewItems = {pid:{'name':name,'cnname':cnname,'enname':enname,'type':typ,'tag':tag} 
					for pid,name,cnname,enname,typ,tag in 
					zip(PIDlist,Namelist,CnNamelist,EnNamelist,Typelist,Taglist)}
	NameIndex = IndexByName(BrandDB,'name')

	# Search By Name
	for pid in NewItems:
		if NewItems[pid]['name'] in  NameIndex:
			NewBrRecord = {'name':NewItems[pid]['name'],
			 			 'cnname':NewItems[pid]['cnname'],
						 'enname':NewItems[pid]['enname'],	
						 'type':NewItems[pid]['type'],
						 'tag':NewItems[pid]['tag']}
			BrID_cur = NameIndex[NewItems[pid]['name']][0]
			# print BrID_cur
			Record_M = MergeBrandDBRecord(NewBrRecord,BrandDB[BrID_cur])
			BrandDB.update({BrID_cur:Record_M})
			pass
		else:
		
			# # For Debug
			# if NewItems[pid]['name'] == 'Coach' and len(BrandDB)>250:
			# 	print 'find coach','Coach' in NameIndex
			# 	print BrandDB['213']				
			# 	print NameIndex['Coach']
			# # -- For Debug

			# Insert new record
			BrandDB.update({str(len(BrandDB)):{'name':NewItems[pid]['name'],
								 'cnname':NewItems[pid]['cnname'],
								 'enname':NewItems[pid]['enname'],	
								 'type':NewItems[pid]['type'],
								 'tag':NewItems[pid]['tag']}})
			NameIndex = IndexByName(BrandDB,'name')

	return BrandDB


'''
Update dict by append the val_list
{key:[val1]} + {key:[val2]} = {key:[val1,val2]}
'''
def UpdateDictbyAppend(DB,items):
	for key in items.keys():
		if key in DB:
			print DB[key],items[key]
			DB[key] = list(set(DB[key]+[items[key]]))
		else:
			DB.update({key:[items[key]]})

'''
For Tag list output:
[tag1,tag2,tag3...] => tag1 tag2 tag3 ...
'''
def StrTag(Taglist,SpaceMark):
	StrTag = ''
	for tag in Taglist:
		StrTag += str(tag)+SpaceMark
	return StrTag


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

		# For Debug
		# if DB[key][NameField] == 'Coach':
		# 	print 'Got coach in index func:',key
		# 	print DB[key]
		# -- For Debug


	pass
	return NameDict

'''
Query the brand info in BrandDB by name 
'''
def QueryBrInfoByName(name,BrandDB,NameIndex={}):
	if NameIndex == {}:
		NameIndex = IndexByName(BrandDB,'name')
	if name in NameIndex:
		return BrandDB[NameIndex[name][0]]
	else:
		return {}


'''
Query the brand info in BrandDB by names in the Namelist
For dupulicated name, it gives dupulicated record 
Input NameList: [name1,name2,....]
Output format: [{name:name1,type:XX,...},{name:name2,type:XXX...},...]
'''
def QueryBrInfoByNameList(Namelist,BrandDB,NameIndex={}):
	InfoList = [] 
	if NameIndex == {}:
		NameIndex = IndexByName(BrandDB,'name')
	for name in Namelist:
		info = QueryBrInfoByName(name,BrandDB,NameIndex)
		info = info.update({'name':name})
		InfoList.append(info)
	return InfoList


'''
Insert Infromation into POI list
Output format: {PID:{name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}}
'''
def InsertInfoInPOIList(PIDlist,Namelist,BrandDB):
	InfoList = QueryBrInfoByNameList(Namelist,BrandDB)
	POIDB = {}
	for pid,info in zip(PIDlist,InfoList):
		POIDB.update({pid:info})

	return POIDB


def main():

	# Add Mall 1 into DB
	KeyList = ['PID','name','type','tag','phone']
	FilePath = '.\DataInMall\ShuangAn.csv'
	data = ReadCSV(FilePath,KeyList)
	print data[50]['name'],data[50]['tag'],data[50]['type']

	Namelist = [record['name'] for record in data]
	CnNameList,EnNameList = CNNamelistFilter(Namelist)
	PIDlist = [record['PID'] for record in data]
	Typelist = [record['type'] for record in data]
	Taglist = [[record['tag']] for record in data]
	Phonelist = [record['phone'] for record in data]
	BrandDB = {}
	BrandDB = UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist)
	fp = open('.\TXT\output.txt','w')
	print len(BrandDB)
	# for key in BrandDB:
	# 	fp.write(key+'\t'+str(BrandDB[key]['name']).encode('utf8')+'\n')

	# Add Mall 2 into DB
	FilePath = '.\DataInMall\HuaRunWuCaiCheng.csv'
	KeyList = ['PID','name','type','tag','phone']
	data = ReadCSV(FilePath,KeyList)
	print data[50]['name'],data[50]['tag'],data[50]['type']

	Namelist = [record['name'] for record in data]
	CnNameList,EnNameList = CNNamelistFilter(Namelist)
	PIDlist = [record['PID'] for record in data]
	Typelist = [record['type'] for record in data]
	Taglist = [[record['tag']] for record in data]
	Phonelist = [record['phone'] for record in data]
	BrandDB = UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist)

	print len(BrandDB)
	# for key in BrandDB:
	# 	fp.write(key+'\t'+str(BrandDB[key]['name']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['cnname']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['enname']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['type']).encode('utf8')+
	# 		'\t'+StrTag(BrandDB[key]['tag'],'\t').encode('utf8')+'\n')

	FilePath = '.\TXT\ShuangAnShangChang_POI.txt'
	KeyList = ['PID','name']
	data = ReadCSV(FilePath,KeyList,'\t')
	print data[50]['PID'],data[50]['name']
	PIDlist = [record['PID'] for record in data]
	Namelist = [record['name'] for record in data]

	POIDB = InsertInfoInPOIList(PIDlist,Namelist,BrandDB)
	fp_poi = open('.\TXT\POIDB.txt','w')
	for key in POIDB:
		fp_poi.write(str(POIDB[key])+'\n')
	


	fp.close()
	fp_poi.close()




if __name__ == '__main__':
	main()