#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 16.基于Dlib玩转人脸身份识别
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：16.基于Dlib玩转人脸身份识别.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：16.基于Dlib玩转人脸身份识别<br>

# ## 1.人脸识别库识别人脸

# In[ ]:


import face_recognition
import cv2
print(cv2.__version__)


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


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge = widgets.Image(format='jpeg', width=640, height=480)
display(face_imge)


# In[ ]:


image=face_recognition.load_image_file('./unknown/u13.jpg')
face_locations=face_recognition.face_locations(image)
print(face_locations)
image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
for(row1,col1,row2,col2) in face_locations:
    cv2.rectangle(image,(col1,row1),(col2,row2),(0,0,255),2)
face_imge.value = bgr8_to_jpeg(image)


# ## 2.人脸身份识别

# In[ ]:


import face_recognition
import cv2
print(cv2.__version__)


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge1 = widgets.Image(format='jpeg', width=640, height=480)
display(face_imge1)


# In[ ]:


donFace=face_recognition.load_image_file('./known/Donald Trump.jpg')
donEncode = face_recognition.face_encodings(donFace)[0]

nancyFace=face_recognition.load_image_file('./known/Nancy Pelosi.jpg')
nancyEncode = face_recognition.face_encodings(nancyFace)[0]

penceFace=face_recognition.load_image_file('./known/Mike Pence.jpg')
penceEncode = face_recognition.face_encodings(penceFace)[0]

zhulinFace=face_recognition.load_image_file('./known/zhulin.jpg')
zhulinEncode = face_recognition.face_encodings(zhulinFace)[0]

Encodings=[donEncode,nancyEncode,penceEncode,zhulinEncode]
Names=['The Donald','Nancy Pelosi','Mike Pence','zhulin']

font = cv2.FONT_HERSHEY_SIMPLEX
testImage=face_recognition.load_image_file('./unknown/u13.jpg')
facePositions=face_recognition.face_locations(testImage)
allEncodings=face_recognition.face_encodings(testImage,facePositions)

testImage=cv2.cvtColor(testImage,cv2.COLOR_RGB2BGR)


# In[ ]:


for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
    name='Unknown Person'
    matches=face_recognition.compare_faces(Encodings,face_encoding)
    if True in matches:
        first_match_index=matches.index(True)
        name=Names[first_match_index]
    cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
    cv2.putText(testImage,name,(left,top-6),font,.75,(0,255,255),2)
face_imge1.value = bgr8_to_jpeg(testImage)


# ## 3.人脸身份识别2

# In[ ]:


import face_recognition
import cv2
import os
print(cv2.__version__)


# In[ ]:


Encodings=[]
Names=[]
j=0


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge2 = widgets.Image(format='jpeg', width=640, height=480)
display(face_imge2)


# In[ ]:


image_dir='./known'
for root,dirs,files in os.walk(image_dir):
    print(files)
    for file in files:
        path = os.path.join(root,file)
        print(path)
        name=os.path.splitext(file)[0]
        print(name)
        person=face_recognition.load_image_file(path)
        encoding=face_recognition.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)
print(Names)

font=cv2.FONT_HERSHEY_SIMPLEX
image_dir='./unknown'
for root,dirs,files in os.walk(image_dir):
    for file in files:
        print(root)
        print(file)
        testImagePath=os.path.join(root,file)
        testImage=face_recognition.load_image_file(testImagePath)
        facePositions=face_recognition.face_locations(testImage)
        allEncodings=face_recognition.face_encodings(testImage,facePositions)
        testImage=cv2.cvtColor(testImage,cv2.COLOR_RGB2BGR)  
        for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
            name='Unknown Person'
            matches=face_recognition.compare_faces(Encodings,face_encoding)
            if True in matches:
                first_match_index=matches.index(True)
                name=Names[first_match_index]
            cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
            cv2.putText(testImage,name,(left,top-6),font,.75,(0,255,255),2)
        face_imge2.value = bgr8_to_jpeg(testImage)


# ## 4.在OpenCV中训练面部识别模型
# 生成训练模型

# In[ ]:


import face_recognition
import cv2
import os
import pickle
print(cv2.__version__)


# In[ ]:


Encodings=[]
Names=[]
j=0


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge3 = widgets.Image(format='jpeg', width=640, height=480)
display(face_imge3)


# In[ ]:


image_dir='./known'
for root,dirs,files in os.walk(image_dir):
    print(files)
    for file in files:
        path = os.path.join(root,file)
        print(path)
        name=os.path.splitext(file)[0]
        print(name)
        person=face_recognition.load_image_file(path)
        encoding=face_recognition.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)
print(Names)

with open('train.pkl','wb') as f:
    pickle.dump(Names,f)
    pickle.dump(Encodings,f)
Encodings=[]
Names=[]
with open('train.pkl','rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)

font=cv2.FONT_HERSHEY_SIMPLEX
image_dir='./unknown'


# In[ ]:


for root,dirs,files in os.walk(image_dir):
    for file in files:
        print(root)
        print(file)
        testImagePath=os.path.join(root,file)
        testImage=face_recognition.load_image_file(testImagePath)
        facePositions=face_recognition.face_locations(testImage)
        allEncodings=face_recognition.face_encodings(testImage,facePositions)
        testImage=cv2.cvtColor(testImage,cv2.COLOR_RGB2BGR)  
        for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
            name='Unknown Person'
            matches=face_recognition.compare_faces(Encodings,face_encoding)
            if True in matches:
                first_match_index=matches.index(True)
                name=Names[first_match_index]
            cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
            cv2.putText(testImage,name,(left,top-6),font,.75,(0,255,255),2)
        face_imge3.value = bgr8_to_jpeg(testImage)


# ## 5.在OpenCV中直接调用面部识别训练模型
# ### 直接导入模型进行识别

# In[ ]:


import face_recognition
import cv2
import os
import pickle
print(cv2.__version__)


# In[ ]:


j=0
Encodings=[]
Names=[]


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge4 = widgets.Image(format='jpeg', width=640, height=480)
display(face_imge4)


# In[ ]:


with open('train.pkl','rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)

font=cv2.FONT_HERSHEY_SIMPLEX
image_dir='./unknown'


# In[ ]:


for root,dirs,files in os.walk(image_dir):
    for file in files:
        print(root)
        print(file)
        testImagePath=os.path.join(root,file)
        testImage=face_recognition.load_image_file(testImagePath)
        facePositions=face_recognition.face_locations(testImage)
        allEncodings=face_recognition.face_encodings(testImage,facePositions)
        testImage=cv2.cvtColor(testImage,cv2.COLOR_RGB2BGR)  
        for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
            name='Unknown Person'
            matches=face_recognition.compare_faces(Encodings,face_encoding)
            if True in matches:
                first_match_index=matches.index(True)
                name=Names[first_match_index]
            cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
            cv2.putText(testImage,name,(left,top-6),font,.75,(0,255,255),2)
        face_imge4.value = bgr8_to_jpeg(testImage)


# ## 6.通过摄像头进行面部身份识别

# ## 为了可以打开摄像头，这里关闭摄像头所有进程

# In[ ]:


import face_recognition
import cv2
import os
import pickle
import time
print(cv2.__version__)
fpsReport=0
scaleFactor=.25


# In[ ]:


# 创建显示控件
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
face_imge5 = widgets.Image(format='jpeg')#, width=320, height=240)
display(face_imge5)


# In[ ]:


Encodings=[]
Names=[]

with open('train.pkl','rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)

font=cv2.FONT_HERSHEY_SIMPLEX

import libcamera
from picamera2 import Picamera2

picamera = Picamera2()
config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)},
                                               raw={"format": "SRGGB12", "size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picamera.configure(config)
picamera.start()       # 开启摄像头

timeStamp=time.time()


# In[ ]:


while True:
    frame = picamera.capture_array()
    frameSmall=cv2.resize(frame,(0,0),fx=scaleFactor,fy=scaleFactor)
    frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
        name='Unkown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]

        top=int(top/scaleFactor)
        right=int(right/scaleFactor)
        bottom=int(bottom/scaleFactor)
        left=int(left/scaleFactor)

        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)

    dt = time.time()-timeStamp
    fps=1/dt
    fpsReport=.90*fpsReport + .1*fps
    #print('fps is:',round(fpsReport))
    timeStamp=time.time()
    cv2.rectangle(frame,(0,0),(100,40),(0,0,255),-1)
    cv2.putText(frame,str(round(fpsReport,1)) + 'fps',(0,25),font,.75,(0,255,255,2))
    face_imge5.value = bgr8_to_jpeg(frame)


# In[ ]:




