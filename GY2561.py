#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 0029 23:29
# @Author    : Smart 
# @Site    : 
# @File    : GY2561.py
# @Software: PyCharm

import os
import sys

# !/usr/lib/python3.5

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

class GY2561(object):
    def __init__(self):
        self.fd = wp.wiringPiI2CSetup(I2C)#初始化I2C总线设备
        #初始化I2C
        pass
    def getlux(self):
        #寄存器操作流程，1、写要操作的寄存器 2、写值，要对之前写的寄存器写入的值
        wp.wiringPiI2CWrite(self.fd, CONTROL)#写控制寄存器，
        wp.wiringPiI2CWrite(self.fd, POWER_UP)#开机
        time.sleep(0.5)
        #必要的延时
        ##read data

        wp.wiringPiI2CWrite(self.fd, DATA0LOW)
        data0_L = wp.wiringPiI2CRead(self.fd)
        #读取数据0 的地位
        wp.wiringPiI2CWrite(self.fd, DATA0HIGH)
        data0_H = wp.wiringPiI2CRead(self.fd)
        #读取数据0的高位
        wp.wiringPiI2CWrite(self.fd, DATA1LOW)
        data1_L = wp.wiringPiI2CRead(self.fd)
        #读取数据1的地位
        wp.wiringPiI2CWrite(self.fd, DATA1HIGH)
        data1_H = wp.wiringPiI2CRead(self.fd)
        #读取数据1的高位
        ##calulate Lux
        CH0 = 256 * data0_H + data0_L
        CH1 = 256 * data1_H + data1_L
        #解析数据，下面的解析方法请百度GY2561模块资料
        if (CH0 == 0 | CH1 == 0):
            Lux = 0
        else:
            div = float(CH1) / float(CH0)
            if (div <= 0.5):
                Lux = 0.034 * float(CH0) - 0.063 * float(CH0) * (div ** 1.4)
            elif (div > 0.5 & div <= 0.61):
                Lux = 0.0224 * float(CH0) - 0.031 * CH1
            elif (div > 0.61 & div <= 0.8):
                Lux = 0.0128 * float(CH0) - 0.0153 * CH1
            elif (div > 0.8 & div <= 1.3):
                Lux = 0.00146 * float(CH0) - 0.00112 * CH1
            elif (div > 1.3):
                Lux = 0
        wp.wiringPiI2CWrite(self.fd, CONTROL)
        wp.wiringPiI2CWrite(self.fd, POWER_DOWN)
        #关闭模块
        return Lux
        pass