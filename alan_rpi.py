#!/usr/bin/python

#import packages
import sys
import time
import RPi.GPIO as GPIO
import ConfigParser
import csv
from shutil import copyfile
import filecmp


#this python script should be run with a config.txt argument that defines two variables. This config file will be edited on github to change the settings of the program
inputfile=str(sys.argv[1])

#name the outfile based on teh day the program started
outFile="/home/pi/log."+time.strftime("%Y-%m-%d")+".txt"

#definte a function to read the variables from teh configuration file
def readInput(startingfile):
    Config = ConfigParser.ConfigParser()
    Config.read(startingfile)
    #Main light cycle
    ventilation_on_time=Config.getint("settings", "ventilation_on_time") #time in minutes the vents should be on
    ventilation_off_time=Config.getint("settings", "ventilation_off_time") #time in minutes the vents should be off


#define function to that will copy the configuration file into a dated copy. this will be used to see if the configuration file has changed
def configureSettings():

    #make a dated copy of current configuration file at start of new configuration
    configpath="/home/pi/"+inputfile
    configcopy="/home/pi/"+inputfile+time.strftime("%Y-%m-%d")+"copy.log"
    copyfile(configpath, configcopy)


#setup ventilation via Powerswitch on GPIO 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

#turn ventilation off in case it was on when the program started
GPIO.output(23, False)

#define a ventilation variable that says whether ventilation is on or off
ventilation="OFF"

#read the initial input and copy the configuration file
readInput(inputfile)
configureSettings()

#initiate the datalog output file
c =(open(outFile, 'wb'))
wrtr = csv.writer(c)

#write a header column in master data file. this will only happen once at the start of the program and any time the porogram restarts it will make a new one.
wrtr.writerow(["TimeStamp", "Temp", "Humidity", "Ventilation"])
c.flush()

#run an infinite loop that will turn ventilation on and off based on settings
while True:
    #check if input file has changed from the backup copy
    if filecomp(configpath, configcopy)==False:
        readinput(inputFile)
        configureSettings()

    #read Temperature
    currtemp=
    #read humidity
    currhum=
    #make timeStamp
    timeStamp=time.strftime("%Y-%m-%d %H:%M:%S", now)

    #turn ventilation on if it's off, then sleep for the on time
    if ventilation=="OFF":
        GPIO.output(23, True)
        ventilation="ON"
        #write data
        wrtr.writerow([timeStamp, currtemp, currhum, ventilation])
        c.flush()
        #sleep
        time.sleep(ventilation_on_time*60)


    #turn ventilation off if it's on, then sleep for the off time
    else:
        GPIO.output(23,False)
        ventilation="OFF"
        #write data
        wrtr.writerow([timeStamp, currtemp, currhum, ventilation])
        c.flush()
        #sleep
        time.sleep(ventilation_off_time*60)
