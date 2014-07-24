# GotPOINameInMall
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
RootPath = 'E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\\'
MallName = 'ShuangAnShangChang'
SubPath = '\Binary\\'

fp_name = open('E:\POIClassify\\'+MallName+"_POI.txt",'w')

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

# FileName = 'E:\MDBGenerate\= MDB_Modify_BJ\= ModifiedOK\HuaRunWuCaiCheng\Binary\HuaRunWuCaiCheng.FloorF1.xml'
# FileLines = open(FileName,'r').readlines()
# FileText = ' '.join(FileLines)
# soup = BeautifulSoup(FileText)
# for shop in soup.floor.findAll(name = 'feature', attrs = {'type':'1','shape':'0'}):
# 	print str(shop['id'])