# -*- coding: utf-8 -*-
import os
import shutil
import re
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

'''
Read XML file to a List
XML will code by UTF8, by WPS office/MS office
keylist likes: ['kk','xxx','vv']
records likes: [{kk:KK,xxx:XXX,vv:VV..},{}] 
'''
def ReadXML(FilePath,KeyList):
	KeyLen = len(KeyList)
	Records = []
	FileLines = open(FilePath,'r').readlines()
	FileText = ' '.join(FileLines)
	soup = BeautifulSoup(FileText)
	soup.prettify()
	for row in soup.findAll('row'):
		AllData = row.findAll('cell')
		words = [data.text.strip() for data in AllData]
		if len(words) >= KeyLen:
			record = dict(zip(KeyList,words))
			Records.append(record)
			pass
		else:
			print len(AllData)
			print 'Error, word length is not match.',len(words),KeyLen
	return Records


'''
Read CSV file to a List
each line(record) in CSV is a element(dict) in the List
in each element(dict), keys are given by KeyList
keylist likes: ['kk','xxx','vv']
records likes: [{kk:KK,xxx:XXX,vv:VV..},{}] 
'''
def ReadCSV(FilePath,KeyList,SpaceMark=','):
	fp = open(FilePath,'rU')
	AllData = []
	KeyLen = len(KeyList)
	Records = []
	for line in fp.readlines():
		words = [word.strip() for word in line.split(SpaceMark)]
		# print words[0]
		if len(words) >= KeyLen:
			record = dict(zip(KeyList,words))
			Records.append(record)
			pass
		else:
			print words
			print 'Error, word length is not match.',len(words),KeyLen
	# print len(Records)
	return Records


'''
Read data file: read data file to a list
Function is same with ReadCSV, default SpaceMark is tab
keylist likes: ['kk','xxx','vv']
records likes: [{kk:KK,xxx:XXX,vv:VV..},{}] 
'''
def ReadDAT(FilePath,KeyList,SpaceMark='\t'):
	fp = open(FilePath,'r')
	AllData = []
	KeyLen = len(KeyList)
	Records = []
	for line in fp.readlines():
		words = [word.strip() for word in line.split(SpaceMark)]
		
		if len(words) >= KeyLen:
			record = dict(zip(KeyList,words))
			Records.append(record)
			pass
		else:
			print words
			print 'Error, word length is not match.',len(words),KeyLen
	# print len(Records)
	return Records

'''
Convert Raw record list to DB format
[{kk:KK,xxx:XXX,vv:VV..},{}] => {KK:{xxx:XXX,vv:VV,...},{...},...} 
'''
def Recodelist2DB(recordlist,keyfield):
	NewDB = {}
	for record in recordlist:
		rec = record.copy()
		key = rec.pop(keyfield)
		NewDB.update({key:rec})
	return NewDB


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
		# name = unicode(name)
		if re.findall(u'[\u4e00-\u9fa5]',unicode(name)):
			CnNameList.append(name)
			EnNameList.append('???')
		else:
			EnNameList.append(name)
			CnNameList.append('???')

	return CnNameList,EnNameList

'''
Match the Name by lower case
Return Boolean value
'''
def MatchNameByLowerCase(Name,NameList):
	NameLow = Name.lower()
	NameLowList = [n.lower() for n in NameList]
	return NameLow in NameLowList

