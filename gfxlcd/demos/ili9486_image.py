import RPi.GPIO
import sys
from PIL import Image
sys.path.append("../../")
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486
RPi.GPIO.setmode(RPi.GPIO.BCM)


drv = SPI()
lcd_tft = ILI9486(320, 480, drv)
#lcd_tft.rotation = 270
lcd_tft.init()

image_file = Image.open("assets/japan_temple_240x320.jpg")
lcd_tft.draw_image(0, 0, image_file)

numbers_image = Image.open("assets/dsp2017_101_64.png")
lcd_tft.transparency_color = (0, 0, 0)
lcd_tft.draw_image(10, 10, numbers_image)
