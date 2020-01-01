#!/usr/bin/python
#coding:utf-8

import time
import RPi.GPIO as GPIO    
from bottle import route,run,template,static_file

import sys
sys.path.append('./lib')
import servo
import motor

args = sys.argv
if not len(args) == 3:
    print('usage avante.py <address> <port>')
    quit()

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
    sv.angle(float(v[0]))
    return 

#--- ---
try:
    run(host=args[1],port=args[2])
except Exception as e:
    print(e)
    pass
finally:
    print('..Cleanup')
    sv.stop()
    mt.stop()
    GPIO.cleanup()
    quit()

