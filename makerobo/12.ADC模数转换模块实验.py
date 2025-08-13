#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 12.ADC模数转换模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：12.ADC模数转换模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：模数转换模块实验
# 模数转换模块实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，可以非常便利操作8路10位ADC采集！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import PWMLED, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause


# ## 2.定义使用通道和LED灯控制管脚

# In[2]:


led = PWMLED(17)
pot = MCP3008(channel=0)


# ## 3.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        led.source = absoluted(pot)
        pause()
    except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
        led.close()     #  释放资源

