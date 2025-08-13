#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 4.继电器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：4.继电器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：继电器实验
# 继电器控制程序，通过LED的方式控制继电器开关！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import LED
from time import sleep


# ## 2.定义继电器管脚 GPIO17

# In[2]:


makerobo_RelayPin = LED(17)


# ## 3.初始化工作

# In[3]:


def makerobo_setup():
    makerobo_RelayPin.off() # 关闭继电器	


# ## 4.主程序

# In[ ]:


# 循环函数
def makerobo_loop():
	while True:
		# 继电器打开
		makerobo_RelayPin.on()  # 打开继电器
		sleep(0.5)              # 延时500ms
		# 继电器关闭
		makerobo_RelayPin.off() # 关闭继电器
		sleep(0.5)         # 延时500ms

# 释放资源
def makerobo_destroy():
    makerobo_RelayPin.close()

# 程序入口
if __name__ == '__main__':
	makerobo_setup()           #  初始化
	try:
		makerobo_loop()        #  调用循环函数
	except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
		makerobo_destroy()     #  释放资源


# In[ ]:




