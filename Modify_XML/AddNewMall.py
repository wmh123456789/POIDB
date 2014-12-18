# coding=utf-8
# To Add new mall into DD's DB
import XMLEditorLib as XE
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element  

# Config the basic Information of the mall
MallID = '7995'
MallInfo = {'ShortNM':'KK',
				 'PY':'Kuike',
				'CHN':u'奎科大厦'}
# FloorList = ['B2S','B2N','B1S','B1N','L1S','L1N','L2S','L2N','L3','L4']
FloorList = ['F4','F5'] # To del a mall, make '' in the list

filePathSpace = 'E:\MDBGenerate\mappy\space\\010\\'+MallID+'.xml'
filePathMalls = 'E:\MDBGenerate\mappy\malls\\0101.xml'
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