#!/usr/bin/python

#import packages
import sys
import time
import RPi.GPIO as GPIO
import ConfigParser
import csv
from shutil import copyfile
import filecmp
import smbus
import time


#this python script should be run with a config.txt argument that defines two variables. This config file will be edited on github to change the settings of the program
inputfile=str(sys.argv[1])

#name the outfile based on teh day the program started
outFile="/home/pi/cheesy/log."+time.strftime("%Y-%m-%d")+".txt"

#definte a function to read the variables from teh configuration file
Config = ConfigParser.ConfigParser()
Config.read(inputfile)
ventilation_on_time=Config.getint("settings", "ventilation_on_time") #time in minutes the vents should be on
ventilation_off_time=Config.getint("settings", "ventilation_off_time") #time in minutes the vents should be off


# function to that will copy the configuration file into a dated copy. this will be used to see if the configuration file has changed

    
#make a dated copy of current configuration file at start of new configuration
configpath = "/home/pi/cheesy/"+inputfile
configcopy = "/home/pi/cheesy/config"+time.strftime("%Y-%m-%d")+".copy.log"
copyfile(configpath, configcopy)


#setup ventilation via Powerswitch on GPIO 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

#turn ventilation off in case it was on when the program started
GPIO.output(23, False)

#define a ventilation variable that says whether ventilation is on or off
ventilation="OFF"



#initiate the datalog output file
c =(open(outFile, 'wb'))
wrtr = csv.writer(c)

#write a header column in master data file. this will only happen once at the start of the program and any time the porogram restarts it will make a new one.
wrtr.writerow(["TimeStamp", "cTemp", "fTemp", "Humidity", "Ventilation"])
c.flush()

#run an infinite loop that will turn ventilation on and off based on settings
while True:
    #check if input file has changed from the backup copy
    if filecmp.cmp(configpath, configcopy) == False:
        print "configuration changed! updating settings"
        configcopy = "/home/pi/cheesy/config"+time.strftime("%Y-%m-%d")+".copy.log"
        copyfile(configpath, configcopy)
        Config.read(inputfile)
        ventilation_on_time=Config.getint("settings", "ventilation_on_time") #time in minutes the vents should be on
        ventilation_off_time=Config.getint("settings", "ventilation_off_time") #time in minutes the vents should be off
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x44, 0x00, 6)

# Convert the data
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    now = time.localtime(time.time())
    timeStamp = time.strftime("%Y-%m-%d %H:%M:%S", now)

    #turn ventilation on if it's off, then sleep for the on time
    if ventilation=="OFF":
        GPIO.output(23, True)
        print "turning ventilation on"
        ventilation="ON"
        #write data
        wrtr.writerow([timeStamp, cTemp, fTemp, humidity, ventilation])
        c.flush()
        #sleep
        print "sleeping " + str(ventilation_on_time) + " minutes"
        time.sleep(ventilation_on_time*60)


    #turn ventilation off if it's on, then sleep for the off time
    else:
        print "turning ventilation off"
        GPIO.output(23,False)
        ventilation="OFF"
        #write data
        wrtr.writerow([timeStamp, cTemp, fTemp, humidity, ventilation])
        c.flush()
        #sleep
        print "sleeping " + str(ventilation_off_time) + " minutes"
        time.sleep(ventilation_off_time*60)
