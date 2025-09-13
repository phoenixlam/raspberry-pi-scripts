#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 32.DS1307实时时钟模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：32.DS1307实时时钟模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：32.DS1307实时时钟模块实验
# DS1307实时时钟模块实验，DS1307库进行操作，进行I2C控制方式，控制DS1307实时时钟模块，并在界面上设置和打印出对应的实时时间！！！！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


import sys
import time
import datetime
import SDL_DS1307   # DS1307 实时时钟模块库


# ## 2.初始化工作

# In[ ]:


print(" ")
print("makerobo DS1307 Real-time clock Demo")
print(" ")
print(" ")
print("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.datetime.utcnow()


# ## 3.DS1307 实时时钟I2C实例化

# In[ ]:


ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)  # i2c地址为0x68
ds1307.write_now()


# ## 4.循环函数

# In[ ]:


# 循环函数
def makerobo_loop():
    while True:
        #currenttime = datetime.datetime.utcnow()
        #deltatime = currenttime - starttime
        print(" ")
        print("Raspberry Pi=\t" + time.strftime("%Y-%m-%d %H:%M:%S"))
        print("DS1307 RTC =\t20%d-%d-%d %d:%d:%d" 
              % (ds1307._read_year(),ds1307._read_month(),
                 ds1307._read_date(),ds1307._read_hours(),
                 ds1307._read_minutes(),ds1307._read_seconds()))
        time.sleep(10.0)


# ## 5.程序入口

# In[ ]:


# 程序入口
if __name__ == "__main__":
	try:
		makerobo_loop()       # 循环显示信息
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		print("Exit")  # Exit on CTRL+C

