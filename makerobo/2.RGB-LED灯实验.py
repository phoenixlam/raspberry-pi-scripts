#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 2.RGB-LED灯传感器实验
# 
# @----湖南创乐博智能科技有限公司---<br>
# @ 文件名：2.RGB-LED灯传感器实验.ipynb <br>
# @ 版本：V2.0 <br>
# @ author: zhulin <br>
# @ 说明：RGBLED灯控制程序，采用PWM方式进行控制! <br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import RGBLED
from colorzero import Color
from time import sleep


# ## 2.定义颜色范围值

# In[2]:


colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']


# ## 3.实例化LED管脚

# In[3]:


led = RGBLED(17, 18, 27)


# ## 4.主程序

# In[ ]:


# 调用循环函数
def makerobo_loop():
	while True:
		for col in colors:
			led.color = Color(col)
			sleep(0.5)
# 释放资源
def makerobo_destroy():
	led.close()

# 程序入口
if __name__ == "__main__":
	try:
		makerobo_loop()        # 调用循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		makerobo_destroy()     # 释放资源

