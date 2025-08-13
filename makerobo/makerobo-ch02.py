from gpiozero import RGBLED
from colorzero import Color
from time import sleep

colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']

led = RGBLED(red=17, green=18, blue=27)

def makerobo_loop():
    while True:
        for col in colors:
            led.color = Color(col)
            sleep(2)

def makerobo_destroy():
    led.close()

if __name__ == '__main__':
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    