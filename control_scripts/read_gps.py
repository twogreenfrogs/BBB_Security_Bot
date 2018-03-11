#!/usr/bin/python
import serial
import time
import datetime
import re
import os

'''
http://www.softree.com/Tips_Techniques/T-039/Nmea_0183_Import_example.pdf
NMEA data format
$GPRMC, 103804.374 ,A,0411.8650,N,10326.3480,E,0.00,3.85,010304,,*03
103804.374 - Time of fix 10:38:04.374 UTC
A - Navigation receiver warning A = OK, V = warning 
0411.8650,N - Latitude 4 deg. 11.8650 min. North
10326.3480,E - Longitude 103 deg. 26.3480 min East
0.0 - Speed over ground, Knots 
etc...
'''

#os.system("echo uart1 > /sys/devices/bone_capemgr.9/slots")

serial = serial.Serial("/dev/ttyO2", baudrate=9600)

resp = ""

while True:
        while (serial.inWaiting() > 0):
                resp += serial.read()
                if "\r\n" in resp:
                        if "$GPRMC" in resp:
				print resp.strip()
                                data = resp.split(',')
                                info = data[3] + " " + data[4] + " " + data[5] + " " + data[6]
                                print "GPS lat, long: " + info + "\r\n"
                        resp = ""

