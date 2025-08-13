#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 33.循迹传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：33.循迹传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：循迹传感器实验
# 循迹传感器实验，通过GPIOZero库的Button库直接检测红外循迹传感器是否检测到黑线，然后在jupyter 界面下打印显示提示！！！！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Button
from gpiozero import LED
from time import sleep
from signal import pause


# ## 2.定义红外避障传感器管脚

# In[2]:


makerobo_ObstaclePin = Button(17,pull_up=True)      # 红外循迹传感器模块


# ## 3.主程序

# In[ ]:


# 循环函数	
def makerobo_loop():
    while True:
        if makerobo_ObstaclePin.is_pressed:            # 检测到白色线
            print('********************************') 
            print('*Makerobo White line is detected*') 
            print('********************************')
        else:
            print ('...Makerobo Black line is detected')  # 检测到黑色线

        sleep(0.2) # 延时200ms

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_loop()        #  调用循环函数
	except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
		pass

