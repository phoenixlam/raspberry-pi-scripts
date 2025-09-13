#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 13.OpenCV 摄像头云台人脸追踪
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：13.OpenCV摄像头云台人脸追踪.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV摄像头云台人脸追踪<br>

# In[1]:


# 载入必要的库
import cv2
import numpy as np
from adafruit_servokit import ServoKit
import time


# In[2]:


kit = ServoKit(channels=16)


# In[3]:


pan =  90
tilt = 90
# 初始化位置
kit.servo[0].angle=pan
kit.servo[1].angle=tilt


# In[4]:


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


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display

frame_img = widgets.Image(format='jpeg', width=320, height=240)
display(frame_img)


# In[6]:


import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()

dispW  = 320
dispH = 240


# In[7]:


# 载入人脸和眼睛的HAAR 模型
face_cascade = cv2.CascadeClassifier('./images/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./images/haarcascade_eye.xml')


# In[8]:


def Video_display():
    global pan
    global tilt
    while True: 
        frame = picamera.capture_array()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            Xcent = x + w/2
            Ycent = y + h/2
            errorPan  = Xcent - dispW/2 
            errorTilt = Ycent - dispH/2
            if abs(errorPan)>15:
                pan=pan-errorPan/50
            if abs(errorTilt)>15:
                tilt=tilt-errorTilt/50
            if pan > 180:
                pan = 180
                print("Pan out of Range")
            if pan < 0:
                pan = 0
                print("pan Out of Range")
            if tilt > 180:
                tilt = 180
                print("Pan out of Range")
            if tilt < 0:
                tilt = 0
                print("pan Out of Range")

            kit.servo[0].angle=180-pan
            kit.servo[1].angle=180-tilt

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]        
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)          
        frame_img.value = bgr8_to_jpeg(frame)
    cap.release()


# In[9]:


# 开始线程
t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[10]:


# 结束线程
stop_thread(t)


# In[ ]:




