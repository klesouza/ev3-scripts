#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

if __name__ == "__main__":
  us = ev3.UltrasonicSensor('in4')
  i = us.distance_centimeters
  n = us.distance_centimeters
  while True:
    if abs(n-i) > 40:
      for i in range(2):   
        ev3.Sound.speak("Surprise!", 
        espeak_opts="-a 100 -s 130").wait()
        time.sleep(2)  
      time.sleep(10)
    n = us.distance_centimeters