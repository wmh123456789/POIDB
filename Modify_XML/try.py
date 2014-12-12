# print 'XinaAdafkj'.lower()
# print set(['1','1'])

# myfile = 'E:\= Workspaces\Git\POIDB\Pinyin2Hanzi\OurWords.csv'
# data = open(myfile).read()
# print data.decode('gbk')


def editdict(d):
	for key in d:
		d[key] += 2
	pass



d = {'a':1,'b':2}
editdict(d)
print d
a = '3.44'
print float(a)+1 