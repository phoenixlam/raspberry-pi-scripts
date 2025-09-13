#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 4.OpenCV的读取、显示和保存视频
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：4.OpenCV读取显示和保存视频.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV基础，读取显示和保存视频操作！<br>

# ## 1、用摄像头捕获视频

# In[ ]:


# 载入库
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

# 线程函数操作库
import threading # 线程
import ctypes
import inspect


# ### 1.1  创建显示控件

# In[ ]:


import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
makerobo_image = widgets.Image(format='jpeg', width=640, height=480)
display(makerobo_image)


# ### 1.2 线程的结束代码

# In[ ]:


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


# ### 1.3 动态显示摄像头视频

# In[ ]:


import numpy as np
import time
import ipywidgets.widgets as widgets
import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()

def Video_display():
    while True:
        frame = picamera.capture_array()
        makerobo_image.value = bgr8_to_jpeg(frame)
    # 
    cap.release()


# ### 1.4.开启线程

# In[ ]:


t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# ### 1.5 结束线程

# In[ ]:


stop_thread(t)


# ## 2、从文件中播放视频

# In[ ]:


# -*- coding: utf-8 -*-
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import numpy as np
import cv2


# In[ ]:


import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_image = widgets.Image(format='jpeg', width=640, height=480)
display(face_image)


# In[ ]:


cap = cv2.VideoCapture('./images/walking.avi')

while cap.isOpened():
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv2.flip(frame,4)
    face_image.value = bgr8_to_jpeg(frame)



# ## 3.保存视频

# In[ ]:


# 载入库
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])


# In[ ]:


import numpy as np
import time
import ipywidgets.widgets as widgets
import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()


# In[ ]:


import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
makerobo_image = widgets.Image(format='jpeg', width=640, height=480)
display(makerobo_image)


# In[ ]:


# 定义编解码器并创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while True:
    frame = picamera.capture_array()
    frame = cv2.flip(frame, 4)
    # 写翻转的框架
    out.write(frame)
    makerobo_image.value = bgr8_to_jpeg(frame)

# 完成工作后释放所有内容
cap.release()
out.release()

