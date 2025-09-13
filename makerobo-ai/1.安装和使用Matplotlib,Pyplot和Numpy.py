#!/usr/bin/env python
# coding: utf-8

# <center><img src="./images/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 1.安装和使用Matplotlib、Pyplot和Numpy
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：1.安装和使用Matplotlib、Pyplot和Numpy.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：使用Matplotlib、Pyplot和Numpy
# 我们来学习一下AI人工智能的先导性课程，Matplotlib、Pyplot和Numpy的使用！！<br>

# ## 1.载入库文件

# In[1]:


import matplotlib.pyplot as plt
import numpy as np


# ## 2. 绘制函数

# In[2]:


x=np.arange(0,2*np.pi,.1)
y=np.sin(x)
y2=np.cos(x)
y3=np.square(x)+4
plt.grid(True)
plt.xlabel('My X Values')
plt.ylabel('My Y Values')
plt.title('My First Graph')
#plt.axis([0,5,2,11])
plt.plot(x,y,'b-^',linewidth=3,markersize=7,label='Sin(x)')
plt.plot(x,y2,'r-^',linewidth=3,markersize=7,label='Cos(x)')
#plt.plot(x,y3,'g-^',linewidth=3,markersize=7,label='Green Line')
plt.legend(loc='upper center')
plt.show()


# In[ ]:




