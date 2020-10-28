#!/bin/bash

sleep 30
hn=cheesy
cd /home/pi/$hn
git pull

if pgrep -f "masterprogram.py" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    sudo python /home/pi/$hn/masterprogram.py /home/pi/$hn/config.txt &
    sleep 15
    
fi
