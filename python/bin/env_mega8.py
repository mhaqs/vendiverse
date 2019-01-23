#!/usr/bin/python
#
# env_mega8.py
#

import smbus
import time

class env_module:

  I2CADDR    = 0x11     # valid range is 0x20 - 0x27
  
  i2c = smbus.SMBus(0) 
  
  coolerStarted = False
  powered = False
  auxOpen = False
  fanOpen = False
  
  def __init__(self,addr):
    self.I2CADDR = addr
    self.powerUp()
    self.stopCooler()
    self.closeAux()
    self.openFan()
    
  def getTemp1(self):
    temps = self.i2c.read_i2c_block_data(self.I2CADDR, 0, 2);
    return temps[0]
    
  def getTemp2(self):
    temps = self.i2c.read_i2c_block_data(self.I2CADDR, 0, 2);
    return temps[1]
    
  def powerUp(self):
    self.powered = True
    self.i2c.write_byte(self.I2CADDR, 0x83)

  def powerDown(self):
    self.powered = False
    self.i2c.write_byte(self.I2CADDR, 0x03)
  
  def getPower(self):
    return self.powered
    
  def startCooler(self):
    self.coolerStarted = True
    self.i2c.write_byte(self.I2CADDR, 0x84)

  def stopCooler(self):
    self.coolerStarted = False
    self.i2c.write_byte(self.I2CADDR, 0x04)
  
  def getCooler(self):
    return self.coolerStarted
    
  def openAux(self):
    self.auxOpen = True
    self.i2c.write_byte(self.I2CADDR, 0x85)

  def closeAux(self):
    self.auxOpen = False
    self.i2c.write_byte(self.I2CADDR, 0x05)
  
  def getAux(self):
    return self.auxOpen
    
  def openFan(self):
    self.fanOpen = True
    self.i2c.write_byte(self.I2CADDR, 0x86)

  def closeFan(self):
    self.fanOpen = False
    self.i2c.write_byte(self.I2CADDR, 0x06)
  
  def getFan(self):
    return self.fanOpen
    
# test code
def main(): 
  env = env_module(0x11)  
  while 1:
    print(env.getTemp1())
    print(env.getTemp2()) 
    time.sleep(2)

# don't runt test code if we are imported
if __name__ == '__main__':
  main()
