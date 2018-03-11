#!/bin/bash
# to open stream in the browser or in vlc
# http://192.168.1.114:8080/?action=stream
# vlc http://192.168.1.114:8080/?action=stream

start () {
	/usr/local/bin/mjpg_streamer -b -i "/usr/local/lib/input_uvc.so -r 640x480 -f 15 -d /dev/video0" -o "/usr/local/lib/output_http.so -p 8080 -w /usr/local/www" > /dev/null
	sleep 5
	pgrep mjpg_streamer 
	if [ $? != 0 ]
	then
		logger "webcam_script.bash: Error - failed to start webcam"
		exit 1
	else
		logger "webcam_script.bash: webcam started..."
	fi
}

stop () {
	killall mjpg_streamer > /dev/null
	sleep 3
	pgrep mjpg_streamer
	if [ $? == 1 ]
		then
        	logger "webcam_script.bash: stopped webcam"
	else
        	logger "webcam_script.bash: failed to stoop webcam"
        	exit 1
	fi


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
