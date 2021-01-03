#!/usr/bin/python
#encoding:utf-8

import wiringpi as wp
import time

I2C         =0x39
datareg_num =4
DATA0LOW    =0x8C
DATA0HIGH   =0x8D
DATA1LOW    =0x8E
DATA1HIGH   =0x8F
CONTROL     =0x80
POWER_UP    =0x33
POWER_DOWN  =0x00

fd=wp.wiringPiI2CSetup(I2C)

wp.wiringPiI2CWrite(fd,CONTROL)
wp.wiringPiI2CWrite(fd,POWER_UP)
time.sleep(1)

##read data

wp.wiringPiI2CWrite(fd,DATA0LOW)
data0_L=wp.wiringPiI2CRead(fd)

wp.wiringPiI2CWrite(fd,DATA0HIGH)
data0_H=wp.wiringPiI2CRead(fd)

wp.wiringPiI2CWrite(fd,DATA1LOW)
data1_L=wp.wiringPiI2CRead(fd)

wp.wiringPiI2CWrite(fd,DATA1HIGH)
data1_H=wp.wiringPiI2CRead(fd)

##calulate Lux
CH0=256*data0_H+data0_L
CH1=256*data1_H+data1_L
print(CH0)
print(CH1)
if(CH0==0 | CH1==0):
    Lux=0
else:
    div=float(CH1)/float(CH0)
    if(div <= 0.5):
        Lux=0.034*float(CH0)-0.063*float(CH0)*(div**1.4)
    elif(div>0.5 & div<=0.61):
        Lux=0.0224*float(CH0)-0.031*CH1
    elif(div>0.61 & div<=0.8):
        Lux=0.0128*float(CH0)-0.0153*CH1
    elif(div>0.8 & div<=1.3):
        Lux=0.00146*float(CH0)-0.00112*CH1
    elif(div>1.3):
        Lux=0
print '%f' % Lux

wp.wiringPiI2CWrite(fd,CONTROL)
wp.wiringPiI2CWrite(fd,POWER_DOWN)
