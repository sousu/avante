#!/usr/bin/python
#coding:utf-8

import RPi.GPIO as GPIO    
import time

class Motor():
    # PWM config: 
    #  50hz->20ms 
    #  1.1ms-1.45ms-1.8ms
    #  5.5%(-2.00)-7.25%-9%(+1.75)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4,GPIO.OUT)
        self.mt = GPIO.PWM(4,50)
        self.mt.start(0.0)
        self.mt.ChangeDutyCycle(7.25)

    def accelerate(self,pw):
        if pw < 0 or 100 < pw:
            return 
        self.mt.ChangeDutyCycle(7.25+(-2.00)*pw/100)
        time.sleep(0.1)

    def back(self,pw):
        if pw < 0 or 20 < pw:
            return 
        self.mt.ChangeDutyCycle(7.25+(2.00)*pw/100)
        time.sleep(0.1)
    
    def free(self,pw):
        self.mt.ChangeDutyCycle(7.25+(-2.00)*pw/100)
        time.sleep(0.1)

    def stop(self):
        self.mt.ChangeDutyCycle(7.25)
        time.sleep(0.5)
        self.mt.stop()

# debug
if __name__ == '__main__':
    mt = Motor()
    try:
        while True:
            #mt.accelerate(float(input()))
            mt.free(float(input()))

    except KeyboardInterrupt:
        mt.stop()
        GPIO.cleanup()
