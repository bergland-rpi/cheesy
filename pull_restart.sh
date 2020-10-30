#!/bin/bash

sleep 30
hn=cheesy
cd /home/pi/$hn
git pull

if ps -e | grep python > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    cd /home/pi/cheesy
    sudo python masterprogram.py config.txt &
    sleep 15
    
fi
