# Circuit Playground NeoPixel
import time
import board
from rainbowio import colorwheel
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixels_circuit = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pixels_neo = neopixel.NeoPixel(board.A2, 60, brightness=1, auto_write=False, pixel_order=neopixel.RGBW)

def rainbow(wait, pixels):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)
        for i in range(len(pixels_circuit)):
            idx = int(i + j)
            pixels_circuit[i] = colorwheel(idx & 255)
        pixels_circuit.show()
        time.sleep(wait)

while True:
    rainbow(0.1, pixels_neo)  # Increase the number to slow down the rainbow.
