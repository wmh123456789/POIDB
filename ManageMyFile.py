# coding=utf-8
import os
import shutil
from bs4 import BeautifulSoup 

def listFiles(dir):
	return [f for f in os.listdir(dir) if (f != ".DS_Store" and f != "ManageMyFile.py")]

def NewInnerFolder(NewName):
	for FolderName in listFiles("./"):
		os.mkdir("./"+FolderName+"/"+NewName)
	pass


def PickFile(SourceDir,SubDir,TargetDir):
	for BldName in os.listdir(SourceDir):
		if not os.path.isdir(os.path.join(TargetDir,BldName)):
			os.mkdir(os.path.join(TargetDir,BldName))
		if not os.path.isdir(os.path.join(TargetDir,BldName,SubDir)):
			os.mkdir(os.path.join(TargetDir,BldName,SubDir))
		for FileName in os.listdir(os.path.join(SourceDir,BldName,SubDir)):
			if not os.path.isdir(os.path.join(SourceDir,BldName,SubDir,FileName)):
				shutil.copy(os.path.join(SourceDir,BldName,SubDir,FileName),os.path.join(TargetDir,BldName,SubDir))
	pass

def PickFileToAssign(SourceDir,SubDir,TargetDir):
	for BldName in os.listdir(SourceDir):
		if os.path.isdir(os.path.join(SourceDir,BldName,"ScanFile")):
			if not os.path.isdir(os.path.join(TargetDir,BldName)):
				os.mkdir(os.path.join(TargetDir,BldName))
			for FileName in  os.listdir(os.path.join(SourceDir,BldName,SubDir)):
				if not os.path.isdir(os.path.join(TargetDir,BldName,SubDir)):
					os.mkdir(os.path.join(TargetDir,BldName,SubDir))
				extName = os.path.splitext(FileName)[1][1:]
				if extName == "jpg" or extName == "JPG" :
					shutil.copy(os.path.join(SourceDir,BldName,SubDir,FileName),os.path.join(TargetDir,BldName,SubDir))
	pass

def PickImgFile(SourceDir,TargetDir):
	for BldName in os.listdir(SourceDir):
		if not os.path.isdir(os.path.join(TargetDir,BldName)):
			os.mkdir(os.path.join(TargetDir,BldName))
		os.mkdir(os.path.join(TargetDir,BldName,"ScanFile"))
		for SubDir in listFiles(os.path.join(SourceDir,BldName)):
			if os.path.isdir(os.path.join(SourceDir,BldName,SubDir)):
				for FileName in listFiles(os.path.join(SourceDir,BldName,SubDir)):
					if not os.path.isdir(os.path.join(SourceDir,BldName,SubDir,FileName)): 
						extName = os.path.splitext(FileName)[1][1:]
						if extName == "jpg" or extName == "png" :
							shutil.copy(os.path.join(SourceDir,BldName,SubDir,FileName),os.path.join(TargetDir,BldName,"ScanFile"))

	pass

def PickWiFiFile(SourceDir,TargetDir):
	for  BldName in os.listdir(SourceDir):
		if not os.path.isdir(os.path.join(TargetDir,BldName)):
			os.mkdir(os.path.join(TargetDir,BldName))
		if BldName[0]!= '=' and os.path.isdir(os.path.join(SourceDir,BldName)):
			for Floor in listFiles(os.path.join(SourceDir,BldName)):
				if os.path.isdir(os.path.join(SourceDir,BldName,Floor)):
					pass
					# WiFiFile = os.path.join(SourceDir,BldName,Floor,'data.wifi')
					# if os.path.isfile(WiFiFile):
					# 	shutil.copy(WiFiFile,os.path.join(TargetDir,BldName,Floor+'.wifi'))
				elif os.path.splitext(Floor)[1] == '.params':
					print Floor
					shutil.copy(os.path.join(SourceDir,BldName,Floor)
						,os.path.join(TargetDir,BldName))




def PickXMLFile(SourceDir,SubDir,TargetDir):
	for BldName in os.listdir(SourceDir):
		if not os.path.isdir(os.path.join(TargetDir,BldName)):
			os.mkdir(os.path.join(TargetDir,BldName))
		if BldName[0]!= '=' and os.path.isdir(os.path.join(SourceDir,BldName,SubDir)):
			for FileName in listFiles(os.path.join(SourceDir,BldName,SubDir)):
				if not os.path.isdir(os.path.join(SourceDir,BldName,SubDir,FileName)): 
					extName = os.path.splitext(FileName)[1]
					bodyName = os.path.splitext(FileName)[0]
					if extName == ".xml": 
						if bodyName[0] == "1" :
							shutil.copy(os.path.join(SourceDir,BldName,SubDir,FileName),os.path.join(TargetDir,BldName))
						elif '.mall' in bodyName:
							print bodyName
							shutil.copy(os.path.join(SourceDir,BldName,SubDir,FileName),os.path.join(TargetDir,BldName))
	pass

def NewScanFolders(SourceDir):
	for BldName in os.listdir(SourceDir):
		if os.path.isdir(os.path.join(SourceDir,BldName)):
			for FileName in listFiles(os.path.join(SourceDir,BldName)):
				extName = os.path.splitext(FileName)[1][1:]
				if extName == "jpg" or  extName == "JPG" or extName == "png" or extName == "PNG":
					if not os.path.isdir(os.path.join(SourceDir,BldName,"ScanFile")):
						os.mkdir(os.path.join(SourceDir,BldName,"ScanFile"))
					shutil.move(os.path.join(SourceDir,BldName,FileName),os.path.join(SourceDir,BldName,"ScanFile"))



def CopyBiMap (SourceDir,TargetDir):
	for FileName in listFiles(SourceDir):
		if os.path.splitext(FileName)[1][1:] == "params":
			shutil.copy(os.path.join(SourceDir,FileName),TargetDir)

	SourceDir = os.path.join(SourceDir,"routed")
	for MapName in listFiles(SourceDir):
		bodyName = os.path.splitext(MapName)[0]
		if bodyName.split("_")[0] == "ExtPath" and bodyName.split("_")[1] != "ExtPath":
			if os.path.isdir(os.path.join(TargetDir,bodyName.split("_")[3])):
				shutil.copy(os.path.join(SourceDir,MapName),os.path.join(TargetDir,bodyName.split("_")[3]))


def GetBIDFromXML(FilePath):
	data = open(FilePath).read()
	soup = BeautifulSoup(data)
	bid = soup.mall['id']
	return str(bid)

def BName2BID(RootDir):
	for BldName in os.listdir(RootDir):
		if os.path.isdir(os.path.join(RootDir,BldName)):
			XMLFile = os.path.join(RootDir,BldName,BldName+'.mall.xml')
			if os.path.isfile(XMLFile):
				Bid = GetBIDFromXML(XMLFile)
				os.rename(os.path.join(RootDir,BldName),os.path.join(RootDir,Bid))
	pass



# SourceDir = "E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\XiDanDaYueCheng\Binary"
# TargetDir = u"D:\WiSLAM\WiSLAMOK\XiDanDaYueCheng"
# CopyBiMap(SourceDir,TargetDir)

# SourceDir = "E:\= AllDataSet\= Malls Info in ShangHai"
# NewScanFolders(SourceDir)

# SourceDir = "E:\= AllDataSet\= Malls Info in ShangHai"
# SubDir = "ScanFile"
# TargetDir = "E:\MDBGenerate\MDB_Modify_SH\ToAssign"
# PickFileToAssign(SourceDir,SubDir,TargetDir)

# SourceDir = "E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK"
# SubDir = "Binary"
TargetDir = u"D:\map_xml"
# PickXMLFile(SourceDir,SubDir,TargetDir)

# SourceDir = "D:\WiSLAM\WiSLAMOK"
# TargetDir = "D:\WiSLAM\WiFiFilesOnly"
# PickWiFiFile(SourceDir,TargetDir)

BName2BID(TargetDir)