'''
Updata Names By E-C Name dict
@param: DB : {KK:{'cnname':XXX,'enname':VV,...},{...},...}
@param: ECDict [{'cnname':'中','enname':'EN'},{,},...]
output: NewCnNameList, NewEnNameList
'''
def UpdateNameByECDict(DB,ECDict):
	print 'Start updating...'
	CnIndex = Recodelist2DB(ECDict,'cnname')
	EnIndex = Recodelist2DB(ECDict,'enname')
	EnIndexLow = {key.lower():EnIndex[key] for key in EnIndex} 
	N = 0
	print "Keys in DB:",len(DB.keys())

	NewNames = []   # Record the new names 
	for key in DB:
		# print CnIndex['英纳格']
		EnName = DB[key]['enname']
		CnName = DB[key]['cnname']
		# Add New Name, if not yet
		if  CnName in ['','null','???']:
			if MatchNameByLowerCase(EnName,EnIndex.keys()):
				name = EnIndexLow[EnName.lower()]['cnname'] 
				DB[key].update({'cnname':name})
				print 'New Name Added:',name 
				N += 1
			else: # Cannot find EnName
				NewNames.append(EnName)
				print 'Cannot find:',EnName 
			pass
		elif EnName in ['','null','???']:
			if CnName in CnIndex:
				name = CnIndex[CnName]['enname'] 
				DB[key].update({'enname':name})
				print 'New Name Added:',name 
				N += 1
			else:
				NewNames.append(CnName)
				print 'Cannot find:',CnName 
			pass
		elif not EnName in EnIndex :
			NewNames.append(EnName)
			print 'Cannot find:',EnName 
			pass
		elif not CnName in CnIndex:
			NewNames.append(CnName)
			print 'Cannot find:',CnName
			pass
		elif EnName != CnIndex[CnName]['enname']:
			print 'Name conflict:',EnName,CnName,CnIndex[CnName]['enname']
		elif CnName != EnIndex[EnName]['cnname']:
			print 'Name conflict:',CnName,EnName,EnIndex[EnName]['cnname']
		else: # Name matches
			pass
	print 'Find name pairs:', N

	# TODO: output the conflict name pairs 

	return CNNamelistFilter(NewNames)


	pass


'''
Merge 2 Records(New and Old) in safe way:
name is main key. if New name matches old cnname or enname, update. 
if not, output Records and not merge
for cnname,enname,type, if not conflict, update. 
if conflict, output Records and not merge
for  tag, merge the tag list 
'''

def MergeBrandDBRecord(NewBrRecord,OldBrRecord):
	Record_M = {'name':'','cnname':'','enname':'','type':'','tag':[''],'phone':'','story':''}
	fp = open('MergeFailedRecords.txt','a')
	for key in NewBrRecord:
		if key == 'name':
			if not (NewBrRecord[key] in ['','???']): 
				if (OldBrRecord[key] in ['','???']):
					Record_M[key] = NewBrRecord[key]
				elif OldBrRecord[key].lower() != NewBrRecord[key].lower():
					if NewBrRecord[key].lower() in [OldBrRecord['enname'].lower(),OldBrRecord['cnname']]:
						Record_M[key] = NewBrRecord[key]
					else:
						NameConflicMsg = StrRecord(OldBrRecord)+' => '+StrRecord(NewBrRecord)
						fp.write(NameConflicMsg+'\n')
						print 'Find Name conflict:', NameConflicMsg
						return OldBrRecord
				else:  #OldBrRecord[key].lower() == NewBrRecord[key].lower()
					Record_M[key] = OldBrRecord[key]
			else: #NewBrRecord[key] in ['','???']
				Record_M[key] = OldBrRecord[key]

			pass
		elif key in ['cnname','enname','type','phone','story']:
			if not (NewBrRecord[key] in ['','???']):
				if (OldBrRecord[key] in ['','???']):
					Record_M[key] = NewBrRecord[key]
				elif OldBrRecord[key].lower() != NewBrRecord[key].lower():
					NameConflicMsg = StrRecord(OldBrRecord)+' => '+StrRecord(NewBrRecord)
					fp.write(NameConflicMsg+'\n')
					# print 'Find Record conflict:', NameConflicMsg
					return OldBrRecord
				else: #OldBrRecord[key].lower() == NewBrRecord[key].lower()
					Record_M[key] = OldBrRecord[key]
			else: #NewBrRecord[key] in ['','???']
				Record_M[key] = OldBrRecord[key]
			pass
		elif key == 'tag':
			Record_M['tag'] = list(set(NewBrRecord['tag']+OldBrRecord['tag']))
		else: 
			print 'Key Error, cannot find the key:', key

	fp.close()
	# # for Debug
	# if len(Record_M['tag'])>2:
	# 	print 'find long tag list:',len(Record_M['tag'])
	# #- for Debug
	return Record_M


'''
Merge 2 Records(New and Old) in unsafe way:
Update the data with the NewBrRecord if conflict
Append the new tags
'''
def UpdateBrandDBRecord(NewBrRecord,OldBrRecord):
	Record_M = {'name':'','cnname':'','enname':'','type':'','tag':[''],'phone':'','story':''}
	for key in NewBrRecord:
		if key in ['name','cnname','enname','type','phone','story']:
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
@Param input：PIDlist,Namelist,CnNamelist,EnNamelist,Typelist,Taglist,Phonelist,Storylist
@Param output：BrandDB

