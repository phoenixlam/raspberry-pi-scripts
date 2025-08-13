#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 39.VL53L0X ToF激光雷达距离传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：39.VL53L0X ToF激光雷达距离传感器.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：VL53L0X ToF激光雷达距离传感器
# VL53L0X ToF激光雷达距离传感器，通过第三方自定义的adafruit_vl53l0x库操作该传感器模块，该传感器模块采用的是I2C的通讯方式，可以打印出测量的距离值！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


import time
import board
import busio
import adafruit_vl53l0x


# ## 2.实例化I2C设备和初始化激光测距传感器模块

# In[ ]:


pii2c = busio.I2C(board.SCL, board.SDA)
makerobo_vl53 = adafruit_vl53l0x.VL53L0X(pii2c)


# ## 3.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        # 循环持续输出距离值
        while True:
            print("Range: {0}mm".format(makerobo_vl53.range))   # 打印出距离值
            time.sleep(1.0)                                     # 延时1s
    except KeyboardInterrupt:
        print("Exit")  # Exit on CTRL+C


# In[ ]:




