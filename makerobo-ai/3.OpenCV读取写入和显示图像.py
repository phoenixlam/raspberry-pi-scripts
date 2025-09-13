#!/usr/bin/env python
# coding: utf-8

# <center><img src="../image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 3.OpenCV读取写入和显示图像
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：3.OpenCV读取写入和显示图像.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：OpenCV读取写入和显示图像
# OpenCV 读取写入和显示图像属于OpenCV的基础知识之一，我们必须熟悉这些函数的使用！！！<br>

# ## 导入OpenCV 库

# In[3]:


import cv2
import numpy as np 


# ### 1、读取图像

# In[4]:


# 使用'imread'加载图像，指定图像
input = cv2.imread('./images/CLBLOGO.jpg')


# ### 2、显示图像操作

# In[5]:


# 载入显示库
import ipywidgets.widgets as widgets
from IPython.display import display
image = widgets.Image(format='jpeg', width=640, height=480)
display(image)

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

# 显示图像
image.value = bgr8_to_jpeg(input)


# ### 3、保存图像

# In[6]:


# Import numpy 
import  numpy  as  np

print(input.shape)


# 形状表示图像数组的尺寸
# 2D尺寸是830像素高bv 1245像素宽。“3L”意味着有3个其他成分(RGB)组成了这个图像。

# In[7]:


# 让我们打印图像的每个尺寸
print('Height of Image:', int(input.shape[0]), 'pixels')
print('Width of Image: ', int(input.shape[1]), 'pixels')


# ### 如何在OpenCV中保存编辑过的图像?

# In[8]:


# 只需使用'imwrite'指定文件名和要保存的图像
cv2.imwrite('output.jpg', input)
cv2.imwrite('output.png', input)


# ### 4.使用Matplotlib显示图像
# Matplotlib是Python的绘图库，
# 
# 可为你提供多种绘图方法。你将在接下来的文章中看到它们。
# 
# 在这里，你将学习如何使用Matplotlib显示图像。你可以使用Matplotlib缩放图像，保存图像等。

# In[6]:


import matplotlib.pyplot as plt
img = cv2.cvtColor(input,cv2.COLOR_BGR2RGB)
plt.imshow(img),plt.title('Makerobo image',color='blue')
plt.xticks([]), plt.yticks([]) # 隐藏 x 轴和 y 轴上的刻度值
plt.show()

