#!/bin/bash

for ((i=0;i<=9;i++))
do
	sudo bluetoothctl connect 90:7f:61:58:10:80
	sudo bluetoothctl info 90:7f:61:58:10:80 | grep "Connected: yes"
	if [ $? -eq 0 ]
	then
		break
	else
		sleep 3
	fi
done
