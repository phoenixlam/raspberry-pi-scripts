from gpiozero import LED
from gpiozero import Button
#from colorzero import Color
from time import sleep
from signal import pause

btn = Button(17)
p_R = LED(18)
p_G = LED(27)

def pressed():
    p_R.on()
    p_G.off()
    print("Button pressed!")

def released():
    p_R.off()
    p_G.on()
    print("Button released!")

btn.when_pressed = pressed
btn.when_released = released

#def makerobo_setup():
#    relaypin.off()

def makerobo_loop():
    pause() # Keeps the program running

def makerobo_destroy():
    p_R.close()
    p_G.close()

if __name__ == '__main__':
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    