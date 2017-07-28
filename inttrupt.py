#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
import RPi.GPIO as GPIO
import time


import requests
import json
API_KEY = 'o.ct3xmty7V8sNuvcN63SvPNv2GQsoUERg'

def pushMessage(title, body):
    data = {
        'type':'note',
        'title':title,
        'body':body
        }
    resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,'')) #defining the pushmessage function
# Test the function:
pushMessage("SERVER UP", "Hi this is your Pi, I am up and running. I will keep you posted.")


GPIO.setmode(GPIO.BCM)
# GPIO 23 & 24 set up as inputs. One pulled up, the other down.
# 23 will go to GND when button pressed and 24 will go to 3V3 (3.3V)
# this enables us to demonstrate both rising and falling edge detection
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.output(19,GPIO.LOW)
GPIO.output(26,GPIO.HIGH)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #defining intrrupt as input with pullup resistor
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #defining PIR1 pin a input with pulldown resistor
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #defining PIR2 pin a input with pulldown resistor
time_stamp2 = time.time() #inititalize time_stamp variable with current system time
time_stamp1 = time.time()

# now we'll define the threaded callback function
# this will run in another thread when our event is detected
count = 0
def my_callback(channel):
    global time_stamp1
    global count
    time_now = time.time()
    if (time_now - time_stamp1) >= 0.3 :
        count = count + 1
        print "Rising edge detected on port 24 - even though, in the main thread,"
        print "we are still waiting for a falling edge - how cool?\n"
        print count
        pushMessage("Alert", " Something detected  "+ str(count))
        GPIO.output(13,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(13,GPIO.LOW)
    time_stamp1 = time_now
print "Make sure you have a button connected so that when pressed"
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"
print "You will also need a second button connected so that when pressed"
print "it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)"
raw_input("Press Enter when ready\n>")

def PIR2_callback(channel):
    global time_stamp2
    global count
    time_now = time.time()
    if (time_now - time_stamp2) >= 0.3 :
        count = count + 1
        print "PIR 2 detected something"
        print "we are still waiting for a falling edge - how cool?\n"
        print count
        pushMessage("Alert", " PIR2 detected "+ str(count))
        GPIO.output(13,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(13,GPIO.LOW)
    time_stamp2 = time_now
print "Make sure you have a button connected so that when pressed"
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"
print "You will also need a second button connected so that when pressed"
print "it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)"
raw_input("Press Enter when ready\n>")


# The GPIO.add_event_detect() line below set things up so that
# when a rising edge is detected on port 24, regardless of whatever
# else is happening in the program, the function "my_callback" will be run
# It will happen even while the program is waiting for
# a falling edge on the other button.
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback)
GPIO.add_event_detect(25, GPIO.RISING, callback=PIR2_callback)

try:
    print "Waiting for falling edge on port 23"
    GPIO.wait_for_edge(23, GPIO.FALLING)
    print "Falling edge detected. Here endeth the second lesson."
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
pushMessage("SERVER GOING DOWN", "Good Bye")
GPIO.cleanup()           # clean up GPIO on normal exit