'''

def UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist=[],CnNamelist=[],EnNamelist=[],
							Typelist=[],Taglist=[],Phonelist=[],Storylist=[]):
	# {PID:{name:'',cnname:'',enname:'',type:'',tag:[tag1,tag2,...]}}
	if BrandDB == {}:
		BrandDB = {'-1':{'name':'','cnname':'','enname':'','type':'','tag':[''],'phone':'','story':''}}

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
	if Phonelist == []:
		Phonelist = EmptyList(N)
	if Storylist == []:
		Storylist = EmptyList(N)	

	# initialize the input POI DB
	NewItems = {pid:{'name':name,'cnname':cnname,'enname':enname,'type':typ,'tag':tag,'phone':phone,'story':story} 
					for pid,name,cnname,enname,typ,tag,phone,story in 
					zip(PIDlist,Namelist,CnNamelist,EnNamelist,Typelist,Taglist,Phonelist,Storylist)}
	NameIndex = IndexByName(BrandDB,'name')

	# Search By Name
	for pid in NewItems:
		if NewItems[pid]['name'] in  NameIndex:  #Current POI info is in BrandDB
			NewBrRecord = {'name':NewItems[pid]['name'],
			 			 'cnname':NewItems[pid]['cnname'],
						 'enname':NewItems[pid]['enname'],	
						 'type':NewItems[pid]['type'],
						 'tag':NewItems[pid]['tag'],
						 'phone':NewItems[pid]['phone'],
						 'story':NewItems[pid]['story']}
			BrID_cur = NameIndex[NewItems[pid]['name']][0] # Assume the first BrID is matched.
			# print BrID_cur
			Record_M = MergeBrandDBRecord(NewBrRecord,BrandDB[BrID_cur])
			BrandDB.update({BrID_cur:Record_M})
			pass
		else: #Current POI info is not in BrandDB
		
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
								 'tag':NewItems[pid]['tag'],
								 'phone':NewItems[pid]['phone'],
						 		 'story':NewItems[pid]['story']}})
			NameIndex = IndexByName(BrandDB,'name')

	return BrandDB

'''
Read a data-ready file and update the BrandDB
Support file format: txt,csv,xml(recommended)

