#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 25.DS18B20温度传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：25.DS18B20 温度传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：DS18B20温度传感器实验
# DS18B20温度传感器实验，通过树莓派的单总线通讯的方式建立通讯，DS18B20有着唯一的ID号，一般为28-XXXXXXX,在操作之前我们要获取这个唯一的ID号！！！！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


import os

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# ## 2.ds18b20 设备ID

# In[ ]:


makerobo_ds18b20 = '28-4d0cd4445032'  # ds18b20 设备，每个设备地址都会不一样，需要修改


# ## 3.初始化函数

# In[ ]:


def makerobo_setup():
	global makerobo_ds18b20  # 全局变量
	# 获取 ds18b20 地址
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			makerobo_ds18b20 = i       # ds18b20存放在ds18b20地址


# ## 4.功能函数

# In[ ]:


# 读取ds18b20地址数据
def makerobo_read():
    makerobo_location = '/sys/bus/w1/devices/' + makerobo_ds18b20 + '/w1_slave' # 保存ds18b20地址信息
    makerobo_tfile = open(makerobo_location)  # 打开ds18b20 
    makerobo_text = makerobo_tfile.read()     # 读取到温度值
    makerobo_tfile.close()                    # 关闭读取
    try:
        secondline = makerobo_text.split("\n")[1] # 格式化处理
    except IndexError as e:
        return 0
    temperaturedata = secondline.split(" ")[9]# 获取温度数据
    temperature = float(temperaturedata[2:])  # 去掉前两位
    temperature = temperature / 1000          # 去掉小数点
    return temperature                        # 返回温度值

# 循环函数	
def makerobo_loop():
	while True:
		if makerobo_read() != None:  # 调用读取温度值，如果读到到温度值不为空
			print ("Current temperature : %0.3f C" % makerobo_read()) # 打印温度值

# 释放资源
def destroy():
	pass


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup()  # 调用初始化程序
		makerobo_loop()   # 调用循环函数
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()             # 释放资源


# In[ ]:




