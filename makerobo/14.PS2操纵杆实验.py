#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 14.PS2 操纵杆实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：14.PS2操纵杆实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：PS2操纵杆实验
# PS2操纵杆实验，通过GPIOZero库自带的MCP3008 10位模数转换库直接控制，分别检测到PS2操纵杆的X分量和Y分量，从而判断方向！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import Button, MCP3008
from gpiozero.tools import absoluted, scaled
from signal import pause
from time import sleep


# ## 2.定义使用通道
pot_x = MCP3008(channel=0) # 定义PS2操纵杆对应的X方向管脚
pot_y = MCP3008(channel=1) # 定义PS2操纵杆对应的y方向管脚
pot_z = MCP3008(channel=2) # 定义PS2操纵杆对应的z方向管脚


# ## 3.定义方向函数
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


# ## 4.循环函数

# 循环函数
def makerobo_loop():
    makerobo_status = ''    # 状态值赋空值
    while True:
        makerobo_tmp = makerobo_direction()   # 调用方向判断函数
        sleep(0.2)
        if makerobo_tmp != None and makerobo_tmp != makerobo_status:  # 判断状态是否发生改变
            print (makerobo_tmp) # 打印出方向位
            makerobo_status = makerobo_tmp # 把当前状态赋给状态值，以防止同一状态多次打印

# 异常处理函数
def destroy():
	pass

# ## 5.主程序


# 程序入口
if __name__ == '__main__':		
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()   # 调用释放函数
