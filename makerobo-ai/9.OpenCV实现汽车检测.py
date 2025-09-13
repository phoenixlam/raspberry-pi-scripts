#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 9.OpenCV实现汽车检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：9.OpenCV实现汽车检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV实现汽车检测<br>

# In[1]:


# 载入必要的库
import cv2
import time
import numpy as np


# In[2]:


# 载入HAAR分类器
car_classifier = cv2.CascadeClassifier('./images/haarcascade_car.xml')
# 载入视频文件
cap = cv2.VideoCapture('./images/cars.avi')


# In[3]:


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


# In[4]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
car_imge = widgets.Image(format='jpeg', width=480, height=320)
display(car_imge)


# In[5]:


#一旦视频成功加载，循环播放
def car_Video_display():
    while cap.isOpened():
        time.sleep(.05)
        # Read first frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Pass frame to our car classifier
        cars = car_classifier.detectMultiScale(gray, 1.4, 2)       
        # Extract bounding boxes for any bodies identified
        for (x,y,w,h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            car_imge.value = bgr8_to_jpeg(frame)
    cap.release()


# In[6]:


t = threading.Thread(target=car_Video_display)
t.setDaemon(True)
t.start()


# In[7]:


# 结束线程
stop_thread(t)


# In[ ]:




