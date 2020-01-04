#!/usr/bin/python
#coding:utf-8

import RPi.GPIO as GPIO    
import time

class Servo():
    # PWM config: 
    #  50hz->20ms 
    #  1.1ms-1.45ms-1.8ms
    #  5.5%(-1.75)-7.25%-9%(+1.75)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,GPIO.OUT)
        self.sv = GPIO.PWM(3,50)
        self.sv.start(0.0)

    def angle(self,dgree):
        if dgree < -44 or 44 < dgree:
            return 
        self.sv.ChangeDutyCycle(7.25+1.75*dgree/45)
        #time.sleep(0.01)

    def stop(self):
        self.sv.ChangeDutyCycle(7.25)
        time.sleep(0.5)
        self.sv.stop()

# debug
if __name__ == '__main__':
    sv = Servo()
    try:
        while True:
            sv.angle(float(input()))
    except KeyboardInterrupt:
        sv.stop()
        GPIO.cleanup()

