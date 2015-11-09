"""
Created on Wed Jul  1 13:12:46 2015
@author: ashish
"""

import time, sys, datetime
import serial

def interruptibleSleep(secs):
    for num in range (secs):
        time.sleep(1)

f = open('urv35LevelMeter.log', 'w');
f.write("----- URV35 LEVEL METER TESTING LOG -----\n\n")

se = serial.Serial(port='/dev/ttyUSB0',
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=4,
                    xonxoff=True,			# must be true
                    rtscts=False,
                    writeTimeout=1,
                    dsrdtr=True,
                    interCharTimeout=None)
                    
se.setDTR(True)

print se.portstr					# confirm which port was really used
time.sleep(2)

se.write('ZV\r')					# Identify the meter 
time.sleep(2) 
data = se.read(se.inWaiting())    			# read data from meter 
print data
f.write("Device Name: %s\n"%data)

f.write("\nREADING               	TIME \n")
f.write('--------------------------------------------------\n')

while 1:
	try:
		se.write('W1\r')			# Set CR as terminator
		time.sleep(1)
		se.write('X3\r')			# Trigger measurement automatically
		time.sleep(1)
		se.write('ZM\r')			# Measure a value 
		time.sleep(2) 
		s1 = se.read(se.inWaiting())    	# read data from meter 
		print s1
		s2 = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S')
        	s3 = s1+'\t\t\t'+s2+'\n'
        	print s3
        	f.write(s3)
	except: 					#catch all exceptions here
		e = sys.exc_info()[0]
		print("Error: %s"%e)
		break

se.flush()
se.close()						# close port
print "\ndone! port is closed"
