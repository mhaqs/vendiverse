# -*- coding: utf-8 -*-

import I2C_LCD_driver
#from time import time, sleep
import time

mylcd = I2C_LCD_driver.lcd()

#while True:
#    mylcd.lcd_display_string("Hello world!")
#    sleep(0.1)
#    mylcd.lcd_clear()
#    sleep(0.1)

while True:
    mylcd.lcd_display_string("MACGAL OTOMAT M100-S")
    mylcd.lcd_display_string("%s" %time.strftime("%H:%M:%S  %m/%d/%Y"), 2)
