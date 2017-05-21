import RPi.GPIO
import sys
import random
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450
RPi.GPIO.setmode(RPi.GPIO.BCM)


lcd_nju = NJU6450(122, 32, GPIO())
lcd_nju.init()
lcd_nju.auto_flush = False

image_file = Image.open("assets/dsp2017_122_29.png")
# lcd_nju.threshold = 50
# lcd_nju.transparency_color = [110, 57]
lcd_nju.draw_image(0, 0, image_file)

lcd_nju.flush(True)
