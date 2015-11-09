'''
author: ashish
license: GPL v3.0
brief: Read LeCroy WS64MXs-A oscilloscopes's screenshot.
       Enter number of points to be captured.
       Do install vxi11 package from https://github.com/python-ivi/python-vxi11
       make one change in the package by adding read_ieee_block() function from
       https://github.com/ceeeeej/python-ivi/blob/develop/ivi/ivi.py
'''

import vxi11, struct
import matplotlib.pyplot as plt

import sys, time, math
from numpy import *
import numpy.fft
from scipy import optimize 
from scipy.optimize import leastsq

from scipy.interpolate import UnivariateSpline
from scipy.interpolate import splrep, sproot, splev
from scipy.optimize import curve_fit


#-------------------------- Gauss Fit ----------------------------------------
def gauss_erf(p,y,x):#height, mean, sigma
	return y - p[0] * exp(-(x-p[1])**2 /(2.0 * p[2]**2))

def gauss_eval(x,p):
	return p[0] * exp(-(x-p[1])**2 /(2.0 * p[2]**2))

def fit_gauss(xlist, ylist):
	size = len(xlist)
	xa = array(xlist, dtype=float)
	ya = array(ylist, dtype=float) 
	'''	
	for num in range(size):
		if math.isnan(ya[num]):
			ya[num] = ya[num-1] + 0.05
	'''	
	maxy = max(ya)
	halfmaxy = maxy / 2.0
	for k in range(size):
		if ya[k] == maxy:#abs(ya[k] - maxy) < maxy/100:
			mean = xa[k]
			break
	for k in range(size):
		if abs(ya[k] - halfmaxy) < halfmaxy/10:
			halfmaxima = xa[k]
			break                      
	sigma = mean - halfmaxima
	par = [maxy, mean, sigma]# [maxy, halfmaxima, sigma] # Amplitude, mean, sigma
	plsq = leastsq(gauss_erf, par,args=(ya,xa))
	if plsq[1] > 4:
		return None
	yfit = gauss_eval(xa, plsq[0])
	# create a spline of x and yfit-np.max(yfit)/2 
	spline = UnivariateSpline(xa, yfit-max(yfit)/2, s=0)
	r1, r2 = spline.roots() # find the roots
	#print r1, r2
	fwhm = 2 * math.sqrt(2*log(2))*sigma
	import pylab as pl
	pl.plot(xa, yfit, xa, ya)
	pl.axvspan(r1, r2, facecolor='g', alpha=0.5)
	pl.show()
	print (r2-r1), fwhm
	return yfit,plsq[0]


def gaus(x,a,x0,sigma,c):
	return a*numpy.exp(-(x-x0)**2/(2*sigma**2))+c

def G_fit(xlist, ylist):
	size = len(xlist)
	x = array(xlist, dtype=float)
	y = array(ylist, dtype=float) 
	mean = sum(x*y)/sum(y)
	sigma = sqrt(abs(sum((x-mean)**2*y)/sum(y)))
	popy, pcov = curve_fit(gaus,x,y,p0=[-max(y),mean,sigma,min(x)+((max(x)-min(x)))/2])
	import pylab as pl
	print popy
	pl.plot(x,gaus(x,*popy))
	pl.show()

'''
def fwhm(X,Y):
    print Y
    half_max = max(Y) / 2.
    #find when function crosses line half_max (when sign of diff flips)
    #take the 'derivative' of signum(half_max - Y[])
    d = numpy.sign(half_max - numpy.array(Y[0:-1])) - numpy.sign(half_max - numpy.array(Y[1:]))
    #plt.plot(X[0:len(d)],d) #if you are interested
    #plt.show()
    #find the left and right most indexes
    print d
    left_idx = find(d > 0)[0]
    right_idx = find(d < 0)[-1]
    return X[right_idx] - X[left_idx]
'''


# Modified for LeCroy, WORKING ON WR104XI-A
def _measurement_fetch_waveform(ch):
	instr = vxi11.Instrument("192.168.2.103")
	print(instr.ask("*IDN?"))
	instr.write("CHDR OFF")
	# Send the MSB first
	# old - instr.write(":waveform:byteorder msbfirst")
	instr.write("COMM_ORDER HI")
	instr.write("COMM_FORMAT DEF9,WORD,BIN")
	# Read wave description and split up parts into variables
	#pre = instr.ask("%s:INSPECT? WAVEDESC" % ch)
	# Replace following with a more simple solution, make it < Python 2.7 compatible
	#temp = []
	#for item in pre:
	#	temp.append(item.split(':'))
	#print temp
	# Dict comprehension, python 2.7+
	#mydict = {t[0].strip(): ["".join(elem.strip()) for elem in t[1:]] for t in temp}
	
	fmt = instr.ask("%s:INSPECT? COMM_TYPE" % ch)
	points = instr.ask("%s:INSPECT? PNTS_PER_SCREEN" % ch)
	xincrement = instr.ask("%s:INSPECT? HORIZ_INTERVAL" % ch)
	xorigin = instr.ask("%s:INSPECT? HORIZ_OFFSET" % ch)
	yincrement = instr.ask("%s:INSPECT? VERTICAL_GAIN" % ch)
	yorigin = instr.ask("%s:INSPECT? VERTICAL_OFFSET" % ch)
	print fmt, points, xincrement, xorigin, yincrement, yorigin
	# Dict with lost comprehension, python 2.6+
	'''
	mydict = dict([(d[0].strip(), "".join(d[1:]).strip()) for d in temp])
	format = str(mydict["COMM_TYPE"])
	points = int(mydict["PNTS_PER_SCREEN"])
	xincrement = float(mydict["HORIZ_INTERVAL"])
	xorigin = float(mydict["HORIZ_OFFSET"])
	yincrement = float(mydict["VERTICAL_GAIN"])
	yorigin = float(mydict["VERTICAL_OFFSET"])
	# Verify that the data is in 'word' format
	if format.lower() != "word":
		print "Problem..format is not word"
	#raise ivi.UnexpectedResponseException()
	'''
	# Read waveform data
	instr.write("%s:WAVEFORM? DAT1" % ch)
	raw_data = instr.read_ieee_block()#(1024, 'ISO-8859-1')
	#print raw_data
	# Split out points and convert to time and voltage pairs
	data = list()
	points = int(input('Enter points: '))#5000
	xincrement = 4.0000e-010
	xorigin = -8.00110420e-007
	yincrement = 2.1249e-006
	yorigin = -1.2000e-003
	#with open('screen.png', 'wb') as f:
    	#	f.write(raw_data)
	x = [0 for n in range(points)]
	y = [0 for n in range(points)]
	for i in range(points):
		x[i] = (i * xincrement) + xorigin
		#print(struct.calcsize(raw_data[i * 2:i * 2 + 2]))
		
		yval = struct.unpack(">H", raw_data[i * 2:i * 2 + 2])[0]
		if yval > 32767:
			yval = yval - (2 ** 16)
		if yval == 0:
			# hole value
			y[i] = float('nan')
		else:
			y[i] = (yincrement * yval) - yorigin
		data.append((x[i], y[i]))

	#plt.plot(x, y,linewidth="3", alpha=0.3)
	#plt.show()
	#G_fit(x,y)
	fit_gauss(x,y)
	#print ('FWHM = ',fwhm(x,y))
	
	
	return data

_measurement_fetch_waveform("C1")
