#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 15.电位器传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：15.电位器传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：电位器传感器实验
# 电位器传感器实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到电位器的模拟值，从而通过PWM方式控制双色LED灯红色灯的亮度！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import PWMLED, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义使用通道和LED灯控制管脚

# In[ ]:


pot = MCP3008(channel=0) # 定义电位器获取ADC值通道
r_Led = PWMLED(17)         # 定义控制的LED管脚


# ## 3.循环函数

# In[ ]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():

    while True:
        pot_value = round(pot.value * 1000)       # 扩大1000倍，方便读取
        print ('Potentiometer Value:', pot_value) # 获取AIN0上的值，读取电位器模拟量值；
        r_Led.source = absoluted(pot)              # 通过PWM方式，控制LED灯
        sleep(0.5)                               # 延时500ms

# 释放资源
def destroy():
    r_Led.close()


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()   # 调用释放函数


# In[ ]:




