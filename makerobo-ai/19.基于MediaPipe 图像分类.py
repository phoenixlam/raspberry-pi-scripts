#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 19.基于MediaPipe图像分类
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：19.基于MediaPipe图像分类.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：基于MediaPipe图像分类<br>

# ## 1.载入必要的库文件

# In[ ]:


import cv2
import numpy as np
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ## 2.创建显示窗口

# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
classification_imge = widgets.Image(format='jpeg', width=1280, height=720)
display(classification_imge)


# ## 3.创建摄像头及检测模型

# In[ ]:


import libcamera
from picamera2 import Picamera2

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()

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

    # Label box parameters
    label_text_color = (0, 0, 0)  # red
    label_background_color = (255, 255, 255)  # white
    label_font_size = 1
    label_thickness = 2
    label_width = 50  # pixels
    label_rect_size = 16  # pixels
    label_margin = 40
    label_padding_width = 600  # pixels

    classification_frame = None
    classification_result_list = []

    def save_result(result: vision.ImageClassifierResult, unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME
        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        classification_result_list.append(result)
        COUNTER += 1

    # Initialize the image classification model
    base_options = python.BaseOptions(model_asset_path='efficientnet_lite0.tflite')
    options = vision.ImageClassifierOptions(base_options=base_options,
                                          running_mode=vision.RunningMode.LIVE_STREAM,
                                          max_results=5,
                                          score_threshold=0.5,
                                          result_callback=save_result)
    classifier = vision.ImageClassifier.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while True:
        frame = picamera.capture_array()
        image = cv2.flip(frame, 1)
        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run image classifier using the model.
        classifier.classify_async(mp_image, time.time_ns() // 1_000_000)

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(FPS)
        text_location = (left_margin, row_size)
        current_frame = image
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,font_size, text_color, font_thickness, cv2.LINE_AA)

        # Initialize the origin coordinates of the label.
        legend_x = current_frame.shape[1] + label_margin
        legend_y = current_frame.shape[0] // label_width + label_margin

        # Expand the frame to show the labels.
        current_frame = cv2.copyMakeBorder(current_frame, 0, 0, 0, label_padding_width,cv2.BORDER_CONSTANT, None,label_background_color)

        # Show the labels on right-side frame.
        if classification_result_list:
            # Show classification results.
            for idx, category in enumerate(classification_result_list[0].classifications[0].categories):
                category_name = category.category_name
                score = round(category.score, 2)
                result_text = category_name + ' (' + str(score) + ')'

                label_location = legend_x + label_rect_size + label_margin, legend_y + label_margin
                cv2.putText(current_frame, result_text, label_location,cv2.FONT_HERSHEY_DUPLEX, label_font_size, label_text_color,label_thickness, cv2.LINE_AA)
                legend_y += (label_rect_size + label_margin)


            classification_frame = current_frame
            classification_result_list.clear()

        if classification_frame is not None:
            classification_imge.value = bgr8_to_jpeg(classification_frame)

    classifier.close()


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

