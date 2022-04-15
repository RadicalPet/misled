# Circuit Playground NeoPixel
import time
import board
from rainbowio import colorwheel
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixels_circuit = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pixels_neo = neopixel.NeoPixel(board.A2, 60, brightness=1, auto_write=False, pixel_order=neopixel.RGBW)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def rainbow_cycle(wait, pixels):
    for j in range(255):
        for i in range(len(pixels)):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def color_chase(color, wait, pixels):
    for i in range(len(pixels)):
        pixels[i] = color
        pixels[round(i/6)] = color
        time.sleep(wait)
        pixels.show()
        pixel.show()
    time.sleep(0.5)


def color_chase_demo(pixels):
    color_chase(RED, 0.1, pixels)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1, pixels)
    color_chase(GREEN, 0.1, pixels)
    color_chase(CYAN, 0.1, pixels)
    color_chase(BLUE, 0.1, pixels)
    color_chase(PURPLE, 0.1, pixels)
    color_chase(OFF, 0.1, pixels)

def rainbow(wait, pixels):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)

while True:
    #rainbow_cycle(0.03, pixels_circuit)
    rainbow(0.03, pixels_neo)
    
