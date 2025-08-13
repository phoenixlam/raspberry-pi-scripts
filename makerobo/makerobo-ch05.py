from gpiozero import LED
#from colorzero import Color
from time import sleep

#colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']

relaypin = LED(17)

def makerobo_setup():
    relaypin.off()

def makerobo_loop():
    while True:
        relaypin.on()
        sleep(2)
        relaypin.off()
        sleep(2)

def makerobo_destroy():
    relaypin.close()

if __name__ == '__main__':
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    