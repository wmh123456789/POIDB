# coding=utf-8
from bs4 import BeautifulSoup 
import os


def SoupFile(FilePath):
	FileLines = open(FilePath,'r').readlines()
	FileText = ' '.join(FileLines)
	return BeautifulSoup(FileText)

# Make a fake miao file for test
def FakeMiao(cnname,FloorList,CityCode,MallID,MallName,GPS):

	soup = BeautifulSoup()

	mall_tag = soup.new_tag('mall')
	mall_tag['cnname'] = cnname
	mall_tag['floorcount'] = str(len(FloorList))
	mall_tag['id'] = CityCode + MallID
	mall_tag['name'] = MallName
	soup.append(mall_tag)

	for fid,floorname in  enumerate(FloorList):
		floor_tag = soup.new_tag('floor')
		floor_tag['id'] = CityCode+MallID+str(10001+fid)[1:]
		floor_tag['string'] = floorname
		soup.mall.append(floor_tag)

	gps_tag = soup.new_tag('gps')
	gps_tag.string = GPS
	soup.mall.append(gps_tag)
	# soup.prettify()
	return soup

def MakeFakeMiaoFile(rootpath,cnname,FloorList,CityCode,MallID,MallName,GPS):
	fp = open(os.path.join(rootpath,MallName+'.miao.xml'),'w')
	soup = FakeMiao(cnname,FloorList,CityCode,MallID,MallName,GPS)
	fp.write(str(soup))
	fp.close()



# info = [
# ['8001', 'JianWaiSOHOA',  'JWSOHOA', u'建外SOHO A座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F']],
# ['8002', 'JianWaiSOHOB',  'JWSOHOB', u'建外SOHO B座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F']],
# ['8003', 'JianWaiSOHO1',  'JWSOHO1', u'建外SOHO 1座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8004', 'JianWaiSOHO2',  'JWSOHO2', u'建外SOHO 2座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8005', 'JianWaiSOHO3',  'JWSOHO3', u'建外SOHO 3座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8006', 'JianWaiSOHO4',  'JWSOHO4', u'建外SOHO 4座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8007', 'JianWaiSOHO5',  'JWSOHO5', u'建外SOHO 5座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8008', 'JianWaiSOHO6',  'JWSOHO6', u'建外SOHO 6座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8009', 'JianWaiSOHO7',  'JWSOHO7', u'建外SOHO 7座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8010', 'JianWaiSOHO8',  'JWSOHO8', u'建外SOHO 8座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8011', 'JianWaiSOHO9',  'JWSOHO9', u'建外SOHO 9座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8012', 'JianWaiSOHO10', 'JWSOHO10', u'建外SOHO 10座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8013', 'JianWaiSOHO11', 'JWSOHO11', u'建外SOHO 11座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8014', 'JianWaiSOHO12', 'JWSOHO12', u'建外SOHO 12座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8015', 'JianWaiSOHO13', 'JWSOHO13', u'建外SOHO 13座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8016', 'JianWaiSOHO14', 'JWSOHO14', u'建外SOHO 14座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8017', 'JianWaiSOHO15', 'JWSOHO15', u'建外SOHO 15座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8018', 'JianWaiSOHO16', 'JWSOHO16', u'建外SOHO 16座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8019', 'JianWaiSOHO17', 'JWSOHO17', u'建外SOHO 17座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8020', 'JianWaiSOHO18', 'JWSOHO18', u'建外SOHO 18座', ['B1','1F','2F','3F','4F','5F','6F','7F','8F','9F','10F','11F','12F','13F','14F','15F','16F','17F','18F','19F','20F','21F','22F','23F','24F','25F','26F','27F','28F','29F','30F','31F','32F','33F','34F','35F','36F']],
# ['8021', 'WangJingSOHO1',  'WJSOHO1', u'望京SOHO 1座', ['B1','1F','2F','3F','4F','5F','6F']],
# ['8022', 'WangJingSOHO2',  'WJSOHO2', u'望京SOHO 2座', ['B1','1F','2F','3F','4F','5F','6F']],
# ['8023', 'WangJingSOHO3',  'WJSOHO3', u'望京SOHO 3座', ['B1','1F','2F','3F','4F','5F','6F']]
 # ]

info = [
['8024', 'ChaoWaiSOHOA', 'CWSOHOA', u'朝外SOHO A座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F', '13F', '14F', '15F', '16F', '17F', '18F', '19F', '20F', '21F', '22F', '23F', '24F', '25F', '26F', '27F', '28F', '29F']],
['8025', 'ChaoWaiSOHOB', 'CWSOHOB', u'朝外SOHO B座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F']],
['8026', 'ChaoWaiSOHOC', 'CWSOHOC', u'朝外SOHO C座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F']],
['8027', 'ChaoWaiSOHOD', 'CWSOHOD', u'朝外SOHO D座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F']],
['8028', 'YinHeSOHOA', 'YHSOHOA', u'银河SOHO A座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F', '13F', '14F', '15F', '16F', '17F']],
['8029', 'YinHeSOHOB', 'YHSOHOB', u'银河SOHO B座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F', '13F', '14F', '15F', '16F', '17F']],
['8030', 'YinHeSOHOC', 'YHSOHOC', u'银河SOHO C座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F', '13F', '14F', '15F', '16F', '17F']],
['8031', 'YinHeSOHOD', 'YHSOHOD', u'银河SOHO D座', ['B1', '1F', '2F', '3F', '4F', '5F', '6F', '7F', '8F', '9F', '10F', '11F', '12F', '13F', '14F', '15F', '16F', '17F']]

]




def main():
	# MallID = '8002'
	# MallName = 'JianWaiSOHOB'
	# cnname = u'建外SOHO B座'
	GPS = '116.310719655,39.9792287782'
	CityCode = '1010'

	# # FloorList = ['1F','2F','3F']
	# FloorList = ['B1',
	# 	    	'1F', '2F', '3F', '4F', '5F', '6F' ,'7F', '8F', '9F', '10F',
	# 	    	'11F','12F','13F','14F','15F','16F','17F','18F','19F','20F',
	# 	    	'21F','22F','23F','24F','25F','26F','27F','28F','29F','30F',
	# 	    	'31F','32F'
	# 	    	# ,'33F','34F','35F','36F'
	# 	     ] # To del a mall, make '' in the list
	
	for line in info:
		MallID = line[0]
		MallName = line[1]
		cnname = line[3]
		FloorList = line[4]
		# FakeMiao(cnname,FloorList,CityCode,MallID,MallName,GPS)
		rootpath = r'E:\Data\WiSLAM\fakemiao'
		MakeFakeMiaoFile(rootpath,cnname,FloorList,CityCode,MallID,MallName,GPS)


if __name__ == '__main__':
	main()