#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 0025 16:23
# @Author    : Smart 
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import os
import sys
from TemplateMode import *
from MotoControl import *
from KeyScanf import *
from FanControl import *
from GY2561 import *
import time
if __name__ == '__main__':
    #温度模块初始化
    ModeDownTime = 0;#模式切换倒计时计数变量
    TempDownTime = 0;#传感器读取倒计时计数变量
    KeyCount = 0
    Mode = 0#自动模式
    TemplateModes = TemplateMode()#温湿度传感器
    GY2561 = GY2561()#光强传感器
    KeyScanf = KeyScanf()#按键模块初始化
    FanControl = FanControl()#风扇模块初始化
    MotoControl = MotoControl()#窗帘模块初始化
    Lux = 0#当前光强
    WindowState = 0;#0 打开 1关闭
    while(True):
        try:
            #传感器读取倒计时为0，代表要进行传感器读取
            if(TempDownTime == 0):

                TemplateModes.DHT11_receive()#读取温度
                Lux = GY2561.getlux()#读取光强值
                print("Lux: %s" % Lux)
                TempDownTime = 20  * 2.5
                #写入下一次读取传感器的时间
                if (Mode == 0):
                    # 自动模式，温度过高风扇正传
                    if (TemplateModes.temperature > 20):
                        #判断温度是否大于设定值，风扇正转
                        FanControl.Turn();
                    elif (TemplateModes.humidity > 90 and TemplateModes.humidity < 120):
                        FanControl.Teversal()#风扇反转
                    else:
                        FanControl.Stop()#关闭风扇
                    # 光强强则关闭窗帘,光强过强且窗户为打开状态则关闭，
                    if (Lux > 10 and WindowState == 0):
                        MotoControl.backward(0.0025, 512)#关闭窗帘
                        WindowState = 1#设置当前为关闭装填
                    # 光强一般，且窗户为关闭状态
                    elif (Lux < 10 and WindowState == 1):
                        MotoControl.forward(0.0025, 512)#打开窗帘
                        WindowState = 0#设置当前为开启状态
                    else:
                        MotoControl.stop()#停止
                    # 光强一般则打开窗帘
            TempDownTime = TempDownTime - 1;#传感器计数变量递减
            keyvalue = KeyScanf.keyscanf()#读取按键
            if (keyvalue):#检测有按键按下则进入手动模式
                print("HandMode")
                ModeDownTime = 20 * 30 * 1  # 1分钟后进入自动模式，是30的原因是光强和温湿度采集里面有延时。
                Mode = 1  # 手动模式
            if (keyvalue & 0x03 == 0x03):#风扇停止，第一个和第二个按钮同时按下
                print("Stop")
                FanControl.Stop()
                continue
            if(keyvalue & 0x01):#正转
                print("Fan Turn");
                FanControl.Turn();
            if(keyvalue & 0x02):#反转
                print("Reversal");
                FanControl.Teversal();
            if(keyvalue & 0x0c == 0x0c):#窗帘停止
                MotoControl.stop()
                print("WindowStop")
            if(keyvalue & 0x04):#窗帘打开
                print("WindowOn")
                MotoControl.forward(0.0025,512)
                WindowState = 0
            if(keyvalue & 0x08):
                print("MotoOff")#窗帘关闭
                MotoControl.backward(0.0025,512)
                WindowState = 1
            time.sleep(0.05)#20ms
            if(ModeDownTime > 0):
                ModeDownTime = ModeDownTime - 1;#模式切换倒计时
                #手动模式时间倒计时
            else:
                if(Mode == 1):
                    Mode = 0;
                    print("AutoMode")#切换模式
        except KeyboardInterrupt:#检测程序停止按钮，当程序结束时，关闭所有的电机
            MotoControl.stop()
            FanControl.Stop()
            break

            
