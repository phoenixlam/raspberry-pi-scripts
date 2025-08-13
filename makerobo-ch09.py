from gpiozero import LED
from gpiozero import Button
from gpiozero import Buzzer
#from colorzero import Color
from time import sleep
from signal import pause

#btn = Button(17)
#p_R = LED(18)
#p_G = LED(27)

def makerobo_setup():
    global bz
    bz = Buzzer(17, active_high=False)
    bz.off()
    
def beep():
    bz.on()
    sleep(0.5)
    bz.off()    
    sleep(0.5)

    

def loop():
    while True:
        beep()

def makerobo_destroy():
    bz.close()


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    