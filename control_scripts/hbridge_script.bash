#!/bin/bash
#enable GPIOs in P8_11, P8_12, P8_13, P8_14
#cp BBB-Hbridge-00A0.dtbo /lib/firmware/
#export PINS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pins
#export SLOTS=/sys/devices/bone_capemgr.9/slots
#echo BBB-Hbridge > $SLOTS

if [ $# -ne 4 ]
then
	echo "usage: base0 pin1_val pin2_val pin3_val pin4_val"
	exit 1
fi

#gpio sys directory
base_dir="/sys/class/gpio"
# 4 gpio pins going to H-Bridge
pin1=45 # P8_11
pin2=44 # P8_12
pin3=23 # P8_13
pin4=26 # P8_14

#export gpio pins in user land
if [ ! -d ${base_dir}/gpio${pin1} ]
then
	echo $pin1 > "${base_dir}/export"
fi
if [ ! -d ${base_dir}/gpio${pin2} ]
then
	echo $pin2 > "${base_dir}/export"
fi
if [ ! -d ${base_dir}/gpio${pin3} ]
then
	echo $pin3 > "${base_dir}/export"
fi
if [ ! -d ${base_dir}/gpio${pin4} ]
then
	echo $pin4 > "${base_dir}/export"
fi

#set pins to OUTPUT
echo "out" > "${base_dir}/gpio${pin1}/direction"
echo "out" > "${base_dir}/gpio${pin2}/direction"
echo "out" > "${base_dir}/gpio${pin3}/direction"
echo "out" > "${base_dir}/gpio${pin4}/direction"

#set pins to 1 or 0 from argument
echo $1 > "${base_dir}/gpio${pin1}/value"
echo $2 > "${base_dir}/gpio${pin2}/value"
echo $3 > "${base_dir}/gpio${pin3}/value"
echo $4 > "${base_dir}/gpio${pin4}/value"

echo "done..."
exit 0
