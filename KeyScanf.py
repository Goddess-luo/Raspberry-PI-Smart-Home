# -*- coding: utf-8 -*-
import  os
import  sys
import re
import operator
import  time
import array
import RPi.GPIO as GPIO

class KeyScanf(object):
    def __init__(self):
        self.key = (37,35,33,31)#4个按钮的引脚
        self.flage = array.array('i',[0,0,0,0])
        self.keyvalue= 0;
        GPIO.setmode(GPIO.BOARD)  ## 使用BOARD引脚编号，此外还有 GPIO.BCM
        for pin in self.key:
            GPIO.setup(pin, GPIO.IN)  ## 设置7号引脚输出
        pass
    def keyscanf(self):
        self.keyvalue = 0;
        self.uiLoop = 0;
        for pin in self.key:
            if(GPIO.input(pin) == 0):#判断当前按键是否为低电平
                self.flage[self.uiLoop] = 1
            #判断当前按键是否为高电平且上一次为低电平。代表判断按键的按下
            if((GPIO.input(pin) == 1) and (self.flage[self.uiLoop] == 1)):
                self.keyvalue |= (0x01 << self.uiLoop)
                self.flage[self.uiLoop] = 0#如果确认按下则对应bit位写1
            else:
                self.keyvalue &= ~(0x01 << self.uiLoop)
                #该按键没有按下则对bit位清零
                #0x01 0x02 0x04 0x08 分别代表4个按钮被按下，
            self.uiLoop = self.uiLoop + 1
        return self.keyvalue
        pass
    
