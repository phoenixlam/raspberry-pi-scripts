#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 31.MPU6050陀螺仪加速度传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：31.MPU6050陀螺仪加速度传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：MPU6050陀螺仪加速度传感器实验
# MPU6050陀螺仪加速度传感器实验，mpu6050库进行操作，进行I2C控制方式，控制MPU6050陀螺仪加速度传感器，并在界面上打印出对应的加速度速度和陀螺仪数据！！！！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from mpu6050 import mpu6050
from time import sleep


# ## 2.初始化工作

# In[ ]:


# 初始化I2C地址为0x68的MPU-6050传感器
makerobo_sensor = mpu6050(0x68)


# ## 3.循环函数

# In[ ]:


# 循环函数
def makerobo_loop():
    try:
        while True:
            # 从传感器中检索加速度计数据。
            accel_data = makerobo_sensor.get_accel_data()
            # 从传感器中检索陀螺仪数据。
            gyro_data = makerobo_sensor.get_gyro_data()
            # 从传感器检索温度数据。
            temp = makerobo_sensor.get_temp()

            # 打印加速度计数据。
            print("Accelerometer data")
            print("x: " + str(accel_data['x']))
            print("y: " + str(accel_data['y']))
            print("z: " + str(accel_data['z']))

            # 打印陀螺仪数据。
            print("Gyroscope data")
            print("x: " + str(gyro_data['x']))
            print("y: " + str(gyro_data['y']))
            print("z: " + str(gyro_data['z']))

            # 以摄氏度打印温度
            print("Temp: " + str(temp) + " C")

            # 在下一个读取周期之前暂停0.5秒。
            sleep(0.5)
    except KeyboardInterrupt:
        print("Exit")  # Exit on CTRL+C


# ## 4.程序入口

# In[ ]:


# 程序入口
if __name__ == "__main__":
	try:
		makerobo_loop()       # 循环显示信息
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		print("Exit")  # Exit on CTRL+C


# In[ ]:




