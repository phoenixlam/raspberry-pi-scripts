#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 35.直流电机风扇模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：35.直流电机风扇模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：直流电机风扇模块实验
# 直流电机风扇模块实验，通过GPIOzero 自带的Motor 直流电机驱动库，可以方便控制直流电机的速度、方向等！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import Motor   # 直流电机驱动库
from time import sleep


# ## 2.定义直流电机风扇驱动管脚

# In[ ]:


Makerobo_motor = Motor(forward=17, backward=18, enable=19)


# ## 3.初始化

# In[ ]:


fs_directions = {'clockwiseOpen': Makerobo_motor.forward,'anticlockwiseOpen':Makerobo_motor.backward,'STOP': Makerobo_motor.stop} # 定义开和关


# ## 4.主程序

# In[ ]:


# 循环函数	
def makerobo_loop():
    while True:
        for action in ['clockwiseOpen', 'STOP', 'anticlockwiseOpen', 'STOP']:  # 循环通过定义的动作来控制电机方向
            fs_directions[action]()  # 执行当前动作
            print(f"{action}")       # 打印提示信息
            sleep(5)                 # 延时5S，开启下一个动作

# 释放资源
def destroy():
	# 关闭风扇
    Makerobo_motor.stop()


# 程序入口
if __name__ == '__main__':
	try:
		makerobo_loop()        #  调用循环函数
	except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
		destroy()   # 关闭风扇


# In[ ]:




