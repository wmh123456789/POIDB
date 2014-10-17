import zipfile
import os
import io
import pymongo
import shutil
import ssh
import hashlib
import time
import datetime


global mdb,r,sftp,sshc

def zipFolder(folder,zipPath):
	zip = zipfile.ZipFile(zipPath+'.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(folder):
		for f in files:
			zip.write(os.path.join(root, f), os.path.join(root,f).replace(folder+os.sep, ''))
	zip.close()

def md5File(name):
	m = hashlib.md5()  
	file = io.FileIO(name,'r')  
	bytes = file.read(1024)  
	while(bytes != b''):  
		m.update(bytes)  
		bytes = file.read(1024)   
	file.close()  
	return m.hexdigest()  	

def validateZipFile(file):
	name = os.path.basename(file)
	if (name.endswith('.zip') and name.replace('.zip','').isdigit()):
		return True
	return False

def uploadZipFiles(root):
	st = time.time()
	remotePath = '/home/www/static/map/'
	flist = os.listdir(root)
	uploadCount = 0
	validCount = 0
	
	for f in flist:
		localFile = os.path.join(root,f)
		
		if not validateZipFile(localFile):
			continue
		validCount += 1
		fmd5 = md5File(localFile)
		_id = long(f.replace('.zip',''))
		
		res = mdb.find_one({'_id':_id})
		ver = datetime.datetime.now().strftime('%y%m%d%H')
		if res != None and res.has_key('md5') and res['md5'] == fmd5:
			#print 'FILE %s IGNORED' %(f)
			continue
		
		uploadFile(localFile, remotePath)
		mdb.update({'_id':_id},{'$set':{'md5':fmd5,'version':ver}},upsert=True)
		print 'FILE %s -> %s' %(f,remotePath)
		print 'MD5: %s\tDATE: %s' %(fmd5,ver)
		uploadCount += 1		
	ed = time.time()	
	
	print 'Finished Uploading on %s' %(root)
	print '%d files scanned, %d valid, %d uploaded' %(len(flist),validCount,uploadCount)
	print 'Time elapsed: %f' %((ed-st))
	print ''
	
def uploadFile(localFile, remotePath):
	if not remotePath.endswith('/'):
		remotePath = remotePath + '/'
	
	sftp.put(localFile, remotePath + os.path.basename(localFile))
	
def zipFiles(root, zipPath):
	st = time.time()
	zippedCount = 0
	if not os.path.exists(zipPath):
		os.makedirs(zipPath)
	flist = os.listdir(root)
	for f in flist:
		fpath = os.path.join(root,f)
		if os.path.isdir(fpath) and str.isdigit(f):
			zipFolder(fpath,os.path.join(zipPath,f))
			zippedCount += 1
	ed = time.time()
	print 'Finished Zipping from %s to %s' %(root,zipPath)
	print '%d files scanned, %d zipped' %(len(flist),zippedCount)
	print 'Time elapsed: %f' %((ed-st))
	print ''

def deletePath(path):
	shutil.rmtree(path)

def initEnv():
	global r,mdb
	global sshc,sftp
	r = pymongo.Connection(host='115.28.129.220')
	mdb = r.ika.map_xml
	#ftp = ftplib.FTP(host='114.215.154.80', user='root', passwd='nexd65535')
	sshc = ssh.SSHClient()
	sshc.set_missing_host_key_policy(ssh.AutoAddPolicy())
	sshc.connect(hostname='114.215.154.80',username='root',password='nexd65535')
	sftp = sshc.open_sftp()	
	
def destroyEnv():
	global r
	global sshc
	r.disconnect()
	sshc.close()
			
xml_path = 'D:\map_xml'
zip_path = os.path.join(xml_path,'tmp')

initEnv()
zipFiles(xml_path, zip_path)
uploadZipFiles(zip_path)
# deletePath(zip_path)

destroyEnv()