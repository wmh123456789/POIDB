# Encode Utility. Dealwith char Encode problems

import codecs

'''
Auto detect the file encoding and transform it to UTF8 string 
'''
def ReadFileToUTF8(filepath):
	fp = open(filepath)
	data = fp.read()
	fp.close()
	newdata = 'Cannot transform this file~'
	if data[:2] == codecs.BOM_UTF16_LE:
		data = data[2:]
		newdata = data.decode('UTF-16LE').encode('utf-8')
	return newdata

'''
Auto detect the file encoding and transform it to UTF8 string, then write to new file
'''
def TransFileToUTF8(inputfile,outputfile):
	data = ReadFileToUTF8(inputfile)
	fp = open(outputfile,'w')
	fp.write(data)
	fp.close()

def main():
	inputfile = '.\TXT\unicode.txt'
	outputfile = '.\TXT\utf8.txt'
	TransFileToUTF8(inputfile,outputfile)
	
	
	
	lines = open(inputfile).read()
	print len(lines),repr(lines[:100])
	pass


if __name__ == '__main__':
	main()