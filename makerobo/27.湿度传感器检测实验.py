#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 27.湿度传感器检测实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：27.湿度传感器检测实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：湿度传感器检测实验
# 湿度传感器检测实验，通过adafruit_dht库可以直接读取对应的温度值和湿度值，然后在jupyter 界面下打印出温度值和湿度值！！！！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


import time
import board
import adafruit_dht


# ## 2.DHT11 温湿度传感器管脚定义

# In[ ]:


makerobo_dhtDevice = adafruit_dht.DHT11(board.D17) 


# ## 3.功能函数

# In[ ]:


# 循环函数
def loop():
    while True:
        try:
            # 将数值打印到串口
            temperature_c = makerobo_dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = makerobo_dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(2.0)


# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        pass

