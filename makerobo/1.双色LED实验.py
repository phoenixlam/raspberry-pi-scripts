#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 1.双色LED灯实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：1.双色LED灯实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：双色LED灯实验
# 双色LED灯控制程序，通过PWM方式控制LED的亮度！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import PWMLED
from time import sleep


# ## 2.定义颜色范围值

# In[2]:


colors = [0xFF00, 0x00FF, 0x0FF0, 0xF00F]
makerobo_pins = (17, 18)  # PIN管脚字典，红色LED接GPIO17，绿色LED接GPIO18


# ## 3.实例化LED管脚

# In[3]:


p_R = PWMLED(pin=makerobo_pins[0],initial_value = 0, frequency=2000)  # 设置频率为2KHz
p_G = PWMLED(pin=makerobo_pins[1],initial_value = 0, frequency=2000)  # 设置频率为2KHz


# ## 4.主程序

# In[4]:


def makerobo_pwm_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_set_Color(col):   # 例如:col = 0x1122
	R_val = col  >> 8
	G_val = col & 0x00FF
	# 把0-255的范围同比例缩小到0-100之间
	R_val = makerobo_pwm_map(R_val, 0, 255, 0, 100)
	G_val = makerobo_pwm_map(G_val, 0, 255, 0, 100)

	p_R.value = (R_val)/100.0     # 改变占空比
	p_G.value = (G_val)/100.0     # 改变占空比

# 调用循环函数
def makerobo_loop():
	while True:
		for col in colors:
			makerobo_set_Color(col)
			sleep(0.5)
# 释放资源
def makerobo_destroy():
	p_G.close()
	p_R.close()

# 程序入口
if __name__ == "__main__":
	try:
		makerobo_loop()        # 调用循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		makerobo_destroy()     # 释放资源


# In[ ]:




