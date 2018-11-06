#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time, sys, signal
import datetime
import json

hist = []

def exit(signum, frame):
  global hist
  with open('monitor-hist.json', 'w+') as f:
    json.dump(hist, f)
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGTERM, exit)
  signal.signal(signal.SIGINT, exit)
  us = ev3.UltrasonicSensor('in3')
  motor = ev3.LargeMotor('outD')
  ls = ev3.ColorSensor('in4')
  ls.mode = ev3.ColorSensor.MODE_COL_AMBIENT
  rot = 1 if motor.position <= 360 else -1
  while True:  
    ts = datetime.datetime.utcnow().isoformat()
    hist.append({
      "ts": ts,
      "ultrasonic": us.distance_centimeters,
      "motor_pos": motor.position,
      "light": ls.ambient_light_intensity
    })
    if (rot == -1 and motor.position <= 0) or (rot == 1 and motor.position >= 360):
      rot = rot*-1
    
    motor.run_timed(time_sp=500, speed_sp=(rot)*30)
    #TODO: flush results / send to pubsub or GCS
    if len(hist) > 3000:
      exit(None, None)

    