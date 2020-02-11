#!/usr/bin/python
#coding:utf-8

import time
from bottle import route,run,template,static_file
#import RPi.GPIO as GPIO    

import sys
sys.path.append('./lib')
import servo
import motor

args = sys.argv
if not len(args) == 3:
    print('usage rc.py <address> <port>')
    quit()

c = ['']*2
sv = servo.Servo()
mt = motor.Motor()

@route('/')
def index():
    return template('ctl')

@route('/res/<path>')
def index(path):
    return static_file(path,root='./res')

@route('/state/<val>')
def index(val='0_0'):
    v = val.split('_')
    if not c[0] == v[0]:
        sv.angle(float(v[0]))
        c[0] = v[0]
    if not c[1] == v[1]:
        mt.move(float(v[1]))
        c[1] = v[1]
    return 

try:
    run(host=args[1],port=args[2])
except Exception as e:
    print('..ERR')
    print(e)
finally:
    print('..Cleanup')
    sv.stop()
    mt.stop()
    #GPIO.cleanup()
    quit()

