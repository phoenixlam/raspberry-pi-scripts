#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 37.PIR 人体热释电感应模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：37.PIR 人体热释电感应模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：PIR 人体热释电感应模块实验
# 直流电机风扇模块实验，通过GPIOzero 自带的 MotionSensor 人体热释电感应模块库，可以方便感知运动物体的释放出的热释电！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import RGBLED, MotionSensor
from time import sleep


# ## 2.定义PIR 和RGB 对应的管脚

# In[2]:


makerobo_rgb = RGBLED(red=18, green=19, blue=27)  # 定义RGB灯管脚
makerobo_pir = MotionSensor(17)                   # 定义PIR人体热释电管脚


# ## 3.定义循环函数

# In[3]:


# 循环函数
def makerobo_loop():
    try:
        while True:
            if makerobo_pir.motion_detected:  # 检查PIR传感器检测到的运动
                makerobo_rgb.color = (1, 1, 0)         # 设置LED颜色为黄色(红色+绿色)
            else:
                makerobo_rgb.color = (0, 0, 1)         # 设置LED颜色为蓝色(仅为蓝色)
            sleep(0.1)                        # 短延迟，降低CPU负载

    except KeyboardInterrupt:
        pass


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        makerobo_loop()  # 循环函数
    except KeyboardInterrupt:   # 当按下Ctrl+C时，将执行destroy()子程序。
        pass  


# In[ ]:




