# -*- coding: utf-8 -*-
# Test

import sys, traceback
import I2C_LCD_driver
import time
import curses
import MySQLdb
import keypad_mega8
import env_mega8
import mdb_mega328
import motor_mega8
from decimal import *
from time import sleep
import MFRC522
# import pir
import subprocess

MIFAREReader = MFRC522.MFRC522()

connection = None
mysqlConnected = False
while not mysqlConnected:
    try:
        connection=MySQLdb.connect(host='localhost',user='vendiverse',passwd='vendiverse',db='vendiverse')
        mysqlConnected = True
    except MySQLdb.Error, e:
        print("Can not connect MySQL Server.")
    sleep(2)

mylcd = I2C_LCD_driver.lcd()

kpd = keypad_mega8.keypad_module(0x10)
env = env_mega8.env_module(0x11)
sleep(5)
mdb = mdb_mega328.mdb_module("/dev/ttyS1")
motor = motor_mega8.motor_module(0x1F)

# pir = pir.pir_module(0x1f)

#while True:
#    mylcd.lcd_display_string("Hello world!")
#    sleep(0.1)
#    mylcd.lcd_clear()
#    sleep(0.1)

def play(audio_file_path):
    subprocess.Popen(["ffplay", "-nodisp", "-autoexit", audio_file_path])

def setDate(day, month, year):
    subprocess.Popen(["date", "+%Y%m%d", "-s", "%4s%2s%2s" % (year, str(month).zfill(2), str(day).zfill(2))])
    subprocess.Popen(["hwclock", "-f", "/dev/rtc1", "-w"])
    
def setTime(hour, minute, second):
    subprocess.Popen(["date", "+%T", "-s", "%s:%s:%s" % (str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2))])
    subprocess.Popen(["hwclock", "-f", "/dev/rtc1", "-w"])
    
def displayLogo():
    subprocess.Popen(["fbi", "-T", "1", "-a", "/home/eliverse/res/logo.png"])

vendiverseMenu = [ \
    { 'key' : 1,
      'name' : 'CHANGE PRICES',
      'sub' : [ \
        {  'key' : 1,
           'name' : 'CHANGE BY SHELF',
           'fn' : 'a11' },
        {  'key' : 2,
           'name' : 'CHANGE BY PRODUCT',
           'fn' : 'a12' } ] },
    { 'key' : 2,
      'name' : 'SALES & REFILL',
      'sub' : [ \
        {  'key' : 1,
           'name' : 'SHELF TOTAL',
           'fn' : 'a21' },
        {  'key' : 2,
           'name' : 'TRAY TOTAL',
           'fn' : 'a22' },
        {  'key' : 3,
           'name' : 'REFILL',
           'sub' : [ \
                {  'key' : 1,
                   'name' : 'REFILL SHELF',
                   'fn' : 'a231' },
                {  'key' : 2,
                   'name' : 'REFILL TRAY',
                   'fn' : 'a232' },
                {  'key' : 3,
                   'name' : 'REFILL ALL',
                   'fn' : 'a233' }
           ] } ] },
    { 'key' : 3,
      'name' : 'MONEY REPORT',
      'sub' : [ \
        {  'key' : 1,
           'name' : 'COINS IN TUBES',
           'fn' : 'a31' },
        {  'key' : 2,
           'name' : 'COINS IN CASHBOX',
           'fn' : 'a32' },
        {  'key' : 3,
           'name' : 'TOTAL CHANGE',
           'fn' : 'a33' },
        {  'key' : 4,
           'name' : 'TOTAL OF COINS',
           'fn' : 'a34' },
        {  'key' : 5,
           'name' : 'TOTAL OF BILLS',
           'fn' : 'a35' },
        {  'key' : 6,
           'name' : 'TOTAL CARD SALE',
           'fn' : 'a36' },
        {  'key' : 7,
           'name' : 'TOTAL DISCOUNT SALE',
           'fn' : 'a37' } ] },
    { 'key' : 4,
      'name' : 'REPORTS',
      'sub' : [ \
        {  'key' : 1,
           'name' : 'BY HOURS',
           'fn' : 'a41' },
        {  'key' : 2,
           'name' : 'BY DAYS',
           'fn' : 'a42' },
        {  'key' : 3,
           'name' : 'BY MONTHS',
           'fn' : 'a43' },
        {  'key' : 4,
           'name' : 'TOP PRODUCTS',
           'fn' : 'a44' },
        {  'key' : 5,
           'name' : 'TOP SHELVES',
           'fn' : 'a45' },
        {  'key' : 6,
           'name' : 'TOP TRAYS',
           'fn' : 'a46' },
        {  'key' : 7,
           'name' : 'WORST PRODUCTS', 
           'fn' : 'a47' },
        {  'key' : 8,
           'name' : 'WORST SHELVES',
           'fn' : 'a48' },
        {  'key' : 9,
           'name' : 'WORST TRAYS',
           'fn' : 'a49' } ] },
    { 'key' : 5,
      'name' : 'SYSTEM CONFIGURATION',
      'sub' : [ \
        {  'key' : 1,
           'name' : 'TIME',
           'fn' : 'a51' },
        {  'key' : 2,
           'name' : 'DATE',
           'fn' : 'a52' },
        {  'key' : 3,
           'name' : 'TEMPERATURE',
           'fn' : 'a53' },
        {  'key' : 4,
           'name' : 'SALES',
           'fn' : 'a54' },
        {  'key' : 5,
           'name' : 'COUNTERS',
           'fn' : 'a55' },
        {  'key' : 6,
           'name' : 'SOFTWARE UPDATE',
           'fn' : 'a56' },
        {  'key' : 7,
           'name' : 'SECURITY',
           'fn' : 'a57' },
        {  'key' : 8,
           'name' : 'ENERGY SAVING',
           'fn' : 'a58' },
        {  'key' : 9,
           'name' : 'FACTORY DEFAULTS',
           'fn' : 'a59' } ] },
    { 'key' : 6,
      'name' : 'CONTROL & TEST', 
      'sub' : [ \
        {  'key' : 1,
           'name' : 'COOLER FAN',
           'fn' : 'a61' },
        {  'key' : 2,
           'name' : 'COOLER COMPRESSOR',
           'fn' : 'a62' },
        {  'key' : 3,
           'name' : '24V SUPPLY',
           'fn' : 'a63' },
        {  'key' : 4,
           'name' : 'AUXILLARY RELAY',
           'fn' : 'a64' },
        {  'key' : 5,
           'name' : 'BOARD LEDS',
           'fn' : 'a65' },
        {  'key' : 6,
           'name' : 'TEMPERATURE',
           'fn' : 'a66' },
        {  'key' : 7,
           'name' : 'VENDING MOTORS',
           'fn' : 'a67' }] } ]
          
