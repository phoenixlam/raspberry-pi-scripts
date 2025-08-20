#!/usr/bin/env python
# coding: utf-8
 
# # 9-2.无源蜂鸣器实验
# @  说明：无源蜂鸣器实验<br>
# 无源蜂鸣器实验，通过GPIOZero库的TonalBuzzer专用音频合成库直接驱动无源蜂鸣器发出具有频率信息的声音！！！<br>

# ## 1.导入必要的库文件

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
from signal import pause


# ## 2.定义无源蜂鸣器管脚

makerobo_Buzzer = 17    # 有源蜂鸣器管脚定义


# ## 3.音谱定义

# 音谱定义
Tone_CL = [220, 220, 220, 220, 220, 220, 220, 248]		# 低C音符的频率
Tone_CM = [220, 262, 294, 330, 350, 393, 441, 495]		# 中C音的频率
Tone_CH = [220, 525, 589, 661, 700, 786, 800, 880]		# 高C音符的频率

# 第一首歌音谱
makerobo_song_1 = [	Tone_CM[3], Tone_CM[5], Tone_CM[6], Tone_CM[3], Tone_CM[2], Tone_CM[3], Tone_CM[5], Tone_CM[6], 
			        Tone_CH[1], Tone_CM[6], Tone_CM[5], Tone_CM[1], Tone_CM[3], Tone_CM[2], Tone_CM[2], Tone_CM[3], 
			        Tone_CM[5], Tone_CM[2], Tone_CM[3], Tone_CM[3], Tone_CL[6], Tone_CL[6], Tone_CL[6], Tone_CM[1],
			        Tone_CM[2], Tone_CM[3], Tone_CM[2], Tone_CL[7], Tone_CL[6], Tone_CM[1], Tone_CL[5]	]
# 第1首歌的节拍，1表示1/8拍
makerobo_beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			
			        1, 1, 1, 1, 1, 1, 3, 1, 
			        1, 3, 1, 1, 1, 1, 1, 1, 
			        1, 2, 1, 1, 1, 1, 1, 1, 
			        1, 1, 3	]
# 第二首歌音谱
makerobo_song_2 = [	Tone_CM[1], Tone_CM[1], Tone_CM[1], Tone_CL[5], Tone_CM[3], Tone_CM[3], Tone_CM[3], Tone_CM[1],
			        Tone_CM[1], Tone_CM[3], Tone_CM[5], Tone_CM[5], Tone_CM[4], Tone_CM[3], Tone_CM[2], Tone_CM[2], 
			        Tone_CM[3], Tone_CM[4], Tone_CM[4], Tone_CM[3], Tone_CM[2], Tone_CM[3], Tone_CM[1], Tone_CM[1], 
			        Tone_CM[3], Tone_CM[2], Tone_CL[5], Tone_CL[7], Tone_CM[2], Tone_CM[1]	]

# 第2首歌的节拍，1表示1/8拍
makerobo_beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			
			        1, 1, 2, 2, 1, 1, 3, 1, 
			        1, 2, 2, 1, 1, 2, 2, 1, 
			        1, 2, 2, 1, 1, 3 ]


# ## 3.初始化工作

# GPIO设置函数
def makerobo_setup():
    global bz
    bz = TonalBuzzer(makerobo_Buzzer)  # 设置管脚
    bz.stop()


# ## 4.功能函数

# 循环函数
def makerobo_loop():
	while True:
		#    播放第一首歌音乐...
		for i in range(1, len(makerobo_song_1)):     # 播放第一首歌
			bz.play(Tone(makerobo_song_1[i]))              # 设置歌曲音符的频率
			sleep(makerobo_beat_1[i] * 0.5)	         # 延迟一个节拍* 0.5秒的音符
		sleep(1)						             # 等待下一首歌。

		#    播放第二首歌音乐...
		for i in range(1, len(makerobo_song_2)):     # 播放第二首歌
			bz.play(Tone(makerobo_song_2[i]))              # 设置歌曲音符的频率
			sleep(makerobo_beat_2[i] * 0.5)          # 延迟一个节拍* 0.5秒的音符

# 释放资源函数
def makerobo_destory():
	bz.stop()			    # 停止蜂鸣器


# ## 5.主程序

# 程序入口
if __name__ == '__main__':		
	makerobo_setup()
	try:
		makerobo_loop()
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行destroy()子程序。
		makerobo_destory()      # 释放资源
