from gpiozero import PWMLED
from time import sleep

colors = [0xFF00, 0x00FF, 0x0FF0, 0xF00F]
makerobo_pins = (17, 18)

# xxx Hz = xxx / 1s
p_R = PWMLED(makerobo_pins[0], initial_value=0, frequency=2000)
p_G = PWMLED(makerobo_pins[1], initial_value=0, frequency=2000)

def makerobo_pwm_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_set_Color(col):
    R_val = col >> 8
    G_val = col & 0x00FF
    R_val = makerobo_pwm_map(R_val, 0, 255, 0, 100)
    G_val = makerobo_pwm_map(G_val, 0, 255, 0, 100)
    print (f'Setting color R: {R_val}, G: {G_val}')
    p_R.value = (R_val) / 100.0
    p_G.value = (G_val) / 100.0

def makerobo_loop():
    while True:
        for col in colors:
            makerobo_set_Color(col)
            sleep(0.5)

def makerobo_destroy():
    p_R.close()
    p_G.close()

if __name__ == '__main__':
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    