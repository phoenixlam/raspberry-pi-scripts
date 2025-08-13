#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 9-1.有源蜂鸣器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：9-1.有源蜂鸣器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：有源蜂鸣器实验<br>
# 有源蜂鸣器实验，通过GPIOZero库的Buzzer库直接驱动有源蜂鸣器发出报警声！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Buzzer
from gpiozero import LED
from time import sleep
from signal import pause


# ## 2.定义有源蜂鸣器管脚

# In[2]:


makerobo_Buzzer = 17    # 有源蜂鸣器管脚定义


# ## 3.初始化工作

# In[3]:


# GPIO设置函数
def makerobo_setup():
    global bz
    bz = Buzzer(pin=makerobo_Buzzer,active_high = False )  # 设置管脚，及改为低电平开启蜂鸣器
    bz.off()


# ## 4.功能函数

# In[4]:


#  打开蜂鸣器
def makerobo_buzzer_on():
	bz.on()    # 蜂鸣器为低电平触发，所以使能蜂鸣器让其发声
# 关闭蜂鸣器
def makerobo_buzzer_off():
	bz.off()  # 蜂鸣器设置为高电平，关闭蜂鸟器

# 控制蜂鸣器鸣叫
def makerobo_beep(x):
	makerobo_buzzer_on()     # 打开蜂鸣器控制
	sleep(x)            # 延时时间
	makerobo_buzzer_off()    # 关闭蜂鸣器控制
	sleep(x)            # 延时时间


# ## 5.主程序

# In[ ]:


# 循环函数
def loop():
	while True:
		makerobo_beep(0.5) # 控制蜂鸣器鸣叫，延时时间为500mm

def destroy():
    p_G.close() # 释放资源


# 程序入口
if __name__ == '__main__':    
	makerobo_setup()                # 设置GPIO管脚
	try:                            # 检测异常
		loop()                      # 调用循环函数     
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()              # 释放资源

