#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 19.光敏传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：19.光敏传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：光敏传感器实验
# 光敏传感器实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到光敏传感器的模拟值，转换为亮度值，并且打印出亮度的模拟值及提示信息！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义光敏传感器使用通道

# In[ ]:


makerobo_PhotoPin = MCP3008(channel=0)    # 定义光敏传感器使用通道


# ## 3.循环函数

# In[ ]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():
    makerobo_count = 0                                                              # 计数值
    while True:                                                                     # 无限循环
        makerobo_PhotoValue = makerobo_PhotoPin.value
        makerobo_PhotoValue = round(MAP(makerobo_PhotoValue,0,1,0,255))       # 读取AIN0上的模拟值
        print ('Photoresistor Value: ', makerobo_PhotoValue)                  # 读取AIN0的值，获取光敏模拟量值
        sleep(0.2)                                                            # 延时 200ms


# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		pass


# In[ ]:




