import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.nju6450.gpio import GPIO
from gfxlcd.driver.nju6450.nju6450 import NJU6450
RPi.GPIO.setmode(RPi.GPIO.BCM)

lcd = NJU6450(122, 32, GPIO())
lcd.rotation = 0
lcd.init()
lcd.auto_flush = False

lcd.draw_text(25, 1, "Star Wars")
lcd.draw_text(30, 10, "Death Star")

image_file = Image.open("assets/20x20.png")
lcd.threshold = 0

lcd.draw_image(0, 0, image_file)

lcd.flush(True)
