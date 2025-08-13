#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 24.超声波传感器距离检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：24.超声波传感器距离检测.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：超声波传感器距离检测
# 超声波传感器距离检测，通过GPIOZero库的超声波DistanceSensor库直接控制超声波传感器进行距离检测，从而打印在jupyter 界面上！！！！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import DistanceSensor
from time import sleep


# ## 2.定义超声波传感器管脚

# In[ ]:


makerobo_sensor = DistanceSensor(echo=17, trigger=18,max_distance=3, threshold_distance=0.2)


# ## 3.主程序

# In[ ]:


try:
    # 循环函数
    while True:
        dis = makerobo_sensor.distance * 100  # 测量距离值，并把m单位换成cm单位
        print('Distance: {:.2f} cm'.format(dis))  # 以两位小数精度打印距离
        sleep(0.3)  # 等待0.3秒再进行下一次测量

except KeyboardInterrupt:
    # 处理KeyboardInterrupt (Ctrl+C)以正常退出循环
    pass

