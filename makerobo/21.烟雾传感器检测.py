#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 21.烟雾传感器检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：21.烟雾传感器检测.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：烟雾传感器检测
# 烟雾传感器检测实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，采集到烟雾传感器的模拟值，到达一定的阈值后，控制蜂鸣器报警，并且打印出烟雾的模拟值及读取数字量打印出提示信息！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from gpiozero import Button,Buzzer,MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义烟雾传感器通道和烟雾传感器数字IO及蜂鸣器数字IO口

# In[2]:


makerobo_DO = Button(17)                              # 烟雾传感器数字IO口
makerobo_Buzz = Buzzer(pin=18,active_high = False )  # 设置管脚，及改为低电平开启蜂鸣器
makerobo_GasPin = MCP3008(channel=0)                # 定义烟雾传感器使用通道


# ## 3.定义打印

# In[3]:


# 打印信息，打印出是否检测到烟雾信息
def makerobo_Print(x):
	if x == 1:     # 安全
		print ('')
		print ('   ******************')
		print ('   * Makerobo Safe~ *')
		print ('   ******************')
		print ('')
	if x == 0:    # 检测到烟雾
		print ('')
		print ('   ************************')
		print ('   * Makerobo Danger Gas! *')
		print ('   ************************')
		print ('')


# ## 3.循环函数

# In[4]:


def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# 循环函数
def makerobo_loop():
    makerobo_status = 1   # 定义状态值变量
    makerobo_count = 0    # 定义计数器变量值
    while True:    # 无限循环
        makerobo_tmpval = makerobo_GasPin.value
        makerobo_tmpval = round(MAP(makerobo_tmpval,0,1,0,255))                     # 读取AIN0上的模拟值
        print ('Gas Value: ', makerobo_tmpval)                                    # 读取AIN0的值，获取光敏模拟量值

        makerobo_tmp = not makerobo_DO.is_pressed  # 读取GAS烟雾传感器数字IO口值
        if makerobo_tmp != makerobo_status:     # 判断状态发生改变
            makerobo_Print(makerobo_tmp)        # 打印函数，打印出烟雾传感器信息
            makerobo_status = makerobo_tmp      # 把当前状态值设置为比较状态值，避免重复打印；
        if makerobo_status == 0:                # 当检测到烟雾
            makerobo_count += 1                 # 计数器值累计
            # 高低电平交替变化，让蜂鸣器发声
            if makerobo_count % 2 == 0:         # 进行求余处理，一半为1，一半为0
                makerobo_Buzz.on()
            else:
                makerobo_Buzz.off()
        else:
            makerobo_Buzz.off()                 # 设置蜂鸣器为高电平，初始状态关闭蜂鸣器鸣叫
            makerobo_count = 0                  # 计数器赋0s
        sleep(0.2)                         # 延时200ms


def destroy():
    makerobo_Buzz.off()   # 关闭蜂鸣器
    makerobo_Buzz.close() # 释放资源


# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()  #资源释放


# In[ ]:




