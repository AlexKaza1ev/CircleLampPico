import board
import neopixel
import digitalio
import time
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, AMBER, JADE, WHITE

# LED strip control pin
pixel_pin = board.GP27
# Number of pixels
pixel_num = 144
# Brightness button pin
bright_pin = board.GP12
# Mode control pin
mode_pin = board.GP13
# Mode variable : 0 = animation; 1 = light; 2 = off
mode = 1

# Buttons setup
button = digitalio.DigitalInOut(mode_pin)
button.switch_to_input(pull=digitalio.Pull.DOWN)

brightness_btn = digitalio.DigitalInOut(bright_pin)
brightness_btn.switch_to_input(pull=digitalio.Pull.DOWN)

# Animations setup
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)
sparkle_pulse = SparklePulse(pixels, speed=0.05, period=3, color=JADE)
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=AMBER)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=5, spacing=3)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=10)


animations = AnimationSequence(sparkle_pulse, comet, chase, rainbow_comet, rainbow_chase, rainbow_sparkle, advance_interval=10, auto_clear=True)

while True:
    animations.animate()
    if brightness_btn.value:
        xx = pixels.brightness
        xx += 0.1
        if (xx > 1):
            xx = 0.1
        pixels.brightness = xx
        if mode:
            pixels.show()
        time.sleep(.5)
    if button.value:
        mode = (mode + 1) % 3
        if mode == 0:
            animations.freeze()
            pixels.fill(WHITE)
            pixels.show()
        elif mode == 1:
            animations.resume()
        else:
            animations.freeze()
            pixels.fill((0, 0, 0))
            pixels.show()
        time.sleep(.5)


