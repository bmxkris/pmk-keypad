from pmk import PMK, number_to_xy, hsv_to_rgb
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import math
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

keybow = PMK(Hardware())
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap = [
    [Keycode.F13],
    [Keycode.F14],
    [Keycode.F15],
    [Keycode.F16],
    [Keycode.F17],
    [Keycode.F18],
    [Keycode.F19],
    [Keycode.GUI, Keycode.SHIFT, Keycode.F9],
    [], # modifier see code below!
    [Keycode.NINE],
    [Keycode.A],
    [Keycode.B],
    [Keycode.GUI, Keycode.SHIFT, Keycode.F12],  # mute Teams
    [Keycode.GUI, Keycode.SHIFT, Keycode.F10],  # close Teams window/ end call
    [Keycode.ALT, Keycode.GUI, Keycode.F1],     # sleep (see Custom shortcuts workflow in Alfred)
    [Keycode.GUI, Keycode.SHIFT, Keycode.F11]  # eject CIRCUITPY
]

numpad = [
    [],
    [Keycode.ONE],
    [Keycode.TWO],
    [Keycode.THREE],
    [],
    [Keycode.FOUR],
    [Keycode.FIVE],
    [Keycode.SIX],
    [], # modifier
    [Keycode.SEVEN],
    [Keycode.EIGHT],
    [Keycode.NINE],
    [],
    [],
    [Keycode.ZERO],
    [Keycode.C]
]
"""
    [Keycode.A],
    [Keycode.B],
    [Keycode.C],
    [Keycode.D],
    [Keycode.E],
    [Keycode.F],
    [Keycode.G],
    [Keycode.H],
    [Keycode.I],
    [Keycode.J],
    [Keycode.K],
    [Keycode.L],
    [Keycode.SHIFT, Keycode.M],  # mute Teams
    [Keycode.SHIFT, Keycode.N],  # close Teams window/ end call
    [Keycode.O],
    [Keycode.SHIFT, Keycode.P]  # eject CIRCUITPY
"""

modifier = keys[8]

def default_key_map():

    global keymap_default

    for key in keys:
        @keybow.on_press(key)
        def press_handler(key):
            print("Key {} pressed".format(key.number))
            key.set_led(0, 0, 255)
            keycode = keymap[key.number]
            keyboard.send(*keycode)

        @keybow.on_release(key)
        def release_handler(key):
            print("Key {} released".format(key.number))
            key.set_led(255, 0, 0)

    keymap_default = True
    set_modifier()

def numlock_key_map():

    global keymap_default

    for key in keys:
        @keybow.on_press(key)
        def press_handler(key):
            print("Key {} pressed".format(key.number))
            key.set_led(0, 0, 255)
            keycode = numpad[key.number]
            keyboard.send(*keycode)

    keymap_default = False
    set_modifier()

def set_modifier():
    @keybow.on_press(modifier)
    def press_handler(key):
        if keymap_default is True:
            numlock_key_map()
        else:
            default_key_map()


default_key_map()
keymap_default = True

#  keybow.led_sleep_enabled = True
#  keybow.led_sleep_time = 2
step = 0
rainbow_speed = 20  # normally 20, lower is faster
dullness = 10

while True:
    keybow.update()

    if keymap_default is False:
        # set the numbers to one colour
        for i in [1,2,3,5,6,7,9,10,11,14]:
            keys[i].set_led(10,10,20)

        # set the modifier to another colour
        modifier.set_led(100,10,10)

        # off the rest
        for j in [0,4,8,12,13,15]:
            keys[j].set_led(0,0,0)

    else:

        step += 1
        for i in range(16):
            # Convert the key number to an x/y coordinate to calculate the hue
            # in a matrix style-y.
            x, y = number_to_xy(i)

            # Calculate the hue.d
            hue = (x + y + (step / rainbow_speed)) / 11
            hue = hue - int(hue)
            hue = hue - math.floor(hue)

            # Convert the hue to RGB values.
            r, g, b = hsv_to_rgb(hue, 1, 1)

            # Display it on the key!
            keys[i].set_led(r/dullness, g/dullness, b/dullness)  # divide by makes keys less bright

