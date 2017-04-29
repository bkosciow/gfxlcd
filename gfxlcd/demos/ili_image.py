import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
RPi.GPIO.setmode(RPi.GPIO.BCM)


lcd_tft = ILI9325(240, 320, ILIGPIO())
lcd_tft.init()

# bypass of missing +3v line to power backlight
LED = 6
RPi.GPIO.setup(LED, RPi.GPIO.OUT)
RPi.GPIO.output(LED, 1)

image_file = Image.open("assets/japan_temple_240x320.jpg")
lcd_tft.draw_image(0, 0, image_file)

numbers_image = Image.open("assets/dsp2017_101_64.png")
lcd_tft.transparency_color = (0, 0, 0)
lcd_tft.draw_image(10, 10, numbers_image)
