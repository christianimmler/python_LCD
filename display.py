#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_E,  GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

LCD_WIDTH = 16
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_CHR = True
LCD_CMD = False
E_PULSE = 0.00005
E_DELAY = 0.00005

def lcd_enable():
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  GPIO.output(LCD_RS, mode)
  GPIO.output(LCD_D4, bits&0x10==0x10)
  GPIO.output(LCD_D5, bits&0x20==0x20)
  GPIO.output(LCD_D6, bits&0x40==0x40)
  GPIO.output(LCD_D7, bits&0x80==0x80)
  lcd_enable()
  GPIO.output(LCD_D4, bits&0x01==0x01)
  GPIO.output(LCD_D5, bits&0x02==0x02)
  GPIO.output(LCD_D6, bits&0x04==0x04)
  GPIO.output(LCD_D7, bits&0x08==0x08)
  lcd_enable()

def lcd_string(message):
  message = message.ljust(LCD_WIDTH," ")
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_anzeige(z1, z2):
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string(z1)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string(z2)

LCD_INIT = [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]
for i in LCD_INIT:
  lcd_byte(i,LCD_CMD)

while True:
  zeile1 = time.asctime()
  zeile2 = "IP:" + subprocess.check_output(["hostname","-I"])
  lcd_anzeige(zeile1, zeile2)
  time.sleep(pause)
