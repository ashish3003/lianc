# -*- coding: utf-8 -*-
'''
author: ashish
license: GPL v3.0
brief: TMC Therionincs Stepper Motor Comtrol using MCode.
       Ref: http://motion.schneider-electric.com/downloads/manuals/MCode.pdf 
'''

import serial,time

def waitFor(ser):
	b = ser.inWaiting() # returns 0]
	while b>0:
		b = ser.inWaiting()
		print b

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,timeout=0)

print ser

a = ser.isOpen() # returns True
print a

'''

    PG ‘ exits program mode (if needed)
    E ‘ ends any running programs
    EE=1 ‘ enables the encoder
    SL 0 ‘ stops movement
    ER=0 ‘ clears errors
    ST=0 ‘ clears stall
    PR AL ‘ get all parameters
    L ‘ get program listing
'''

ser.write('1PG\r\n')
time.sleep(0.5)
ser.write('1E\r\n')
time.sleep(0.5)
ser.write('1EE\0751\r\n')
time.sleep(0.5)
ser.write('1SL 0\r\n')
time.sleep(0.5)
ser.write('1ER\0750\r\n')
time.sleep(0.5)
ser.write('1ST\0750\r\n')
time.sleep(0.5)

ser.write('1PR AL\r\n')
time.sleep(0.5)

data = ser.read(ser.inWaiting())
time.sleep(0.5)
print "All Params",data

ser.write('1PR SN\r\n')
time.sleep(0.5)

data = ser.read(ser.inWaiting())
time.sleep(0.5)
print "SN = ", data

ser.write('1PR PN\r\n')
time.sleep(0.5)

data = ser.read(ser.inWaiting())
time.sleep(0.5)
print "PN = ",data

ser.write('1PR VR\r\n')
time.sleep(0.5)

data = ser.read(ser.inWaiting())
time.sleep(0.5)
print "Version = ",data

ser.write('1L\r\n')
time.sleep(0.5)


#ser.write('1A 10000\r\n')
#time.sleep(1)

#ser.write('1MA -1000\r\n')
time.sleep(3)

#ser.write('1ER\0750\r\n')
#ser.write('1PR AL\r\n')
#time.sleep(0.5)
#data = ser.read(ser.inWaiting())
#print ("AL = %s"%data)

ser.write('1PR P\r\n')
time.sleep(1)

data = ser.read(ser.inWaiting())
#waitFor(ser)
print "P = ",data


ser.close()




