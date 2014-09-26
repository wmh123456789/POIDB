#Edit Miao xml file
import os
import XMLEditorLib as XE
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element  
from bs4 import BeautifulSoup,Tag

def SoupFile(FilePath):
	FileLines = open(FilePath,'r').readlines()
	FileText = ' '.join(FileLines)
	return BeautifulSoup(FileText)

def name2cnname(name):
	return name
	pass

def GetNoSpaceMallNameDict(dictfile):
	SpaceMark = ',' # for csv file
	NameDict = {}
	for line in open(dictfile).readlines():
		words = [word.strip() for word in line.split(SpaceMark)]
		if len(words) >= 2:
			NameDict.update({words[0]:words[1]})

	return NameDict

def updategpscsv(gpsfile,NoSpaceMallNameDict):
	fp = open('NewGPSBJ.csv','w')
	for line in open(gpsfile).readlines():
		words = [word.strip() for word in line.split(',')]
		if len(words) > 0:
			if words[0] in NoSpaceMallNameDict:
				name = NoSpaceMallNameDict[words[0]]
			else:
				name = words[0]
			gps = ['-1','-1']
			if len(words) >= 3 :
				gps = [words[1],words[2]]
			fp.write(name+','+gps[0]+','+gps[1]+'\n')
	fp.close()



def GetGPSDict(gpsfile,NoSpaceMallNameDict):
	
	SpaceMark = ',' # for csv file
	GPSDict = {}
	for line in open(gpsfile).readlines():
		words = [word.strip() for word in line.split(SpaceMark)]
		if len(words) >= 3 :
			GPSDict.update({words[0]:[words[1],words[2]]})
	return GPSDict

def UpdateMalltoMiao(soup,GPSDict):
	name = soup.mall['name']
	soup.mall['cnname'] = name2cnname(name)
	GPSText = 'none'
	if name in GPSDict:
		GPSText = str(GPSDict[name][0])+','+str(GPSDict[name][1])
	else:
		print name
	if soup.mall.gps.string:
		soup.mall.gps.string.replaceWith(GPSText)
	else:
		soup.mall.gps.string = GPSText
	return soup


def main():
	xmlpath = 'D:\WiSLAM\miao'
	# outpath = 'D:\WiSLAM\miao\MSRA.test.xml'
	GPSpath = 'E:\= Workspaces\Python Space\Modify_XML\NewGPSBJ.csv'
	NameDictFile = 'E:\= Workspaces\Python Space\Modify_XML\NoSpaceMallNameDict.csv'
	
	NoSpaceMallNameDict = GetNoSpaceMallNameDict(NameDictFile)

	GPSDict = GetGPSDict(GPSpath,NoSpaceMallNameDict)
	for afile in os.listdir(xmlpath):
		if '.mall.xml' in afile:
			mallname = afile.split('.')[0]
			soup = SoupFile(os.path.join(xmlpath,afile))
			soup = UpdateMalltoMiao(soup,GPSDict)
			# output the new miao xml
			outpath = os.path.join(xmlpath,mallname+'.miao.xml')
			fp = open(outpath,'w')
			fp.write(str(soup))
			fp.close()
	


if __name__ == "__main__":
	main()