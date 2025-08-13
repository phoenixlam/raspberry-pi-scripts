#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 26.旋转编码器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：26.旋转编码器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：旋转编码器实验
# 旋转编码器实验，通过gpiozero库自带的RotaryEncoder操作库，可以直接对旋转编码器进行操作，SW按下通过button函数库来检查按键是否按下！！！！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import RotaryEncoder, Button
from time import sleep


# ## 2.定义旋转编码器管脚

# In[2]:


encoder = RotaryEncoder(a=17, b=18)  #旋转编码器的CLK连接GPIO 17，DT连接GPIO 18
button = Button(27)                  # SW连接 GPIO27


# ## 3.初始化函数

# In[3]:


makerobo_globalCounter = 0          # 计数器值
makerobo_tmp = 0	                # 当前状态判断


# ## 4.功能函数

# In[4]:


# 旋转编码方向位判断函数
def makerobo_rotaryDeal():
    global makerobo_globalCounter
    global makerobo_tmp
    makerobo_globalCounter += encoder.steps  # 根据编码器步骤调整计数器
    encoder.steps = 0 # 更新计数器后重置编码器步骤
    if makerobo_tmp != makerobo_globalCounter: # 判断状态值发生改变
        print ('makerobo_globalCounter = %d' % makerobo_globalCounter) # 打印出状态信息
        makerobo_tmp = makerobo_globalCounter    #  把当前状态赋值到下一个状态，避免重复打印

# 中间按键按下响应程序
def makerobo_btnISR():
    global makerobo_globalCounter
    makerobo_globalCounter = 0     # 复位计数器值
    print('Counter reset') # 计数器值复位

# 按键按下中断响应程序
button.when_pressed = makerobo_btnISR


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        while True:
            makerobo_rotaryDeal()  # 更新编码器值
            sleep(0.1)             # 短延迟，降低CPU负载
    except KeyboardInterrupt:
        pass

