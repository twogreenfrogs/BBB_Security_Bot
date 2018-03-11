#!/bin/bash
#dtc compiled device tree files .dtbo should be under /lib/firmwares
#example:
# 1. dtc -O dtb -o DM-GPIO-Test-00A0.dtbo -b 0 -@ DM-GPIO-Test.dts
# 2. cp DM-GPIO-Test-00A0.dtbo /lib/firmwares
# 3. echo DM-GPIO-Test > /sys/devices/bone_capemgr.9/slots
SLOTS="/sys/devices/bone_capemgr.9/slots"
PINS="/sys/kernel/debug/pinctrl/44e10800.pinmux/pins"
echo BBB-Robot-GPIO > $SLOTS 
#gpio sys directory
base_dir="/sys/class/gpio"

# 4 GPIO pins for hbridge
pin1=45 # P8_11
pin2=44 # P8_12
pin3=23 # P8_13
pin4=26 # P8_14
pin5=47 # P8_15
pin6=46 # P8_16

#export gpio pins in user land
if [ ! -d ${base_dir}/gpio${pin1} ]
then
        echo $pin1 > "${base_dir}/export"
fi

if [ ! -d ${base_dir}/gpio${pin1} ]
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
if [ ! -d ${base_dir}/gpio${pin5} ]
then
        echo $pin5 > "${base_dir}/export"
fi
if [ ! -d ${base_dir}/gpio${pin6} ]
then
        echo $pin6 > "${base_dir}/export"
fi

#set pins to OUTPUT
echo "out" > "${base_dir}/gpio${pin1}/direction"
echo "out" > "${base_dir}/gpio${pin2}/direction"
echo "out" > "${base_dir}/gpio${pin3}/direction"
echo "out" > "${base_dir}/gpio${pin4}/direction"
echo "out" > "${base_dir}/gpio${pin5}/direction"
echo "out" > "${base_dir}/gpio${pin6}/direction"
