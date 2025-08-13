#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 6.轻触按键实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：6.轻触按键实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：轻触按键实验
# 轻触传感器实验，通过GPIOZero库的Button库直接检测轻触按键是否按下，从而来点亮双色LED灯！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Button
from gpiozero import LED
from time import sleep
from signal import pause


# ## 2.定义轻触按键管脚和双色LED管脚

# In[2]:


btn = Button(17)     # 轻触按键管脚
p_R = LED(18)        # 红色LED管脚
p_G = LED(27)        # 绿色LED管脚


# ## 3.初始化工作及中断函数定义

# In[3]:


def pressed():
    print('*****************************************') 
    print('* makerobo Raspberry Kit Button Pressed!*') 
    print('*****************************************')
    p_R.on()  # 打开红色LED
    p_G.off() # 关闭绿色LED

def released():
    print("button was released")
    p_R.off()   # 关闭红色LED
    p_G.on()    # 打开绿色LED

btn.when_pressed = pressed
btn.when_released = released


# ## 4.主程序

# In[ ]:


# 循环函数	
def makerobo_loop():
    pause()

# 释放资源
def makerobo_destroy():
    p_R.close()
    p_G.close()

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_loop()        #  调用循环函数
	except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
		makerobo_destroy()     #  释放资源

