# coding=utf-8
#Edit Miao xml file
# input is bd09 GPS system

import os
import XMLEditorLib as XE
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element  
from bs4 import BeautifulSoup,Tag
from CoordUtil import *

def SoupFile(FilePath):
	FileLines = open(FilePath,'r').readlines()
	FileText = ' '.join(FileLines)
	return BeautifulSoup(FileText)

def Name2CNName(name,PinyinDict):
	cnname = u''
	name = name.lower()

	unknownword = []
	for c in ['(',')','dian','mall']:
		name = name.replace(c,'')
	for word in name.split():
		if word.lower() in PinyinDict:
			cnname += PinyinDict[word.lower()].decode().encode('utf8')
		else:
			unknownword.append(word)
			cnname += word.decode().encode('utf8')
	# print cnname
	for w in list(set(unknownword)):
		# print w
		pass
	return cnname


def GetKVDict(dictfile,NameDict = {}):
	SpaceMark = ',' # for csv file
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

def GetPinyinDict(pinyindir):
	PinyinDict = {}
	for afile in os.listdir(pinyindir):
		PinyinDict = GetKVDict(os.path.join(pinyindir,afile),PinyinDict)
	return PinyinDict

# GPS Dict : {MallName:[lat,lng]}
def GetGPSDict(gpsfile):	
	SpaceMark = ',' # for csv file
	GPSDict = {}
	for line in open(gpsfile).readlines():
		words = [word.strip() for word in line.split(SpaceMark)]
		if len(words) >= 3 :
			GPSDict.update({words[0]:[words[1],words[2]]})
	ConvertGPSDict(GPSDict)  # Convert Baidu GPS to GCJ GPS
	return GPSDict

# Convert Baidu GPS to GCJ GPS
def ConvertGPSDict(GPSDict):
	for key in GPSDict:
		lat = float(GPSDict[key][0])
		lng = float(GPSDict[key][1])
		glat,glng = bd09_to_gcj02(lat,lng)
		GPSDict.update({key:[str(glat),str(glng)]})




def UpdateMalltoMiao(soup,GPSDict,PinyinDict):
	name = soup.mall['name']
	soup.mall['cnname'] = Name2CNName(name,PinyinDict)
	GPSText = 'none'
	if name in GPSDict:
		GPSText = str(GPSDict[name][0])+','+str(GPSDict[name][1])
		if soup.mall.gps.string:
			soup.mall.gps.string.replaceWith(GPSText)
		else:
			soup.mall.gps.string = GPSText
	else:
		print 'Cannot find the GPS of: ',name
	
	return soup

def UpdateMiaoForMalls(XMLPath,GPSFile,PinyinDict):
	GPSDict = GetGPSDict(GPSFile)
	for afile in os.listdir(XMLPath):
		if '.mall.xml' in afile:
			mallname = afile.split('.')[0]
			if mallname in GPSDict:
				soup = SoupFile(os.path.join(XMLPath,afile))
				soup = UpdateMalltoMiao(soup,GPSDict,PinyinDict)
				# output the new miao xml
				outpath = os.path.join(XMLPath,mallname+'.miao.xml')
				fp = open(outpath,'w')
				fp.write(str(soup).encode('utf8'))
				fp.close()

def main():
	xmlpath = 'D:\WiSLAM\miao\mall'
	GPSpath = 'NewGPSSH.csv'
	pinyindir = u'..\Pinyin2Hanzi'
	KeyWordDict = {'beijing':u'北京',
					'mall':u'mall',
					'dian':u'店',
					'shangcheng':u'商城',
					'shangchang':u'商场',
					'gouwuzhongxin':u'购物中心',
					'guangchang':u'广场'}

	# PinyinFile = u'..\Pinyin2Hanzi\BJ.txt'
	# PinyinFileList = [u'..\Pinyin2Hanzi\BJ.txt',
	# 					u'..\Pinyin2Hanzi\BJ2.txt',
	# 					u'..\Pinyin2Hanzi\BJ3.txt',
	# 					u'..\Pinyin2Hanzi\BJ4.txt']

	# PinyinDict = {}
	# for PinyinFile in PinyinFileList:
	# 	PinyinDict = GetKVDict(PinyinFile,PinyinDict)

	# NameDictFile = 'NoSpaceMallNameDict.csv'
	# NoSpaceMallNameDict = GetNoSpaceMallNameDict(NameDictFile)
	
	PinyinDict = GetPinyinDict(pinyindir)	

	UpdateMiaoForMalls(xmlpath,GPSpath,PinyinDict)



if __name__ == "__main__":
	main()