#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 38.MAX30102脉搏血氧及心率传感器实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：38.MAX30102脉搏血氧及心率传感器实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：MAX30102脉搏血氧及心率传感器实验
# MAX30102脉搏血氧及心率传感器实验，通过第三方自定义的heartrate_monitor库操作该传感器模块，该传感器模块采用的是I2C的通讯方式，可以直接读取脉搏及血氧含量！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from heartrate_monitor import HeartRateMonitor
import time


# ## 2.初始化脉搏血氧仪心率传感器

# In[2]:


# 打印出一条信息说明传感器开始启动
print('Makerobo Max30102 Sensor starting...')
#设置持续读取时间
durationtime = 15


# ## 3.设置传感器输出信息

# In[3]:


# 初始化hearttratemonitor对象
# 将print_raw设置为False以避免打印原始数据
# 设置print_result为True，打印计算结果
makerobo_hrm = HeartRateMonitor(print_raw=False, print_result=True)


# ## 5.主程序

# In[5]:


# 程序入口
if __name__ == '__main__':
    # 开始读取传感器
    makerobo_hrm.start_sensor()
    try:
        time.sleep(durationtime)  # 持续时间
    except KeyboardInterrupt:
        print('keyboard interrupt detected, exiting...')

    # 在持续时间过去后停止传感器
    makerobo_hrm.stop_sensor()

    # 打印一条消息，表明传感器已停止
    print('Makerobo Max30102 Sensor stopped!')


# In[ ]:




