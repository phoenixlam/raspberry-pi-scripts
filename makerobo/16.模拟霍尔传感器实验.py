#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 16.模拟霍尔传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：16.模拟霍尔传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：模拟霍尔传感器实验
# 模拟霍尔传感器实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到模拟霍尔传感器的模拟值，从而判断磁性物质！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import PWMLED, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义使用通道

# In[ ]:


makerobo_hall = MCP3008(channel=0) # 定义电位器获取ADC值通道


# ## 3.定义打印

# In[ ]:


# 打印出磁场的信息
def makerobo_Print(x):
	if x == 0:    #  没有磁场
		print ('')
		print ('*************')
		print ('* No Magnet *')
		print ('*************')
		print ('')
	if x == 1:    #  磁场为南
		print ('')
		print ('****************')
		print ('* Magnet North *')
		print ('****************')
		print ('')
	if x == -1:   # 磁场为北
		print ('')
		print ('****************')
		print ('* Magnet South *')
		print ('****************')
		print ('')


# ## 4.循环函数

# In[ ]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_loop():
    makerobo_status = 0 # 给状态变量赋0值
    while True:  # 无限循环
        makerobo_res = round(makerobo_hall.value * 1000)  # 获取AIN0 的模拟量值，并扩大1000倍
        makerobo_res = round(MAP(makerobo_res,0,1000,0,255))
        print ('Current intensity of magnetic field : ', makerobo_res) # 打印出磁场的电流强度值
        if makerobo_res - 133 < 5 and makerobo_res - 133 > -5: # 判断磁场强度范围
            makerobo_tmp = 0    #  没有磁场
        if makerobo_res < 128:  # 磁场强度为北
            makerobo_tmp = -1
        if makerobo_res > 138:  # 磁场强度为南
            makerobo_tmp = 1
        if makerobo_tmp != makerobo_status: # 磁场发生改变
            makerobo_Print(makerobo_tmp) # 调用打印出磁场的信息
            makerobo_status = makerobo_tmp # 把当前状态值设置为比较状态值，避免重复打印；
        sleep(0.2) # 延时200ms 


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()   # 调用释放函数


# In[ ]:




