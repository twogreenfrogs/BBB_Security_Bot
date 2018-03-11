#!/bin/bash
if [ $# -ne 4 ]
then
	echo "usage: base0 pin1_val pin2_val pin3_val pin4_val"
	exit 1
fi

#gpio sys directory
base_dir="/sys/class/gpio"
# 4 gpio pins going to H-Bridge
pin1=45
pin2=44
pin3=23
pin4=26

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
