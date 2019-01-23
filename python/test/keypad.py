#!/usr/bin/python

import smbus
from time import sleep

i2c = smbus.SMBus(0) 

while 1:
    print(chr(i2c.read_byte(0x10)))
    sleep(0.1)
