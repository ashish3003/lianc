# -*- coding: utf-8 -*-
"""
author: ashish
license: GPL v3.0
brief: Interfacing of Amplifier Research 200T8G18A 250W Microwave amplifier and 
       R&S RF and Microwave Signal Generator using GPIB.
pre: python gpib packge must be installed first. Download it from:
     http://sourceforge.net/projects/linux-gpib/files/
     Ref: http://cdn.rohde-schwarz.com/pws/dl_downloads/dl_application/application_notes/1gp79/1GP79_1E_SCPI_Programming_Guide_SigGens.pdf  
"""

import gpib
import time
rfAmp= gpib.find("fCtr") # define in /etc/gpib.conf
sigGen= gpib.find("pMtr")

def query(handle, command, numbytes=100):
	gpib.write(handle,command)
	time.sleep(0.1)
	response = gpib.read(handle,numbytes)
	return response
 
print "Connected to,"
print query(rfAmp,"*IDN?")
print query(sigGen,"*IDN?")

print "RF Forward Power", query(rfAmp,"RDPOD")
print "RF Reverse Power", query(rfAmp,"RDPRD")

print "Read Gain", query(rfAmp, "RDA")
#print "Set Gain", query(rfAmp, "SA 10")

print "Set Signal Generator Frequency", query(sigGen,"FREQ 12 GHz")
print "Set Signal Generator Power", query(sigGen,"POW -10 dBm")
print "Set Signal Generator Output"
resp = query(sigGen,"OUTP ON; *OPC?")
if resp != 1:
	sys.exit(0)
else:
	print "Returning to local mode..bye!!"
	gpib.ibloc(rfAmp)
	gpib.ibloc(sigGen)
	gpib.close(rfAmp)
	gpib.close(sigGen)