currentMenu = vendiverseMenu
previousMenu = vendiverseMenu

def a11(win):
    redraw = 1
    selectedShelf = ''
    previousShelf = ''
    leftover = ''
    count = 0
    lMode = False
    lcdClear = True
    row = {}
    pName = ''
    
    while True:
        if ( redraw == 1 ):
            if ( lcdClear ):
                mylcd.lcd_clear()
            
            mylcd.lcd_display_string('Raf No: %2s' % selectedShelf,1)

            if ( len(selectedShelf) == 2 ):
                if ( selectedShelf != previousShelf ):
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("SELECT product.name, shelf.id as shelf_id, shelf.product_id, product.price, product.vat FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % selectedShelf)
                    row = cursor.fetchone()
                    cursor.close()
                    previousShelf = selectedShelf
                
                pName = row['name']
                
                if ( len(pName) > 20 ):
                    leftover = pName[20:]
                    pName = pName[:20]
                else:
                    leftover = pName
                
                if ( lMode ):
                    mylcd.lcd_display_string("%-20s" % leftover, 2)
                else:
                    mylcd.lcd_display_string("%-20s" % pName, 2)
            redraw = 0
            
        key = kpd.getch()
        if ( kpd.isNum(key) ):
            if ( len(selectedShelf) == 2 ):
                selectedShelf = ''
                lcdClear = True
            selectedShelf = selectedShelf + key
            redraw = 1
        elif ( key == 'D' ):
            return
        elif ( key == '#' and len(selectedShelf) == 2):
            newPrice = 0.0
            mylcd.lcd_display_string("%-20s" % pName, 2)
            mylcd.lcd_display_string("Old Price:  %5.2f TL" % row['price'],3)
            mylcd.lcd_display_string("New Price:  %5.2f TL" % newPrice, 4)
            digit = 0
            priceCompleted = False
            while True:
                nKey = kpd.getch()
                if ( kpd.isNum(nKey) ):
                    if ( digit > 0 ):
                        newPrice = newPrice * 10
                    newPrice = newPrice + (0.01 * int(nKey))
                    mylcd.lcd_display_string("New Price:  %5.2f TL" % newPrice, 4)
                    digit += 1
                    if ( digit == 4 ):
                        priceCompleted = True
                elif ( nKey == '#' ):
                    priceCompleted = True
                
                if ( priceCompleted ):
                    cursor = connection.cursor()
                    cursor.execute("UPDATE product SET price=%s WHERE id=%s", (newPrice, row['product_id']))
                    connection.commit()
                    selectedShelf = ''
                    lcdClear = True
                    redraw = 1
                    break
                    
                sleep(0.1)
        
        count += 1
        if ( count > 10 ):
            count = 0
            lMode = not lMode
            redraw = 1
            lcdClear = False
        
        sleep(0.1)
        
def a12(win):
    redraw = 1
    selectedShelf = ''
    previousShelf = ''
    leftover = ''
    count = 0
    lMode = False
    lcdClear = True
    row = {}
    pName = ''
    
    while True:
        if ( redraw == 1 ):
            if ( lcdClear ):
                mylcd.lcd_clear()
            
            mylcd.lcd_display_string('Shelf No: %2s' % selectedShelf,1)

            if ( len(selectedShelf) == 2 ):
                if ( selectedShelf != previousShelf ):
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("SELECT product.name, shelf.id as shelf_id, shelf.product_id, product.price, product.vat FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % selectedShelf)
                    row = cursor.fetchone()
                    cursor.close()
                    previousShelf = selectedShelf
                
                pName = row['name']
                
                if ( len(pName) > 20 ):
                    leftover = pName[20:]
                    pName = pName[:20]
                else:
                    leftover = pName
                
                if ( lMode ):
                    mylcd.lcd_display_string("%-20s" % leftover, 2)
                else:
                    mylcd.lcd_display_string("%-20s" % pName, 2)
            redraw = 0
            
        key = kpd.getch()
        if ( kpd.isNum(key) ):
            if ( len(selectedShelf) == 2 ):
                selectedShelf = ''
                lcdClear = True
            selectedShelf = selectedShelf + key
            redraw = 1
        elif ( key == 'D' ):
            return
        elif ( key == '#' and len(selectedShelf) == 2):
            newProduct = ""
            mylcd.lcd_display_string("%-20s" % pName, 2)
            # mylcd.lcd_display_string("Eski Fiyat: %5.2f TL" % row['price'],3)
            mylcd.lcd_display_string("Yeni Urun: %s" % newProduct, 4)
            npCompleted = False
            while True:
                nKey = kpd.getch()
                if ( kpd.isNum(nKey) ):
                    newProduct = newProduct + nKey
                    mylcd.lcd_display_string("New Product: %s" % newProduct, 4)
                elif ( nKey == '#' ):
                    npCompleted = True
                
                if ( npCompleted ):
                    cursor = connection.cursor()
                    print(row["shelf_id"])
                    cursor.execute("UPDATE shelf SET product_id=%s WHERE id=%s", (newProduct, row['shelf_id']))
                    connection.commit()
                    selectedShelf = ''
                    lcdClear = True
                    redraw = 1
                    break
                    
                sleep(0.1)
        
        count += 1
        if ( count > 10 ):
            count = 0
            lMode = not lMode
            redraw = 1
            lcdClear = False
        
        sleep(0.1)
        
def a231(win):
    redraw = 1
    selectedShelf = ''
    previousShelf = ''
    leftover = ''
    count = 0
    lMode = False
    lcdClear = True
    row = {}
    pName = ''
    
    while True:
        if ( redraw == 1 ):
            if ( lcdClear ):
                mylcd.lcd_clear()
            
            mylcd.lcd_display_string('Shelf No : %2s' % selectedShelf,1)

            if ( len(selectedShelf) == 2 ):
                if ( selectedShelf != previousShelf ):
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("SELECT product.name, shelf.id as shelf_id, shelf.product_id, shelf.remaining FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % selectedShelf)
                    row = cursor.fetchone()
                    previousShelf = selectedShelf
                
                pName = row['name']
                
                if ( len(pName) > 20 ):
                    leftover = pName[20:]
                    pName = pName[:20]
                else:
                    leftover = pName
                
                if ( lMode ):
                    mylcd.lcd_display_string("%-20s" % leftover, 2)
                else:
                    mylcd.lcd_display_string("%-20s" % pName, 2)
                    
                mylcd.lcd_display_string("Current : %s" % row['remaining'], 3)
                mylcd.lcd_display_string("A) Refill   D) Exit", 4);
            redraw = 0
            
        key = kpd.getch()
        if ( kpd.isNum(key) ):
            if ( len(selectedShelf) == 2 ):
                selectedShelf = ''
                lcdClear = True
            selectedShelf = selectedShelf + key
            redraw = 1
        elif ( key == 'A' and len(selectedShelf) == 2 ):
            print("Shelf filled.")      
            cursor = connection.cursor()
            cursor.execute("UPDATE shelf SET remaining=capacity WHERE id='%s'" % selectedShelf);
            connection.commit()
            lcdClear = True
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
        
        count += 1
        if ( count > 10 ):
            count = 0
            lMode = not lMode
            redraw = 1
            lcdClear = False
        
        sleep(0.1)
    
def a232(win):
    redraw = 1
    rack = "  "
    pos = 0
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            
            mylcd.lcd_display_string("Tray  : %s" % rack, 1)
            mylcd.lcd_display_string("A) Refill   D) Exit", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( kpd.isNum(key)):
            rackL = list(rack)
            rackL[pos] = key
            rack = "".join(rackL)
            redraw = 1
            pos = pos + 1
            if ( pos > 1 ):
                pos = 0
            continue
        elif ( key == 'A'):
            cursor = connection.cursor()
            cursor.execute("UPDATE shelf SET remaining=capacity WHERE rack_id='%s'" % rack.strip());
            connection.commit()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  
        
def a233(win):
    redraw = 1
    vmc = "  "
    pos = 0
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            
            mylcd.lcd_display_string("Vender : %s" % vmc, 1)
            mylcd.lcd_display_string("A) Refill   D) Exit", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( kpd.isNum(key)):
            vmcL = list(vmc)
            vmcL[pos] = key
            vmc = "".join(vmcL)
            redraw = 1
            pos = pos + 1
            if ( pos > 1 ):
                pos = 0
            continue
        elif ( key == 'A'):
            cursor = connection.cursor()
            cursor.execute("UPDATE shelf SET remaining=capacity");
            connection.commit()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  


def a44(win):
    redraw = 1
    page = 1
    mode = False
    count = 0
    leftover = []
    lcdClear = True

    while True:
        
        if ( redraw == 1 ): 
            if ( lcdClear ):
                mylcd.lcd_clear()

            if ( not mode ):
                leftover = []
                cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT product.name, sl.total FROM (SELECT COUNT(*) AS total, product_id FROM sale GROUP BY product_id) sl LEFT JOIN product ON product.id=sl.product_id ORDER BY TOTAL DESC LIMIT %s,%s", (((page-1)*4), 4))
                rows = cursor.fetchall()
                
                line = 1
                for row in rows :
                    pName = row['name']

                    if ( len(pName) > 15 ):                    
                        leftover.append({'name' : pName[15:], 'total' : row['total']})
                        pName = pName[:15]
                    else:
                        leftover.append({'name' : pName, 'total' : row['total']})
                    
                    mylcd.lcd_display_string("%-15s %4s" % (pName[:15], row['total']), line)
                    line += 1
                redraw = 0
            else:
                line = 1
                for lo in leftover :
                    mylcd.lcd_display_string("%-15s %4s" % (lo['name'], lo['total']), line)
                    line += 1
                redraw = 0

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            lcdClear = True
            mode = False
            continue
        elif ( key == '#' and page < 6 ):
            page += 1
            redraw = 1
            lcdClear = True
            mode = False
            continue
        elif ( key == 'D' ):
            return

        count += 1
        if ( count > 10 ):
            count = 0
            mode = not mode 
            redraw = 1
            lcdClear = False
            
        sleep(0.1)
      
def a41(win):
    redraw = 1
    page = 1

    while True:
        
        if ( redraw == 1 ): 
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT _hour.h, IFNULL(slh.total, 0) as total FROM _hour LEFT JOIN (SELECT COUNT(*) as total, sl.h FROM (SELECT hour(sale_dt) as h FROM sale) sl GROUP BY sl.h) slh ON slh.h=_hour.h ORDER BY _hour.no LIMIT %s,%s", (((page-1)*4), 4))
            rows = cursor.fetchall()
            
            line = 1
            for row in rows :
                pName = "%-15s" % (str(row['h']) + ':00 - ' + str(row['h']) + ':59')
                mylcd.lcd_display_string("%s %4s" % (pName, row['total']), line)
                line += 1
            redraw = 0      

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            continue
        elif ( key == '#' and page < 6 ):
            page += 1
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
        
def a42(win):
    redraw = 1
    page = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT _day.d, IFNULL(slh.total, 0) as total FROM _day LEFT JOIN (SELECT COUNT(*) as total, sl.dow FROM (SELECT dayofweek(sale_dt) as dow FROM sale) sl GROUP BY sl.dow) slh ON slh.dow=_day.dow ORDER BY _day.no LIMIT %s,%s", (((page-1)*4), 4))
            rows = cursor.fetchall()
            
            line = 1
            for row in rows :
                pName = "%-15s" % str(row['d'])
                mylcd.lcd_display_string("%s %4s" % (pName, row['total']), line)
                line += 1
            redraw = 0      

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            continue
        elif ( key == '#' and page < 2 ):
            page += 1
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)

def a43(win):
    redraw = 1
    page = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT _month.m, IFNULL(slh.total, 0) as total FROM _month LEFT JOIN (SELECT COUNT(*) as total, sl.m FROM (SELECT month(sale_dt) as m FROM sale) sl GROUP BY sl.m) slh ON slh.m=_month.no ORDER BY _month.no LIMIT %s,%s", (((page-1)*4), 4))
            rows = cursor.fetchall()
            
            line = 1
            for row in rows :
                pName = "%-15s" % str(row['m'])
                mylcd.lcd_display_string("%s %4s" % (pName, row['total']), line)
                line += 1
            redraw = 0      

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            continue
        elif ( key == '#' and page < 3 ):
            page += 1
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  

def a21(win):
    redraw = 1
    page = 1
    mode = False
    count = 0
    leftover = []
    lcdClear = True

    while True:
        
        if ( redraw == 1 ): 
            if ( lcdClear ):
                mylcd.lcd_clear()

            if ( not mode ):
                leftover = []
                cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT id, p.name, remaining FROM shelf LEFT JOIN product p ON shelf.product_id=p.id ORDER BY id LIMIT %s,%s", (((page-1)*4), 4))
                rows = cursor.fetchall()
                
                line = 1
                for row in rows :
                    pName = row['name']

                    if ( len(pName) > 14 ):                    
                        leftover.append({'id' : row['id'], 'name' : pName[14:], 'remaining' : row['remaining']})
                        pName = pName[:14]
                    else:
                        leftover.append({'id' : row['id'], 'name' : pName, 'remaining' : row['remaining']})
                    
                    mylcd.lcd_display_string("%2s %-14s %2s" % (row['id'], pName[:14], row['remaining']), line)
                    line += 1
                redraw = 0
            else:
                line = 1
                for lo in leftover :
                    mylcd.lcd_display_string("%2s %-14s %2s" % (lo['id'], lo['name'], lo['remaining']), line)
                    line += 1
                redraw = 0

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            lcdClear = True
            mode = False
            continue
        elif ( key == '#' and page < 6 ):
            page += 1
            redraw = 1
            lcdClear = True
            mode = False
            continue
        elif ( key == 'D' ):
            return

        count += 1
        if ( count > 10 ):
            count = 0
            mode = not mode 
            redraw = 1
            lcdClear = False
            
        sleep(0.1)          
    
def a22(win):
    redraw = 1
    page = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT rack_id, SUM(remaining) as total FROM shelf GROUP BY (rack_id) LIMIT %s,%s", (((page-1)*4), 4))
            rows = cursor.fetchall()
            
            line = 1
            for row in rows :
                pName = "%-15s" % str(row['rack_id'])
                mylcd.lcd_display_string("%s %4s" % (pName, row['total']), line)
                line += 1
            redraw = 0      

        key = kpd.getch()
        if ( key == '*' and page > 1 ):
            page -= 1
            redraw = 1
            continue
        elif ( key == '#' and page < 2 ):
            page += 1
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
    
def a31(win):
    redraw = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            tubes = mdb.getTubes()
                
            mylcd.lcd_display_string("%-15s %4s" % ("1 TL", tubes["C100"]), 1)
            mylcd.lcd_display_string("%-15s %4s" % ("50 Kurus", tubes["C50"]), 2)
            mylcd.lcd_display_string("%-15s %4s" % ("25 Kurus", tubes["C25"]), 3)
            mylcd.lcd_display_string("(A) Refresh", 4)
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
  
def a51(win):
    redraw = 1
    newTime = "000000"
    pos = 0
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            
            mylcd.lcd_display_string("Current: %-12s" % time.strftime("%H:%M:%S"), 1)
            mylcd.lcd_display_string("New   : %2s:%2s:%2s" % (newTime[0:2], newTime[2:4], newTime[4:6]), 2)
            mylcd.lcd_display_string("A) Change  D) Back", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( kpd.isNum(key)):
            newTimeL = list(newTime)
            newTimeL[pos] = key
            newTime = "".join(newTimeL)
            redraw = 1
            pos = pos + 1
            if ( pos > 5 ):
                pos = 0
            continue
        elif ( key == 'A'):
            setTime(int(newTime[0:2]), int(newTime[2:4]), int(newTime[4:6]))
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  
        
def a52(win):
    redraw = 1
    newDate = "01012016"
    pos = 0
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            
            mylcd.lcd_display_string("Current: %-12s" % time.strftime("%d/%m/%Y"), 1)
            mylcd.lcd_display_string("New    :  %2s/%2s/%4s" % (newDate[0:2], newDate[2:4], newDate[4:8]), 2)
            mylcd.lcd_display_string("A) Change  D) Back", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( kpd.isNum(key)):
            newDateL = list(newDate)
            newDateL[pos] = key
            newDate = "".join(newDateL)
            redraw = 1
            pos = pos + 1
            if ( pos > 7 ):
                pos = 0
            continue
        elif ( key == 'A'):
            setDate(int(newDate[0:2]), int(newDate[2:4]), int(newDate[4:8]))
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
  
def a53(win):
    redraw = 1

    paramId = 11
    
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            param = getParamById(paramId)
            
            choice = ""
            if ( param['type'] == 1 ):
                yes = " "
                no = " "
                if ( param['value'] == '1' ):
                    yes = "X"
                else:
                    no = "X"
                choice = "[%s] OPEN [%s] CLOSED" % (yes, no)
            elif (param['type'] == 2 ):
                choice = "VALUE:%2s   A)+ B)-" % param['value']
            
            mylcd.lcd_display_string("%-2s)%-17s" % (param['id']-10, param['detail'][:17]), 1)
            mylcd.lcd_display_string("%-20s" % param['detail'][17:], 2)
            mylcd.lcd_display_string(choice, 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            setParamById(paramId, str(int(param['value']) + 1))
            redraw = 1
            continue
        elif ( key == 'B'):
            setParamById(paramId, str(int(param['value']) - 1))
            redraw = 1
            continue
        elif ( key == '#' ):
            paramId = paramId + 1
            if ( paramId > 15 ):
                paramId = 11
            redraw = 1
            continue
        elif ( key == '*' ):
            paramId = paramId - 1
            if ( paramId < 11 ):
                paramId = 15
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  
  
def a54(win):
    redraw = 1

    paramId = 1
    
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            param = getParamById(paramId)
            
            choice = ""
            if ( param['type'] == 1 ):
                yes = " "
                no = " "
                if ( param['value'] == '1' ):
                    yes = "X"
                else:
                    no = "X"
                choice = "[%s] OPEN  [%s] CLOSED" % (yes, no)
            
            mylcd.lcd_display_string("%-2s)%-17s" % (param['id'], param['detail'][:17]), 1)
            mylcd.lcd_display_string("%-20s" % param['detail'][17:], 2)
            mylcd.lcd_display_string(choice, 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            setParamById(paramId, '1')
            redraw = 1
            continue
        elif ( key == 'B'):
            setParamById(paramId, '0')
            redraw = 1
            continue
        elif ( key == '#' ):
            paramId = paramId + 1
            if ( paramId > 10 ):
                paramId = 1
            redraw = 1
            continue
        elif ( key == '*' ):
            paramId = paramId - 1
            if ( paramId < 1 ):
                paramId = 10
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)

  
def a61(win):
    redraw = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            sFan = env.getFan()
            strFan = ""
            if ( sFan ):
                strFan = "OPEN"
            else:
                strFan = "CLOSED"
                
            mylcd.lcd_display_string("COOLER FAN  : %s" % strFan, 1)
            mylcd.lcd_display_string("A: OPEN", 2)
            mylcd.lcd_display_string("B: CLOSE", 3)
            mylcd.lcd_display_string("D: EXIT", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            env.openFan()
            redraw = 1
            continue
        elif ( key == 'B'):
            env.closeFan()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
        
def a62(win):
    redraw = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            sCooler = env.getCooler()
            strCooler = ""
            if ( sCooler ):
                strCooler = "OPEN"
            else:
                strCooler = "CLOSED"
                
            mylcd.lcd_display_string("CLR. CMPR.: %s" % strCooler, 1)
            mylcd.lcd_display_string("A: OPEN", 2)
            mylcd.lcd_display_string("B: CLOSE", 3)
            mylcd.lcd_display_string("D: EXIT", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            env.startCooler()
            redraw = 1
            continue
        elif ( key == 'B'):
            env.stopCooler()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
        
def a63(win):
    redraw = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            sPower = env.getPower()
            strPower = ""
            if ( sPower ):
                strPower = "OPEN"
            else:
                strPower = "CLOSE"
                
            mylcd.lcd_display_string("24V POWER: %s" % strPower, 1)
            mylcd.lcd_display_string("A: OPEN", 2)
            mylcd.lcd_display_string("B: CLOSE", 3)
            mylcd.lcd_display_string("D: EXIT", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            env.powerUp()
            redraw = 1
            continue
        elif ( key == 'B'):
            env.powerDown()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
        
def a64(win):
    redraw = 1

    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            sAux = env.getAux()
            strAux = ""
            if ( sAux ):
                strAux = "OPEN"
            else:
                strAux = "CLOSE"
                
            mylcd.lcd_display_string("AUX RELAY : %s" % strAux, 1)
            mylcd.lcd_display_string("A: OPEN", 2)
            mylcd.lcd_display_string("B: CLOSE", 3)
            mylcd.lcd_display_string("D: EXIT", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( key == 'A' ):
            env.openAux()
            redraw = 1
            continue
        elif ( key == 'B'):
            env.closeAux()
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)
        
def a65(win):
    redraw = 1
    leds = [False, False, False, False]
    
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
                
            mylcd.lcd_display_string("LED 1 : %s" % leds[0], 1)
            mylcd.lcd_display_string("LED 2 : %s" % leds[1], 2)
            mylcd.lcd_display_string("LED 3 : %s" % leds[2], 3)
            mylcd.lcd_display_string("LED 4 : %s" % leds[3], 4)
            
            for num in range(0,4):
               kpd.led(num, leds[num])
            
            redraw = 0      

        key = kpd.getch()
        if ( key == '1' ):
            leds[0] = not leds[0]
            redraw = 1
            continue
        elif ( key == '2'):
            leds[1] = not leds[1]
            redraw = 1
            continue
        elif ( key == '3'):
            leds[2] = not leds[2]
            redraw = 1
            continue
        elif ( key == '4'):
            leds[3] = not leds[3]
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)

def checkCooler(win):
    temp1 = int(env.getTemp1());
    temp2 = int(env.getTemp2());
    
    maxTemp1 = int(getParamById(11)["value"]); #MAXTEMP1
    minTemp1 = int(getParamById(12)["value"]); #MINTEMP1
    maxTemp2 = int(getParamById(13)["value"]); #MAXTEMP2
    minTemp2 = int(getParamById(14)["value"]); #MINTEMP2
    
    if ( temp1 < minTemp1):
        print("Min. Temp1 reached.")
        env.stopCooler()
        sleep(3)
        env.closeFan()
    elif ( temp1 > maxTemp1):
        print("Max. Temp1 reached.")
        env.openFan()
        env.startCooler()
    elif ( temp2 < minTemp2):
        print("Min. Temp2 reached.")
        env.stopCooler()
        sleep(3)
        env.closeFan()
    elif ( temp2 > maxTemp2):
        print("Max. Temp2 reached.")
        env.openFan()
        env.startCooler()
        
def a66(win):
    redraw = 1
    count = 0
    
    while True:
        
        if ( redraw == 1 ): 
            temp1 = int(env.getTemp1());
            temp2 = int(env.getTemp2());
            
            mylcd.lcd_clear()
                
            mylcd.lcd_display_string("Sensor 1 : %s %sC" % (temp1, chr(223)), 1)
            mylcd.lcd_display_string("Sensor 2 : %s %sC" % (temp2, chr(223)), 2)
            
            mylcd.lcd_display_string("D) Cikis", 4)
            
            maxTemp1 = int(getParamById(11)["value"]); #MAXTEMP1
            minTemp1 = int(getParamById(12)["value"]); #MINTEMP1
            maxTemp2 = int(getParamById(13)["value"]); #MAXTEMP1
            minTemp2 = int(getParamById(15)["value"]);
            
            print("Max temp1: %s" % maxTemp1)
            print("Min temp1: %s" % minTemp1)
            print("Max temp2: %s" % maxTemp2)
            print("Min temp2: %s" % minTemp2)
            print("C temp1: %s" % int(temp1))
            print("C temp2: %s" % int(temp2))
            
            if ( temp1 < minTemp1):
                print("Min. Temp1 reached.")
                env.stopCooler()
                sleep(3)
                env.closeFan()
            elif ( temp1 > maxTemp1):
                print("Max. Temp1 reached.")
                env.openFan()
                env.startCooler()
            elif ( temp2 < minTemp2):
                print("Min. Temp2 reached.")
                env.stopCooler()
                sleep(3)
                env.closeFan()
            elif ( temp2 > maxTemp2):
                print("Max. Temp2 reached.")
                env.openFan()
                env.startCooler()
            
            
            redraw = 0      

        key = kpd.getch()
        
        if ( key == 'D' ):
            return
            
        count = count + 1
        if ( count > 50 ):
            count = 0
            redraw = 1
            
        sleep(0.1)
  
def a67(win):
    redraw = 1
    motorNo = "0-00"
    pos = 0
    sensorParam = int(getParamById(9)["value"])
    
    while True:
        
        if ( redraw == 1 ): 
            mylcd.lcd_clear()
            
            mylcd.lcd_display_string("MOTOR  : %s" % motorNo, 1)
            mylcd.lcd_display_string("A) START D) EXIT", 4) 
            redraw = 0      

        key = kpd.getch()
        if ( kpd.isNum(key)):
            motorNoL = list(motorNo)
            motorNoL[pos] = key
            motorNo = "".join(motorNoL)
            redraw = 1
            pos = pos + 1
            if ( pos == 1 ):
                pos = 2
            if ( pos > 3 ):
                pos = 0
            continue
        elif ( key == 'A'):
            # print("Starting motor : %s" % int(str(motorNo[0])))
            motor.startMotor(int(str(motorNo[0])), int(motorNo[2:]))
            if ( sensorParam == 1 ):
                pCounter = 0
                while True:
                    keyP = kpd.getch()
                    if ( keyP == 'P' ):
                        break
                    else:
                        pCounter = pCounter + 1
                        
                    if ( pCounter > 50):
                        motor.startMotorQuarter(int(str(motorNo[0])), int(motorNo[2:])) 
                        break
                        
                    sleep(0.1)
            redraw = 1
            continue
        elif ( key == 'D' ):
            return
            
        sleep(0.1)  
  
def openMenu(win, cMenu):
    pPage = 1
    displayed = 0
    while True:
        if ( displayed == 0 ):
            mylcd.lcd_clear()
            for menu in cMenu : 
                if ( (menu['key'] > ((pPage-1)*4)) and (menu['key'] <= (pPage*4))):
                    mylcd.lcd_display_string("%s. " % menu['key'] + menu['name'], menu['key'] - ((pPage - 1) * 4))
            displayed = 1
        key = kpd.getch()
        if ( (key == 'Z') or (key == 'D') ):
            return
        elif ( key == '*' ):
            if ( pPage > 1 ):
                pPage -= 1
                displayed = 0
        elif ( key == '#'):    
            if ( pPage < 2 ):
                pPage += 1
                displayed = 0
                #win.addstr(str(pPage))
        elif ( kpd.isNum(key)):
            menuNum = int(key) - 1
            if ( cMenu[menuNum].get('sub', None) is not None ):
                previousMenu = cMenu
                currentMenu = cMenu[menuNum]['sub']
                openMenu(win, currentMenu)
                displayed = 0
            elif ( cMenu[menuNum].get('fn', None) is not None ):
                globals()[cMenu[menuNum]['fn']](win)
                displayed = 0
        sleep(0.1)

def getPrice(shelf):
    cursor = connection.cursor()
    cursor.execute("SELECT price FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % shelf)
    row = cursor.fetchone()
    cursor.close()
    return row
    
def getParamById(id):
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM parameter WHERE id='%s'" % id)
    row = cursor.fetchone()
    return row
    
def setParamById(id, val):
    cursor2 = connection.cursor()
    cursor2.execute("UPDATE parameter SET value='%s' WHERE id='%s'" % (val, id))
    connection.commit()

def getCard(cuid):
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM card WHERE cuid='%s'" % cuid)
    row = cursor.fetchone()
    return row
    
def dispense(shelf, remaining, balance):
    dispensed = False
    count = 0
    timeout = 0
    lMode = False
    redraw = 1
    leftover = ''
    pName = ''
    sensorParam = int(getParamById(9)["value"])
    pCounter = 0
    
    # play('../res/success.wav')
    
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    mylcd.lcd_clear() 
    cursor.execute("SELECT product.name, shelf.id as shelf_id, shelf.rack_id, shelf.shelf_no, shelf.product_id, product.price, product.vat FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % shelf)
    row = cursor.fetchone()
    motor.startMotor(int(row['rack_id']), int(row['shelf_no']))
            
    if (len(row['name']) > 20 ):
        pName = row['name'][:20]
        leftover = row['name'][20:]
    else:
        pName = row['name']
        leftover = row['name']
    
    while ( not dispensed ):
        if ( redraw == 1 ):
            mylcd.lcd_display_string("DELIVERING PRODUCT..", 1)
            mylcd.lcd_display_string("--------------------", 2)
            
            if ( lMode ):
                mylcd.lcd_display_string("%-20s" % leftover, 3)
            else:
                mylcd.lcd_display_string("%-20s" % pName, 3)
                
            mylcd.lcd_display_string("CHANGE    : %5.2f TL" % remaining, 4)
            redraw = 0
        
        count += 1
        timeout += 1
        
        if ( count > 10 ):
            count = 0
            lMode = not lMode
            redraw = 1
            # motor.stopMotor(3)
        
        #if ( timeout > 50 ):
        #    break;
        
        if ( sensorParam == 1 ):
            keyP = kpd.getch()
            if ( keyP == 'P' ):
                dispensed = True
            else:
                pCounter = pCounter + 1
                
            if ( pCounter == 100):
                motor.startMotorQuarter(int(row['rack_id']), int(row['shelf_no']))
            elif (pCounter == 200):
                sale(1, balance)
                return Decimal(0)            
        sleep(0.05)

    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO sale(product_id, shelf_id, price, sale_dt, balance, remaining, sale_type, success) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", \
        (row['product_id'], row['shelf_id'], row['price'], time.strftime('%Y-%m-%d %H:%M:%S'), balance, remaining, 1, 1)) 
    cursor2.execute("UPDATE shelf SET remaining=remaining-1 WHERE id='%s'" % shelf)
    connection.commit()
    mdb.stackBill()
    mdb.dispense(remaining)
    return Decimal(0)

def cardDispense(shelf, card):
    dispensed = False
    count = 0
    timeout = 0
    lMode = False
    redraw = 1
    leftover = ''
    pName = ''
    
    play('../res/success.wav')
    
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    mylcd.lcd_clear()
    cursor.execute("SELECT product.name, shelf.id as shelf_id, shelf.product_id, product.price, product.vat FROM shelf LEFT JOIN product ON shelf.product_id=product.id WHERE shelf.id='%s'" % shelf)
    row = cursor.fetchone()
    
    remaining = card['balance'] - row['price']
    
    if (len(row['name']) > 20 ):
        pName = row['name'][:20]
        leftover = row['name'][20:]
    else:
        pName = row['name']
        leftover = row['name']
    
    while ( not dispensed ):
        if ( redraw == 1 ):
            mylcd.lcd_display_string("DELIVERING PRODUCT..", 1)
            mylcd.lcd_display_string("--------------------", 2)
            
            if ( lMode ):
                mylcd.lcd_display_string("%-20s" % leftover, 3)
            else:
                mylcd.lcd_display_string("%-20s" % pName, 3)
                
            mylcd.lcd_display_string("FUNDS  :   %6.2f TL" % remaining, 4)
            redraw = 0
        
        count += 1
        timeout += 1
        
        if ( count > 10 ):
            count = 0
            lMode = not lMode
            redraw = 1
        
        if ( timeout > 50 ):
            break;
            
        sleep(0.1)

    
    
    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO sale(product_id, shelf_id, price, sale_dt, balance, remaining, sale_type, card_id, success) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
        (row['product_id'], row['shelf_id'], row['price'], time.strftime('%Y-%m-%d %H:%M:%S'), card['balance'], remaining, 2, card['id'], 1)) 
    cursor2.execute("UPDATE shelf SET remaining=remaining-1 WHERE id='%s'" % shelf)
    cursor2.execute("UPDATE card SET balance=%s WHERE id='%s'" % ("%6.2f" % remaining, card['id']))
    connection.commit() 
    
def chex(num):
    return "%0.2X" % num
    
def idle(win):
    redraw = 1
    count = 0
    coolerCount = 0

    pirState = False
    
    adminPassBuffer = "" 
    
    print("idle")
    displayLogo()
    
    while True: 
        try:
            key = kpd.getch()
            # print(key)
            coin = mdb.getCoin()
            
            if ( not coin == '-'):
                balance = coin
                sale(win, balance)
                mylcd.lcd_clear()
            #cursesKey = win.getch()
            elif ( key == 'A' or key == 'B' ):
                balance = 0
                if ( key == 'A' ):
                    # play('../res/coin.wav')
                    balance = 1.0
                else:
                    # play('../res/coin.wav')
                    balance = 0.5
                sale(win, balance)
                mylcd.lcd_clear()
            elif ( kpd.isNum(key)):
                balance = 0.0
                sale(win, balance, key)
                mylcd.lcd_clear()
            elif ( key == 'Z' ):
                adminPassBuffer = ""
                openMenu(win, currentMenu)
                mylcd.lcd_clear()
                redraw = 1
            elif ( key == '#' ):
                adminPassBuffer = ""
            elif ( not (key == '_')):
                adminPassBuffer = adminPassBuffer + key
                print(adminPassBuffer)
                if ( adminPassBuffer == "**1234" ):
                    openMenu(win, currentMenu)
                    mylcd.lcd_clear()
                    redraw = 1
            if ( redraw == 1 ):
                # mylcd.lcd_display_string("VENDIVERSE     %sC" % env.getTemp2())
                mylcd.lcd_display_string("==== VENDIVERSE ====")
                mylcd.lcd_display_string("%s" %time.strftime("%d/%m/%Y  %H:%M:%S  "), 2)
                mylcd.lcd_display_string("PLEASE INSERT MONEY", 4)
                redraw = 0 
            
            count += 1
            if ( count > 5 ):
                count = 0
                redraw = 1
                
            coolerCount += 1
            if ( coolerCount > 100 ):
                coolerCount = 0
                checkCooler(1)
            
            # Check pir state
            # ps = pir.pirState()
            # if ( ps != pirState):
            #    if ( ps ):
            #        win.addstr("Pir detected...")
            #        play('../res/elevatording.wav')
            #    pirState = ps
            
            # Scan for cards    
            #(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            #if status == MIFAREReader.MI_OK:
            #    (status,uid) = MIFAREReader.MFRC522_Anticoll()
            #    
            #    if status == MIFAREReader.MI_OK:
            #        cuid = chex(uid[0]) + chex(uid[1]) + chex(uid[2]) + chex(uid[3])
            #        
            #        win.addstr("Card read UID: " + cuid)
            #        
            #        card = getCard(cuid)
            #        if ( card is not None ):
            #            cardSale(win, card)
            #            mylcd.lcd_clear() 
            #            redraw=1
            
            sleep(0.1)
        except:
            mylcd.lcd_clear()
            redraw = 1
            traceback.print_exc(file=sys.stdout) 

def sale(win, balance, key = None):
    balance = Decimal(balance)
    redraw = 1
    product = ''
    temporary = False
    tempCount = 30
    
    if ( key is not None ):
        product = key
        temporary = True
        
    mylcd.lcd_clear()
    price = Decimal(0)
    remaining = Decimal(0)

    while True: 
        if ( redraw == 1 ):
            mylcd.lcd_display_string("FUNDS :  %5.2f TL" % balance, 1)
            mylcd.lcd_display_string("--------------------", 2)
            if ( len(product) == 0 ):
                mylcd.lcd_display_string("PLEASE SELECT ITEM", 3)
            elif ( len(product) < 2 ):
                mylcd.lcd_display_string("ITEM : %s            " % product, 3)
                mylcd.lcd_display_string("                    ", 4)
            elif ( len(product) == 2):
                price = getPrice(product)
                if ( price is None ): 
                    product = ''
                    mylcd.lcd_clear()
                    continue
                    
                remaining = Decimal("%5.2f" % price) - balance
                
                if ( temporary == True ):
                    mylcd.lcd_display_string("ITEM  : %s   " % product, 3)
                    mylcd.lcd_display_string("PRICE :     %5.2f TL" % remaining, 4)
                else:
                    mylcd.lcd_display_string("ITEM  : %s  " % product + "%5.2f TL" % price, 3)
                    mylcd.lcd_display_string("PRICE :     %5.2f TL" % remaining, 4)

                if ( remaining <= 0 ):
                    balance = dispense(product, abs(remaining), balance)
                    # balance = abs(remaining)
                    if ( int(balance) == 0):
                        return
                    product = ''
                    mylcd.lcd_clear()
                    redraw = 1
                    continue
            redraw = 0
        key = kpd.getch()
        coin = mdb.getCoin()
        if ( key == 'A' ):
        #    play('../res/coin.wav')
            balance = balance + Decimal(1.0)
            redraw = 1
        elif ( key == 'B' ):
        #    play('../res/coin.wav')
            balance = balance + Decimal(0.5)
            redraw = 1
        elif ( coin == 'P' ):
            mdb.dispense(balance)
            return
        elif ( not coin == '-' ):
            balance = balance + Decimal(coin)
            redraw = 1
        elif ( key == 'D' ):
            product = ''
            redraw = 1
            mylcd.lcd_clear()
        elif ( kpd.isNum(key) ):
            # play('../res/keypress.wav')
            if ( len(product) == 2 ):
                product = ''
            product = product + key
            redraw = 1

        sleep(0.1)
        tempCount -= 1
        if ( temporary == True and tempCount == 0 ):
            return        
        
def cardSale(win, card):
    balance = card['balance']
    redraw = 1
    product = ''
    mylcd.lcd_clear()
    price = Decimal(0)
    remaining = Decimal(0)

    while True: 
        if ( redraw == 1 ):
            mylcd.lcd_display_string("%-20s" % card['name'], 1)
            mylcd.lcd_display_string("FUNDS  :   %6.2f TL" % card['balance'], 2)
            if ( len(product) == 0 ):
                mylcd.lcd_display_string("ITEM   : SELECT", 3)
            elif ( len(product) < 2 ):
                mylcd.lcd_display_string("ITEM   : %s          " % product, 3)
                mylcd.lcd_display_string("                    ", 4)
            elif ( len(product) == 2):
                price = getPrice(product)
                remaining = card['balance'] - Decimal("%5.2f" % price)
                mylcd.lcd_display_string("ITEM   : %s " % product, 3)
                mylcd.lcd_display_string("PRICE  :   %5.2f TL" % price, 4)

                if ( remaining > 0 ):
                    cardDispense(product, card)
                    mylcd.lcd_clear()
                    return
            redraw = 0
        key = kpd.getch()
        if ( key == 'D' ):
            return
        elif ( kpd.isNum(key) ):
            play('../res/keypress.wav')
            if ( len(product) == 2 ):
                product = ''
            product = product + key
            redraw = 1

        sleep(0.1)

def main(win):
    #win.nodelay(True)
    #win.clear()
    idle(win)
         
main(1) 
         
# curses.wrapper(main)

#while True:
#    mylcd.lcd_display_string("MACGAL OTOMAT M100-S")
#    mylcd.lcd_display_string("%s" %time.strftime("%H:%M:%S  %m/%d/%Y"), 2)
