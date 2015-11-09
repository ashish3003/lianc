# -*- coding: utf-8 -*-
"""
@file  : prologix_pMtr.py
@author: ashish
@brief : To stress test prologix GPIB-USB converter 
         with Clarke-Hess 6000A Phase Meter.
         Setup:      Function Generator
                             ||
                      -------  --------
                    REF             SIGNAL
         Results are stored in prologixStressTest.log
         in the same folder.
"""

import time, datetime
import serial

def interruptibleSleep(secs):
    for num in range (secs):
        time.sleep(1)

f = open('prologixStressTest.log', 'w');
f.write("----- PROLOGIX GPIB-USB STRESS TESTING LOG -----\n\n")


# Open serial port
ser = serial.Serial( "/dev/ttyUSB0", 9600, timeout=0.5 )

# Set mode as CONTROLLER
ser.write("++mode 1\n")

# Set 6000A address = 5
addr = "5"
ser.write("++addr " + addr + "\n")

# Turn off read-after-write to avoid "Query Unterminated" errors
ser.write("++auto 0\n")

# Do not append CR or LF to GPIB data
ser.write("++eos 3\n")

# Assert EOI with last byte to indicate end of data
ser.write("++eoi 1\n")

# Reset AWG 
cmd = "*IDN?"
print cmd
ser.write(cmd + "\n")   
time.sleep(2)
ser.write("++read eoi\n")
s0 = ser.read(100)
f.write("Device Name: %s"%s0)
print s0    

# Set Function generator address = 9
addr = "9"
ser.write("++addr " + addr + "\n")

# Turn off read-after-write to avoid "Query Unterminated" errors
ser.write("++auto 0\n")

# Do not append CR or LF to GPIB data
ser.write("++eos 3\n")

# Assert EOI with last byte to indicate end of data
ser.write("++eoi 1\n")

# Reset AWG 
cmd = "*IDN?"
print cmd
ser.write(cmd + "\n")   
time.sleep(2)
ser.write("++read eoi\n")
s0 = ser.read(100)
f.write("Device Name: %s"%s0)
print s0    

freq = "1200"
cmd = "APPL:SIN "+freq+" KHZ, 3.0 VPP, -2.5 V"
print cmd
ser.write(cmd + "\n")   

f.write("\nFREQUENCY             PHASE               TIME \n")
f.write('-----------------------------------------------------------------\n')

while 1:
    try:
	# Read Phase Meter
	addr = "5"
	ser.write("++addr " + addr + "\n")
        cmd = "FREQ?"
        print cmd
        ser.write(cmd + "\n")   
#        time.sleep(0.5)
        ser.write("++read eoi\n")
        s1 = ser.read(100)
        s1 = s1.rstrip()
        print s1    
        
        cmd = "PHASE?"
        print cmd
        ser.write(cmd + "\n")   
#        time.sleep(0.5)
        ser.write("++read eoi\n")
        s2 = ser.read(100)
        s2 = s2.rstrip()
        print s2   
        
        s3 = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S')
        
        s4 = s1+'\t\t      '+s2+'\t\t'+s3+'\n'
        print s4
        f.write(s4)
        interruptibleSleep(1800)        # wait for 30 mins for next reading
    except:
        f.close()
        cmd = "++loc"
        print cmd
        ser.write(cmd + "\n")   
        ser.close()
#f.close()
