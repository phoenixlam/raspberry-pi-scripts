#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 11.OpenCV 定位物体的实时位置
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：11.OpenCV定位物体的实时位置.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV定位物体的实时位置<br>

# In[ ]:


# 载入必要的库文件
from __future__ import print_function
from gpiozero import LED
from adafruit_servokit import ServoKit
from imutils.video import VideoStream
import imutils
import time
import cv2
import os


# In[ ]:


kit = ServoKit(channels=16)

# 舵机调零
pan =  90
tilt = 60    # 往上仰，方便操作
# 初始化位置
kit.servo[0].angle=pan
kit.servo[1].angle=tilt

# LED 初始化
redLed = LED(19)


# In[ ]:


# 打印物体的实时位置
def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))


# In[ ]:


import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()

time.sleep(2.0)


# In[ ]:


# 定义对象的上下边界
# 在HSV颜色空间中进行跟踪
colorLower = (9,135,231)
colorUpper = (31,255,255)


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
Frame = widgets.Image(format='jpeg', width=500, height=350)
display(Frame)


# In[ ]:


# 线程函数操作库
import threading # 线程
import ctypes
import inspect

# 线程结束代码
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# In[ ]:


# 关闭LED灯
redLed.off()
ledOn = False


# In[ ]:


def Video_display():
    global ledOn
    # 循环的帧从视频流
    while True:
        # 从视频流中抓取下一帧，调整大小
        # 帧，并将其转换为HSV颜色空间
        frame = picamera.capture_array()
        frame = imutils.resize(frame, width=500)
        frame = imutils.rotate(frame, angle=0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 为对象颜色构造一个遮罩，然后执行
        # 一系列的膨胀和侵蚀，以消除任何小的
        # blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 找到遮罩中的轮廓并初始化
        # (x, y) center of the object
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        #cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None

        # 只有在找到至少一条轮廓线时才进行
        if len(cnts) > 0:
            # 在蒙版中找到最大的轮廓，然后使用
            # 它可以计算出最小的围圆
            # 重心
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # 只有当半径满足最小尺寸时才进行
            if radius > 10:
                # 在框架上画圆和质心，
                # 然后更新跟踪点的列表
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # 定位舵机在圆心
                mapObjectPosition(int(x), int(y))

                # 如果led还没有打开，打开led
                if not ledOn:
                    redLed.on()
                    ledOn = True
        # 如果没有检测到球，关闭LED灯
        elif ledOn:
            redLed.off()
            ledOn = False

        # 向我们的屏幕显示框架
        Frame.value = bgr8_to_jpeg(frame) 
        time.sleep(0.01)                # 不要CPU 占用太高
    # 做点清理工作
    print("\n [INFO] Exiting Program and cleanup stuff \n")


# In[ ]:


# 开始线程
t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)

