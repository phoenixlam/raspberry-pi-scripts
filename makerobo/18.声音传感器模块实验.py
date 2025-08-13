#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 18.声音传感器模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：18.声音传感器模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：声音传感器模块实验
# 声音传感器模块实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到声音传感器的模拟值，转换为声音大小，试试打印出声音的模拟值及提示信息！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义声音传感器使用通道

# In[2]:


makerobo_voiceValuePin = MCP3008(channel=0)    # 定义声音传感器使用通道


# ## 3.循环函数

# In[3]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():
    makerobo_count = 0                                                              # 计数值
    while True:                                                                     # 无限循环
        makerobo_voiceValue = makerobo_voiceValuePin.value
        makerobo_voiceValue = round(MAP(makerobo_voiceValue,0,1,0,255))       # 读取AIN0上的模拟值             
        if makerobo_voiceValue:                                              # 当声音值不为0
            print ("Sound Value:", makerobo_voiceValue)                      # 打印出声音值
            if makerobo_voiceValue < 100:                                     # 如果声音传感器读取值小于80
                print ("Voice detected! ", makerobo_count)                   # 打印出计数值
                makerobo_count += 1                                          # 计数值累加
            sleep(0.2)                                                  # 延时 200ms


# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		pass


# In[ ]:




