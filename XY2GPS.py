import scipy as sp
from scipy import array, dot, insert, linalg
import os
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
		return y, (y-g)*K
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
	# Data of XiDanDaYueCheng
	# pN are the gps coordinates
	p1 = [116.380003,39.916442]
	p2 = [116.379999,39.917642]
	p3 = [116.379244,39.916397]
	p4 = [116.378813,39.91639]

	# rN are the local coordinates (MDB)
	r1 = [9.806,6.605]
	r2 = [139.972,3.404]
	r3 = [13.4,73.6]
	r4 = [11.84,113.57]

	A,X0,K = CalcXY2GPSParam_2p(r2,r3,p2,p3)
	print 'Y2p_Error = '
	y = XY2GPS(A,X0,K,r3,p3)
	print y


	A,X0,K = CalcXY2GPSParam_3p(r1,r2,r3,p1,p2,p3)
	print 'Y3p_Error = '
	y = XY2GPS(A,X0,K,r3,p3)
	print y

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
	