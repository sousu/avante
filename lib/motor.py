#!/usr/bin/python
#coding:utf-8

import pigpio
import time

class Motor():
    # PWM config: 
    #  50hz->20ms 
    p = 4
    c = 1520 # center 15.2ms
    b = 25 # back limit

    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(Motor.p,pigpio.OUTPUT)
        time.sleep(0.1)
        self.pi.set_servo_pulsewidth(Motor.p,Motor.c)

    def accelerate(self,pw):
        if pw < 0 or 100 < pw:
            return 
        self.pi.set_servo_pulsewidth(Motor.p,Motor.c+(-350)*pw/100)

    def back(self,pw):
        if pw < 0 or 100 < pw:
            return 
        if Motor.b < pw:
            pw = Motor.b
        self.pi.set_servo_pulsewidth(Motor.p,Motor.c+(350)*pw/100)
        #time.sleep(0.01)
    
    def move(self,pw):
        if pw < Motor.b*(-1):
            pw = Motor.b*(-1)
        self.pi.set_servo_pulsewidth(Motor.p,Motor.c+(-350)*pw/100)
        #time.sleep(0.01)

    def stop(self):
        self.pi.set_servo_pulsewidth(Motor.p,Motor.c)
        time.sleep(1.0)
        self.pi.set_servo_pulsewidth(Motor.p,0)

# debug
if __name__ == '__main__':
    mt = Motor()
    try:
        while True:
            #mt.back(float(input()))
            mt.move(float(input()))
    except KeyboardInterrupt:
        mt.stop()

