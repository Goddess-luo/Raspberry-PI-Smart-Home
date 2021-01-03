#coding:utf-8
import thread
import time
import array
import RPi.GPIO as GPIO
import time
#温湿度传感器面向对象编程
class TemplateMode(object):
    def __init__(self):
        #温湿度传感器初始化
        self.channel = 7
        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        time.sleep(1)

        self.data= []
        pass
    #接收温湿度传感器的温湿度信息
    def DHT11_receive(self):
        time.sleep(1)
        j = 0
        GPIO.setup(self.channel,GPIO.OUT)
        GPIO.output(self.channel, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.channel, GPIO.HIGH)
        i = 1
        GPIO.setup(self.channel, GPIO.IN)

        while GPIO.input(self.channel) == GPIO.LOW:
            continue
        while GPIO.input(self.channel) == GPIO.HIGH:
            continue
        #接收5个字节的数据
        while j < 40:
            k = 0
            while GPIO.input(self.channel) == GPIO.LOW:
                continue
            while GPIO.input(self.channel) == GPIO.HIGH:
                k += 1
                if k > 100: break
            if k < 8:
                self.data.append(0)
            else:
                self.data.append(1)
            j += 1
        #解析温湿度数据
        humidity_bit = self.data[0:8]
        humidity_point_bit = self.data[8:16]
        temperature_bit = self.data[16:24]
        temperature_point_bit = self.data[24:32]
        check_bit = self.data[32:40]

        self.humidity = 0
        humidity_point = 0
        self.temperature = 0
        temperature_point = 0
        check = 0
        for i in range(8):
            self.humidity += humidity_bit[i] * 2 ** (7 - i)
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
            self.temperature += temperature_bit[i] * 2 ** (7 - i)
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
            check += check_bit[i] * 2 ** (7 - i)
        #解析出温湿度数据
        tmp = self.humidity + humidity_point + self.temperature + temperature_point
        if check == tmp:
            print "temperature is ", self.temperature, "wet is ", self.humidity, "%"
        else:
            print "something is worong the humidity,humidity_point,temperature,temperature_point,check is", self.humidity, humidity_point, self.temperature, temperature_point, check
        pass