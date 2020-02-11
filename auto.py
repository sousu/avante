#!/usr/bin/python
#coding:utf-8

import sys
sys.path.append('./lib')
import tracker
import servo

args = sys.argv
if not len(args) == 2:
    print('usage auto.py <jnldir>')
    quit()

sv = servo.Servo()
tr = tracker.Tracker(args[1])
def handle(angle):
    sv.angle(int(angle))

try:
    tr.track(handle)
except Exception as e:
    print('..ERR')
    print(e)
finally:
    print('..Cleanup')
    sv.stop()
    quit()

