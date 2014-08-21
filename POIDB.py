# Initialize the data (JD)
# -*- coding: utf-8 -*-
import os,re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def UpdateList(oldlist,newlist):
	for item in newlist:
		if not item in oldlist:
			oldlist.append(item)
	return oldlist

'''
Write the DB into a csv file 
input is the txt files
'''
def InitDB_JD(RootPath,CVSFileName):
	fp = open(os.path.join(RootPath,CVSFileName),'w')
	fp_tmp = open(os.path.join(RootPath,'tmp.txt'),'w')

	for tag1 in os.listdir(RootPath):
		if os.path.isdir(os.path.join(RootPath,tag1)) and tag1 != 'try':
			for tag2 in os.listdir(os.path.join(RootPath,tag1)):
				for tag3 in os.listdir(os.path.join(RootPath,tag1,tag2)):
					BrandFile = os.path.join(RootPath,tag1,tag2,tag3)
					for line in open(BrandFile).readlines():
						BrandName = line.split(u':')[0]
						Names = re.findall(u'(.*?)[(（](.*?)[)）]',BrandName)
						Tags = line.split(u':')[1]
						if len(Names) > 0:
							zhcn,encn = Names[0]
							fp_tmp.write(zhcn + ' , ' + encn+'\n')
							fp.write(BrandName+','+zhcn+','+encn+',')
						else:
							if re.findall(u'[\u4e00-\u9fa5]',BrandName):
								fp.write(BrandName+','+BrandName+','+'???'+',')
								#print re.findall('[\u4e00-\u9fa5]',BrandName)
							else:							
								fp.write(BrandName+','+'???'+','+BrandName+',')
						# Write the tags
						Tag_list = []
						for tag in Tags.split():
							if not tag in Tag_list:
								Tag_list.append(tag)
						for tag in Tag_list:
							fp.write(tag+',')
						fp.write('\n')
											
	fp_tmp.close()
	fp.close()

'''
Merge the repieted brand
'''
def CompactPOIDB(RootPath,CVSFileName):
	fp = open(os.path.join(RootPath,CVSFileName),'r')
	BrandDic = {}
	for line in fp.readlines():
		BrandName = line.split(',')[0]
		BrandTags = line.split(',')[3:-1]
		if BrandName in BrandDic:
			BrandDic.update({BrandName:UpdateList(BrandDic[BrandName],BrandTags)})
		else:
			BrandDic.update({BrandName:BrandTags})

	print len(BrandDic)
	fp_compact = open(os.path.join(RootPath,'JD_Compact.csv'),'w')
	for brand in BrandDic:
		fp_compact.write(brand+',')
		for tag in BrandDic[brand]:
			fp_compact.write(tag+',')
		fp_compact.write('\n')
	fp.close()
	fp_compact.close()


RootPath = 'E:\= Workspaces\Python Space\POICrwal\JD'
CVSFileName = 'JD.csv'
# InitDB_JD(RootPath,CVSFileName)
CompactPOIDB(RootPath,CVSFileName)







