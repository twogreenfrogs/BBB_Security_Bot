#!/usr/bin/python
import httplib, sys, string, json, copy, logging, logging.handlers, pickle
import serial, time
from base64 import b64encode
from time import sleep
from subprocess import call

#import DTS overlay scripts
overlay_gpio="/root/startup_scripts/overlay_gpio.bash"
overlay_uart="/root/startup_scripts/overlay_uart.bash"
overlay_pwm="/root/startup_scripts/overlay_pwm.bash"
call([overlay_gpio])
call([overlay_uart])
call([overlay_pwm])

#srv_addr=sys.argv[1]
srv_addr="192.168.1.107"
#define script to execute
wifi_script="/root/startup_scripts/wifi_script.bash"
umts_script="/root/startup_scripts/umts_script.bash"
webcam_script="/root/startup_scripts/webcam_script.bash"
ipcam_script="/root/startup_scripts/ipcam_script.bash"
robot_script="/root/startup_scripts/robot_script.bash"
move_script="/root/startup_scripts/move_script.bash"
arm_script="/root/startup_scripts/arm_script.bash"
lamp_script="/root/startup_scripts/lamp_script.bash"
hbridge_script="/root/startup_scripts/hbridge_script.bash"
#enable logging & debugging
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler('/dev/log')
my_logger.addHandler(handler)

debug = True
def debugMsg(msg):
	if (debug):
		print(msg)
		#my_logger.debug(msg)
		

# open serial ports for lprf and keypad
try:
        keypad=serial.Serial('/dev/ttyO4', 9600, timeout=1)
        time.sleep(1)
        lprf=serial.Serial('/dev/ttyO1', 9600, timeout=1)
except:
        debugMsg("failed to open serial ports...")
        exit()

# default robot status
with open('robot_status.pickle', 'rb') as handle:
        robot_status = pickle.load(handle)

def put_status(api_server):
	headers={"Accept": "*/*",
         	 "Content-Type": "application/json",
	 	 "User-Agent": "inzoo-beablebone",
	}
	try:
		conn = httplib.HTTPConnection(api_server)
		for item in robot_status:
			body = '{"desc":"'+item['desc']+'", "status":"'+item['status']+'"}'
			conn.request("PUT", "/robot/api/"+item['desc'], body, headers=headers)
			response = conn.getresponse()
			data = response.read()
			my_logger.debug("REST_client.py:\n" +  data)
			sleep(0.5)
		conn.close()
		return None
	except:
		return "error"	

def put_status_item(api_server, item):
        headers={"Accept": "*/*",
                 "Content-Type": "application/json",
                 "User-Agent": "inzoo-beablebone",
        }
        try:
                conn = httplib.HTTPConnection(api_server)
                body = '{"desc":"'+item['desc']+'", "status":"'+item['status']+'"}'
                conn.request("PUT", "/robot/api/"+item['desc'], body, headers=headers)
                response = conn.getresponse()
                data = response.read()
                my_logger.debug("REST_client.py:\n" +  data)
                sleep(0.5)
                conn.close()
                return None
        except:
                return "error"

# read api web server status and check if in sync
def get_status(api_server):
	headers={"Accept": "*/*",
         	 "Content-Type": "application/json",
	 	 "User-Agent": "inzoo-beablebone",
	}
	try:
		conn = httplib.HTTPConnection(api_server)
		conn.request("GET", "/robot/api", headers=headers)
		response = conn.getresponse()
		data = response.read()
		server_status=json.loads(data)
		conn.close()
		return server_status 
	except:
		return "error"

def get_status_item(api_server, item):
        headers={"Accept": "*/*",
                 "Content-Type": "application/json",
                 "User-Agent": "inzoo-beablebone",
        }
        try:
                conn = httplib.HTTPConnection(api_server)
                conn.request("GET", "/robot/api/"+item, headers=headers)
                response = conn.getresponse()
                data = response.read()
                server_status=json.loads(data)
                conn.close()
                return server_status
        except:
                return "error"

def take_action(item, status):
	if item == 'wifi':
		if status == 'on':
			call([wifi_script, "start"])
			debugMsg("REST_client.py: wifi_script start")
		else:
			call([wifi_script, "stop"])
			debugMsg("REST_client.py: execute wifi_script stop")

	elif item == 'umts':
		if status == 'on':
			if call([umts_script, "start"]):
				debugMsg("REST_client.py: umts_script start failed")
				item=filter(lambda t: t['desc'] == 'umts', robot_status)
				item[0]['status']='off'
			else:
				debugMsg("REST_client.py: umts_script start")
				
		else:
			if call([umts_script, "stop"]):
				debugMsg("REST_client.py: umts_script stop failed")
				item=filter(lambda t: t['desc'] == 'umts', robot_status)
				item[0]['status']='on'
			else:
				debugMsg("REST_client.py: execute umts_script stop")

	elif item == 'webcam':
		if status == 'on':
			call([webcam_script, "start"])
			debugMsg("REST_client.py: webcam_script start")
		else:
			call([webcam_script, "stop"])
			debugMsg("REST_client.py: execute webcam_script stop")


	elif item == 'ipcam':
		debugMsg("REST_client.py: execute ipcam_script")
		print "ipcam_script ", status

	elif item == 'robot':
		debugMsg("REST_client.py: execute robot_script")
		print "robot_script ", status

	elif item == 'move':
		print "move_script ", status
		debugMsg("REST_client.py: execute move_script")
                if status == 'forward':
			debugMsg("REST_client.py: move_script forward")
                        call([hbridge_script, "1", "0", "0", "1"])
                elif status == 'backward':
			debugMsg("REST_client.py: move_script backward")
                        call([hbridge_script, "0", "1", "1", "0"])
                elif status == 'right':
			debugMsg("REST_client.py: move_script right")
                        call([hbridge_script, "0", "1", "0", "1"])
                elif status == 'left':
			debugMsg("REST_client.py: move_script left")
                        call([hbridge_script, "1", "0", "1", "0"])
                else:
			debugMsg("REST_client.py: move_script stop")
                        call([hbridge_script, "0", "0", "0", "0"])
		
	elif item == 'armed':
		keypad.flush()
		lprf.flush()
                if status == 'on':
			lprf.write('^i1c111$')
			time.sleep(1)
			keypad.write('^i1k111$')
                        debugMsg("REST_client.py: keypad/lprf armed")
                else:
			lprf.write('^i1c110$')
			time.sleep(1)
			keypad.write('^i1k110$')
                        debugMsg("REST_client.py: keypad/lprf unarmed")

	elif item == 'lamp':
		# no diffrent lamp on/off command.
		keypad.flush()
		lprf.flush()
                if status == 'on':
			lprf.write('^i1p111$')
                	debugMsg("REST_client.py: lamp turn on/off")
		else:
			lprf.write('^i1p110$')
                	debugMsg("REST_client.py: lamp turn on/off")
	else:
               	debugMsg("REST_client.py: unrecognized item")
		

def main():
	prev_status=copy.deepcopy(robot_status)

	# configure system per robot_status
        for item in robot_status:
        	take_action(item['desc'], item['status'])
		debugMsg(item['desc'] + " initialized")
		sleep(1)
	
	# sync robot status with api web server
	try:
		while True:
			sleep(3) #every 5 sec, REST_client.py tries to connect to server until successful
			if put_status(srv_addr) == "error":
				debugMsg("REST_client.py: put_status- status update error...")
			else:
				debugMsg("REST_client.py: put_status- sync up done...")
                                debugMsg("Beablebone Robot ready...")
				print
				break
        except KeyboardInterrupt:
                debugMsg("keyboard interrupt caught")
		return	

	# get server status and sync up with robot_status. take appropriate action
	try:
		while True:
			sleep(3) #every 5 sec, REST_client.py tries to sync with server
			keypad.flush()
			lprf.flush()
	
			#sync up with servr	
			'''
        		for item in robot_status:
				server_status = get_status_item(srv_addr, item['desc'])	
				if server_status == "error":
					debugMsg("REST_client.py: get_status_item- error occured...")
					break

                		if server_status['status']['status'] != item['status']:
					item['status']=server_status['status']['status']
				debugMsg("REST_client.py: get_status_item- sync up done...")
			'''
                        server_status = get_status(srv_addr) 
                        if server_status == "error":
                                debugMsg("REST_client.py: get_status_item- error occured...")
                                break
			else:
				for server_item in server_status['status']:
					robot_item = filter(lambda t: t['desc'] == server_item['desc'], robot_status)	
					robot_item[0]['status'] = server_item['status']
					#debugMsg(robot_item[0]['desc'] + " changed to " + robot_item[0]['status'])
	
			#read keypad input
		        resp = keypad.readline().strip()
        		
			if resp == '^k1i111$':
				item = filter(lambda t: t['desc'] == 'armed', robot_status)
				item[0]['status'] = u'on'
                		debugMsg('arm system...')
        		elif resp == '^k1i110$':
				item = filter(lambda t: t['desc'] == 'armed', robot_status)
				item[0]['status'] = u'off'
                		debugMsg('unarmed system...')
        		elif resp == '*':
                		debugMsg('turn on/off outlet')
				item = filter(lambda t: t['desc'] == 'lamp', robot_status)
				if item[0]['status'] == u'off':
					item[0]['status']=u'on'
				else:
					item[0]['status']=u'off'
        		else:
                		print resp
        			resp = ''

			#find changes and take action 
			if prev_status != robot_status:
				debugMsg("REST_client.py: prev_status is different from curr_status")
				changes=[i for i,j in zip(robot_status, prev_status) if i != j]
				print "changes:"
				print changes
				print
				for item in changes:
					take_action(item['desc'], item['status'])
					#sync up with server
					if put_status_item(srv_addr, item) == "error":
						debugMsg("put_status_item error...")	
					else:	
						prev_status=copy.deepcopy(robot_status)
						debugMsg("current robot status:")
						debugMsg(robot_status)

	except KeyboardInterrupt:
		debugMsg("keyboard interrupt caught")
		return

if __name__=='__main__':
	main()
