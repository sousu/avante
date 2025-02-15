#!/usr/bin/python
#coding:utf-8

import pigpio
import time

class Servo():
    # PWM config: 
    #  50hz->20ms 
    #  1.1ms-1.45ms-1.8ms
    #  5.5%(-1.75)-7.25%-9%(+1.75)
    p = 3  # GPIO_3 not pin_num

    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(Servo.p,pigpio.OUTPUT)

    def angle(self,dgree):
        if dgree < -44 or 44 < dgree:
            return 
        self.pi.set_servo_pulsewidth(Servo.p,1450+350*dgree/45)

    def stop(self):
        self.pi.set_servo_pulsewidth(Servo.p,1450)
        time.sleep(1.0)
        self.pi.set_servo_pulsewidth(Servo.p,0)

# debug
if __name__ == '__main__':
    sv = Servo()
    try:
        while True:
            sv.angle(float(input()))
    except KeyboardInterrupt:
        sv.stop()

