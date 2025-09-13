#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 22.基于MediaPipe 人脸识别
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：22.基于MediaPipe人脸识别.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：基于MediaPipe人脸识别<br>

# ## 1.载入必要的库文件

# In[ ]:


import time
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils2 import visualize


# ## 2.创建显示窗口

# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge = widgets.Image(format='jpeg', width=1280, height=720)
display(face_imge)


# ## 3.创建摄像头及检测模型

# In[ ]:


import libcamera
from picamera2 import Picamera2

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
DETECTION_RESULT = None

def run():
    # Start capturing video input from the camera
    picamera = Picamera2()
    config = picamera.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)},
                                                   raw={"format": "SRGGB12", "size": (1920, 1080)})
    config["transform"] = libcamera.Transform(hflip=0, vflip=1)
    picamera.configure(config)
    picamera.start()       # 开启摄像头

    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    def save_result(result: vision.FaceDetectorResult, unused_output_image: mp.Image,timestamp_ms: int):
        global FPS, COUNTER, START_TIME, DETECTION_RESULT
        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        DETECTION_RESULT = result
        COUNTER += 1

    # Initialize the image classification model
    base_options = python.BaseOptions(model_asset_path='blaze_face_short_range.tflite')
    options = vision.FaceDetectorOptions(base_options=base_options,
                                              running_mode=vision.RunningMode.LIVE_STREAM,
                                              min_detection_confidence=0.3,
                                              min_suppression_threshold=0.5,
                                              result_callback=save_result)

    detector = vision.FaceDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while True:
        image = picamera.capture_array()
        image = cv2.flip(image, 1)
        image = image.astype(np.uint8)
        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        raw_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)  # 强制格式为BGR

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run face detection using the model.
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(FPS)
        text_location = (left_margin, row_size)
        current_frame = raw_image
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,font_size, text_color, font_thickness, cv2.LINE_AA)

        if DETECTION_RESULT:
            # print(DETECTION_RESULT)
            current_frame = visualize(current_frame, DETECTION_RESULT)

        face_imge.value = bgr8_to_jpeg(current_frame)

    detector.close()


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


# 开始线程
t = threading.Thread(target=run)
t.setDaemon(True)
t.start()


# In[ ]:


# 结束线程
stop_thread(t)

