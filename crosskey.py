#!/usr/bin/python
#coding:utf-8

#import RPi.GPIO as GPIO    
import time

import sys
sys.path.append('./lib')
import servo
import motor

sv = servo.Servo()
mt = motor.Motor()

def getch():
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,termios.TCSADRAIN,old)

cur = 0
back = False
try:
    while True:
        key = ord(getch())
        print(key)
        if key == 27:
            print("ESC")
            raise 
        if key == 106:
            if not cur == 106:
                sv.angle(0)
                cur = 106
            else:
                sv.angle(-30)
        if key == 108:
            if not cur == 108:
                sv.angle(0)
                cur = 108
            else:
                sv.angle(30)
        if key == 105:
            if back:
                mt.accelerate(0)
                back=False
            else:
                mt.accelerate(22)
        if key == 107:
            if not back:
                mt.back(0)
                back=True
            else:
                mt.back(15)

except Exception as e:
    print(e)
finally:
    sv.stop()
    mt.stop()
    #GPIO.cleanup()

