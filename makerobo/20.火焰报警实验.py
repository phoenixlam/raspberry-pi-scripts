#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 20.火焰报警实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：20.火焰报警实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：火焰报警实验
# 火焰报警实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到火焰传感器的模拟值，并且打印出火焰的模拟值及提示信息！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义火焰传感器使用通道及数字IO口

# In[2]:


makerobo_DO = Button(17)                  # 火焰传感器数字IO口
makerobo_flamePin = MCP3008(channel=0)    # 定义火焰传感器使用通道


# ## 3.定义打印

# In[3]:


# 打印信息，打印出火焰传感器的状态值
def makerobo_Print(x):
	if x == 1:      # 安全
		print ('')
		print ('   *******************')
		print ('   *  Makerobo Safe~ *')
		print ('   *******************')
		print ('')
	if x == 0:     # 有火焰
		print ('')
		print ('   ******************')
		print ('   * Makerobo Fire! *')
		print ('   ******************')
		print ('')


# ## 3.循环函数

# In[4]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# 循环函数
def makerobo_loop():
    makerobo_status = 1      # 状态值
    # 无限循环
    while True:
        makerobo_tmpval = makerobo_flamePin.value
        makerobo_tmpval = round(MAP(makerobo_tmpval,0,1,0,255))                     # 读取AIN0上的模拟值
        print ('flam Value: ', makerobo_tmpval)                                    # 读取AIN0的值，获取光敏模拟量值

        # 读取火焰传感器数字IO口
        makerobo_tmp = not makerobo_DO.is_pressed    # 获取温度传感器的数字量
        if makerobo_tmp != makerobo_status:          # 判断状态发生改变
            makerobo_Print(makerobo_tmp)             # 打印出火焰传感器的提示信息
            status = makerobo_tmp                    # 当前状态值作为下次状态值进行比较，避免重复打印

        sleep(0.2)                                   # 延时200ms


# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		pass


# In[ ]:




