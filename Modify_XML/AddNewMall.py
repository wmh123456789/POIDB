# coding=utf-8
# To Add new mall into DD's DB
import XMLEditorLib as XE
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element  


# Config the basic Information of the mall
MallID = '8031'
MallInfo = {'ShortNM':'YHSOHOD',
				 'PY':'YinHeSOHOD',
				'CHN':u'银河SOHO D座'}
# FloorList = ['B2S','B2N','B1S','B1N','L1S','L1N','L2S','L2N','L3','L4']
FloorList = ['B1',
		     '1F', '2F', '3F', '4F', '5F', '6F' ,'7F', '8F', '9F', '10F',
		     '11F','12F','13F','14F','15F','16F','17F'
		     # ,'18F','19F','20F',
		     # '21F','22F','23F','24F','25F','26F','27F','28F','29F'
		     # , '30F',
		     # '31F','32F','33F','34F','35F','36F'
		     ] # To del a mall, make '' in the list

RootPath = 'E:\Personal\MinghuiWang\Git\mappy'
filePathSpace = RootPath+'\space\\010\\'+MallID+'.xml'
filePathMalls = RootPath+'\malls\\0101.xml'
filePathLog = 'NewBeijing.log'

# Creat a new XML file in Space
root = Element('space',{'h':'0','w':'0'})
tree = ElementTree(root)
FloorID = 0
for FloorName in FloorList:
	FloorID += 1
	floor = Element('floor',{'brief':FloorName,'cx':'0','cy':'0','id':str(FloorID),'nar':'0','nm':FloorName})
	root.append(floor)
if not '' in FloorList :
	tree.write(filePathSpace)

# Add New Line in XML file in Malls
tree = XE.read_xml(filePathMalls)
root = tree.getroot()
# Delete old info to update
XE.del_node_by_tagkeyvalue([root], "mall", {"id" : MallID})
# Insert new info
if not '' in FloorList :
	XE.insert_mall(root,MallID,MallInfo['ShortNM'],MallInfo['PY'],MallInfo['CHN'])
	tree.write(filePathMalls)

# Write a log file 
output = open(filePathLog,'a')
output.write(MallID+': ')
output.write(MallInfo['PY']+' '+MallInfo['ShortNM']+' '+MallInfo['CHN']+' --')
for f in FloorList:
	output.write(' '+f)
output.write('\n')
output.close()