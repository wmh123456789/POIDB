# Get POI Info in XML
from XY2GPS import *
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
		if line.split('\t')[0] == MallName:
			ParamText = line.split('\t')[1:]
			# print ParamText
			while ParamText[0][0] == '[':
				AnchorGPS.append([float(a) for a in ParamText.pop(0).strip('[]').split(',')])
				AnchorXY.append([float(a) for a in ParamText.pop(0).strip('[]').split(',')])
				# print '3',ParamText
			Error = float(ParamText[0].strip())
			
	A,X0,K = [[-1],[-1],[-1]]
	if len(AnchorGPS) == 2:
		A,X0,K = CalcXY2GPSParam_2p(AnchorXY[0],AnchorXY[1],AnchorGPS[0],AnchorGPS[1])
	elif len(AnchorGPS) == 3:
		A,X0,K = CalcXY2GPSParam_3p(AnchorXY[0],AnchorXY[1],AnchorXY[2],AnchorGPS[0],AnchorGPS[1],AnchorGPS[2])
	elif len(AnchorGPS) == 0:
		print 'No Anchor Point!'
	else:
		print 'Anchor Points Error'
		

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

						fp_name.write(str(shop['id'])+'\t'+str(shop['name'])+
							'\tLng='+str(lng)+'\tLat='+str(lat)+'\n')
			fp_name.close()
	pass
	pass

if __name__ == '__main__':
	RootPath = 'E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\\'
	MallNameList = ['']
	SubPath = '\Binary\\'
	OutputPath = 'E:\POIClassify\POIListInMall\\'
	ParamFile = 'E:\= Workspaces\Python Space\GisLib\GPSErrorResultSets.txt'
	# # OutputShopNames(RootPath,MallNameList,SubPath,OutputPath)
	# # OutputShopXY(RootPath,MallNameList,SubPath,OutputPath)
	OutputShopGPS(RootPath,MallNameList,SubPath,OutputPath,ParamFile)


	# GetGPSParam('AiQinHaiGouWuZhongXin',ParamFile)
