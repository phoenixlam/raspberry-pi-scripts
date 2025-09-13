#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 6.OpenCV进行颜色检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：6.使用OpenCV在Python进行颜色检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：使用OpenCV在Python中进行颜色检测<br>

# ## 1、 颜色空间转换

# In[ ]:


# -*- coding: utf-8 -*-
import cv2 

flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(flags)


# ### 1.1 把BGR转换为HSV颜色空间

# In[ ]:


import sys
import numpy as np
import cv2

print("Please enter blue:")
blue = input()
print("Please enter green:")
green = input()
print("Please enter red:")
red = input()

color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

hue = hsv_color[0][0][0]

print("Lower bound is :")
print("[" + str(hue-10) + ", 100, 100]\n")

print("Upper bound is :"),
print("[" + str(hue + 10) + ", 255, 255]")


# ### 1.2 OpenCV颜色检测

# In[ ]:


import cv2
import numpy as np

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

# 创建显示控件
import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
mask_image = widgets.Image(format='jpeg', width=640, height=480)
image = widgets.Image(format='jpeg', width=640, height=480)
# 放置一个水平容器，让图片水平放置
image_container = widgets.HBox([image,mask_image])
display(image_container)


# In[ ]:


# 1表示我们想要BGR中的图像
img = cv2.imread('./images/makerobo.jpg', 1)

# 将imag在每个轴上的大小调整为20%
img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
# 将BGR图像转换为HSV图像
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# NumPy来创建数组以保存上下范围
# dtype = np。“uint8”表示数据类型是8位整数

lower_range = np.array([24, 100, 100], dtype=np.uint8)
upper_range = np.array([44, 255, 255], dtype=np.uint8)

# 为图像创建一个遮罩
mask = cv2.inRange(hsv, lower_range, upper_range)

# 将遮罩和图像并排显示
mask_image.value = bgr8_to_jpeg(mask)
image.value = bgr8_to_jpeg(img)


# ## 2.OpenCV 中颜色物体追踪

# In[ ]:


# 导入必要的包
from collections import deque
import numpy as np
import argparse
import imutils
import cv2


# In[ ]:


# 线程函数操作库
import threading # 线程
import ctypes
import inspect


# In[ ]:


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


# 构造参数解析并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
args = vars(ap.parse_args(args=[]))


# In[ ]:


# 定义“黄色对象”的上下边界
# (或“球”)中的HSV颜色空间，然后初始化
# 跟踪点列表

colorLower = (24, 100, 100)
colorUpper = (44, 255, 255)
pts = deque(maxlen=args["buffer"])


# In[ ]:


import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
Frame = widgets.Image(format='jpeg', width=480, height=320)
display(Frame)


# In[ ]:


def Video_display():
    while True:
        frame = picamera.capture_array()
        # 调整帧大小，倒转(垂直翻转180度)，
        # 模糊它，并转换为HSV颜色空间
        frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        pts.appendleft(center)

        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue

            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)


        Frame.value = bgr8_to_jpeg(frame)

    camera.release()

t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)


# In[ ]:




