#!/bin/bash
dir="/root/startup_scripts"
PATH=$PATH:$dir
export PATH
#int_out="wwan0"
#int_in="wlan0"
check_error() {
        if [ $? != 0 ]
        then
                echo "Error: $1"
                exit 1
        else
                echo "$1: OK"
        fi
}

start () {
	logger "wifi_script.bash:starting wifi access point..."
	ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
	check_error ifconfig_wlan0
	sleep 2

       #start hostapd
        logger "checking hostapd"
        pgrep hostapd
        if [ $? != 0 ]
        then
                logger "hostapd is not running.... starting"
                hostapd -B /etc/hostapd/hostapd.conf > /dev/null
                ps -e | grep hostapd > /dev/null
                check_error hostadp
        fi

	#start dhcpd
        logger "checking dhcpd"
	pgrep dhcpd
	if [ $? != 0 ] 
	then
		dhcpd wlan0 &
		ps -e | grep dhcpd > /dev/null
		check_error dhcpd_wlan0
	fi
	logger "wifi_script.bash: dhcpd - OK"

	#enable masquerade
	#modprobe iptable_nat
	#iptables --flush
	#iptables -t nat -A POSTROUTING -o $int_out -j MASQUERADE
	#iptables -A FORWARD -i $int_in -o $int_out -j ACCEPT
	#iptables -A FORWARD -i $int_in -o $int_out -m state --state RELATED,ESTABLISHED -j ACCEPT
	#sysctl -w net.ipv4.ip_forward=1a
	#echo 1 > /proc/sys/net/ipv4/ip_forward

	logger "wifi_script.bash: hostapd - OK"
	logger "wifi_script.bash: wifi started..."
}

stop () {
	logger "wifi_script.bash: stopping wifi access point..."
	killall hostapd
	killall dhcpd
	ifconfig wlan0 down
	logger "wifi_script.bash: wifi stopped..."
}

restart () {
	logger "wifi_script.bash: restarting wifi access point..."
	stop
	start	
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		restart
		;;
	*)
		echo "usage: $0 {start|stop|restart}"
esac
exit 0
