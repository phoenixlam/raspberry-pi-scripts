#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 41.综合案例-智能温度测量系统
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：41.综合案例-智能温度测量系统.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：综合案例-智能温度测量系统
# 综合案例-智能温度测量系统，该案例为所学传感器知识的一个综合应用案例，为进一步巩固所学知识的一个总结！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import MCP3008
import os
from gpiozero.tools import absoluted, scaled
from signal import pause
from gpiozero import Buzzer
from gpiozero import RGBLED
from colorzero import Color
from time import sleep


# ## 2.管脚定义

# In[ ]:


## DS18B20 地址，该地址需要修改
makerobo_ds18b20 = '28-4d0cd4445032'  # ds18b20 设备，每个设备地址都会不一样，需要修改


# In[ ]:


## 颜色定义
makerobo_color = ['red', 'green', 'blue']
## DS18B20 初始化
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

## RGB-LED灯定义
led = RGBLED(17, 18, 19)     # RGB-LED灯定义
makerobo_Buzzer = 20        # 有源蜂鸣器管脚定义
# PS2操纵杆定义
pot_x = MCP3008(channel=0) # 定义PS2操纵杆对应的X方向管脚
pot_y = MCP3008(channel=1) # 定义PS2操纵杆对应的y方向管脚
pot_z = MCP3008(channel=2) # 定义PS2操纵杆对应的z方向管脚


# ## 3. 功能函数

# In[ ]:


# 初始化函数
def makerobo_setup():
    global bz
    global makerobo_ds18b20  # 全局变量
    global ds_lowl, ds_highl  # 定义温度值的上下限值
    ds_lowl = 29              # 初始化下限值为29度
    ds_highl = 31             # 初始化上限值为31度
    bz = Buzzer(pin=makerobo_Buzzer,active_high = False )  # 设置管脚，及改为低电平开启蜂鸣器
    bz.off()
    # 获取 ds18b20 地址
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            makerobo_ds18b20 = i       # ds18b20存放在ds18b20地址

def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# 方向判断函数
def makerobo_direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']  # 方向状态信息
    i = 0
    x_value = round(pot_x.value * 1024)
    y_value = round(pot_y.value * 1024)
    z_value = round(pot_z.value * 1024)
    x_value = round(MAP(x_value,0,1023,0,255))
    y_value = round(MAP(y_value,0,1023,0,255))
    z_value = round(MAP(z_value,0,1023,0,255))
    '''
    print('x_value:{},y_value:{},z_value{}'.format(x_value,y_value,z_value))
    '''
    if x_value <= 30:
        i = 1     # up方向
    if x_value >= 225:
        i = 2    # down方向
    if y_value >= 225:
        i = 4    # left 方向
    if y_value <= 30:
        i = 3    # right 方向
    if z_value <= 2 and y_value >= 128:
        i = 5    # Button 按下
    if x_value - 125 < 15 and x_value - 125 > -15	and y_value - 125 < 15 and y_value - 125 > -15 and z_value >= 250:
        i = 0

    return state[i]   # 返回状态

# 计算
def makerobo_edge():
	global ds_lowl, ds_highl
	ds_temp = makerobo_direction()   # 调用PS2操作函数进行方向判断
	if ds_temp == 'Pressed':
		makerobo_destroy()   # 退出系统
		quit()
	if ds_temp == 'up' and ds_lowl < ds_highl-1:   # PS2手柄向上拨动  上限值加1
		ds_highl += 1
	if ds_temp == 'down' and ds_lowl >= -5:        # PS2手柄向下拨动  上限值减1
		ds_highl -= 1
	if ds_temp == 'right' and ds_highl <= 125:     # PS2手柄向右拨动 下限值加1
		ds_lowl += 1
	if ds_temp == 'left' and ds_lowl < ds_highl-1: # PS2手柄向左拨动 下限值减1
		ds_lowl -= 1

# 检查值是否在闭区间内（包括边界值）
def is_in_closed_range(value, start, end):
    return start <= value <= end

# 读取ds18b20地址数据
def makerobo_read():
    makerobo_location = '/sys/bus/w1/devices/' + makerobo_ds18b20 + '/w1_slave' # 保存ds18b20地址信息
    makerobo_tfile = open(makerobo_location)  # 打开ds18b20 
    makerobo_text = makerobo_tfile.read()     # 读取到温度值
    makerobo_tfile.close()                    # 关闭读取
    try:
        secondline = makerobo_text.split("\n")[1] # 格式化处理
    except IndexError as e:
        return 1000  # 抛出不正常的温度
    temperaturedata = secondline.split(" ")[9]# 获取温度数据
    temperature = float(temperaturedata[2:])  # 去掉前两位
    temperature = temperature / 1000          # 去掉小数点
    return temperature                        # 返回温度值

# 控制蜂鸣器鸣叫
def makerobo_beep(x):
	bz.on()     # 打开蜂鸣器控制
	sleep(x)   # 延时时间
	bz.off()    # 关闭蜂鸣器控制
	sleep(x)   # 延时时间

# 无限循环函数
def makerobo_loop():
    while True:
        makerobo_edge()       #  调用计算函数
        ds_temp = makerobo_read()  # 读取温度值
        if is_in_closed_range(ds_temp, -20.0, 100.0):   # 排除错误的温度值
            print ('Makerobo The lower limit of temperature : ', ds_lowl)    # 打印出下限值
            print ('Makerobo The upper limit of temperature : ', ds_highl)   # 打印出上限值
            print ('Makerobo Current temperature : ', ds_temp)               # 打印读取DS18B20温度值
            if float(ds_temp) < float(ds_lowl):                              # 当实际温度值小于下限值，驱动蜂鸣器发出警报
                led.color = Color('blue')                                    # RGB—LED 显示蓝色              
                for i in range(0, 3):
                    makerobo_beep(0.5)                                       # 蜂鸣器发出叫声
            if ds_temp >= float(ds_lowl) and ds_temp < float(ds_highl):      # 当实际温度值在上下限值之内，则工作正常
                led.color = Color('green')                                   # RGB—LED 显示绿色
            if ds_temp >= float(ds_highl):                                   #  当实际温度值大于上限值
                led.color = Color('red')                                     # RGB—LED 显示红色
                for i in range(0, 3):
                    makerobo_beep(0.1)                                      #  蜂鸣器发出叫声   
# 释放函数
def makerobo_destroy():
    led.close()




# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        makerobo_setup()                                                # 调用初始化
        makerobo_loop()                                                 # 调用循环函数
    except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
        makerobo_destroy()     #  释放资源


# In[ ]:




