#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 10.OpenCV车牌检测
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：10.OpenCV车牌检测.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV实现汽车检测<br>

# In[1]:


import cv2
import imutils
import numpy as np
import pytesseract


# In[2]:


img  = cv2.imread('./images/makecar.jpg',cv2.IMREAD_COLOR)


# In[3]:


img = cv2.resize(img, (600,400) )


# In[4]:


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
gray = cv2.bilateralFilter(gray, 13, 15, 15) 


# In[5]:


edged = cv2.Canny(gray, 30, 200) 
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None


# In[6]:


# 载入显示库
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

import ipywidgets.widgets as widgets
from IPython.display import display
imagecar = widgets.Image(format='jpeg', width=600, height=400)
imageCropped = widgets.Image(format='jpeg', width=600, height=400)
display(imagecar)
display(imageCropped)


# In[7]:


for c in contours:

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No contour detected")
else:
     detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]

text = pytesseract.image_to_string(Cropped, config='--psm 11')
print("programming_fever's License Plate Recognition\n")
print("Detected license plate Number is:",text)
img = cv2.resize(img,(500,300))
Cropped = cv2.resize(Cropped,(400,200))
# 显示图像
imagecar.value = bgr8_to_jpeg(img)
imageCropped.value = bgr8_to_jpeg(Cropped)


# In[ ]:




