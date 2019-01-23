#!/usr/bin/python

import keypad16
import time

kpd = keypad16.keypad_module(0x38)

while True: 
    key = kpd.getch()
    print(key)
        