'''
def UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB={}):
	ExtName = os.path.splitext(FilePath)[1]
	if ExtName == '.xml':
		data = ReadXML(FilePath,KeyList)
	elif ExtName == '.csv':
		data = ReadCSV(FilePath,KeyList)
	else: # .txt or other self-defined formats 
		data = ReadDAT(FilePath,KeyList)

	Namelist = [record['name'] for record in data]
	CnNameList,EnNameList = CNNamelistFilter(Namelist)

	PIDlist = [record['pid'] for record in data]
	Typelist = [record['type'] for record in data]
	Taglist = [[record['tag']] for record in data]
	Phonelist = [record['phone'] for record in data]
	Storylist = [record['story'] for record in data]
	BrandDB = UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist,Phonelist,Storylist)
	return BrandDB


'''
Update dict by append the val_list
{key:[val1]} + {key:[val2]} = {key:[val1,val2]}
Can be useed in tag-merge, or generating name index 
'''
def UpdateDictbyAppend(DB,items):
	for key in items.keys():
		if key in DB:
			# print DB[key],items[key]
			DB[key] = list(set(DB[key]+[items[key]]))
		else:
			DB.update({key:[items[key]]})

'''
For Tag list output:
[tag1,tag2,tag3...] => tag1 tag2 tag3 ...
TagNum is the tag number to output, if tags not enough, gives ''
'''
def StrTag(Taglist,SpaceMark='\t',TagNum = 2):
	StrTag = ''
	# for tag in Taglist:
	# 	StrTag += str(tag)+SpaceMark
	if len(Taglist)>2:
		print 'find long tag list:',len(Taglist)

	for i in xrange(TagNum):
		if len(Taglist)>0:
			StrTag += str(Taglist.pop(0))+SpaceMark
		else:
			StrTag += 'null'+SpaceMark

	return StrTag

'''
For Record output:
{name:XX,tag:[tag1,tag2,...]} => XX tag1 tag2 ...
'''
def StrRecord(Record,SpaceMark='\t',Order = []):
	StrRecord = ''
	if Order == []:
		for key in Record:
			if key == 'tag':
				StrRecord += StrTag(Record['tag'],SpaceMark)
			else:
				# print Record
				StrRecord += str(Record[key]+SpaceMark)
		return StrRecord
	else: # if the output order is fixed 
		for key in Order:
			if key in Record:
				if key == 'tag':
					StrRecord += StrTag(Record['tag'],SpaceMark)
				else:
					# print Record
					StrRecord += str(Record[key]+SpaceMark)
				pass
			else:
				StrRecord += ''+SpaceMark
				print 'Error when output Recod, cannot find key:',key
		return StrRecord

'''
@param DB :  The DB to be indexed
@param NameField: The field to be indexed
@usage:
NameField = 'name':   {ID:{'name':,....}} => {name:[ID1,ID2,....]}
NameField = 'cnname': {ID:{'cnname':,....}} => {cnname:[ID1,ID2,....]}
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
Function is same with IndexByName
All names in output-dict are in lower case
'''
def IndexByLowerName(DB,NameField):
	NameDict = {}
	for key in DB:
		UpdateDictbyAppend(NameDict,{DB[key][NameField].lower():key})

		# For Debug
		# if DB[key][NameField] == 'Coach':
		# 	print 'Got coach in index func:',key
		# 	print DB[key]
		# -- For Debug


	pass
	return NameDict

'''
Query the brand info in BrandDB by name 
@Param output: {name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}
NOTE: it DOESNOT return the BrID
'''
def QueryBrInfoByName(name,BrandDB,NameIndex={}):
	if NameIndex == {}:
		NameIndex = IndexByName(BrandDB,'name')
	if name in NameIndex:
		return BrandDB[NameIndex[name][0]] # Retern the first BrID in Nameindex as default
	else:
		return {}


'''
Query the brand info in BrandDB by names in the Namelist
NOTE：For dupulicated name, it gives dupulicated record 
Input NameList: [name1,name2,....]
Output format: [{name:name1,type:XX,...},{name:name2,type:XXX...},...]
'''
def QueryBrInfoByNameList(Namelist,BrandDB,NameIndex={}):
	InfoList = [] 
	if NameIndex == {}:
		NameIndex = IndexByName(BrandDB,'name')
	for name in Namelist:
		# print name
		info = QueryBrInfoByName(name,BrandDB,NameIndex)
		InfoList.append(info)
	return InfoList


'''
Insert Infromation into POI list
NOTE: PIDlist and Nameist should match
Output format: {PID:{name:...,cnname:...,enname:...,type:...,tag:[tag1,tag2,...]}}
'''
def InsertInfoInPOIList(PIDlist,Namelist,BrandDB):
	InfoList = QueryBrInfoByNameList(Namelist,BrandDB)
	POIDB = {}
	for pid,info in zip(PIDlist,InfoList):
		POIDB.update({pid:info})

	return POIDB


'''
write DB to data file
The order of the values is given by OutputOrder
Ex.  OutputOrder = ['name','phone','type','tag','story']
'''
def WriteDBtoDAT(DB,OutputOrder,DBFilePath):
	fp_db = open(DBFilePath,'w')
	if 'pid' in OutputOrder:
		OutputOrder.pop('pid')
	fp_db.write('\t'.join(['ID']+OutputOrder)+'\n')
	for keyid in DB:
		fp_db.write(keyid+'\t'+StrRecord(DB[keyid],'\t',OutputOrder)+'\n')
		
	fp_db.close()

def main():
	# Add Mall 1 into DB
	KeyList = ['pid','name','type','tag','phone','story']
	FilePath = '.\DataInMall\DangDaiShangCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath)
	FilePath = '.\DataInMall\HuaRunWuCaiCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	FilePath = '.\DataInMall\KaiDeMaoTaiYangGong.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	

	# data = ReadCSV(FilePath,KeyList)
	# print data[50]['name'],data[50]['tag'],data[50]['type']

	# Namelist = [record['name'] for record in data]
	# CnNameList,EnNameList = CNNamelistFilter(Namelist)
	# PIDlist = [record['pid'] for record in data]
	# Typelist = [record['type'] for record in data]
	# Taglist = [[record['tag']] for record in data]
	# Phonelist = [record['phone'] for record in data]
	# BrandDB = {}
	# BrandDB = UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist)
	# fp = open('.\TXT\output.txt','w')
	# print len(BrandDB)


	# Add Mall 2 into DB
	# FilePath = '.\DataInMall\HuaRunWuCaiCheng.csv'
	# KeyList = ['pid','name','type','tag','phone']
	# data = ReadCSV(FilePath,KeyList)
	# print data[50]['name'],data[50]['tag'],data[50]['type']

	# Namelist = [record['name'] for record in data]
	# CnNameList,EnNameList = CNNamelistFilter(Namelist)
	# PIDlist = [record['pid'] for record in data]
	# Typelist = [record['type'] for record in data]
	# Taglist = [[record['tag']] for record in data]
	# Phonelist = [record['phone'] for record in data]
	# BrandDB = UpdateBrandDBbyPOIlist(BrandDB,PIDlist,Namelist,CnNameList,EnNameList,Typelist,Taglist)

	# print len(BrandDB)
	# for key in BrandDB:
	# 	fp.write(key+'\t'+str(BrandDB[key]['name']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['cnname']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['enname']).encode('utf8')+
	# 		'\t'+str(BrandDB[key]['type']).encode('utf8')+
	# 		'\t'+StrTag(BrandDB[key]['tag'],'\t').encode('utf8')+'\n')

	# # print QueryBrInfoByName('BUOUBVOV',BrandDB)
	# print QueryBrInfoByNameList(['姑姑宴','和合谷'],BrandDB)

	# FilePath = '.\TXT\ShuangAnShangChang_POI.txt'
	# KeyList = ['pid','name']
	# data = ReadCSV(FilePath,KeyList,'\t')
	# print data[50]['pid'],data[50]['name']
	# PIDlist = [record['pid'] for record in data]
	# Namelist = [record['name'] for record in data]

	# POIDB = InsertInfoInPOIList(PIDlist,Namelist,BrandDB)
	# fp_poi = open('.\TXT\POIDB.csv','w')
	OutputOrder = ['name','phone','type','tag','story']
	# fp_poi.write(','.join(['pid']+OutputOrder)+'\n')
	# for pid in POIDB:
	# 	fp_poi.write(pid+','+StrRecord(POIDB[pid],',',OutputOrder)+'\n')
	# fp_poi.close()
	# # fp.close()

	DBFilePath = '.\TXT\BrandDB.txt'
	WriteDBtoDAT(BrandDB,OutputOrder,DBFilePath)
	data = ReadDAT(DBFilePath,OutputOrder,'\t')
	# for record in data:
	# 	if record['pid'] == '191':
	# 		print StrRecord(record)
	# 		print record
	# 		fp_tmp = open('.\TXT\\tmp.txt','w')
	# 		fp_tmp.write(StrRecord(record))
	# 		fp_tmp.close()

	NewMallPath = '.\DataInMall\ShuangAn.txt'
	NewMallPath2 = '.\DataInMall\ShuangAn2.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,NewMallPath,BrandDB)
	NewMallData = ReadDAT(NewMallPath,KeyList)
	NewMallDB = Recodelist2DB(NewMallData,'pid')
	Namelist = IndexByName(BrandDB,'name')
	for pid in NewMallDB:
		info = QueryBrInfoByName(NewMallDB[pid]['name'],BrandDB,Namelist)
		NewMallDB.update({pid:info})
	WriteDBtoDAT(NewMallDB,OutputOrder,NewMallPath2)

	FilePath = '.\BrandE-CDict.csv'
	KeyList = ['enname','cnname']
	data = ReadCSV(FilePath,KeyList)
	EnNamelist = [record['enname'] for record in data]
	CnNamelist = [record['cnname'] for record in data]
	MatchN = 0
	for key in BrandDB:
		if BrandDB[key]['name'] in (EnNamelist + CnNamelist):
			MatchN += 1
	print MatchN, 'names are found.'


def main2():
	FilePath = '.\BrandE-CDict.csv'
	KeyList = ['enname','cnname']
	ECdata = ReadCSV(FilePath,KeyList)
	# print ECdata[2]

		# Add Mall 1 into DB
	KeyList = ['pid','name','type','tag','phone','story']
	FilePath = '.\DataInMall\DangDaiShangCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath)
	FilePath = '.\DataInMall\HuaRunWuCaiCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	FilePath = '.\DataInMall\KaiDeMaoTaiYangGong.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	FilePath = '.\XML\ShuangAn\ShuangAn2.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)

	DBFilePath = '.\TXT\BrandDB.txt'
	OutputOrder = ['name','cnname','enname','type']
	print BrandDB[3]
	WriteDBtoDAT(BrandDB,OutputOrder,DBFilePath)


if __name__ == '__main__':
	main2()
