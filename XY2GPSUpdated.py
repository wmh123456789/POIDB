import scipy as sp
from scipy import array, dot, insert, linalg
import os
import itertools
import shutil

def myArctan(x,y):
	alpha = sp.arctan(y/x)
	if x < 0:
		alpha += sp.pi
	elif y < 0:
		alpha += 2*sp.pi
	# print 'myArctan: ',x,y,alpha
	return alpha

# Let all rad in 0~2Pi
def CheckRad(alpha):
	while alpha<0:
		alpha += 2*sp.pi
	while alpha>=2*sp.pi:
		alpha -= 2*sp.pi
	return alpha


'''
	Assume X is XY coordinates, Y is GPS coordinates
	A is a rotation Matrix
	X0 is shift
	K is (dLng/dx, dlat/dy)
	Then Y = A*(X-X0).*K
'''
def XY2GPS(A,X0,K,x,g=[0,0]):
	y = dot(A,(x-X0))/K
	if g[0] == 0:
		return y
	else:
		return y, linalg.norm((y-g)*K)
	pass
def CalcXY2GPSParam_2p(x1,x2,g1,g2,K=[0,0]):
	# Kx = dLng/dx; Ky = dlat/dy;
	# In China:
	# Kx = (133.4-1.2*lat)*1e3
	# Ky = (110.2+0.002*lat)*1e3

	X1 = array(x1)
	Y1 = array(g1)
	X2 = array(x2)
	Y2 = array(g2)
	detX = X2-X1
	detY = Y2-Y1
	lat = Y1[1]
	if K[0] == 0:
		Kx = (133.4-1.2*lat)*1e3
		Ky = (110.2+0.002*lat)*1e3
		K = array([Kx,Ky])
	else:
		Kx = K[0]
		Ky = K[1]
	detKY = detY*K

	alpha =  myArctan(detX[0],detX[1]) - myArctan(detKY[0],detKY[1])
	A = array([[sp.cos(alpha),sp.sin(alpha)],[-sp.sin(alpha),sp.cos(alpha)]])
	X01 = X1 - dot(linalg.inv(A),Y1*K) 
	X02 = X2 - dot(linalg.inv(A),Y2*K)
	X0 = (X01+X02) /2

	return A,X0,K
def Average(A,X0,K,r1,p1,r2,p2,r3,p3,r4,p4,area=100):
	BS = 100
	total = 0
	average = 0
	rs1=list(XY2GPS(A, X0, K, r1, p1))
	rs2=list(XY2GPS(A, X0, K, r2, p2))
	rs3=list(XY2GPS(A, X0, K, r3, p3))
	rs4=list(XY2GPS(A, X0, K, r4, p4))
	
	if (rs1[1] < area)&(rs2[1] < area)&(rs3[1] < area)&(rs4[1] < area) :
		average = (rs1[1]+rs2[1]+rs3[1]+rs4[1])/4
		return average
	else :
		return -1
	
        

def CalcXY2GPSParam_3p(x1,x2,x3,g1,g2,g3,K=[0,0]):
	# Kx = dLng/dx; Ky = dlat/dy;
	# In China:
	# Kx = (133.4-1.2*lat)*1e3
	# Ky = (110.2+0.002*lat)*1e3

	X1 = array(x1)
	Y1 = array(g1)
	X2 = array(x2)
	Y2 = array(g2)
	X3 = array(x3)
	Y3 = array(g3)
	detX1, detX2, detX3 = (X2-X1, X3-X2, X1-X3)
	detY1, detY2, detY3 = (Y2-Y1, Y3-Y2, Y1-Y3)

	# Calc K
	lat = Y1[1]
	if K[0] == 0:
		Kx = (133.4-1.2*lat)*1e3
		Ky = (110.2+0.002*lat)*1e3
		K = array([Kx,Ky])
	else:
		Kx = K[0]
		Ky = K[1]

	# Calc A
	detKY1, detKY2, detKY3 = (detY1, detY2, detY3)*K
	alpha1 =  myArctan(detX1[0],detX1[1]) - myArctan(detKY1[0],detKY1[1])
	alpha2 =  myArctan(detX2[0],detX2[1]) - myArctan(detKY2[0],detKY2[1])
	alpha3 =  myArctan(detX3[0],detX3[1]) - myArctan(detKY3[0],detKY3[1])
	alpha1,alpha2,alpha3 = [CheckRad(a) for a in [alpha1,alpha2,alpha3] ]
	alpha = (alpha1+alpha2+alpha3)/3
	A = array([[sp.cos(alpha),sp.sin(alpha)],[-sp.sin(alpha),sp.cos(alpha)]])
	
	# Calc X0
	X01 = X1 - dot(linalg.inv(A),Y1*K) 
	X02 = X2 - dot(linalg.inv(A),Y2*K)
	X03 = X3 - dot(linalg.inv(A),Y3*K)
	X0 = (X01+X02+X03) /3
	return A,X0,K
	pass

