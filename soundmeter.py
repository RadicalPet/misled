import array
import math
import audiobusio
import board
import neopixel
import time

import adafruit_fancyled.adafruit_fancyled as fancy

#from adafruit_circuitplayground import cp


FANCY_CHSV_RED = 0
FANCY_CHSV_YELLOW = 1/6
FANCY_CHSV_GREEN = 1/3
FANCY_CHSV_CYAN = 1/2
FANCY_CHSV_BLUE = 2/3
FANCY_CHSV_PURPLE = 5/6

# Set up NeoPixels and turn them all off.
pixels_circuit = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pixels_neo = neopixel.NeoPixel(board.A2, 60, brightness=1, auto_write=False, pixel_order=neopixel.RGBW)
pixels = pixels_neo


def fancy_palette(pixels, start, end):
    palette = list()
    reverse = False

    if start > end:
        unit = (start-end) / len(pixels)
        reverse = True

    else:
        unit = (end-start) / len(pixels)

    if reverse:
        for i in range(len(pixels)):
            palette.append(fancy.CHSV(start - unit*i, 1.0, 1.0).pack())
        return palette

    for i in range(len(pixels)):
        palette.append(fancy.CHSV(start + unit*i, 1.0, 1.0).pack())
    return palette


# Color of the peak pixel.
PEAK_COLOR = (0,0,0)
# Number of total pixels - 10 build into Circuit Playground
NUM_PIXELS = 60

# Exponential scaling factor.
# Should probably be in range -10 .. 10 to be reasonable.
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

# Number of samples to read at once.
NUM_SAMPLES = 160


# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)


def volume_color(volume):
    return 200, volume * (255 // NUM_PIXELS), 0


# Main program

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
# Set lowest level to expect, plus a little.
input_floor = normalized_rms(samples) + 10
# OR: used a fixed floor
# input_floor = 50

# You might want to print the input_floor to help adjust other values.
# print(input_floor)

# Corresponds to sensitivity: lower means more pixels light up with lower sound
# Adjust this as you see fit.
input_ceiling = input_floor + 500

peak = 0

def blink_circuit():
    #cp.play_file("shutup.wav")
    pixels_circuit.fill((255, 0, 0))
    pixels_circuit.show()
    time.sleep(0.02)
    pixels_circuit.fill(0)
    pixels_circuit.show()
    time.sleep(0.02)


while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    # You might want to print this to see the values.
    # print(magnitude)

    # Compute scaled logarithmic reading in the range 0 to NUM_PIXELS
    c = log_scale(constrain(magnitude, input_floor, input_ceiling),
                  input_floor, input_ceiling, 0, NUM_PIXELS)

    # Light up pixels that are below the scaled and interpolated magnitude.
    pixels.fill(0)
    palette = fancy_palette(pixels, FANCY_CHSV_RED, FANCY_CHSV_GREEN)
    max_volume = len(pixels) - 2
    max_reached = False
    for i in range(NUM_PIXELS):
        if c > max_volume:
            max_reached = True
        if i < c:
            pixels[i] = palette[i]
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, NUM_PIXELS - 1)
        elif peak > 0:
            peak = peak - 1

        #if peak > 0:
        #    pixels[int(peak)] = (255, 0, 0)
    pixels.show()
    if max_reached:
        for i in range(5):
            blink_circuit()
