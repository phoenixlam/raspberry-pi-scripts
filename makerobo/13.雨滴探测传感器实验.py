#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 13.雨滴探测传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：13.雨滴探测传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：雨滴探测传感器实验
# 模数转换模块实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，检测雨滴探测器的模拟量从而判断雨量强度！！！<br>

# ## 1.导入必要的库文件
from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义使用通道和雨滴传感器数字量IO口
makerobo_DO = Button(17)     # 雨滴传感器数字管脚
pot = MCP3008(channel=0)


# ## 3.初始化工作及中断函数定义
def pressed():        # 有雨滴
    print ('')
    print ('   **********************')
    print ('   * makerobo Raining!! *')
    print ('   **********************')
    print ('')

def released():
    print ('')
    print ('   ************************')
    print ('   * makerobo Not raining *')
    print ('   ************************')
    print ('')

makerobo_DO.when_pressed = pressed
makerobo_DO.when_released = released


# ## 4.循环函数
def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():
    while True:
        pot_vlue =  pot.value
        pot_vlue = MAP(pot_vlue,0,1,0,100)
        print ("{:.2f}".format(pot_vlue))   # 打印出AIN0的模拟量数值
        sleep(0.2)                  # 延时200ms



# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        makerobo_loop()         #  循环函数
    except KeyboardInterrupt:   #  当按下Ctrl+C时，将执行destroy()子程序。
        makerobo_DO.close()     #  释放资源

