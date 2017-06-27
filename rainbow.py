#!/usr/bin/env python
#from the Pimoroni blinkt libary - https://github.com/pimoroni/blinkt/blob/master/examples/rainbow.py
#Prerequisite :: sudo apt-get install python-blinkt

import colorsys
import time

import blinkt

spacing = 360.0 / 16.0
hue = 0

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

def rainbow_cycle():
    while True:
        hue = int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.001)

#rainbow_cycle()
