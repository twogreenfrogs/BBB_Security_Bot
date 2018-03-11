#!/usr/bin/python
import serial, time, datetime, re, os, sys, logging, logging.handlers

#os.system("echo uart1 > /sys/devices/bone_capemgr.9/slots")
cmd=sys.argv[1]

serial = serial.Serial("/dev/ttyACM1", 115200, 8, 'N', 1, timeout=10)
resp = ""

#enable logging
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler('/dev/log')
my_logger.addHandler(handler)


#while True:
#serial.write("at*eevinfo\r\n")
#serial.write("AT+CPIN?\r\n")
serial.write(cmd + "\r\n")
time.sleep(1)
while (serial.inWaiting() > 0):
	resp += serial.read(1)

if resp !='':
	print resp
#        if "\n" in resp:
#		print resp
resp = ""

