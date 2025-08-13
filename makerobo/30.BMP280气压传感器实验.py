#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 30.BMP280气压传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：30.BMP280气压传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：BMP280气压传感器实验
# BMP280气压传感器实验，通过对应的adafruit_bmp280库函数，进行I2C控制方式，控制_bmp280气压传感器显示出当前气压和温度值，并在界面上打印出来！！！！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


import time
import board
import adafruit_bmp280 # 载入bmp280 传感器库


# ## 2.初始化工作

# In[ ]:


# 创建传感器对象，通过主板默认的I2C总线进行通信
i2c = board.I2C()  
makerobo_bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)

# 将其更改为与该位置在海平面上的压力(hPa)相匹配
makerobo_bmp280.sea_level_pressure = 1013.25


# ## 3.循环函数

# In[ ]:


# 循环函数
def makerobo_loop():
    try:
        while True:
            print("\nTemperature: %0.1f C" % makerobo_bmp280.temperature)
            print("Pressure: %0.1f hPa" % makerobo_bmp280.pressure)
            print("Altitude = %0.2f meters" % makerobo_bmp280.altitude)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exit")  # Exit on CTRL+C


# ## 4.程序入口

# In[ ]:


# 程序入口
if __name__ == "__main__":
	try:
		makerobo_loop()       # 循环显示信息
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		print("Exit")  # Exit on CTRL+C


# In[ ]:




