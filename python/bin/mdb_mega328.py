#!/usr/bin/python
#
# mdb_mega328.py
#

import serial
import time
from decimal import *

class mdb_module:
  DEVADDR = "/dev/ttyS1" 
  
  bill = 0
  
  ser = serial.Serial( \
    port = DEVADDR,
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0 )
    
#  try: 
#    ser.open()
#  except Exception, e:
#    print "error open serial port: " + str(e 
#    #exit()
  
  def __init__(self,addr):
    self.DEVADDR = addr
    if self.ser.isOpen():
        print("Serial opened.");
        self.ser.write("-") 
    
  def stackBill(self):
    self.ser.write("B.ST-")
    counter = 0
    self.bill = 0
    while True:
        line = self.ser.readline()
        if ( line.startswith("B.DEP:")):
            break
        else:
            counter = counter + 1
        time.sleep(0.1)
        if ( counter > 20 ):
            print("Bill stack timed out.")
            break
    
  def getCoin(self):
    line = self.ser.readline()
    if ( line.startswith("C.D100")):
        return 1.00
    elif ( line.startswith("C.D50")):
        return 0.50
    elif ( line.startswith("C.D25")):
        return 0.25
    elif ( line.startswith("B.DEP:")):
        self.bill = Decimal(line[8:])
        return self.bill
    elif ( line.startswith("C.PO")):
        return "P"
    else:
        return "-"
        
  def getTubes(self):
    self.ser.reset_input_buffer()
    cmd = "C.TC-"
    print(cmd)
    coins = { "C100" : 0, "C50" : 0, "C25" : 0 }
    self.ser.write(cmd)
    time.sleep(0.1)
    self.ser.read(len(cmd)) # Read echo
    completed = False
    count = 0
    timeOut = 0
    while ( not completed ):
        line = self.ser.readline()
        line = line.strip()
        if (len(line) > 0 ):
            count = count + 1
            print("%s %s" % (count, line))
            if ( line.startswith("C.TC:100:")):
                coins["C100"] = int(line[9:])
            elif ( line.startswith("C.TC:050:")):
                coins["C50"] = int(line[9:])
            elif ( line.startswith("C.TC:025:")):
                coins["C25"] = int(line[9:])
        
        if ( count == 3):
            completed = True
            
        timeOut = timeOut + 1
        if ( timeOut > 50 ):
            return False
        time.sleep(0.1)
            
    return coins

  def dispense(self, amount):
    c100 = 0;
    c50 = 0;
    c25 = 0;
    
    if ( self.bill > 0 ):
        self.ser.write("B.ES-")
        while True:
            line = self.ser.readline()
            if ( line.startswith("B.DEP:") ):
                break
        amount = amount - self.bill
        self.bill = 0
    
    while (amount >= 1 ):
        c100 = c100 + 1
        amount = amount - Decimal(1)
    while (amount >= 0.50 ):
        c50 = c50 + 1
        amount = amount - Decimal(0.50)
    while (amount > 0 ):
        c25 = c25 + 1
        amount = amount - Decimal(0.25)
        
    if ( c100 > 0 ):
        cmd = "C.D:%s:100-" % str(c100).zfill(2)
        print(cmd)
        self.ser.write(cmd)
        self.ser.read(len(cmd))
        dispCompleted = False
        timeOut = 0
        while ( not dispCompleted ):
            line = self.ser.readline()
            #print(line)
            line = line.strip()
            if ( line.endswith("C.READY")):
                print(line)
                print("Coin dispense completed.")
                dispCompleted = True
            timeOut = timeOut + 1
            if ( timeOut > 50 ):
                break
            time.sleep(0.5)
    
    if ( c50 > 0 ):
        cmd = "C.D:%s:050-" % str(c50).zfill(2)
        print(cmd)
        self.ser.write(cmd)
        self.ser.read(len(cmd))
        dispCompleted = False
        timeOut = 0
        while ( not dispCompleted ):
            line = self.ser.readline()
            #print(line)
            line = line.strip()
            if ( line.endswith("C.READY")):
                print(line)
                print("Coin dispense completed.")
                dispCompleted = True
            timeOut = timeOut + 1
            if ( timeOut > 50 ):
                break
            time.sleep(0.1)
    
    if ( c25 > 0 ):
        cmd = "C.D:%s:025-" % str(c25).zfill(2)
        print(cmd)
        self.ser.write(cmd)
        self.ser.read(len(cmd))
        dispCompleted = False
        timeOut = 0
        while ( not dispCompleted ):
            line = self.ser.readline()
            #print(line)
            line = line.strip()
            if ( line.endswith("C.READY")):
                print(line)
                print("Coin dispense completed.")
                dispCompleted = True
            timeOut = timeOut + 1
            if ( timeOut > 50 ):
                break
            time.sleep(0.1)
            
# test code
def main(): 
  mdb = mdb_module("/dev/ttyS1")  
  while 1:
    print mdb.getCoin()
    time.sleep(0.1)

# don't runt test code if we are imported
if __name__ == '__main__':
  main()
