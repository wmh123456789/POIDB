# Get POI Info in XML
# -*- coding: utf-8 -*-
from XY2GPS import *
from DBUtility import *
import scipy as sp
from scipy import array, dot, insert, linalg
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Load the Anchors for the Mall
def GetGPSParam(MallName,ParamFile):
	fp = open(ParamFile,'r')
	AnchorXY = []
	AnchorGPS = []
	for line in fp.readlines():
		if line.split(',')[0] == MallName:
			print line
			ParamText = line.strip().split(',')[1:]
			Error = float(ParamText.pop(0))
			print ParamText

			while not(len(ParamText)==0 or ParamText[0] == '\n' or ParamText[0] == ''):
			# while len(ParamText) >0:
				AnchorGPS.append([float(ParamText.pop(0)),float(ParamText.pop(0))])
				AnchorXY.append([float(ParamText.pop(0)),float(ParamText.pop(0))])
				# print '3',ParamText
						
	A,X0,K = [[-1],[-1],[-1]]
	if len(AnchorGPS) == 2:
		A,X0,K = CalcXY2GPSParam_2p(AnchorXY[0],AnchorXY[1],AnchorGPS[0],AnchorGPS[1])
	elif len(AnchorGPS) == 3:
		A,X0,K = CalcXY2GPSParam_3p(AnchorXY[0],AnchorXY[1],AnchorXY[2],AnchorGPS[0],AnchorGPS[1],AnchorGPS[2])
	elif len(AnchorGPS) == 0:
		print 'No Anchor Point!'
	else:
		print 'Anchor Points Error:', AnchorGPS
		

	fp.close()
	return A,X0,K
	

# Calc GPS by X,Y in Mall 
def XY2GPSinMall(x,y,A,X0,K):
	 
	return x,y


def SoupFile(FilePath):
	FileLines = open(FilePath,'r').readlines()
	FileText = ' '.join(FileLines)
	return BeautifulSoup(FileText)
	
# Output ID, Name for each POI in each Mall
def OutputShopNames(RootPath,MallNameList,SubPath,OutputPath):
	# Check mall list
	if '' in MallNameList:
		MallNameList = [MallName for  MallName in os.listdir(RootPath) 
						if os.path.isdir(os.path.join(RootPath,MallName))]

	#Check output path
	if not os.path.isdir(OutputPath):
		os.mkdir(OutputPath)

	#Loop over malls
	for MallName in MallNameList:
		print MallName
		if os.path.isdir(RootPath+MallName+SubPath):
			fp_name = open(os.path.join(OutputPath,MallName+"_POIList.txt"),'w')
			for FileName in os.listdir(RootPath+MallName+SubPath):
				extName = os.path.splitext(FileName)[1][1:]
				ext2Name = os.path.splitext(FileName)[0].split(".")[-1]
				if extName == 'xml' and ext2Name != 'mall':
					FileName = RootPath+MallName+SubPath+FileName
					soup = SoupFile(FileName)
					for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
						fp_name.write(str(shop['id'])+'\t'+str(shop['name']+'\n'))
			fp_name.close()

# Output ID, Name, X,Y for each POI in each Mall
def OutputShopXY(RootPath,MallNameList,SubPath,OutputPath):
	# Check mall list
	if '' in MallNameList:
		MallNameList = [MallName for  MallName in os.listdir(RootPath) 
						if os.path.isdir(os.path.join(RootPath,MallName))]

	#Check output path
	if not os.path.isdir(OutputPath):
		os.mkdir(OutputPath)

	#Loop over malls
	for MallName in MallNameList:
		print MallName
		if os.path.isdir(RootPath+MallName+SubPath):
			fp_name = open(os.path.join(OutputPath,MallName+"_POIXY.txt"),'w')
			for FileName in os.listdir(RootPath+MallName+SubPath):
				extName = os.path.splitext(FileName)[1][1:]
				ext2Name = os.path.splitext(FileName)[0].split(".")[-1]
				if extName == 'xml' and ext2Name != 'mall':
					FileName = RootPath+MallName+SubPath+FileName
					soup = SoupFile(FileName)
					for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
						fp_name.write(str(shop['id'])+'\t'+str(shop['name'])+
							'\tX='+str(shop.center['x'])+
							'\tY='+str(shop.center['y'])+'\n')
			fp_name.close()
	pass


