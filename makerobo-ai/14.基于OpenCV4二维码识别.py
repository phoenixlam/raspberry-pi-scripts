#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 14.基于OpenCV 二维码识别
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：14.基于OpenCV 二维码识别.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：基于OpenCV 二维码识别<br>

# In[ ]:


# 载入必要的库
import cv2
import numpy as np
from pyzbar import pyzbar
import imutils
import sys
import time


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


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display

QR_img = widgets.Image(format='jpeg', width=320, height=240)
testQRCode_img = widgets.Image(format='jpeg', width=320, height=240)

dispaly_img = widgets.HBox([testQRCode_img,QR_img])
display(dispaly_img)


# ## 载入图片QR二维码

# In[ ]:


import cv2
image = cv2.imread('./images/testQRCode.png')
frame = imutils.resize(image, width=400)
barcodes = pyzbar.decode(frame)
for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(frame, text, (x, y-40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  
    testQRCode_img.value = bgr8_to_jpeg(frame)
    print(text)  


# ## 摄像头二维码实时识别

# In[ ]:


import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
#picamera.set_controls({"ExposureTime":info['ExposureTime'], "AnalogueGain":info['AnalogueGain'], "AwbMode":info['AwbMode'], "FrameDurationLimits": (100000, 100000)})
#picamera.set_controls({"ExposureTime": 50000, "AnalogueGain": 1.0, "ColourGains": (2.522, 1.897)})
picamera.start()


# In[ ]:


def Video_display():
    while True:
        frame1 = picamera.capture_array()
        frame = imutils.resize(frame1, width=400)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  
            print(text) 

        QR_img.value = bgr8_to_jpeg(frame) # 实时显示图像



# In[ ]:


# 开始线程
t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)


# In[ ]:




