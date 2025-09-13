#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 36.步进电机驱动模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：36.步进电机驱动模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：步进电机驱动后模块实验
# 步进电机驱动模块实验，gpiostepper步进电机驱动库，可以方便控制步进电机的速度、方向等！！！<br>

# ## 1.导入必要的库文件

# In[1]:


from time import sleep
from gpiostepper import Stepper


# ## 2.定义步进电机管脚

# In[2]:


speed = 300
print("Speed: {} rpm".format(speed))
number_of_steps = 32
step_motor1 = Stepper(motor_pins=[17, 18, 19, 20], number_of_steps = number_of_steps)


# ## 3.初始化

# In[3]:


step_motor1.set_speed(speed)  # 设置速度
amount_of_gear_reduction = 64 # Gear ratios?
number_of_steps_per_revolution_geared_output = number_of_steps * amount_of_gear_reduction


# ## 4.定义功能函数

# In[4]:


# 步进电机旋转
def makerobo_rotary(clb_direction):
    if(clb_direction == 'a'):     # 逆时针旋转
        step_motor1.step(number_of_steps_per_revolution_geared_output)
        sleep(1)

    elif(clb_direction == 'c'):    # 顺时针旋转
        step_motor1.step(-number_of_steps_per_revolution_geared_output)
        sleep(1)

# 循环函数
def makerobo_loop():
    while True:
        clb_direction = input('Makerobo select motor direction a=anticlockwise, c=clockwise: ')
        if(clb_direction == 'c'):
            print('Makerobo motor running clockwise\n')       # 顺时针旋转
            break
        elif(clb_direction == 'a'):
            print('Makerobo motor running anti-clockwise\n')  # 逆时针旋转
            break
        else:
            print('Makerobo input error, please try again!') # 输入错误，再次输入
    while True:
        makerobo_rotary(clb_direction)       # 让步进电机旋转


# ## 5.主程序

# In[ ]:


# 程序入口
if __name__ == '__main__':
    try:
        makerobo_loop()  # 循环函数
    except KeyboardInterrupt:   # 当按下Ctrl+C时，将执行destroy()子程序。
        pass  


# In[ ]:





# In[ ]:




