#!/usr/bin/python
#
# keypad_mega8.py
#

import smbus
import time

class motor_module:

  I2CADDR    = 0x19     # valid range is 0x20 - 0x27
  
  i2c = smbus.SMBus(1) 
  released = False
  quarters = []
  
  def startMotor(self, tray, motor):
    print("Starting motor %s on tray %s" % (motor, tray))
    print("Sending I2C : %s" % str(self.I2CADDR + tray))
    mKey = str(tray) + "-" + str(motor)
    if ( mKey in self.quarters ):
        self.startMotorQuarter(tray, motor)
        return
    start = 0b10000000
    cmd = start | motor
    self.i2c.write_byte(self.I2CADDR + tray, cmd)
    
  def startMotorQuarter(self, tray, motor):
    print("Starting motor %s on tray %s" % (motor, tray))
    print("Sending I2C : %s" % str(self.I2CADDR + tray))
    start = 0b00000000 
    cmd = start | motor
    self.i2c.write_byte(self.I2CADDR + tray, cmd)
    mKey = str(tray) + "-" + str(motor)
    if ( mKey not in self.quarters ):
        self.quarters.append(mKey)
    else:
        self.quarters.remove(mKey)

  def stopMotor(self, motor):
    start = 0b00000000
    cmd = start | motor
    self.i2c.write_byte(self.I2CADDR + tray, cmd)
  
  # initialize the keypad class
  def __init__(self,addr):
    self.I2CADDR = addr
    
# test code
def main(): 
  motor = motor_module(0x10)  
  while 1:
    print '-'
    time.sleep(0.5)

# don't runt test code if we are imported
if __name__ == '__main__':
  main()
