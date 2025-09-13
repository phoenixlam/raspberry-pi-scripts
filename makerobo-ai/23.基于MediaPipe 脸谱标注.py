#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 23.基于MediaPipe 脸谱标注
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：23.基于MediaPipe脸谱标注.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：23.基于MediaPipe脸谱标注<br>

# ## 1.载入必要的库文件

# In[ ]:


import time
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2


# ## 2.创建显示窗口

# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge = widgets.Image(format='jpeg', width=1280, height=960)
display(face_imge)


# ## 3.创建摄像头及检测模型

# In[ ]:


import libcamera
from picamera2 import Picamera2

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
DETECTION_RESULT = None

def run():
    # Start capturing video input from the camera
    picamera = Picamera2()
    config = picamera.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 960)},
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
    label_background_color = (255, 255, 255)  # White
    label_padding_width = 1500  # pixels



    def save_result(result: vision.FaceLandmarkerResult,unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME, DETECTION_RESULT
        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        DETECTION_RESULT = result
        COUNTER += 1

    # Initialize the image classification model
    base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
    options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_faces=2,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            output_face_blendshapes=True,
            result_callback=save_result)

    detector = vision.FaceLandmarker.create_from_options(options)

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
            # Draw landmarks.
            for face_landmarks in DETECTION_RESULT.face_landmarks:
                face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                face_landmarks_proto.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x,y=landmark.y,z=landmark.z) for landmark in face_landmarks])
                mp_drawing.draw_landmarks(image=current_frame,landmark_list=face_landmarks_proto,connections=mp_face_mesh.FACEMESH_TESSELATION,landmark_drawing_spec=None,connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(image=current_frame,landmark_list=face_landmarks_proto,connections=mp_face_mesh.FACEMESH_CONTOURS,landmark_drawing_spec=None,connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(image=current_frame,landmark_list=face_landmarks_proto,connections=mp_face_mesh.FACEMESH_IRISES,landmark_drawing_spec=None,connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style())

        # Expand the right side frame to show the blendshapes.
        current_frame = cv2.copyMakeBorder(current_frame, 0, 0, 0,label_padding_width,cv2.BORDER_CONSTANT, None,label_background_color)

        if DETECTION_RESULT:
            # Define parameters for the bars and text
            legend_x = current_frame.shape[1] - label_padding_width + 20
            legend_y = 30 
            bar_max_width = label_padding_width - 40
            bar_height = 8  # Height of the bar
            gap_between_bars = 5  # Gap between two bars
            text_gap = 5  # Gap between the end of the text and the start of the bar

            face_blendshapes = DETECTION_RESULT.face_blendshapes

            if face_blendshapes:
                for idx, category in enumerate(face_blendshapes[0]):
                    category_name = category.category_name
                    score = round(category.score, 2)
                    # Prepare text and get its width
                    text = "{} ({:.2f})".format(category_name, score)
                    (text_width, _), _ = cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,0.4, 1)
                    # Display the blendshape name and score
                    cv2.putText(current_frame, text,(legend_x, legend_y + (bar_height // 2) + 5),
                                # Position adjusted for vertical centering
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.4,  # Font size
                                (0, 0, 0),  # Black color
                                1,
                                cv2.LINE_AA)  # Thickness
                    # Calculate bar width based on score
                    bar_width = int(bar_max_width * score)

                    # Draw the bar to the right of the text
                    cv2.rectangle(current_frame,(legend_x + text_width + text_gap, legend_y),(legend_x + text_width + text_gap + bar_width,legend_y + bar_height),
                                  (0, 255, 0),  # Green color
                                  -1)  # Filled bar
                    # Update the Y-coordinate for the next bar
                    legend_y += (bar_height + gap_between_bars)

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

