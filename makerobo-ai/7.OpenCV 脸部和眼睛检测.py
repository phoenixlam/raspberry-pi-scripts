#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 7.OpenCV脸部和眼睛检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：7.OpenCV脸部和眼睛检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV脸部和眼睛检测<br>

# In[ ]:


# 导入必要的库
import numpy as np
import cv2


# In[ ]:


# 载入HAAR模型
face_cascade = cv2.CascadeClassifier('./images/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./images/haarcascade_eye.xml')


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
face_imge = widgets.Image(format='jpeg', width=480, height=320)
display(face_imge)


# In[ ]:


def Video_display():
    while True:      
        frame = picamera.capture_array()
        img = cv2.flip(frame,1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            print(int(x+w/2), int(y+h/2))
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        face_imge.value = bgr8_to_jpeg(img)
    cap.release()


# In[ ]:


t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)


# In[ ]:




