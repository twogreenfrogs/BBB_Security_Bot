#!/bin/bash

dir="/root/startup_scripts"
PATH=$PATH:$dir
export PATH

check_error() {
	if [ $? != 0 ] 
	then
		logger "umts_script.bash: Error- $1"
		exit 1
	else
		logger "umts_script.bash: $1- OK"
	fi
}

start() {
	umts_cmd.py AT+CPIN? | grep OK > /dev/null
	check_error CPIN

	umts_cmd.py 'AT+CFUN=1' > /dev/null
	umts_cmd.py AT+CFUN? | grep OK > /dev/null
	check_error CFUN

	umts_cmd.py AT+CREG? | grep '+CREG: 0,1' > /dev/null
	check_error CREG

	umts_cmd.py AT+CGATT? | grep OK > /dev/null
	check_error CGATT

	umts_cmd.py 'AT+CGDCONT=1,"IP","broadband"' | grep OK > /dev/null
	check_error CGDCONT

	umts_cmd.py 'AT*ENAP=1,1' | grep OK > /dev/null
	check_error ENAP
	
	umts_cmd.py 'AT*E2IPCFG=1' | grep OK > /dev/null
	check_error E2IPCFG

	umts_cmd.py AT*E2IPCFG? | grep OK > /dev/null
	if [ $? == 0 ] 
	then
		cfg=$(3g_cmd.py AT*E2IPCFG?)
		logger "umts_script.bash: AT*E2IPCFG?: " 
		logger "umts_script.bash: ------------ "
		ipaddr=$(echo $cfg | awk -F'"' '{print $2}')
		gwaddr=$(echo $cfg | awk -F'"' '{print $4}')
		dns1=$(echo $cfg | awk -F'"' '{print $6}')
		dns2=$(echo $cfg | awk -F'"' '{print $8}')
		logger "umts_script.bash: IP_Addr: $ipaddr, GW_Addr: $gwaddr, DNS Srv1: $dns1, DNS Srv2: $dns2"
		echo ""
	else
		logger "umts_script.bash: 3g start failed..."
		exit 1
	fi

	ifconfig wwan0 $ipaddr netmask 255.255.255.0 > /dev/null
	check_error ifconfig_wwan0 > /dev/null
	ifconfig wwan0 up > /dev/null
	check_error wwan0_up > /dev/null
	route del default gw $gwaddr > /dev/null
	route add default gw $gwaddr > /dev/null
	check_error config_defaultgw > /dev/null

	#empty /etc/resolv.conf and populate with 3g dns servers
	echo "" > /etc/resolv.conf
	echo "nameserver $dns1" >> /etc/resolv.conf
	echo "nameserver $dns2" >> /etc/resolv.conf
	logger "umts_script.bash: 3g start successful..."
	exit 0
}

stop () {
	ifconfig wwan0 down
	logger "umts_script.bash: 3g stopped..."
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	*)
		echo "usage: $0 {start|stop|restart}"
esac
exit 0
