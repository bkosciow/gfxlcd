import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ili9325.gpio import GPIO as ILIGPIO
from gfxlcd.driver.ili9325.ili9325 import ILI9325
RPi.GPIO.setmode(RPi.GPIO.BCM)

drv = ILIGPIO()
drv.pins['LED'] = 6
drv.pins['CS'] = 18
lcd = ILI9325(240, 320, drv)
lcd.rotation = 0
lcd.init()
lcd.auto_flush = False

lcd.color = (255, 255, 255)
lcd.draw_text(25, 1, "Star Wars")
lcd.draw_text(30, 10, "Death Star")

image_file = Image.open("assets/20x20.png")
lcd.transparency_color = (0, 0, 0)

lcd.draw_image(0, 0, image_file)