# Output ID, Name, Lng,Lat for each POI in each Mall
def OutputShopGPS(RootPath,MallNameList,SubPath,OutputPath,ParamFile):
	# Check mall list
	if '' in MallNameList:
		MallNameList = [MallName for  MallName in os.listdir(RootPath) 
						if os.path.isdir(os.path.join(RootPath,MallName))]

	#Check output path
	if not os.path.isdir(OutputPath):
		os.mkdir(OutputPath)

	#Loop over malls
	for MallName in MallNameList:
		print MallName
		A,X0,K = GetGPSParam(MallName,ParamFile)
		if len(X0)==2 and os.path.isdir(RootPath+MallName+SubPath):
			fp_name = open(os.path.join(OutputPath,MallName+"_POIGPS.txt"),'w')
			for FileName in os.listdir(RootPath+MallName+SubPath):
				extName = os.path.splitext(FileName)[1][1:]
				ext2Name = os.path.splitext(FileName)[0].split(".")[-1]
				if extName == 'xml' and ext2Name != 'mall':
					FileName = RootPath+MallName+SubPath+FileName
					soup = SoupFile(FileName)
					for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
						# Calc GPS
						x = float(shop.center['x'])
						y = float(shop.center['y'])
						lng,lat = XY2GPS(A,X0,K,array([x,y]))

						# fp_name.write(str(shop['id'])+'\t'+str(shop['name'])+
						# 	'\tLng='+str(lng)+'\tLat='+str(lat)+
						# 	'\tX='+str(x)+'\tY='+str(y)+'\n')
						fp_name.write(str(shop['id'])+'#'+str(shop['name'])+
							'#Lng='+str(lng)+'#Lat='+str(lat)+
							'#X='+str(x)+'#Y='+str(y)+'\n')
			fp_name.close()
	pass
	pass

def ModifyTypeCodebyBrDB(BrandDB,TypeCodeDict,XMLInput,XMLOutput):
	soup = SoupFile(XMLInput)
	soup.prettify()
	Namelist = IndexByName(BrandDB,'name')
	CnNamelist = IndexByName(BrandDB,'cnname')
	EnNamelist = IndexByName(BrandDB,'enname')

	for i in xrange(len(soup.floor.contents)):
		for i in xrange(len(soup.floor.contents)):
 			if not soup.floor.contents[i] in ['\n']:
 				Name = soup.floor.contents[i]['name']
 				Type = 'null'
 				if Name in Namelist:
 					Type = QueryBrInfoByName(Name,BrandDB,Namelist)['type']
 				elif Name in CnNamelist:
 					Type = QueryBrInfoByName(Name,BrandDB,CnNamelist)['type']
 				elif Name in EnNamelist:
 					Type = QueryBrInfoByName(Name,BrandDB,EnNamelist)['type']
 				else:
 					print 'Cannot find the name:', Name
 				if Type == '':
 					TypeCode = '0'
 				else:
 					TypeCode = str(TypeCodeDict[Type])
 				soup.floor.contents[i]['type'] = TypeCode
 				pass

 	fp = open(XMLOutput,'w')
	fp.write(str(soup))
	fp.close()


def ModifyTypeCode(POIDBFile,POIDBKeyList,TypeCodeDict,XMLInput,XMLOutput):
	soup = SoupFile(XMLInput)
	data = ReadDAT(POIDBFile,POIDBKeyList)
	POIDB = Recodelist2DB(data,'pid')
	soup.prettify()
	for i in xrange(len(soup.floor.contents)):
 		if not soup.floor.contents[i] in ['\n']:
 			PID = soup.floor.contents[i]['id']
 			if PID in POIDB: 				
 				if PID == '':
 					POIType = '0'
 				elif not POIDB[PID]['type'].encode('utf8') in TypeCodeDict:
 					POIType = str(TypeCodeDict['其他'])
 				else:
 					POIType = str(TypeCodeDict[POIDB[PID]['type']])
 				pass
 			else: # PID is not in DB
 				POIType = '0'
 				pass
 			pass
 			# print POIType
 			soup.floor.contents[i]['type'] = POIType

	fp = open(XMLOutput,'w')
	fp.write(str(soup))
	fp.close()

