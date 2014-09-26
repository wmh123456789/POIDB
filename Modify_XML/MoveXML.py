# move xml
import os
import shutil

RootDir = 'C:\Users\XiaoMing-OfficePC\Desktop\AllXML'
for xmlfile in os.listdir(RootDir):
	if not os.path.isdir(os.path.join(RootDir,xmlfile)): 
		MallName = xmlfile.split('.')[0]
		MallDir = os.path.join(RootDir,MallName)
		print MallName
		if not os.path.isdir(MallDir):
			os.mkdir(MallDir)
		shutil.move(os.path.join(RootDir,xmlfile),MallDir)
