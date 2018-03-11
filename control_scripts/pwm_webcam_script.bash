#!/bin/bash
if [ $# -gt 2 ]
then
        echo "usage: $0 [l|r|u|d|c]"
        echo " or    $0 servo_num[31|42] servo_val[1000000-2000000]"
        exit 1
fi

#center servos
cd /sys/devices/ocp.3/pwm_test_P9_42*
echo 20000000 > period
echo 0 > polarity
echo 1500000 > duty
cd /sys/devices/ocp.3/pwm_test_P9_31*
echo 20000000 > period
echo 0 > polarity
echo 1500000 > duty

if [ $# == 1 ]
then
	case "$1" in
	l)
		cd /sys/devices/ocp.3/pwm_test_P9_42*
		servo_val=2000000
		while [ $servo_val -gt 1000000 ]
		do
			echo $servo_val > duty
			servo_val=$(($servo_val - 10000))
			echo $servo_val
			sleep 0.05
		done	 
		exit 0	
		;;
	r)
	        cd /sys/devices/ocp.3/pwm_test_P9_42*
                servo_val=1000000
                while [ $servo_val -le 2000000 ]
                do
                        echo $servo_val > duty
                        servo_val=$(($servo_val + 10000))
                        echo $servo_val
                        sleep 0.05
                done
                exit 0
		;;
	u)
	        cd /sys/devices/ocp.3/pwm_test_P9_31*
                servo_val=1000000
                while [ $servo_val -le 2000000 ]
                do
                        echo $servo_val > duty
                        servo_val=$(($servo_val + 10000))
                        echo $servo_val
                        sleep 0.05
                done
                exit 0 
                ;;
	d)
	        cd /sys/devices/ocp.3/pwm_test_P9_31*
                servo_val=2000000
                while [ $servo_val -gt 1000000 ]
                do
                        echo $servo_val > duty
                        servo_val=$(($servo_val - 10000))
                        echo $servo_val
                        sleep 0.05
                done
                exit 0	
		;;
	c)	
	        cd /sys/devices/ocp.3/pwm_test_P9_42*
                echo 1500000 > duty
	        cd /sys/devices/ocp.3/pwm_test_P9_31*
                echo 1500000 > duty
		exit 0
		;;
	*)
		exit 1	
		;;
	esac
else
	cd /sys/devices/ocp.3/pwm_test_P9_$1*
	echo $2 > duty
	exit 0
fi