if __name__ == "__main__":	
	
	fp = open('BadGPS.txt','r')
	#resultsetfile = open('ErrorResult.csv','w')
	# pN are the gps coordinates
while 1:
	line = file.readlines(fp)
	if not line:
		break
	for subline in line:
		subline = subline.split('/')
		lines = []
		lineForGps = []
		listForGpsCombin = []
		lineForIndoor = []
		listForIndoorCombin = []
		lines.append(subline)
		name = str(lines[0][0])
		
		#GPSCombination
		for i in range(1,5):
			lineForGps.append(lines[0][i])
		lineForGps = [[i] for i in lineForGps]
		for k in range(1,len(lineForGps)+1):
			iter = itertools.combinations(lineForGps,k)
			listForGpsCombin.append(list(iter))
			
		#IndoorCombination
		for i in range(5,9):
			lineForIndoor.append(lines[0][i])
		lineForIndoor = [[i] for i in lineForIndoor]
		for k in range(1,len(lineForIndoor)+1):
			iter = itertools.combinations(lineForIndoor,k)
			listForIndoorCombin.append(list(iter))	

		#TheVauleOfPoint
		m1 =  [float(listForGpsCombin[3][0][0][0].split(',')[0]),float(listForGpsCombin[3][0][0][0].split(',')[1])]
		m2 =  [float(listForGpsCombin[3][0][1][0].split(',')[0]),float(listForGpsCombin[3][0][1][0].split(',')[1])]
		m3 =  [float(listForGpsCombin[3][0][2][0].split(',')[0]),float(listForGpsCombin[3][0][2][0].split(',')[1])]
		m4 =  [float(listForGpsCombin[3][0][3][0].split(',')[0]),float(listForGpsCombin[3][0][3][0].split(',')[1])]
		n1 =  [float(listForIndoorCombin[3][0][0][0].split(',')[0]),float(listForIndoorCombin[3][0][0][0].split(',')[1])]
		n2 =  [float(listForIndoorCombin[3][0][1][0].split(',')[0]),float(listForIndoorCombin[3][0][1][0].split(',')[1])]
		n3 =  [float(listForIndoorCombin[3][0][2][0].split(',')[0]),float(listForIndoorCombin[3][0][2][0].split(',')[1])]
		n4 =  [float(listForIndoorCombin[3][0][3][0].split(',')[0]),float(listForIndoorCombin[3][0][3][0].split(',')[1])]
	
		#TwoPoint	
		TheMinum = [0,100]	
		for j in range(1,7):
			p1 = [float(listForGpsCombin[1][j-1][0][0].split(',')[0]),float(listForGpsCombin[1][j-1][0][0].split(',')[1])]
			p2 = [float(listForGpsCombin[1][j-1][1][0].split(',')[0]),float(listForGpsCombin[1][j-1][1][0].split(',')[1])]
			#rN are the local coordinates (MDB)
			r1 = [float(listForIndoorCombin[1][j-1][0][0].split(',')[0]),float(listForIndoorCombin[1][j-1][0][0].split(',')[1])]
			r2 = [float(listForIndoorCombin[1][j-1][1][0].split(',')[0]),float(listForIndoorCombin[1][j-1][1][0].split(',')[1])]
				
			A,X0,K = CalcXY2GPSParam_2p(r1,r2,p1,p2)
			temp = Average(A, X0, K, n1, m1, n2, m2, n3, m3, n4, m4)
			#print temp
			if (temp <= TheMinum[1]) & (temp != -1):
				TheMinum[1] = temp
				TheMinumr1 = r1
				TheMinumr2 = r2
				TheMinump1 = p1
				TheMinump2 = p2
				
		#print 'ShopName=',lines[0][0],'Y2P_ERROR=',TheMinum[1],'\nPoints is ',TheMinump1,TheMinump2,TheMinumr1,TheMinumr2
		#print TheMinum
		
		#ThreePoint		
		for j in range(1,5):
			p1 = [float(listForGpsCombin[2][j-1][0][0].split(',')[0]),float(listForGpsCombin[2][j-1][0][0].split(',')[1])]
			p2 = [float(listForGpsCombin[2][j-1][1][0].split(',')[0]),float(listForGpsCombin[2][j-1][1][0].split(',')[1])]
			p3 = [float(listForGpsCombin[2][j-1][2][0].split(',')[0]),float(listForGpsCombin[2][j-1][2][0].split(',')[1])]	
			#rN are the local coordinations (MDB)
			r1 = [float(listForIndoorCombin[2][j-1][0][0].split(',')[0]),float(listForIndoorCombin[2][j-1][0][0].split(',')[1])]
			r2 = [float(listForIndoorCombin[2][j-1][1][0].split(',')[0]),float(listForIndoorCombin[2][j-1][1][0].split(',')[1])]
			r3 = [float(listForIndoorCombin[2][j-1][2][0].split(',')[0]),float(listForIndoorCombin[2][j-1][2][0].split(',')[1])]
			A,X0,K = CalcXY2GPSParam_3p(r1,r2,r3,p1,p2,p3)
			
			temp = Average(A, X0, K, n1, m1, n2, m2, n3, m3, n4, m4)
			#print temp
			if (temp <= TheMinum[1]) & (temp != -1):
				TheMinum[1] = temp
				TheMinumr1 = r1
				TheMinumr2 = r2
				TheMinumr3 = r3
				TheMinump1 = p1
				TheMinump2 = p2
				TheMinump3 = p3
				#print 'ShopName=',lines[0][0],'Y3P_ERROR=',TheMinum[1],'\nPoints is ',TheMinump1,TheMinump2,TheMinump3,TheMinumr1,TheMinumr2,TheMinumr3
		if ('TheMinump3' in dir()) == True:
			print (name+','+str(TheMinum[1])+','+str(TheMinump1)+','+str(TheMinumr1)+','+str(TheMinump2)+','+str(TheMinumr2)+','+str(TheMinump3)+','+str(TheMinumr3))
			
			del TheMinump3,TheMinumr3
		elif (('TheMinump1' in dir()) == True) & (('TheMinump3' in dir()) == False) :
			print (name+','+str(TheMinum[1])+','+str(TheMinump1)+','+str(TheMinumr1)+','+str(TheMinump2)+','+str(TheMinumr2))


fp.close()
#resultsetfile.close()
	
	
	#print 'Y2p_Error = '
	#print TheMinum
	#print average


	# =============================
	# x1 = [0,0]
	# x2 = [1,1]
	# x3 = [2,0]
	# x4 = [0,1]

	# g1 = [0,0]
	# g2 = [1.0/3.0,1.0/2.0]
	# g3 = [2.0/3.0,0]
	# g4 = [-0.25,0.5]

	# K = array([3.0,2.0])
	# A,X0,K = CalcXY2GPSParam(x1,x2,g1,g2,K)

	# print 'Y = '
	# print dot(A,(x3-X0))/K

	# =========================================
	# x1 = [0,0]
	# x2 = [1,1]
	# x3 = [0,2]
	# x4 = [0,1]

	# g1 = [-0.5,0]
	# g2 = [0.0,0.0]
	# g3 = [0,1]
	# g4 = [-0.25,0.5]

	# K = array([2*sp.sqrt(2),sp.sqrt(2)])
	# A,X0,K = CalcXY2GPSParam(x1,x2,g1,g2,K)

	# print 'Y = '
	# print dot(A,(x1-X0))/K
	