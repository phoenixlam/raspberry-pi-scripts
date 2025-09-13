#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 15.SSD Mobilenet V3 目标检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：15.SSD Mobilenet V3 目标检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：SSD Mobilenet V3 目标检测<br>

# ## 1、现成视频目标识别实时识别

# In[ ]:


# 载入必要的库
import cv2


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

detection_img = widgets.Image(format='jpeg', width=1920, height=1080)
display(detection_img)


# In[ ]:


config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)
classLabels = []
filename = 'labels.txt'
with open(filename, 'rt') as spt:
    classLabels = spt.read().rstrip('\n').split('\n')

model.setInputSize(320, 320)  #greater this value better the reults but slower. Tune it for best results
model.setInputScale(1.0/127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

cap = cv2.VideoCapture('test_video.mp4')
ret, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.avi', fourcc, 25, (frame.shape[1], frame.shape[0]))  #25 is the frame rate of output video you can change it as required


font = cv2.FONT_HERSHEY_PLAIN


# In[ ]:


def Video_display():
    while(True):
        ret, frame = cap.read()
        classIndex, confidence, bbox = model.detect(frame , confThreshold=0.65)  #tune the confidence  as required
        if(len(classIndex) != 0):
            for classInd, boxes in zip(classIndex.flatten(), bbox):
                cv2.rectangle(frame, boxes, (255, 0, 0), 2)
                cv2.putText(frame, classLabels[classInd-1], (boxes[0] + 10, boxes[1] + 40), font, fontScale = 1, color=(0, 255, 0), thickness=2)

        video.write(frame)
        detection_img.value = bgr8_to_jpeg(frame) # 实时显示图像                   


# In[ ]:


# 开始线程
t = threading.Thread(target=Video_display)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)


# ## 2、摄像头目标识别实时识别

# In[ ]:


import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()


# In[ ]:


pidetection_img = widgets.Image(format='jpeg', width=640, height=480)
display(pidetection_img)


# In[ ]:


def PiVideo_display():
    while(True):
        frame = picamera.capture_array()
        classIndex, confidence, bbox = model.detect(frame , confThreshold=0.65)  #tune the confidence  as required
        if(len(classIndex) != 0):
            for classInd, boxes in zip(classIndex.flatten(), bbox):
                cv2.rectangle(frame, boxes, (255, 0, 0), 2)
                cv2.putText(frame, classLabels[classInd-1], (boxes[0] + 10, boxes[1] + 40), font, fontScale = 1, color=(0, 255, 0), thickness=2)

        video.write(frame)
        pidetection_img.value = bgr8_to_jpeg(frame) # 实时显示图像  


# In[ ]:


# 开始线程
t1 = threading.Thread(target=PiVideo_display)
t1.setDaemon(True)
t1.start()


# In[ ]:


# 结束线程
stop_thread(t1)

