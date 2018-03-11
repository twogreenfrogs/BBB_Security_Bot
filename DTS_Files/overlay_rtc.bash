#!/bin/bash
#i2cdetect -y -r 1; to check RTC module is recognized in I2C bus
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
sleep 1
#hwclock -r -f /dev/rtc1; to read time from RTC module
#hwclock -w -f /dev/rtc1; to write system time(from ntp) to RTC module
hwclock -s -f /dev/rtc1 # set system time from RTC
hwclock -w # set HW clock from current system time
