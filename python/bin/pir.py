#!/usr/bin/python

import smbus


class pir_module:
    I2CADDR    = 0x1f
    i2c = smbus.SMBus(0)
    
    def pirState(self):
        state = self.i2c.read_byte(self.I2CADDR)
        if ( state == 0x30 ):
            return False
        elif ( state == 0x31 ):
            return True
            
        
    def __init__(self,addr):
        self.I2CADDR = addr
    
    
    


