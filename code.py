from pmk import PMK, number_to_xy, hsv_to_rgb
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import math
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

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
    [Keycode.SEVEN],
    [Keycode.EIGHT],
    [Keycode.NINE],
    [Keycode.A],
    [Keycode.B],
    [Keycode.GUI, Keycode.SHIFT, Keycode.F12],  # mute Teams
    [Keycode.GUI, Keycode.SHIFT, Keycode.F10],  # close Teams window/ end call
    [Keycode.E],
    [Keycode.GUI, Keycode.SHIFT, Keycode.F11]  # eject CIRCUITPY
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


#  keybow.led_sleep_enabled = True
#  keybow.led_sleep_time = 2
step = 0
rainbow_speed = 20  # normally 20, lower is faster

while True:
    keybow.update()
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
        keys[i].set_led(r/15, g/15, b/15)  # divide by makes keys less bright



"""

I imagine you've figured this out by now, but in case you haven't and someone else looks for this: I had the same struggle and with enough digging managed to figure a way of doing it. In your keymap you need to put multiple keycodes in a list (), and single keycodes in an array []. Then you need to use the * operator when passing to send method i.e. keyboard.send(*keycode)

"""
