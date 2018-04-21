#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time, sys, signal

hist = {}

def exit(signum, frame):
  global hist
  with open('hist', 'w+') as f:
    f.writelines(["[{},{}]".format(k,v) for k,v in hist.items()])
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGTERM, exit)
  signal.signal(signal.SIGINT, exit)
  us = ev3.UltrasonicSensor('in4')
  i = us.distance_centimeters
  while True:  
    i = us.distance_centimeters
    hist[i] = hist[i] + 1 if i in hist else 1
    print("({}) ({})".format(len(hist), hist[i]))
    if len(hist) > 2000 or hist[i] > 5000:
      exit(None, None)
    time.sleep(0.05)