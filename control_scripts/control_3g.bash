#!/bin/bash
# Get function from functions library
#. /etc/init.d/functions
dir="/root/startup_scripts"
PATH=$PATH:$dir
export PATH

check_error() {
	if [ $? != 0 ] 
	then
		echo "Error: $1"
		exit 1
	else
		echo "$1: OK"
	fi
}

start() {
	3g_cmd.py AT+CPIN? | grep OK > /dev/null
	check_error CPIN

	3g_cmd.py AT+CFUN=1 > /dev/null
	3g_cmd.py AT+CFUN? | grep OK > /dev/null
	check_error CFUN

	3g_cmd.py AT+CREG? | grep OK > /dev/null
	check_error CREG

	3g_cmd.py AT+CGATT? | grep OK > /dev/null
	check_error CGATT

	#3g_cmd.py 'AT+CGDCONT=1,"IP","broadband"' | grep OK > /dev/null
	3g_cmd.py 'AT+CGDCONT=1,"IP","broadband"' | grep OK > /dev/null
	check_error CGDCONT

	#3g_cmd.py AT*ENAP=1,1 | grep OK > /dev/null
	#??check_error ENAP
	#3g_cmd.py AT*E2IPCFG=1
	#check_error E2IPCFG

	3g_cmd.py AT*E2IPCFG? | grep OK > /dev/null
	if [ $? == 0 ] 
	then
		cfg=$(3g_cmd.py AT*E2IPCFG?)
		echo "AT*E2IPCFG?: " 
		echo "------------ "
		ipaddr=$(echo $cfg | awk -F'"' '{print $2}')
		gwaddr=$(echo $cfg | awk -F'"' '{print $4}')
		dns1=$(echo $cfg | awk -F'"' '{print $6}')
		dns2=$(echo $cfg | awk -F'"' '{print $8}')
		echo "IP_Addr: $ipaddr, GW_Addr: $gwaddr, DNS Srv1: $dns1, DNS Srv2: $dns2"
		echo ""
	else
		echo "3g start failed..."
		exit 1
	fi

	ifconfig wwan0 $ipaddr netmask 255.255.255.0 > /dev/null
	check_error ifconfig_wwan0
	ifconfig wwan0 up > /dev/null
	check_error wwan0_up
	route del default gw $gwaddr > /dev/null
	route add default gw $gwaddr > /dev/null
	check_error config_defaultgw

	#empty /etc/resolv.conf and populate with 3g dns servers
	echo "" > /etc/resolv.conf
	echo "nameserver $dns1" >> /etc/resolv.conf
	echo "nameserver $dns2" >> /etc/resolv.conf
	echo "3g start successful..."
}
stop() {
	ifconfig wwan0 down
	echo "3g stopped..."
}
### main logic ###
case "$1" in
start)
	start
    	;;
stop)
    	stop
    	;;
status)
    	ifconfig | grep wwan0 > /dev/null
	if [ $? == 0 ]
	then
		echo "3g up"
	else
		echo "3g down"
	fi
    	;;
restart|reload)
    stop
    start
    ;;
*)
    echo $"Usage: $0 {start|stop|restart|reload|status}"
    exit 1
esac
exit 0