def main():
	RootPath = 'E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\\'
	MallNameList = ['KaiDeMaoTaiYangGong','ShuangAnShangChang']
	SubPath = '\Binary\\'
	OutputPath = 'E:\POIClassify\POIListInMall\\'
	ParamFile = '.\GPSAnchorPointsBJ.csv'
	# # OutputShopNames(RootPath,MallNameList,SubPath,OutputPath)
	# # OutputShopXY(RootPath,MallNameList,SubPath,OutputPath)
	OutputShopGPS(RootPath,MallNameList,SubPath,OutputPath,ParamFile)



	# A,X,K = GetGPSParam('AiQinHaiGouWuZhongXin',ParamFile)
	# print A,X,K	
def test2():
	# Add Mall 1 into DB
	KeyList = ['pid','name','type','tag','phone','story']
	FilePath = '.\DataInMall\DangDaiShangCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath)
	FilePath = '.\DataInMall\HuaRunWuCaiCheng.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	FilePath = '.\DataInMall\KaiDeMaoTaiYangGong.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	FilePath = 'E:\= Workspaces\Git\POIDB\XML\ShuangAn\ShuangAn.txt'
	BrandDB = UpdateBrandDBbyPOIlistFile(KeyList,FilePath,BrandDB)
	TypeCode = {'服装':1,'餐饮':2,'电器':3,'体育':4,'儿童母婴':5,
				'店内娱乐':6,'超市':7,'个护化妆':8,'其他':9,'null':0}
	XMLFilePath = 'E:\= Workspaces\Git\POIDB\XML\ShuangAn'
	for FileName in os.listdir(XMLFilePath):
		extName = os.path.splitext(FileName)[1]
		bodyName = os.path.splitext(FileName)[0]
		if extName=='.xml' and not('NewTypeCode' in bodyName):
			InFilePath = os.path.join(XMLFilePath,FileName)
			if not os.path.isdir(os.path.join(XMLFilePath,'NewTypeCode')):
				os.mkdir(os.path.join(XMLFilePath,'NewTypeCode'))
			OutFilePath = os.path.join(XMLFilePath,'NewTypeCode',FileName)
			print FileName
			ModifyTypeCodebyBrDB(BrandDB,TypeCode,InFilePath,OutFilePath)


def test():
	DBFilePath = 'E:\= Workspaces\Git\POIDB\XML\ShuangAn\ShuangAn.txt'
	KeyList = ['pid','name','type','tag','phone','story']
	TypeCode = {'服装':1,'餐饮':2,'电器':3,'体育':4,'儿童母婴':5,
				'店内娱乐':6,'超市':7,'个护化妆':8,'其他':9,'null':0}
	# XMLFilePath = '.\XML\ShuangAnShangChang.FloorB1.xml'
	# OutFilePath = '.\XML\Result.xml'

	XMLFilePath = 'E:\= Workspaces\Git\POIDB\XML\ShuangAn'
	for FileName in os.listdir(XMLFilePath):
		extName = os.path.splitext(FileName)[1]
		bodyName = os.path.splitext(FileName)[0]
		if extName=='.xml' and not('NewTypeCode' in bodyName):
			InFilePath = os.path.join(XMLFilePath,FileName)
			if not os.path.isdir(os.path.join(XMLFilePath,'NewTypeCode')):
				os.mkdir(os.path.join(XMLFilePath,'NewTypeCode'))
			OutFilePath = os.path.join(XMLFilePath,'NewTypeCode',FileName)
			print FileName
			ModifyTypeCode(DBFilePath,KeyList,TypeCode,InFilePath,OutFilePath)

	# soup = SoupFile(XMLFilePath)
	# data = ReadDAT(InFilePath,KeyList)
	# POIDB = Recodelist2DB(data,'pid')
	# soup.prettify()
	# for i in xrange(len(soup.floor.contents)):
 # 		if not soup.floor.contents[i] in ['\n']:
 # 			PID = soup.floor.contents[i]['id']
 # 			if PID in POIDB:
 # 				POIType = str(TypeCode[POIDB[PID]['type'].encode('utf8')])
 # 				pass
 # 			else:
 # 				POIType = '0'
 # 				pass
 # 			pass
 # 			print POIType
 # 			soup.floor.contents[i]['type'] = POIType




	# fp = open(OutFilePath,'w')
	# fp.write(str(soup))
	# fp.close()

if __name__ == '__main__':
	# main()
	test2()

