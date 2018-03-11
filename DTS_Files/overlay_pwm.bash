#!/bin/bash

cat /sys/devices/bone_capemgr.9/slots | grep am33xx_pwm
if [ $? != 0 ] 
then
	echo am33xx_pwm > /sys/devices/bone_capemgr.9/slots
fi

cat /sys/devices/bone_capemgr.9/slots | grep P9_14
if [ $? != 0 ] 
then
	echo bone_pwm_P9_14 > /sys/devices/bone_capemgr.9/slots
fi

cat /sys/devices/bone_capemgr.9/slots | grep P9_16
if [ $? != 0 ] 
then
	echo bone_pwm_P9_16 > /sys/devices/bone_capemgr.9/slots
fi
echo "done..."
exit 0
