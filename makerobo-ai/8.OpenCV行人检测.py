#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 8.OpenCV实现行人检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：8.OpenCV行人检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV行人检测<br>

# In[1]:


# 载入必要的库
import cv2
import numpy as np

# 创建我们的身体分类器
body_classifier = cv2.CascadeClassifier('./images/haarcascade_fullbody.xml')


# In[2]:


# 为视频文件启动视频捕获
cap = cv2.VideoCapture('./images/walking.avi')


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


# In[5]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
Pedestrians_imge = widgets.Image(format='jpeg', width=480, height=320)
display(Pedestrians_imge)


# In[6]:


#一旦视频成功加载，循环播放
def Video_display():
    while cap.isOpened():
        # Read first frame
        ret, frame = cap.read()
        frame = cv2.resize(frame, None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Pass frame to our body classifier
        bodies = body_classifier.detectMultiScale(gray, 1.2, 3)

        # Extract bounding boxes for any bodies identified
        for (x,y,w,h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            Pedestrians_imge.value = bgr8_to_jpeg(frame)
    cap.release()


# In[7]:


t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[8]:


# 结束线程
stop_thread(t)


# In[ ]:




