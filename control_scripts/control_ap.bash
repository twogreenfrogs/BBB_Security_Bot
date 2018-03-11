#!/bin/bash
# Get function from functions library
#. /etc/init.d/functions
dir="/root/startup_scripts"
PATH=$PATH:$dir
export PATH
int_out="wwan0"
int_in="wlan0"

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
	ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
	check_error ifconfig_wlan0
	sleep 2

	#start dhcpd
	ps -ef | grep -v grep | grep dhcpd > /dev/null
	if [ $? != 0 ] 
	then
		dhcpd wlan0 & > /dev/null
		ps -ef | grep -v grep | grep dhcpd > /dev/null
		check_error dhcpd_wlan0
	fi
	echo "dhcpd: OK"

	#enable masquerade
	modprobe iptable_nat
	iptables --flush
	iptables -t nat -A POSTROUTING -o $int_out -j MASQUERADE
	iptables -A FORWARD -i $int_in -o $int_out -j ACCEPT
	iptables -A FORWARD -i $int_in -o $int_out -m state --state RELATED,ESTABLISHED -j ACCEPT
	#sysctl -w net.ipv4.ip_forward=1a
	echo 1 > /proc/sys/net/ipv4/ip_forward

	#start hostapd
	if [ "$(ps -e | grep hostapd)" == "" ] 
	then
		hostapd -B /etc/hostapd/hostapd.conf > /dev/null
		ps -e | grep hostapd > /dev/null
		check_error hostadp
	fi
	echo "hostapd: OK"
	echo "access point started..."
}
stop() {
	killall hostapd
	killall dhcpd
	ifconfig wlan0 down
	echo "access point stopped..."
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
    	ifconfig | grep wlan0 > /dev/null
	if [ $? == 0 ]
	then
		echo "access point up"
	else
		echo "access point down"
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
