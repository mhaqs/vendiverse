#!/usr/bin/python
#
# keypad_mega8.py
#

import smbus
import time

class keypad_module:

  I2CADDR    = 0x10     # valid range is 0x20 - 0x27
  
  i2c = smbus.SMBus(0) 
  released = False
  
  leds = 0x00
  
  NUMERICS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
  
  def isNum(self, key):
    return (key in self.NUMERICS)
  
  # get a keystroke from the keypad
  def getch(self):
    while 1:
      key = chr(self.i2c.read_byte(self.I2CADDR));
      if ( key == '-' ):
        self.released = True
        return '_'
      elif ( key == 'P' ):
        self.released = True
        return key
      elif ( self.released ):
        self.released = False
        return key
        
      
      time.sleep(0.1)     
        #if (key) != 0b1111:
        #  row = self.DECODE[key]
        #  while (self.i2c.read_byte_data(self.I2CADDR, self.GPIOA+self.port) >> 4) != 15:
        #   time.sleep(0.01)
        #  if self.UPSIDEDOWN == 0:
        #    return self.KEYCODE[col][row] # keypad right side up
        #  else:
        #    return self.KEYCODE[3-row][3-col] # keypad upside down

        
  def led(self, num, val):
    if ( val ):
       mask = 0x01
       mask = mask << num
       self.leds = self.leds | mask
       self.i2c.write_byte(self.I2CADDR, self.leds)
    else:
       mask = 0x01
       mask = mask << num
       mask = ~mask
       self.leds = self.leds & mask
       self.i2c.write_byte(self.I2CADDR, self.leds)

  # initialize the keypad class
  def __init__(self,addr):
    self.I2CADDR = addr
    self.i2c.write_byte(self.I2CADDR, self.leds)
    
# test code
def main(): 
  keypad = keypad_module(0x10)  
  while 1:
    ch = keypad.getch()
    print ch
    time.sleep(0.1)

    if ch == 'D':
      exit()

# don't runt test code if we are imported
if __name__ == '__main__':
  main()
