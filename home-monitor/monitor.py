#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time, sys, signal
import datetime
import json, re

class Bufferize:
  def __init__(self,buffer_size=None):
    self.collection = []
    self.buffer_size = buffer_size or 300

  def write_item(self, item):
    self.collection.append(item)
    if len(self.collection) > self.buffer_size:
      self.flush()
  
  def flush(self):
    # self.file_flusher()
    self.udp_flusher()
    del self.collection[:]
  
  def file_flusher(self):
    date=re.sub('[^0-9]', '', datetime.datetime.utcnow().isoformat())
    with open("monitor-hist-{date}.json".format(date=date), "w+") as f :
      f.writelines([x+'\n' for x in self.collection])

  def udp_flusher(self):
    import socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto("\n".join(self.collection).encode('utf-8'), ("10.42.0.1", 9876))

buf = Bufferize()

def exit(signum, frame):
  buf.flush()
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
    buf.write_item(
      '{{"ts": {ts},"ultrasonic": {dist},"motor_pos": {pos},"light": {light} }}'\
      .format(ts=ts, dist=us.distance_centimeters, pos=motor.position,light=ls.ambient_light_intensity)
    )
    if (rot == -1 and motor.position <= 0) or (rot == 1 and motor.position >= 360):
      rot = rot*-1
    
    motor.run_timed(time_sp=500, speed_sp=(rot)*30)