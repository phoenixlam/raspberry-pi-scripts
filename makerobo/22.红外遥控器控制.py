#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 22.红外遥控器控制
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：22.红外遥控器控制.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：红外遥控器控制
# 红外遥控器控制程序，通过pylirc库接收红外遥控器信号，把接收到的红外遥控器控制信号解码后，判断哪个键按下，从而控制RGB LED灯亮灭情况！！！<br>

# ## 1.导入必要的库文件

# In[1]:


import time
import pylirc as lirc
from gpiozero import RGBLED


# ## 2.定义颜色范围值

# In[2]:


rgb_Lv = [100, 20, 0]   # RGB 亮度配置
rgb_color = [00, 00, 00]  # RGB 颜色配置


# ## 3.实例化LED管脚

# In[3]:


led = RGBLED(18, 19, 20)
makerobo_blocking = 0 # 判断值


# ## 4.RGB控制函数

# In[4]:


# 从一个区域映射到另一个区域函数
def makerobo_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# RGB-LED 颜色设置
def makerobo_ledColorSet(color):
    r_val = 100 - color[0]
    g_val = 100 - color[1]
    b_val = 100 - color[2]
    r_val = makerobo_map(r_val,0,100,0,1)
    g_val = makerobo_map(g_val,0,100,0,1)
    b_val = makerobo_map(b_val,0,100,0,1)
    led.color = (r_val,g_val,b_val)


# ## 5.初始化函数

# In[5]:


# GPIO初始化设置
def makerobo_setup():
	lirc.init("pylirc", "/etc/lirc/conf", makerobo_blocking) # 载入配置参数


# ## 6.RGB控制函数

# In[6]:


def RGB_control(config):
	global color
	if config == 'KEY_CHANNELDOWN':  # 按键第一行第一个
		rgb_color[0] = rgb_Lv[0]
		print ('Makerobo Red OFF')

	if config == 'KEY_CHANNEL':     # 按键第一行第二个
		rgb_color[0] = rgb_Lv[1]
		print ('Makerobo Light Red')

	if config == 'KEY_CHANNELUP':   # 按键第一行第三个
		rgb_color[0] = rgb_Lv[2]
		print ('Makerobo Red')

	if config == 'KEY_PREVIOUS':    # 第二行第一个
		rgb_color[1] = rgb_Lv[0]
		print ('Makerobo Green OFF')

	if config == 'KEY_NEXT':       # 第二行第二个
		rgb_color[1] = rgb_Lv[1]
		print ('Makerobo Light Green')

	if config == 'KEY_PLAYPAUSE':  # 第二行第三个
		rgb_color[1] = rgb_Lv[2]
		print ('Makerobo Green')

	if config == 'KEY_VOLUMEDOWN': # 第三行第一个
		rgb_color[2] = rgb_Lv[0]
		print ('Makerobo Blue OFF')

	if config == 'KEY_VOLUMEUP':  # 第三行第二个
		rgb_color[2] = rgb_Lv[1]
		print ('Makerobo Light Blue')

	if config == 'KEY_EQUAL':    # 第三行第三个
		rgb_color[2] = rgb_Lv[2]
		print ('Makerobo BLUE')


# ## 7.循环函数

# In[7]:


# 循环函数
def makerobo_loop():
	while True:
		s = lirc.nextcode(1)    # 获取红外遥控器码值		
		while(s):
			for (code) in s:
				print ("Command: ", code["config"]) # 调试信息，可以具体知道按下了哪个按键
				RGB_control(code["config"])  # 调用控制RGB函数
				makerobo_ledColorSet(rgb_color)  # RGB-LED 颜色设置
			if(not makerobo_blocking):       # 读取到值
				s = lirc.nextcode(1)       # 再一次获取红外遥控器码值	
			else:
				s = []


# ## 8.释放函数

# In[8]:


def destroy():
    led.close()
    lirc.exit()  # 退出红外遥控器接收


# ## 9.程序入口

# In[ ]:


# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # GPIO初始化程序
		makerobo_loop()  # 调用循环函数
	except KeyboardInterrupt: # 如果按下ctrl + C,退出，处理异常
		destroy() # 释放资源

