#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

if __name__ == "__main__":
  us = ev3.UltrasonicSensor('in3')
  # i = us.distance_centimeters
  # n = us.distance_centimeters
  while True:
    if us.distance_centimeters < 50:
      print(us.distance_centimeters)
      for i in range(1):   
        ev3.Sound.speak("Merry Christmas!", 
        espeak_opts="-a 100 -s 120").wait()
        time.sleep(2)  
      time.sleep(3)
    n = us.distance_centimeters