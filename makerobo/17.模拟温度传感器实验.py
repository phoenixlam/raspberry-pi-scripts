#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 17.模拟温度传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：17.模拟温度传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：模拟模拟温度传感器实验
# 模拟温度传感器实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到模拟温度传感器的模拟值，然后折算成具体的温度值，同时通过数字端口检测判断温度是否过高，从而进行提示！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep
import math


# ## 2.定义温度传感器使用通道和温度传感器数字管脚

# In[ ]:


makerobo_DO = Button(17)                 # 温度传感器Do管脚
makerobo_tempPin = MCP3008(channel=0)    # 定义温度传感器获取ADC值通道


# ## 3.定义打印

# In[ ]:


# 打印出温度传感器的提示信息
def makerobo_Print(x):
	if x == 1:     # 正合适
		print ('')
		print ('***********')
		print ('* Better~ *')
		print ('***********')
		print ('')
	if x == 0:    # 太热
		print ('')
		print ('************')
		print ('* Too Hot! *')
		print ('************')
		print ('')


# ## 4.循环函数

# In[ ]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():
    makerobo_status = 1  # 状态值
    makerobo_tmp = 1     # 当前值
    while True:  # 无限循环
        makerobo_analogVal = makerobo_tempPin.value                       # 获取AIN0 的模拟量值
        makerobo_Vr = float(makerobo_analogVal) * 3.3                     # 转换为电压值
        makerobo_Rt = 10000 * makerobo_Vr / (3.3 - makerobo_Vr)
        makerobo_temp = 1/(((math.log(makerobo_Rt / 10000)) / 3950) + (1 / (273.15+25)))
        temp_c = makerobo_temp - 273.15
        temp_f = temp_c * 9.0 / 5.0 + 32
        print("Temp C={:.2f}\tTemp F={:.2f}".format(temp_c, temp_f))

        makerobo_tmp = not makerobo_DO.is_pressed    # 获取温度传感器的数字量
        if makerobo_tmp != makerobo_status:          # 判断状态值发生改变
            makerobo_Print(makerobo_tmp)    # 打印出温度传感器的提示信息
            makerobo_status = makerobo_tmp  # 把当前状态值设置为比较状态值，避免重复打印； 
        sleep(0.2) # 延时200ms 


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		pass


# In[ ]:




