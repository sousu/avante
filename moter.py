#!/usr/bin/python
#coding:utf-8

import RPi.GPIO as GPIO    
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

moter = GPIO.PWM(4,50)
moter.start(0.0)

# 50hz 20ms 1.1ms-1.45ms-1.8ms
#     5.5%(-1.75)-7.25%-9%(+1.75)
def handle(moter,dgree):
    if dgree < -44 or 44 < dgree:
        return 
    p = 7.25+1.75*dgree/45
    print(p)
    moter.ChangeDutyCycle(p)
    time.sleep(0.8)

try:
    print("input dgree")
    while True:
        handle(moter,float(input()))

except KeyboardInterrupt:
    moter.ChangeDutyCycle(7.25)
    time.sleep(0.8)
    moter.stop()
    GPIO.cleanup()


