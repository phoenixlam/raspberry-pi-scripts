#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 5.OpenCV绘图函数使用
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：5.OpenCV绘图函数使用.ipynb <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV绘图函数使用<br>
# 

# ## 1.画线
# 让我们在黑色方块上画一条线
# cv2.line(image, starting cordinates, ending cordinates, color, thickness)

# In[1]:


# 载入库
import cv2
import numpy as np
from matplotlib import pyplot as plt


# In[2]:


# 画一条5像素的对角蓝线
image = np.zeros((512,512,3), np.uint8)
#cv2.line(image, (startposition), (endposition), (Farbe der Linie), Linienbreite)
cv2.line(image, (0,0), (511,511), (255,127,0), 5)
cv2.line(image, (511,0), (0,511), (255,127,0), 5)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('Blue Line')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()


# ## 2.画矩形图形
# 现在让我们画一个矩形<br>
# cv2.rectangle(image, starting vertex, opposite vertex, color, thickness)

# In[3]:


# 绘制一个矩形
image = np.zeros((512,512,3), np.uint8)
# eine negative Linienbreite füllt das viereck aus
cv2.rectangle(image, (100,100), (300,250), (127,50,127), -1)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('Rectangle')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()


# ## 3.绘制圆
# cv2.cirlce(image, center, radius, color, fill)

# In[4]:


image = np.zeros((512,512,3), np.uint8)
#cv2.circle(image, (Zentrum), Radius, (15,75,50), -1) 
cv2.circle(image, (350, 350), 100, (15,75,50), 10) 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('Circle')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()


# ## 4.绘制椭圆
# 

# In[5]:


image = np.zeros((512,512,3), np.uint8)
cv2.ellipse(image,(256,256),(100,50),0,0,180,255,-1)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('ellipse')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()


# ## 5.绘制多边形

# In[6]:


mage = np.zeros((512,512,3), np.uint8)

# 让我们定义四个点
pts = np.array( [[10,50], [400,50], [90,200], [50,500]], np.int32)

print(pts.shape)
# 现在让我们以折线
pts = pts.reshape((-1,1,2))
print(pts.shape)

cv2.polylines(image, [pts], True, (0,0,255), 3)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('Polygon')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()


# ### 6.在图片上增加文字
# cv2.putText(image, 'Text to Display', bottom left starting point, Font, Font Size, Color, Thickness)
# 
# - FONT_HERSHEY_SIMPLEX, FONT_HERSHEY_PLAIN
# - FONT_HERSHEY_DUPLEX,FONT_HERSHEY_COMPLEX 
# - FONT_HERSHEY_TRIPLEX, FONT_HERSHEY_COMPLEX_SMALL
# - FONT_HERSHEY_SCRIPT_SIMPLEX
# - FONT_HERSHEY_SCRIPT_COMPLEX

# In[7]:


image = np.zeros((512,512,3), np.uint8)

cv2.putText(image, 'Hello World!', (75,290), cv2.FONT_HERSHEY_COMPLEX, 2, (100,170,0), 3)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image),plt.title('Hello World!')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()

