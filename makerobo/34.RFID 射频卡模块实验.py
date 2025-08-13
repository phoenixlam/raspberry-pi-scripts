#!/usr/bin/env python
# coding: utf-8

# <center><img src="./image/CLBLOGO.jpg" alt="创乐博" style="width: 300px;"/></center>
# 
# # 34.RFID 射频卡模块实验
# 
# @－－－－湖南创乐博智能科技有限公司－－－－<br>
# @  文件名：35.RFID射频卡模块实验.py <br>
# @  版本：V2.0 <br>
# @  author: zhulin<br>
# @  说明：RFID 射频卡模块实验
# RFID射频模块属于串口通讯模块，对于树莓派操作我们只需要使用Serial串口通讯库进行相关操作即可，读取射频标签卡！！！<br>

# ## 1.导入必要的库文件

# In[ ]:


from gpiozero import LED
import serial


# ## 2.定义使能管脚和串口端口号

# In[ ]:


ENABLE_PIN  = 17              # ENABLE Pin GPIO17
# Sout Pin - Raspberry Pi 5 Uart RXI 
SERIAL_PORT = '/dev/ttyAMA0'  # The location of our serial port. 


ENABLE = LED(ENABLE_PIN)


# ## 3.定义功能函数

# In[ ]:


def validate_rfid(code):
    # A valid code will be 12 characters long with the first char being
    # a line feed and the last c har being a carriage return.
    s = code.decode("ascii")
    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        return s[1:-1]
    else:
        # We didn't match a valid code, so return False.
        return False


# ## 4.定义主函数

# In[ ]:


def main():
    print("Enabling RFID reader...\n")
    ENABLE.off()  # 使能ENABLE
    # Set up the serial port as per the makerobo reader's datasheet.
    ser = serial.Serial(baudrate = 2400,
                        bytesize = serial.EIGHTBITS,
                        parity   = serial.PARITY_NONE,
                        port     = SERIAL_PORT,
                        stopbits = serial.STOPBITS_ONE,
                        timeout  = 1)

    # Wrap everything in a try block to catch any exceptions.
    try:
        # Loop forever, or until CTRL-C is pressed.

        while 1:
            # Read in 12 bytes from the serial port.
            data = ser.read(12)
            # Attempt to validate the data we just read.
            code = validate_rfid(data)

            # If validate_rfid() returned a code, display it.
            if code:
                print("Read RFID code: " + code);
    except Exception:
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print ("Couldn't do it: %s" % e)
        print("Disabling RFID reader...")
        ENABLE.on()  # 关闭ENABLE


if __name__ == "__main__":
    main()


# In[ ]:




