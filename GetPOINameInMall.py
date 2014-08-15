# GotPOINameInMall
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def OutPutShopNames(RootPath,MallNameList,SubPath,OutputPath):
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
					FileLines = open(FileName,'r').readlines()
					FileText = ' '.join(FileLines)
					soup = BeautifulSoup(FileText)
					for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
						fp_name.write(str(shop['id'])+'\t'+str(shop['name']+'\n'))
			fp_name.close()

if __name__ == '__main__':
	RootPath = 'D:\\'
	MallNameList = ['AiQinHaiGouWuZhongXin']
	SubPath = '\Binary\\'
	OutputPath = 'D:\AiQinHaiGouWuZhongXin\\'
	OutPutShopNames(RootPath,MallNameList,SubPath,OutputPath)






# FileName = 'E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\HuaRunWuCaiCheng\Binary\HuaRunWuCaiCheng.FloorF1.xml'
# FileLines = open(FileName,'r').readlines()
# FileText = ' '.join(FileLines)
# soup = BeautifulSoup(FileText)
# for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
# 	print str(shop['id'])