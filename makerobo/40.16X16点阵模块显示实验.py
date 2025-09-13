#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 40.16X16点阵模块显示实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：40.16X16点阵模块显示实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：16X16点阵模块显示实验
# 16X16点阵模块显示实验，通过第三方自定义的adafruit_vl53l0x库操作该传感器模块，该传感器模块采用的是I2C的通讯方式，可以打印出测量的距离值！！！<br>

# ## 1.导入必要的库文件

# In[1]:


import board
import time
from PIL import Image
from adafruit_ht16k33 import matrix


# ## 2.实例化两个16x8的点阵模块

# In[2]:


i2c = board.I2C()
matrix1 = matrix.MatrixBackpack16x8(i2c)
matrix2 = matrix.MatrixBackpack16x8(i2c, address=0x71)
# 清空显示
matrix1.fill(0)
matrix2.fill(0)
# 设置闪烁频率和亮度
#display.blink_rate = 3
#display.brightness = 0.5


# ## 3. 功能函数

# In[3]:


def matrix_display():
    # 显示第一个字
    image1 = Image.open("./images/1_01.png")
    image2 = Image.open("./images/1_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

    # 显示第二个字
    image1 = Image.open("./images/2_01.png")
    image2 = Image.open("./images/2_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

    # 显示第三个字
    image1 = Image.open("./images/3_01.png")
    image2 = Image.open("./images/3_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

    # 显示第三个字
    image1 = Image.open("./images/4_01.png")
    image2 = Image.open("./images/4_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

    # 显示第三个字
    image1 = Image.open("./images/5_01.png")
    image2 = Image.open("./images/5_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

    # 显示第三个字
    image1 = Image.open("./images/6_01.png")
    image2 = Image.open("./images/6_02.png")
    matrix1.image(image1)
    matrix2.image(image2)
    for count in range(16):
        matrix1.shift_left(True)
        matrix2.shift_left(True)
        time.sleep(0.5)

def makerobo_destroy():
    matrix1.fill(0)
    matrix2.fill(0)



# ## 4.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        while True:
            matrix_display()        #  点阵显示函数
    except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
        makerobo_destroy()     #  释放资源


# In[ ]:




