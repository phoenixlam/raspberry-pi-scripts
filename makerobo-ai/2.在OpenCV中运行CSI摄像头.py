#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 2.在OpenCV 中调用CSI摄像头
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：2.在OpenCV 中调用CSI摄像头.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：使用picamera2库操作摄像头
# 我们来学习一下摄像头的开启方式之一吧，一般来说，对于我们使用摄像头的时候，首先我们需要测试我们的摄像头是否正常工作，画面是否清晰，让我们一起来测试我们的摄像头吧！！！<br>

# ## 1、打印出OPENCV 版本

# In[ ]:


import cv2
print(cv2.__version__)


# #Uncomment These next Two Line for Pi Camera

# In[ ]:


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])


# # 2.创建显示控件

# In[ ]:


import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
makerobo_image = widgets.Image(format='jpeg', width=640, height=480)
display(makerobo_image)


# # 3. 主程序

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

#while True:
frame = picamera.capture_array()
#makerobo_image.value = bgr8_to_jpeg(frame)
cv2.imwrite("makerobo.jpg", frame)

