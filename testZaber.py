'''
author: ashish
license: GPL v3.0
brief: Zaber's binary stepper motor control. The code demonstrates a circular motion
       of the combination of two devices in a plane.
       Ref: http://www.zaber.com/wiki/Manuals/Binary_Protocol_Manual
Pre: Do install Zaber's serial package from http://www.zaber.com/wiki/Software
'''


from zaber.serial import BinarySerial, BinaryDevice, BinaryCommand
import sys,os,thread,time,xlsxwriter,xlrd,re,math,serial


print "Port Opening..."
port = BinarySerial("/dev/ttyUSB0")
port.timeout = 30

resolution_mm = 0.124023438*1e-3
spd_mm_s = 10
spd_steps = int((spd_mm_s * 1.6384)/resolution_mm)
print spd_steps 

# Device number 0, command number 1.
radius = 100000
steps = 10
theta = (2*3.14159)/steps

device = BinaryDevice(port, 2)
device1 = BinaryDevice(port, 3)

device.send(42, spd_steps)
device1.send(42, spd_steps)

#move to diameteric point so as to avoid negative cos and sin
dia = 2*radius+1000000
resp = device.move_abs(dia)
resp1 = device1.move_abs(dia)
print 'New origin (',resp.data,', ',resp1.data,')'
time.sleep(2)
#move (R,0) relative to diamteric opposite point
#resp = device.move_rel(radius)
#print 'moving to (',resp.data,', ',0,') for theta value = 0'
time.sleep(2)

for step in range(steps+1):
	x = int(dia + radius * math.cos(step*theta))
	y = int(dia + radius * math.sin(step*theta))
	print 'moving to (',x,', ',y,') for theta value = ',(step*theta)
	resp = device.move_abs(x)
	resp1 = device1.move_abs(y)
	print 'moved to (',resp.data,', ',resp1.data,') for theta value = ',(step*theta)
	print 'reading field'
	time.sleep(2)

'''
#device.send(36)

print device.home()
#device.send(22, 13210)
if (not(device.get_status()==0)):
	print "1"
	time.sleep(2)
time.sleep(1)
resp = device.move_rel(100000)
distRead = (resp.data*0.124023438)
print (distRead*1e-4),'cm'
time.sleep(1)
resp = device.move_rel(100000)
distRead = (resp.data*0.124023438)
print (distRead*1e-4),'cm'
time.sleep(1)
resp = device.move_rel(100000)
distRead = (resp.data*0.124023438)
print (distRead*1e-4),'cm'

if (not(device.get_status()==0)):
	print "2"
	time.sleep(0.5)
#device.send(42, 13210)
print device.get_status()
'''
'''
axis1 = device.axis(1)

axis1.send("home")

reply = portZaber.read()

if reply.reply_flag == "RJ":
    print("A command was rejected! Reason: {}".format(reply.data))
if reply.warning_flag != "--":
    print("Warning received! Flag: {}".format(reply.warning_flag))

axis1.poll_until_idle()
axis1.send("move rel 100")

reply = portZaber.read()

if reply.reply_flag == "RJ":
    print("A command was rejected! Reason: {}".format(reply.data))
if reply.warning_flag != "--":
    print("Warning received! Flag: {}".format(reply.warning_flag))

# Wait for the device to finish moving.
axis1.poll_until_idle()
'''
