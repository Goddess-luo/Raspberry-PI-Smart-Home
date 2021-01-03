#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/20 0020 15:21
# @Author    : Smart 
# @Site    : 
# @File    : MotoControl.py
# @Software: PyCharm

import os
import sys

# !/usr/bin/env python
#########################################################
#	File name: stepMotor.py
#	   Author: Jason Dai
#	     Date: 2015/01/26
#########################################################
import RPi.GPIO as GPIO
import time

IN1 = 32  # pin11
IN2 = 36
IN3 = 38
IN4 = 40
#步进电机控制程序
class MotoControl:
        #构造函数初始化
    def setStep(self,w1, w2, w3, w4):
        GPIO.output(IN1, w1)
        GPIO.output(IN2, w2)
        GPIO.output(IN3, w3)
        GPIO.output(IN4, w4)

    def __init__(self,):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
        GPIO.setup(IN1, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)
        #设置4相的gpio为输出模式
    #正转
    def forward(self,delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 0, 0, 1)
            time.sleep(delay)
    #反转
    def backward(self,delay, steps):
        for i in range(0, steps):
            self.setStep(0, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)
    def stop(self):
        self.setStep(0, 0, 0, 0)
    def destroy(self):
        GPIO.cleanup()  # Release resource

       
