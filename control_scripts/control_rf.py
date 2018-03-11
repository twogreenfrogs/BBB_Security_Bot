#!/usr/bin/python 
import serial 
import time

armed = False
prev_state = False
curr_state = False
keypad_data = ''
lprf_data = ''
resp = ''

try:
	keypad=serial.Serial('/dev/ttyO4', 9600, timeout=1)
	time.sleep(1)
	lprf=serial.Serial('/dev/ttyO1', 9600, timeout=1)
	time.sleep(1)

	keypad.flush()
	lprf.flush()
except:
	print "failed to open serial ports..."
	exit()

# disarm lprf, keypad when starting system
print "disarm keypad and lprf..."
lprf.write('^i1c110$')
keypad.write('^i1k110$')

#print "arming keypad and lprf"
#lprf.write('^i1c111$');
#keypad.write('^i1k111$');
#to control outlet
#lprf.write('^i1p111$')

while True:
	keypad.flush()
	lprf.flush() 
#	todo: send time stamp to keypad from realtime clock
#	keypad.write('^'+time.strftime('%H:%M:%S %b %d')+'$')

	#while(keypad.inWaiting() > 0):
	#	resp += keypad.read(1)
	resp = keypad.readline().strip()

	if resp == '^k1i111$':
		curr_state=True
		armed=True
		print 'system armed'
	elif resp == '^k1i110$':
		curr_state=False
		armed=False
		print 'system unarmed'
	elif resp == "arming system":
		print 'system arming.'
	elif resp == '*':
		print '---> controlling outlet: ^i1p111$'
		lprf.write('^i1p111$')
	else:
		print resp 
	resp = ''

	# arm or disarm lprf board
	if prev_state is not curr_state:
		prev_state = curr_state

		if armed:
			lprf.write('^i1c111$')
			print '--->lprf armed: ^i1c111$'
			while(lprf.inWaiting() > 0):
        			resp +=lprf.read(1)
			print resp
		else :
			lprf.write('^i1c110$')
			print '--->lprf unarmed: ^i1c110$'
			while(lprf.inWaiting() > 0):
            			resp +=lprf.read(1)
			print resp 
	while(lprf.inWaiting() > 0):
       		resp +=lprf.read(1)
	print resp 

	# todo: take command from main program
        # if logic to break out and close serial ports
	print '---end of loop---'	
	print ''

# close serial ports before exit
lprf.close()
keypad.close()
