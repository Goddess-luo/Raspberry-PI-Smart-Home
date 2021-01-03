#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 0029 21:12
# @Author    : Smart 
# @Site    : 
# @File    : FanControl.py
# @Software: PyCharm

import os
import sys
import RPi.GPIO as GPIO
import time

class FanControl(object):
    def __init__(self):
        self.InA = 16#电机控制端
        self.InB = 18
        GPIO.setwarnings(False)#忽略wri库的警告信息
        GPIO.setmode(GPIO.BOARD)#设置GPIO编码方式
        GPIO.setup(self.InA, GPIO.OUT)#设置输出模式
        GPIO.setup(self.InB, GPIO.OUT)

        GPIO.output(self.InA, GPIO.LOW)#设置低电平，关闭电机
        GPIO.output(self.InB, GPIO.LOW)
        pass
    def  Turn(self):
        #正转
        GPIO.output(self.InA, GPIO.HIGH)#高
        GPIO.output(self.InB, GPIO.LOW)#低
        pass
        #反转
    def Teversal(self):
        GPIO.output(self.InA, GPIO.LOW)
        GPIO.output(self.InB, GPIO.HIGH)
    def Stop(self):
        #停止
        GPIO.output(self.InA, GPIO.LOW)#低电平
        GPIO.output(self.InB, GPIO.LOW)

        
